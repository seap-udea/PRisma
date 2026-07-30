# Paper figures — exact reproduction

Every figure in the manuscript, regenerated from this repository's pipeline code. Run
[`reproduce_paper_figures.ipynb`](reproduce_paper_figures.ipynb) and it writes each one into
[`img/`](img/) under the exact filename the LaTeX source expects.

The manuscript's LaTeX source is developed separately and is not part of this repository; only
the code and inputs behind its figures live here.

## Figure map

| Manuscript figure | File | Produced by |
|---|---|---|
| Photo-Ring effect vs ring orientation | `aPRe-PhotoRingContour-K51b.png` | `photoring.contour.plot_pr_contour` (§2) |
| Transit observable posteriors | `k51_observables_posteriors.png` | `photoring.plotting.plot_observable_posteriors` (§3) |
| Stellar-density anomaly | `rho_obs_comparison.png` | `photoring.plotting.plot_asterodensity_profiling` (§4) |
| Segment consistency, planet b | `k51_observables_posteriors_segments.png` | `photoring.plotting.plot_segment_consistency` (§5) |
| Ring geometry, planet b | `final_planetb_panel_.png` | `photoring.plotting.plot_results_panel_inset` (§6) |
| Ring geometry, planet d | `final_planetd_panel_.png` | idem (§6) |
| Posterior predictive check, planet b | `ppc_planet_b.png` | `photoring.plotting.plot_ppc` (§7) |
| Posterior predictive check, planet d | `ppp_planet_d.png` | idem (§7) |

`ppp_planet_d.png` is spelled that way in the manuscript source (a typo for `ppc_`); the
filename is preserved here so the paper still compiles.

Two files in `img/` are **not** analysis outputs and are not regenerated: `kepler_51b.png`
(illustrative artwork) and `ringed_transit.pdf` (a hand-drawn schematic of the ringed-transit
geometry). Both are inputs to the manuscript.

Superseded files also present in `img/`: `PhotoRingContour.png` (an earlier version of the
contour map, for a Saturn analogue) and `final_planet{b,d}_panel.png` without the trailing
underscore (an earlier panel layout). The manuscript uses neither.

## `reference_runs/`

The posterior chains behind the ring-geometry and PPC figures, versioned here so those figures
reproduce immediately without re-running the retrievals.

They are the manuscript's adopted configuration — the **fully free** model
(`fe, ir, theta, p, tau, rho_true, b` all sampled) with likelihood
`L_KDE = (delta, T14, rho_obs)`, nested sampling at `nlive=1200`, `dlogz=0.01`, `NKDE=5000`,
`seed=2026` — which the run tag encodes in full:

```
kepler_51_<planet>_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE
```

These are **inputs to the paper reproduction**, which is why they live here rather than under
`pipeline/<case>/results/` — that directory is gitignored, since everything in it is
regenerable pipeline output. To reproduce the chains themselves from scratch, run the pipeline
with the configuration above; see [`../pipeline/README.md`](../pipeline/README.md).

One caveat on reloaded runs: `samples`, `logwt` and `logl` are the real nested-sampling output,
which is all the corner plot needs, but the full sampling history (`samples_u`, `logvol`, …)
was not persisted for these particular runs, so `dyplot.runplot` / `dyplot.traceplot` must not
be used on them. Runs saved by the current pipeline do persist the full set — see
`photoring.io.dynesty_arrays`.

## Style

The notebook calls `plot.apply_style(plot.PAPER_STYLE)`, which switches the shared plotting
layer to the manuscript's appearance: saturated per-planet colours, LaTeX rendering, and
dynesty's default 95% credible interval in the corner titles. Because every figure is drawn
through that single style authority, they are consistent with each other by construction
rather than by hand.

`PAPER_STYLE` needs a working TeX installation. Without one:

```python
plot.apply_style(plot.PAPER_STYLE | {"use_latex": False})
```

## Reproducing

```bash
cd paper_figures
jupyter nbconvert --to notebook --execute --inplace reproduce_paper_figures.ipynb
```

The contour map (§2) is the slow part — roughly 6000 numerical contact-time solutions at the
published grid resolution. Lower `N_COS_IR` / `N_THETA` in that cell for a quick look.

Sections 3–5 need the derived-observables files, i.e. `pipeline/01_observables.ipynb` must have
been run first for the case.
