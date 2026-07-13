# Scientific background

## The Photo-Ring effect

The **Photo-Ring (PR) effect** (Zuluaga et al. 2015, ApJL 803, L14) is a systematic bias in
transit-derived stellar density caused by an unmodeled planetary ring system. When a ringed planet
transits its host star:

1. **Increased transit depth** — the projected area of the rings adds to the planet's silhouette,
   inflating the observed transit depth δ and, if unmodeled, the inferred planetary radius.
2. **Modified contact times** — rings extend the total transit duration T₁₄ (earlier first
   contact, later fourth contact) and can shorten the full-transit duration T₂₃.
3. **Biased stellar density** — because ρ★,obs is derived from (δ, T₁₄, T₂₃, P) via
   Seager & Mallén-Ornelas (2003), these geometric distortions propagate into a stellar density
   that differs systematically from the star's true density ρ★,true.

This negative deviation (in the sense defined below) is what distinguishes rings from other
"photo-X" biases discussed in the asterodensity-profiling literature (Kipping 2014):
**PhotoEccentric** (eccentric orbits, opposite-sign deviation), **PhotoBlend** (unresolved stellar
companions), and **PhotoSpot** (unocculted starspots).

### Key relations

Stellar density from transit observables (Seager & Mallén-Ornelas 2003):

```
ρ★,obs = (3π / G P²) × (a/R★)³_obs
```

Scaled semi-major axis and impact parameter, both derived from the observables (δ, T₁₄, T₂₃, P):

```
(a/R★)²_obs = [(1+√δ)² − b²_obs(1 − sin²(πT14/P))] / sin²(πT14/P)

b²_obs = [(1−√δ)² − sin²(πT23/P)/sin²(πT14/P)·(1+√δ)²] / [1 − sin²(πT23/P)/sin²(πT14/P)]
```

The forward model used throughout `pipeline/` (`exorings_model`, mirrored in
[`exorings/basic.py`](../exorings/basic.py)) predicts (δ, T₁₄, T₂₃, ρ★,obs, b_obs) for a ringed
planet given its true density, orbital period, impact parameter, planet-to-star radius ratio, and
ring geometry (inner/outer radius, opacity, projected inclination and tilt) — see
[`pipeline/README.md`](../pipeline/README.md) for the exact parameter definitions and priors used
in the Bayesian inference.

## The Kepler-51 system

Kepler-51 hosts four known transiting planets (b, c, d, and a fourth, e, discovered later — see
Masuda et al. 2024), all with exceptionally low densities (ρ < 0.1 g/cm³, "super-puffs").

**Stellar properties:** (Berger et al. 2023)
- Mass: M★ = 0.915 ± 0.050 M☉
- Radius: R★ = 0.869 ± 0.029 R☉

**Kepler-51b** (Masuda et al. 2024):
- Orbital period: P = 45.154 ± 0.0004 days
- Observed planetary radius: Rp = 0.609 ± 0.012 Rjup
- Planetary mass (from TTVs): Mp = 0.011 ± 0.007 Mjup
- Impact parameter: b = 0.074 ± 0.072
- Orbital inclination: iorb ≈ 89.93°
- Minimum physical radius (max density for Mp): Rp,min = 0.138 Rjup

This project asks whether rings around Kepler-51 b and d can reconcile ρ★,obs (as inferred from
each planet's own transit) with ρ★,true (as measured independently from the star, e.g. via
asteroseismology/spectroscopy, Berger et al. 2023) — i.e. whether the "super-puff" appearance is,
at least partly, a ring illusion rather than an intrinsically inflated planet.

## Two generations of method in this repo

1. **`legacy/`** — the original approach: Monte Carlo Rejection-Acceptance (MCRA) sampling over a
   5×5 grid in stellar (M★, R★) space, comparing sampled ring configurations against target
   density distributions p(ρ★,obs) and p(δ). See [`legacy/README.md`](../legacy/README.md).
2. **`pipeline/`** — the current approach: a joint KDE likelihood built directly from each
   planet's TTV posterior (no stellar grid needed), sampled with `emcee` and independently with
   `dynesty` (which additionally yields the Bayesian evidence ln Z). This is the method intended
   for reuse on new targets. See [`pipeline/README.md`](../pipeline/README.md).

## Core references

- Zuluaga et al. (2015, ApJL, 803, L14) — original Photo-Ring effect paper.
- Kipping (2014) — asterodensity profiling methodology.
- Seager & Mallén-Ornelas (2003) — transit-density relations.
- Masuda et al. (2024) — Kepler-51 system characterization and discovery of planet e.
- Berger et al. (2023) — Kepler stellar properties catalog (used as the ρ★,true prior).
- Barnes & Fortney (2004) — detectability of Saturn-like rings.
- Akinsanmi et al. (2020) — HIP 41378 f as a ringed-planet candidate.