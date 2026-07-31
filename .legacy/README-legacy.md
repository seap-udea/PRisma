# PRisma — a reproducible pipeline for exoplanet-ring detection via asterodensity profiling

This repository is the consolidated, documented, and reproducible version of the thesis research
by **Sebastián Numpaque** (Universidad de Antioquia), advised by **Jorge I. Zuluaga**, with
**Jaime A. Alvarado-Montes** (Macquarie University) and **David Kipping** (Columbia University).
It investigates whether **planetary rings** can explain the anomalously low transit-inferred
stellar densities of the Kepler-51 planets, using the **Photo-Ring (PR) effect**
(Zuluaga et al. 2015, ApJL 803, L14).

It supersedes the exploratory research repo this project grew out of. That original repo is kept
untouched, privately, as a historical archive; this repository re-derives a clean, runnable
version of the method and its Kepler-51 application from it. See [`legacy/`](legacy/) for what
was carried over from the first exploratory version of the analysis and why.

## Scientific question

A planet with rings transiting its host star produces a light curve whose depth (δ) and contact
durations (T₁₄, T₂₃) are modified relative to a bare planet of the same physical size. Because the
stellar density inferred from a transit (Seager & Mallén-Ornelas 2003) depends on exactly those
observables, an unmodeled ring system biases the inferred density ρ★,obs away from the star's true
density ρ★,true. This is the Photo-Ring effect, and it is a candidate explanation for Kepler-51's
planets (b, c, d — all with ρ < 0.1 g/cm³, "super-puffs") without invoking exotic bulk
compositions. Full physics background: [`docs/science_background.md`](docs/science_background.md).

## What's reproducible here

The core deliverable is **`pipeline/`**: a Bayesian-inference pipeline that goes from a planet's
TTV posterior to a posterior over ring geometry, using either `emcee` (MCMC) or `dynesty` (Nested
Sampling). The analysis is packaged as importable modules — the **`photoring`** package — and the
five numbered notebooks are thin, documented guides that import it and are driven by a single
`CASE` variable. The Kepler-51 application ships as a self-contained example case
([`pipeline/kepler_51/`](pipeline/kepler_51/)); point the pipeline at a **different target** by
copying that directory and dropping in your own data. Read
[`pipeline/README.md`](pipeline/README.md) first — it documents the input contract, the model,
the output structure, and how to run it end to end.

The **`photoring`** analysis code, the Kepler-51 inputs, and the posterior chains under
`pipeline/<case>/results/` (`.npz` + `_meta.json`) are versioned so anyone can rebuild
tables and figures without re-running nested sampling. Regenerable diagnostic plot scratch
(`pipeline/**/figures/`, `tests_outputs/`, `tests_logs/`) stays gitignored. Manuscript figures
live under [`papers/kepler51/figures/`](papers/kepler51/figures/).

## Repository map

| Path | Contents |
|---|---|
| [`pipeline/`](pipeline/) | **The reproducible method**: `photoring/`, forward models `exorings/` + `geotrans/`, sweep runners, and the bundled `kepler_51/` case |
| [`pipeline/exorings/`](pipeline/exorings/) | Closed-form ring-transit forward model (`forward.py`, `basic.py`) |
| [`pipeline/geotrans/`](pipeline/geotrans/) | Independent numerical ring-transit model (validation / alt forward model / diagrams) |
| [`papers/kepler51/`](papers/kepler51/) | Manuscript notebooks, `figures/`, `reference_runs/`, LaTeX |
| [`.legacy/`](.legacy/) | Superseded notebooks, papermill `run_sweep.sh`, exploratory geotrans tests |
| [`docs/`](docs/) | Science background, diagrams, and narrative history |
| [`bibliography/`](bibliography/) | Curated `.bib` reference library |

Full guided tour, including *why* each directory looks the way it does: [`STRUCTURE.md`](STRUCTURE.md).

## Quickstart

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cd pipeline
bash run_sweep_parallel.sh --dry-run --n-procs 6   # preview campaign grid

cd ../papers/kepler51
make notebooks   # regenerate manuscript figures + tables
```

Nothing needs installing — put `pipeline/` on `sys.path` and import `exorings`, `geotrans`, and
`photoring` directly.

`requirements.txt` lists dependencies without pinned versions (none were pinned in the original
research environment); pin them once you have a working install if you need a frozen environment.

## Configuration sweeps

A *sweep* runs nested sampling over many retrieval scenarios (planets × KDE observable sets ×
which of `ρ★,true`, `b`, `τ`, `p` are free). Edit the combinatorial grid in
[`pipeline/run_sweep.py`](pipeline/run_sweep.py) (`KDE_VARIANTS`, `FREE_PARAM_VARIANTS`,
`TAU_FREE_VARIANTS`, `P_FREE_VARIANTS`, `PLANETS`, `NS_CONFIG_BASE`, `PLANET_PARAMS`). The default
grid is **96** dynesty runs for Kepler-51.

Run campaigns with [`pipeline/run_sweep_parallel.py`](pipeline/run_sweep_parallel.py) (direct
`photoring` calls; fork pool OK on macOS). The old papermill launcher is under
[`.legacy/pipeline_sweep/`](.legacy/pipeline_sweep/).

### Prepare

```bash
cd pipeline
# Preview the run list (no sampling):
bash run_sweep_parallel.sh --dry-run --n-procs 6

# Optional: only the two manuscript reference tags (all-free, L=δ,T14,ρ):
bash run_sweep_parallel.sh --dry-run --validate-refs --n-procs 6
```

### Launch

```bash
cd pipeline
nohup bash run_sweep_parallel.sh --n-procs 6 > sweep_parallel_96.log 2>&1 &
tail -f sweep_parallel_96.log
```

Useful flags: `--jobs 2` (two configs at once; workers are split), `--validate-refs`,
`--skip-ppc`, `--case my_planet`. Chains are written to
`pipeline/<case>/results/exorings/<run_tag>.npz` (+ `_meta.json`).

### Stop (pause)

```bash
cd pipeline
bash stop_sweep_parallel.sh            # SIGTERM the runner
bash stop_sweep_parallel.sh --status   # list PIDs only
```

Completed runs already have a `.npz` on disk. The run that was in progress (no `.npz`
yet) will restart from scratch when you resume — that is expected.

### Resume

Re-run the **same** launch command. Finished tags are reported as `[SKIP]`:

```bash
cd pipeline
nohup bash run_sweep_parallel.sh --n-procs 6 > sweep_parallel_96.log 2>&1 &
tail -f sweep_parallel_96.log
```

Configs whose prior never intersects the KDE (typical when `T14` is in the likelihood and
`ρ★,true`/`b` are fixed) are reported as `[PLATEAU]` and are **not** saved.

More detail: [`pipeline/README.md`](pipeline/README.md).

## License

MIT — see [`LICENSE`](LICENSE).

## Citation

If you use this method, please cite:

> Zuluaga, J.I., Kipping, D., Sucerquia, M., Alvarado, J. A. "A novel method for identifying
> exoplanetary rings", ApJL 803, L14 (2015).

## Contact

- Sebastián Numpaque — david.rodriguez1@udea.edu.co
- Jorge I. Zuluaga — jorge.zuluaga@udea.edu.co
