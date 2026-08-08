#!/usr/bin/env python3
"""run_inference.py — Photo-Ring pipeline · pure-Python sweep (no notebooks, no papermill).

Runs the nested-sampling (dynesty) inference directly for every configuration defined in a
run-config file, writing only the final products per run:

    <case>/results/<forward_model>/<run_tag>.npz
    <case>/results/<forward_model>/<run_tag>_meta.json

Usage
-----
    python bin/run_inference.py [options]

    --config FILE       Run-config Python file (default: run_config.py).
    --case CASE         Case directory (default: from config or 'kepler_51').
    --sampler dynesty   Only 'dynesty' is supported here (default: dynesty).
    --n-procs N         Worker processes for dynesty pool (default: 1).
    --nlive N           Override nested-sampling nlive (default: from NS_CONFIG_BASE).
    --dlogz Z           Override dlogz stopping criterion (default: from NS_CONFIG_BASE).
    --force             Re-run and overwrite existing results.
    --dry-run           Print what would run without running anything.
    --no-ppc            Skip the posterior predictive check (saves a bit of time).
"""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import multiprocessing as mp
import os
import sys
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

import numpy as np

# ── locate the pipeline package ───────────────────────────────────────────────
# Support running from either pipeline/ or the repo root.
_here = Path(__file__).resolve().parent          # bin/
_pipeline = _here.parent                          # pipeline/
if str(_pipeline) not in sys.path:
    sys.path.insert(0, str(_pipeline))

import photoring as pr


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DEFAULTS  (same as run_sweep_configurable.py)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NS_CONFIG_BASE = {
    "nlive": 1200, "sample": "rslice", "dlogz": 0.01, "bound": "multi",
    "seed": 2026, "use_pool": False, "n_procs": 1,
}
MODEL_CONFIG_BASE = {
    "RHO_TRUE_FIXED": None, "FI_FIXED": 1.0, "FE_MAX": 10.0,
    "ALPHA_FIXED": float(np.exp(-1.0)), "ALPHA_FREE": False,
    "ALPHA_PRIOR_LO": 0.0, "ALPHA_PRIOR_HI": 1.0,
    "p_prior_hi": 1.0,
}

N_KDE    = 5000
SEED_KDE = 123

R_STAR_RSUN  = 0.869
RSUN_REARTH  = 109.2

PLANET_PARAMS = {
    "d": dict(B_FIXED=0.0030, B_SIGMA=2 * 0.0950, p_mean_ref=0.09857, Mp=6.9),
    "b": dict(B_FIXED=0.0740, B_SIGMA=2 * 0.0720, p_mean_ref=0.07225, Mp=6.9),
}
for _pl, _pp in PLANET_PARAMS.items():
    _pmin = float(_pp["Mp"]) ** (1.0 / 3.0) / (R_STAR_RSUN * RSUN_REARTH)
    _pp["p_min"] = _pmin
    _pp["p_prior_lo"] = _pmin / float(_pp["p_mean_ref"])
