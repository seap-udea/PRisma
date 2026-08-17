# run_config-berger.py  — Berger et al. 2023 empirical rho_true prior (planet b only)
# Same inference setup as run_config-full.py but with explicit RHO_TRUE_DIST.
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
PLANETS = ["b"]

# Distribution of the rho_true nuisance parameter
# Berger et al. 2023: empirical KDE from isochrone samples (default pipeline behaviour)
RHO_TRUE_DIST = dict(
    name="Berger et al. 2023",
    pdf="inputs/rho_true_data/",
    file="rho_grid_cdf.txt",
)
