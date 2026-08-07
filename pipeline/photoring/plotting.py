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

from datetime import datetime
from pathlib import Path

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
    from dynesty import plotting as _dyplot
    HAS_DYNESTY = True
except ImportError:
    HAS_DYNESTY = False

try:
    import corner as _corner
    HAS_CORNER = True
except ImportError:
    HAS_CORNER = False


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

    # Median / credible-interval markers drawn by _annotate_stats
    "median_ls": "--",
    "median_lw": 1.2,
    "median_alpha": 0.85,
    "sigma_ls": ":",
    "sigma_lw": 0.7,
    "sigma_alpha": 0.50,

    # Literature overlays (unfilled reference curves)
    "lit_lw": 1.5,
    "lit_alpha": 0.90,
    "lit_ls": "-",

    # Grid and spines
    "show_grid": True,
    "grid_alpha": 0.1,
    "grid_lw": 0.2,
    "minor_ticks": True,
    "top_spine": False,
    "right_spine": False,

    # Corner-specific
    # NOTE: dynesty's own default is the 95% interval [0.025, 0.5, 0.975]; the
    # published figures use that default (see PAPER_STYLE).
    "corner_quantiles": [0.16, 0.5, 0.84],
    "corner_levels": [0.393, 0.865],
    # Corner smoothing, as a *fraction of each parameter's plotted span* — this is
    # dynesty's own convention, and is not the same quantity as `contour_smooth`
    # (which counts bins). Values above ~0.1 wash the posterior out entirely.
    "corner_smooth": 0.02,

    # Output
    "fig_format": "png",
    "transparent": False,
}

# Pristine copy of the defaults, so ``apply_style(..., reset=True)`` can restore them
# after a preset has been applied in the same session.
_STYLE_DEFAULTS = dict(STYLE)

# ── Paper preset ──────────────────────────────────────────────────────────────
# Overrides that reproduce the published figures exactly. Apply with
# ``apply_style(PAPER_STYLE)``; see ``paper_figures/reproduce_paper_figures.ipynb``.
#
# It differs from the pipeline default in three ways that matter for reproduction:
#   1. a saturated palette with a separate fill/line colour per planet (the pipeline
#      default is a single pale pastel per planet),
#   2. ``use_latex=True`` — the manuscript figures are rendered by a real TeX install,
#   3. ``corner_quantiles`` = dynesty's default 95% interval, which is what the
#      published corner titles report.
PAPER_STYLE = {
    "use_latex": True,
    "fig_dpi": 220,
    "font_size": 10,
    "annot_size": 7.5,
    "title_size": 15,
    "label_size": 13,
    "tick_size": 13,
    "legend_size": 8,
    "grid_alpha": 0.18,
    "grid_lw": 0.4,
    "spine_lw": 0.75,
    "line_lw": 1.8,
    "corner_quantiles": [0.16, 0.5, 0.84],

    # Planets: saturated line colour + pale fill.
    "c_planet_b": "#A2BCCE",
    "c_planet_d": "#9AC2B8",
    "c_planet_b_line": "#0072B2",
    "c_planet_d_line": "#009E73",
    # The published corner plots are drawn in the pale per-planet colour.
    "c_corner_b": "#A2BCCE",
    "c_corner_d": "#9AC2B8",

    # Independent stellar-density reference (isochrone posterior samples).
    "c_rho_true": "#CC79A7",
    # TTV segments (segment-consistency figure).
    "c_segments": ["#B0C8E8", "#B8D4B0", "#E8C8B0"],
}

# Default per-planet display names. Override per case with :func:`set_case_labels`.
PLANET_LABELS = {"b": "Kepler-51 b", "c": "Kepler-51 c", "d": "Kepler-51 d"}

# ══════════════════════════════════════════════════════════════════════════
#  Metadata: one table per concept
# ══════════════════════════════════════════════════════════════════════════
# OBS_META is the single source of truth for the transit observables. Fields:
#   df_col   column name in the TTV dict returned by photoring.io.load_observables
#   ppc_col  column index in the PPC array built by inference.compute_ppc
#            (fixed order: delta, T14, T23, rho_obs, b_obs; None if not predicted)
#   scale    multiply raw values by this to get display units
#   unit     display unit, as it should appear after a value
#   symbol   bare LaTeX symbol, for annotations and composed titles
#   label    axis label (symbol + unit)
#   xlabel   verbose axis label used on the multi-panel observables figure
OBS_META = {
    "delta": dict(
        df_col="delta", ppc_col=0, scale=1e6, unit="ppm",
        symbol=r"$\delta$", label=r"$\delta$ [ppm]",
        xlabel=r"Transit depth $\delta$ [ppm]", short="Transit depth"),
    "T14": dict(
        df_col="T14", ppc_col=1, scale=1.0, unit="h",
        symbol=r"$T_{14}$", label=r"$T_{14}$ [h]",
        xlabel=r"Total duration $T_{14}$ [h]", short="Total duration"),
    "T23": dict(
        df_col="T23", ppc_col=2, scale=1.0, unit="h",
        symbol=r"$T_{23}$", label=r"$T_{23}$ [h]",
        xlabel=r"Flat duration $T_{23}$ [h]", short="Flat duration"),
    "rho_obs": dict(
        df_col="rho_obs_gcc", ppc_col=3, scale=1.0, unit=r"g cm$^{-3}$",
        symbol=r"$\rho_{\star,\rm obs}$",
        label=r"$\rho_{\star,\rm obs}$ [g cm$^{-3}$]",
        xlabel=r"Stellar density $\rho_{\star,\rm obs}$ [g cm$^{-3}$]",
        short="Obs. density"),
    "b_obs": dict(
        df_col="b", ppc_col=4, scale=1.0, unit="",
        symbol=r"$b_{\rm obs}$", label=r"$b_{\rm obs}$",
        xlabel=r"Impact parameter $b_{\rm obs}$", short="Impact parameter"),
    "aR": dict(
        df_col="aR", ppc_col=None, scale=1.0, unit="",
        symbol=r"$a/R_{\star}$", label=r"$a/R_{\star}$",
        xlabel=r"Scaled semimajor axis $a/R_{\star}$", short="Scaled semimajor axis"),
}

# Model parameters, in the canonical order used by PhotoRingModel.PARAM_NAMES.
# NOTE on ``theta``: the manuscript's symbol table calls this $\theta_R$, but the
# published corner plots are labelled $\theta$. The bare $\theta$ is kept here so the
# figures reproduce exactly.
PARAM_META = {
    "fe":       dict(label=r"$f_e\,[R_p]$", desc="Outer ring radius", symbol=r"$f_e$"),
    "ir":       dict(label=r"$i_R\,$[deg]", desc="Ring inclination", symbol=r"$i_R$"),
    "theta":    dict(label=r"$\theta\,$[deg]", desc="Ring projected tilt", symbol=r"$\theta$"),
    "p":        dict(label=r"$p=R_p/R_\star$", desc="Planet radius ratio", symbol=r"$p$"),
    "tau":      dict(label=r"$\tau$", desc="Ring opacity", symbol=r"$\tau$"),
    "rho_true": dict(label=r"$\rho_{\star,\rm true}\,$[g/cm$^3$]",
                     desc="True stellar density", symbol=r"$\rho_{\star,\rm true}$"),
    "b":        dict(label=r"$b$", desc="Impact parameter", symbol=r"$b$"),
}

# Observables predicted by the forward model, in PPC column order.
ALL_OBS_KEYS = [k for k, m in sorted(OBS_META.items(), key=lambda kv: (kv[1]["ppc_col"] is None,
                                                                      kv[1]["ppc_col"] or 0))
                if m["ppc_col"] is not None]

CMAP_POSTERIOR = None  # built by apply_style


