import json
import numpy as np
from pathlib import Path

M_E_M_S = 3.0034895e-6
R_E_R_S = 0.0091577
RHO_E = 5.51
M_p_earth = 6.9
R_star_sun = 0.869
R_star_earth = R_star_sun / R_E_R_S

def get_param(data, param, run_tag="", fmt="{:.2f}"):
    if f"stat_{param}_median" in data:
        med = data[f"stat_{param}_median"]
        p16 = data[f"stat_{param}_p16"]
        p84 = data[f"stat_{param}_p84"]
        upper = p84 - med
        lower = med - p16
        return f"${fmt.format(med)}^{{+{fmt.format(upper)}}}_{{-{fmt.format(lower)}}}$", med
    elif f"{param.upper()}_FIXED" in data:
        val = data[f"{param.upper()}_FIXED"]
        return f"${fmt.format(val)}$", val
    else:
        if param == "p" and "_P" in run_tag:
            import re
            m = re.search(r"_P([13579])(?:_|$)", run_tag)
            if m:
                frac = float(m.group(1)) / 10.0
                p_min = data.get("p_min", 0.0)
                p_max = data.get("p_mean_ref", 0.0)
                val = p_min + frac * (p_max - p_min)
                return f"${fmt.format(val)}$", val
        return "N/A", 0.0

def make_table():
    base_dir = Path("pipeline/kepler_51/results/exorings/explore_radius_alpha")
    rows = []
    
    for planet in ["b", "d"]:
        score_file = base_dir / f"scoring_kepler_51_{planet}.json"
        if not score_file.exists():
            continue
        with open(score_file) as f:
            scores = json.load(f)
            
        for score in scores:
            if score.get("category") == "[Excellent] Golden Sample":
                tag = score["tag"]
                meta_file = base_dir / f"{tag}_meta.json"
                with open(meta_file) as f:
                    meta = json.load(f)
                    
                p_str, p_val = get_param(meta, "p", tag, "{:.4f}")
                R_p_earth = p_val * R_star_earth
                p_earth_str = "{:.2f}".format(R_p_earth)
                p_comb = f"{p_str}\\;({p_earth_str})"
                
                fe_str, _ = get_param(meta, "fe", tag, "{:.2f}")
                ir_str, _ = get_param(meta, "ir", tag, "{:.1f}")
                theta_str, _ = get_param(meta, "theta", tag, "{:.1f}")
                alpha_str, _ = get_param(meta, "alpha", tag, "{:.2f}")
                rho_star_str, _ = get_param(meta, "rho_true", tag, "{:.2f}")
                b_str, _ = get_param(meta, "b", tag, "{:.2f}")
                
                rho_p = RHO_E * M_p_earth / (R_p_earth**3) if R_p_earth > 0 else 0
                rho_p_str = f"{rho_p:.3f}"
                
                lnZ = score.get("logz", 0.0)
                lnZ_str = f"{lnZ:.2f}"
                
                rows.append({
                    "planet": planet,
                    "p_comb": p_comb,
                    "fe": fe_str,
                    "ir": ir_str,
                    "theta": theta_str,
                    "alpha": alpha_str,
                    "rho_star": rho_star_str,
                    "b": b_str,
                    "rho_p": rho_p_str,
                    "lnZ": lnZ,
                    "lnZ_str": lnZ_str
                })
                
    # Sort by planet then lnZ descending
    rows.sort(key=lambda x: (x["planet"], -x["lnZ"]))
    
    latex = []
    latex.append("\\begin{table*}[t]")
    latex.append("\\centering")
    latex.append("\\footnotesize")
    latex.append("\\caption{Golden Sample retrievals from the radius-alpha grid search for \\exoplanet{Kepler-51}{b} and \\exoplanet{Kepler-51}{d}.}")
    latex.append("\\label{tab:grid_golden}")
    latex.append("\\setlength{\\tabcolsep}{4pt}")
    latex.append("\\begin{tabular*}{1.0\\textwidth}{@{\\extracolsep{\\fill}} lccccccccc}")
    latex.append("\\hline")
    latex.append("\\hline")
    latex.append("Planet & $p\\;[R_\\star]\\;(R_\\oplus)$ & $f_e\\;[R_p]$ & $i_R\\;[^\\circ]$ & $\\theta_R\\;[^\\circ]$ & $\\alpha$ & $\\rho_{\\star,\\mathrm{true}}\\:[\\mathrm{g\\,cm^{-3}}]$ & $b$ & $\\rho_p\\:[\\mathrm{g\\,cm^{-3}}]$ & $\\ln \\mathcal{Z}$ \\\\")
    latex.append("\\hline")
    
    current_planet = None
    for r in rows:
        pl = "b" if r["planet"] == "b" else "d"
        pl_name = f"\\exoplanet{{Kepler-51}}{{{pl}}}"
        
        row_str = f"{pl_name} & {r['p_comb']} & {r['fe']} & {r['ir']} & {r['theta']} & {r['alpha']} & {r['rho_star']} & {r['b']} & {r['rho_p']} & {r['lnZ_str']} \\\\"
        latex.append(row_str)
        
    latex.append("\\hline")
    latex.append("\\hline")
    latex.append("\\end{tabular*}")
    latex.append("\\end{table*}")
    
    with open("papers/kepler51/tab_grid_golden.tex", "w") as f:
        f.write("\n".join(latex) + "\n")
        
    print("Generated papers/kepler51/tab_grid_golden.tex")

if __name__ == "__main__":
    make_table()
