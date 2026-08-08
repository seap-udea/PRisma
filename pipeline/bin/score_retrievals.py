#!/usr/bin/env python3
"""score_retrievals.py — Classify Photo-Ring retrievals based on a decision tree.

Generates a JSON table with categories and saves it in the results directory.
"""

import os
import sys
import json
import urllib.parse
import argparse
import numpy as np
from pathlib import Path

# Make sure we can import photoring and generate_figures
_PIPELINE = Path(__file__).resolve().parent.parent
if str(_PIPELINE) not in sys.path:
    sys.path.insert(0, str(_PIPELINE))

import photoring as pr
from photoring.io import load_run, load_observables
from generate_figures import PPC_OBSERVABLES, _infer_case_root, _load_ttv_cache
import glob
from collections import defaultdict

def count_kde_peaks(samples):
    try:
        from scipy.stats import gaussian_kde
        from scipy.signal import find_peaks
        kde = gaussian_kde(samples)
        x = np.linspace(np.min(samples), np.max(samples), 200)
        y = kde(x)
        peaks, _ = find_peaks(y, prominence=0.05*np.max(y))
        return len(peaks) if len(peaks) > 0 else 1
    except:
        return 1

def compute_z1(run, ttv_data):
    from photoring import plotting as plot
    ppc = run.get("ppc")
    if ppc is None or not hasattr(ppc, "shape") or ppc.ndim != 2:
        return float("nan"), float("nan")

    w1_vals = []
    lc_w1_vals = []
    crit_w1_vals = []
    for key in PPC_OBSERVABLES:
        meta = plot.obs_meta(key)
        col = meta.get("ppc_col")
        if col is None or col >= ppc.shape[1]:
            continue
        scale = float(meta.get("scale", 1.0))
        emp = np.asarray(ttv_data.get(meta["df_col"], []), dtype=float).ravel() * scale
        pred = np.asarray(ppc[:, col], dtype=float).ravel() * scale
        emp = emp[np.isfinite(emp)]
        pred = pred[np.isfinite(pred)]
        if emp.size == 0 or pred.size == 0:
            continue
        mu = float(np.mean(emp))
        if not np.isfinite(mu) or abs(mu) < 1e-12:
            continue
        stats = plot.ppc_stats_1d(emp, pred)
        w1 = float(stats["W1"]) / abs(mu)
        if np.isfinite(w1) and w1 > 0:
            w1_vals.append(w1)
            if key in ["delta", "T14", "T23"]:
                lc_w1_vals.append(w1)
            if key in ["delta", "rho_obs_gcc", "rho_obs_kgm3", "rho_obs"]:
                crit_w1_vals.append(w1)

    if not w1_vals:
        return float("nan"), float("nan"), float("nan")
    z1 = float(-np.log10(float(np.mean(w1_vals))))
    if lc_w1_vals:
        z1_min = float(-np.log10(float(np.max(lc_w1_vals))))
    else:
        z1_min = float("nan")
        
    if crit_w1_vals:
        z_crit = float(-np.log10(float(np.max(crit_w1_vals))))
    else:
        z_crit = float("nan")
        
    return z1, z1_min, z_crit

def get_decision_tree_category(z1, z1_min, z_crit, err_rho_true, fe_p16, angle_peaks, logz):
    """
    Evaluates the retrieval through a strict decision tree.
    Returns a string category.
    """
    if z1 is None or not np.isfinite(z1):
        return "[Rejected] Missing PPC"
    if z1 < 1.3:
        return "[Rejected] Poor Fit"
    if z1_min is not None and z1_min < 1.2:
        return "[Rejected] Poor Individual Fit"
    if z_crit is not None and z_crit < 1.75:
        return "[Rejected] Poor Critical Fit"
    if err_rho_true is not None and err_rho_true > 0.25:
        return "[Rejected] Unphysical Nuisance"
    if fe_p16 is not None and fe_p16 < 1.0:
        return "[Degenerate] Ringless"
    if angle_peaks is not None and angle_peaks > 1.5:
        return "[Acceptable] Multimodal Angles"
    if logz is not None and logz < 0.0:  # Threshold for Bayesian evidence
        return "[Acceptable] Low Bayesian Evidence"
    
    return "[Excellent] Golden Sample"