def obs_meta(key):
    """Metadata for an observable key, with a clear error for unknown keys."""
    try:
        return OBS_META[key]
    except KeyError:
        raise KeyError(
            f"Unknown observable {key!r}. Known keys: {sorted(OBS_META)}") from None


def param_meta(name):
    """Metadata for a model-parameter name, falling back to the bare name."""
    return PARAM_META.get(name, dict(label=name, desc=name, symbol=name))


def set_case_labels(labels):
    """Replace :data:`PLANET_LABELS` for a non-Kepler-51 case.

    ``labels`` maps planet key -> display name, e.g. ``{"b": "HIP 41378 f"}``.
    """
    PLANET_LABELS.clear()
    PLANET_LABELS.update(labels)


def apply_style(style=None, reset=False):
    """Apply the pipeline's matplotlib rcParams.

    Pass a dict (e.g. :data:`PAPER_STYLE`) to override :data:`STYLE` first. Use
    ``reset=True`` to drop any previously applied overrides and start from the module
    defaults, so switching presets inside one kernel is not order-dependent.
    """
    global CMAP_POSTERIOR
    if reset:
        STYLE.clear()
        STYLE.update(_STYLE_DEFAULTS)
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
        # amssymb is required by the check/cross marks plot_ppc puts in panel titles.
        mpl.rcParams["text.latex.preamble"] = r"\usepackage{amsmath}\usepackage{amssymb}"
    CMAP_POSTERIOR = LinearSegmentedColormap.from_list(
        "posterior_pastel", ["#FFFFFF", STYLE["c_posterior"], STYLE["c_median"]], N=256)


#: Fallback cycle for cases with more planets than the palette names explicitly.
_PLANET_COLOR_CYCLE = ["#A6CEE8", "#90DBC7", "#F5C5A0", "#C8B0E8", "#E8C8B0"]
_PLANET_LINE_CYCLE = ["#0072B2", "#009E73", "#C17D11", "#6A3D9A", "#8B4513"]


def planet_color(planet, kind="fill"):
    """Palette colour for a planet key.

    ``kind`` selects ``"fill"`` (histograms, ring patches), ``"line"`` (KDE curves,
    median markers) or ``"corner"`` (corner-plot ink). Planets beyond those named in
    :data:`STYLE` fall back to a deterministic cycle keyed on the planet letter, so a
    case with more than two planets still gets stable, distinct colours.
    """
    prefix = "c_corner_" if kind == "corner" else "c_planet_"
    suffix = "_line" if kind == "line" else ""
    explicit = STYLE.get(f"{prefix}{planet}{suffix}")
    if explicit:
        return explicit
    # "corner"/"line" not declared for this planet -> fall back to its fill colour.
    if kind != "fill":
        fallback = STYLE.get(f"c_planet_{planet}")
        if fallback:
            return fallback

    # Unnamed planet: take the next cycle entry not already claimed by an explicit
    # STYLE colour, so a third planet never collides with b's or d's colour.
    cycle = _PLANET_LINE_CYCLE if kind == "line" else _PLANET_COLOR_CYCLE
    claimed = {v for k, v in STYLE.items()
               if k.startswith("c_planet_") and isinstance(v, str)}
    free = [c for c in cycle if c not in claimed] or cycle
    unnamed = [p for p in sorted(PLANET_LABELS) if not STYLE.get(f"c_planet_{p}")]
    idx = unnamed.index(planet) if planet in unnamed else 0
    return free[idx % len(free)]


# ── low-level helpers ────────────────────────────────────────────────────────
def _style_ax(ax, xlabel="", ylabel="Density", title="", legend=True):
    ax.set_xlabel(xlabel, labelpad=4)
    ax.set_ylabel(ylabel, labelpad=4)
    if title:
        ax.set_title(title, fontsize=STYLE["title_size"])
    if legend:
        handles, labels = ax.get_legend_handles_labels()
        # Split Photo/Posterior (inside axes) from GoF metrics (above), so the
        # identity legend does not collide with the figure title on PPC panels.
        id_h, id_l, other_h, other_l = [], [], [], []
        for h, lab in zip(handles, labels):
            if lab in ("Photo", "Posterior"):
                id_h.append(h); id_l.append(lab)
            else:
                other_h.append(h); other_l.append(lab)
        frame = dict(framealpha=0.85, edgecolor="#cccccc", fancybox=False)
        if id_h:
            leg_id = ax.legend(
                id_h, id_l, loc="best",
                fontsize=STYLE["legend_size"], **frame)
            ax.add_artist(leg_id)
            if other_h:
                ax.legend(
                    other_h, other_l, loc="lower center",
                    bbox_to_anchor=(0.5, 1.04), borderaxespad=0, ncol=1,
                    fontsize=STYLE["annot_size"], **frame)
        elif other_h:
            ax.legend(
                other_h, other_l, loc="lower center",
                bbox_to_anchor=(0.5, 1.04), borderaxespad=0, ncol=1,
                fontsize=STYLE["annot_size"], **frame)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    return ax


def _annotate_stats(ax, v, symbol="", unit="", color="k", xpos="left", ypos=0.97,
                    offset=0.0, x=None, sep=" = ", fmt=".2f", draw_vlines=True,
                    vline_color=None, show_interval=True):
    """Annotate the median and 68% credible interval of ``v`` inside ``ax``.

    Writes ``"<symbol><sep><median>^{+p84}_{-p16} <unit>"`` and, unless
    ``draw_vlines=False``, draws a dashed line at the median plus dotted lines at the
    16th/84th percentiles (``show_interval``).

    Parameters
    ----------
    symbol : str
        LaTeX symbol identifying the quantity (e.g. ``r"$\\delta$"``), or any label —
        the asterodensity panel passes a planet name.
    unit : str
        Unit appended after the value; ``""`` for dimensionless quantities.
    sep : str
        Separator between ``symbol`` and the value. Use ``" = "`` for normal panels and
        ``"\\n"`` to put the label on its own line above the value.
    fmt : str
        Format spec for median and both error terms. ``".2f"`` suits ppm/hours;
        use ``".3g"`` for quantities spanning several orders of magnitude.
    x : float, optional
        Horizontal position in *data* coordinates (converted internally). Defaults to a
        fixed inset from the left or right edge according to ``xpos``.
    vline_color : str, optional
        Colour of the vertical lines; defaults to ``color``.
    """
    med, p16, p84 = np.percentile(v, [50, 16, 84])
    unit_str = f" {unit}" if unit else ""
    txt = (f"{symbol}{sep}{med:{fmt}}"
           f"$^{{+{p84 - med:{fmt}}}}_{{-{med - p16:{fmt}}}}${unit_str}")
    ha = "left" if xpos == "left" else "right"
    if x is None:
        x = 0.04 if xpos == "left" else 0.96
    else:
        lo, hi = ax.get_xlim()
        x = (x - lo) / (hi - lo)

    if draw_vlines:
        vc = vline_color or color
        _vline(ax, med, vc, lw=STYLE["median_lw"], ls=STYLE["median_ls"],
               alpha=STYLE["median_alpha"], zorder=4)
        if show_interval:
            for q in (p16, p84):
                _vline(ax, q, vc, lw=STYLE["sigma_lw"], ls=STYLE["sigma_ls"],
                       alpha=STYLE["sigma_alpha"], zorder=3)

    ax.text(x, ypos + offset, txt, transform=ax.transAxes,
            fontsize=STYLE["annot_size"] + 4, color=color, ha=ha, va="top",
            fontfamily=STYLE["font_family"])


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


def run_version_id(files):
    """YYYYMMDDHH stamp from the newest file mtime (campaign identifier)."""
    files = [Path(f) for f in files if f is not None and Path(f).exists()]
    if not files:
        return "unknown"
    newest = max(files, key=lambda p: p.stat().st_mtime)
    return datetime.fromtimestamp(newest.stat().st_mtime).strftime("%Y%m%d%H")


