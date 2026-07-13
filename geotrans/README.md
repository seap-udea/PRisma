# geotrans — independent, numerically-integrated ring-transit model

`geotrans2` is a refactor of J. Zuluaga's original `GeoTrans` code. Unlike the closed-form
[`exorings`](../exorings/) model, it computes a ringed-planet transit by **numerically integrating**
the projected ring+planet area — slower, but more rigorous, especially near grazing / edge-on
geometries.

It lives in its **own top-level package**, deliberately *not* under `exorings`, because it plays
three independent roles:

1. **Validation** — cross-check the closed-form `exorings` model (see [`tests/`](tests/)).
2. **Alternative forward model** — drop-in for the inference pipeline via
   `MODEL_CONFIG['FORWARD_MODEL'] = 'geotrans'`.
3. **Geometry rendering** — draw the projected ring diagrams in the results notebook.

## API

```python
from geotrans.model import geotrans2_model

obs = geotrans2_model(rhotrue_gcc=1.406, P_days=365.0, b=0.19, p=0.08,
                      fi=1.5, fe=2.35, tau=1.0, theta_deg=30.0, ir_deg=80.0)
# -> dict(delta, T14, T23, rhoobs, bobs, aobs, pobs, logPR)   or   None (unphysical)
```

`geotrans2_model` has **exactly the same signature and return contract** as
[`exorings.forward.forward_observables`](../exorings/forward.py), so the pipeline swaps between the
two models transparently. The heavy lifting is in [`geotrans2_lite.py`](geotrans2_lite.py)
(`RingedSystem`, `Figure`, `plotEllipse`, geometric primitives); it is imported as
`geotrans.geotrans2_lite`.

## Contents

| File | Contents |
|---|---|
| `model.py` | `geotrans2_model(...)` — sampler-friendly wrapper (dict / `None`) |
| `geotrans2_lite.py` | the full model: `RingedSystem`, geometry classes, area integration, plotting |
| `geotrans2.py` | the fuller original `geotrans2` module (superset, kept for reference) |
| `tests/` | notebooks/notes cross-checking `exorings` vs `geotrans` (see `exorings_geotrans.md`) |

## Validation summary

For the default parameter set the closed-form transit depth and opacity-blocking factor agree with
`geotrans` to machine precision; contact-time/duration approximations can differ by tens of seconds
near grazing configurations, where `geotrans` is the more rigorous reference. `geotrans` also guards
the edge-on (`cos i_R → 0`) singularity. See [`tests/exorings_geotrans.md`](tests/exorings_geotrans.md).

## Reference

> Zuluaga, J.I., Kipping, D., Sucerquia, M., Alvarado, J.A. "A novel method for identifying
> exoplanetary rings", ApJL 803, L14 (2015).
