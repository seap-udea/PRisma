"""Publication-ready plotting for the Photo-Ring pipeline.

This is the single, consistent home for every figure the pipeline produces. It adopts the
publication style of the results/observables notebooks (a configurable pastel palette,
serif typography, in/out-of-likelihood colour coding, PPC goodness-of-fit statistics),
so that the quick diagnostics that used to live inline in the inference notebooks and the
final figures share one look — consistent per planet / case.

Design
------
- One mutable :data:`STYLE` dict controls all aesthetics; call :func:`apply_style` after
  editing it (or pass ``style=`` overrides to :func:`apply_style`).
- Metadata tables :data:`OBS_META` and :data:`PARAM_META` map observable / parameter keys
  to LaTeX labels, units, and display scales.
- Each ``plot_*`` function takes a ``run`` dict (from :func:`photoring.io.load_run`) plus,
  where needed, the TTV data, and can save into a case's ``figures/<type>/`` directory when
  passed a :class:`~photoring.config.CasePaths`.

The ``dynesty``-native diagnostics (run plot, trace plot, corner) remain in the inference
notebook; everything that reads the saved results uses the functions here.

LaTeX note: :data:`STYLE`\\ ``['use_latex']`` defaults to ``False`` for portability. Set it
to ``True`` (needs a TeX installation) for full LaTeX rendering in the manuscript figures.
"""

from __future__ import annotations

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as mgridspec
import matplotlib.image as mpimg
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import AutoMinorLocator
from scipy.stats import gaussian_kde, truncnorm as _truncnorm
from scipy.stats import wasserstein_distance, ks_2samp, energy_distance

try:
    import corner as _corner
    HAS_CORNER = True
except ImportError:
    HAS_CORNER = False

try:
    from dynesty import plotting as _dyplot
    HAS_DYNESTY = True
except ImportError:
    HAS_DYNESTY = False


# ══════════════════════════════════════════════════════════════════════════
#  STYLE
# ══════════════════════════════════════════════════════════════════════════
STYLE = {
    # Typography
    "font_family": "serif",
    "font_size": 18,
    "annot_size": 12,
    "title_size": 20,
    "label_size": 18,
    "tick_size": 12,
    "legend_size": 13,
    "use_latex": False,      # True -> full LaTeX rendering (needs texlive)
    "math_font": "cm",

    # Palette (pastel astronomical)
    "c_posterior": "#A8C8E8",
    "c_data": "#808080",
    "c_prior": "#F5C5A0",
    "c_ppc_in": "#A8D8C8",
    "c_ppc_out": "#F5C5A0",
    "c_planet_b": "#A2BCCE",
    "c_planet_d": "#9AC2B8",
    "c_median": "#3D424A",
    "c_interval": "#4B5666",
    "c_accent": "#E88A6A",
    "c_corner_2d": "#7FB3D3",
    "c_corner_1d": "#6487AA",
    "c_logz": "#9CC2A5",
    "c_logl": "#E8A8A8",

    # Figure geometry
    "fig_dpi": 200,
    "fig_w_single": 3.5,
    "fig_h_single": 3.5,
    "fig_w_ppc": 4.2,
    "hspace": 0.2,
    "wspace": 0.2,

    # Lines and fills
    "hist_alpha": 0.8,
    "hist_bins": "scott",
    "hist_edgecolor": "none",
    "line_lw": 1.2,
    "line_lw_thin": 1.2,
    "spine_lw": 1.2,
    "contour_alpha": 0.85,
    "contour_smooth": 1.5,

    # Grid and spines
    "show_grid": True,
    "grid_alpha": 0.1,
    "grid_lw": 0.2,
    "minor_ticks": True,
    "top_spine": False,
    "right_spine": False,

    # Corner-specific
    "corner_quantiles": [0.16, 0.5, 0.84],
    "corner_levels": [0.393, 0.865],

    # Output
    "fig_format": "png",
    "transparent": False,
}

PLANET_LABELS = {"b": "Kepler-51 b", "c": "Kepler-51 c", "d": "Kepler-51 d"}

