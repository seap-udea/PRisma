"""Transit-observable derivation from a TTV-fit posterior (pipeline step 1).

Converts posterior samples of ``(Rp/R*, rho_star, b, P)`` from a light-curve / TTV fit
into the full set of transit observables ``(delta, a/R*, T14, T23, b, i_orb, P)`` that the
photo-ring likelihood consumes, following the Zuluaga et al. (2015) / Kipping (2014)
asterodensity-profiling formalism (Eqs. 1-4).

All derivations are **deterministic transforms** of the posterior columns: the spread of
the resulting observable samples inherits the full covariance of the photometric fit, so
no error-propagation formula is needed.

This module holds the functions that used to be defined inline in ``01_observables.ipynb``
(``load_posterior`` and ``derive_observables``), unchanged, so the notebook becomes a thin
guide that imports them.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

# Physical constants (must match exorings.py / the forward model exactly).
GCONST = 6.67428e-11   # m^3 kg^-1 s^-2
DAY = 86400.0          # s
HOUR = 3600.0          # s
DEG = np.pi / 180

# Column order of the derived-observables ``.dat`` files written by the pipeline.
OBS_COLUMNS = ["p", "delta", "aR", "rho_obs", "P", "b", "i_orb", "T14", "T23"]

# Header written at the top of each derived-observables file.
OBS_HEADER = (
    "# Transit observable posteriors (photo-ring pipeline, step 1)\n"
    "# Derived from a TTV-fit MCMC posterior via asterodensity profiling (Zuluaga+2015 Eq.1-4)\n"
    "#\n"
    "# Columns:\n"
    "#   p        : Rp/R*          [dimensionless]\n"
    "#   delta    : transit depth  [dimensionless = (Rp/R*)^2]\n"
    "#   aR       : a/R*           [dimensionless]\n"
    "#   rho_obs  : stellar density [kg/m^3]\n"
    "#   P        : orbital period [days]\n"
    "#   b        : impact param   [R*]\n"
    "#   i_orb    : inclination    [degrees]\n"
    "#   T14      : total duration [hours]\n"
    "#   T23      : full duration  [hours]\n"
)


def load_posterior(path, col_p=0, col_rho=1, col_b=2, col_per=3, col_tmid=4, col_logl=-1):
    """Load a raw TTV-fit posterior table (e.g. a MultiNest ``post_equal_weights.dat``).

    Parameters
    ----------
    path : str or Path
        File with whitespace-separated posterior samples.
    col_p, col_rho, col_b, col_per, col_tmid, col_logl : int
        Column indices for ``Rp/R*``, ``rho_star [kg/m^3]``, impact parameter,
        orbital period [days], mid-transit time, and log-likelihood (last column by
        default). Adjust these to match your own TTV output format.

    Returns
    -------
    pandas.DataFrame
        Columns ``p, rho_obs, b, P_days, T_mid, logL``.
    """
    data = np.loadtxt(path)
    df = pd.DataFrame({
        "p":       data[:, col_p],       # Rp/R*
        "rho_obs": data[:, col_rho],     # kg/m^3
        "b":       data[:, col_b],
        "P_days":  data[:, col_per],
        "T_mid":   data[:, col_tmid],
        "logL":    data[:, col_logl],
    })
    return df


def derive_observables(df):
    """Compute all transit observables from TTV posterior columns.

    Parameters
    ----------
    df : pandas.DataFrame
        Must contain columns ``p, rho_obs, b, P_days`` (and, if present, ``logL`` is
        carried through). ``rho_obs`` is the transit-inferred stellar density [kg/m^3].

    Returns
    -------
    pandas.DataFrame
        Columns ``p, delta, rho_obs, aR, P, b, i_orb, T14, T23, logL``. Rows that fail
        the transit-validity gate are set to ``NaN`` in the geometry-dependent columns.

    Notes
    -----
    ``delta = p^2``;   ``a/R* = (G rho_obs P^2 / 3pi)^(1/3)``;
    ``T14/23 = P/pi * arcsin( sqrt[ ((1 +/- p)^2 - b^2) / ((a/R*)^2 - b^2) ] )``;
    ``i_orb = arccos(b / (a/R*))``.
    """
    p = df["p"].values
    rho_obs = df["rho_obs"].values
    b = df["b"].values
    # Raw TTV posteriors name the period column 'P_days'; this function's own output
    # names it 'P', so accept either and stay re-appliable to a combined posterior.
    if "P_days" in df:
        P_days = df["P_days"].values
    elif "P" in df:
        P_days = df["P"].values
    else:
        raise KeyError("derive_observables needs a period column named 'P_days' or 'P'")
    P_s = P_days * DAY

    # ── Observable 1: transit depth ───────────────────────────────────────
    delta = p**2

    # ── Observable 2: scaled semimajor axis ───────────────────────────────
    aR = (GCONST * rho_obs / (3 * np.pi) * P_s**2)**(1 / 3)

    # ── Validity gate ─────────────────────────────────────────────────────
    denom = aR**2 - b**2            # must be > 0
    num14 = (1 + p)**2 - b**2       # must be > 0
    num23 = (1 - p)**2 - b**2       # must be > 0
    valid = (denom > 0) & (num14 > 0) & (num23 > 0) & (b < aR)

    arg14 = np.where(valid, np.sqrt(num14 / denom), np.nan)
    arg23 = np.where(valid, np.sqrt(num23 / denom), np.nan)
    arg14 = np.clip(arg14, 0, 1)
    arg23 = np.clip(arg23, 0, 1)

    # ── Observable 3: T14, T23 [hours] ────────────────────────────────────
    T14 = np.where(valid, P_days / np.pi * np.arcsin(arg14) * 24, np.nan)
    T23 = np.where(valid, P_days / np.pi * np.arcsin(arg23) * 24, np.nan)

    # ── Observable 4: orbital inclination [deg] ───────────────────────────
    cosiorb = np.clip(b / aR, -1 + 1e-10, 1 - 1e-10)
    i_orb = np.arccos(cosiorb) / DEG

    n_invalid = int((~valid).sum())
    if n_invalid > 0:
        print(f"  WARNING: {n_invalid} samples ({n_invalid / len(df) * 100:.1f}%) "
              f"failed the transit-validity check -- set to NaN")

    return pd.DataFrame({
        "p":       p,
        "delta":   delta,
        "rho_obs": rho_obs,
        "aR":      aR,
        "P":       P_days,
        "b":       b,
        "i_orb":   i_orb,
        "T14":     T14,
        "T23":     T23,
        "logL":    df["logL"].values if "logL" in df else np.nan,
    })


# ══════════════════════════════════════════════════════════════════════════
#  Combining independent posteriors of the same planet
# ══════════════════════════════════════════════════════════════════════════
# A planet with many observed epochs can make a single nested-sampling run
# intractable, because every epoch contributes its own mid-transit time as a free
# parameter. The workaround is to split the light curve into independent temporal
# segments, fit each separately, and combine the resulting posteriors afterwards.
#
# Those segments constrain *the same* transit-shape parameters, so the combined
# posterior is their **product**, not their union. Concatenating them ("pooling")
# would instead give the average of the segments, and keeping only one segment
# would throw away most of the data — neither is a valid combination. Importance
# sampling against the pooled proposal is the only method used here.

#: Parameters combined in the product. These are the *native* TTV-fit quantities;
#: every other observable is derived afterwards, from the combined samples.
SEGMENT_NATIVE_KEYS = ["p", "rho_obs", "b"]


def effective_sample_size(w):
    """Kish effective sample size of (unnormalised) importance weights."""
    w = np.asarray(w, dtype=float)
    w = w / w.sum()
    return float(1.0 / np.sum(w**2))


def weight_diagnostics(w, label="", verbose=True):
    """Report how concentrated a set of importance weights is.

    A small effective sample size relative to the proposal size means a few samples
    carry almost all the weight, and the combined posterior is correspondingly noisy.

    Returns
    -------
    dict
        ``n_eff, n_total, frac, n50, n90`` — the last two being how many samples carry
        50% / 90% of the total weight.
    """
    w = np.asarray(w, dtype=float)
    w_n = w / w.sum()
    n_total = len(w_n)
    n_eff = 1.0 / np.sum(w_n**2)

    cumw = np.cumsum(np.sort(w_n)[::-1])
    n50 = int(np.searchsorted(cumw, 0.50)) + 1
    n90 = int(np.searchsorted(cumw, 0.90)) + 1
    frac = n_eff / n_total

    if verbose:
        flag = "LOW ESS -- combination unreliable" if frac < 0.01 else "ok"
        print(f"  [{label}]")
        print(f"    N_eff = {n_eff:.0f} / {n_total}  ({100 * frac:.1f}%)  {flag}")
        print(f"    50% of the weight in the top {n50} samples ({100 * n50 / n_total:.1f}%)")
        print(f"    90% of the weight in the top {n90} samples ({100 * n90 / n_total:.1f}%)")
    return dict(n_eff=float(n_eff), n_total=n_total, frac=float(frac), n50=n50, n90=n90)


def drop_invalid(seg, keys=None):
    """Keep only rows where the native parameters *and* the derived durations are finite."""
    keys = list(keys or SEGMENT_NATIVE_KEYS)
    check_cols = [c for c in keys + ["T14", "T23"] if c in seg.columns]
    return seg[seg[check_cols].notna().all(axis=1)].reset_index(drop=True)


def segment_tension(segments, keys=None, verbose=True):
    """Pairwise tension between segments, in sigma, per native parameter.

    Tension is ``|median_i - median_j| / sqrt(std_i^2 + std_j^2)``. Values above ~2
    sigma flag a systematic inconsistency between epochs rather than statistical
    scatter — for Kepler-51 b this is expected in the durations and the inferred
    density, because different stretches of the light curve sample different stages of
    the system's dynamical evolution (large-amplitude TTVs).

    Returns
    -------
    dict
        ``{param: {"i-j": tension}}``.
    """
    keys = list(keys or SEGMENT_NATIVE_KEYS)
    pairs = [(i, j) for i in range(len(segments)) for j in range(i + 1, len(segments))]
    out = {}
    if verbose:
        header = "  ".join(f"{f'{i+1}v{j+1}':>9s}" for i, j in pairs)
        print(f"  {'Param':10s}  {header}")
    for k in keys:
        row = {}
        cells = []
        for i, j in pairs:
            dm = abs(segments[i][k].median() - segments[j][k].median())
            ds = np.sqrt(segments[i][k].std()**2 + segments[j][k].std()**2)
            t = float(dm / ds) if ds > 0 else np.inf
            row[f"{i+1}-{j+1}"] = t
            cells.append(f"{t:.2f}s{'  !' if t > 2 else '   '}")
        out[k] = row
        if verbose:
            print(f"  {k:10s}  " + "  ".join(f"{c:>9s}" for c in cells))
    if verbose:
        print("\n  Tension > 2 sigma indicates a systematic difference between epochs\n"
              "  (e.g. starspots, or TTVs sampling different dynamical states).")
    return out


def combine_segments(segments, keys=None, seed=42, n_draw=None, verbose=True):
    """Combine independent posteriors of one planet by importance sampling.

    The segments constrain the same parameters, so the target is the **product** of
    their densities. That product is estimated by importance sampling: the pooled
    samples act as the proposal, each is weighted by the product of every segment's KDE
    evaluated there, and the weighted set is resampled to equal weight.

    Steps
    -----
    1. Drop rows that failed the transit-validity gate.
    2. Report pairwise tension between segments (:func:`segment_tension`).
    3. Standardise the pooled native parameters — they span several orders of magnitude
       (``p ~ 0.07`` vs ``rho_obs ~ 2000``), and Scott's-rule bandwidths assume
       comparable scales.
    4. Fit one Gaussian KDE per segment in that standardised space.
    5. Weight every pooled sample by ``prod_k p_k(theta)``, computed as a sum of
       log-densities and shifted by its maximum for numerical stability.
    6. Report the effective sample size, overall and for each pair of segments (which
       identifies the segment most in tension with the rest).
    7. Resample with replacement to equal weight.
    8. Re-derive the observables **from the combined native parameters**, so
       ``delta``/``aR``/``T14``/``T23`` stay mutually consistent — deriving them before
       combining would break that.

    Parameters
    ----------
    segments : sequence of pandas.DataFrame
        Output of :func:`derive_observables` per segment. A single segment is returned
        cleaned and unchanged (nothing to combine).
    keys : list of str, optional
        Native parameters spanning the KDE space. Defaults to
        :data:`SEGMENT_NATIVE_KEYS`.
    seed : int
        Seed for the resampling draw, so the combined posterior is reproducible.
    n_draw : int, optional
        Number of resampled draws. Defaults to the effective sample size, which avoids
        inflating the apparent precision of the combined posterior.

    Returns
    -------
    tuple(pandas.DataFrame, dict)
        The combined observables and a diagnostics dict (``n_eff``, ``tension``,
        ``pair_ess``, ``n_draw``, ``bandwidths``).
    """
    from scipy.stats import gaussian_kde

    keys = list(keys or SEGMENT_NATIVE_KEYS)
    segs = [drop_invalid(s, keys) for s in segments]

    if verbose:
        print("=" * 62)
        print(f"  Combining {len(segs)} segment(s) by importance sampling")
        print("=" * 62)
        for i, s in enumerate(segs, 1):
            print(f"  Segment {i}: {len(s)} valid samples")

    if len(segs) == 1:
        if verbose:
            print("  Single segment -- nothing to combine.")
        out = segs[0].dropna().reset_index(drop=True)
        return out, dict(n_eff=float(len(out)), n_draw=len(out), tension={}, pair_ess={})

    if verbose:
        print("\n-- Consistency: pairwise tension between segments " + "-" * 12)
    tension = segment_tension(segs, keys, verbose=verbose)

    # ── Proposal: the pooled samples ──────────────────────────────────────
    pooled = pd.concat(segs, ignore_index=True)
    X_all = pooled[keys].values.T
    g_mean = X_all.mean(axis=1, keepdims=True)
    g_std = X_all.std(axis=1, keepdims=True)

    def _standardize(X):
        return (X - g_mean) / g_std

    if verbose:
        print(f"\n-- {len(keys)}-D KDE per segment in standardised native space " + "-" * 8)
    kdes = [gaussian_kde(_standardize(s[keys].values.T)) for s in segs]
    bandwidths = [float(k.factor) for k in kdes]
    if verbose:
        for i, k in enumerate(kdes, 1):
            print(f"  Segment {i}: Scott bandwidth h={k.factor:.4f}  (n={k.n}, d={k.d})")

    # ── Importance weights = product of the segment densities ─────────────
    X_pool = _standardize(pooled[keys].values.T)
    log_ps = [k.logpdf(X_pool) for k in kdes]
    log_w = np.sum(log_ps, axis=0)
    log_w -= log_w.max()
    w = np.exp(log_w)
    w /= w.sum()

    if verbose:
        print("\n-- Weight diagnostics " + "-" * 40)
    diag = weight_diagnostics(w, label=f"Product of {len(segs)} segments", verbose=verbose)
    n_eff = diag["n_eff"]

    pair_ess = {}
    if verbose:
        print("\n  Pairwise ESS (identifies the segment most in tension):")
    for i in range(len(segs)):
        for j in range(i + 1, len(segs)):
            lw = log_ps[i] + log_ps[j]
            lw -= lw.max()
            wp = np.exp(lw)
            wp /= wp.sum()
            ne = effective_sample_size(wp)
            pair_ess[f"{i+1}-{j+1}"] = ne
            if verbose:
                print(f"    Segments {i+1}+{j+1}: N_eff = {ne:.0f}/{len(pooled)} "
                      f"({100 * ne / len(pooled):.1f}%)")

    # ── Resample to equal weight ──────────────────────────────────────────
    n_draw = int(n_draw or min(int(n_eff), len(pooled)))
    if verbose and n_eff < 500:
        print(f"\n  WARNING: N_eff={n_eff:.0f} < 500 -- the combined posterior may be "
              f"noisy.\n  Check the tensions above before trusting it.")
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(pooled), size=n_draw, replace=True, p=w)
    native = pooled.iloc[idx].reset_index(drop=True)

    # ── Re-derive observables from the combined native parameters ─────────
    combined = derive_observables(native).dropna().reset_index(drop=True)

    if verbose:
        print("\n-- Combined posterior " + "-" * 40)
        print(f"  Samples: {len(combined)}  (input N_eff = {n_eff:.0f})")
        for name, vals, unit in [("delta [ppm]", combined["delta"] * 1e6, ""),
                                 ("T14 [h]", combined["T14"], ""),
                                 ("T23 [h]", combined["T23"], ""),
                                 ("rho_obs [g/cm^3]", combined["rho_obs"] / 1000.0, ""),
                                 ("b", combined["b"], ""),
                                 ("a/R*", combined["aR"], "")]:
            lo, med, hi = np.percentile(vals, [16, 50, 84])
            print(f"  {name:18s}: {med:.4g}  +{hi - med:.3g} / -{med - lo:.3g}")

    return combined, dict(n_eff=n_eff, n_draw=n_draw, tension=tension,
                          pair_ess=pair_ess, bandwidths=bandwidths)


def save_observables(obs_df, path):
    """Write a derived-observables table to ``path`` in the pipeline's ``.dat`` format.

    Drops rows with NaN, writes the columns of :data:`OBS_COLUMNS` with the standard
    :data:`OBS_HEADER`, and returns the written array.
    """
    from pathlib import Path
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data_out = obs_df[OBS_COLUMNS].dropna().values
    header_line = OBS_HEADER + "# " + "  ".join(f"{k:>12s}" for k in OBS_COLUMNS)
    np.savetxt(path, data_out, fmt=["%.8f"] * len(OBS_COLUMNS),
               header=header_line, comments="")
    return data_out
