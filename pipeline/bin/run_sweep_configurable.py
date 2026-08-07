#!/usr/bin/env python3
"""run_sweep.py — Photo-Ring pipeline · multi-configuration sweep.

Runs ``02_inference_emcee.ipynb`` and/or ``02_inference_dynesty.ipynb`` over many
configurations (subsets of KDE observables x free-parameter toggles x forward model),
injecting each configuration with ``papermill`` and collecting the outputs.

Usage
-----
    python run_sweep.py [--sampler emcee|dynesty|both] [--case CASE]
                        [--notebook-emcee PATH] [--notebook-dynesty PATH] [--dry-run]

Dependencies: ``pip install papermill`` (see the repo ``.venv``).

How injection works
-------------------
``papermill`` requires injected parameters to be plain scalars / lists / dicts of scalars —
never expressions referencing other notebook variables (e.g. ``PLANET_PARAMS[PLANET]`` inside
``MODEL_CONFIG`` would fail). So this script resolves every concrete value here (using
``PLANET_PARAMS[planet]``) and passes fully-expanded dicts. The notebook's ``parameters``-tagged
cell must contain only literals; the model is built in a *separate*, untagged cell that runs
after injection.

Outputs land only under the case directory (never under ``papers/``):

- executed notebooks → ``<case>/tests_outputs/``
- logs → ``<case>/tests_logs/``
- chains / metadata → ``<case>/results/<forward_model>/``

The manuscript figure chains in ``papers/<case>/reference_runs/`` are a separate artefact
(``rhoFREE_bFREE_tauFREE_pFREE``) and are not part of this 32-run grid; this sweep will not
overwrite them.

Default grid size (dynesty)
---------------------------
``2 planets × 3 KDE sets × 4 nuisance combos × 2 τ × 2 p = 96`` runs.
"""

import argparse
import itertools
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SWEEP CONFIGURATION  <- edit here
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

import argparse
import importlib.util

# Parse --config early to load the correct configuration
_parser = argparse.ArgumentParser(add_help=False)
_parser.add_argument("--config", default="run_config.py")
_early_args, _ = _parser.parse_known_args()

_config_path = _early_args.config
if not Path(_config_path).exists():
    print(f"Error: Config file {_config_path} not found.")
    sys.exit(1)

_spec = importlib.util.spec_from_file_location("cfg", _config_path)
cfg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cfg)

DEFAULT_CASE = getattr(cfg, "DEFAULT_CASE", "kepler_51")
KDE_VARIANTS = getattr(cfg, "KDE_VARIANTS", [])
FREE_PARAM_VARIANTS = getattr(cfg, "FREE_PARAM_VARIANTS", [])
ALPHA_FREE_VARIANTS = getattr(cfg, "ALPHA_FREE_VARIANTS", [])
P_FREE_VARIANTS = getattr(cfg, "P_FREE_VARIANTS", [])
FORWARD_MODEL_VARIANTS = getattr(cfg, "FORWARD_MODEL_VARIANTS", ["exorings"])
PLANETS = getattr(cfg, "PLANETS", ["b", "d"])
P_FIXED_RUNS = getattr(cfg, "P_FIXED_RUNS", [])
ALPHA_FIXED_RUNS = getattr(cfg, "ALPHA_FIXED_RUNS", [])

MCMC_CONFIG_BASE = {
    "nwalkers": 64, "nsteps": 10000, "burnin": 2000, "thin": 50,
    "seed": 2026, "use_pool": False, "n_procs": 1,
}
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

N_KDE = 5000
SEED_KDE = 123

R_STAR_RSUN = 0.869
RSUN_REARTH = 109.2

def p_min_earth_density(Mp_earth, R_star_rsun=R_STAR_RSUN, Rsun_Rearth=RSUN_REARTH):
    return float(Mp_earth) ** (1.0 / 3.0) / (float(R_star_rsun) * float(Rsun_Rearth))

PLANET_PARAMS = {
    "d": dict(B_FIXED=0.0030, B_SIGMA=2 * 0.0950, p_mean_ref=0.09857, Mp=6.9),
    "b": dict(B_FIXED=0.0740, B_SIGMA=2 * 0.0720, p_mean_ref=0.07225, Mp=6.9),
}
for _pl, _pp in PLANET_PARAMS.items():
    _pmin = p_min_earth_density(_pp["Mp"])
    _pp["p_min"] = _pmin
    _pp["p_prior_lo"] = _pmin / float(_pp["p_mean_ref"])
