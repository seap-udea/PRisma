# PRisma: PhotoRing inference and modeling algorithm

**PRisma** is an open-source Bayesian pipeline for detecting and characterizing exoplanetary rings via the **PhotoRing (PR) effect** — an asterodensity-profiling signature in which unmodeled rings bias the stellar density inferred from a transit. The repository ships the full inference stack (forward models, likelihood, nested sampling) and a complete worked application to the Kepler-51 “super-puff” planets, including the notebooks, reference chains, tables, and figures that underlie the accompanying manuscript.

## Citing this work

If you use this code or results, please cite:

> Numpaque, S., Zuluaga, J. I., Kipping, D., & Alvarado-Montes, J. A. *Probing Exoplanetary Rings with Asterodensity Profiling: A PhotoRing Analysis of Kepler-51*. In preparation.

```bibtex
@misc{NumpaqueZuluaga2026PRisma,
  author        = {Numpaque, Sebasti{\'a}n and Zuluaga, Jorge I.
                   and Kipping, David and Alvarado-Montes, Jaime A.},
  title         = {Probing Exoplanetary Rings with Asterodensity Profiling:
                   A PhotoRing Analysis of Kepler-51},
  year          = {2026},
  note          = {In preparation},
  howpublished  = {\url{https://github.com/seap-udea/PRisma}}
}
```

The geometric PhotoRing framework itself was introduced in:

> Zuluaga, J. I., Kipping, D., Sucerquia, M., & Alvarado, J. A. (2015). *A novel method for identifying exoplanetary rings*. The Astrophysical Journal Letters, 803, L14.

---

## Scientific summary

### The PhotoRing (PR) effect

Asterodensity profiling compares the mean stellar density inferred from transit observables — depth $\delta$, durations $T_{14}$ and $T_{23}$, impact parameter, and period — with an independent estimate of the star’s true density $\rho_{\star,\mathrm{true}}$ (e.g. from isochrones). When an unmodeled phenomenon distorts the light curve, the transit-inferred density $\rho_{\star,\mathrm{obs}}$ disagrees with $\rho_{\star,\mathrm{true}}$.

Planetary rings are one such phenomenon. A ringed planet occults a larger projected area than a bare planet of the same physical size, so the fitted radius is overestimated and the contact times are shifted. These biases propagate into $\rho_{\star,\mathrm{obs}}$, producing the **PhotoRing (PR) effect** (Zuluaga et al. 2015). The PR diagnostic is conventionally written

$$
\mathrm{PR} \equiv 10\log_{10}\!\left(\frac{\rho_{\star,\mathrm{obs}}}{\rho_{\star,\mathrm{true}}}\right).
$$

Negative PR values mean the transit underestimates the true stellar density — the regime most often expected for opaque rings, and a candidate explanation for the extreme “super-puff” densities of Kepler-51 b and d.

The contour map below shows how PR varies with ring orientation ($\cos i_R$, $\theta_R$) for a Kepler-51b analogue. Icons illustrate the projected ring geometry at each location; blue (red) regions mark overestimated (underestimated) $\rho_{\star,\mathrm{obs}}$.

<p align="center">
  <img src="papers/kepler51/figures/PRContours-K51b.png" alt="PR contour map for a Kepler-51b analogue" width="640"/>
</p>

<p align="center"><em>Figure — PhotoRing contour for a Kepler-51b analogue ($R_p = 1.9\,R_\oplus$, $f_i = 1$, $f_e = 2$). Color encodes PR; the highlighted contour marks $\mathrm{PR} = 0.865$.</em></p>

### Bayesian retrieval and products

PRisma turns that geometric idea into a full Bayesian retrieval. A deterministic forward model (`exorings`) maps a ringed-planet configuration — outer radius $f_e$, ring inclination $i_R$, tilt $\theta_R$, planet-to-star radius ratio $p$, optical depth $\tau$, plus optional nuisance parameters $\rho_{\star,\mathrm{true}}$ and $b$ — onto predicted transit observables. Those predictions are compared to empirical observable posteriors (from TTV photometry) through a KDE likelihood. Nested sampling (`dynesty`) explores the posterior and returns the Bayesian evidence.

Primary products of each retrieval:

