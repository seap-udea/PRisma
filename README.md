# PRisma: PhotoRing inference and modeling algorithm

**PRisma** is an open-source Bayesian pipeline for detecting and characterizing exoplanetary rings via the **PhotoRing (PR) effect** — an asterodensity-profiling signature in which unmodeled rings bias the stellar density inferred from a transit. The repository ships the full inference stack (forward models, likelihood, nested sampling) and a complete worked application to the Kepler-51 “super-puff” planets, including versioned reference chains under `pipeline/kepler_51/results/exorings/`, the notebooks, tables, and figures that underlie the accompanying manuscript.

The current reference setup adopts **Masuda et al. (2024)** stellar parameters ($R_\star=0.869\,R_\odot$, $M_{b,d}=6.9\,M_\oplus$) and a Gaussian prior on the true stellar density, $\rho_{\star,\mathrm{true}}\sim\mathcal{N}(2.08,\,0.08)\,\mathrm{g\,cm^{-3}}$. Full-set retrievals live in [`pipeline/kepler_51/results/exorings/full_masuda/`](pipeline/kepler_51/results/exorings/full_masuda/); the radius–opacity grid search in [`explore_radius_alpha_masuda/`](pipeline/kepler_51/results/exorings/explore_radius_alpha_masuda/).

## Citing this work

If you use this code or results, please cite:

> Zuluaga, J. I., Numpaque, S., Kipping, D., & Alvarado-Montes, J. A. *Probing Exoplanetary Rings with Asterodensity Profiling: A PhotoRing Analysis of Kepler-51*. In preparation.

