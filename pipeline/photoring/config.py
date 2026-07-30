"""Case-directory layout and path resolution for the Photo-Ring pipeline.

The pipeline is *case-oriented*: every concrete target (Kepler-51, or your own planet)
lives in a self-contained subdirectory ``pipeline/<CASE>/`` with a fixed internal layout.
The notebooks select a case with a single variable, ``CASE = "kepler_51"``, and this
module turns that string into every input/output path they need — so the analysis code
never hard-codes a path.

Layout of a case directory::

    pipeline/<CASE>/
      inputs/
        ttv/<planet>/...post_equal_weights.dat   # raw MultiNest TTV posteriors  (entry A)
        observables/<CASE>_<planet>_observables.dat  # derived observables         (entry B)
        rho_true_data/
          rho_true_samples.dat                    # rho_star,true samples [kg/m^3]
          rho_grid_cdf.txt                         # its inverse-CDF grid (regenerable)
      results/
        exorings/   geotrans/                      # <sampler>.npz + _meta.json, by forward model
      figures/
        ppc/ corner/ marginal/ ring/ trace/ ...    # publication figures, by figure type
      README.md  science_background.md

To run the pipeline on a **new** target, copy ``kepler_51/`` to ``pipeline/<your_case>/``,
drop your data in ``inputs/`` following the same layout, and set ``CASE = "<your_case>"``
at the top of each notebook.
"""

from __future__ import annotations

from pathlib import Path

# Canonical figure-type subdirectories (figures/<type>/).
FIGURE_TYPES = (
    "kde_ppc",       # KDE self-consistency check
    "ppc",           # posterior predictive check
    "corner",        # joint posteriors
    "marginal",      # 1-D marginal posteriors
    "ring",          # projected ring-geometry diagram
    "trace",         # sampler trace / run diagnostics
    "diagnostics",   # convergence diagnostics (emcee)
    "observables",   # transit-observable posteriors and density anomaly (step 1)
    "panel",         # consolidated results panel
)

# Forward-model subdirectories (results/<model>/).
FORWARD_MODELS = ("exorings", "geotrans")


class CasePaths:
    """Resolve all input/output paths for a single analysis case.

    Parameters
    ----------
    case : str
        Case name, e.g. ``"kepler_51"``. Maps to ``<pipeline_dir>/<case>/``.
    pipeline_dir : str or Path, optional
        Directory that holds the case subdirectories (and the notebooks). Defaults to
        the current working directory, which is where Jupyter / papermill / nbconvert
        execute the pipeline notebooks from.
    """

    def __init__(self, case: str, pipeline_dir=None):
        self.case = str(case)
        self.pipeline_dir = Path(pipeline_dir) if pipeline_dir is not None else Path.cwd()
        self.root = self.pipeline_dir / self.case

    # ── Inputs ────────────────────────────────────────────────────────────
    @property
    def inputs(self) -> Path:
        return self.root / "inputs"

    @property
    def ttv_dir(self) -> Path:
        return self.inputs / "ttv"

    @property
    def observables_dir(self) -> Path:
        return self.inputs / "observables"

    @property
    def rho_true_dir(self) -> Path:
        return self.inputs / "rho_true_data"

    def observables_file(self, planet: str) -> Path:
        """Derived-observables table for a planet (output of notebook 01)."""
        return self.observables_dir / f"{self.case}_{planet}_observables.dat"

    @property
    def rho_true_samples(self) -> Path:
        """Samples of the star's true density [kg/m^3]."""
        return self.rho_true_dir / "rho_true_samples.dat"

    @property
    def rho_cdf_file(self) -> Path:
        """Pre-computed inverse-CDF grid of the rho_true prior (see photoring.rho_cdf)."""
        return self.rho_true_dir / "rho_grid_cdf.txt"

    # ── Outputs ───────────────────────────────────────────────────────────
    def results_dir(self, forward_model: str = "exorings") -> Path:
        """Directory for posterior chains/metadata of a given forward model."""
        return self.root / "results" / str(forward_model).lower()

    def figures_dir(self, figure_type: str = "") -> Path:
        """Directory for figures of a given type (see FIGURE_TYPES)."""
        base = self.root / "figures"
        return base / figure_type if figure_type else base

    @property
    def tests_outputs(self) -> Path:
        """papermill-executed notebooks from run_sweep."""
        return self.root / "tests_outputs"

    @property
    def tests_logs(self) -> Path:
        """Per-run logs from run_sweep."""
        return self.root / "tests_logs"

    # ── Convenience ───────────────────────────────────────────────────────
    def ensure_outputs(self, forward_model: str = "exorings"):
        """Create the results/figures output directories for a run."""
        self.results_dir(forward_model).mkdir(parents=True, exist_ok=True)
        for ftype in FIGURE_TYPES:
            self.figures_dir(ftype).mkdir(parents=True, exist_ok=True)
        return self

    def __repr__(self):
        return f"CasePaths(case={self.case!r}, root={self.root})"