1. **Posterior chains** over ring geometry (and free nuisance parameters), saved as compressed NumPy archives with sidecar metadata.
2. **Corner plots** summarizing the joint posterior, optionally with an inset of the median ring geometry.
3. **Posterior predictive checks (PPCs)** comparing predicted vs. observed distributions of $\delta$, $T_{14}$, $T_{23}$, $\rho_{\star,\mathrm{obs}}$, and $b_{\mathrm{obs}}$.

Examples for Kepler-51 d (all-free retrieval with likelihood $\mathcal{L}_{\mathrm{KDE}}[\delta,\,T_{14},\,\rho_{\star,\mathrm{obs}}]$):

<p align="center">
  <img src="papers/kepler51/figures/final_planetd_panel_reduced.png" alt="Corner plot for Kepler-51 d" width="560"/>
</p>

<p align="center"><em>Figure — Joint posterior (corner plot) for Kepler-51 d, with the median ring geometry inset.</em></p>

<p align="center">
  <img src="papers/kepler51/figures/ppp_planet_d_vertical.png" alt="Posterior predictive check for Kepler-51 d" width="420"/>
</p>

<p align="center"><em>Figure — Posterior predictive check for Kepler-51 d. Grey: photometric (TTV) observables; teal: predictions drawn from the posterior.</em></p>

---

## Repository contents

| Path | Role |
|---|---|
| [`papers/`](papers/) | Manuscript material, organized by paper. |
| [`papers/kepler51/`](papers/kepler51/) | Kepler-51 paper: LaTeX source, `PRisma-*.ipynb` notebooks, `figures/`, `reference_runs/`, and generated tables (`tab_*.tex`). Running `make notebooks` regenerates figures and tables from the versioned chains. |
| [`pipeline/`](pipeline/) | The PRisma algorithm: packages and scripts that implement the PR Bayesian pipeline. |
| [`pipeline/photoring/`](pipeline/photoring/) | Core analysis package — observables, likelihood, priors, inference, I/O, plotting. |
| [`pipeline/exorings/`](pipeline/exorings/) | Closed-form ringed-transit forward model (default). |
| [`pipeline/geotrans/`](pipeline/geotrans/) | Independent numerical ring-transit model (validation / diagrams). |
| [`pipeline/kepler_51/`](pipeline/kepler_51/) | Bundled case study: TTV inputs, observable posteriors, $\rho_{\star,\mathrm{true}}$ samples, and versioned result chains. |
| [`pipeline/run_sweep_parallel.py`](pipeline/run_sweep_parallel.py) | Parallel dynesty campaign runner (preferred). |
| [`.legacy/`](.legacy/) | Superseded exploratory material kept for provenance. |

---

## Quickstart

### System requirements

> **Python 3.9–3.12 recommended.** A multi-core workstation or laptop is strongly preferred: each nested-sampling run uses `nlive = 1200` live points and benefits from several CPU workers (`--n-procs`). A full Kepler-51 campaign is **96** dynesty configurations; on a 6-core machine a single run typically takes on the order of minutes to tens of minutes depending on the free-parameter set. Disk space for a full `results/` tree is a few hundred MB to a few GB.

### Clone and install