def add_run_version_label(fig, version, *, x=0.988, y=0.98, fontsize=12, alpha=0.4):
    """Small vertical campaign stamp on the upper-right edge of the figure."""
    if not version or version == "unknown":
        return
    fig.text(
        x, y, str(version),
        rotation=90, va="top", ha="right",
        fontsize=fontsize, alpha=alpha, color="0.25",
        transform=fig.transFigure, clip_on=False,
    )


# ── PPC statistics ───────────────────────────────────────────────────────────
def ppc_stats_1d(emp, pred):
    """Wasserstein-1, KS (+ p-value) and Energy distance between two 1-D sample sets."""
    emp = np.asarray(emp, dtype=float); emp = emp[np.isfinite(emp)]
    pred = np.asarray(pred, dtype=float); pred = pred[np.isfinite(pred)]
    if emp.size == 0 or pred.size == 0:
        # e.g. b_obs undefined for all PPC draws (forward model returns NaN)
        return dict(W1=float("nan"), KS=float("nan"), KS_p=float("nan"), E=float("nan"))
    W1 = float(wasserstein_distance(emp, pred))
    KS, KS_p = ks_2samp(emp, pred)
    E = float(energy_distance(emp, pred))
    return dict(W1=W1, KS=float(KS), KS_p=float(KS_p), E=E)


def _stats_legend_lines(stats, unit=""):
    u = f" {unit}" if unit else ""
    return [rf"$W_1 = {stats['W1']:.3g}${u}",
            rf"$E = {stats['E']:.3g}${u}"]


def _stats_legend_line(stats, unit=""):
    """Compact single-line metrics label for panel legends."""
    u = f" {unit}" if unit else ""
    return f"W1 = {stats['W1']:.3g}{u}   E = {stats['E']:.3g}{u}"


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
        meta = obs_meta(key)
        col, scale = meta["ppc_col"], meta["scale"]
        if col is None:
            continue  # not predicted by the forward model (e.g. aR)
        emp_raw = ttv.get(meta["df_col"], np.array([]))
        pred_raw = ppc[:, col] if (ppc is not None and ppc.ndim == 2 and col < ppc.shape[1]) else np.array([])
        emp = np.asarray(emp_raw).ravel() * scale
        pred = np.asarray(pred_raw).ravel() * scale
        emp = emp[np.isfinite(emp)]; pred = pred[np.isfinite(pred)]
        if len(emp) and len(pred):
            entries.append((key, emp, pred, meta["label"]))
    return entries


# Preferred top-row observables for the 2+3 PPC layout; remaining keys go below.
_PPC_TOP_KEYS = ("rho_obs", "delta")


def plot_ppc(run, ttv, obs_keys=None, paths=None):
    """Posterior-predictive check: Photo vs predicted distributions with GoF statistics.

    Layout (when 5 observables are present):
      row 1 — ``rho_obs``, ``delta`` (2 panels)
      row 2 — remaining observables, e.g. ``T14``, ``T23``, ``b_obs`` (3 panels)
    """
    planet = run["planet"]
    keys = obs_keys if obs_keys is not None else ALL_OBS_KEYS
    entries = _ppc_entries(run, ttv, keys)
    if not entries:
        print(f"No PPC data for {run['tag']} — skipping.")
        return None, {}
    all_stats = {key: ppc_stats_1d(emp, pred) for key, emp, pred, _ in entries}

    # Quality score for ranking runs by PPC agreement:
    #   w1_i = W1_i / mean(emp_i),  <w1> = mean_i(w1_i),  z1 = -log10(<w1>)
    # where emp_i is the observed posterior sample of observable i.
    w1_vals = []
    for key, emp, _pred, _lbl in entries:
        mu = float(np.mean(emp))
        if not np.isfinite(mu) or abs(mu) < 1e-12:
            continue
        w1 = float(all_stats[key]["W1"]) / abs(mu)
        if np.isfinite(w1) and w1 > 0:
            w1_vals.append(w1)
    w1_mean = float(np.mean(w1_vals)) if w1_vals else float("nan")
    z1 = float(-np.log10(w1_mean)) if np.isfinite(w1_mean) and w1_mean > 0 else float("nan")
    all_stats["_summary"] = {
        "w1_mean": w1_mean,
        "z1": z1,
        "n_obs": len(w1_vals),
    }

    by_key = {key: (key, emp, pred, lbl) for key, emp, pred, lbl in entries}
    top = [by_key[k] for k in _PPC_TOP_KEYS if k in by_key]
    bot = [e for e in entries if e[0] not in _PPC_TOP_KEYS]
    # Fall back to a simple split if the preferred 2+3 layout is incomplete.
    if len(top) != 2 or len(bot) != 3:
        top, bot = entries[:2], entries[2:]

    W = STYLE["fig_w_ppc"]
    H = STYLE["fig_h_single"]
    # Compact 2+3 layout with tighter vertical spacing between rows.
    fig = plt.figure(figsize=(W * 3.2 * 0.6, H * 2.15))
    gs = fig.add_gridspec(2, 1, height_ratios=[1, 1], hspace=0.52)
    gs_top = gs[0].subgridspec(1, max(len(top), 1), wspace=0.32)
    gs_bot = gs[1].subgridspec(1, max(len(bot), 1), wspace=0.32)
    axes = ([fig.add_subplot(gs_top[0, i]) for i in range(len(top))]
            + [fig.add_subplot(gs_bot[0, i]) for i in range(len(bot))])
    ordered = top + bot

    col = planet_color(planet)
    for i, (ax, (key, emp, pred, lbl)) in enumerate(zip(axes, ordered)):
        _lim = np.percentile(np.concatenate([emp, pred]), [0.5, 99.5])
        # Histogram identity (Photo / Posterior) only on the first panel.
        photo_lbl = "Photo" if i == 0 else None
        post_lbl = "Posterior" if i == 0 else None
        _hist1d(ax, emp, STYLE["c_data"], photo_lbl, alpha=0.55)
        _hist1d(ax, pred, col, post_lbl, alpha=0.65)
        ax.set_xlim(_lim)
        ax.plot([], [], color="none",
                label=_stats_legend_line(all_stats[key], unit=obs_meta(key)["unit"]))
        _style_ax(ax, xlabel=lbl, legend=True)

    # Draw title lines explicitly so line spacing is consistent with/without usetex.
    title_fs = STYLE["title_size"] * 0.74
    title_lines = [
        f"Posterior Predictive Check — {PLANET_LABELS.get(planet, planet)}",
        _run_title(run, z1=z1),
        _bestfit_medians_line(run, include_metrics=False),
    ]
    line_step = 1.45 * (title_fs / 72.0) / fig.get_figheight()
    y_top = 0.985
    for i, line in enumerate(title_lines):
        fig.text(0.5, y_top - i * line_step, line,
                 ha="center", va="top", fontsize=title_fs,
                 transform=fig.transFigure)

    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.08, top=0.84)
    _save(fig, f"{run['tag']}_ppc", paths, "")
    return fig, all_stats


