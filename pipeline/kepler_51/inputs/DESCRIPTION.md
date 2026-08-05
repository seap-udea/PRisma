# Data Description: `pipeline/kepler_51/inputs`

This directory contains the input data for running the "Photo-Ring" (PR) pipeline applied to the Kepler-51 system. Kepler-51 is a compact multi-planetary system known because its planets b, c, and d are "super-puffs" (planets with extremely low densities). These data are used to evaluate whether the presence of planetary rings can explain these apparent density anomalies.

Below, the structure and content of each subdirectory and file are detailed so that they can be assimilated by another model:

## 1. `observables/`
Contains the derived transit observables (MCMC posterior samples) that are used to build the KDE (Kernel Density Estimation) likelihood function in the model.
* **Files:** `kepler_51_b_observables.dat`, `kepler_51_c_observables.dat`, `kepler_51_d_observables.dat` (one for each planet).
* **Format:** Tabular text files with the following 9 columns:
  1. `p`: Planet-to-star radius ratio $R_p/R_\star$ (dimensionless).
  2. `delta`: Transit depth (dimensionless, equivalent to $(R_p/R_\star)^2$).
  3. `aR`: Scaled semi-major axis $a/R_\star$ (dimensionless).
  4. `rho_obs`: Transit-inferred stellar density [kg/m³].
  5. `P`: Orbital period [days].
  6. `b`: Impact parameter [$R_\star$].
  7. `i_orb`: Orbital inclination [degrees].
  8. `T14`: Total transit duration [hours].
  9. `T23`: Full transit duration (flat-bottom phase) [hours].

## 2. `rho_true_data/`
Contains information about the "true" stellar density ($\rho_{\star,\rm true}$) of the Kepler-51 system, derived externally (e.g., Berger et al. 2023). They are used as a prior distribution or fixed value during sampling.
* **Files:**
  * `rho_true_samples.dat`: Single-column file containing samples of the true stellar density [kg/m³].
  * `rho_grid_cdf.txt`: Two-column file approximating the inverse Cumulative Distribution Function (CDF) for the stellar density. The first column (`rho_grid_gcc`) represents a grid of stellar density and the second (`rho_cdf`) the cumulative value.

## 3. `ttv/`
Contains the results of the Transit Timing Variations (TTV) analysis. These are externally provided equal-weight posteriors from MultiNest.
* **Subdirectories and Files:**
  * **`Kepler-51b/`**:
    * `TTVplan1-post_equal_weights.dat`, `TTVplan2-post_equal_weights.dat`, `TTVplan3-post_equal_weights.dat`: Posterior samples corresponding to three different light curve segments evaluated for planet b.
    * `rho_b_samples.dat`: Samples (1 column) of the stellar density inferred specifically from the data of planet b.
  * **`Kepler-51c/`**:
    * `TTVplan-post_equal_weights.dat`: Posterior samples of a single global fit for planet c.
  * **`Kepler-51d/`**:
    * `TTVplan-post_equal_weights.dat`: Posterior samples of a single global fit for planet d.
    * `rho_d_samples.dat`: Samples (1 column) of the stellar density inferred specifically from the data of planet d.