del _pl, _pp, _pmin

OVERRIDES = {}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PATHS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DEFAULT_NB_EMCEE = Path("02_inference_emcee.ipynb")
DEFAULT_NB_DYNESTY = Path("02_inference_dynesty.ipynb")
DEFAULT_KERNEL = "python3"  # repo .venv registers itself as the ``python3`` kernel


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HELPERS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def free_tag(rho_free, b_free, alpha_free=False, p_free=True):
    """Suffix matching PhotoRingModel.free_tag() (order: rho, b, alpha, p)."""
    parts = ""
    if rho_free:
        parts += "_rhoFREE"
    if b_free:
        parts += "_bFREE"
    if alpha_free:
        parts += "_alphaFREE"
    if p_free:
        parts += "_pFREE"
    return parts


def build_run_tag(sampler, case, planet, observables, rho_free, b_free, alpha_free, cfg,
                  p_free=True, forward_model="exorings", run_label=None):
    """Reproduce the notebooks' RUN_TAG exactly."""
    kt = "-".join(observables)
    ft = free_tag(rho_free, b_free, alpha_free, p_free)
    fm = forward_model.lower()
    if sampler == "emcee":
        c = cfg["MCMC_CONFIG"]
        tag = (f"{case}_{planet}_MCMC_{fm}_kde_{kt}"
                f"_nw{c['nwalkers']}_ns{c['nsteps']}_bi{c['burnin']}_th{c['thin']}"
                f"_NKDE{N_KDE}_seed{c['seed']}{ft}")
    else:
        c = cfg["NS_CONFIG"]
        tag = (f"{case}_{planet}_NS_{fm}_kde_{kt}"
                f"_nlive{c['nlive']}_dlogz{c['dlogz']}"
                f"_NKDE{N_KDE}_seed{c['seed']}{ft}")
    
    if run_label:
        tag += f"_{run_label}"
    return tag
    c = cfg["NS_CONFIG"]
    return (f"{case}_{planet}_NS_{fm}_kde_{kt}"
            f"_nlive{c['nlive']}_dlogz{c['dlogz']}"
            f"_NKDE{N_KDE}_seed{c['seed']}{ft}")


def build_params(sampler, case, planet, observables, rho_free, b_free, alpha_free, overrides,
                 p_free=True, forward_model="exorings", p_fixed_value=None, alpha_fixed_value=None):
    """Build the fully-resolved papermill parameter dict (literals only)."""
    pp = PLANET_PARAMS[planet]
    model_cfg = {
        **MODEL_CONFIG_BASE,
        "B_FREE": bool(b_free), "B_FIXED": float(pp["B_FIXED"]), "B_SIGMA": float(pp["B_SIGMA"]),
        "RHO_TRUE_FREE": bool(rho_free), "ALPHA_FREE": bool(alpha_free),
        "P_FREE": bool(p_free), "FORWARD_MODEL": str(forward_model).lower(),
        "p_mean_ref": float(pp["p_mean_ref"]), "p_prior_lo": float(pp["p_prior_lo"]),
    }
    if p_fixed_value is not None:
        model_cfg["P_FIXED_VALUE"] = float(p_fixed_value)
    if alpha_fixed_value is not None:
        model_cfg["ALPHA_FIXED"] = float(alpha_fixed_value)
        
    model_cfg = {**model_cfg, **overrides.get("MODEL_CONFIG", {})}
    kde_cfg = {"observables": list(observables), "N_KDE": int(N_KDE), "seed_kde": int(SEED_KDE)}
    base = {"CASE": str(case), "PLANET": str(planet),
            "KDE_CONFIG": kde_cfg, "MODEL_CONFIG": model_cfg}
    if sampler == "emcee":
        base["MCMC_CONFIG"] = {**MCMC_CONFIG_BASE, **overrides.get("MCMC_CONFIG", {})}
    else:
        base["NS_CONFIG"] = {**NS_CONFIG_BASE, **overrides.get("NS_CONFIG", {})}
    return base