# ══════════════════════════════════════════════════════════════════════════
#  Marginal posteriors
# ══════════════════════════════════════════════════════════════════════════
def plot_marginals(run, rho_true_dist=None, b_obs_dist=None, paths=None):
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
        if name == "rho_true" and rho_true_dist is not None:
            k = gaussian_kde(rho_true_dist)
            x = np.linspace(np.min(rho_true_dist), np.max(rho_true_dist), 400)
            ax.plot(x, k(x), color="k", lw=STYLE["line_lw"], ls="-",
                    label="Isochrone Prior", zorder=5)
        if name == "b":
            if b_obs_dist is not None:
                k = gaussian_kde(b_obs_dist)
                x = np.linspace(np.min(b_obs_dist), np.max(b_obs_dist), 400)
                ax.plot(x, k(x), color="k", lw=STYLE["line_lw"], ls="-",
                        label="Observable $b_{obs}$", zorder=5)
            else:
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
def plot_corner(run, rho_true_dist=None, b_obs_dist=None, paths=None, ax_grid=None, title=True, save=True):
    """Joint-posterior corner plot, drawn by ``dynesty.plotting.cornerplot``.

    dynesty is the only backend: it works from the *weighted* nested-sampling output
    (``samples`` + ``logwt``), which is the posterior the sampler actually produced. The
    equal-weight ``chain`` is a resampled view of it, so a corner drawn from ``chain``
    with a different library gives subtly different contours and quantiles.

    The reported credible interval follows ``STYLE["corner_quantiles"]``; dynesty's own
    default (and the one the published figures use, see :data:`PAPER_STYLE`) is the 95%
    interval ``[0.025, 0.5, 0.975]``.

    Parameters
    ----------
    ax_grid : ndarray of Axes, optional
        Existing ``(ndim, ndim)`` axes grid to draw into, e.g. to compose the corner
        with other panels in one figure.
    title : bool
        Add a suptitle. Pass ``False`` when embedding the corner in a larger panel that
        carries its own title.

    Returns
    -------
    fig, axes
        The matplotlib figure and the ``(ndim, ndim)`` axes grid from dynesty.
    """
    if not HAS_DYNESTY:
        print("dynesty is not installed — cannot draw the corner plot.")
        return None, None
    if run.get("dres") is None:
        print(f"No dynesty results for {run['tag']} — cannot draw the corner plot.\n"
              "  The .npz must contain 'samples' (see photoring.io.load_run).")
        return None, None

    labels = [param_meta(n)["label"] for n in run["param_names"]]
    span = []
    for i, name in enumerate(run["param_names"]):
        if name == "b":
            span.append((0.0, 1.0))
        elif name == "rho_true" and rho_true_dist is not None:
            post_samples = run["chain"][:, i]
            min_val = min(np.min(rho_true_dist), np.min(post_samples))
            max_val = max(np.max(rho_true_dist), np.max(post_samples))
            pad = 0.05 * (max_val - min_val)
            span.append((float(min_val - pad), float(max_val + pad)))
        else:
            span.append(0.9999999)

    kwargs = dict(
        labels=labels, show_titles=True,
        title_kwargs={"fontsize": STYLE["tick_size"] + 10},
        quantiles=STYLE["corner_quantiles"],
        color=planet_color(run["planet"], "corner"),
        smooth=STYLE["corner_smooth"],
        span=span,
    )
    if ax_grid is not None:
        # dynesty takes an existing grid as a (figure, axes) tuple.
        kwargs["fig"] = (ax_grid[0, 0].get_figure(), ax_grid)
    fig, _axes = _dyplot.cornerplot(run["dres"], **kwargs)

    for ax in _axes.flatten():
        if ax is not None:
            ax.tick_params(axis='both', which='major', labelsize=STYLE['label_size'] + 5)
            ax.xaxis.label.set_size(STYLE['label_size'] + 5)
            ax.yaxis.label.set_size(STYLE['label_size'] + 5)

    meta = run.get("meta", {})
    for i, name in enumerate(run["param_names"]):
        ax = _axes[i, i]
        if ax is None:
            continue
            
        tax = ax.twinx()
        tax.set_yticks([])
        tax.set_ylim(0, 1.1)
        
        plotted = False
        if name == "rho_true" and rho_true_dist is not None:
            k = gaussian_kde(rho_true_dist)
            x = np.linspace(np.min(rho_true_dist), np.max(rho_true_dist), 400)
            y = k(x)
            tax.plot(x, y / np.max(y), color="k", lw=STYLE["line_lw"], ls=":", zorder=5)
            plotted = True
            
        if name == "b":
            if b_obs_dist is not None:
                k = gaussian_kde(b_obs_dist)
                x = np.linspace(np.min(b_obs_dist), np.max(b_obs_dist), 400)
                y = k(x)
                tax.plot(x, y / np.max(y), color="k", lw=STYLE["line_lw"], ls=":", zorder=5)
                plotted = True
            else:
                bf = meta.get("B_FIXED", 0.0)
                bs = meta.get("B_SIGMA", 0.1)
                dist = _truncnorm((0.0 - bf) / bs, (1.0 - bf) / bs, loc=bf, scale=bs)
                x = np.linspace(0, 1, 400)
                y = dist.pdf(x)
                tax.plot(x, y / np.max(y), color="k", lw=STYLE["line_lw"], ls=":", zorder=5)
                plotted = True
            
        if not plotted:
            tax.remove()

    if title:
        planet_label = PLANET_LABELS.get(run["planet"], run["planet"])
        fig.suptitle(f"Joint posteriors — {planet_label}",
                     fontsize=STYLE["title_size"] + 5, y=1.01)
    if save:
        _save(fig, f"{run['tag']}_corner", paths, "")
    return fig, _axes


# ══════════════════════════════════════════════════════════════════════════
#  Ring-diagram median values (shared with plot_ring_diagram)
# ══════════════════════════════════════════════════════════════════════════
def _get_ring_diagram_values(run):
    """Extract the median ring-diagram parameter values from a run.

    Returns a dict with keys ``fe``, ``ir``, ``theta``, ``p``, ``tau`` — the same
    values that :func:`plot_ring_diagram` uses to draw the projected ring system.
    """
    chain = run["chain"]; pnames = run["param_names"]; meta = run["meta"]

    def _get(name, default):
        return chain[:, pnames.index(name)] if name in pnames else np.full(len(chain), default)

    # If a parameter is fixed, it is absent from ``param_names``/``chain``.
    # Use the explicit fixed values saved in metadata so annotations/ring inset
    # reflect the actual run configuration.
    p_fixed = meta.get("P_FIXED_VALUE", meta.get("p_min", meta.get("p_mean_ref", 0.08)))
    tau_fixed = meta.get("TAU_FIXED", 0.5)

    return dict(
        fe=float(np.median(_get("fe", meta.get("FE_MAX", 5.0) / 2))),
        ir=float(np.median(_get("ir", 45.0))),
        theta=float(np.median(_get("theta", 90.0))),
        p=float(np.median(_get("p", p_fixed))),
        tau=float(np.median(_get("tau", tau_fixed))),
    )


