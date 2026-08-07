# run_config_full.py
DEFAULT_CASE = "kepler_51"

# Observables to include in the KDE likelihood
KDE_VARIANTS = [
    ["delta", "T14", "T23", "rho_obs"],
]

# Grid of nuisance parameters (rho_star,true and impact parameter b)
FREE_PARAM_VARIANTS = [
    {"RHO_TRUE_FREE": True,  "B_FREE": True},   # all-free (nuisance)
]

# Toggles for ring opacity (tau) and planetary radius ratio (p)
TAU_FREE_VARIANTS = [True]
P_FREE_VARIANTS = [True]

FORWARD_MODEL_VARIANTS = ["exorings"]

# Planets to run
PLANETS = ["b", "d"]
