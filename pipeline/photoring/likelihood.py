"""Empirical KDE likelihood over transit observables.

The photo-ring likelihood is a Gaussian kernel-density estimate (KDE) trained on the
TTV-fit posterior of a user-selected subset of transit observables. Evaluating the KDE at
the observables predicted by the forward model for a proposed ring geometry gives the
likelihood of that geometry.

This module provides:

- :data:`OBS_MAP` — the metadata table linking each observable *key* to its column in the
  TTV posterior, the corresponding forward-model output key, and display metadata.
- :func:`build_kde` — build the joint KDE and the (display-scaled) training histograms
  used by the KDE self-consistency check.
"""

from __future__ import annotations

import numpy as np
from scipy.stats import gaussian_kde

# key -> (TTV_dict_column, forward_output_key, plot_label, display_scale, display_unit)
OBS_MAP = {
    "delta":   ("delta",       "delta",  r"$\delta$",                    1e6, "ppm"),
    "T14":     ("T14",         "T14",    r"$T_{14}$ [h]",                1.0, "h"),
    "T23":     ("T23",         "T23",    r"$T_{23}$ [h]",                1.0, "h"),
    "rho_obs": ("rho_obs_gcc", "rhoobs", r"$\rho_{\star,obs}$ [g/cm$^3$]", 1.0, "g/cm3"),
    "b_obs":   ("b",           "bobs",   r"$b_{\mathrm{obs}}$",          1.0, ""),
}

VALID_OBSERVABLES = tuple(OBS_MAP.keys())


def validate_observables(observables):
    """Assert that ``observables`` is a non-empty, duplicate-free subset of the valid keys."""
    valid = set(OBS_MAP)
    chosen = list(observables)
    assert len(chosen) >= 1, "Need at least 1 observable"
    assert all(k in valid for k in chosen), f"Unknown observable. Valid: {sorted(valid)}"
    assert len(chosen) == len(set(chosen)), "Duplicate observables"
    return chosen


def build_kde(ttv, observables, n_kde=5000, seed_kde=123):
    """Build the joint KDE likelihood from the TTV posterior.

    Parameters
    ----------
    ttv : dict
        TTV observable arrays, keyed by the *TTV column* names in :data:`OBS_MAP`
        (``delta, T14, T23, rho_obs_gcc, b, ...``).
    observables : list of str
        Observable keys entering the likelihood (subset of :data:`VALID_OBSERVABLES`).
    n_kde : int
        Number of posterior samples to train the KDE on (random subsample without
        replacement; use all samples if fewer are available).
    seed_kde : int
        RNG seed for the training subsample (and, via ``+1``, the resample check).

    Returns
    -------
    kde : scipy.stats.gaussian_kde
        Joint KDE over the chosen observables (in the order of ``observables``).
    idx_train : ndarray
        Indices of the training subsample.
    train_emp : dict
        ``{obs_key: display-scaled training vector}`` for the self-consistency check.
    """
    observables = validate_observables(observables)
    rng_kde = np.random.default_rng(seed_kde)
    n_obs = len(ttv["delta"])
    idx_train = (rng_kde.choice(n_obs, size=min(n_kde, n_obs), replace=False)
                 if n_kde is not None and n_kde < n_obs else np.arange(n_obs))

    train_rows = []
    train_emp = {}
    for key in observables:
        ttv_col, _, _, scale, _ = OBS_MAP[key]
        vec = np.asarray(ttv[ttv_col])[idx_train]
        train_rows.append(vec)
        train_emp[key] = vec * scale

    kde = gaussian_kde(np.vstack(train_rows))
    return kde, idx_train, train_emp
