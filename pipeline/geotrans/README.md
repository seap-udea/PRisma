# geotrans — independent, numerically-integrated ring-transit model

`geotrans` is a refactor of J. Zuluaga's original `GeoTrans` code. Unlike the closed-form
[`exorings`](../exorings/) model, it computes a ringed-planet transit by **numerically integrating**
the projected ring+planet area — slower, but more rigorous, especially near grazing / edge-on
geometries.

It lives under [`pipeline/`](../) next to `photoring` and `exorings` because the inference stack
imports it as an optional forward model and for orientation / ring diagrams.

## Roles

1. **Validation** — cross-check the closed-form `exorings` model (see `.legacy/geotrans/tests/` for
   exploratory notebooks; automated checks are in [`../tests/`](../tests/)).
2. **Alternative forward model** — drop-in for the inference pipeline via
   `MODEL_CONFIG['FORWARD_MODEL'] = 'geotrans'`.
3. **Geometry rendering** — draw projected ring diagrams (`photoring.plotting`, Contours notebook).

## API

```python
from geotrans.model import geotrans2_model

obs = geotrans2_model(rhotrue_gcc=1.406, P_days=365.0, b=0.19, p=0.08,
                      fi=1.5, fe=2.35, tau=1.0, theta_deg=30.0, ir_deg=80.0)
# -> dict(delta, T14, T23, rhoobs, bobs, aobs, pobs, logPR)   or   None (unphysical)
```

`geotrans2_model` has **exactly the same signature and return contract** as
[`exorings.forward.forward_observables`](../exorings/forward.py). The heavy lifting is in
[`geotrans.py`](geotrans.py) (`RingedSystem`, `Figure`, geometric primitives), also imported as
`geotrans.geotrans`.

```python
import geotrans.geotrans as geo
# geo.RingedSystem, geo.dict2obj, geo.MSUN, ...
```

## Contents

| File | Contents |
|---|---|
| `model.py` | `geotrans2_model(...)` — sampler-friendly wrapper (dict / `None`) |
| `geotrans.py` | full model: `RingedSystem`, geometry, area integration, plotting |

The fuller original `geotrans2.py` and Spanish exploratory notebooks live under
[`.legacy/geotrans/`](../../.legacy/geotrans/).

## Reference

> Zuluaga, J.I., Kipping, D., Sucerquia, M., Alvarado, J.A. "A novel method for identifying
> exoplanetary rings", ApJL 803, L14 (2015).