OBS_META = {
    "delta":   dict(col="delta",       scale=1e6, unit="ppm",
                    label=r"$\delta$ [ppm]", short="Transit depth", symbol=r"$\delta$"),
    "T14":     dict(col="T14",         scale=1.0, unit="h",
                    label=r"$T_{14}$ [h]", short="Total duration", symbol=r"$T_{14}$"),
    "T23":     dict(col="T23",         scale=1.0, unit="h",
                    label=r"$T_{23}$ [h]", short="Flat duration", symbol=r"$T_{23}$"),
    "rho_obs": dict(col="rho_obs_gcc", scale=1.0, unit=r"g cm$^{-3}$",
                    label=r"$\rho_{\star,\rm obs}$ [g cm$^{-3}$]", short="Obs. density",
                    symbol=r"$\rho_{\star,\rm obs}$"),
    "b_obs":   dict(col="b",           scale=1.0, unit="",
                    label=r"$b_{\rm obs}$", short="Impact parameter", symbol=r"$b_{\rm obs}$"),
}

PARAM_META = {
    "fe":       dict(label=r"$f_e\;[R_p]$", desc="Outer ring radius", symbol=r"$f_e$"),
    "ir":       dict(label=r"$i_R\;[\deg]$", desc="Ring inclination", symbol=r"$i_R$"),
    "theta":    dict(label=r"$\theta_R\;[\deg]$", desc="Ring projected tilt", symbol=r"$\theta_R$"),
    "p":        dict(label=r"$p = R_p/R_\star$", desc="Planet radius ratio", symbol=r"$p$"),
    "tau":      dict(label=r"$\tau$", desc="Ring opacity", symbol=r"$\tau$"),
    "rho_true": dict(label=r"$\rho_{\star,\rm true}\;[\rm g\,cm^{-3}]$",
                     desc="True stellar density", symbol=r"$\rho_{\star,\rm true}$"),
    "b":        dict(label=r"$b$", desc="Impact parameter", symbol=r"$b$"),
}

# Fixed column order of the PPC array produced by inference.compute_ppc.
_PPC_COL = {"delta": 0, "T14": 1, "T23": 2, "rho_obs": 3, "b_obs": 4}
_PPC_SCALE = {"delta": 1e6, "T14": 1.0, "T23": 1.0, "rho_obs": 1.0, "b_obs": 1.0}
_PPC_TTV_KEY = {"delta": "delta", "T14": "T14", "T23": "T23",
                "rho_obs": "rho_obs_gcc", "b_obs": "b"}
_PPC_LABEL = {k: OBS_META[k]["label"] for k in OBS_META}
_PPC_UNIT = {"delta": "ppm", "T14": "h", "T23": "h", "rho_obs": r"g\,cm$^{-3}$", "b_obs": ""}

ALL_OBS_KEYS = ["delta", "T14", "T23", "rho_obs", "b_obs"]

CMAP_POSTERIOR = None  # built by apply_style


def apply_style(style=None):
    """Apply the pipeline's matplotlib rcParams. Pass a dict to override :data:`STYLE` first."""
    global CMAP_POSTERIOR
    if style:
        STYLE.update(style)
    mpl.rcParams.update({
        "font.family": STYLE["font_family"],
        "font.size": STYLE["font_size"],
        "axes.labelsize": STYLE["label_size"],
        "axes.titlesize": STYLE["title_size"],
        "xtick.labelsize": STYLE["tick_size"],
        "ytick.labelsize": STYLE["tick_size"],
        "legend.fontsize": STYLE["legend_size"],
        "mathtext.fontset": STYLE["math_font"],
        "text.usetex": STYLE["use_latex"],
        "axes.linewidth": STYLE["spine_lw"],
        "axes.spines.top": STYLE["top_spine"],
        "axes.spines.right": STYLE["right_spine"],
        "axes.grid": STYLE["show_grid"],
        "grid.alpha": STYLE["grid_alpha"],
        "grid.linewidth": STYLE["grid_lw"],
        "savefig.dpi": STYLE["fig_dpi"],
        "savefig.bbox": "tight",
        "savefig.transparent": STYLE["transparent"],
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.minor.visible": STYLE["minor_ticks"],
        "ytick.minor.visible": STYLE["minor_ticks"],
        "xtick.top": False,
        "ytick.right": False,
    })
    if STYLE["use_latex"]:
        mpl.rcParams["text.latex.preamble"] = r"\usepackage{amsmath}"
    CMAP_POSTERIOR = LinearSegmentedColormap.from_list(
        "posterior_pastel", ["#FFFFFF", STYLE["c_posterior"], STYLE["c_median"]], N=256)


