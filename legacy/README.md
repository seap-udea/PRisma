# Legacy — the first exploratory version of the analysis

Before the TTV-posterior + KDE-likelihood approach now in [`../pipeline/`](../pipeline/) existed, the
analysis was built as a small installable package, [`photoring/`](photoring/), using **Monte-Carlo
Rejection-Acceptance (MCRA)** sampling on a stellar-parameter grid. That package is preserved here
essentially intact — its clean `package/` + `dev/` structure is, in fact, the model the current
`pipeline/` was reorganised to resemble.

**This is not the recommended way to run the method today** — use [`../pipeline/`](../pipeline/).
It is kept because (a) it documents how the method arrived at its current form, and (b) a few of its
artifacts (interpolated target-density functions) are still cited as ground truth by the (private)
paper draft.

## `photoring/` — the MCRA package

```
photoring/
├── package/photoring/          # the importable package
│   ├── photoring.py            #   forward model + system definitions
│   ├── montecarlo.py           #   MCRA machinery (mcra_grid_general, parallel_mcra_grid)
│   ├── geotrans.py             #   the original numerically-integrated ring-transit model
│   ├── constants.py  plot.py  version.py
│   └── data/
│       ├── GKTHCatalogue.csv               # stellar catalogue
│       └── kepler51/rho_{obs_b,obs_c,obs_d,true}_fun.pkl   # interpolated target-density PDFs (ground truth)
├── dev/                        # per-planet application notebooks + .py mirrors
│   ├── pr-kepler51{b,c,d}.ipynb / .py       pr-tutorial.ipynb
│   └── prdata/                 # MCRA output samples/figures (regenerable; gitignored)
├── pyproject.toml  setup.py  Makefile  LICENSE
```

### The MCRA method (for context)

Monte-Carlo Rejection-Acceptance on a grid in stellar parameter space:

- **Stellar grid** in `(M★, R★)` with multivariate-Gaussian weights capturing the mass–radius
  correlation.
- **Sampled parameters**: ring outer radius `fe`, planet radius, ring inclination `ir`, ring roll
  `phir`, optionally ring opacity `tau`.
- **Target distributions**: the transit-fit `p(ρ★,obs)` and `p(δ)`; acceptance
  `α = p(ρ_obs)·p(δ) / (p_max,ρ·p_max,δ)`.

Why it was superseded: it requires `(M★, R★)` as explicit inputs and a hand-built stellar grid; the
current `pipeline/` builds its likelihood directly from each planet's TTV posterior — more direct and
immediately reusable on a new target.

## Still cited as ground truth

- `photoring/package/photoring/data/kepler51/rho_true_fun.pkl`, `rho_obs_{b,c,d}_fun.pkl` —
  interpolated target-density PDFs. Small, genuinely reusable inputs.
- `photoring/package/photoring/geotrans.py` — the original numerically-integrated model, adapted
  into the top-level [`../geotrans/`](../geotrans/) package as the pipeline's validation harness.

Not versioned: the MCRA output sample CSVs and figures under `dev/prdata/` (regenerable; gitignored),
and large external TTV/MultiNest archives.