# ══════════════════════════════════════════════════════════════════════════
#  Ring geometry diagram
# ══════════════════════════════════════════════════════════════════════════
def plot_ring_diagram(run, ax=None, paths=None, scale=0.2, dx=0.0):
    """Draw the median-posterior ring geometry projected onto the stellar disk.

    Uses the same projected-geometry convention as the ``exorings`` forward model:
    ``i_R`` and ``theta`` are in degrees, with projected ring axes
    ``A = f_e p`` and ``B = A cos(i_R)``.

    Parameters
    ----------
    dx : float
        Horizontal offset of the diagram centre in axes fraction (useful when the
        inset sits near a figure edge).
    """
    meta = run["meta"]
    ring_vals = _get_ring_diagram_values(run)
    fe = ring_vals["fe"]
    ir = ring_vals["ir"]
    theta = ring_vals["theta"]
    p = ring_vals["p"]
    tau = ring_vals["tau"]
    fi = meta.get("FI_FIXED", 1.0)

    own_fig = ax is None
    if own_fig:
        fig = plt.figure(figsize=(3, 3)); ax = fig.add_subplot(111)
    else:
        fig = ax.get_figure()
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_axis_off()
    ax.set_aspect("equal", adjustable="box")

    col = planet_color(run["planet"])

    # Geometric scales in stellar-radius units: Rp/R* = p, Re/R* = fe*p, Ri/R* = fi*p.
    Rp = float(p)
    Re = float(fe) * Rp
    Ri = float(fi) * Rp
    if Re <= 0 or Rp <= 0:
        raise ValueError(f"Invalid ring geometry (Rp={Rp}, Re={Re})")

    # Projected ring ellipse (exorings convention): B = A * cos(i_R), angle = theta.
    cos_ir = float(np.cos(np.deg2rad(ir)))
    Aout, Bout = Re, Re * cos_ir
    Ain, Bin = Ri, Ri * cos_ir

    # Ring attenuation factor (exorings/geotrans convention):
    #   beta = 1 - exp(-tau / cos(i_R)).
    # Use |cos(i_R)| for numerical safety and clamp to [0, 1] for alpha mapping.
    mu = max(abs(cos_ir), 1e-6)
    tau_eff = max(float(tau), 0.0)
    beta = float(np.clip(1.0 - np.exp(-tau_eff / mu), 0.0, 1.0))

    # Keep visibility for very transparent rings while still encoding beta.
    ring_fill_alpha = 0.08 + 0.62 * beta
    ring_edge_alpha = 0.35 + 0.60 * beta
    ring_inner_edge_alpha = 0.25 + 0.45 * beta

    fh = scale / Aout
    fv = fh
    C = np.array([0.5 + dx, 0.5])

    # Outer ring body and inner cutout to show an annulus, not a solid disk.
    ring_body = mpl.patches.Ellipse(
        xy=C, width=2 * fh * Aout, height=2 * fv * Bout, angle=float(theta),
        facecolor=col, edgecolor=col, alpha=ring_fill_alpha, lw=STYLE["line_lw"],
        transform=ax.transAxes, zorder=8,
    )
    ring_hole = mpl.patches.Ellipse(
        xy=C, width=2 * fh * Ain, height=2 * fv * Bin, angle=float(theta),
        facecolor="white", edgecolor="none", alpha=1.0,
        transform=ax.transAxes, zorder=9,
    )
    ring_edge_out = mpl.patches.Ellipse(
        xy=C, width=2 * fh * Aout, height=2 * fv * Bout, angle=float(theta),
        fill=False, edgecolor=col, alpha=ring_edge_alpha, lw=STYLE["line_lw"],
        transform=ax.transAxes, zorder=10,
    )
    ring_edge_in = mpl.patches.Ellipse(
        xy=C, width=2 * fh * Ain, height=2 * fv * Bin, angle=float(theta),
        fill=False, edgecolor=col, alpha=ring_inner_edge_alpha, lw=STYLE["line_lw_thin"],
        transform=ax.transAxes, zorder=10,
    )
    planet = mpl.patches.Circle(
        xy=C, radius=fh * Rp, facecolor="k", edgecolor="k", lw=0.0,
        transform=ax.transAxes, zorder=11,
    )

    ax.add_patch(ring_body)
    ax.add_patch(ring_hole)
    ax.add_patch(ring_edge_out)
    ax.add_patch(ring_edge_in)
    ax.add_patch(planet)
    # Red centre mark — same meaning as the red median markers on the corner panels.
    ax.plot(C[0], C[1], "o", color="red", ms=8, mew=1.5, mec="darkred",
            transform=ax.transAxes, zorder=12, clip_on=False)

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
        corner_png = paths.figures_dir() / f"{run['tag']}_corner.png"
        if not corner_png.exists():
            fig_c, _ = plot_corner(run, paths=paths)
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
            for s in _stats_legend_lines(stats, unit=obs_meta(key)["unit"]):
                ax.plot([], [], color="none", label=s)
            tick = r"$\checkmark$" if key in in_like else r"$\times$"
            _style_ax(ax, xlabel=lbl, title=f"{key} {tick}", legend=True)

    fig.suptitle(f"{PLANET_LABELS.get(planet, planet)} — Posterior results",
                 fontsize=STYLE["title_size"] + 2, y=0.98)
    _save(fig, f"{run['tag']}_panel", paths, "panel")
    return fig


def _run_title(run, z1=None):
    r"""``L_KDE: [obs…]   theta: [ring params…]   eta: [nuisance…]``.

    Parameters appearing before ``rho_true`` in ``param_names`` are treated as the
    ring-geometry vector ``θ``; ``rho_true`` and everything after it go into ``η``.
    """
    kde_symbols = r" \; ".join(obs_meta(k)["symbol"].replace("$", "")
                               for k in run["kde_obs"])
    params, etas, qeta = [], [], False
    for p in run["param_names"]:
        if "true" in param_meta(p)["symbol"] or "$b$" in param_meta(p)["symbol"]:
            qeta = True
        sym = param_meta(p)["symbol"].replace("$", "")
        if not qeta:
            params.append(sym)
        else:
            etas.append(sym)
    par_symbols = r" \; ".join(params)
    eta_symbols = r" \; ".join(etas)
    z1_suffix = ""
    if z1 is not None and np.isfinite(z1):
        z1_suffix = rf"\; (\langle z_1 \rangle = {z1:.2f})"

    return (rf"$\mathcal{{L}}_{{\mathrm{{KDE}}}}\text{{: }}"
            rf"\left[ {kde_symbols} \right]{z1_suffix}"
            rf" \qquad \boldsymbol{{{{\theta}}}}\text{{: }}"
            rf"\left[ {par_symbols} \right]"
            rf" \qquad \boldsymbol{{{{\eta}}}}\text{{: }}"
            rf"\left[ {eta_symbols} \right]$")


def _overlay_ring_medians(axes, pnames, ring_vals):
    """Mark ring-diagram medians on a corner axes grid (1-D lines + 2-D dots)."""
    ndim = len(pnames)
    for col_idx in range(ndim):
        px = pnames[col_idx]
        if px not in ring_vals:
            continue
        for row_idx in range(col_idx + 1, ndim):
            py = pnames[row_idx]
            if py not in ring_vals:
                continue
            ax = axes[row_idx, col_idx]
            if ax is not None:
                ax.plot(ring_vals[px], ring_vals[py],
                        "o", color="red", ms=8, mew=1.5,
                        mec="darkred", zorder=100)
    for idx in range(ndim):
        pname = pnames[idx]
        if pname not in ring_vals:
            continue
        ax = axes[idx, idx]
        if ax is not None:
            ax.axvline(ring_vals[pname], color="red", ls="-",
                       lw=1.5, alpha=0.9, zorder=100)


def _bestfit_medians_line(run, include_metrics=True):
    """Return the medians line used in panel titles (shared by corner + PPC)."""
    ring_vals = _get_ring_diagram_values(run)
    free = set(run["param_names"])

    def _sym(name, latex):
        return rf"{latex}^\dagger" if name not in free else latex

    logz_str = ""
    if include_metrics and run.get("logz") is not None and np.isfinite(run["logz"]):
        logz_str = rf" ($\ln \mathcal{{Z}} = {run['logz']:.3f}"
        if run.get("logl") is not None and len(run.get("param_names", [])) > 0:
            max_logl = np.max(run["logl"])
            k = len(run["param_names"])
            aic = 2 * k - 2 * max_logl
            logz_str += rf", \mathrm{{AIC}} = {aic:.1f}"
        logz_str += "$)"

    return (
        rf"Medians: "
        rf"${_sym('p', 'p')}={ring_vals['p']:.3f}$, "
        rf"${_sym('fe', 'f_e')}={ring_vals['fe']:.2f}$, "
        rf"${_sym('ir', 'i_R')}={ring_vals['ir']:.1f}^\circ$, "
        rf"${_sym('theta', r'\theta')}={ring_vals['theta']:.1f}^\circ$, "
        rf"${_sym('tau', r'\tau')}={ring_vals['tau']:.2f}$"
        + logz_str
    )