```bibtex
@misc{NumpaqueZuluaga2026PRisma,
  author        = {Zuluaga, Jorge I. and Numpaque, Sebasti{\'a}n
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

```bibtex
@article{Zuluaga2015,
  author        = {{Zuluaga}, Jorge I. and {Kipping}, David M. and {Sucerquia}, Mario and {Alvarado}, Jaime A.},
  title         = {{A Novel Method for Identifying Exoplanetary Rings}},
  journal       = {\apjl},
  keywords      = {methods: analytical, occultations, planets and satellites: rings, techniques: photometric, Astrophysics - Earth and Planetary Astrophysics},
  year          = 2015,
  month         = apr,
  volume        = {803},
  number        = {1},
  eid           = {L14},
  pages         = {L14},
  doi           = {10.1088/2041-8205/803/1/L14},
  archiveprefix = {arXiv},
  eprint        = {1502.07818},
  primaryclass  = {astro-ph.EP},
  adsurl        = {https://ui.adsabs.harvard.edu/abs/2015ApJ...803L..14Z},
  adsnote       = {Provided by the SAO/NASA Astrophysics Data System}
}
```

---

## Scientific summary

### The PhotoRing (PR) effect

Asterodensity profiling compares the mean stellar density inferred from transit observables — depth $\delta$, durations $T_{14}$ and $T_{23}$, impact parameter, and period — with an independent estimate of the star’s true density $\rho_{\star,\mathrm{true}}$ (here, a Gaussian prior informed by Masuda et al. 2024). When an unmodeled phenomenon distorts the light curve, the transit-inferred density $\rho_{\star,\mathrm{obs}}$ disagrees with $\rho_{\star,\mathrm{true}}$.

Planetary rings are one such phenomenon. A ringed planet occults a larger projected area than a bare planet of the same physical size, so the fitted radius is overestimated and the contact times are shifted. These biases propagate into $\rho_{\star,\mathrm{obs}}$, producing the **PhotoRing (PR) effect** (Zuluaga et al. 2015). The PR diagnostic is conventionally written

$$
\mathrm{PR} \equiv 10\log_{10}\!\left(\frac{\rho_{\star,\mathrm{obs}}}{\rho_{\star,\mathrm{true}}}\right).
$$

Negative PR values mean the transit underestimates the true stellar density — the regime most often expected for opaque rings, and a candidate explanation for the extreme “super-puff” densities of Kepler-51 b and d.

The contour map below shows how PR varies with ring orientation ($\cos i_R$, $\theta_R$) for a Kepler-51b analogue. Icons illustrate the projected ring geometry at each location; blue (red) regions mark overestimated (underestimated) $\rho_{\star,\mathrm{obs}}$.

<p align="center">
  <img src="gallery/PRContours-K51b.png" alt="PR contour map for a Kepler-51b analogue" width="640"/>
</p>

<p align="center"><em>Figure — PhotoRing contour for a Kepler-51b analogue ($R_p = 1.9\,R_\oplus$, $f_i = 1$, $f_e = 2$). Color encodes PR; the highlighted contour marks $\mathrm{PR} = 0.865$.</em></p>

### Bayesian retrieval and products

PRisma turns that geometric idea into a full Bayesian retrieval. A deterministic forward model (`exorings`) maps a ringed-planet configuration — outer radius $f_e$, ring inclination $i_R$, tilt $\theta_R$, planet-to-star radius ratio $p$, ring opacity $\alpha=\exp(-\tau)$, plus optional nuisance parameters $\rho_{\star,\mathrm{true}}$ and $b$ — onto predicted transit observables. Those predictions are compared to empirical observable posteriors (from TTV photometry) through a KDE likelihood on $(\delta,\,T_{14},\,T_{23},\,\rho_{\star,\mathrm{obs}})$. Nested sampling (`dynesty`) explores the posterior and returns the Bayesian evidence.

Each run writes a compressed chain (`.npz`) and sidecar metadata (`_meta.json`) that records the sampler settings, posterior summaries, and—when parameters are held fixed—the explicit values used in the forward model (e.g. `P_FIXED_VALUE` and `ALPHA_FIXED` for grid-search runs). Plotting and table generation read these fields so fixed inputs match the inference configuration.

Primary products of each retrieval:

1. **Posterior chains** over ring geometry (and free nuisance parameters), saved as compressed NumPy archives with sidecar metadata.
2. **Corner plots** summarizing the joint posterior, optionally with an inset of the median ring geometry.
3. **Posterior predictive checks (PPCs)** comparing predicted vs. observed distributions of $\delta$, $T_{14}$, $T_{23}$, $\rho_{\star,\mathrm{obs}}$, and $b_{\mathrm{obs}}$.

**Kepler-51 full-set example (planet d).** All ring parameters and nuisances are free; $\rho_{\star,\mathrm{true}}$ follows the Masuda et al. (2024) Gaussian prior above. Posterior medians: $f_e=1.73\,R_p$, $i_R=70.9^\circ$, $\theta_R=67.3^\circ$, $p=0.081$, $\alpha=0.34$, $\rho_{\star,\mathrm{true}}=2.14\,\mathrm{g\,cm^{-3}}$, $b=0.28$; $\ln\mathcal{Z}=6.94$. Under the same mass assumption, this corresponds to $R_p\simeq7.7\,R_\oplus$ and $\rho_p\simeq0.08\,\mathrm{g\,cm^{-3}}$—roughly a factor of two above the ringless TTV-inferred density ($\rho_p\simeq0.04\,\mathrm{g\,cm^{-3}}$). Planet b shows a similar $\sim\times2$ shift in the full-set retrieval ($R_p\simeq5.5\,R_\oplus$, $\rho_p\simeq0.23\,\mathrm{g\,cm^{-3}}$ vs. $0.11\,\mathrm{g\,cm^{-3}}$ ringless).

<p align="center">
  <img src="gallery/final_planetd_panel_.png" alt="Corner plot for Kepler-51 d (full-set retrieval)" width="640"/>
</p>

<p align="center"><em>Figure — Joint posterior for Kepler-51 d (all-free retrieval; likelihood $\mathcal{L}_{\mathrm{KDE}}[\delta,\,T_{14},\,T_{23},\,\rho_{\star,\mathrm{obs}}]$; nuisances $\rho_{\star,\mathrm{true}}$ and $b$ free; Masuda et al. 2024 prior on $\rho_{\star,\mathrm{true}}$). Medians listed in the panel header; ring inset shows the projected median geometry.</em></p>

<p align="center">
  <img src="gallery/ppc_planet_d_vertical.png" alt="Posterior predictive check for Kepler-51 d" width="420"/>
</p>

<p align="center"><em>Figure — Posterior predictive check for the same Kepler-51 d retrieval ($\langle z_1\rangle=1.60$). Grey: TTV-derived observable KDEs; teal: posterior predictive draws. Header lists the same median ring parameters as the corner plot.</em></p>

> 💡 **Explore more figures in the [PRisma Image Gallery](https://seap-udea.github.io/gallery/?repo=PRisma&id=golden_samples)** (Kepler-51 grid-search corner/PPC figures; Masuda et al. 2024 stellar density). [Main-text figures](https://seap-udea.github.io/gallery/?repo=PRisma&id=main) are in a separate gallery section.

---

## Repository contents

| Path | Role |
|---|---|
| [`gallery/`](gallery/) | Frozen copies of the figures embedded in this README (independent of regenerable `papers/*/figures/`). Synced from the Masuda et al. (2024) reference runs in `full_masuda/`. |
| [`papers/`](papers/) | Manuscript material, organized by paper. |
| [`papers/kepler51/`](papers/kepler51/) | Kepler-51 paper: LaTeX source, `PRisma-*.ipynb` notebooks, `figures/`, and generated tables (`tab_*.tex`). Running `make notebooks` regenerates figures and tables from the versioned chains under `pipeline/kepler_51/results/exorings/full_masuda/` and `explore_radius_alpha_masuda/`. |
| [`pipeline/`](pipeline/) | The PRisma algorithm: packages and scripts that implement the PR Bayesian pipeline. |
| [`pipeline/photoring/`](pipeline/photoring/) | Core analysis package — observables, likelihood, priors, inference, I/O, plotting (`fixed_p_from_meta`, metadata-aware corner/PPC annotations). |
| [`pipeline/exorings/`](pipeline/exorings/) | Closed-form ringed-transit forward model (default). |
| [`pipeline/geotrans/`](pipeline/geotrans/) | Independent numerical ring-transit model (validation / diagrams). |
| [`pipeline/kepler_51/`](pipeline/kepler_51/) | Bundled case study: TTV inputs, observable posteriors, and versioned result chains (`full_masuda/`, `explore_radius_alpha_masuda/`, …). |

---

## Running PRisma

All pipeline execution details are documented in [`pipeline/README.md`](pipeline/README.md).
For running analyses, generating figures, PPC ordering (`z1`/`ORDKEY`), and gallery previews, use that guide.

---

## AI assistance disclosure

Portions of the code review, refactoring, inline documentation, debugging, and repository restructuring in this project were assisted by AI language models (used as coding assistants inside Cursor and related tools).

The human authors assert that all scientific ideas, the overall project conception, the design of the numerical and scientific experiments, the interpretation of the results, and the conclusions of the accompanying manuscript are original contributions of the human authors. AI tools were used exclusively as coding and writing assistants — analogous to a spell-checker or a compiler — and bear no intellectual authorship over the scientific content of this work. AI models also assisted with translation from Spanish (the native language of several authors) into English, and with English spelling and grammar review.

---

## Authors

- **Jorge I. Zuluaga** — [jorge.zuluaga@udea.edu.co](mailto:jorge.zuluaga@udea.edu.co) · [ORCID 0000-0002-6140-3116](https://orcid.org/0000-0002-6140-3116)
- **Sebastián Numpaque** — [david.rodriguez1@udea.edu.co](mailto:david.rodriguez1@udea.edu.co) · [ORCID 0009-0000-5697-3416](https://orcid.org/0009-0000-5697-3416)

**Affiliation:** [SEAP/FACom](https://www.udea.edu.co), Instituto de Física – FCEN, Universidad de Antioquia, Calle 70 No. 52-21, Medellín, Colombia.

---

## License

MIT — see [`LICENSE`](LICENSE).
