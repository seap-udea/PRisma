"""Pre-compute the inverse-CDF grid of the ``rho_true`` prior.

Nested sampling encodes the prior as a *prior transform* that maps the unit interval to
the parameter via the inverse CDF. For the ``rho_star,true`` parameter the prior is an
empirical KDE over external stellar-density samples (Berger et al. 2023 for Kepler-51),
whose inverse CDF has no closed form. Evaluating it by integrating the KDE on the fly at
every live-point proposal is far too slow, so we tabulate it **once** on a grid and
interpolate during sampling.

This module implements exactly the (previously commented-out) tabulation block from the
inference notebooks, as a reusable function and a small CLI::

    python -m photoring.rho_cdf pipeline/kepler_51/inputs/rho_true_data/rho_true_samples.dat

writes ``rho_grid_cdf.txt`` (two columns: ``rho_grid_gcc  rho_cdf``) next to the samples.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.stats import gaussian_kde


def make_rho_cdf(rho_true_gcc_samples, n_grid=20000):
    """Tabulate the normalised inverse-CDF grid of a KDE over ``rho_true`` samples.

    Parameters
    ----------
    rho_true_gcc_samples : array_like
        1-D samples of the star's true density [g/cm^3].
    n_grid : int
        Number of grid points spanning ``[min, max]`` of the samples.

    Returns
    -------
    rho_grid : ndarray
        Density grid [g/cm^3], shape ``(n_grid,)``.
    rho_cdf : ndarray
        Corresponding CDF values in ``[0, 1]`` (monotone), shape ``(n_grid,)``.
        In the prior transform, ``rho_true = interp(u, rho_cdf, rho_grid)``.
    """
    samples = np.asarray(rho_true_gcc_samples, dtype=float).ravel()
    kde = gaussian_kde(samples)
    rho_min = float(samples.min())
    rho_max = float(samples.max())
    rho_grid = np.linspace(rho_min, rho_max, int(n_grid))
    rho_cdf = np.array([float(kde.integrate_box_1d(rho_min, x)) for x in rho_grid])
    rho_cdf = (rho_cdf - rho_cdf[0]) / (rho_cdf[-1] - rho_cdf[0])
    return rho_grid, rho_cdf


def save_rho_cdf(rho_grid, rho_cdf, path):
    """Write the ``(rho_grid, rho_cdf)`` table to ``path`` (header ``rho_grid_gcc  rho_cdf``)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savetxt(path, np.column_stack([rho_grid, rho_cdf]),
               header="rho_grid_gcc  rho_cdf")
    return path


def load_rho_cdf(path):
    """Load a pre-computed ``(rho_grid, rho_cdf)`` table written by :func:`save_rho_cdf`."""
    loaded = np.loadtxt(path, skiprows=1)
    return loaded[:, 0], loaded[:, 1]


def build_from_samples_file(samples_path, out_path=None, n_grid=20000, kgm3=True):
    """Read ``rho_true`` samples, tabulate the inverse CDF, and write it out.

    Parameters
    ----------
    samples_path : str or Path
        File with one column of ``rho_true`` samples.
    out_path : str or Path, optional
        Output path. Defaults to ``rho_grid_cdf.txt`` next to ``samples_path``.
    n_grid : int
        Grid resolution.
    kgm3 : bool
        If ``True`` (default), the input samples are in kg/m^3 and are converted to g/cm^3
        (divide by 1000) before tabulation — matching the pipeline's internal units.
    """
    samples_path = Path(samples_path)
    samples = np.loadtxt(samples_path)
    if kgm3:
        samples = samples / 1000.0
    rho_grid, rho_cdf = make_rho_cdf(samples, n_grid=n_grid)
    if out_path is None:
        out_path = samples_path.with_name("rho_grid_cdf.txt")
    save_rho_cdf(rho_grid, rho_cdf, out_path)
    return out_path


def _main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(
        description="Tabulate the inverse-CDF grid of the rho_true prior.")
    ap.add_argument("samples", type=Path,
                    help="File with one column of rho_true samples.")
    ap.add_argument("-o", "--out", type=Path, default=None,
                    help="Output path (default: rho_grid_cdf.txt next to samples).")
    ap.add_argument("-n", "--n-grid", type=int, default=20000,
                    help="Grid resolution (default 20000).")
    ap.add_argument("--gcc", action="store_true",
                    help="Samples are already in g/cm^3 (skip kg/m^3 -> g/cm^3).")
    args = ap.parse_args(argv)
    out = build_from_samples_file(args.samples, args.out, n_grid=args.n_grid,
                                  kgm3=not args.gcc)
    print(f"rho_cdf written -> {out}")


if __name__ == "__main__":
    _main()