def case_dir(case):
    return Path(case)


def results_exist(case, forward_model, run_tag):
    return (case_dir(case) / "results" / forward_model.lower() / f"{run_tag}.npz").exists()


def fmt_duration(seconds):
    h, r = divmod(int(seconds), 3600)
    m, s = divmod(r, 60)
    return f"{h:02d}h{m:02d}m{s:02d}s"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CORE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def execute_run(case, forward_model, notebook_in, run_tag, params, dry_run, kernel=DEFAULT_KERNEL, force=False):
    # Results / logs stay under pipeline/<case>/ — never under papers/.
    results_root = (case_dir(case) / "results").resolve()
    if set(results_root.parts) & {"PaperFigures", "paper_figures", "papers"}:
        raise RuntimeError(
            f"Refusing to write results under papers/: {results_root}"
        )

    out_dir = case_dir(case) / "tests_outputs"
    log_dir = case_dir(case) / "tests_logs"
    out_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)
    nb_out = out_dir / f"{run_tag}.ipynb"
    log_out = log_dir / f"{run_tag}.log"

    if not force and results_exist(case, forward_model, run_tag):
        print(f"  [SKIP] {run_tag} already has results.")
        return {"status": "skipped", "run_tag": run_tag, "duration": 0}

    if dry_run:
        print(f"  [DRY]  {run_tag}")
        return {"status": "dry", "run_tag": run_tag, "duration": 0}

    cmd = [sys.executable, "-m", "papermill", str(notebook_in), str(nb_out),
           "--cwd", ".", "--parameters_file", "/dev/stdin",
           "--no-progress-bar", "--kernel", kernel]
    t0 = time.time()
    try:
        with open(log_out, "w") as log_fh:
            subprocess.run(cmd, input=json.dumps(params).encode(),
                           stdout=log_fh, stderr=subprocess.STDOUT, check=True)
        status = "ok"
    except subprocess.CalledProcessError:
        status = "FAILED"
    return {"status": status, "run_tag": run_tag,
            "duration": time.time() - t0, "log": str(log_out)}


def build_run_list(sampler, case):
    runs = []
    combos = itertools.product(PLANETS, KDE_VARIANTS, FREE_PARAM_VARIANTS,
                               ALPHA_FREE_VARIANTS, P_FREE_VARIANTS, FORWARD_MODEL_VARIANTS)
    for idx, (planet, obs, free, alpha_free, p_free, fm) in enumerate(combos):
        ov = OVERRIDES.get(idx, {})
        rho_free, b_free = free["RHO_TRUE_FREE"], free["B_FREE"]
        
        # Prepare permutations for p
        p_perms = [{"label": "", "p_val": None}]
        if not p_free and P_FIXED_RUNS:
            p_perms = []
            for fixed_run in P_FIXED_RUNS:
                frac = fixed_run.get("fraction", 0.0)
                p_min = p_min_earth_density(PLANET_PARAMS[planet]["Mp"])
                p_max = PLANET_PARAMS[planet]["p_mean_ref"]
                p_perms.append({
                    "label": fixed_run.get("label", ""),
                    "p_val": p_min + frac * (p_max - p_min)
                })

        # Prepare permutations for alpha (fixed values when alpha is not free)
        alpha_perms = [{"label": "", "alpha_val": None}]
        if not alpha_free and ALPHA_FIXED_RUNS:
            alpha_perms = []
            for fixed_run in ALPHA_FIXED_RUNS:
                alpha_perms.append({
                    "label": fixed_run.get("label", ""),
                    "alpha_val": fixed_run.get("value")
                })
        
        # Cartesian product of p and alpha permutations
        for p_perm in p_perms:
            for alpha_perm in alpha_perms:
                # combine labels (e.g. "P1_A2")
                labels = [l for l in [p_perm["label"], alpha_perm["label"]] if l]
                run_label = "_".join(labels) if labels else None
                
                params = build_params(
                    sampler, case, planet, obs, rho_free, b_free, alpha_free, ov,
                    p_free=p_free, forward_model=fm,
                    p_fixed_value=p_perm["p_val"],
                    alpha_fixed_value=alpha_perm["alpha_val"]
                )
                tag = build_run_tag(
                    sampler, case, planet, obs, rho_free, b_free, alpha_free, params,
                    p_free=p_free, forward_model=fm, run_label=run_label
                )
                # Keep run_label in params so run_sweep_parallel_configurable can extract it later
                params["run_label"] = run_label
                runs.append({"sampler": sampler, "run_tag": tag, "params": params, "forward_model": fm})
    return runs


