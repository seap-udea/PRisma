"""photoring — the Photo-Ring Bayesian-inference pipeline as importable modules.

This package is the reusable core of ``pipeline/``: it turns a transiting planet's TTV
posterior into a posterior over ring geometry (and the Bayesian evidence), testing whether
a ring system can explain the planet's stellar-density anomaly (the Photo-Ring effect,
Zuluaga et al. 2015).

The pipeline notebooks (``pipeline/0*.ipynb``) are thin guides that import from here; the
concrete Kepler-51 application lives in ``pipeline/kepler_51/``. To run the method on your
own target, copy that case directory, drop your data in, and set ``CASE`` in the notebooks.

Layers
------
- Case layout / IO ....... :mod:`photoring.config`, :mod:`photoring.io`
- Step 1 (observables) ... :mod:`photoring.observables`, :mod:`photoring.rho_cdf`
- Model ................... :mod:`photoring.likelihood`, :mod:`photoring.priors`,
                            :class:`photoring.model.PhotoRingModel`
- Step 2 (inference) ..... :mod:`photoring.inference`
- Step 3 (figures) ....... :mod:`photoring.plotting`

The two forward models live in sibling packages, imported by :mod:`photoring.model`:
``exorings`` (closed-form, default) and ``geotrans`` (numerically integrated).
"""

from __future__ import annotations

from .config import CasePaths, FIGURE_TYPES, FORWARD_MODELS
from .observables import (
    derive_observables,
    load_posterior,
    save_observables,
    combine_segments,
    segment_tension,
    effective_sample_size,
    weight_diagnostics,
    SEGMENT_NATIVE_KEYS,
)
from .rho_cdf import make_rho_cdf, build_from_samples_file, load_rho_cdf
from .likelihood import OBS_MAP, build_kde, VALID_OBSERVABLES, validate_observables
from .priors import build_param_space, PARAM_LABEL_MAP
from .model import PhotoRingModel
from .io import (
    load_observables,
    load_case_data,
    save_run,
    load_run,
    discover_runs,
    make_run,
    dynesty_arrays,
)
from . import literature
from .inference import run_dynesty, run_emcee, compute_ppc, posterior_stats, init_walkers

__all__ = [
    "CasePaths", "FIGURE_TYPES", "FORWARD_MODELS",
    "derive_observables", "load_posterior", "save_observables",
    "combine_segments", "segment_tension", "effective_sample_size",
    "weight_diagnostics", "SEGMENT_NATIVE_KEYS",
    "literature",
    "make_rho_cdf", "build_from_samples_file", "load_rho_cdf",
    "OBS_MAP", "build_kde", "VALID_OBSERVABLES", "validate_observables",
    "build_param_space", "PARAM_LABEL_MAP",
    "PhotoRingModel",
    "load_observables", "load_case_data", "save_run", "load_run", "discover_runs", "make_run",
    "run_dynesty", "run_emcee", "compute_ppc", "posterior_stats", "init_walkers",
]
