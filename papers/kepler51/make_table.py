import json
import numpy as np

M_E_M_S = 3.0034895e-6 # Earth mass in solar masses
R_E_R_S = 0.0091577 # Earth radius in solar radii
RHO_E = 5.51 # Earth density g/cm^3
M_p_earth = 6.9 # Earth masses
R_star_sun = 0.869 # Solar radii
R_star_earth = R_star_sun / R_E_R_S

def get_stats(data, param):
    med = data[f"stat_{param}_median"]
    p16 = data[f"stat_{param}_p16"]
    p84 = data[f"stat_{param}_p84"]
    upper = p84 - med
    lower = med - p16
    return med, upper, lower

def get_derived(data):
    med_p, _, _ = get_stats(data, "p")
    # Rp in Earth radii
    R_p_earth = med_p * R_star_earth
    # rho_p in g/cm^3
    rho_p = RHO_E * M_p_earth / (R_p_earth**3)
    return R_p_earth, rho_p

def format_val(val, up, low, fmt="{:.2f}"):
    s_val = fmt.format(val)
    s_up = fmt.format(up)
    s_low = fmt.format(low)
    return f"${s_val}^{{+{s_up}}}_{{-{s_low}}}$"

with open("pipeline/kepler_51/results/exorings/kepler_51_b_NS_exorings_kde_delta-T14-T23-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_alphaFREE_pFREE_meta.json") as f:
    data_b = json.load(f)

with open("pipeline/kepler_51/results/exorings/kepler_51_d_NS_exorings_kde_delta-T14-T23-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_alphaFREE_pFREE_meta.json") as f:
    data_d = json.load(f)

latex = r"""
\begin{table}[t]
\centering
\caption{Full-set retrieval results for \exoplanet{Kepler-51}{b} and \exoplanet{Kepler-51}{d}. The table reports the median values and the 16th and 84th percentiles for the ring geometry parameters, nuisance parameters, and selected derived physical properties.}
\label{tab:full_set_results}
\begin{tabular}{lcc}
\toprule
Parameter & \exoplanet{Kepler-51}{b} & \exoplanet{Kepler-51}{d} \\
\midrule
\multicolumn{3}{l}{\textit{Ring geometry}} \\
$f_e$ [$R_p$] & %s & %s \\
$i_R$ [$^\circ$] & %s & %s \\
$\theta_R$ [$^\circ$] & %s & %s \\
$p$ & %s & %s \\
$\alpha$ & %s & %s \\
\midrule
\multicolumn{3}{l}{\textit{Nuisance parameters}} \\
$\rho_{\star,\mathrm{true}}$ [$\mathrm{g\,cm^{-3}}$] & %s & %s \\
$b$ & %s & %s \\
\midrule
\multicolumn{3}{l}{\textit{Derived parameters}} \\
$R_p$ [$R_\oplus$] & %.2f & %.2f \\
$\rho_p$ [$\mathrm{g\,cm^{-3}}$] & %.3f & %.3f \\
\bottomrule
\end{tabular}
\end{table}
"""

params = [
    ("fe", "{:.2f}"),
    ("ir", "{:.1f}"),
    ("theta", "{:.1f}"),
    ("p", "{:.4f}"),
    ("alpha", "{:.3f}"),
    ("rho_true", "{:.2f}"),
    ("b", "{:.3f}")
]

vals = []
for param, fmt in params:
    vb, ub, lb = get_stats(data_b, param)
    vd, ud, ld = get_stats(data_d, param)
    vals.append(format_val(vb, ub, lb, fmt))
    vals.append(format_val(vd, ud, ld, fmt))

Rb, rhob = get_derived(data_b)
Rd, rhod = get_derived(data_d)
vals.extend([Rb, Rd, rhob, rhod])

print(latex % tuple(vals))
