"""Samplers and posterior post-processing for the ring-geometry retrieval.

Thin, reusable drivers around :class:`~photoring.model.PhotoRingModel`:

- :func:`run_dynesty` — static nested sampling (evidence + posterior).
- :func:`run_emcee` — ensemble MCMC (posterior).
- :func:`compute_ppc` — propagate posterior draws through the forward model for the PPC.
- :func:`posterior_stats` — median / 16-84 percentile summary per parameter.

All numerics are ported from the inference notebooks; the model callables are passed to
the samplers so the same code path serves any run configuration.
"""

from __future__ import annotations

import time

import numpy as np


# ── posterior statistics ────────────────────────────────────────────────────
def posterior_stats(chain, param_names):
    """Return ``{name: {mean, std, median, p16, p84}}`` for a posterior chain."""
    out = {}
    for i, name in enumerate(param_names):
        v = chain[:, i]
        out[name] = dict(mean=float(np.mean(v)), std=float(np.std(v)),
                         median=float(np.median(v)),
                         p16=float(np.percentile(v, 16)), p84=float(np.percentile(v, 84)))
    return out


# ── posterior predictive check ──────────────────────────────────────────────
def compute_ppc(model, chain, n_ppc=2500, seed=888):
    """Propagate posterior draws through the forward model.

    Returns
    -------
    ndarray, shape (N_valid, 5)
        Columns ``[delta, T14, T23, rhoobs, bobs]`` for each valid draw.
    """
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(chain), size=min(n_ppc, len(chain)), replace=False)
    rows = []
    for i in idx:
        res = model.forward(model.unpack(chain[i]))
        if res is None:
            continue
        rows.append([res["delta"], res["T14"], res["T23"], res["rhoobs"], res["bobs"]])
    return np.asarray(rows)


# ── dynesty (nested sampling) ────────────────────────────────────────────────
def run_dynesty(model, ns_config, ctx=None, verbose=True):
    """Run static nested sampling with ``dynesty``.

    Parameters
    ----------
    model : PhotoRingModel
    ns_config : dict
        ``nlive, sample, dlogz, seed, use_pool, n_procs``.
    ctx : multiprocessing context, optional
        Used to build the worker pool when ``use_pool`` and ``n_procs > 1``.
    """
    import dynesty
    from dynesty import NestedSampler
    from dynesty import utils as dyfunc

    def _run(seed, pool=None):
        rng_ns = np.random.default_rng(seed)
        n_procs = ns_config["n_procs"] if pool is not None else 1
        sampler = NestedSampler(
            model.log_likelihood, model.prior_transform, ndim=model.NDIM,
            nlive=ns_config["nlive"], sample=ns_config["sample"],
            rstate=rng_ns, pool=pool, queue_size=n_procs,
        )
        t0 = time.time()
        sampler.run_nested(dlogz=ns_config["dlogz"], print_progress=verbose)
        runtime = time.time() - t0
        dres = sampler.results
        weights = np.exp(dres.logwt - dres.logz[-1])
        weights /= weights.sum()
        chain = dyfunc.resample_equal(dres.samples, weights)
        return dict(dres=dres, chain=chain,
                    logz=float(dres.logz[-1]), logz_err=float(dres.logzerr[-1]),
                    n_iter=len(dres.samples), runtime_s=float(runtime))

    if ns_config.get("use_pool") and ns_config.get("n_procs", 1) > 1:
        if ctx is None:
            import multiprocessing as mp
            try:
                ctx = mp.get_context("fork")
            except ValueError:
                ctx = mp
        with ctx.Pool(processes=ns_config["n_procs"]) as pool:
            result = _run(ns_config["seed"], pool=pool)
    else:
        result = _run(ns_config["seed"], pool=None)

    result["stats"] = posterior_stats(result["chain"], model.PARAM_NAMES)
    return result