def _apply_panel_title(fig, axes, run, pnames, main_title="Joint posterior results (w/ nuisance)"):
    """Title anchored above the ``f_e`` (or first) diagonal axis title.

    Places a figure-level text label ``1.5 ×`` the ``f_e`` title height above that
    label. The medians line lists ``p, f_e, i_R, θ, τ``; symbols of parameters
    that were held fixed (absent from ``run['param_names']``) carry a dagger.
    """
    planet_label = PLANET_LABELS.get(run["planet"], run["planet"])
    ring_vals = _get_ring_diagram_values(run)
    fontsize = STYLE["title_size"] + 5
    free = set(run["param_names"])

    def _sym(name, latex):
        return rf"{latex}^\dagger" if name not in free else latex

    # Need a renderer to measure the dynesty axis-title position.
    fig.canvas.draw()
    idx = pnames.index("fe") if "fe" in pnames else 0
    ax0 = axes[idx, idx]
    title = ax0.title
    renderer = fig.canvas.get_renderer()
    bb = title.get_window_extent(renderer=renderer)
    # Top centre of the f_e axis title, in figure coordinates.
    _x_fig, y_top = fig.transFigure.inverted().transform(
        ((bb.x0 + bb.x1) / 2.0, bb.y1))

    # Offset = 1.5 × height of the f_e axis title (figure fraction).
    fig_h_px = fig.bbox.height
    dy = 1.5 * (bb.y1 - bb.y0) / fig_h_px

    medians = _bestfit_medians_line(run)
    lines = [
        f"{planet_label} — {main_title}",
        _run_title(run),
        medians,
    ]
    # ``Text.linespacing`` is unreliable when ``text.usetex=True`` (PAPER_STYLE):
    # TeX owns the baselineskip and ignores matplotlib's multiplier, so a
    # multiline ``fig.text``/``suptitle`` looks cramped. Place each line with an
    # explicit figure-fraction step instead (works for both usetex and mathtext).
    linespacing = 1.85
    line_step = linespacing * (fontsize / 72.0) / fig.get_figheight()
    y0 = y_top + dy  # bottom of the title block (above the f_e axis title)
    for i, line in enumerate(reversed(lines)):
        fig.text(
            0.5, y0 + i * line_step, line,
            ha="center", va="bottom", fontsize=fontsize,
            transform=fig.transFigure, clip_on=False,
        )
    return 1.0


def _ring_inset_rect(ndim, ring_frac=None, pad=0.01, top=1.0):
    """Figure-fraction rect for the ring inset in the free upper-right triangle."""
    frac = ring_frac if ring_frac is not None else min(0.2 + 0.025 * ndim, 0.40)
    x0 = 1.0 - frac - pad
    y0 = min(1.0 - frac - pad, top - frac - pad)
    y0 = max(y0, pad)
    return [x0, y0, frac, frac]


def plot_results_panel_inset(run, rho_true_dist=None, b_obs_dist=None, paths=None, ring_frac=None, pad=0.01,
                             run_tag_suffix="corner", title=True):
    """Square corner plot with the inferred ring geometry inset in the upper-right.

    This is the per-planet summary figure: the joint posterior over ring and nuisance
    parameters, plus — drawn in the empty upper-right triangle that a corner plot always
    leaves free — a sky-plane sketch of the ring system at the posterior medians.

    Red markers on the 1-D / 2-D corner panels (and the red centre of the planet disk)
    show the same median values used by :func:`plot_ring_diagram`.

    Unlike :func:`plot_results_panel`, the corner is rendered **live** by
    :func:`plot_corner` rather than re-read from a saved PNG, so the result stays
    resolution-independent and needs no image post-processing.

    Parameters
    ----------
    ring_frac : float, optional
        Side of the inset as a fraction of the figure. Defaults to
        ``min(0.2 + 0.025 * ndim, 0.40)``, which keeps the sketch inside the free
        triangle as the number of parameters grows.
    """
    pnames = list(run["param_names"])
    ndim = len(pnames)
    fig, axes = plot_corner(run, rho_true_dist=rho_true_dist, b_obs_dist=b_obs_dist, paths=None, title=False, save=False)
    if fig is None:
        return None

    ring_vals = _get_ring_diagram_values(run)
    _overlay_ring_medians(axes, pnames, ring_vals)

    side = ndim * STYLE["fig_w_single"] * 1.05
    fig.set_size_inches(side, side)
    fig.set_dpi(STYLE["fig_dpi"])

    ax_ring = fig.add_axes(_ring_inset_rect(ndim, ring_frac, pad))
    ax_ring.set_axis_off()
    try:
        plot_ring_diagram(run, ax=ax_ring)
    except Exception as e:
        ax_ring.text(0.5, 0.5, f"Ring diagram\nunavailable\n({e})", ha="center",
                     va="center", color="gray", fontsize=STYLE["annot_size"] + 2,
                     transform=ax_ring.transAxes)

    if title:
        _apply_panel_title(fig, axes, run, pnames)

    _save(fig, f"{run['tag']}_{run_tag_suffix}", paths, "")
    return fig


def plot_corner_reduced(run, paths=None, ax_grid=None, title=True, save=True):
    """Corner plot restricted to ring-geometry parameters (drops ``rho_*`` and ``b``).

    Returns ``(fig, axes, plotted_param_names)``.
    """
    if not HAS_DYNESTY:
        print("dynesty is not installed — cannot draw the corner plot.")
        return None, None, []
    if run.get("dres") is None:
        print(f"No dynesty results for {run['tag']} — cannot draw the corner plot.\n"
              "  The .npz must contain 'samples' (see photoring.io.load_run).")
        return None, None, []

    pnames = run["param_names"]
    dims = [i for i, p in enumerate(pnames) if "rho" not in p and p != "b"]
    plotted_pnames = [pnames[i] for i in dims]
    labels = [param_meta(p)["label"] for p in plotted_pnames]
    kwargs = dict(
        labels=labels, show_titles=True,
        title_kwargs={"fontsize": STYLE["tick_size"] + 10},
        quantiles=STYLE["corner_quantiles"],
        color=planet_color(run["planet"], "corner"),
        smooth=STYLE["corner_smooth"],
        dims=dims,
    )
    if ax_grid is not None:
        kwargs["fig"] = (ax_grid[0, 0].get_figure(), ax_grid)
    fig, axes = _dyplot.cornerplot(run["dres"], **kwargs)

    for ax in axes.flatten():
        if ax is not None:
            ax.tick_params(axis="both", which="major", labelsize=STYLE["label_size"] + 5)
            ax.xaxis.label.set_size(STYLE["label_size"] + 5)
            ax.yaxis.label.set_size(STYLE["label_size"] + 5)

    if title:
        planet_label = PLANET_LABELS.get(run["planet"], run["planet"])
        fig.suptitle(f"Joint posteriors — {planet_label}",
                     fontsize=STYLE["title_size"] + 5, y=1.01)
    if save:
        _save(fig, f"{run['tag']}_corner_reduced", paths, "")
    return fig, axes, plotted_pnames


def plot_results_panel_reduced_inset(run, paths=None, ring_frac=None, pad=0.01,
                                     run_tag_suffix="corner_reduced",
                                     title=True):
    """Like :func:`plot_results_panel_inset` but only for ring-geometry parameters."""
    fig, axes, plotted_pnames = plot_corner_reduced(
        run, paths=None, title=False, save=False)
    if fig is None:
        return None

    ndim = len(plotted_pnames)
    ring_vals = _get_ring_diagram_values(run)
    _overlay_ring_medians(axes, plotted_pnames, ring_vals)

    side = ndim * STYLE["fig_w_single"] * 1.05
    fig.set_size_inches(side, side)
    fig.set_dpi(STYLE["fig_dpi"])

    ax_ring = fig.add_axes(_ring_inset_rect(ndim, ring_frac, pad))
    ax_ring.set_axis_off()
    try:
        plot_ring_diagram(run, ax=ax_ring, dx=-0.15)
    except Exception as e:
        ax_ring.text(0.5, 0.5, f"Ring diagram\nunavailable\n({e})", ha="center",
                     va="center", color="gray", fontsize=STYLE["annot_size"] + 2,
                     transform=ax_ring.transAxes)

    if title:
        _apply_panel_title(fig, axes, run, plotted_pnames, main_title="Joint posterior results (w/o nuisance)")

    _save(fig, f"{run['tag']}_{run_tag_suffix}", paths, "")
    return fig


