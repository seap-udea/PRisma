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
│   ├── observables/kepler_51_<planet>_observables.dat
│   └── rho_true_data/
│       ├── rho_true_samples.dat               # ρ★,true samples [kg/m³] (Berger et al. 2023)
│       └── rho_grid_cdf.txt                   # its inverse-CDF grid (regenerable)
└── results/<forward_model>/                   # <run_tag>.npz + _meta.json
```

`results/` is **versioned**. Manuscript figures/tables come from
[`papers/kepler51/`](../../papers/kepler51/) (`make notebooks`), which reads these chains (and
`reference_runs/`). Optional `figures/` under this case directory is gitignored diagnostic scratch
from older plotting notebooks — not used by the paper.

## Inputs in detail

- **`inputs/ttv/`** — TTV-fit posteriors (D. Kipping). Planet **b** has three light-curve segments
  (`TTVplan1/2/3`); planets **c** and **d** have a single fit.
- **`inputs/observables/`** — derived observable posteriors
  (`p, δ, a/R★, ρ_obs[kg/m³], P[days], b, i_orb[°], T14[h], T23[h]`).
- **`inputs/rho_true_data/`** — Berger et al. (2023) stellar-density samples / inverse CDF.

Planet-specific priors (`b`, `p_mean_ref`, Earth-density `p_min`) use Masuda et al. (2024)
Table 6 **Outside 2:1** masses $M_b = M_d = 6.9\,M_\oplus$ and are set in
`pipeline/run_sweep.py` (`PLANET_PARAMS`).

## Reproduce

```bash
cd ..    # pipeline/
bash run_sweep_parallel.sh --n-procs 6

cd ../papers/kepler51
make notebooks
```