del _pl, _pp, _pmin


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HELPERS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _load_config(path):
    """Load a run-config .py file and return its module."""
    spec = importlib.util.spec_from_file_location("run_cfg", path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _free_tag(rho_free, b_free, alpha_free=False, p_free=True):
    """Suffix matching PhotoRingModel.free_tag()."""
    parts = ""
    if rho_free:    parts += "_rhoFREE"
    if b_free:      parts += "_bFREE"
    if alpha_free:  parts += "_alphaFREE"
    if p_free:      parts += "_pFREE"
    return parts


def _build_run_tag(case, planet, observables, rho_free, b_free, alpha_free,
                   p_free, forward_model, ns_cfg, run_label=None):
    kt  = "-".join(observables)
    ft  = _free_tag(rho_free, b_free, alpha_free, p_free)
    tag = (f"{case}_{planet}_NS_{forward_model.lower()}_kde_{kt}"
           f"_nlive{ns_cfg['nlive']}_dlogz{ns_cfg['dlogz']}"
           f"_NKDE{N_KDE}_seed{ns_cfg['seed']}{ft}")
    if run_label:
        tag += f"_{run_label}"
    return tag


def _build_model_cfg(planet, rho_free, b_free, alpha_free, p_free,
                     forward_model, p_fixed_value=None, alpha_fixed_value=None,
                     rho_fixed_value=None):
    pp = PLANET_PARAMS[planet]
    cfg = {
        **MODEL_CONFIG_BASE,
        "B_FREE":        bool(b_free),
        "B_FIXED":       float(pp["B_FIXED"]),
        "B_SIGMA":       float(pp["B_SIGMA"]),
        "RHO_TRUE_FREE": bool(rho_free),
        "ALPHA_FREE":    bool(alpha_free),
        "P_FREE":        bool(p_free),
        "FORWARD_MODEL": str(forward_model).lower(),
        "p_mean_ref":    float(pp["p_mean_ref"]),
        "p_prior_lo":    float(pp["p_prior_lo"]),
    }
    if p_fixed_value is not None:
        cfg["P_FIXED_VALUE"] = float(p_fixed_value)
    if alpha_fixed_value is not None:
        cfg["ALPHA_FIXED"] = float(alpha_fixed_value)
    if rho_fixed_value is not None:
        cfg["RHO_TRUE_FIXED"] = float(rho_fixed_value)
    return cfg


def _fmt(seconds):
    h, r = divmod(int(seconds), 3600)
    m, s = divmod(r, 60)
    return f"{h:02d}h{m:02d}m{s:02d}s"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SINGLE-RUN EXECUTOR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def run_one(case, planet, model_cfg, kde_cfg, ns_cfg,
            run_tag, forward_model, run_suffix="", skip_ppc=False, force=False, verbose=True):
    """Execute a single nested-sampling run and save .npz + _meta.json.

    Returns
    -------
    dict
        ``{status, run_tag, duration, npz, json}``
    """
    paths = pr.CasePaths(case, pipeline_dir=Path.cwd())
    results_dir = paths.results_dir(forward_model)
    if run_suffix:
        results_dir = results_dir / run_suffix
        results_dir.mkdir(parents=True, exist_ok=True)
    npz_path  = results_dir / f"{run_tag}.npz"
    json_path = results_dir / f"{run_tag}_meta.json"

    if not force and npz_path.exists():
        if verbose:
            print(f"  [SKIP] {run_tag}")
        return {"status": "skipped", "run_tag": run_tag, "duration": 0,
                "npz": str(npz_path), "json": str(json_path)}

    paths.ensure_outputs(forward_model)

    # ── load data ────────────────────────────────────────────────────────────
    data = pr.load_case_data(paths, planet)

    # ── build model ──────────────────────────────────────────────────────────
    model = pr.PhotoRingModel(
        data["ttv"], data["rho_true_gcc_samples"], model_cfg, kde_cfg,
        rho_grid=data["rho_grid"], rho_cdf=data["rho_cdf"],
        p_fixed=data["P_fixed"],
    )

    if verbose:
        print(f"  NDIM={model.NDIM}  params={model.PARAM_NAMES}")

    # ── nested sampling ──────────────────────────────────────────────────────
    ctx = None
    if ns_cfg.get("use_pool") and ns_cfg.get("n_procs", 1) > 1:
        try:
            ctx = mp.get_context("fork")
        except ValueError:
            ctx = mp

    t0 = time.time()
    result = pr.run_dynesty(model, ns_cfg, ctx=ctx, verbose=verbose)
    duration = time.time() - t0

    # ── posterior predictive check ───────────────────────────────────────────
    ppc = None
    if not skip_ppc:
        ppc = pr.compute_ppc(model, result["chain"])

    # ── assemble metadata ─────────────────────────────────────────────────────
    meta = dict(
        planet=planet, case=case, run_tag=run_tag, sampler="dynesty",
        kde_observables=model.observables,
        N_KDE=int(len(model.idx_train)),
        seed_kde=int(kde_cfg["seed_kde"]),
        nlive=int(ns_cfg["nlive"]),
        sample=ns_cfg["sample"],
        dlogz=float(ns_cfg["dlogz"]),
        seed_ns=int(ns_cfg["seed"]),
        FORWARD_MODEL=forward_model,
        B_FREE=bool(model.B_FREE),
        B_FIXED=float(model.B_FIXED),
        B_SIGMA=float(model.B_SIGMA),
        RHO_TRUE_FREE=bool(model.RHO_TRUE_FREE),
        RHO_TRUE_FIXED=float(model.RHO_TRUE_FIXED),
        ALPHA_FREE=bool(model.ALPHA_FREE),
        ALPHA_FIXED=float(model.ALPHA_FIXED),
        P_FREE=bool(model.P_FREE),
        FI_FIXED=float(model.FI_FIXED),
        FE_MAX=float(model.FE_MAX),
        p_min=float(model.p_min),
        p_max=float(model.p_max),
        p_mean_ref=float(model.p_mean_ref),
        P_fixed_days=float(model.P_fixed),
        logz=float(result["logz"]),
        logz_err=float(result["logz_err"]),
        n_iter=int(result["n_iter"]),
        runtime_s=float(duration),
        n_samples=int(len(result["chain"])),
        param_names=model.PARAM_NAMES,
    )
    for _n, _s in result["stats"].items():
        meta[f"stat_{_n}_median"] = float(_s["median"])
        meta[f"stat_{_n}_p16"]    = float(_s["p16"])
        meta[f"stat_{_n}_p84"]    = float(_s["p84"])

    # ── save ─────────────────────────────────────────────────────────────────
    dres = result["dres"]
    arrays = dict(chain=result["chain"])
    if ppc is not None and len(ppc):
        arrays["ppc"] = ppc
    arrays.update(pr.dynesty_arrays(dres))

    pr.save_run(results_dir, run_tag, arrays, meta, overwrite=force)

    return {"status": "ok", "run_tag": run_tag, "duration": duration,
            "npz": str(npz_path), "json": str(json_path),
            "logz": float(result["logz"]), "logz_err": float(result["logz_err"])}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# RUN LIST BUILDER  (mirrors run_sweep_configurable.py logic)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def build_run_list(cfg_mod, ns_cfg, run_suffix=""):
    """Return a list of run-spec dicts from a loaded config module."""
    planets           = getattr(cfg_mod, "PLANETS",             ["b", "d"])
    kde_variants      = getattr(cfg_mod, "KDE_VARIANTS",        [])
    free_variants     = getattr(cfg_mod, "FREE_PARAM_VARIANTS", [])
    alpha_free_vars   = getattr(cfg_mod, "ALPHA_FREE_VARIANTS", [False])
    p_free_vars       = getattr(cfg_mod, "P_FREE_VARIANTS",     [True])
    fm_variants       = getattr(cfg_mod, "FORWARD_MODEL_VARIANTS", ["exorings"])
    p_fixed_runs      = getattr(cfg_mod, "P_FIXED_RUNS",        [])
    alpha_fixed_runs  = getattr(cfg_mod, "ALPHA_FIXED_RUNS",    [])
    rho_fixed_runs    = getattr(cfg_mod, "RHO_FIXED_RUNS",      [])

    runs = []
    combos = itertools.product(planets, kde_variants, free_variants,
                               alpha_free_vars, p_free_vars, fm_variants)

    for planet, obs, free, alpha_free, p_free, fm in combos:
        rho_free = free["RHO_TRUE_FREE"]
        b_free   = free["B_FREE"]

        # --- rho permutations ---
        rho_perms = [{"label": "", "rho_val": None}]
        if not rho_free and rho_fixed_runs:
            rho_perms = [{"label": r.get("label", ""), "rho_val": r.get("value")}
                         for r in rho_fixed_runs]

        # --- p permutations ---
        p_perms = [{"label": "", "p_val": None}]
        if not p_free and p_fixed_runs:
            p_perms = []
            pp = PLANET_PARAMS[planet]
            for pr_run in p_fixed_runs:
                frac  = pr_run.get("fraction", 0.0)
                p_val = pp["p_min"] + frac * (pp["p_mean_ref"] - pp["p_min"])
                p_perms.append({"label": pr_run.get("label", ""), "p_val": p_val})

        # --- alpha permutations ---
        alpha_perms = [{"label": "", "alpha_val": None}]
        if not alpha_free and alpha_fixed_runs:
            alpha_perms = [{"label": r.get("label", ""), "alpha_val": r.get("value")}
                           for r in alpha_fixed_runs]

        for r_perm in rho_perms:
            for p_perm in p_perms:
                for a_perm in alpha_perms:
                    labels = [l for l in [r_perm["label"], p_perm["label"], a_perm["label"]] if l]
                    run_label = "_".join(labels) if labels else None

                    model_cfg = _build_model_cfg(
                        planet, rho_free, b_free, alpha_free, p_free, fm,
                        p_fixed_value=p_perm["p_val"],
                        alpha_fixed_value=a_perm["alpha_val"],
                        rho_fixed_value=r_perm["rho_val"],
                    )
                    kde_cfg = {
                        "observables": list(obs),
                        "N_KDE":       N_KDE,
                        "seed_kde":    SEED_KDE,
                    }
                    tag = _build_run_tag(
                        getattr(cfg_mod, "DEFAULT_CASE", "kepler_51"),
                        planet, obs, rho_free, b_free, alpha_free, p_free, fm,
                        ns_cfg, run_label,
                    )
                    runs.append(dict(
                        case=getattr(cfg_mod, "DEFAULT_CASE", "kepler_51"),
                        planet=planet,
                        model_cfg=model_cfg,
                        kde_cfg=kde_cfg,
                        forward_model=fm,
                        run_tag=tag,
                        run_suffix=run_suffix,
                    ))
    return runs


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# WORKER  (top-level so ProcessPoolExecutor can pickle it)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _worker(payload):
    """Entry point for a subprocess in the ProcessPoolExecutor."""
    try:
        return run_one(**payload)
    except Exception as exc:
        return {"status": "FAILED", "run_tag": payload.get("run_tag", "?"),
                "duration": 0, "error": str(exc), "tb": traceback.format_exc()}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MAIN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    cpu = os.cpu_count() or 4
    ap = argparse.ArgumentParser(
        description="Photo-Ring pipeline — pure-Python dynesty sweep (no notebooks)")
    ap.add_argument("--config",   default="run_config.py",
                    help="Run-config .py file (default: run_config.py)")
    ap.add_argument("--case",     default=None,
                    help="Override the case directory from the config")
    ap.add_argument("--jobs",     type=int, default=1,
                    help="Concurrent independent runs (default: 1). "
                         "--n-procs is split across jobs to avoid oversubscription.")
    ap.add_argument("--n-procs",  type=int, default=min(6, max(1, cpu // 2)),
                    help=f"Total worker processes for dynesty pools (default: min(6, cpu/2)={min(6, max(1, cpu//2))}). "
                         "Split evenly across --jobs.")
    ap.add_argument("--nlive",    type=int, default=None,
                    help="Override nlive (default: from NS_CONFIG_BASE)")
    ap.add_argument("--dlogz",    type=float, default=None,
                    help="Override dlogz (default: from NS_CONFIG_BASE)")
    ap.add_argument("--seed",     type=int, default=None,
                    help="Override RNG seed (default: from NS_CONFIG_BASE)")
    ap.add_argument("--force",    action="store_true",
                    help="Re-run and overwrite existing results")
    ap.add_argument("--dry-run",  action="store_true",
                    help="Print what would run without running anything")
    ap.add_argument("--no-ppc",   action="store_true",
                    help="Skip the posterior predictive check")
    args = ap.parse_args()

    # ── load config ───────────────────────────────────────────────────────────
    cfg_path = Path(args.config)
    if not cfg_path.exists():
        print(f"Error: config file '{cfg_path}' not found.", file=sys.stderr)
        sys.exit(1)
    cfg_mod = _load_config(cfg_path)
    
    cfg_name = cfg_path.name
    if cfg_name.startswith("run_config-") and cfg_name.endswith(".py"):
        run_suffix = cfg_name[len("run_config-"):-len(".py")]
    else:
        run_suffix = ""

    # ── split n_procs across concurrent jobs ──────────────────────────────────
    n_procs_each = max(1, args.n_procs // args.jobs) if args.jobs > 1 else args.n_procs

    # ── NS config (base + overrides) ──────────────────────────────────────────
    ns_cfg = dict(NS_CONFIG_BASE)
    ns_cfg["use_pool"] = n_procs_each > 1
    ns_cfg["n_procs"]  = n_procs_each
    if args.nlive is not None:  ns_cfg["nlive"] = args.nlive
    if args.dlogz is not None:  ns_cfg["dlogz"] = args.dlogz
    if args.seed  is not None:  ns_cfg["seed"]  = args.seed

    # ── build run list ────────────────────────────────────────────────────────
    runs  = build_run_list(cfg_mod, ns_cfg, run_suffix=run_suffix)
    total = len(runs)

    default_case = getattr(cfg_mod, "DEFAULT_CASE", "kepler_51")
    case = args.case or default_case

    print(f"\n{'=' * 64}")
    print(f"  Photo-Ring inference — case '{case}' — {total} runs  |  {datetime.now():%Y-%m-%d %H:%M}")
    print(f"  jobs={args.jobs}  n_procs/run={n_procs_each}  (--n-procs {args.n_procs})")
    print(f"  nlive={ns_cfg['nlive']}  dlogz={ns_cfg['dlogz']}")
    print(f"  Python: {sys.executable}")
    out_dir = Path(case).resolve() / 'results'
    if run_suffix:
        out_dir = out_dir / "<forward_model>" / run_suffix
    print(f"  Results -> {out_dir}")
    print(f"{'=' * 64}\n")

    # ── build per-run payloads ────────────────────────────────────────────────
    payloads = [
        dict(
            case          = run["case"],
            planet        = run["planet"],
            model_cfg     = run["model_cfg"],
            kde_cfg       = run["kde_cfg"],
            ns_cfg        = ns_cfg,
            run_tag       = run["run_tag"],
            forward_model = run["forward_model"],
            run_suffix    = run.get("run_suffix", ""),
            skip_ppc      = args.no_ppc,
            force         = args.force,
            verbose       = (args.jobs == 1),   # suppress per-iteration prints when parallel
        )
        for run in runs
    ]

    results_log = []
    t_start = time.time()

    def _announce(i, tag, res):
        st = res["status"]
        prefix = f"[{i:>3}/{total}]  {tag}"
        if st == "ok":
            lz = res.get("logz", float("nan"))
            print(f"{prefix}\n  [OK]   {_fmt(res['duration'])}  logZ={lz:+.2f}  -> {res.get('npz','')}", flush=True)
        elif st == "skipped":
            print(f"{prefix}\n  [SKIP] already exists", flush=True)
        elif st == "dry":
            print(f"{prefix}\n  [DRY]", flush=True)
        else:
            tb = res.get("tb", "")
            if tb:
                print(tb, flush=True)
            print(f"{prefix}\n  [FAIL] {res.get('error', '')}", flush=True)
        print()

    # ── sequential (jobs=1) or parallel (jobs>1) ──────────────────────────────
    if args.jobs == 1 or args.dry_run:
        for i, (payload, run) in enumerate(zip(payloads, runs), 1):
            tag = run["run_tag"]
            if args.dry_run:
                _announce(i, tag, {"status": "dry", "run_tag": tag})
                results_log.append({"status": "dry", "run_tag": tag})
                continue
            res = _worker(payload)
            results_log.append(res)
            _announce(i, tag, res)
    else:
        try:
            ctx = mp.get_context("fork")
        except ValueError:
            ctx = mp.get_context()
        print(f"Dispatching {total} runs with ProcessPoolExecutor(jobs={args.jobs})...\n",
              flush=True)
        with ProcessPoolExecutor(max_workers=args.jobs, mp_context=ctx) as ex:
            futs = {ex.submit(_worker, pl): (i, run["run_tag"])
                    for i, (pl, run) in enumerate(zip(payloads, runs), 1)}
            done = 0
            for fut in as_completed(futs):
                done += 1
                i, tag = futs[fut]
                try:
                    res = fut.result()
                except Exception as exc:
                    res = {"status": "FAILED", "run_tag": tag, "duration": 0,
                           "error": str(exc)}
                results_log.append(res)
                _announce(i, tag, res)

    ok      = sum(1 for r in results_log if r["status"] == "ok")
    skipped = sum(1 for r in results_log if r["status"] == "skipped")
    failed  = sum(1 for r in results_log if r["status"] == "FAILED")
    dry     = sum(1 for r in results_log if r["status"] == "dry")

    print(f"{'=' * 64}")
    print(f"  Done in {_fmt(time.time() - t_start)}")
    print(f"  OK={ok}  SKIP={skipped}  FAIL={failed}  DRY={dry}")
    print(f"{'=' * 64}\n")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    mp.freeze_support()   # needed on macOS/Windows with spawn context
    main()
