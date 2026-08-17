# PRisma Pipeline Guide

The PRisma pipeline is designed to probe exoplanetary rings through Asterodensity Profiling (AP) and the PhotoRing effect.

## Theoretical Background

As detailed in the manuscript *"Probing Exoplanetary Rings with Asterodensity Profiling: A PhotoRing Analysis of Kepler-51"* (Zuluaga et al.), the PhotoRing (PR) effect occurs when an unmodeled planetary ring system alters a transit light curve. This typically causes the stellar density inferred from the transit ($\rho_{\star,\mathrm{obs}}$) to differ systematically from independent isochrone-based estimates ($\rho_{\star,\mathrm{true}}$). 

By combining Asterodensity Profiling with a TTV-aware fit of transit light-curves, the PRisma pipeline utilizes a geometric forward model for transiting ringed planets to retrieve ring configurations that explain these observed density anomalies. This provides a mechanism for identifying the potential presence of rings even when their direct photometric signatures are not obvious, such as in the case of the highly inflated "super-puff" planets.

**Citation:**
If you use this pipeline in your research, please cite our paper:
> *Zuluaga, J. I., Numpaque, S., Kipping, D., & Alvarado-Montes, J. A. (202X). Probing Exoplanetary Rings with Asterodensity Profiling: A PhotoRing Analysis of Kepler-51.*

---

## 1. Required Inputs

To run the pipeline for a given system (e.g., `kepler_51`), the input data must be structured inside the `pipeline/<case>/inputs/` folder. For each planet (e.g., `b`, `d`), you need to provide the following:

- **TTV Data:** `ttv/<planet>/...post_equal_weights.dat` 
  Contains the transit times and related uncertainties.
- **Observables:** `observables/<case>_<planet>_observables.dat` 
  The posterior distributions of the transit observables (e.g., transit depth $\delta$, impact parameter $b$, and durations $T_{14}$, $T_{23}$).
- **True Stellar Density:** `rho_true_data/rho_true_samples.dat` 
  An independent estimate of the true stellar density, typically derived from isochrones or asteroseismology.

---

## 2. Creating a Run Configuration File

The behavior of the retrieval sweep is governed by a Python configuration file named `run_config-<config>.py` (e.g., `run_config_full.py`).

To create a new configuration, define a new Python file in the `pipeline/` directory specifying the target planets, observables, forward models, and free parameters. For instance, to test different `rho_true` nuisance-parameter prior distributions (such as a Gaussian prior), you can add a `RHO_TRUE_DIST` dictionary:

```python
# run_config_custom.py
PLANETS = ["b", "d"]

# Distribution of the rho_true nuisance parameter
# e.g., Gaussian prior N(mean, sigma) in g/cm^3
RHO_TRUE_DIST = dict(
    name="Masuda et al. 2024",
    mean=2.08,
    sigma=0.08,
)

# ... define KDE_VARIANTS, FREE_PARAM_VARIANTS, etc.
```

---

## 3. Parallel Execution and Outputs

Once your configuration file is ready, you can launch a parallel Nested Sampling sweep.

### Launching the Sweep

From the `pipeline/` directory, use the Python runner `run_inference.py`:

```bash
# Preview the runs without executing them
python3 bin/run_inference.py --config run_config_custom.py --dry-run

# Execute the sweep in the background
nohup python3 bin/run_inference.py --config run_config_custom.py --n-procs 4 --jobs 2 > sweep.log 2>&1 &
tail -f sweep.log
```

**Useful flags:**
- `--config FILE`: The Python configuration file to use.
- `--n-procs N`: Number of dynesty worker processes per configuration.
- `--jobs J`: Concurrent configurations to run (useful for running multiple configurations in parallel).
- `--case CASE`: Case directory (default: from config or 'kepler_51').
- `--forward-models MODELS`: Forward model(s) to run (default: `exorings`).
- `--nlive N`: Override nested-sampling nlive (default: from config).
- `--dlogz Z`: Override dlogz stopping criterion (default: from config).
- `--force`: Re-run and overwrite existing results.
- `--dry-run`: Print what would run without running anything.
- `--no-ppc`: Skip the posterior predictive check (saves a bit of time).

### Outputs and File Naming Convention

The pipeline outputs the retrieval results into `pipeline/<case>/results/<forward_model>/`. The primary outputs for each run are:
- `<run_tag>.npz`: The compressed numpy archive containing the Nested Sampling chain and samples.
- `<run_tag>_meta.json`: Metadata summarizing the run parameters, Bayesian evidence ($\ln \mathcal{Z}$), and prior information.

