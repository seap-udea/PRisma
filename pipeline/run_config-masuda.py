# run_config-masuda.py  — Masuda et al. 2024 Gaussian rho_true prior (planet b only)
# Same inference setup as run_config-full.py but with a Gaussian rho_true prior.
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
# Masuda et al. 2024: Gaussian prior N(mean, sigma) in g/cm^3
RHO_TRUE_DIST = dict(
    name="Masuda et al. 2024",
    mean=2.08,
    sigma=0.08,
)
