# exorings — ring-transit forward model

The forward model used throughout [`../pipeline/`](../pipeline/): given a planet's true stellar
density, orbital period, impact parameter, radius ratio, and ring geometry, compute the transit
observables (depth, contact durations, apparent stellar density) a ringed planet would produce.

## Python API

Two entry points, one physics:

**1. The pipeline contract — [`forward.py`](forward.py).** `forward_observables(...)` returns a
plain dict of transit observables, or `None` for unphysical geometries — the contract the samplers
need. This is what the inference pipeline imports (it replaces the model code the notebooks used to
define inline and had let drift between the emcee and dynesty versions).

```python
from exorings.forward import forward_observables

obs = forward_observables(rhotrue_gcc=1.406, P_days=365.0, b=0.19, p=0.08,
                          fi=1.5, fe=2.35, tau=1.0, theta_deg=30.0, ir_deg=80.0)
# -> dict(delta, T14, T23, rhoobs, bobs, aobs, pobs, beta, a, logPR)  or  None
```

The `bobs_method` argument selects the impact-parameter inversion (`'kipping'`, default, or
`'mallen'`); all other outputs are independent of it.

**2. The reference OO API — [`basic.py`](basic.py).** A frozen-dataclass parameter object
(`ExoringsBasicParams`), a pure function (`compute_exorings_basic`) and a thin OO wrapper
(`ExoringsBasic`) returning a rich `ExoringsBasicResult` and *raising* on non-transiting geometries.

```python
from exorings import ExoringsBasic, ExoringsBasicParams

result = ExoringsBasic(ExoringsBasicParams(rhotrue=1.40598, P=365.2446, b=0.1875,
                                           p=0.08, fi=1.5, fe=2.35, tau=1.0,
                                           theta=30.0, ir=80.0)).compute()
print(result.delta, result.T14, result.rhoobs)
```

Both guard the `cos(ir) → 0` singularity at exactly edge-on ring inclination (`ir = 90°`). For the
underlying physics, equation by equation: [`theory.md`](theory.md).

## CLI (legacy)

The original standalone scripts still work and are kept as the reference implementation
`basic.py` was derived from:

```bash
python exorings.py                                  # dependency check
python legacy/exorings-basic.py fi=1.5 fe=2.35 theta=30.0 ir=80.0
```

Output: transit depth (ppm), total/full transit duration (hours), observed radius ratio (pobs),
observed asterodensity (rhoobs). `legacy/python2/` holds the untouched original Python 2 sources.

Note: `exorings.py` (physical constants + CLI argument parsing) lives at the package's top level,
not under `legacy/`, because `__init__.py` still imports its constants directly
(`from .exorings import ...`) to back the OO API's re-exports. Only the standalone
`exorings-basic.py` CLI script — functionally superseded by `basic.py` — moved to `legacy/`.

## Validation — the sibling `geotrans` package

`exorings` implements an *analytical approximation* of the ring-transit geometry. The independent,
numerically-integrated cross-check now lives in its own top-level package,
[`../geotrans/`](../geotrans/) (it used to sit under `exorings/`). It validates this model, offers an
alternative forward model to the pipeline (`FORWARD_MODEL='geotrans'`), and draws the ring diagrams.
See [`../geotrans/README.md`](../geotrans/README.md) and
[`../geotrans/tests/exorings_geotrans.md`](../geotrans/tests/exorings_geotrans.md): transit depth and
the opacity-blocking factor β agree to machine precision on the default parameter set; contact-time
approximations can differ by tens of seconds near grazing configurations, where `geotrans` is more
rigorous.

## Reference

> Zuluaga, J.I., Kipping, D., Sucerquia, M., Alvarado, J. A. "A novel method for identifying
> exoplanetary rings", ApJL 803, L14 (2015).
