# run_config-selection.py  (alphatest branch)
# Ring opacity parametrized by alpha = exp(-tau), Uniform[0, 1].
# alpha=1 => transparent ring (tau=0), alpha->0 => opaque ring (tau->inf).
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

# Toggles for ring opacity (alpha) and planetary radius ratio (p)
ALPHA_FREE_VARIANTS = [False, True]
P_FREE_VARIANTS = [True, False]

FORWARD_MODEL_VARIANTS = ["exorings"]

# Planets to run
PLANETS = ["b", "d"]

# When P_FREE=False, fix p to multiple intermediate values.
# If this list is empty, p is fixed to p_min with no label.
P_FIXED_RUNS = []