**Naming Convention:** 
The base `<run_tag>` is automatically constructed using the case, planet, forward model, and free parameter flags (e.g., `kepler_51_b_NS_exorings_kde_..._rhoFREE_bFREE`). If a custom configuration is provided, such as `RHO_TRUE_DIST`, a specific label is appended (e.g., `_rhoMasuda` or `_rhoBerger`) to prevent overwriting base tags.

---

## 4. Scoring the Results

After the retrievals complete, you must evaluate and classify the physical quality of the runs using a Multi-Metric Decision Tree Classification system. 

The scoring uses the Posterior Predictive Check (PPC) score (`z1`)—which measures the average agreement between the predictive checks and the empirical observables—along with other physical constraints (e.g., physical density, ring presence, stable angles) to rank the runs. Categories range from "Golden Sample" to "Rejected".

### Running the Scorer

### Running the Scorer

From the `pipeline/` directory, execute the scoring script. You can pass a specific directory containing `.npz` files (e.g. `berger`), or use the `--recursive` flag to process all subdirectories. Adding the `--report` flag will automatically generate the visual Markdown report alongside the JSON scoring:

```bash
# Evaluate and Classify a specific directory (e.g., 'berger' inside 'exorings')
python bin/score_retrievals.py berger --report

# Evaluate and Classify all subdirectories recursively
python bin/score_retrievals.py --recursive --report
```

**Useful flags:**
- `results_dir`: Directory containing the `.npz` files (default is `kepler_51/results/exorings`).
- `--recursive`: Recursively score all subdirectories with results.
- `--force`: Force rescoring all files. By default, only new files are scored.
- `--report`: Generate the visual Markdown report.

This produces a `scoring_{case}_{planet}.json` file. The scoring is critical because it dictates the file ordering and categorization in the subsequent steps. 

To examine the results, you will generate a Markdown Visual Report (see next section, as it requires the figures to be generated first).

---

## 5. Generating Figures and Gallery Previews

### Generating Figures

Once the runs are scored, you can generate the diagnostic figures (Corner plots and PPC light curves). The figure generator reads the scoring JSON to apply an `ORDKEY` prefix to the filenames, which automatically sorts the best fits first based on their `z1` score.

```bash
# Generate figures for specific files or a single directory
python bin/generate_figures.py kepler_51/results/exorings/*.npz
python bin/generate_figures.py kepler_51/results/exorings

# Generate figures recursively for all subdirectories
python bin/generate_figures.py --recursive
```

**Useful flags:**
- `npz`: One or more `.npz` files or a results directory.
- `--recursive`: Recursively find all `.npz` files in results subdirectories.
- `--only [corner|reduced|ppc]`: Restrict to one figure kind.
- `--force`: Force regeneration of figures.
- `--dry-run`: List targets without drawing.
- `--no-prefix`: Generate figures without the scoring category and ranking prefix in the filenames.

By default, the script reads the scoring JSON to apply an `ORDKEY` prefix, writing figures into `pipeline/<case>/results/figures/` (or the corresponding subfolder) using the following naming convention:
`{case}_{planet}_{catX}_{CategoryName}_{ORDKEY}-{run_tag}_[corner|corner_reduced|ppc].png`

**Example filename for Kepler-51b (with scoring prefix):**
```text
kepler_51_b_cat1_GoldenSample_ord91978-lnZ_+08.02-kepler_51_b_NS_exorings_kde_delta-T14-T23-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_alphaFREE_pFREE_corner.png
```

If you use the `--no-prefix` flag, or if the runs have not been scored yet, the figures will be saved simply as:
`{run_tag}_[corner|corner_reduced|ppc].png`

**Example filename for Kepler-51b (without scoring prefix):**
```text
kepler_51_b_NS_exorings_kde_delta-T14-T23-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_alphaFREE_pFREE_corner.png
```

### Generating the Visual Report

