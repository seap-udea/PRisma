# AppPR — a reproducible pipeline for exoplanet-ring detection via asterodensity profiling

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

Only the pipeline's **code and the minimal input data it needs to run** are versioned here — not
the large sweep of result files/figures already produced during the thesis. Running the pipeline
regenerates `pipeline/<case>/results/` and `figures/` locally (they are gitignored).

## Repository map

| Path | Contents |
|---|---|
| [`pipeline/`](pipeline/) | **The reproducible method**: the `photoring` package (analysis as `.py` modules) + case-driven notebooks (observables → emcee/dynesty inference → figures), plus the bundled `kepler_51/` example case |
| [`exorings/`](exorings/) | The closed-form ring-transit forward model as a Python package: `forward.py` (the pipeline's model contract), `basic.py` (reference OO API) |
| [`geotrans/`](geotrans/) | An **independent**, numerically-integrated ring-transit model — validates `exorings`, serves as an alternative forward model, and draws the ring diagrams |
| [`paper_figures/`](paper_figures/) | Traceability only: the scripts and final images behind the (private) thesis figures — no LaTeX |
| [`legacy/`](legacy/) | The first, exploratory version (Monte-Carlo Rejection-Acceptance) as the installable `photoring` package it grew into — superseded, kept for reference/ground-truth |
| [`docs/`](docs/) | Science background, diagrams, and narrative history |
| [`bibliography/`](bibliography/) | Curated `.bib` reference library |

Full guided tour, including *why* each directory looks the way it does: [`STRUCTURE.md`](STRUCTURE.md).

## Quickstart

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cd pipeline
jupyter nbconvert --to notebook --execute 01_observables.ipynb
jupyter nbconvert --to notebook --execute 02_inference_dynesty.ipynb
jupyter nbconvert --to notebook --execute 03_results_plotting.ipynb
```

The notebooks default to `CASE = "kepler_51"`, reading/writing `pipeline/kepler_51/`. Nothing needs
installing — the notebooks put the repo root and `pipeline/` on `sys.path` and import `exorings`,
`geotrans` and `photoring` directly.

Or run the full configuration sweep used in the thesis:

```bash
cd pipeline
bash run_sweep.sh dynesty              # nested sampling, all configs, case kepler_51
bash run_sweep.sh emcee --dry-run      # preview configurations
```

`requirements.txt` lists dependencies without pinned versions (none were pinned in the original
research environment); pin them once you have a working install if you need a frozen environment.

## License

MIT — see [`LICENSE`](LICENSE).

## Citation

If you use this method, please cite:

> Zuluaga, J.I., Kipping, D., Sucerquia, M., Alvarado, J. A. "A novel method for identifying
> exoplanetary rings", ApJL 803, L14 (2015).

## Contact

- Sebastián Numpaque — david.rodriguez1@udea.edu.co
- Jorge I. Zuluaga — jorge.zuluaga@udea.edu.co
