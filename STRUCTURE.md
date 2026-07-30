# Repository structure — guided tour

What every top-level directory is for, why it is organised this way, and where to start. For
the physics see [`docs/science_background.md`](docs/science_background.md); for running the method
see [`pipeline/README.md`](pipeline/README.md).

## Design principle

The repo separates three things that were tangled together in the original research working
directory:

1. **The forward models** — [`exorings/`](exorings/) (closed-form ring transit) and
   [`geotrans/`](geotrans/) (numerically-integrated, independent) — as reusable packages.
2. **The reproducible method** — [`pipeline/`](pipeline/): the `photoring` package (the analysis
   as importable `.py` modules) plus thin, case-driven notebooks that guide you through it.
3. **A concrete application** — Kepler-51, which lives *inside* the pipeline as a self-contained
   case directory ([`pipeline/kepler_51/`](pipeline/kepler_51/)): its inputs, outputs and writeup.

Nothing installs: the notebooks put the repo root and `pipeline/` on `sys.path` and `import
exorings`, `geotrans`, `photoring` directly. Everything that predates this design (the first,
exploratory MCRA analysis) is kept under [`legacy/`](legacy/).

## Top-level layout

```
AppPR/
├── exorings/            # closed-form ring-transit forward model (package)
├── geotrans/            # independent numerically-integrated model (package)
├── pipeline/            # THE reproducible method
│   ├── photoring/       #   the analysis as importable modules
│   ├── 01_observables.ipynb          02_inference_{emcee,dynesty}.ipynb
│   ├── 03_results_plotting.ipynb
│   ├── run_sweep.py / run_sweep.sh   # multi-config sweep (papermill)
│   ├── tests/           #   forward-model equivalence tests
│   └── kepler_51/       #   the bundled worked example (inputs + outputs + writeup)
├── paper_figures/       # traceability for the (private) thesis figures
├── legacy/              # first exploratory version (MCRA); superseded, kept for reference
├── docs/                # science background, diagrams, history
├── bibliography/        # curated .bib library
├── STRUCTURE.md         # this file
└── README.md  requirements.txt  LICENSE
```

## `exorings/` — closed-form forward model

The default ring-transit model (Zuluaga et al. 2015): given a planet's true stellar density,
period, impact parameter, radius ratio and ring geometry, it computes the transit observables a
ringed planet produces.

- [`forward.py`](exorings/forward.py) — `forward_observables(...)`: the **sampler contract** used by
  the pipeline (returns a dict of observables, or `None` for unphysical geometries). This replaces
  the model code the notebooks used to define inline.
- [`basic.py`](exorings/basic.py) — the reference OO API (`ExoringsBasic`, `compute_exorings_basic`)
  returning a rich dataclass and raising on non-transiting geometries.
- [`exorings.py`](exorings/exorings.py) — physical constants + the legacy CLI parser.
- [`legacy/`](exorings/legacy/) — the original standalone `exorings-basic.py` script and its
  untouched Python-2 sources.
- [`theory.md`](exorings/theory.md) — physics-to-code walkthrough of every equation (Spanish).

## `geotrans/` — independent validation model

An isolated home for the `geotrans2` code (a refactor of J. Zuluaga's `GeoTrans`). It is
deliberately **separate from `exorings`**: it numerically integrates the projected ring+planet
area — slower but more rigorous — and is used to (a) validate `exorings`, (b) act as an alternative
forward model in the pipeline (`FORWARD_MODEL='geotrans'`), and (c) draw the ring-geometry diagrams.
See [`geotrans/README.md`](geotrans/README.md); `model.py` exposes `geotrans2_model(...)` with the
same contract as `exorings.forward.forward_observables`.

## `pipeline/` — the reproducible method

The core deliverable. The analysis is packaged as importable modules in
[`photoring/`](pipeline/photoring/) (observables, KDE likelihood, priors, the `PhotoRingModel`,
samplers, publication plotting); the five numbered notebooks are thin guides that import them and
are driven by a single `CASE` variable. Outputs are structured by forward model
(`results/<model>/`) and by figure type (`figures/<type>/`). **Start with
[`pipeline/README.md`](pipeline/README.md).**

`pipeline/kepler_51/` is the bundled worked example — Kepler-51 b/c/d inputs, its regenerated
outputs, and [`pipeline/kepler_51/README.md`](pipeline/kepler_51/README.md). Copy it to
`pipeline/<your_target>/` to run the method on new data.

## `paper_figures/`

Exact reproduction of the manuscript's figures — a notebook driving the shared plotting layer, the reference posterior chains (`reference_runs/`) and the final images
(`img/`) — **without any LaTeX**. See [`paper_figures/README.md`](paper_figures/README.md).

## `legacy/`

The first, exploratory version of the analysis: Monte-Carlo Rejection-Acceptance (MCRA) sampling on
a stellar-parameter grid, kept as the installable `photoring` package it grew into. Superseded by
`pipeline/`, but kept because a few of its artifacts are still cited as ground truth and because it
documents how the method evolved. See [`legacy/README.md`](legacy/README.md).

## `docs/`

- [`science_background.md`](docs/science_background.md) — the physics (start here if new to the
  Photo-Ring effect).
- diagrams / history — conceptual schematics and primary-source narrative material.

## `bibliography/`

`bibliography.bib` — the curated reference library (Zuluaga 2015, Kipping 2014, Seager &
Mallén-Ornelas 2003, …). Reference PDFs are not redistributed (copyright; see `.gitignore`).

## What's deliberately *not* here

- **The paper's LaTeX source** — private; only figure-generating code and final images are traced.
- **Bulk generated results/figures** — the pipeline regenerates them on demand
  (`pipeline/**/results/`, `figures/` are gitignored).
- **Large external datasets** referenced by the legacy analysis.
