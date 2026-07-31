"""Exorings — exoring transit calculations.

This repository started as a CLI-focused toolkit (see `exorings/exorings.py` and
`exorings/exorings-basic.py`). For research workflows (notebooks/pipelines) it's
often more convenient to *import* the computations instead of copy/pasting
formulas.

This package exposes:
- Legacy constants/utilities from `exorings/exorings.py`.
- An object-oriented API for the `exorings-basic` model (see `exorings/basic.py`).

Note: running scripts directly from inside the `exorings/` folder still works,
but for imports you typically want the repository root on `PYTHONPATH`.
"""

from __future__ import annotations

from sys import exit

import numpy as np

from .exorings import AU, DAY, DEG, GCONST, HOUR, MSUN, RAD, RSUN, dict2obj, getParameters
from .basic import (
    ExoringsBasic,
    ExoringsBasicParams,
    ExoringsBasicResult,
    ExoringsError,
    NoTransitError,
    compute_exorings_basic,
    render_exorings_basic_report,
)
from .forward import forward_observables

__all__ = [
    # Legacy re-exports
    "np",
    "DEG",
    "RAD",
    "DAY",
    "HOUR",
    "GCONST",
    "MSUN",
    "RSUN",
    "AU",
    "dict2obj",
    "getParameters",
    "exit",
    # OO API
    "ExoringsBasicParams",
    "ExoringsBasicResult",
    "ExoringsBasic",
    "ExoringsError",
    "NoTransitError",
    "compute_exorings_basic",
    "render_exorings_basic_report",
    # Sampler-friendly forward model
    "forward_observables",
]
