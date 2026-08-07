# run_config_all.py
DEFAULT_CASE = "kepler_51"

# Observables to include in the KDE likelihood
KDE_VARIANTS = [
    ["delta", "rho_obs"],
    ["delta", "T14", "rho_obs"],
    ["delta", "T14", "T23"],
]

# Grid of nuisance parameters (rho_star,true and impact parameter b)
FREE_PARAM_VARIANTS = [
    {"RHO_TRUE_FREE": False, "B_FREE": False},  # all-fixed (nuisance)
    {"RHO_TRUE_FREE": True,  "B_FREE": False},  # ρ★,true free
    {"RHO_TRUE_FREE": False, "B_FREE": True},   # b free
    {"RHO_TRUE_FREE": True,  "B_FREE": True},   # all-free (nuisance)
]

# Toggles for ring opacity (tau) and planetary radius ratio (p)
TAU_FREE_VARIANTS = [False, True]
P_FREE_VARIANTS = [True, False]

FORWARD_MODEL_VARIANTS = ["exorings"]

# Planets to run
PLANETS = ["b", "d"]

# When P_FREE=False, we can fix p to multiple intermediate values.
# If this list is empty (or None), p is fixed to p_min with no label,
# which replicates the behavior of the original 96-run grid.
P_FIXED_RUNS = []
