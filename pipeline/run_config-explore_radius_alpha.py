# run_config-explore_radius_alpha.py  (alphatest branch)
# Ring opacity parametrized by alpha = exp(-tau), Uniform[0, 1].
# alpha=1 => transparent ring (tau=0), alpha->0 => opaque ring (tau->inf).
DEFAULT_CASE = "kepler_51"

# Observables to include in the KDE likelihood
KDE_VARIANTS = [
    ["delta", "T14", "rho_obs"],
]

# Grid of nuisance parameters (rho_star,true and impact parameter b)
FREE_PARAM_VARIANTS = [
    {"RHO_TRUE_FREE": True,  "B_FREE": True},
]

# Toggles for ring opacity (alpha) and planetary radius ratio (p)
ALPHA_FREE_VARIANTS = [False]
P_FREE_VARIANTS = [False]

FORWARD_MODEL_VARIANTS = ["exorings"]

# Planets to run
PLANETS = ["b", "d"]

# When P_FREE=False, fix p to multiple intermediate values.
# 'fraction' is between 0 (p_min) and 1 (p_max = p_mean_ref).
P_FIXED_RUNS = [
    {"label": "P1", "fraction": 0.1},
    {"label": "P2", "fraction": 0.2},
    {"label": "P3", "fraction": 0.3},
    {"label": "P4", "fraction": 0.4},
    {"label": "P5", "fraction": 0.5},
    {"label": "P6", "fraction": 0.6},
    {"label": "P7", "fraction": 0.7},
    {"label": "P8", "fraction": 0.8},
    {"label": "P9", "fraction": 0.9},
]

# Multiple fixed values for alpha (only applies if ALPHA_FREE=False)
# alpha = exp(-tau): e.g. exp(-0.5)=0.607, exp(-1)=0.368, exp(-2)=0.135
ALPHA_FIXED_RUNS = [
    {"label": "A1", "value": 0.6065},   # equiv. tau=0.5
    {"label": "A2", "value": 0.3679},   # equiv. tau=1.0
    {"label": "A3", "value": 0.1353},   # equiv. tau=2.0
]
