# run_config-density.py (alphatest branch)
# Explores fixing rho_true to specific values.
DEFAULT_CASE = "kepler_51"

# Observables to include in the KDE likelihood
KDE_VARIANTS = [
    ["delta", "T14", "T23", "rho_obs"],
]

# Grid of nuisance parameters (rho_star,true and impact parameter b)
# We set RHO_TRUE_FREE to False so that RHO_FIXED_RUNS will be used.
FREE_PARAM_VARIANTS = [
    {"RHO_TRUE_FREE": False,  "B_FREE": True},
]

# Toggles for ring opacity (alpha) and planetary radius ratio (p)
ALPHA_FREE_VARIANTS = [True]
P_FREE_VARIANTS = [True]

FORWARD_MODEL_VARIANTS = ["exorings"]

# Planets to run
PLANETS = ["b", "d"]

# Specific fixed values for rho_true (only applies if RHO_TRUE_FREE=False)
RHO_FIXED_RUNS = [
    {"label": "BM",  "value": 1.9},
    {"label": "MLR", "value": 2.0},
    {"label": "BP1", "value": 2.1},
    {"label": "BP2", "value": 2.3},
]