With the figures created, you can now generate the comprehensive Markdown report (if you didn't already pass `--report` during scoring):

```bash
python bin/score_retrievals.py kepler_51/results/exorings --report
```

Review this Markdown report to examine the categorized results, paying special attention to the "Golden Sample" models with high Bayesian Evidence ($\ln \mathcal{Z}$).

### Generating Web Gallery Previews

Finally, to create lightweight `.webp` thumbnails for a web gallery, run the gallery script from the repository root:

```bash
bash bin/seap-udea-gallery.sh
```

This script reads `.seap-udea-gallery.json` and populates the `pipeline/<case>/results/figures/.gallery/` directory with optimized preview images.

---

## 6. Scoring Details and Ordering

### PPC score (`z1`) and ordering

For each observable in the Posterior Predictive Check (PPC) set `{delta, T14, T23, rho_obs, b_obs}`:

1. Compute normalized mismatch:
$$ w_{1,i} = \frac{W1_i}{|\langle x_{obs,i} \rangle|} $$

2. Average across available observables:
$$ \langle w_1 \rangle = \text{mean}_i(w_{1,i}) $$

3. Define score:
$$ z_1 = -\log_{10}(\langle w_1 \rangle) $$

Interpretation: A larger `z1` means better PPC agreement.

### `ORDKEY` structure

The `ORDKEY` prefix format is:
`ordXXXXX-z1_YY.YY`

Where:
- `z1_YY.YY` is the readable score (2 decimals).
- `ordXXXXX` is an inverted sortable bucket:
$$ \text{ord} = \text{clip}(\text{round}((100-z_1)\times 1000), 0, 99999) $$

Because `ord` decreases when `z1` increases, standard alphabetical sorting puts better runs first.
If `z1` cannot be computed (for example missing PPC array), the script uses `ord99999-z1_nan` so those files go to the end.

### Multi-Metric Retrieval Classification

While `z1` is useful for comparing predictive checks, we provide a more comprehensive **Decision Tree Classification** system to determine the physical quality of a retrieval. This system assigns a mutually exclusive category to each retrieval by checking its properties sequentially. Within each category, retrievals are ranked primarily by their Bayesian Evidence ($\ln \mathcal{Z}$). Additional metrics like the Akaike Information Criterion (AIC) and the maximum log-likelihood (`max_logl`) are also computed and stored in the scoring JSON for further model selection comparisons.

The categories are evaluated in this strict order:

1. **Rule 1: Good Average Fit (PPC)**:
   Measures the average agreement between the posterior predictive checks (PPC) and the empirical observables using the $z_1$ metric.
   - **Condition**: $z_1 \ge 1.3$
   - **If it fails**: `[Rejected] Poor Fit`

2. **Rule 2: Good Individual Lightcurve Fit (PPC Min)**:
   Ensures that no individual strict lightcurve observable (`delta`, `T14`, `T23`) has a catastrophic fit hidden by a good average. It computes the worst individual $z_1$ among these geometry variables.
   - **Condition**: $z_{1,\mathrm{min}} \ge 1.2$.
   - **If it fails**: `[Rejected] Poor Individual Fit`

3. **Rule 3: Good Critical Fit (PPC Crit)**:
   Ensures that the critical variables (transit depth $\delta$ and the observed density proxies) are exceptionally well-fitted.
   - **Condition**: $z_{\mathrm{crit}} \ge 1.75$.
   - **If it fails**: `[Rejected] Poor Critical Fit`

4. **Rule 4: Physical Density (Nuisance Constraint)**:
   Evaluates how well the marginal posterior of the nuisance stellar density $\rho_{\mathrm{true}}$ matches the independent empirical prior.
   - **Condition**: Fractional error between the median $\rho_{\mathrm{true}}$ and the empirical true density must be $\le 25\%$.
   - **If it fails**: `[Rejected] Unphysical Nuisance`

5. **Rule 5: Confirmed Ring ($f_e$)**:
   Ensures the retrieval converges to a ringed model ($f_e > 1$). 
   - **Condition**: The 16th percentile of the $f_e$ marginal posterior ($f_{e,p16}$) must be $\ge 1.0$.
   - **If it fails**: `[Degenerate] Ringless`

6. **Rule 6: Stable Angles ($i_r, \theta$)**:
   Evaluates multimodality in ring orientation.
   - **Condition**: Both angles should ideally be unimodal. Average KDE peaks $\le 1.5$.
   - **If it fails**: `[Acceptable] Multimodal Angles`

7. **Rule 7: Significant Bayesian Evidence ($\ln \mathcal{Z}$)**:
   Ensures the model performs strictly better than the base null-hypothesis.
   - **Condition**: Bayesian Evidence $\ln \mathcal{Z} \ge 0.0$.
   - **If it fails**: `[Acceptable] Low Bayesian Evidence`
   - **If it passes**: `[Excellent] Golden Sample`
