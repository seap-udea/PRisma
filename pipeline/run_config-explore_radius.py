# run_config-explore_radius.py  (alphatest branch)
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
PLANETS = ["b"]

# When P_FREE=False, fix p to multiple intermediate values.
# 'fraction' is between 0 (p_min) and 1 (p_max = p_mean_ref).
P_FIXED_RUNS = [
    {"label": "P1", "fraction": 0.25},
    {"label": "P2", "fraction": 0.50},
    {"label": "P3", "fraction": 0.75},
]