# ══════════════════════════════════════════════════════════════════════════
#  Observable posteriors (pipeline step 1)
# ══════════════════════════════════════════════════════════════════════════
def gauss(x, mu, sigma):
    """Normal pdf — used to draw a literature value from its point estimate + error."""
    return np.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))


def gauss_trunc(x, mu, sigma, lo=0.0, hi=1.0):
    """Normal pdf truncated to ``[lo, hi]``.

    Used for the impact parameter, whose physical range is bounded: a plain Gaussian
    around a near-zero point estimate would put weight at ``b < 0``.
    """
    a, b_ = (lo - mu) / sigma, (hi - mu) / sigma
    return _truncnorm.pdf(x, a, b_, loc=mu, scale=sigma)


def gauss_asym(x, mu, sigma_minus, sigma_plus):
    """Two-sided Gaussian with different widths below and above ``mu``.

    Represents a published value reported as ``mu (+sigma_plus, -sigma_minus)``. The
    normalisation makes the two halves join continuously and integrate to one.
    """
    x = np.asarray(x, dtype=float)
    sigma = np.where(x < mu, sigma_minus, sigma_plus)
    norm = np.sqrt(2 / np.pi) / (sigma_minus + sigma_plus)
    return norm * np.exp(-0.5 * ((x - mu) / sigma) ** 2)


def _lit_curve(ax, key, entry, color, label=None, n=600, span=3.0):
    """Draw one literature reference curve; returns its x-range for limit bookkeeping."""
    mu, sigma = entry["mu"], entry["sigma"]
    xg = np.linspace(mu - span * sigma, mu + span * sigma, n)
    yg = gauss_trunc(xg, mu, sigma) if key == "b_obs" else gauss(xg, mu, sigma)
    ax.plot(xg, yg, color=color, lw=STYLE["lit_lw"], ls=STYLE["lit_ls"],
            alpha=STYLE["lit_alpha"], zorder=5, label=label)
    return xg.min(), xg.max()


def plot_observable_posteriors(ttv_by_planet, keys=None, lit=None, paths=None,
                              run_tag="observables", title=None):
    """Grid of transit-observable posteriors: **one row per planet**, one column per key.

    Each panel shows the TTV posterior as a filled histogram plus its KDE, the median
    and 68% interval (see :func:`_annotate_stats`), and — where available — published
    values as unfilled reference curves. Only the observables a given source reports are
    drawn, so a column may legitimately have no literature overlay.

    Parameters
    ----------
    ttv_by_planet : dict
        ``{planet: ttv_dict}``, each from :func:`photoring.io.load_observables`.
        Row order follows this dict's insertion order.
    keys : list of str, optional
        Observable keys (of :data:`OBS_META`) to show as columns.
        Defaults to ``["delta", "T14", "T23", "b_obs", "aR"]``.
    lit : dict, optional
        ``{planet: {source: {obs_key: {"mu":…, "sigma":…}}}}``, e.g.
        :func:`photoring.literature.observables`. Omit to draw posteriors only.
    """
    from . import literature as _lit_mod

    keys = list(keys or ["delta", "T14", "T23", "b_obs", "aR"])
    planets = list(ttv_by_planet)
    lit = lit or {}
    nrows, ncols = len(planets), len(keys)

    fig, axes = plt.subplots(
        nrows, ncols,
        figsize=(STYLE["fig_w_ppc"] * ncols * 1.08, STYLE["fig_h_single"] * nrows * 1.1),
        gridspec_kw=dict(wspace=STYLE["wspace"], hspace=STYLE.get("hspace", 0.2) * 3),
        squeeze=False)

    sources_seen = []
    for row, planet in enumerate(planets):
        ttv = ttv_by_planet[planet]
        fill = planet_color(planet, "fill")
        line = planet_color(planet, "line")
        for col_i, key in enumerate(keys):
            ax = axes[row][col_i]
            meta = obs_meta(key)
            v = np.asarray(ttv.get(meta["df_col"], []), dtype=float)
            v = v[np.isfinite(v)] * meta["scale"]
            if len(v) < 5:
                ax.set_axis_off()
                continue

            _hist1d(ax, v, fill, "", alpha=0.5, zorder=2)
            _kde_line(ax, v, line, label=PLANET_LABELS.get(planet, planet),
                      lw=STYLE["line_lw"])

            # Literature overlays, and the x-range they need to stay visible.
            xmin, xmax = float(v.min()), float(v.max())
            for source, obs in lit.get(planet, {}).items():
                if key not in obs:
                    continue
                if source not in sources_seen:
                    sources_seen.append(source)
                lo, hi = _lit_curve(ax, key, obs[key], _lit_mod.color(source))
                xmin, xmax = min(xmin, lo), max(xmax, hi)
            if key == "b_obs":
                xmin = 0.0
            pad = 0.01 * (xmax - xmin)
            ax.set_xlim(xmin - pad, xmax + pad)

            _annotate_stats(ax, v, symbol=meta["symbol"], unit=meta["unit"],
                            color="k", vline_color=line, xpos="left", ypos=0.97)
            ax.set_ylabel("")
            if row == nrows - 1:
                ax.set_xlabel(meta["xlabel"], labelpad=8, fontsize=STYLE["label_size"])
            ax.xaxis.set_minor_locator(AutoMinorLocator())
            ax.yaxis.set_minor_locator(AutoMinorLocator())

    fig.supylabel("Probability Density", fontsize=STYLE["label_size"] + 4, x=0.085)
    if title:
        fig.suptitle(title, fontsize=STYLE["label_size"] + 3, y=0.98)

    # One shared legend: a patch per planet, a line per literature source.
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    handles = [Patch(facecolor=planet_color(p, "fill"),
                     edgecolor=planet_color(p, "line"), lw=0.8, alpha=0.75,
                     label=PLANET_LABELS.get(p, p)) for p in planets]
    handles += [Line2D([0], [0], color=_lit_mod.color(s), lw=STYLE["lit_lw"],
                       ls=STYLE["lit_ls"], label=s) for s in sources_seen]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, -0.02),
               ncol=3, fontsize=STYLE["legend_size"], framealpha=0.92,
               edgecolor="#cccccc", fancybox=False, handlelength=2.0,
               handletextpad=0.5, columnspacing=1.3, labelspacing=0.35)

    fig.tight_layout(rect=[0, 0.07, 1, 0.96])
    _save(fig, run_tag, paths, "observables")
    return fig