# ── emcee (ensemble MCMC) ────────────────────────────────────────────────────
def init_walkers(model, nwalkers, rng):
    """Sample initial walker positions from the prior, rejecting ``-inf`` log-prob draws."""
    p0 = []
    n_tries = 0
    while len(p0) < nwalkers:
        n_tries += 1
        _fe = rng.uniform(model.FI_FIXED + 0.01, model.FE_MAX)
        _ir = rng.uniform(5.0, 89.0)
        _th = rng.uniform(0.0, 90.0)
        _p = rng.uniform(model.p_min, model.p_max)
        vals = [_fe, _ir, _th, _p]
        if model.ALPHA_FREE:
            # alpha ~ Uniform(ALPHA_LO, ALPHA_HI); default (0, 1]
            vals.append(float(rng.uniform(max(model.ALPHA_LO, 1e-6), model.ALPHA_HI)))
        if model.RHO_TRUE_FREE:
            vals.append(float(np.clip(
                model.RHO_TRUE_MEAN + rng.normal(0.0, 0.2 * model.RHO_TRUE_STD),
                model.RHO_TRUE_MIN, model.RHO_TRUE_MAX)))
        if model.B_FREE:
            vals.append(float(np.clip(rng.normal(model.B_FIXED, 0.5 * model.B_SIGMA), 0.0, 1.0)))
        params = np.array(vals)
        if np.isfinite(model.log_prob(params)):
            p0.append(params)
        if n_tries > 100_000:
            raise RuntimeError("Could not initialise walkers — check priors / forward model.")
    return np.asarray(p0)


def run_emcee(model, mcmc_config, ctx=None, verbose=True):
    """Run ensemble MCMC with ``emcee``.

    Parameters
    ----------
    model : PhotoRingModel
    mcmc_config : dict
        ``nwalkers, nsteps, burnin, thin, seed, use_pool, n_procs``.
    ctx : multiprocessing context, optional
        Used to build the worker pool when ``use_pool`` and ``n_procs > 1``.
    """
    import emcee

    def _run(pool=None):
        rng = np.random.default_rng(mcmc_config["seed"])
        p0 = init_walkers(model, mcmc_config["nwalkers"], rng)
        # Differential-evolution ensemble moves (robust for multimodal / correlated
        # posteriors); overridable via MCMC_CONFIG['moves'].
        moves = mcmc_config.get("moves") or [
            (emcee.moves.DEMove(), 0.8),
            (emcee.moves.DESnookerMove(), 0.2),
        ]
        sampler = emcee.EnsembleSampler(
            mcmc_config["nwalkers"], p0.shape[1], model.log_prob,
            pool=pool, moves=moves)
        t0 = time.time()
        sampler.run_mcmc(p0, mcmc_config["nsteps"], progress=verbose)
        runtime = time.time() - t0
        chain_raw = sampler.get_chain()
        logprob_raw = sampler.get_log_prob()
        chain = sampler.get_chain(discard=mcmc_config["burnin"],
                                  thin=mcmc_config["thin"], flat=True)
        logprob = sampler.get_log_prob(discard=mcmc_config["burnin"],
                                       thin=mcmc_config["thin"], flat=True)
        acc_frac = float(np.mean(sampler.acceptance_fraction))
        return dict(chain=chain, logprob=logprob, chain_raw=chain_raw,
                    logprob_raw=logprob_raw, acc_frac=acc_frac, runtime_s=float(runtime))

    if mcmc_config.get("use_pool") and mcmc_config.get("n_procs", 1) > 1:
        if ctx is None:
            try:
                import multiprocess as mp
            except ImportError:
                import multiprocessing as mp
            try:
                ctx = mp.get_context("fork")
            except (AttributeError, ValueError):
                ctx = mp
        with ctx.Pool(processes=mcmc_config["n_procs"]) as pool:
            result = _run(pool=pool)
    else:
        result = _run(pool=None)

    result["stats"] = posterior_stats(result["chain"], model.PARAM_NAMES)
    return result