def score_retrieval(npz_path: Path, ttv_cache_dict: dict):
    """
    Evaluates a single retrieval and extracts metrics for the decision tree.
    """
    print(f"Scoring {npz_path.name} ...")
    
    npz_path = Path(npz_path)
    meta_path = npz_path.with_name(npz_path.stem + "_meta.json")
    if not meta_path.exists():
        return None
        
    try:
        run = load_run(npz_path)
    except Exception as e:
        print(f"Error loading {npz_path.name}: {e}")
        return None
        
    case_root = _infer_case_root(npz_path)
    case_paths = pr.CasePaths(case_root.name, pipeline_dir=_PIPELINE)
    key = str(case_root.resolve())
    if key not in ttv_cache_dict:
        ttv_cache_dict[key] = _load_ttv_cache(case_paths, {})
    ttv_get = ttv_cache_dict[key]
    
    meta = run.get('meta', {})
    planet = run.get("planet", meta.get("planet"))
    
    ttv = {}
    try:
        ttv = ttv_get(planet)
        z1, z1_min, z_crit = compute_z1(run, ttv)
    except Exception as e:
        print(f"Error computing z1 for {npz_path.name}: {e}")
        z1 = float("nan")
        z1_min = float("nan")
        z_crit = float("nan")

    # Get equal-weight samples
    samples = run.get('samples')
    logwt = run.get('logwt')
    if samples is None or logwt is None:
        try:
            with np.load(npz_path) as f:
                samples = f['samples']
                logwt = f['logwt']
        except Exception:
            return None
            
    wt = np.exp(logwt - logwt.max())
    wt /= wt.sum()
    idx = np.random.choice(len(samples), size=3000, p=wt, replace=True)
    eq_samples = samples[idx]
    
    param_names = meta.get('param_names', [])
    k = len(param_names)
    
    max_logl = None
    aic = None
    logl = run.get('logl')
    if logl is None:
        try:
            with np.load(npz_path) as f:
                if 'logl' in f:
                    logl = f['logl']
        except Exception:
            pass

    if logl is not None and len(logl) > 0:
        max_logl = float(np.max(logl))
        aic = 2 * k - 2 * max_logl
    
    # 1. Ring Degeneracy (fe)
    fe_p16 = meta.get('stat_fe_p16')
    if fe_p16 is None and 'fe' in param_names:
        idx = param_names.index('fe')
        fe_p16 = float(np.percentile(eq_samples[:, idx], 16))
        
    # 2. Angles Multimodality
    angle_peaks = None
    angle_peaks_list = []
    for ang in ['ir', 'theta']:
        if ang in param_names:
            idx = param_names.index(ang)
            angle_peaks_list.append(count_kde_peaks(eq_samples[:, idx]))
    if angle_peaks_list:
        angle_peaks = float(np.mean(angle_peaks_list))
    
    # 3. Nuisance `rho_true` should be close to the independent stellar density `RHO_TRUE_FIXED`
    err_rho_true = None
    if 'rho_true' in param_names and 'RHO_TRUE_FIXED' in meta:
        idx = param_names.index('rho_true')
        median_rho_true = float(np.median(eq_samples[:, idx]))
        true_val = float(meta['RHO_TRUE_FIXED'])
        err_rho_true = abs(median_rho_true - true_val) / true_val
    
    raw_z1 = float(z1) if np.isfinite(z1) else None
    raw_z1_min = float(z1_min) if np.isfinite(z1_min) else None
    raw_z_crit = float(z_crit) if np.isfinite(z_crit) else None
    
    category = get_decision_tree_category(raw_z1, raw_z1_min, raw_z_crit, err_rho_true, fe_p16, angle_peaks, meta.get('logz'))
    
    return {
        'file': npz_path.name,
        'case': run.get('case', meta.get('case', 'kepler_51')),
        'planet': planet,
        'tag': run.get('tag', meta.get('run_tag')),
        'raw_z1': raw_z1,
        'z1_min': raw_z1_min,
        'z_crit': raw_z_crit,
        'fe_p16': fe_p16,
        'angle_peaks': angle_peaks,
        'err_rho_true': err_rho_true,
        'logz': meta.get('logz'),
        'max_logl': max_logl,
        'aic': aic,
        'category': category
    }

