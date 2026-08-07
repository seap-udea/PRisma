# run_config_full.py  (alphatest branch)
# Ring opacity is now parametrized by alpha = exp(-tau), Uniform[0, 1].
# alpha=1 => transparent ring (tau=0), alpha->0 => opaque ring (tau->inf).
DEFAULT_CASE = "kepler_51"

# Observables to include in the KDE likelihood
KDE_VARIANTS = [
    ["delta", "T14", "T23", "rho_obs"],
]

# Grid of nuisance parameters (rho_star,true and impact parameter b)
FREE_PARAM_VARIANTS = [
    {"RHO_TRUE_FREE": True,  "B_FREE": True},   # all-free (nuisance)
]

# Toggles for ring opacity (alpha) and planetary radius ratio (p)
ALPHA_FREE_VARIANTS = [True]
P_FREE_VARIANTS = [True]

FORWARD_MODEL_VARIANTS = ["exorings"]

# Planets to run
PLANETS = ["b", "d"]
