# Repository structure — guided tour

What every top-level directory is for, why it is organised this way, and where to start. For
the physics see [`docs/science_background.md`](docs/science_background.md); for running the method
see [`pipeline/README.md`](pipeline/README.md).

## Design principle

The repo separates three things that were tangled together in the original research working
directory:

1. **The forward models** — [`pipeline/exorings/`](pipeline/exorings/) (closed-form) and
   [`pipeline/geotrans/`](pipeline/geotrans/) (numerically integrated) — next to the analysis code.
2. **The reproducible method** — [`pipeline/`](pipeline/): the `photoring` package plus the
   parallel dynesty sweep and case directories.
3. **A concrete application** — Kepler-51 under [`pipeline/kepler_51/`](pipeline/kepler_51/), with
   manuscript notebooks/figures under [`papers/kepler51/`](papers/kepler51/).

Nothing installs: put `pipeline/` on `sys.path` and `import exorings`, `geotrans`, `photoring`.
Superseded material lives under [`.legacy/`](.legacy/).

## Top-level layout

```
PRisma/
├── pipeline/                 # THE reproducible method
│   ├── photoring/            #   analysis modules
│   ├── exorings/             #   closed-form ring-transit forward model
│   ├── geotrans/             #   numerical ring-transit model (validation / alt FM)
│   ├── run_sweep.py          #   shared sweep grid + PLANET_PARAMS
│   ├── run_sweep_parallel.py #   preferred dynesty runner (no papermill)
│   ├── tests/
│   └── kepler_51/            #   worked example (inputs + versioned results/)
├── papers/kepler51/          # manuscript notebooks, figures/, reference_runs/
├── docs/
├── bibliography/
├── .legacy/                  # papermill notebooks, old geotrans tests, etc.
├── STRUCTURE.md
└── README.md  requirements.txt  LICENSE
```

## `pipeline/exorings/` — closed-form forward model

Default ring-transit model (Zuluaga et al. 2015). See [`pipeline/exorings/README.md`](pipeline/exorings/README.md).

- `forward.py` — sampler contract (`forward_observables`)
- `basic.py` — OO reference API
- `theory.md` — equation walkthrough (Spanish)

## `pipeline/geotrans/` — independent validation model

Numerical integration of projected ring+planet area. See
[`pipeline/geotrans/README.md`](pipeline/geotrans/README.md). Used to validate `exorings`, as
`FORWARD_MODEL='geotrans'`, and for PR-contour / ring diagrams.

## `pipeline/` — the reproducible method

Core deliverable: [`photoring/`](pipeline/photoring/), the Kepler-51 case, and the sweep runners.
**Start with [`pipeline/README.md`](pipeline/README.md).**

Manuscript figures and tables are regenerated from
[`papers/kepler51/`](papers/kepler51/) (`make notebooks`), not from `pipeline/<case>/figures/`
(optional diagnostic scratch; gitignored; not required for the paper).

## `papers/kepler51/`

LaTeX manuscript + `PRisma-*.ipynb` that write `figures/` and `tab_*.tex`. Preferred posterior
chains: `reference_runs/`.

## `.legacy/`

Papermill inference notebooks, the old `run_sweep.sh` launcher, exploratory Spanish geotrans
notebooks, and other superseded copies. Not on the hot path.

## `docs/` / `bibliography/`

Science background and curated `.bib` library.

## What's deliberately *not* versioned

- `pipeline/**/figures/` — regenerable diagnostic plots (gitignored).
- `tests_outputs/`, `tests_logs/`.
- Posterior chains under `pipeline/**/results/` **are** versioned so tables/figures can be rebuilt
  without re-running nested sampling.
