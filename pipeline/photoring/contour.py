"""The Photo-Ring effect across ring orientations.

Maps the Photo-Ring bias

.. math:: PR \\equiv 10\\,\\log_{10}(\\rho_{\\star,\\rm obs} / \\rho_{\\star,\\rm true})

over the plane of *effective* ring orientation — projected inclination
:math:`i_{\\rm R}` and projected tilt :math:`\\theta_{\\rm R}` — for a fixed planet and
ring size. It answers the question the inference cannot: *which* ring orientations
produce the density anomaly actually observed, and which produce none at all.

Two features of the resulting map matter physically:

- the **PR = 0 locus**, where a ringed planet mimics a ringless one exactly: the rings
  bias depth and durations in compensating directions, so the inferred stellar density
  comes out right despite the rings being there. A null result in asterodensity
  profiling therefore does not exclude rings;
- the **sign** of PR. Most orientations give ``PR < 0`` (an underestimated density);
  only a comparatively small region gives ``PR > 0``. A target whose observed anomaly is
  positive is thus confined to a restricted part of orientation space — which is what
  makes the observed anomaly informative about the geometry.

The bias is computed with the independent, numerically-integrated ``geotrans`` model
(exact contact times and blocked areas) rather than the pipeline's closed-form
``exorings`` model, because here accuracy matters more than speed: this is a one-off
grid, not a likelihood evaluated millions of times.
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm

from . import plotting as _plot

# Solar / terrestrial reference values, in the unit system geotrans2 uses (SI).
_MSUN = 1.98855e30      # kg
_RSUN = 6.96342e8       # m
_MEARTH = 5.9722e24     # kg
_REARTH = 6.371e6       # m
_AU = 1.495978707e11    # m


def planet_radius_ratio(Rp_earth, Rstar_sun):
    """``p = Rp/R*`` from a planet radius in Earth radii and a stellar radius in solar radii."""
    return (Rp_earth * _REARTH) / (Rstar_sun * _RSUN)


def default_system(*, Rp_earth=1.9, Rstar_sun=0.87, rho_star=1.896, P_days=45.155,
                   b=0.0, fi=1.0, fe=2.0, tau=1.0):
    """Build a ``geotrans`` ringed system for the PR map.

    Defaults describe a **Kepler-51 b analogue**: a compact planet of ``Rp_earth`` Earth
    radii — the small, dense planet the photo-ring hypothesis implies, rather than the
    inflated radius a ringless fit returns — orbiting the real Kepler-51 host at planet
    b's period.

    ``geotrans`` works in normalised units (``R* = 1``), so the system is specified
    by the *true* stellar density, the period, the impact parameter and ``p = Rp/R*``;
    no absolute stellar mass or radius is needed. ``Rstar_sun`` is used only to convert
    ``Rp_earth`` into ``p``.

    Parameters
    ----------
    Rp_earth : float
        Planet radius [R_earth].
    Rstar_sun : float
        Host radius [R_sun], used to form ``p``.
    rho_star : float
        The star's *true* mean density [g/cm^3] — the reference PR is measured against.
    P_days, b : float
        Orbital period [days] and impact parameter [R_star].
    fi, fe : float
        Inner / outer ring radius [R_p]. ``fi=1`` puts the ring's inner edge at the
        planet's surface (photometry cannot resolve anything interior to that).
    tau : float
        Ring normal optical depth.
    """
    import geotrans.geotrans as gt

    return gt.RingedSystem(dict(
        p=planet_radius_ratio(Rp_earth, Rstar_sun),
        rhotrue=rho_star, P=P_days, b=b,
        fe=fe, fi=fi, tau=tau,
        ir=0.0, theta=0.0, ep=0.0, wp=0.0, fp=0.0,
    ))


def compute_pr_map(system, *, n_cos_ir=81, n_theta=73, cos_ir_min=0.01, cos_ir_max=1.0,
                   theta_min_deg=0.0, theta_max_deg=90.0):
    """Evaluate PR (and the ring-only transit depth) over the orientation grid.

    For every ``(cos i_R, theta_R)`` the ring's projected ellipse is re-oriented, the
    contact times and blocked area are computed numerically, and the stellar density a
    standard ringless fit *would* infer from those observables is compared against the
    system's true density.

    Returns
    -------
    tuple
        ``(COS_IR, THETA_deg, PR, DELTA_RING)`` — all ``(n_theta, n_cos_ir)`` arrays.
        ``PR`` is in decibel-like units, ``10 log10(rho_obs/rho_true)``;
        ``DELTA_RING`` is the ring's own contribution to the transit depth.
    """
    import geotrans.geotrans as gt

    ringed = gt.copyObject(system)
    ringed.noauto = True   # freeze auto-recompute while we sweep the orientation
    P_hours = ringed.Porb / 3600.0
    rho_true = ringed.rho_true      # kg/m^3, set by derivedSystemProperties

    cos_irs = np.linspace(cos_ir_min, cos_ir_max, n_cos_ir)
    thetas = np.linspace(np.radians(theta_min_deg), np.radians(theta_max_deg), n_theta)
    COS_IR, THETA = np.meshgrid(cos_irs, thetas)
    PR = np.zeros_like(COS_IR, dtype=float)
    DELTA = np.zeros_like(COS_IR, dtype=float)

    for i, cos_ir in enumerate(cos_irs):
        ieff = np.arccos(cos_ir)
        ringed.ieff = ieff
        ringed.block = gt.blockFactor(ringed.tau, ieff)
        # Foreshorten both ring edges for this effective inclination.
        ringed.Ringext.b = ringed.Ringext.a * np.cos(ieff)
        ringed.Ringint.b = ringed.Ringint.a * np.cos(ieff)

        for j, theta in enumerate(thetas):
            for fig in (ringed.Ringext, ringed.Ringint):
                fig.cost = np.cos(theta)
                fig.sint = np.sin(theta)

            tcs = gt.contactTimes(ringed)
            tT = (tcs[-1] - tcs[1]) / 3600.0      # total duration  [h]
            tF = (tcs[-2] - tcs[2]) / 3600.0      # flat duration   [h]

            area = gt.ringedPlanetArea(ringed)
            p_obs = area / np.pi                   # depth a ringless fit would measure
            rp = ringed.Planet.a
            delta_ring = (area - np.pi * rp**2) / np.pi
            if cos_ir < 1e-10:                     # exactly edge-on: no projected ring
                delta_ring = 0.0

            # Normalised units (R* = 1), so no stellar radius is needed here.
            rho_obs, _a_obs, _b_obs = gt.rhoObserved_Seager(p_obs, tT, tF, P_hours)
            PR[j, i] = 10.0 * np.log10(rho_obs / rho_true)
            DELTA[j, i] = delta_ring

    return COS_IR, np.degrees(THETA), PR, DELTA


def _soft_diverging_cmap(base="RdBu", soften=0.50, n=256):
    """``base`` blended towards white, so the filled map stays readable under contours."""
    cols = plt.colormaps[base](np.linspace(0, 1, n))
    cols[:, :3] = cols[:, :3] * (1 - soften) + soften  # blend towards white
    return LinearSegmentedColormap.from_list(f"soft_{base}", cols)


def plot_pr_contour(COS_IR, THETA, Z, system=None, *, highlight=None, draw_zero=True,
                    cbar_label=None, n_levels=9, fmt="%.2f", title=None,
                    draw_planets=True, paths=None, run_tag=None, figure_type="observables",
                    out_path=None):
    """Filled contour map of the PR bias over ring orientation.

    Parameters
    ----------
    highlight : float, optional
        Draw a thick dashed contour at this PR value — used to mark the anomaly actually
        measured for the target, so one can read off which orientations reproduce it.
    draw_zero : bool
        Emphasise the ``PR = 0`` contour (the density-degeneracy locus).
    draw_planets : bool
        Overlay small ring/planet sketches on a grid, showing the geometry each region of
        the map corresponds to.
    out_path : str or Path, optional
        Explicit output file. Takes precedence over ``paths``/``run_tag``.
    """
    import geotrans.geotrans as gt

    vmin, vmax = float(np.nanmin(Z)), float(np.nanmax(Z))
    diverging = vmin < 0.0 < vmax
    if diverging:
        norm = TwoSlopeNorm(vmin=vmin, vcenter=0.0, vmax=vmax)
        cmap = _soft_diverging_cmap()
    else:
        norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
        cmap = plt.get_cmap("Blues")

    fig, ax = plt.subplots(figsize=(_plot.STYLE["fig_w_ppc"] * 1.9,
                                    _plot.STYLE["fig_h_single"] * 1.7),
                           constrained_layout=True)
    ax.contourf(COS_IR, THETA, Z, levels=np.linspace(vmin, vmax, 256),
                cmap=cmap, norm=norm, antialiased=True)

    levels = np.linspace(vmin, vmax, n_levels)
    cs = ax.contour(COS_IR, THETA, Z, levels=levels, colors="black",
                    linewidths=0.8, alpha=0.7)
    labels = ax.clabel(cs, fmt=fmt, fontsize=_plot.STYLE["annot_size"] + 3.5,
                       inline=True, inline_spacing=4)
    for lab in labels:
        lab.set_fontweight("bold")

    if draw_zero and diverging:
        ax.contour(COS_IR, THETA, Z, levels=[0.0], colors="black", linewidths=2.5)
    if highlight is not None and vmin < highlight < vmax:
        ax.contour(COS_IR, THETA, Z, levels=[highlight], colors="red",
                   linewidths=2.5, linestyles="--")

    if draw_planets and system is not None:
        gt.plotPlanets(ax, system,
                       xmin=float(COS_IR.min()), scalex=float(np.ptp(COS_IR)),
                       ymin=float(THETA.min()), scaley=float(np.ptp(THETA)))

    ax.set_xlabel(r"$\cos\,i_{\rm R}$", fontsize=_plot.STYLE["label_size"] + 3)
    ax.set_ylabel(r"$\theta_{\rm R}$", fontsize=_plot.STYLE["label_size"] + 3)
    ax.tick_params(direction="out", length=4, width=1)
    ax.grid(True, alpha=0.3, color="gray", linestyle="--")
    if title:
        ax.set_title(title, fontsize=_plot.STYLE["title_size"], fontweight="bold")

    cbar = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax,
                        pad=0.02, ticks=levels)
    cbar.set_label(cbar_label or
                   r"$PR\equiv 10\log_{10}(\rho_{\star,\rm obs}/\rho_{\star,\rm true})$",
                   fontsize=_plot.STYLE["label_size"])
    cbar.ax.tick_params(direction="out")

    if out_path is not None:
        from pathlib import Path
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_path, dpi=_plot.STYLE["fig_dpi"])
        print(f"  Saved -> {out_path}")
    elif run_tag:
        _plot._save(fig, run_tag, paths, figure_type)
    return fig
