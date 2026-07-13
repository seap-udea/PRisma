# Pipeline — Photo-Ring Bayesian inference

A reproducible pipeline that goes from a transiting planet's TTV posterior to a posterior over
**ring geometry**, testing whether a ring system can explain the planet's observed stellar-density
anomaly (the Photo-Ring effect, Zuluaga et al. 2015, ApJL 803, L14). It ships with the Kepler-51
b/c/d data used in this thesis as a worked example, and is built to be pointed at a **different
target** by copying one directory and dropping in your data.

Full physics: [`../docs/science_background.md`](../docs/science_background.md).

## How it is organised

The analysis lives in the importable **`photoring`** package; the notebooks are thin guides that
import it and are driven by a single `CASE` variable.

```
pipeline/
├── photoring/              # the analysis as importable .py modules (see "The photoring package")
├── 01_observables.ipynb            # step 1: TTV posterior -> transit observables
├── 01b_observables_plotting.ipynb  # step 1b: observable-posterior figure (optional)
├── 02_inference_dynesty.ipynb      # step 2: ring-geometry inference (nested sampling; gives ln Z)
├── 02_inference_emcee.ipynb        # step 2: ring-geometry inference (MCMC; cross-check)
├── 03_results_plotting.ipynb       # step 3: publication figures + summary tables
├── run_sweep.py / run_sweep.sh     # run step 2 over many configurations (papermill)
├── tests/                          # forward-model equivalence tests
└── kepler_51/                      # the bundled example case (inputs + outputs + writeup)
```

Nothing installs: each notebook's first cell puts the repo root (for `exorings`, `geotrans`) and
`pipeline/` (for `photoring`) on `sys.path`.

## Pipeline steps

| Step | Notebook | Purpose |
|---|---|---|
| 1 | `01_observables.ipynb` | Convert a planet's TTV-fit posterior `(Rp/R★, ρ★, b, P)` into the transit-observable set `(δ, a/R★, T14, T23, b, i, P)` (Zuluaga+2015 Eq. 1–4). Writes `<case>_<planet>_observables.dat`. |
| 1b | `01b_observables_plotting.ipynb` | Publication figure of the observable posteriors. Optional / diagnostic. |
| 2 | `02_inference_dynesty.ipynb` | Build a joint KDE likelihood from the step-1 observables and sample the ring geometry with `dynesty` static nested sampling — the only one that yields the Bayesian evidence ln Z. |
| 2 | `02_inference_emcee.ipynb` | Same model/likelihood sampled with `emcee` (MCMC) — an independent cross-check. |
| 3 | `03_results_plotting.ipynb` | Read step-2 outputs and produce PPCs, corner plots, marginals with priors, ring diagrams, a consolidated panel, and summary tables. |

