"""Reproduce Zuluaga et al. (2015) Figure 3 — contour panel only.

Design goals (per request):
- Keep `overleaf/scripts/` clean: only `.py` files, no `tmp/`, no `figures/`, no `__pycache__/`.
- Save the figure directly into `overleaf/img/` as PNG.
- Generate a redesigned, modernized contour plot (not just a colormap swap).

Output:
- `overleaf/img/PhotoRingContour.png`

Run:
- `cd overleaf/scripts && PYTHONDONTWRITEBYTECODE=1 python3 reproduce_figure3.py`
"""

from __future__ import annotations

import os
import sys

sys.dont_write_bytecode = True

import numpy as np
from matplotlib import colors
from matplotlib import pyplot as plt

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from geotrans import *  # noqa: F401,F403
from system import System


def compute_photoring_contour(
    ringed_system,
    *,
    cieff_min: float = 0.01,
    cieff_max: float = 1.0,
    n_cieff: int = 81,
    teff_min: float = 0.0 * DEG,
    teff_max: float = 90.0 * DEG,
    n_teff: int = 73,
):
    ringed = copyObject(ringed_system)

    # Transit/orbit scalings (same definitions as the original code)
    P = ringed.Porb / HOUR
    rho_true = ringed.Mstar / (4 * pi / 3 * ringed.Rstar**3)

    cieffs = np.linspace(cieff_min, cieff_max, n_cieff)
    teffs = np.linspace(teff_min, teff_max, n_teff)

    CI, TH = np.meshgrid(cieffs, teffs)  # TH in radians
    PR = np.zeros_like(CI, dtype=float)
    Delta = np.zeros_like(CI, dtype=float)

    for i_idx, ci in enumerate(cieffs):
        ieff = arccos(ci)
        ringed.ieff = ieff
        ringed.block = blockFactor(ringed.tau, ieff)

        # Update ring projected semiminor axis for this effective inclination
        ringed.Ringext.b = ringed.Ringext.a * cos(ieff)
        ringed.Ringint.b = ringed.Ringint.a * cos(ieff)

        for t_idx, teff in enumerate(teffs):
            # Update ring tilt orientation
            ringed.Ringext.cost = cos(teff)
            ringed.Ringext.sint = sin(teff)
            ringed.Ringint.cost = cos(teff)
            ringed.Ringint.sint = sin(teff)

            # Numerical contact times
            tcsp = contactTimes(ringed)
            tT = (tcsp[-1] - tcsp[1]) / HOUR
            tF = (tcsp[-2] - tcsp[2]) / HOUR

            # Transit depth proxy p = A_RP / pi (same as original)
            p = ringedPlanetArea(ringed) / pi
            
            # Transit depth delta: ring contribution only
            # Calculate as total area minus planet area
            rp = ringed.Planet.a
            asp = pi * rp**2
            aring = ringedPlanetArea(ringed) - asp
            delta = aring / pi
            
            # Edge-on configuration: no projected ring area
            if ci < 1e-10:  # cos(ieff) ≈ 0 when ieff ≈ 90°
                delta = 0.0

            # PhotoRing ratio: rho_obs / rho_true
            rho_ratio = rhoObserved_Seager(p, ringed.Rstar, tT, tF, P) / rho_true
            PR[t_idx, i_idx] = log10(rho_ratio)
            Delta[t_idx, i_idx] = delta

    return CI, TH, PR, Delta, ringed


