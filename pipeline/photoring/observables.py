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
    P_days = df["P_days"].values
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
