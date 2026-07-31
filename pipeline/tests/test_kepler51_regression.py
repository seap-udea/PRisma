"""Regression: one Kepler-51 dynesty config still matches a saved baseline.

Re-runs planet **b**, ``L = (δ, ρ★,obs)``, only ``p`` free (other nuisances
fixed), and compares lnZ / posterior percentiles to the snapshot in
``tests/baselines/kepler51_b_delta-rho_obs_pFREE/`` (copied from
``pipeline/kepler_51/results/exorings/`` before the package refactor).

Nested sampling is stochastic (especially with a worker pool), so we check
*similarity*, not bit-identity. Run with ``n_procs=1`` for stability.

Usage
-----
From ``pipeline/``, with the repo virtualenv (needs ``dynesty``)::

    ../.venv/bin/python tests/test_kepler51_regression.py
    ../.venv/bin/python -m pytest tests/test_kepler51_regression.py -m slow
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import pytest

_PIPELINE = Path(__file__).resolve().parents[1]
_REPO = _PIPELINE.parent
_VENV_PYTHON = _REPO / ".venv" / "bin" / "python"
if str(_PIPELINE) not in sys.path:
    sys.path.insert(0, str(_PIPELINE))

try:
    import dynesty  # noqa: F401
except ModuleNotFoundError:
    hint = (
        f"  {_VENV_PYTHON} tests/test_kepler51_regression.py"
        if _VENV_PYTHON.is_file()
        else "  python -m pip install -r requirements.txt   # then retry"
    )
    sys.stderr.write(
        "ModuleNotFoundError: dynesty is not installed in this Python.\n"
        f"  interpreter: {sys.executable}\n"
        "Use the repo .venv (or install requirements.txt):\n"
        f"{hint}\n"
    )
    raise SystemExit(2) from None

import photoring as pr
import run_sweep as sweep
from photoring.inference import posterior_stats

BASELINE_DIR = Path(__file__).resolve().parent / "baselines" / "kepler51_b_delta-rho_obs_pFREE"
REFERENCE_SUMMARY = BASELINE_DIR / "reference_summary.json"

# Config pinned to the golden run tag.
PLANET = "b"
OBSERVABLES = ["delta", "rho_obs"]
RHO_FREE = False
B_FREE = False
TAU_FREE = False
P_FREE = True
FORWARD_MODEL = "exorings"

# Tolerances: nested sampling is stochastic (baseline used n_procs=6; we use 1).
# Compare |Δmedian| to the reference 16–84% width, not absolute scales.
LOGZ_ATOL = 0.5
# Max allowed |fresh_median − ref_median| / (ref_p84 − ref_p16).
MEDIAN_FRAC_OF_CI = 0.6
# Same idea for the percentile edges (looser — tails move more).
PERCENTILE_FRAC_OF_CI = 0.75
# Floor so a tiny CI does not explode the relative check.
CI_WIDTH_FLOOR = {
    "fe": 0.5,
    "ir": 5.0,
    "theta": 5.0,
    "p": 0.005,
}


def _build_params():
    return sweep.build_params(
        "dynesty", sweep.DEFAULT_CASE, PLANET, OBSERVABLES,
        RHO_FREE, B_FREE, TAU_FREE, {},
        p_free=P_FREE, forward_model=FORWARD_MODEL,
    )


def _expected_run_tag(params):
    return sweep.build_run_tag(
        "dynesty", sweep.DEFAULT_CASE, PLANET, OBSERVABLES,
        RHO_FREE, B_FREE, TAU_FREE, params,
        p_free=P_FREE, forward_model=FORWARD_MODEL,
    )


def run_config(verbose: bool = True):
    """Execute the baseline NS config; return (meta-like dict, chain, stats)."""
    params = _build_params()
    run_tag = _expected_run_tag(params)
    kde_config = dict(params["KDE_CONFIG"])
    model_config = dict(params["MODEL_CONFIG"])
    ns_config = dict(params["NS_CONFIG"])
    # Single process → closer to reproducible; baseline used n_procs=6.
    ns_config["use_pool"] = False
    ns_config["n_procs"] = 1

    paths = pr.CasePaths(sweep.DEFAULT_CASE, pipeline_dir=_PIPELINE)
    data = pr.load_case_data(paths, PLANET)
    model = pr.PhotoRingModel(
        data["ttv"], data["rho_true_gcc_samples"], model_config, kde_config,
        rho_grid=data["rho_grid"], rho_cdf=data["rho_cdf"],
        p_fixed=data["P_fixed"],
    )
    if verbose:
        print(f"run_tag={run_tag}")
        print(f"  NDIM={model.NDIM}  params={model.PARAM_NAMES}  L={model.observables}")

    t0 = time.time()
    result = pr.run_dynesty(model, ns_config, ctx=None, verbose=verbose)
    stats = posterior_stats(result["chain"], model.PARAM_NAMES)
    elapsed = time.time() - t0
    if verbose:
        print(f"  lnZ={result['logz']:.3f}±{result['logz_err']:.3f}  "
              f"runtime={elapsed:.1f}s  N={len(result['chain'])}")
    out = {
        "run_tag": run_tag,
        "logz": float(result["logz"]),
        "logz_err": float(result["logz_err"]),
        "param_names": list(model.PARAM_NAMES),
        "stats": stats,
        "runtime_s": float(elapsed),
        "n_samples": int(len(result["chain"])),
    }
    return out, result["chain"]


def load_reference():
    ref = json.loads(REFERENCE_SUMMARY.read_text())
    return ref


def _ci_width(ref_stats: dict, name: str) -> float:
    w = float(ref_stats[name]["p84"]) - float(ref_stats[name]["p16"])
    return max(abs(w), CI_WIDTH_FLOOR[name])


def compare_to_reference(fresh: dict, ref: dict, verbose: bool = True):
    """Return a list of failure messages (empty ⇒ pass)."""
    failures = []

    if fresh["run_tag"] != ref["run_tag"]:
        failures.append(
            f"run_tag mismatch: got {fresh['run_tag']!r}, expected {ref['run_tag']!r}"
        )

    dlogz = abs(fresh["logz"] - ref["logz"])
    if verbose:
        print(f"  lnZ  fresh={fresh['logz']:.4f}  ref={ref['logz']:.4f}  "
              f"|Δ|={dlogz:.4f}  (atol={LOGZ_ATOL})")
    if dlogz > LOGZ_ATOL:
        failures.append(
            f"logz |Δ|={dlogz:.4f} > {LOGZ_ATOL} "
            f"(fresh={fresh['logz']:.4f}, ref={ref['logz']:.4f})"
        )

    for name in ref["param_names"]:
        if name not in fresh["stats"]:
            failures.append(f"missing parameter in fresh run: {name}")
            continue
        width = _ci_width(ref["stats"], name)
        checks = (
            ("median", MEDIAN_FRAC_OF_CI),
            ("p16", PERCENTILE_FRAC_OF_CI),
            ("p84", PERCENTILE_FRAC_OF_CI),
        )
        for key, frac_lim in checks:
            a = float(fresh["stats"][name][key])
            b = float(ref["stats"][name][key])
            delta = abs(a - b)
            frac = delta / width
            if verbose:
                print(f"  {name}.{key}: fresh={a:.6g}  ref={b:.6g}  "
                      f"|Δ|/CI={frac:.3f}  (lim={frac_lim}, CI={width:.4g})")
            if frac > frac_lim:
                failures.append(
                    f"{name}.{key} |Δ|/CI={frac:.3f} > {frac_lim} "
                    f"(fresh={a:.6g}, ref={b:.6g}, CI={width:.4g})"
                )
    return failures


@pytest.mark.slow
def test_kepler51_b_delta_rho_obs_pFREE_matches_baseline():
    assert REFERENCE_SUMMARY.is_file(), f"missing baseline: {REFERENCE_SUMMARY}"
    ref = load_reference()
    fresh, _ = run_config(verbose=True)
    failures = compare_to_reference(fresh, ref, verbose=True)
    assert not failures, "regression failures:\n  - " + "\n  - ".join(failures)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    if not REFERENCE_SUMMARY.is_file():
        print(f"ERROR: missing baseline {REFERENCE_SUMMARY}", file=sys.stderr)
        return 2

    ref = load_reference()
    print(f"Baseline: {REFERENCE_SUMMARY}")
    print(f"  ref lnZ={ref['logz']:.4f}  tag={ref['run_tag']}")

    fresh, _ = run_config(verbose=not args.quiet)
    failures = compare_to_reference(fresh, ref, verbose=not args.quiet)
    if failures:
        print("FAIL")
        for msg in failures:
            print(f"  - {msg}")
        return 1
    print("OK — fresh run matches baseline within tolerance.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
