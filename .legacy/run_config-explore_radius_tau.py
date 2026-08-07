# run_config_explore_radius_tau.py
DEFAULT_CASE = "kepler_51"

# Observables to include in the KDE likelihood
KDE_VARIANTS = [
    ["delta", "T14", "rho_obs"],
]

# Grid of nuisance parameters (rho_star,true and impact parameter b)
FREE_PARAM_VARIANTS = [
    {"RHO_TRUE_FREE": True,  "B_FREE": True},
]

# Toggles for ring opacity (tau) and planetary radius ratio (p)
TAU_FREE_VARIANTS = [False]
P_FREE_VARIANTS = [False]

FORWARD_MODEL_VARIANTS = ["exorings"]

# Planets to run
PLANETS = ["b","d"]

# Multiple intermediate values for p
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

# Multiple fixed values for tau (only applies if TAU_FREE=False)
TAU_FIXED_RUNS = [
    {"label": "T1", "value": 0.5},
    {"label": "T2", "value": 1.0},
    {"label": "T3", "value": 2.0},
]