def planet_color(planet):
    """Return the palette colour for a planet key."""
    return STYLE["c_planet_b"] if planet == "b" else STYLE["c_planet_d"]


# ── low-level helpers ────────────────────────────────────────────────────────
def _style_ax(ax, xlabel="", ylabel="Density", title="", legend=True):
    ax.set_xlabel(xlabel, labelpad=4)
    ax.set_ylabel(ylabel, labelpad=4)
    if legend:
        ax.legend(fontsize=STYLE["legend_size"], framealpha=0.85,
                  edgecolor="#cccccc", fancybox=False)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    return ax


def _annotate_stats(ax, v, color, xpos="left", ypos=0.97, offset=0.0, x=None):
    med = np.median(v); p16 = np.percentile(v, 16); p84 = np.percentile(v, 84)
    txt = f"{med:.3g}$^{{+{p84 - med:.2g}}}_{{-{med - p16:.2g}}}$"
    ha = "left" if xpos == "left" else "right"
    if x is None:
        x = 0.04 if xpos == "left" else 0.96
    else:
        x = (x - ax.get_xlim()[0]) / (ax.get_xlim()[1] - ax.get_xlim()[0])
    ax.text(x, ypos + offset, txt, transform=ax.transAxes,
            fontsize=STYLE["annot_size"] + 3, color=color, ha=ha, va="top",
            fontfamily="serif")


def _hist1d(ax, data, color, label, bins=None, density=True, alpha=None, zorder=2):
    b = bins or STYLE["hist_bins"]
    a = alpha if alpha is not None else STYLE["hist_alpha"]
    ax.hist(data, bins=b, density=density, color=color, alpha=a,
            edgecolor=STYLE["hist_edgecolor"], zorder=zorder, label=label)


def _vline(ax, x, color, lw=None, ls="-", alpha=1.0, label="", zorder=3):
    ax.axvline(x, color=color, lw=lw or STYLE["line_lw"], ls=ls, alpha=alpha,
               label=label, zorder=zorder)


def _kde_line(ax, data, color, label="", n=400, lw=None, ls="-", alpha=1.0):
    k = gaussian_kde(data, bw_method="scott")
    x = np.linspace(data.min(), data.max(), n)
    ax.plot(x, k(x), color=color, lw=lw or STYLE["line_lw"], ls=ls, alpha=alpha,
            label=label, zorder=4)


def _save(fig, name, paths=None, figure_type="", dpi=None):
    """Save ``fig`` into ``paths.figures_dir(figure_type)`` if ``paths`` is given."""
    if paths is None:
        return None
    d = paths.figures_dir(figure_type)
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{name}.{STYLE['fig_format']}"
    fig.savefig(p, dpi=dpi or STYLE["fig_dpi"])
    print(f"  Saved -> {p}")
    return p


# ── PPC statistics ───────────────────────────────────────────────────────────
def ppc_stats_1d(emp, pred):
    """Wasserstein-1, KS (+ p-value) and Energy distance between two 1-D sample sets."""
    emp = np.asarray(emp, dtype=float); emp = emp[np.isfinite(emp)]
    pred = np.asarray(pred, dtype=float); pred = pred[np.isfinite(pred)]
    W1 = float(wasserstein_distance(emp, pred))
    KS, KS_p = ks_2samp(emp, pred)
    E = float(energy_distance(emp, pred))
    return dict(W1=W1, KS=float(KS), KS_p=float(KS_p), E=E)


def _stats_legend_lines(stats, unit=""):
    u = f" {unit}" if unit else ""
    p = stats["KS_p"]
    p_str = f"{p:.1e}" if p < 0.001 else f"{p:.3f}"
    return [rf"$W_1 = {stats['W1']:.3g}${u}",
            rf"$p_{{\rm KS}} = {p_str}$",
            rf"$E = {stats['E']:.3g}${u}"]


