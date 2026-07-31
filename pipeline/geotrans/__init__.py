"""geotrans — independent, numerically-integrated ring-transit model.

This package is an isolated home for the ``geotrans`` code (a refactor of the original
``GeoTrans`` by J. Zuluaga). It is kept **separate from** :mod:`exorings` on purpose: it
is not the pipeline's default forward model but an *independent, more rigorous*
implementation used to

1. **validate** the closed-form ``exorings`` model, and
2. serve as an alternative forward model in the inference pipeline
   (``FORWARD_MODEL='geotrans'``), and
3. draw the projected ring-geometry diagrams in the results notebook.

Public API
----------
- :func:`geotrans.model.geotrans2_model` — sampler-friendly wrapper returning a dict of
  transit observables (or ``None`` for unphysical geometries), matching the
  :func:`exorings.forward.forward_observables` contract.
- :mod:`geotrans.geotrans` — the full module (``RingedSystem``, ``Figure``,
  ``plotEllipse``, geometric primitives, constants ``DEG``/``RAD``, …).

The heavy lifting lives in ``geotrans.py``, imported here as a submodule so it can
be reached as ``geotrans.geotrans`` or via the convenience re-exports below.
"""

from __future__ import annotations

from . import geotrans
from .geotrans import (
    RingedSystem,
    Figure,
    plotEllipse,
    DEG,
    RAD,
)
from .model import geotrans2_model

__all__ = [
    "geotrans",
    "geotrans2_model",
    "RingedSystem",
    "Figure",
    "plotEllipse",
    "DEG",
    "RAD",
]