def find_figure(results_dir: Path, tag: str, kind: str):
    """Finds the figure in the figures/ directory ending with {tag}_{kind}.png"""
    figures_dir = results_dir / "figures"
    pattern = str(figures_dir / f"*{tag}_{kind}.png")
    matches = glob.glob(pattern)
    if matches:
        return f"figures/{Path(matches[0]).name}"
    return f"figures/{tag}_{kind}.png"

def format_val(val, fmt="{:.2f}"):
    if val is None:
        return "N/A"
    return fmt.format(val)

def generate_markdown(results_dir: Path, case: str, planet: str, results: list):
    md_path = results_dir / f"scoring_{case}_{planet}.md"
    
    CATEGORY_ORDER = [
        "[Excellent] Golden Sample",
        "[Acceptable] Low Bayesian Evidence",
        "[Acceptable] Multimodal Angles",
        "[Degenerate] Ringless",
        "[Rejected] Unphysical Nuisance",
        "[Rejected] Poor Individual Fit",
        "[Rejected] Poor Fit",
        "[Rejected] Missing PPC"
    ]
    
    lines = [
        f"# {case.capitalize()} {planet.upper()} Retrievals Classification Report",
        "",
        "This report groups retrievals into strict physical categories based on a Decision Tree logic. Within each category, retrievals are ranked by their Bayesian Evidence ($\\ln \\mathcal{Z}$).",
        ""
    ]
    
    by_category = defaultdict(list)
    for r in results:
        cat = r.get('category', 'Unknown')
        by_category[cat].append(r)
        
    lines.append("## Category Summary")
    for cat in CATEGORY_ORDER:
        if cat in by_category:
            lines.append(f"- **{cat}**: {len(by_category[cat])} retrievals")
    lines.append("")
    
    lines.append("## Detailed Results")
    lines.append("")
    
    rank = 1
    for cat in CATEGORY_ORDER:
        if cat not in by_category:
            continue
            
        group = by_category[cat]
        lines.append(f"### Category: {cat}")
        lines.append("")
        
        lines.append("| Rank | Tag | PPC (z1) | PPC (z_crit) | ln Z | max ln L | AIC | Ring fe (16%) | err(rho_true) | Angle Peaks |")
        lines.append("|---|---|---|---|---|---|---|---|---|---|")
        
        for r in group:
            z1_str = format_val(r.get('raw_z1'), "{:.2f}")
            z_crit_str = format_val(r.get('z_crit'), "{:.2f}")
            logz_str = format_val(r.get('logz'), "{:.2f}")
            maxlogl_str = format_val(r.get('max_logl'), "{:.2f}")
            aic_str = format_val(r.get('aic'), "{:.2f}")
            fe_str = format_val(r.get('fe_p16'), "{:.2f}")
            rho_err_str = format_val(r.get('err_rho_true'), "{:.4f}")
            ang_str = format_val(r.get('angle_peaks'), "{:.1f}")
            
            lines.append(f"| {rank} | `{r['tag']}` | **{z1_str}** | **{z_crit_str}** | {logz_str} | {maxlogl_str} | {aic_str} | {fe_str} | {rho_err_str} | {ang_str} |")
            rank += 1
        lines.append("")
        
        for r in group:
            lines.append(f"#### {r['tag']}")
            lines.append(f"- **PPC (z1)**: {format_val(r.get('raw_z1'))}")
            lines.append(f"- **PPC (z_crit)**: {format_val(r.get('z_crit'))}")
            lines.append(f"- **ln Z (Evidence)**: {format_val(r.get('logz'), '{:.3f}')}")
            lines.append(f"- **max ln L**: {format_val(r.get('max_logl'), '{:.3f}')}")
            lines.append(f"- **AIC**: {format_val(r.get('aic'), '{:.3f}')}")
            lines.append(f"- **PPC (z1 min)**: {format_val(r.get('z1_min'))}")
            lines.append(f"- **Ring fe (16th)**: {format_val(r.get('fe_p16'))}")
            lines.append(f"- **err(rho_true)**: {format_val(r.get('err_rho_true'), '{:.4f}')}")
            lines.append(f"- **Angle Peaks**: {format_val(r.get('angle_peaks'), '{:.1f}')}")
            lines.append(f"- **Category**: {r.get('category', cat)}")
            lines.append("")
            
            corner_img = urllib.parse.quote(find_figure(results_dir, r['tag'], "corner"))
            ppc_img = urllib.parse.quote(find_figure(results_dir, r['tag'], "ppc"))
            
            lines.append(f"![Corner Plot]({corner_img})")
            lines.append("")
            lines.append(f"![PPC]({ppc_img})")
            lines.append("")
            lines.append("---")
            lines.append("")

    with open(md_path, "w") as f:
        f.write("\n".join(lines))
        
    print(f"Generated markdown report at {md_path}")

