# Case: Kepler-51

The bundled worked example for the Photo-Ring pipeline — and the template to copy for your own
target. Kepler-51 is a compact three-planet system whose planets b, c and d are all extreme
"super-puffs" (ρ < 0.1 g/cm³ from transit fits). This case tests whether **planetary rings** can
explain those anomalously low transit-inferred densities via the Photo-Ring effect
(Zuluaga et al. 2015). Physics: [`../../docs/science_background.md`](../../docs/science_background.md).

## Layout

```
kepler_51/
├── inputs/
│   ├── ttv/<planet>/…post_equal_weights.dat   # raw TTV posteriors (MultiNest; Kipping)
│   ├── observables/kepler_51_<planet>_observables.dat  # derived by step 1
│   └── rho_true_data/
│       ├── rho_true_samples.dat               # ρ★,true samples [kg/m³] (Berger et al. 2023)
│       └── rho_grid_cdf.txt                   # its inverse-CDF grid (regenerable)
├── results/<forward_model>/                   # <run_tag>.npz + _meta.json   (created on run)
└── figures/<type>/                            # ppc, corner, marginal, ring, trace, panel (created on run)
```

`results/` (posterior `.npz` + `_meta.json`) is **versioned**; `figures/` is **gitignored** —
running the pipeline regenerates figures, while chains stay available for tables/figures.

## Inputs in detail

- **`inputs/ttv/`** — TTV-fit posteriors (D. Kipping). Planet **b** has three light-curve segments
  (`TTVplan1/2/3`); planets **c** and **d** have a single fit. Columns: `Rp/R★`, `ρ★,obs[kg/m³]`,
  `b`, `P[days]`, `t_mid`, …, `logL` (last). `01_observables.ipynb` derives the observables from
  these; for planet b it checks segment consistency (KS tests) and adopts the most complete segment.
- **`inputs/observables/`** — the derived observable posteriors
  (`p, δ, a/R★, ρ_obs[kg/m³], P[days], b, i_orb[°], T14[h], T23[h]`), the direct input to step 2.
- **`inputs/rho_true_data/`** — `rho_true_samples.dat` are Berger et al. (2023) stellar-density
  samples for Kepler-51 (the empirical `RHO_TRUE_FREE` prior); `rho_grid_cdf.txt` is its inverse CDF
  (regenerate with `python -m photoring.rho_cdf inputs/rho_true_data/rho_true_samples.dat`).

Planet-specific priors (impact parameter `b`, reference radius ratio `p_mean_ref`, radius-prior
lower edge `p_prior_lo`) follow Masuda et al. (2024) and are set in the `USER CONFIGURATION` cell of
each step-2 notebook (`PLANET_PARAMS`).

## What the pipeline delivers here

Running steps 1–3 (or `run_sweep.sh`) produces, per planet and per run configuration:
a ring-geometry posterior `(fe, iR, θ, p, …)` and — with dynesty — the Bayesian evidence ln Z; a
posterior-predictive check against all transit observables; corner/marginal plots with the
Berger/Masuda priors overlaid; and the projected best-fit ring diagram. Comparing the evidence
across "rings" vs "no-rings-relevant" configurations is what quantifies whether a ring system is a
viable explanation for each planet's density anomaly.

## Reproduce

```bash
cd ..                     # into pipeline/
jupyter nbconvert --to notebook --execute 01_observables.ipynb        # regenerate observables
jupyter nbconvert --to notebook --execute 02_inference_dynesty.ipynb  # infer ring geometry
jupyter nbconvert --to notebook --execute 03_results_plotting.ipynb   # figures + tables
```

The notebooks default to `CASE = "kepler_51"`. See [`../README.md`](../README.md) for the full
guide and for adapting the pipeline to a new target.
