#!/usr/bin/env python3
"""score_retrievals.py — Classify Photo-Ring retrievals based on a decision tree.

Generates a JSON table with categories and saves it in the results directory.
"""

import os
import sys
import json
import numpy as np
from pathlib import Path

# Make sure we can import photoring and generate_figures
_PIPELINE = Path(__file__).resolve().parent
if str(_PIPELINE) not in sys.path:
    sys.path.insert(0, str(_PIPELINE))

import photoring as pr
from photoring.io import load_run, load_observables
from generate_figures import _compute_z1, PPC_OBSERVABLES, _infer_case_root, _load_ttv_cache

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

    if not w1_vals:
        return float("nan"), float("nan")
    z1 = float(-np.log10(float(np.mean(w1_vals))))
    if lc_w1_vals:
        z1_min = float(-np.log10(float(np.max(lc_w1_vals))))
    else:
        z1_min = float("nan")
    return z1, z1_min

def get_decision_tree_category(z1, z1_min, err_rho_true, fe_p16, angle_peaks):
    """
    Evaluates the retrieval through a strict decision tree.
    Returns a string category.
    """
    if z1 is None or not np.isfinite(z1):
        return "[Rejected] Missing PPC"
    if z1 < 1.2:
        return "[Rejected] Poor Fit"
    if z1_min is not None and z1_min < 1.0:
        return "[Rejected] Poor Individual Fit"
    if err_rho_true is not None and err_rho_true > 0.25:
        return "[Rejected] Unphysical Nuisance"
    if fe_p16 is not None and fe_p16 < 1.0:
        return "[Degenerate] Ringless"
    if angle_peaks is not None and angle_peaks > 1.5:
        return "[Acceptable] Multimodal Angles"
    
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
        z1, z1_min = compute_z1(run, ttv)
    except Exception as e:
        print(f"Error computing z1 for {npz_path.name}: {e}")
        z1 = float("nan")
        z1_min = float("nan")

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
    
    category = get_decision_tree_category(raw_z1, raw_z1_min, err_rho_true, fe_p16, angle_peaks)
    
    return {
        'file': npz_path.name,
        'case': run.get('case', meta.get('case', 'kepler_51')),
        'planet': planet,
        'tag': run.get('tag', meta.get('run_tag')),
        'raw_z1': raw_z1,
        'z1_min': raw_z1_min,
        'fe_p16': fe_p16,
        'angle_peaks': angle_peaks,
        'err_rho_true': err_rho_true,
        'category': category
    }

def main():
    if len(sys.argv) > 1:
        results_dir = Path(sys.argv[1])
    else:
        results_dir = Path(__file__).resolve().parent / "kepler_51" / "results" / "exorings"
        
    npz_files = list(results_dir.glob("*.npz"))
    if not npz_files:
        print(f"Error: No NPZ files found in {results_dir}")
        return

    ttv_cache_dict = {}
    results = []
    for i, f in enumerate(npz_files, 1):
        print(f"[{i:03d}/{len(npz_files)}]", end=" ")
        r = score_retrieval(f, ttv_cache_dict)
        if r:
            results.append(r)
            
    # Calculate order keys
    for r in results:
        z1 = r['raw_z1']
        if z1 is not None:
            inv = int(round((100.0 - float(z1)) * 1000.0))
            inv = max(0, min(99999, inv))
            zkey = f"ord{inv:05d}-z1_{z1:05.2f}"
        else:
            zkey = "ord99999-z1_nan"
        r['zkey'] = zkey
        
    # Group by case and planet
    grouped_results = {}
    for r in results:
        key = (r.get('case', 'kepler_51'), r['planet'])
        if key not in grouped_results:
            grouped_results[key] = []
        grouped_results[key].append(r)
        
    for (case, planet), group in grouped_results.items():
        # Sort entirely by raw_z1 descending!
        group.sort(key=lambda x: (x['raw_z1'] if x['raw_z1'] is not None else -np.inf), reverse=True)
        
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

if __name__ == '__main__':
    main()