# ══════════════════════════════════════════════════════════════════════════
#  Asterodensity profiling — the stellar-density anomaly
# ══════════════════════════════════════════════════════════════════════════
def plot_asterodensity_profiling(ttv_by_planet, rho_true_samples=None, lit_rho=None,
                                 paths=None, run_tag="rho_obs_comparison", title=None,
                                 annot_offsets=None, rho_true_label=None,
                                 legend_loc="upper left"):
    """The stellar-density anomaly: transit-inferred vs independently-measured density.

    Under the standard (ringless, unblended, circular-orbit) transit model, every planet
    of a system must yield the *same* stellar density. This figure puts each planet's
    transit-derived ``rho_star,obs`` on one axis together with an independent estimate of
    the true density, so a disagreement — between planets, or against the independent
    value — is visible directly. Such a disagreement is what the photo-ring hypothesis
    then tries to explain.

    Parameters
    ----------
    ttv_by_planet : dict
        ``{planet: ttv_dict}``; the ``rho_obs`` observable of each is plotted.
    rho_true_samples : array, optional
        Samples of the star's true density [g/cm^3] from an independent method
        (e.g. isochrone fitting), drawn filled for contrast against the transit values.
    lit_rho : dict, optional
        ``{source: {"mu":…, "sigma_minus":…, "sigma_plus":…}}`` of independent
        determinations, e.g. :func:`photoring.literature.rho_star`. Drawn dotted.
    annot_offsets : dict, optional
        ``{planet: (x_data, ypos, offset)}`` to nudge a label away from a collision.
    """
    from . import literature as _lit_mod

    meta = obs_meta("rho_obs")
    lit_rho = lit_rho or {}
    annot_offsets = annot_offsets or {}

    fig, ax = plt.subplots(figsize=(STYLE["fig_w_ppc"] * 2.0, STYLE["fig_h_single"] * 1.8))
    xs_lo, xs_hi = [], []

    for planet, ttv in ttv_by_planet.items():
        v = np.asarray(ttv.get(meta["df_col"], []), dtype=float)
        v = v[np.isfinite(v)] * meta["scale"]
        if len(v) < 5:
            continue
        fill = planet_color(planet, "fill")
        line = planet_color(planet, "line")
        label = PLANET_LABELS.get(planet, planet)
        _hist1d(ax, v, fill, "", alpha=0.45, zorder=2)
        _kde_line(ax, v, line, label=f"{label} (This work)", lw=STYLE["line_lw"])
        xs_lo.append(v.min()); xs_hi.append(v.max())

        # (x_in_data, ypos, offset[, xpos]) — xpos picks which side the label grows from.
        spec = annot_offsets.get(planet, (None, 0.98, 0.0))
        x_at, ypos, off = spec[:3]
        xpos = spec[3] if len(spec) > 3 else "right"
        _annotate_stats(ax, v, symbol=label, unit=meta["unit"], color=line,
                        vline_color=line, xpos=xpos, ypos=ypos, offset=off,
                        x=x_at, sep="\n", show_interval=False)

    # Independent (non-transit) density: the reference the anomaly is measured against.
    if rho_true_samples is not None and len(np.ravel(rho_true_samples)) > 5:
        rho_true = np.asarray(rho_true_samples, dtype=float).ravel()
        rho_true = rho_true[np.isfinite(rho_true)]
        c_ref = STYLE.get("c_rho_true", STYLE["c_prior"])
        _hist1d(ax, rho_true, c_ref, "", alpha=0.20, zorder=1)
        _kde_line(ax, rho_true, c_ref,
                  label=rho_true_label or "Independent (isochrone)",
                  lw=STYLE["lit_lw"], alpha=0.85)
        xs_lo.append(rho_true.min()); xs_hi.append(rho_true.max())

    for source, entry in lit_rho.items():
        sm, sp = entry["sigma_minus"], entry["sigma_plus"]
        span = 4 * max(sm, sp)
        xg = np.linspace(entry["mu"] - span, entry["mu"] + span, 600)
        ax.plot(xg, gauss_asym(xg, entry["mu"], sm, sp), color=_lit_mod.color(source),
                lw=STYLE["lit_lw"], ls=":", alpha=STYLE["lit_alpha"], zorder=6,
                label=source)
        xs_lo.append(xg.min()); xs_hi.append(xg.max())

    if xs_lo:
        lo, hi = min(xs_lo), max(xs_hi)
        pad = 0.05 * (hi - lo)
        ax.set_xlim(lo - pad, hi + pad)
    ax.set_ylim(bottom=0)
    ax.set_xlabel(rf"Stellar density $\rho_{{\star}}$ [{meta['unit']}]",
                  fontsize=STYLE["label_size"] + 2)
    ax.set_ylabel("Probability Density", fontsize=STYLE["label_size"] + 2)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.legend(fontsize=STYLE["legend_size"] - 1, framealpha=0.92, edgecolor="#cccccc",
              fancybox=False, loc=legend_loc)
    if title:
        ax.set_title(title, fontsize=STYLE["label_size"] + 1)

    fig.tight_layout()
    _save(fig, run_tag, paths, "observables")
    return fig


# ══════════════════════════════════════════════════════════════════════════
#  Segment consistency
# ══════════════════════════════════════════════════════════════════════════
def plot_segment_consistency(segments, combined, keys=None, ncols=3, paths=None,
                             run_tag="observables_segments", title=None,
                             segment_labels=None, combined_label="Final"):
    """Per-segment posteriors against their importance-sampled combination.

    When a planet's light curve had to be split into independent temporal segments (see
    :func:`photoring.observables.combine_segments`), this figure is the diagnostic that
    the combination is defensible: it shows each segment's posterior next to the combined
    one, per observable. Segments that disagree by more than their widths point to a
    systematic difference between epochs, not to statistical scatter.

    Parameters
    ----------
    segments : sequence of pandas.DataFrame
        Per-segment observables (output of :func:`photoring.observables.derive_observables`).
    combined : pandas.DataFrame
        The combined posterior returned by
        :func:`photoring.observables.combine_segments`.
    keys : list of str, optional
        Observable keys to panel. Defaults to all six of :data:`OBS_META`.
    """
    keys = list(keys or ["delta", "T14", "T23", "rho_obs", "b_obs", "aR"])
    nrows = (len(keys) + ncols - 1) // ncols
    seg_colors = STYLE.get("c_segments") or _PLANET_COLOR_CYCLE
    segment_labels = segment_labels or [f"Seg. {i}" for i in range(1, len(segments) + 1)]

    fig, axes = plt.subplots(
        nrows, ncols,
        figsize=(STYLE["fig_w_ppc"] * ncols * 1.35, STYLE["fig_h_single"] * nrows * 1.45),
        gridspec_kw=dict(wspace=STYLE["wspace"], hspace=0.35), squeeze=False)
    flat = axes.ravel()

    for i, key in enumerate(keys):
        ax = flat[i]
        meta = obs_meta(key)
        # In a segment DataFrame the density column is the raw kg/m^3 'rho_obs'.
        src = "rho_obs" if key == "rho_obs" else meta["df_col"]
        scale = 1 / 1000.0 if key == "rho_obs" else meta["scale"]

        for s_i, seg in enumerate(segments):
            sv = np.asarray(seg.get(src, []), dtype=float)
            sv = sv[np.isfinite(sv)] * scale
            if len(sv) < 20:
                continue
            c = seg_colors[s_i % len(seg_colors)]
            _hist1d(ax, sv, c, "", alpha=0.25, zorder=2)
            _kde_line(ax, sv, c, label=segment_labels[s_i], lw=1.2, alpha=0.85)

        mv = np.asarray(combined.get(src, []), dtype=float)
        mv = mv[np.isfinite(mv)] * scale
        if len(mv) >= 5:
            _hist1d(ax, mv, planet_color("b", "fill"), "", alpha=0.25, zorder=3)
            _kde_line(ax, mv, planet_color("b", "line"), label=combined_label,
                      lw=STYLE["line_lw"])
            _annotate_stats(ax, mv, symbol=meta["symbol"], unit=meta["unit"], color="k",
                            vline_color=planet_color("b", "line"), xpos="right",
                            ypos=1.01, offset=-0.02, show_interval=False)
            med, std = float(np.median(mv)), float(np.std(mv))
            ax.set_xlim(0 if key == "b_obs" else med - 7 * std, med + 7 * std)

        ax.set_xlabel(meta["label"], labelpad=6)
        ax.set_ylabel("Probability Density" if i % ncols == 0 else "")
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())

    for i in range(len(keys), nrows * ncols):
        flat[i].set_axis_off()

    flat[len(keys) - 1].legend(fontsize=STYLE["legend_size"], framealpha=0.9,
                               edgecolor="#cccccc", fancybox=False)
    if title:
        fig.suptitle(title, fontsize=STYLE["label_size"] + 1, y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
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