```bash
git clone https://github.com/seap-udea/PRisma.git
cd PRisma

python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

No package install step is required beyond `requirements.txt`: put `pipeline/` on `sys.path` (the sweep scripts do this automatically) and import `photoring`, `exorings`, and `geotrans` directly.

Optional, for manuscript notebooks in Jupyter / VS Code:

```bash
python -m ipykernel install --user --name prisma --display-name "Python (PRisma)"
```

### Critical inputs for Bayesian inference

Everything needed to run (or re-run) the Kepler-51 retrieval lives under `pipeline/kepler_51/`:

```
pipeline/kepler_51/
├── inputs/
│   ├── ttv/<planet>/…post_equal_weights.dat   # TTV posterior samples
│   ├── observables/kepler_51_<planet>_observables.dat
│   └── rho_true_data/
│       ├── rho_true_samples.dat               # ρ★,true (Berger et al. 2023)
│       └── rho_grid_cdf.txt
└── results/exorings/                          # <run_tag>.npz + _meta.json
```

The combinatorial grid (planets × KDE observable sets × free-parameter toggles), nested-sampling settings, and planet-specific priors are defined in [`pipeline/run_sweep.py`](pipeline/run_sweep.py). The likelihood, forward-model wiring, and sampler drivers live in [`pipeline/photoring/`](pipeline/photoring/).

Manuscript figures do **not** need a fresh sweep: they read the frozen chains in [`papers/kepler51/reference_runs/`](papers/kepler51/reference_runs/).

### Preview a parallel campaign

```bash
cd pipeline
bash run_sweep_parallel.sh --dry-run --n-procs 6
```

Useful variants:

```bash
# Only the two manuscript reference tags (all-free; L = δ, T14, ρ★,obs)
bash run_sweep_parallel.sh --dry-run --validate-refs --n-procs 6
```

### Launch a parallel run

```bash
cd pipeline
nohup bash run_sweep_parallel.sh --n-procs 6 > sweep_parallel_96.log 2>&1 &
tail -f sweep_parallel_96.log
```

Flags worth knowing:

| Flag | Meaning |
|---|---|
| `--n-procs N` | Dynesty worker processes per configuration |
| `--jobs J` | Run `J` configurations concurrently (workers are split) |
| `--validate-refs` | Restrict to the two manuscript reference tags |
| `--skip-ppc` | Skip posterior-predictive draws (faster; no `ppc` array) |
| `--case NAME` | Case directory under `pipeline/` (default: `kepler_51`) |

### Stop (pause)

```bash
cd pipeline
bash stop_sweep_parallel.sh            # SIGTERM the runner
bash stop_sweep_parallel.sh --status   # list PIDs only
```

Completed runs already have a `.npz` on disk and will be skipped on resume. The configuration that was in progress (no `.npz` yet) restarts from scratch — that is expected.

### Resume

Re-run the **same** launch command. Finished tags are reported as `[SKIP]`:

```bash
cd pipeline
nohup bash run_sweep_parallel.sh --n-procs 6 > sweep_parallel_96.log 2>&1 &
```

Configs whose prior never intersects the KDE support are reported as `[PLATEAU]` and are **not** saved.

### Output files

Each successful retrieval writes a pair under `pipeline/<case>/results/<forward_model>/`:

| File | Contents |
|---|---|
| `<run_tag>.npz` | Posterior `chain`, dynesty `samples` / weights / log-likelihood, and (unless `--skip-ppc`) posterior-predictive draws `ppc` |
| `<run_tag>_meta.json` | Run configuration, free/fixed flags, evidence (`logz`), runtime, and summary percentiles |

The run tag encodes the case, planet, sampler, KDE observable set, nested-sampling settings, and which of $\rho_{\star,\mathrm{true}}$, $b$, $\tau$, $p$ were free — e.g.

```
kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE
```

### Rebuild manuscript figures and tables

```bash
cd papers/kepler51
make notebooks    # syncs reference_runs/ from pipeline results, then executes all PRisma-*.ipynb
make              # compile main-v1r.pdf (requires a LaTeX toolchain)
```

---

## AI assistance disclosure

Portions of the code review, refactoring, inline documentation, debugging, and repository restructuring in this project were assisted by AI language models (used as coding assistants inside Cursor and related tools).

The human authors assert that all scientific ideas, the overall project conception, the design of the numerical and scientific experiments, the interpretation of the results, and the conclusions of the accompanying manuscript are original contributions of the human authors. AI tools were used exclusively as coding and writing assistants — analogous to a spell-checker or a compiler — and bear no intellectual authorship over the scientific content of this work. AI models also assisted with translation from Spanish (the native language of several authors) into English, and with English spelling and grammar review.

---

## Authors

- **Sebastián Numpaque** — [david.rodriguez1@udea.edu.co](mailto:david.rodriguez1@udea.edu.co) · [ORCID 0009-0000-5697-3416](https://orcid.org/0009-0000-5697-3416)
- **Jorge I. Zuluaga** — [jorge.zuluaga@udea.edu.co](mailto:jorge.zuluaga@udea.edu.co) · [ORCID 0000-0002-6140-3116](https://orcid.org/0000-0002-6140-3116)

**Affiliation:** [SEAP/FACom](https://www.udea.edu.co), Instituto de Física – FCEN, Universidad de Antioquia, Calle 70 No. 52-21, Medellín, Colombia.

---

## License

MIT — see [`LICENSE`](LICENSE).
