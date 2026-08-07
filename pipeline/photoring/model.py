"""``PhotoRingModel`` — the statistical model tying data, priors, forward model and KDE
likelihood together for both samplers.

This object replaces the tangle of module-level globals and inline closures the inference
notebooks used to carry (``P_fixed``, ``_kde``, ``PARAM_NAMES``, ``exorings_model``,
``prior_transform``, ``log_prob`` …). It is constructed once from a case's data and the
run configuration, and then exposes the callables the samplers need:

- :meth:`PhotoRingModel.prior_transform` — unit-cube -> parameters (``dynesty``).
- :meth:`PhotoRingModel.log_prior`, :meth:`PhotoRingModel.log_prob` — explicit prior /
  posterior (``emcee``).
- :meth:`PhotoRingModel.log_likelihood` — KDE likelihood (both).
- :meth:`PhotoRingModel.forward` / :meth:`PhotoRingModel.unpack` — forward-model dispatch.

The numerics are a faithful port of the (previously duplicated) inline notebook code; the
only intentional change is that the two forward models are *imported* from the
:mod:`exorings` and :mod:`geotrans` packages instead of being redefined per notebook.
"""

from __future__ import annotations

import numpy as np
from scipy.stats import truncnorm as _truncnorm
from scipy.stats import gaussian_kde

from exorings.forward import forward_observables, forward_observables_legacy
from geotrans.model import geotrans2_model

from .likelihood import OBS_MAP, build_kde, validate_observables
from .priors import build_param_space

FLOAT_TINY = np.finfo(float).tiny


