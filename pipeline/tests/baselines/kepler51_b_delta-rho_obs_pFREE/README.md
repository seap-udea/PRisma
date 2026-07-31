# Baseline: Kepler-51 b · δ+ρ★,obs · p free

Golden reference for the package-layout regression test.

| Field | Value |
|-------|--------|
| Source | `pipeline/kepler_51/results/exorings/` (campaign before `exorings`/`geotrans` move) |
| Run tag | `kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_pFREE` |
| Files | `reference_meta.json` (full meta), `reference_summary.json` (logZ + posterior percentiles) |

The regression script re-runs this exact dynesty config (`nlive=1200`, `seed=2026`, `n_procs=1`) and checks that lnZ is close and that posterior medians / 16–84% edges stay within a fraction of the reference credible-interval width (NS noise is expected; the saved campaign used `n_procs=6`).
