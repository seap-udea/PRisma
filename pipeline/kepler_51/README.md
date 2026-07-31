# Case: Kepler-51

Bundled worked example for the Photo-Ring pipeline — and the template to copy for a new
target. Kepler-51 is a compact multi-planet system whose planets b, c and d are extreme
“super-puffs” (transit-inferred $\rho\lesssim0.1\,\mathrm{g\,cm^{-3}}$). This case asks whether
**planetary rings** can account for those densities via the Photo-Ring (PR) effect
(Zuluaga et al. 2015).

The accompanying manuscript lives in [`../../papers/kepler51/`](../../papers/kepler51/).
Pipeline packages and the parallel runner are documented in the
[repo README](../../README.md).

## Layout

```
kepler_51/
├── inputs/
│   ├── ttv/
│   │   ├── Kepler-51b/   # TTVplan{1,2,3}-post_equal_weights.dat (+ ρ samples)
│   │   ├── Kepler-51c/
│   │   └── Kepler-51d/
│   ├── observables/kepler_51_{b,c,d}_observables.dat
│   └── rho_true_data/
│       ├── rho_true_samples.dat    # ρ★,true [kg/m³] (Berger et al. 2023)
│       └── rho_grid_cdf.txt        # inverse-CDF grid (regenerable)
├── results/exorings/               # <run_tag>.npz + <run_tag>_meta.json
└── tests_logs/                     # <run_tag>.log (+ sweep_parallel_*.json)
```

**Versioned artefacts** (committed to git):

| Path | Contents |
|------|----------|
| `results/exorings/` | Successful dynesty chains + metadata (~78 runs in the current campaign) |
| `tests_logs/<run_tag>.log` | Per-configuration dynesty / runner log (96 files = full grid) |
| `tests_logs/sweep_parallel_*.json` | Machine-readable summary of a parallel campaign |
| `../sweep_parallel_*.log` | Master `nohup` log for the parallel launcher |

Configs whose prior never intersects the KDE support are reported as `[PLATEAU]` and are
**not** written under `results/` (log only). That is why there are more logs than `.npz` files.

Manuscript figures/tables do **not** read this tree directly for the preferred solution: they
use copies under [`papers/kepler51/reference_runs/`](../../papers/kepler51/reference_runs/)
(`make reference-runs` / `make notebooks`). Diagnostic `figures/` under this case directory
(if present) are gitignored and unused by the paper.

## Retrieval grid

Defined in [`../run_sweep.py`](../run_sweep.py). For dynesty the default product is

$$
2\,\mathrm{(planets\,b,d)}\times
3\,\mathrm{(observable\,sets)}\times
4\,\mathrm{(run\,configs)}\times
4\,\mathrm{(input\,selections)}
= 96
$$

| Axis | Options |
|------|---------|
| Planets | `b`, `d` (c has inputs but is not in the default sweep) |
| Observable set $\mathcal{L}_{\rm KDE}$ | $(\delta,\rho_{\star,\rm obs})$ · $(\delta,T_{14},\rho_{\star,\rm obs})$ · $(\delta,T_{14},T_{23})$ |
| Run config (nuisance) | all-fixed · $\rho_{\star,\rm true}$ free · $b$ free · **all-free** |
| Input selection | $p$ and/or $\tau$ free or fixed ($2\times2$) |

Sampler defaults (`NS_CONFIG_BASE`): `nlive=1200`, `dlogz=0.01`, `sample=rslice`, `seed=2026`,
$N_{\rm KDE}=5000$.

**Preferred manuscript setup** (both planets): all-free nuisance+inputs with
$\mathcal{L}=(\delta,T_{14},\rho_{\star,\rm obs})$, e.g.

```
kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE
```

## Inputs

- **`inputs/ttv/`** — MultiNest equal-weight posteriors from the TTV analysis (D. Kipping).
  Planet **b** has three light-curve segments (`TTVplan1/2/3`); **c** and **d** have one fit each.
- **`inputs/observables/`** — derived observable columns used to build the KDE likelihood
  (`p`, $\delta$, $a/R_\star$, $\rho_{\rm obs}$ [kg/m³], $P$ [d], $b$, $i_{\rm orb}$ [°],
  $T_{14}$ [h], $T_{23}$ [h]).
- **`inputs/rho_true_data/`** — Berger et al. (2023) stellar-density samples and inverse CDF
  for the $\rho_{\star,\rm true}$ prior / fixed value.

Planet-specific priors (`B_FIXED`, `B_SIGMA`, `p_mean_ref`, Earth-density `p_min`) use
Masuda et al. (2024) Table 6 **Outside 2:1** masses $M_b=M_d=6.9\,M_\oplus$ and
$R_\star=0.869\,R_\odot$ (Berger et al. 2023). See `PLANET_PARAMS` in `run_sweep.py`.

## Reproduce / extend

From `pipeline/`:

```bash
# Preview the 96-run grid
bash run_sweep_parallel.sh --dry-run --n-procs 6

# Only the two manuscript reference tags
bash run_sweep_parallel.sh --dry-run --validate-refs --n-procs 6

# Full campaign (finished tags are skipped; plateaus are not saved)
nohup bash run_sweep_parallel.sh --n-procs 6 > sweep_parallel_96.log 2>&1 &
tail -f sweep_parallel_96.log
```

Then rebuild paper products:

```bash
cd ../papers/kepler51
make notebooks    # sync reference_runs/ from results/, execute PRisma-*.ipynb
make              # compile main-v1r.pdf
```

Regression check that the packaged forward model + one NS config still match a frozen
baseline:

```bash
cd ../pipeline
../.venv/bin/python tests/test_kepler51_regression.py
```