class PhotoRingModel:
    """Ring-geometry retrieval model for one planet / one run configuration.

    Parameters
    ----------
    ttv : dict
        TTV observable arrays, keyed ``delta, T14, T23, rho_obs_gcc, b, p, P_days``.
    rho_true_gcc_samples : array_like
        Samples of the star's true density [g/cm^3] (empirical ``rho_true`` prior).
    model_config : dict
        The ``MODEL_CONFIG`` dict from the notebooks (flags + fixed values).
    kde_config : dict
        The ``KDE_CONFIG`` dict: ``observables``, ``N_KDE``, ``seed_kde``.
    rho_grid, rho_cdf : array_like, optional
        Pre-computed inverse-CDF grid for the ``rho_true`` prior transform (needed by
        ``dynesty`` when ``RHO_TRUE_FREE``). See :mod:`photoring.rho_cdf`.
    p_fixed : float, optional
        Orbital period [days] held fixed in the forward model. Defaults to the median of
        ``ttv['P_days']``.
    """

    def __init__(self, ttv, rho_true_gcc_samples, model_config, kde_config,
                 rho_grid=None, rho_cdf=None, p_fixed=None):
        self.ttv = ttv
        self.model_config = dict(model_config)
        self.kde_config = dict(kde_config)
        self.rho_true_gcc_samples = np.asarray(rho_true_gcc_samples, dtype=float).ravel()

        self.OBS_MAP = OBS_MAP
        self.observables = validate_observables(kde_config["observables"])

        self.P_fixed = float(p_fixed) if p_fixed is not None else float(np.median(ttv["P_days"]))

        # ── b prior ───────────────────────────────────────────────────────
        self.B_FREE = bool(model_config["B_FREE"])
        self.B_FIXED = float(model_config["B_FIXED"])
        self.B_SIGMA = float(model_config["B_SIGMA"])
        _b_a = (0.0 - self.B_FIXED) / self.B_SIGMA
        _b_b = (1.0 - self.B_FIXED) / self.B_SIGMA
        self.b_prior_dist = _truncnorm(_b_a, _b_b, loc=self.B_FIXED, scale=self.B_SIGMA)

        # ── rho_true prior ────────────────────────────────────────────────
        self.RHO_TRUE_FREE = bool(model_config["RHO_TRUE_FREE"])
        self.rho_true_prior_kde = gaussian_kde(self.rho_true_gcc_samples)
        self.RHO_TRUE_MIN = float(self.rho_true_gcc_samples.min())
        self.RHO_TRUE_MAX = float(self.rho_true_gcc_samples.max())
        self.RHO_TRUE_MEAN = float(np.mean(self.rho_true_gcc_samples))
        self.RHO_TRUE_STD = float(np.std(self.rho_true_gcc_samples))
        _rtf = model_config.get("RHO_TRUE_FIXED", None)
        self.RHO_TRUE_FIXED = float(_rtf) if _rtf is not None else self.RHO_TRUE_MEAN
        self.rho_grid = None if rho_grid is None else np.asarray(rho_grid, dtype=float)
        self.rho_cdf = None if rho_cdf is None else np.asarray(rho_cdf, dtype=float)

        # ── alpha prior (optional, uniform on (0, 1]) ────────────────────────
        self.ALPHA_FIXED = float(model_config.get("ALPHA_FIXED", np.exp(-1.0)))  # equiv. tau=1
        self.ALPHA_FREE = bool(model_config.get("ALPHA_FREE", False))
        self.ALPHA_LO = float(model_config.get("ALPHA_PRIOR_LO", 0.0))  # excluded (alpha>0)
        self.ALPHA_HI = float(model_config.get("ALPHA_PRIOR_HI", 1.0))  # included
        if self.ALPHA_FREE:
            assert 0.0 <= self.ALPHA_LO < self.ALPHA_HI <= 1.0

        # ── other fixed / derived ─────────────────────────────────────────
        self.FI_FIXED = float(model_config["FI_FIXED"])
        self.FE_MAX = float(model_config["FE_MAX"])
        self.p_mean_ref = float(model_config["p_mean_ref"])
        self.p_min = float(model_config["p_prior_lo"]) * self.p_mean_ref
        self.p_max = float(model_config["p_prior_hi"]) * self.p_mean_ref

        self.P_FREE = bool(model_config.get("P_FREE", True))
        self.P_FIXED_VALUE = float(model_config.get("P_FIXED_VALUE", self.p_min))  # used only when P_FREE is False

        self.FORWARD_MODEL = str(model_config.get("FORWARD_MODEL", "exorings")).lower()
        assert self.FORWARD_MODEL in ("exorings", "exorings_legacy", "geotrans"), \
            f"FORWARD_MODEL must be 'exorings', 'exorings_legacy' or 'geotrans', got '{self.FORWARD_MODEL}'"
        self.bobs_method = str(model_config.get("BOBS_METHOD", "kipping")).lower()

        # ── parameter space ───────────────────────────────────────────────
        self.PARAM_NAMES, self.PARAM_LABELS = build_param_space(model_config)
        self.NDIM = len(self.PARAM_NAMES)

        # ── KDE likelihood ────────────────────────────────────────────────
        self.kde, self.idx_train, self.train_emp = build_kde(
            ttv, self.observables,
            n_kde=kde_config["N_KDE"], seed_kde=kde_config["seed_kde"],
        )

    # ── run tag ───────────────────────────────────────────────────────────
    def free_tag(self):
        """Suffix encoding which optional parameters are free (matches run_sweep)."""
        parts = ""
        if self.RHO_TRUE_FREE:
            parts += "_rhoFREE"
        if self.B_FREE:
            parts += "_bFREE"
        if self.ALPHA_FREE:
            parts += "_alphaFREE"
        if self.P_FREE:
            parts += "_pFREE"
        return parts

    # ── forward model dispatch ─────────────────────────────────────────────
    def forward(self, params_dict):
        """Evaluate the selected forward model, resolving fixed b / rho_true / alpha / p."""
        rho_val = params_dict.get("rho_true", self.RHO_TRUE_FIXED)
        b_val = params_dict.get("b", self.B_FIXED)
        alpha_val = params_dict.get("alpha", self.ALPHA_FIXED)
        p_val = params_dict["p"] if self.P_FREE else self.P_FIXED_VALUE

        kwargs = dict(
            rhotrue_gcc=float(rho_val),
            P_days=self.P_fixed,
            b=float(b_val),
            p=float(p_val),
            fi=self.FI_FIXED,
            fe=float(params_dict["fe"]),
            alpha=float(alpha_val),
            theta_deg=float(params_dict["theta"]),
            ir_deg=float(params_dict["ir"]),
        )
        if self.FORWARD_MODEL == "geotrans":
            return geotrans2_model(**kwargs)
        elif self.FORWARD_MODEL == "exorings_legacy":
            return forward_observables_legacy(bobs_method=self.bobs_method, **kwargs)
        return forward_observables(bobs_method=self.bobs_method, **kwargs)

    def unpack(self, params):
        """Map a 1-D parameter array to a name->value dict."""
        return dict(zip(self.PARAM_NAMES, params))

    # ── prior transform (dynesty) ───────────────────────────────────────────
    def prior_transform(self, u):
        """Map the unit hypercube ``[0,1]^NDIM`` to physical parameters (nested sampling)."""
        i = 0
        fe = self.FI_FIXED + u[i] * (self.FE_MAX - self.FI_FIXED); i += 1
        ir_deg = np.degrees(np.arccos(np.clip(1.0 - u[i], -1.0, 1.0))); i += 1
        theta_deg = u[i] * 90.0; i += 1

        out = [fe, ir_deg, theta_deg]
        if self.P_FREE:
            p = self.p_min + u[i] * (self.p_max - self.p_min); i += 1
            out.append(p)

        if self.ALPHA_FREE:
            # alpha ~ Uniform(ALPHA_LO, ALPHA_HI)  (default: Uniform(0, 1))
            # We use a half-open interval: alpha in (ALPHA_LO, ALPHA_HI]
            alpha = self.ALPHA_LO + u[i] * (self.ALPHA_HI - self.ALPHA_LO); i += 1
            out.append(alpha)

        if self.RHO_TRUE_FREE:
            if self.rho_grid is None or self.rho_cdf is None:
                raise RuntimeError(
                    "prior_transform needs rho_grid/rho_cdf when RHO_TRUE_FREE. "
                    "Build them with photoring.rho_cdf and pass to PhotoRingModel.")
            rho_true = float(np.interp(u[i], self.rho_cdf, self.rho_grid)); i += 1
            out.append(rho_true)

        if self.B_FREE:
            b = float(self.b_prior_dist.ppf(np.clip(u[i], 1e-6, 1 - 1e-6))); i += 1
            out.append(b)

        return np.array(out)

    # ── explicit prior / posterior (emcee) ──────────────────────────────────
    def log_prior(self, params):
        """Explicit log-prior for MCMC. Returns ``-inf`` outside the support."""
        d = self.unpack(params)
        fe, ir_deg, theta_deg = d["fe"], d["ir"], d["theta"]

        if fe <= self.FI_FIXED or fe > self.FE_MAX:
            return -np.inf
        if ir_deg <= 0.0 or ir_deg >= 90.0:
            return -np.inf
        if theta_deg < 0.0 or theta_deg > 90.0:
            return -np.inf
        if "p" in d:
            if d["p"] < self.p_min or d["p"] > self.p_max:
                return -np.inf

        log_p = float(np.log(np.sin(ir_deg * np.pi / 180) + 1e-12))  # isotropic prior on iR

        if self.ALPHA_FREE:
            alpha = float(d["alpha"])
            if alpha <= self.ALPHA_LO or alpha > self.ALPHA_HI:
                return -np.inf
            # Uniform prior on (ALPHA_LO, ALPHA_HI]: flat contribution, no term needed
            # (the log-prior contribution is -log(ALPHA_HI - ALPHA_LO), a constant)

        if self.RHO_TRUE_FREE:
            rho = d["rho_true"]
            if rho < self.RHO_TRUE_MIN or rho > self.RHO_TRUE_MAX:
                return -np.inf
            log_p += float(np.log(float(self.rho_true_prior_kde(np.array([rho]))[0]) + 1e-300))

        if self.B_FREE:
            b = d["b"]
            if b < 0.0 or b > 1.0:
                return -np.inf
            log_p += float(self.b_prior_dist.logpdf(b))

        return log_p

    def log_likelihood(self, params):
        """Evaluate the KDE at the forward-model outputs for ``params``."""
        res = self.forward(self.unpack(params))
        if res is None:
            return -np.inf
        eval_vec = []
        for key in self.observables:
            _, model_key, _, _, _ = self.OBS_MAP[key]
            val = res[model_key]
            # Forward can return NaN (e.g. Kipping b_obs when contact geometry is
            # undefined); that must not reach gaussian_kde.
            if val is None or not np.isfinite(val):
                return -np.inf
            eval_vec.append(float(val))
        dens = self.kde(np.asarray(eval_vec, dtype=float).reshape(-1, 1))
        d = float(dens[0])
        if not np.isfinite(d):
            return -np.inf
        # A density underflowing to 0 keeps the finite log(FLOAT_TINY) floor:
        # nested sampling then exits on a detectable plateau instead of stalling
        # forever looking for live points with finite log-likelihood.
        return float(np.log(max(d, FLOAT_TINY)))

    def log_prob(self, params):
        """Log-posterior = log-prior + log-likelihood (MCMC target)."""
        lp = self.log_prior(params)
        if not np.isfinite(lp):
            return -np.inf
        return lp + self.log_likelihood(params)