# ══════════════════════════════════════════════════════════════════════════
#  KDE self-consistency check
# ══════════════════════════════════════════════════════════════════════════
def plot_kde_ppc(model, planet="", paths=None, run_tag=None, seed=None):
    """Compare KDE resamples against the training histograms (KDE self-consistency)."""
    seed = seed if seed is not None else model.kde_config["seed_kde"] + 1
    synth = model.kde.resample(len(model.idx_train), seed=seed)
    obs = model.observables
    n = len(obs)
    ncols = min(n, 4)
    nrows = (n + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.5 * ncols, 3.8 * nrows), squeeze=False)
    for i, key in enumerate(obs):
        ax = axes[i // ncols][i % ncols]
        _, _, lbl, scale, unit = model.OBS_MAP[key]
        _hist1d(ax, model.train_emp[key], STYLE["c_data"], "Training data", alpha=0.55)
        _hist1d(ax, synth[i] * scale, planet_color(planet), "KDE resample", alpha=0.6)
        _style_ax(ax, xlabel=lbl + (f" [{unit}]" if unit else ""), title=key, legend=True)
    for i in range(n, nrows * ncols):
        axes[i // ncols][i % ncols].set_axis_off()
    fig.suptitle(f"KDE self-consistency — {PLANET_LABELS.get(planet, planet)}",
                 fontsize=STYLE["title_size"])
    fig.tight_layout()
    if run_tag:
        _save(fig, f"{run_tag}_kde_ppc", paths, "kde_ppc")
    return fig


# ══════════════════════════════════════════════════════════════════════════
#  Posterior predictive check
# ══════════════════════════════════════════════════════════════════════════
def _ppc_entries(run, ttv, keys):
    entries = []
    ppc = run["ppc"]
    for key in keys:
        col = _PPC_COL[key]; scale = _PPC_SCALE[key]; ttv_key = _PPC_TTV_KEY[key]
        emp_raw = ttv.get(ttv_key, np.array([]))
        pred_raw = ppc[:, col] if (ppc is not None and ppc.ndim == 2 and col < ppc.shape[1]) else np.array([])
        emp = np.asarray(emp_raw).ravel() * scale
        pred = np.asarray(pred_raw).ravel() * scale
        emp = emp[np.isfinite(emp)]; pred = pred[np.isfinite(pred)]
        if len(emp) and len(pred):
            entries.append((key, emp, pred, _PPC_LABEL[key]))
    return entries


def plot_ppc(run, ttv, obs_keys=None, paths=None):
    """Posterior-predictive check: TTV vs predicted distributions with GoF statistics."""
    planet = run["planet"]
    keys = obs_keys if obs_keys is not None else ALL_OBS_KEYS
    entries = _ppc_entries(run, ttv, keys)
    if not entries:
        print(f"No PPC data for {run['tag']} — skipping.")
        return None, {}
    all_stats = {key: ppc_stats_1d(emp, pred) for key, emp, pred, _ in entries}

    n = len(entries)
    W = STYLE["fig_w_ppc"]
    fig, axes = plt.subplots(1, n, figsize=(W * n * 1.2, STYLE["fig_h_single"] * 1.2),
                             gridspec_kw=dict(wspace=STYLE["wspace"] * 1.5), squeeze=False)
    axes = axes[0]
    col = planet_color(planet)
    in_like = set(run["kde_obs"])
    for ax, (key, emp, pred, lbl) in zip(axes, entries):
        _lim = np.percentile(np.concatenate([emp, pred]), [0.5, 99.5])
        _hist1d(ax, emp, STYLE["c_data"], "TTV", alpha=0.55)
        _hist1d(ax, pred, col, "Posterior", alpha=0.65)
        ax.set_xlim(_lim)
        for s in _stats_legend_lines(all_stats[key], unit=_PPC_UNIT[key]):
            ax.plot([], [], color="none", label=s)
        tick = r"$\checkmark$" if key in in_like else r"$\times$"
        _style_ax(ax, xlabel=lbl, title=f"{key} {tick}", legend=True)
    fig.suptitle(f"Posterior Predictive Check — {PLANET_LABELS.get(planet, planet)}",
                 fontsize=STYLE["title_size"] + 2, y=1.03)
    fig.tight_layout()
    _save(fig, f"{run['tag']}_ppc", paths, "ppc")
    return fig, all_stats


# ══════════════════════════════════════════════════════════════════════════
#  Marginal posteriors
# ══════════════════════════════════════════════════════════════════════════
def plot_marginals(run, berger_rho=None, paths=None):
    """1-D marginal posteriors with median/68% lines and prior overlays for rho_true, b."""
    planet = run["planet"]; chain = run["chain"]; pnames = run["param_names"]; meta = run["meta"]
    ndim = len(pnames)
    W = STYLE["fig_w_single"]; H = STYLE["fig_h_single"]
    fig, axes = plt.subplots(1, ndim, figsize=(W * ndim * 1.5, H),
                             gridspec_kw=dict(wspace=STYLE["wspace"] * 1.4), squeeze=False)
    axes = axes[0]
    col = planet_color(planet)
    for ax, name in zip(axes, pnames):
        v = chain[:, pnames.index(name)]
        lbl = PARAM_META.get(name, {}).get("label", name)
        _hist1d(ax, v, col, "")
        med, p16, p84 = np.percentile(v, [50, 16, 84])
        _vline(ax, med, STYLE["c_median"], alpha=0.7)
        _vline(ax, p16, STYLE["c_interval"], ls="--", alpha=0.6)
        _vline(ax, p84, STYLE["c_interval"], ls="--", alpha=0.6)
        _annotate_stats(ax, v, "k", xpos="left", ypos=0.97, x=med * 1.05)
        if name == "rho_true" and berger_rho is not None:
            k = gaussian_kde(berger_rho)
            x = np.linspace(np.min(berger_rho), np.max(berger_rho), 400)
            ax.plot(x, k(x), color="k", lw=STYLE["line_lw"], ls="-",
                    label="Berger et al. 2023", zorder=5)
        if name == "b":
            bf = meta.get("B_FIXED", 0.0); bs = meta.get("B_SIGMA", 0.1)
            dist = _truncnorm((0.0 - bf) / bs, (1.0 - bf) / bs, loc=bf, scale=bs)
            x = np.linspace(0, 1, 400)
            ax.plot(x, dist.pdf(x), color="k", lw=STYLE["line_lw"], ls="-",
                    label="Masuda et al. 2024", zorder=5)
        _style_ax(ax, xlabel=lbl, title=PARAM_META.get(name, {}).get("desc", name), legend=False)
    fig.suptitle(f"Marginal posteriors — {PLANET_LABELS.get(planet, planet)}",
                 fontsize=STYLE["title_size"] + 2, y=1.02)
    fig.tight_layout()
    _save(fig, f"{run['tag']}_marginals", paths, "marginal")
    return fig


# ══════════════════════════════════════════════════════════════════════════
#  Corner plot
# ══════════════════════════════════════════════════════════════════════════
def plot_corner(run, paths=None):
    """Joint-posterior corner plot (``corner`` if available, else the dynesty fallback)."""
    chain = run["chain"]; pnames = run["param_names"]
    labels = [PARAM_META.get(n, {}).get("label", n) for n in pnames]
    if HAS_CORNER:
        fig = _corner.corner(
            chain, labels=labels, quantiles=STYLE["corner_quantiles"],
            show_titles=True, title_kwargs={"fontsize": STYLE["tick_size"]},
            title_fmt=".4f", color=STYLE["c_corner_1d"],
            hist_kwargs=dict(color=STYLE["c_corner_1d"], edgecolor="none", fill=True,
                             alpha=STYLE["hist_alpha"]),
            plot_contours=True, fill_contours=True,
            contourf_kwargs=dict(
                levels=STYLE["corner_levels"] + [1.0],
                colors=[STYLE["c_corner_2d"], STYLE["c_median"] + "80", STYLE["c_median"] + "40"],
                alpha=STYLE["contour_alpha"]),
            contour_kwargs=dict(linewidths=STYLE["line_lw_thin"], colors=STYLE["c_median"]),
            smooth=STYLE["contour_smooth"], plot_density=False,
            data_kwargs=dict(alpha=0.1, ms=1.0, color=STYLE["c_median"]),
        )
    elif HAS_DYNESTY and run.get("dres") is not None:
        fig, _ = _dyplot.cornerplot(run["dres"], labels=labels, show_titles=True,
                                    title_kwargs={"fontsize": STYLE["tick_size"]},
                                    color=STYLE["c_corner_1d"], smooth=STYLE["contour_smooth"])
    else:
        print("Neither corner nor dynesty available — skipping corner plot.")
        return None
    planet_label = PLANET_LABELS.get(run["planet"], run["planet"])
    fig.suptitle(f"Joint posteriors — {planet_label}", fontsize=STYLE["title_size"], y=1.01)
    _save(fig, f"{run['tag']}_corner", paths, "corner")
    return fig


# ══════════════════════════════════════════════════════════════════════════
#  Ring geometry diagram
# ══════════════════════════════════════════════════════════════════════════
def plot_ring_diagram(run, ax=None, paths=None, scale=0.2):
    """Draw the median-posterior ring geometry projected onto the stellar disk.

    Uses :mod:`geotrans` (``RingedSystem`` + ``plotEllipse``) to render the ellipses.
    """
    import geotrans as gt2
    chain = run["chain"]; pnames = run["param_names"]; meta = run["meta"]

    def _get(name, default):
        return chain[:, pnames.index(name)] if name in pnames else np.full(len(chain), default)

    fe = float(np.median(_get("fe", meta.get("FE_MAX", 5.0) / 2)))
    ir = float(np.median(_get("ir", 45.0)))
    theta = float(np.median(_get("theta", 90.0)))
    p = float(np.median(_get("p", meta.get("p_mean_ref", 0.08))))
    fi = meta.get("FI_FIXED", 1.0)

    own_fig = ax is None
    if own_fig:
        fig = plt.figure(figsize=(3, 3)); ax = fig.add_subplot(111)
    else:
        fig = ax.get_figure()
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_axis_off()
    ax.set_aspect("equal", adjustable="box")

    col = planet_color(run["planet"])
    System = gt2.RingedSystem(dict(fe=fe, ir=ir, theta=theta, p=p, fi=fi))
    fh = scale / (System.fe * System.Rp); fv = fh
    C = np.array([0.5, 0.5])
    Planet = gt2.Figure(C, fh * System.Rp, fv * System.Rp, 1.0, 0.0, "Planet")
    Ringe = gt2.Figure(C, fh * System.Re, fv * System.Re * np.cos(System.ir),
                       np.cos(System.phir), np.sin(System.phir), "Ringext")
    Ringi = gt2.Figure(C, fh * System.Ri, fv * System.Ri * np.cos(System.ir),
                       np.cos(System.phir), np.sin(System.phir), "Ringint")
    gt2.plotEllipse(ax, Planet, patch=True, zorder=10, color="k", transform=ax.transAxes)
    gt2.plotEllipse(ax, Ringe, zorder=9, color=col, alpha=0.85,
                    lw=STYLE["line_lw"], transform=ax.transAxes)
    gt2.plotEllipse(ax, Ringi, zorder=9, color=col, alpha=0.30,
                    lw=STYLE["line_lw_thin"], transform=ax.transAxes)
    if own_fig:
        _save(fig, f"{run['tag']}_ring", paths, "ring")
    return fig


# ══════════════════════════════════════════════════════════════════════════
#  Consolidated results panel
# ══════════════════════════════════════════════════════════════════════════
def plot_results_panel(run, ttv, obs_keys=None, paths=None):
    """Consolidated publication figure: corner (image) + ring diagram + PPC row.

    The corner sub-panel is loaded from ``figures/corner/<tag>_corner.png`` (generated by
    :func:`plot_corner`); if it is missing, it is generated on the fly.
    """
    planet = run["planet"]; chain = run["chain"]; pnames = run["param_names"]; meta = run["meta"]
    ndim = len(pnames)
    keys = obs_keys if obs_keys is not None else ALL_OBS_KEYS
    entries = _ppc_entries(run, ttv, keys)
    n_ppc = len(entries)
    col = planet_color(planet)

    # ── ensure the corner image exists ────────────────────────────────────
    corner_png = None
    if paths is not None:
        corner_png = paths.figures_dir("corner") / f"{run['tag']}_corner.png"
        if not corner_png.exists():
            fig_c = plot_corner(run, paths=paths)
            if fig_c is not None:
                plt.close(fig_c)

    cell = STYLE["fig_w_single"] * 1.05
    corner_side = ndim * cell
    ring_side = corner_side * 0.5
    fig_w = corner_side + ring_side
    ppc_h = corner_side * 0.5
    fig_h = corner_side + ppc_h
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=STYLE["fig_dpi"])
    outer = mgridspec.GridSpec(
        2, 2, figure=fig, width_ratios=[corner_side, ring_side],
        height_ratios=[corner_side, ppc_h], wspace=0.05, hspace=0.03,
        left=0.03, right=0.97, top=0.9, bottom=0.05)

    # corner image
    ax_img = fig.add_subplot(outer[0, 0]); ax_img.axis("off")
    if corner_png is not None and corner_png.exists():
        try:
            ax_img.imshow(mpimg.imread(str(corner_png)), aspect="auto")
        except Exception as e:
            ax_img.text(0.5, 0.5, f"corner unavailable\n({e})", ha="center", va="center")
    else:
        ax_img.text(0.5, 0.5, "corner unavailable", ha="center", va="center")

    # ring diagram
    ax_ring = fig.add_subplot(outer[0, 1])
    try:
        plot_ring_diagram(run, ax=ax_ring)
        for spine in ax_ring.spines.values():
            spine.set_visible(True)
            spine.set_linewidth(STYLE["spine_lw"] * 0.6)
            spine.set_edgecolor(STYLE["c_median"] + "55")
    except Exception as e:
        ax_ring.text(0.5, 0.5, f"Ring diagram\nunavailable\n({e})",
                     ha="center", va="center", color="gray", transform=ax_ring.transAxes)

    # PPC row
    if n_ppc > 0:
        bottom_gs = mgridspec.GridSpecFromSubplotSpec(
            1, n_ppc, subplot_spec=outer[1, :],
            wspace=STYLE["wspace"] * 1.2, hspace=STYLE["hspace"])
        in_like = set(run["kde_obs"])
        for j, (key, emp, pred, lbl) in enumerate(entries):
            ax = fig.add_subplot(bottom_gs[0, j])
            stats = ppc_stats_1d(emp, pred)
            _lim = np.percentile(np.concatenate([emp, pred]), [0.5, 99.5])
            _hist1d(ax, emp, STYLE["c_data"], "TTV", alpha=0.55)
            _hist1d(ax, pred, col, "PPC", alpha=0.65)
            ax.set_xlim(_lim)
            for s in _stats_legend_lines(stats, unit=_PPC_UNIT[key]):
                ax.plot([], [], color="none", label=s)
            tick = r"$\checkmark$" if key in in_like else r"$\times$"
            _style_ax(ax, xlabel=lbl, title=f"{key} {tick}", legend=True)

    fig.suptitle(f"{PLANET_LABELS.get(planet, planet)} — Posterior results",
                 fontsize=STYLE["title_size"] + 2, y=0.98)
    _save(fig, f"{run['tag']}_panel", paths, "panel")
    return fig


# ══════════════════════════════════════════════════════════════════════════
#  Observable posteriors (notebook 01b)
# ══════════════════════════════════════════════════════════════════════════
def plot_observable_posteriors(ttv_by_planet, keys=None, paths=None, run_tag="observables"):
    """KDE posteriors of transit observables, overlaid per planet (publication style).

    Parameters
    ----------
    ttv_by_planet : dict
        ``{planet: ttv_dict}`` (each from :func:`photoring.io.load_observables`).
    keys : list of str, optional
        Observable keys to show. Defaults to all in :data:`OBS_META` plus ``aR``, ``i_orb``.
    """
    display = {
        "delta": (r"$\delta$", 1.0), "T14": (r"$T_{14}$ [h]", 1.0),
        "T23": (r"$T_{23}$ [h]", 1.0), "rho_obs_gcc": (r"$\rho_{\star,\rm obs}$ [g cm$^{-3}$]", 1.0),
        "aR": (r"$a/R_\star$", 1.0), "b": (r"$b$", 1.0),
        "i_orb": (r"$i_{\rm orb}$ [deg]", 1.0), "p": (r"$p=R_p/R_\star$", 1.0),
    }
    keys = keys or ["p", "delta", "T14", "T23", "aR", "rho_obs_gcc", "b", "i_orb"]
    ncols = 4
    nrows = (len(keys) + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.2 * ncols, 3.6 * nrows), squeeze=False)
    for i, key in enumerate(keys):
        ax = axes[i // ncols][i % ncols]
        lbl, scale = display.get(key, (key, 1.0))
        for planet, ttv in ttv_by_planet.items():
            if key not in ttv:
                continue
            v = np.asarray(ttv[key], dtype=float)
            v = v[np.isfinite(v)] * scale
            if len(v) < 5:
                continue
            col = planet_color(planet)
            k = gaussian_kde(v)
            xg = np.linspace(v.min() - 0.5 * v.std(), v.max() + 0.5 * v.std(), 400)
            ax.fill_between(xg, k(xg), alpha=0.35, color=col)
            ax.plot(xg, k(xg), color=col, lw=STYLE["line_lw"] * 1.4,
                    label=PLANET_LABELS.get(planet, planet))
            ax.axvline(np.median(v), color=col, lw=1.2, ls="--", alpha=0.8)
        _style_ax(ax, xlabel=lbl, legend=(i == ncols - 1))
    for i in range(len(keys), nrows * ncols):
        axes[i // ncols][i % ncols].set_axis_off()
    fig.suptitle("Transit observable posteriors", fontsize=STYLE["title_size"] + 2)
    fig.tight_layout()
    _save(fig, run_tag, paths, "observables")
    return fig


# ══════════════════════════════════════════════════════════════════════════
#  Summary tables
# ══════════════════════════════════════════════════════════════════════════
def print_summary_table(runs_list, ppc_stats=None):
    """Print a plain-text median +/- 68% parameter table for all runs."""
    ppc_stats = ppc_stats or {}
    W = 108
    print("=" * W)
    print(f"{'Run tag':<35}  {'param':>10}  {'median':>10}  {'-err':>8}  {'+err':>8}  {'ln Z':>10}")
    print("=" * W)
    for r in runs_list:
        chain = r["chain"]; pnames = r["param_names"]; tag = r["tag"][:35]
        for i, name in enumerate(pnames):
            v = chain[:, i]
            med, p16, p84 = np.median(v), np.percentile(v, 16), np.percentile(v, 84)
            lnz = f"{r['logz']:.3f}" if i == 0 else ""
            print(f"{tag:<35}  {name:>10}  {med:>10.5f}  {med - p16:>8.5f}  {p84 - med:>8.5f}  {lnz:>10}")
        if r["tag"] in ppc_stats and ppc_stats[r["tag"]]:
            print(f"  {'':33}  {'observable':<10}  {'W1':>10}  {'KS':>8}  {'p-value':>10}  {'E':>10}")
            for obs_key, s in ppc_stats[r["tag"]].items():
                p = s["KS_p"]; p_str = f"{p:.2e}" if p < 0.001 else f"{p:.4f}"
                print(f"  {'PPC':33}  {obs_key:<10}  {s['W1']:>10.4g}  {s['KS']:>8.4f}  {p_str:>10}  {s['E']:>10.4g}")
        print("-" * W)


def print_latex_table(runs_list):
    """Print a LaTeX-ready parameter table (one row per run)."""
    all_params = []
    for r in runs_list:
        for n in r["param_names"]:
            if n not in all_params:
                all_params.append(n)
    col_spec = "l" + "c" * len(all_params)
    print(r"\begin{table}[ht]")
    print(r"\centering")
    print(r"\caption{Posterior parameter estimates.}")
    print(r"\begin{tabular}{" + col_spec + "}")
    print(r"\hline\hline")
    print(r"Run & " + " & ".join(PARAM_META.get(p, {}).get("label", p) for p in all_params) + r" \\")
    print(r"\hline")
    for r in runs_list:
        chain = r["chain"]; pnames = r["param_names"]
        planet = PLANET_LABELS.get(r["planet"], r["planet"])
        obs = "+".join(r["kde_obs"])
        row = f"{planet} [{obs}]"
        for p in all_params:
            if p in pnames:
                v = chain[:, pnames.index(p)]
                med, p16, p84 = np.median(v), np.percentile(v, 16), np.percentile(v, 84)
                row += f" & ${med:.4f}_{{-{med - p16:.4f}}}^{{+{p84 - med:.4f}}}$"
            else:
                row += " & ---"
        print(row + r" \\")
    print(r"\hline")
    print(r"\end{tabular}")
    print(r"\end{table}")