def main():
    ap = argparse.ArgumentParser(description="Photo-Ring pipeline sweep")
    # dynesty is the manuscript sampler; emcee is an optional cross-check.
    ap.add_argument("--sampler", choices=["emcee", "dynesty", "both"], default="dynesty")
    ap.add_argument("--config", default="run_config.py", help="Config file to use (default: run_config.py)")
    ap.add_argument("--case", default=DEFAULT_CASE, help="Case directory (default kepler_51)")
    ap.add_argument("--notebook-emcee", type=Path, default=DEFAULT_NB_EMCEE)
    ap.add_argument("--notebook-dynesty", type=Path, default=DEFAULT_NB_DYNESTY)
    ap.add_argument("--kernel", default=DEFAULT_KERNEL,
                    help="Jupyter kernel name (default: python3 from the repo .venv)")
    ap.add_argument("--force", action="store_true",
                    help="Overwrite existing runs instead of skipping them")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--forward-models", nargs="+", default=["exorings"],
                    help="Forward model(s) to run (default: exorings). Examples: exorings exorings_legacy")
    args = ap.parse_args()

    if args.forward_models:
        global FORWARD_MODEL_VARIANTS
        FORWARD_MODEL_VARIANTS = args.forward_models

    samplers = ["emcee", "dynesty"] if args.sampler == "both" else [args.sampler]
    nb_map = {"emcee": args.notebook_emcee, "dynesty": args.notebook_dynesty}

    all_runs = []
    for s in samplers:
        all_runs.extend(build_run_list(s, args.case))

    total = len(all_runs)
    print(f"\n{'=' * 64}")
    print(f"  Photo-Ring sweep — case '{args.case}' — {total} runs  |  {datetime.now():%Y-%m-%d %H:%M}")
    print(f"  Samplers: {samplers} | KDE variants: {len(KDE_VARIANTS)}")
    print(f"  Python: {sys.executable}")
    print(f"  Results -> {case_dir(args.case).resolve() / 'results'}")
    print(f"{'=' * 64}\n")

    results_log = []
    t_start = time.time()
    for i, run in enumerate(all_runs, 1):
        s, tag, nb_in = run["sampler"], run["run_tag"], nb_map[run["sampler"]]
        print(f"[{i:>3}/{total}] {s.upper():<8}  {tag}")
        if not nb_in.exists():
            print(f"  [ERROR] notebook not found: {nb_in}\n")
            results_log.append({"status": "no_notebook", "run_tag": tag})
            continue
        res = execute_run(args.case, run["forward_model"], nb_in, tag, run["params"],
                          args.dry_run, kernel=args.kernel, force=args.force)
        results_log.append(res)
        if res["status"] == "ok":
            print(f"  [OK]   {fmt_duration(res['duration'])}  ->  {res['log']}")
        elif res["status"] == "FAILED":
            print(f"  [FAIL] {fmt_duration(res['duration'])}  ->  {res['log']}")
        print()

    ok = sum(1 for r in results_log if r["status"] == "ok")
    skipped = sum(1 for r in results_log if r["status"] == "skipped")
    failed = sum(1 for r in results_log if r["status"] == "FAILED")
    dry = sum(1 for r in results_log if r["status"] == "dry")
    print(f"\n{'=' * 64}")
    print(f"  Sweep done in {fmt_duration(time.time() - t_start)}")
    print(f"  OK={ok}  SKIP={skipped}  FAIL={failed}  DRY={dry}")
    print(f"{'=' * 64}\n")

    if not args.dry_run:
        log_dir = case_dir(args.case) / "tests_logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        sweep_log = log_dir / f"sweep_{datetime.now():%Y%m%d_%H%M%S}.json"
        sweep_log.write_text(json.dumps(results_log, indent=2))
        print(f"  Sweep log -> {sweep_log}\n")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