Both step-2 notebooks have a `parameters`-tagged **USER CONFIGURATION** cell so they can be run
interactively for a single configuration, or swept automatically (see [Sweeps](#running-a-sweep)).

## Running one case

Every notebook selects a case with one line, `CASE = "kepler_51"`, which resolves all paths through
`photoring.CasePaths`. To reproduce Kepler-51 end to end:

```bash
cd pipeline
jupyter nbconvert --to notebook --execute 01_observables.ipynb
jupyter nbconvert --to notebook --execute 02_inference_dynesty.ipynb
jupyter nbconvert --to notebook --execute 03_results_plotting.ipynb
```

## Running it on your own target

The pipeline is case-oriented: each target is a self-contained directory `pipeline/<case>/`.

1. **Copy the example case:** `cp -r kepler_51 my_planet`.
2. **Replace the inputs** under `my_planet/inputs/` (see [Input contract](#input-contract)).
3. **Set `CASE = "my_planet"`** at the top of each notebook (and edit the planet list / priors in
   the `USER CONFIGURATION` cell of step 2).
4. Run the notebooks as above.

### Input contract

Per case, under `pipeline/<case>/inputs/`, there are **two ways in**:

- **A — raw TTV posterior (MultiNest-style).** Place `post_equal_weights.dat` files under
  `inputs/ttv/<planet>/`. Columns used: `Rp/R★`, `ρ★,obs[kg/m³]`, `b`, `P[days]`, `t_mid`, …,
  `logL` (last). Column indices are configurable in `01_observables.ipynb` (`COLS`).
  Step 1 converts them to the observables table.
- **B — pre-derived observables.** If you already have observables, place a file
  `inputs/observables/<case>_<planet>_observables.dat` (9 columns:
  `p, δ, a/R★, ρ_obs[kg/m³], P[days], b, i_orb[°], T14[h], T23[h]`) and **skip step 1**.

Plus, for the `RHO_TRUE_FREE` prior:

- **`inputs/rho_true_data/`** — `rho_true_samples.dat` (samples of the star's true density ρ★,true
  in kg/m³, e.g. from a stellar catalogue) **and** `rho_grid_cdf.txt`, its inverse-CDF grid.
  Regenerate the grid from the samples with:

  ```bash
  python -m photoring.rho_cdf kepler_51/inputs/rho_true_data/rho_true_samples.dat
  ```

## Parameter space

| Parameter | Description | Prior |
|---|---|---|
| `fe` [Rp] | ring outer radius | Uniform `(fi, FE_MAX]` |
| `iR` [°] | projected ring inclination (90° = edge-on) | isotropic, `p(iR) ∝ sin(iR)` on `(0°, 90°)` |
| `θ` [°] | projected tilt (90° = ⊥ orbit) | Uniform `[0°, 90°]` |
| `p = Rp/R★` | planet radius ratio | Uniform `[p_min, p_max]` (from `p_mean_ref × p_prior_{lo,hi}`) |

Optional dimensions, toggled per run in `MODEL_CONFIG`:

| Parameter | Flag | Free | Fixed |
|---|---|---|---|
| `τ` opacity | `TAU_FREE` | log-uniform on `[TAU_PRIOR_LO, TAU_PRIOR_HI]` | `TAU_FIXED` (1.0, opaque) |
| `ρ★,true` | `RHO_TRUE_FREE` | empirical KDE prior over `rho_true` samples | `RHO_TRUE_FIXED` (sample mean) |
| `b` | `B_FREE` | truncated-Gaussian on `[0,1]` (`B_FIXED`, `B_SIGMA`) | `B_FIXED` |
| `p` | `P_FREE` | sampled | pinned to `p_min` |

Dimensionality is `3 + P_FREE + TAU_FREE + RHO_TRUE_FREE + B_FREE` (4–7D); canonical order
`[fe, iR, θ, (p), (τ), (ρ★,true), (b)]`. Fixed: `fi = FI_FIXED` (ring inner edge, default 1.0).

## Likelihood

The joint KDE likelihood is trained on any subset of observables set in
`KDE_CONFIG['observables']`:

| Key | Observable |
|---|---|
| `delta` | transit depth δ |
| `T14`, `T23` | total / flat-bottom contact durations [h] |
| `rho_obs` | transit-inferred stellar density [g/cm³] |
| `b_obs` | transit-inferred impact parameter |

The KDE is trained on `N_KDE` posterior samples; the step-3 posterior-predictive check always
evaluates **all five** observables regardless of which entered the likelihood (out-of-sample
validation).

## Samplers

- **dynesty** (`02_inference_dynesty.ipynb`): static nested sampling (`NS_CONFIG`: `nlive`,
  `sample`, `dlogz`, …). Produces the evidence ln Z and dynesty-native run/trace plots.
- **emcee** (`02_inference_emcee.ipynb`): ensemble MCMC (`MCMC_CONFIG`: `nwalkers`, `nsteps`,
  `burnin`, `thin`, …) with differential-evolution moves; log-prob-trace and autocorrelation-time
  diagnostics.

## Output structure

Written under the case directory:

```
pipeline/<case>/
├── results/<forward_model>/   #  <run_tag>.npz  +  <run_tag>_meta.json   (exorings/ or geotrans/)
└── figures/<type>/            #  ppc/ corner/ marginal/ ring/ trace/ diagnostics/ panel/ ...
```

The `RUN_TAG` encodes the full configuration (case, planet, sampler, KDE observables, sampler
settings, forward model, free-parameter flags). `results/` and `figures/` are **gitignored** — the
pipeline regenerates them; only code and minimal inputs are versioned.

## Running a sweep

`run_sweep.py` / `run_sweep.sh` run step 2 over many configurations via `papermill`:

```bash
bash run_sweep.sh                    # both samplers, all configs, case kepler_51
bash run_sweep.sh dynesty            # nested sampling only
bash run_sweep.sh emcee --dry-run    # preview configurations
bash run_sweep.sh both --case my_planet   # sweep a different case
```

Executed notebooks land in `<case>/tests_outputs/`, logs in `<case>/tests_logs/`, results in
`<case>/results/<model>/`.

## The `photoring` package

| Module | Contents |
|---|---|
| `config.py` | `CasePaths` — resolve a case's input/output paths from its name |
| `io.py` | load observables / rho_true / cdf; save & discover runs |
| `observables.py` | `derive_observables`, `load_posterior`, `save_observables` (step 1) |
| `rho_cdf.py` | tabulate the `rho_true` inverse CDF (function + `python -m photoring.rho_cdf`) |
| `likelihood.py` | `OBS_MAP`, `build_kde` |
| `priors.py` | parameter-space bookkeeping (`build_param_space`) |
| `model.py` | `PhotoRingModel` — ties data + priors + forward model + KDE likelihood together |
| `inference.py` | `run_dynesty`, `run_emcee`, `compute_ppc`, `posterior_stats` |
| `plotting.py` | publication-ready figures (`STYLE`, `plot_ppc`, `plot_marginals`, `plot_corner`, `plot_ring_diagram`, `plot_results_panel`, …) |

The forward models are the sibling packages `exorings` (default, closed-form) and `geotrans`
(numerically integrated), selected with `MODEL_CONFIG['FORWARD_MODEL']`.

## Tests

```bash
cd pipeline && python -m pytest tests/          # forward-model equivalence + geotrans smoke
```
