#!/usr/bin/env python3
"""run_sweep_parallel.py — Photo-Ring dynesty sweep **without papermill**.

Calls ``photoring`` directly so a ``multiprocessing`` fork pool works (the
papermill/ipykernel path deadlocks under ``use_pool=True`` on macOS).

Same 32-run grid as ``run_sweep.py`` (2 planets × 4 KDE × τ × p; ρ★,true and b fixed).
Results land only under ``pipeline/<case>/results/`` — never under ``PaperFigures/``.

Usage
-----
    # preview
    python run_sweep_parallel.py --dry-run

    # one config at a time, 6 workers inside dynesty  (~12 min/run × 32)
    python run_sweep_parallel.py --n-procs 6

    # two configs at once; each gets half the workers
    python run_sweep_parallel.py --jobs 2 --n-procs 6

Recommended from the repo venv::

    cd pipeline
    nohup ../.venv/bin/python run_sweep_parallel.py --n-procs 6 \\
        > sweep_parallel.log 2>&1 &
"""

from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import os
import sys
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

# ── path bootstrap (repo root + pipeline/) ──────────────────────────────────
_PIPELINE = Path(__file__).resolve().parent
_REPO = _PIPELINE.parent
for _p in (str(_REPO), str(_PIPELINE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# Reuse the combinatorial grid / tagging from the papermill sweeper.
import run_sweep as sweep  # noqa: E402

import numpy as np  # noqa: E402
import photoring as pr  # noqa: E402
from photoring.model import FLOAT_TINY  # noqa: E402

# dynesty reports this when every live point shares the same logL (typical when
# the prior never intersects the KDE support — e.g. T14 with ρ/b fixed).
_PLATEAU_LOGZ = float(np.log(FLOAT_TINY))


def _is_plateau_result(result, min_runtime_s=2.0):
    """Return True if nested sampling failed to leave the log(FLOAT_TINY) floor."""
    logz = float(result.get("logz", np.nan))
    runtime = float(result.get("runtime_s", 0.0))
    if not np.isfinite(logz):
        return True
    if abs(logz - _PLATEAU_LOGZ) < 1.0:
        return True
    if logz < -100.0 and runtime < min_runtime_s:
        return True
    dres = result.get("dres")
    if dres is not None and hasattr(dres, "logl"):
        ll = np.asarray(dres.logl, dtype=float)
        if ll.size > 0 and np.nanmax(ll) - np.nanmin(ll) < 1e-9:
            return True
    return False


def _results_dir(case, forward_model):
    """Always write under pipeline/<case>/results/… (cwd-independent)."""
    return _PIPELINE / case / "results" / forward_model.lower()


def _mp_ctx():
    try:
        return mp.get_context("fork")
    except ValueError:
        return mp.get_context()


def _build_meta(model, result, case, planet, run_tag, kde_config, ns_config):
    meta = dict(
        planet=planet, case=case, run_tag=run_tag, sampler="dynesty",
        kde_observables=list(model.observables),
        N_KDE=int(len(model.idx_train)),
        seed_kde=int(kde_config["seed_kde"]),
        nlive=int(ns_config["nlive"]), sample=ns_config["sample"],
        dlogz=float(ns_config["dlogz"]), seed_ns=int(ns_config["seed"]),
        FORWARD_MODEL=str(model.FORWARD_MODEL),
        B_FREE=bool(model.B_FREE), B_FIXED=float(model.B_FIXED),
        B_SIGMA=float(model.B_SIGMA),
        RHO_TRUE_FREE=bool(model.RHO_TRUE_FREE),
        RHO_TRUE_FIXED=float(model.RHO_TRUE_FIXED),
        RHO_TRUE_MIN=float(model.RHO_TRUE_MIN),
        RHO_TRUE_MAX=float(model.RHO_TRUE_MAX),
        TAU_FREE=bool(model.TAU_FREE), TAU_FIXED=float(model.TAU_FIXED),
        TAU_PRIOR_LO=float(model.TAU_LO), TAU_PRIOR_HI=float(model.TAU_HI),
        P_FREE=bool(model.P_FREE), P_FIXED_VALUE=float(model.P_FIXED_VALUE),
        FI_FIXED=float(model.FI_FIXED), FE_MAX=float(model.FE_MAX),
        p_min=float(model.p_min), p_max=float(model.p_max),
        p_mean_ref=float(model.p_mean_ref),
        P_fixed_days=float(model.P_fixed),
        logz=float(result["logz"]), logz_err=float(result["logz_err"]),
        n_iter=int(result["n_iter"]), runtime_s=float(result["runtime_s"]),
        n_samples=int(len(result["chain"])), param_names=list(model.PARAM_NAMES),
        use_pool=bool(ns_config.get("use_pool")),
        n_procs=int(ns_config.get("n_procs", 1)),
    )
    for name, stats in result["stats"].items():
        meta[f"stat_{name}_median"] = float(stats["median"])
        meta[f"stat_{name}_p16"] = float(stats["p16"])
        meta[f"stat_{name}_p84"] = float(stats["p84"])
    return meta


def execute_one(case: str, params: dict, n_procs: int, dry_run: bool = False,
                skip_ppc: bool = False, verbose: bool = True):
    """Run one dynesty retrieval and save ``.npz`` + ``_meta.json``.

    Designed to be called from a worker process (top-level, picklable).
    """
    planet = params["PLANET"]
    kde_config = dict(params["KDE_CONFIG"])
    model_config = dict(params["MODEL_CONFIG"])
    ns_config = dict(params["NS_CONFIG"])
    ns_config["use_pool"] = bool(n_procs > 1)
    ns_config["n_procs"] = int(max(1, n_procs))
    forward_model = str(model_config.get("FORWARD_MODEL", "exorings")).lower()

    # Tag uses the *effective* NS_CONFIG (so nlive/dlogz match the filename).
    tag_params = {"NS_CONFIG": ns_config}
    run_tag = sweep.build_run_tag(
        "dynesty", case, planet, kde_config["observables"],
        model_config["RHO_TRUE_FREE"], model_config["B_FREE"],
        model_config["TAU_FREE"], tag_params,
        p_free=model_config["P_FREE"], forward_model=forward_model,
    )

    results_dir = _results_dir(case, forward_model)
    if "PaperFigures" in results_dir.resolve().parts or "paper_figures" in results_dir.resolve().parts:
        raise RuntimeError(f"Refusing to write under PaperFigures: {results_dir}")

    log_dir = _PIPELINE / case / "tests_logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{run_tag}.log"

    if (results_dir / f"{run_tag}.npz").exists():
        return {"status": "skipped", "run_tag": run_tag, "duration": 0.0}

    if dry_run:
        return {"status": "dry", "run_tag": run_tag, "duration": 0.0,
                "n_procs": ns_config["n_procs"]}

    t0 = time.time()
    try:
        # Tee-ish logging: print + file.
        def log(msg=""):
            line = str(msg)
            print(line, flush=True)
            with open(log_path, "a") as fh:
                fh.write(line + "\n")

        log(f"[{datetime.now():%H:%M:%S}] START {run_tag}  n_procs={ns_config['n_procs']}")

        paths = pr.CasePaths(case, pipeline_dir=_PIPELINE)
        paths.ensure_outputs(forward_model)
        data = pr.load_case_data(paths, planet)
        model = pr.PhotoRingModel(
            data["ttv"], data["rho_true_gcc_samples"], model_config, kde_config,
            rho_grid=data["rho_grid"], rho_cdf=data["rho_cdf"],
            p_fixed=data["P_fixed"],
        )
        log(f"  NDIM={model.NDIM}  params={model.PARAM_NAMES}  "
            f"L_KDE={model.observables}")

        ctx = _mp_ctx()
        result = pr.run_dynesty(model, ns_config, ctx=ctx, verbose=verbose)
        log(f"  lnZ={result['logz']:.3f}±{result['logz_err']:.3f}  "
            f"runtime={result['runtime_s']:.1f}s  N={len(result['chain'])}")

        if _is_plateau_result(result):
            log("  PLATEAU: prior never left log(FLOAT_TINY) — not saving.")
            return {"status": "plateau", "run_tag": run_tag,
                    "duration": time.time() - t0, "logz": float(result["logz"]),
                    "n_procs": ns_config["n_procs"], "log": str(log_path)}

        ppc = None
        if not skip_ppc:
            ppc = pr.compute_ppc(model, result["chain"])
            log(f"  PPC draws: {len(ppc)}")

        meta = _build_meta(model, result, case, planet, run_tag, kde_config, ns_config)
        arrays = dict(chain=result["chain"], **pr.dynesty_arrays(result["dres"]))
        if ppc is not None:
            arrays["ppc"] = ppc
        saved = pr.save_run(results_dir, run_tag, arrays, meta, overwrite=False)
        if saved is None:
            return {"status": "skipped", "run_tag": run_tag,
                    "duration": time.time() - t0}
        log(f"  Saved -> {results_dir / (run_tag + '.npz')}")
        log(f"[{datetime.now():%H:%M:%S}] OK {run_tag}  "
            f"({sweep.fmt_duration(time.time() - t0)})")
        return {"status": "ok", "run_tag": run_tag, "duration": time.time() - t0,
                "logz": result["logz"], "n_procs": ns_config["n_procs"]}
    except Exception as exc:
        with open(log_path, "a") as fh:
            fh.write(traceback.format_exc())
        print(f"FAILED {run_tag}: {exc}", flush=True)
        return {"status": "FAILED", "run_tag": run_tag,
                "duration": time.time() - t0, "error": str(exc),
                "log": str(log_path)}


def _worker(payload):
    """ProcessPoolExecutor entry point."""
    return execute_one(**payload)


def main():
    cpu = os.cpu_count() or 4
    ap = argparse.ArgumentParser(
        description="Photo-Ring dynesty sweep (no papermill; fork pool OK)")
    ap.add_argument("--case", default=sweep.DEFAULT_CASE)
    ap.add_argument("--n-procs", type=int, default=min(6, max(1, cpu // 2)),
                    help="Workers inside each dynesty run (default: min(6, cpu/2))")
    ap.add_argument("--jobs", type=int, default=1,
                    help="Concurrent independent runs (default 1). "
                         "n_procs is split across jobs to avoid oversubscription.")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--skip-ppc", action="store_true",
                    help="Skip posterior-predictive draws (faster; no ppc in npz)")
    ap.add_argument("--quiet", action="store_true",
                    help="Less dynesty progress printing")
    ap.add_argument("--validate-refs", action="store_true",
                    help="Only the two manuscript reference tags "
                         "(All flexible, L=δ,T14,ρ for planets b and d)")
    args = ap.parse_args()

    if args.n_procs < 1 or args.jobs < 1:
        ap.error("--n-procs and --jobs must be >= 1")

    # Split workers across concurrent jobs.
    n_procs_each = max(1, args.n_procs // args.jobs) if args.jobs > 1 else args.n_procs

    # Force pool-capable NS defaults for tag construction / listing.
    sweep.NS_CONFIG_BASE = {
        **sweep.NS_CONFIG_BASE,
        "use_pool": n_procs_each > 1,
        "n_procs": n_procs_each,
    }

    runs = sweep.build_run_list("dynesty", args.case)
    if args.validate_refs:
        want = {
            f"{args.case}_{pl}_NS_exorings_kde_delta-T14-rho_obs"
            f"_nlive{sweep.NS_CONFIG_BASE['nlive']}_dlogz{sweep.NS_CONFIG_BASE['dlogz']}"
            f"_NKDE{sweep.N_KDE}_seed{sweep.NS_CONFIG_BASE['seed']}"
            f"_rhoFREE_bFREE_tauFREE_pFREE"
            for pl in ("b", "d")
        }
        runs = [r for r in runs if r["run_tag"] in want]
        if len(runs) != 2:
            print(f"WARNING: --validate-refs expected 2 runs, got {len(runs)}: "
                  f"{[r['run_tag'] for r in runs]}")

    total = len(runs)
    results_root = _PIPELINE / args.case / "results"

    print(f"\n{'=' * 64}")
    print(f"  Photo-Ring PARALLEL sweep — case '{args.case}' — {total} runs")
    print(f"  {datetime.now():%Y-%m-%d %H:%M:%S}")
    print(f"  Python: {sys.executable}")
    print(f"  jobs={args.jobs}  n_procs/run={n_procs_each}  "
          f"(requested --n-procs {args.n_procs})")
    print(f"  Results -> {results_root.resolve()}")
    print(f"{'=' * 64}\n")

    payloads = []
    for run in runs:
        payloads.append(dict(
            case=args.case,
            params=run["params"],
            n_procs=n_procs_each,
            dry_run=args.dry_run,
            skip_ppc=args.skip_ppc,
            verbose=not args.quiet,
        ))

    results_log = []
    t_start = time.time()

    def _announce(res):
        st = res["status"]
        if st == "ok":
            print(f"  [OK]   {sweep.fmt_duration(res['duration'])}  "
                  f"lnZ={res.get('logz', float('nan')):.3f}")
        elif st == "skipped":
            print("  [SKIP]")
        elif st == "dry":
            print(f"  [DRY]  n_procs={res.get('n_procs')}")
        elif st == "plateau":
            print(f"  [PLATEAU] lnZ={res.get('logz', float('nan')):.3f}  "
                  f"(not saved) -> {res.get('log', '')}")
        else:
            print(f"  [FAIL] {res.get('error', '')}  -> {res.get('log', '')}")

    if args.jobs == 1 or args.dry_run:
        for i, payload in enumerate(payloads, 1):
            p = payload["params"]
            tag = sweep.build_run_tag(
                "dynesty", args.case, p["PLANET"], p["KDE_CONFIG"]["observables"],
                p["MODEL_CONFIG"]["RHO_TRUE_FREE"], p["MODEL_CONFIG"]["B_FREE"],
                p["MODEL_CONFIG"]["TAU_FREE"],
                {"NS_CONFIG": {**p["NS_CONFIG"], "n_procs": n_procs_each,
                               "use_pool": n_procs_each > 1}},
                p_free=p["MODEL_CONFIG"]["P_FREE"],
                forward_model=p["MODEL_CONFIG"]["FORWARD_MODEL"],
            )
            print(f"[{i:>3}/{total}] {tag}")
            res = execute_one(**payload)
            results_log.append(res)
            _announce(res)
            print()
    else:
        print(f"Dispatching {total} runs with ProcessPoolExecutor(jobs={args.jobs})…\n")
        with ProcessPoolExecutor(max_workers=args.jobs, mp_context=_mp_ctx()) as ex:
            futs = {ex.submit(_worker, pl): i for i, pl in enumerate(payloads, 1)}
            done = 0
            for fut in as_completed(futs):
                done += 1
                idx = futs[fut]
                try:
                    res = fut.result()
                except Exception as exc:
                    res = {"status": "FAILED", "run_tag": f"job#{idx}",
                           "duration": 0.0, "error": str(exc)}
                results_log.append(res)
                print(f"[{done:>3}/{total}] {res.get('run_tag', '?')}  "
                      f"{res['status']}  {sweep.fmt_duration(res.get('duration', 0))}",
                      flush=True)

    ok = sum(1 for r in results_log if r["status"] == "ok")
    skipped = sum(1 for r in results_log if r["status"] == "skipped")
    failed = sum(1 for r in results_log if r["status"] == "FAILED")
    dry = sum(1 for r in results_log if r["status"] == "dry")
    plateau = sum(1 for r in results_log if r["status"] == "plateau")
    print(f"\n{'=' * 64}")
    print(f"  Sweep done in {sweep.fmt_duration(time.time() - t_start)}")
    print(f"  OK={ok}  SKIP={skipped}  FAIL={failed}  PLATEAU={plateau}  DRY={dry}")
    print(f"{'=' * 64}\n")

    if not args.dry_run:
        log_dir = _PIPELINE / args.case / "tests_logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        sweep_log = log_dir / f"sweep_parallel_{datetime.now():%Y%m%d_%H%M%S}.json"
        sweep_log.write_text(json.dumps(results_log, indent=2))
        print(f"  Sweep log -> {sweep_log}\n")

    # Plateau is an expected outcome for some fixed-nuisance + T14 configs, not a crash.
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    # Required on macOS when the outer ProcessPoolExecutor uses spawn; harmless with fork.
    mp.freeze_support()
    main()
