"""Published reference values, for overlaying on the pipeline's posterior figures.

Two tables per case, both keyed by source name so a single colour map covers both:

- :data:`LIT_OBSERVABLES` — per planet, per source, the reported transit observables.
  Overlaid as normal distributions on the observables figure. Only the observables a
  given source actually reports are listed; missing entries are simply not drawn.
- :data:`LIT_RHO_STAR` — independent (non-transit) determinations of the *stellar*
  density, used by the asterodensity-profiling figure. These carry asymmetric
  uncertainties, so they are drawn as two-sided Gaussians (see
  :func:`~photoring.plotting.gauss_asym`).

Values are in **display units** — the same units :data:`~photoring.plotting.OBS_META`
declares (``delta`` in ppm, durations in hours, densities in g/cm^3) — so they can be
plotted directly against a scaled posterior with no further conversion.

To use a different target, add an entry to :data:`LIT_OBSERVABLES` /
:data:`LIT_RHO_STAR` under your case name, or pass your own dicts to the plotting
functions; nothing here is imported implicitly.
"""

from __future__ import annotations

# ── Kepler-51 ────────────────────────────────────────────────────────────────
# delta values are (Rp/R*)^2 converted to ppm; T14 converted from days to hours.
# Where a source reports asymmetric errors, sigma is their average.
_K51_OBSERVABLES = {
    "b": {
        "Masuda et al. 2024": {
            "delta":   dict(mu=5220.0, sigma=40.0),    # (Rp/R*)^2 = 0.00522 +/- 0.000004
            "T14":     dict(mu=5.754,  sigma=0.020),   # 0.23975 +/- 0.00084 d
            "b_obs":   dict(mu=0.074,  sigma=0.072),
        },
        "Masuda et al. 2014": {
            "delta":   dict(mu=5500.0, sigma=90.0),    # 0.00550 +/- 0.00009
            "b_obs":   dict(mu=0.251,  sigma=0.106),   # avg of (+0.073, -0.138)
            "aR":      dict(mu=61.5,   sigma=1.35),    # avg of (+1.5, -1.2)
        },
        "Libby-Roberts et al. 2020": {
            "delta":   dict(mu=4750.0, sigma=180.0),   # 0.00475 +/- 0.00018
            "b_obs":   dict(mu=0.22,   sigma=0.16),
            "aR":      dict(mu=59.7,   sigma=2.9),
        },
    },
    "d": {
        "Masuda et al. 2024": {
            "delta":   dict(mu=9710.0, sigma=70.0),    # 0.00971 +/- 0.000007
            "T14":     dict(mu=8.402,  sigma=0.029),   # 0.3501 +/- 0.0012 d
            "b_obs":   dict(mu=0.003,  sigma=0.095),
        },
        "Masuda et al. 2014": {
            "delta":   dict(mu=10280.0, sigma=170.0),  # 0.01028 +/- 0.00017
            "b_obs":   dict(mu=0.250,   sigma=0.108),  # avg of (+0.075, -0.141)
            "aR":      dict(mu=124.7,   sigma=2.75),   # avg of (+3.0, -2.5)
        },
        "Libby-Roberts et al. 2020": {
            "delta":   dict(mu=9530.0, sigma=180.0),   # 0.00953 +/- 0.00018
            "b_obs":   dict(mu=0.19,   sigma=0.145),   # avg of (+0.16, -0.13)
            "aR":      dict(mu=124.9,  sigma=3.8),     # avg of (+2.2, -5.4)
        },
        "Libby-Roberts et al. 2025": {
            "delta":   dict(mu=9370.0,  sigma=100.0),  # 0.00937 +/- 0.00010
            "aR":      dict(mu=124.16,  sigma=0.37),
        },
    },
}

# Independent stellar-density determinations [g/cm^3], asymmetric uncertainties.
# These are *not* transit-derived, so they estimate rho_star,true rather than
# rho_star,obs — that contrast is the point of the asterodensity-profiling figure.
_K51_RHO_STAR = {
    "Libby-Roberts et al. 2020": dict(mu=2.03, sigma_minus=0.08, sigma_plus=0.08),
    "Masuda et al. 2024":        dict(mu=2.08, sigma_minus=0.08, sigma_plus=0.08),
}

#: Colour per literature source. Shared by every figure so a source keeps one colour.
LIT_COLORS = {
    "Masuda et al. 2024":        "#C17D11",  # burnt gold
    "Masuda et al. 2014":        "#B22222",  # firebrick red
    "Libby-Roberts et al. 2020": "#5F0F40",  # dark purple
    "Libby-Roberts et al. 2025": "#8B4513",  # saddle brown
}

#: Fallback colour for a source with no entry in :data:`LIT_COLORS`.
LIT_COLOR_DEFAULT = "#999999"

LIT_OBSERVABLES = {"kepler_51": _K51_OBSERVABLES}
LIT_RHO_STAR = {"kepler_51": _K51_RHO_STAR}


def observables(case):
    """Literature transit observables for ``case`` (``{}`` if the case has none)."""
    return LIT_OBSERVABLES.get(case, {})


def rho_star(case):
    """Independent stellar-density determinations for ``case`` (``{}`` if none)."""
    return LIT_RHO_STAR.get(case, {})


def color(source):
    """Colour for a literature source name."""
    return LIT_COLORS.get(source, LIT_COLOR_DEFAULT)