def plot_contour(CI, TH, Z, ringed, *, out_path: str, cbar_label: str, draw_zero: bool = False, fmt="%.2f"):
    # Matplotlib-only styling (bold and white background)
    plt.style.use('default')
    plt.rcParams.update(
        {
            "figure.dpi": 150,
            "savefig.dpi": 300,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.alpha": 0.3,
            "grid.color": "gray",
            "grid.linestyle": "--",
            "axes.labelsize": 16,
            "axes.titlesize": 18,
            "axes.titleweight": "bold",
            "xtick.labelsize": 12,
            "ytick.labelsize": 12,
            "font.family": "serif",
        }
    )

    fig, ax = plt.subplots(figsize=(8, 6), constrained_layout=True)

    vmin, vmax = float(np.nanmin(Z)), float(np.nanmax(Z))
    if vmin < 0.0 < vmax:

        from matplotlib import colors

        norm = colors.TwoSlopeNorm(vmin=vmin, vcenter=0.0, vmax=vmax)
        # cmap = plt.get_cmap("RdBu_r")

        from matplotlib.colors import LinearSegmentedColormap

        # 1. Get 256 colors from the original intense RdBu colormap
        original_cmap = plt.colormaps['RdBu']
        colors = original_cmap(np.linspace(0, 1, 256))

        # 2. Blend it with white (e.g., 50% original color + 50% pure white)
        soften_factor = 0.50 
        white = np.ones_like(colors)
        soft_colors = colors * (1 - soften_factor) + white * soften_factor

        # 3. Rebuild the new, muted colormap
        cmap = LinearSegmentedColormap.from_list("soft_RdBu", soft_colors)

    else:
        norm = colors.Normalize(vmin=vmin, vmax=vmax)
        cmap = plt.get_cmap("Blues")

    # Smooth field rendering (no blocky cells): filled contours with many levels
    filled_levels = np.linspace(vmin, vmax, 256)
    cf = ax.contourf(
        CI,
        TH * RAD,
        Z,
        levels=filled_levels,
        cmap=cmap,
        norm=norm,
        antialiased=True,
    )

    levels = np.linspace(vmin, vmax, 9)
    cs = ax.contour(CI, TH * RAD, Z, levels=levels, colors="black", linewidths=0.8, alpha=0.7)
    labels = ax.clabel(cs, fmt=fmt, fontsize=11, inline=True, inline_spacing=4)
    # Give the labels bold text to make them more legible
    for label in labels:
        label.set_fontweight("bold")
    
    if draw_zero and (vmin < 0.0 < vmax):
        ax.contour(CI, TH * RAD, Z, levels=[0.0], colors="black", linewidths=2.5, linestyles="-")

    # Keep the ring/planet glyphs (as in original Figure 3)
    plotPlanets(
        ax,
        ringed,
        xmin=float(np.nanmin(CI)),
        scalex=float(np.nanmax(CI) - np.nanmin(CI)),
        ymin=float(np.nanmin(TH) * RAD),
        scaley=float((np.nanmax(TH) - np.nanmin(TH)) * RAD),
    )

    ax.set_xlim(float(np.nanmin(CI)), float(np.nanmax(CI)))
    ax.set_ylim(float(np.nanmin(TH) * RAD), float(np.nanmax(TH) * RAD))
    # Text must match the original Figure 3 exactly
    ax.set_xlabel(r"$\cos\,i_{\rm  R}$")
    ax.set_ylabel(r"$\theta_{\rm R}$")
    ax.set_title("\n", pad=10)
    ax.tick_params(direction="out", length=4, width=1)

    cbar = fig.colorbar(cf, ax=ax, pad=0.02)
    cbar.set_label(cbar_label)
    cbar.ax.tick_params(direction="out", length=3, width=1)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)


def main():
    CI, TH, PR, Delta, ringed = compute_photoring_contour(System)
    
    out_path_pr = os.path.join(_HERE, "..", "img", "PhotoRingContour.png")
    plot_contour(CI, TH, PR, ringed, out_path=out_path_pr, cbar_label=r"$PR\equiv\log_{10}(\rho_{\star,\rm obs}/\rho_{\star,\rm true})$", draw_zero=True)
    
    out_path_delta = os.path.join(_HERE, "..", "img", "TransitDepthContour.png")
    plot_contour(CI, TH, Delta, ringed, out_path=out_path_delta, cbar_label=r"$\delta_{\rm Ring}$", draw_zero=False, fmt="%g")


if __name__ == "__main__":
    main()