def process_directory(results_dir: Path, report: bool, force: bool, ttv_cache_dict: dict):
    npz_files = list(results_dir.glob("*.npz"))
    if not npz_files:
        print(f"Error: No NPZ files found in {results_dir}")
        return

    existing_results = {}
    if not force:
        for json_file in results_dir.glob("scoring_*.json"):
            try:
                with open(json_file, "r") as f:
                    data = json.load(f)
                    for r in data:
                        if 'file' in r:
                            existing_results[r['file']] = r
            except Exception as e:
                print(f"Warning: Could not read {json_file}: {e}")

    results = []
    for i, f in enumerate(npz_files, 1):
        if not force and f.name in existing_results:
            print(f"[{i:03d}/{len(npz_files)}] Skipping {f.name} (already scored)")
            results.append(existing_results[f.name])
            continue
            
        print(f"[{i:03d}/{len(npz_files)}]", end=" ")
        r = score_retrieval(f, ttv_cache_dict)
        if r:
            results.append(r)
            
    # Calculate order keys based on ln Z
    for r in results:
        logz = r.get('logz')
        if logz is not None and np.isfinite(logz):
            inv = int(round((100.0 - float(logz)) * 1000.0))
            inv = max(0, min(99999, inv))
            zkey = f"ord{inv:05d}-lnZ_{float(logz):+06.2f}"
        else:
            zkey = "ord99999-lnZ_nan"
        r['zkey'] = zkey
        
    # Group by case and planet
    grouped_results = {}
    for r in results:
        key = (r.get('case', 'kepler_51'), r['planet'])
        if key not in grouped_results:
            grouped_results[key] = []
        grouped_results[key].append(r)
        
    for (case, planet), group in grouped_results.items():
        # Sort entirely by logz descending!
        group.sort(key=lambda x: (x.get('logz') if x.get('logz') is not None else -np.inf), reverse=True)
        
        out_file = results_dir / f"scoring_{case}_{planet}.json"
        with open(out_file, "w") as f:
            json.dump(group, f, indent=2)
            
        print(f"\nScored {len(group)} retrievals for {case} {planet}. Output written to {out_file}.")
        
        print(f"Categories Distribution:")
        cat_counts = {}
        for r in group:
            cat_counts[r['category']] = cat_counts.get(r['category'], 0) + 1
        for cat, cnt in sorted(cat_counts.items()):
            print(f"  {cat}: {cnt}")
            
        # Generate markdown report only if requested
        if report:
            generate_markdown(results_dir, case, planet, group)

def main():
    parser = argparse.ArgumentParser(description="Classify Photo-Ring retrievals based on a decision tree.")
    parser.add_argument("results_dir", nargs="?", type=str, 
                        default=None,
                        help="Directory or sub-directory containing the .npz files.")
    parser.add_argument("--report", action="store_true", help="Generate the markdown visual report.")
    parser.add_argument("--force", action="store_true", help="Force rescoring all files. By default, only new files are scored.")
    parser.add_argument("--recursive", action="store_true", help="Recursively score all subdirectories with results.")
    args = parser.parse_args()
    
    base_results = Path(__file__).resolve().parent.parent / "kepler_51" / "results" / "exorings"
    ttv_cache_dict = {}

    if args.recursive:
        dirs_with_npz = {f.parent for f in base_results.rglob("*.npz")}
        if not dirs_with_npz:
            print(f"Error: No NPZ files found in {base_results} or its subdirectories.")
            return
        for d in sorted(dirs_with_npz):
            print(f"\n{'='*60}\nScoring directory: {d}\n{'='*60}")
            process_directory(d, args.report, args.force, ttv_cache_dict)
    else:
        if args.results_dir is None:
            target_dir = base_results
        else:
            target_dir = Path(args.results_dir)
            if not target_dir.is_absolute() and not target_dir.exists():
                candidate = base_results / args.results_dir
                if candidate.exists():
                    target_dir = candidate

        process_directory(target_dir, args.report, args.force, ttv_cache_dict)

if __name__ == '__main__':
    main()
