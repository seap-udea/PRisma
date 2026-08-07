# Kepler_51 B Retrievals Classification Report

This report groups retrievals into strict physical categories based on a Decision Tree logic. Within each category, retrievals are ranked by their Bayesian Evidence ($\ln \mathcal{Z}$).

## Category Summary
- **[Excellent] Golden Sample**: 27 retrievals
- **[Acceptable] Multimodal Angles**: 7 retrievals
- **[Rejected] Unphysical Nuisance**: 8 retrievals
- **[Rejected] Poor Individual Fit**: 2 retrievals
- **[Rejected] Poor Fit**: 16 retrievals

## Detailed Results

### Category: [Excellent] Golden Sample

| Rank | Tag | PPC (z1) | ln Z | PPC (z1 min) | Ring fe (16%) | err(rho_true) | Angle Peaks |
|---|---|---|---|---|---|---|---|
| 1 | `kepler_51_b_NS_exorings_kde_delta-T14-T23-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE` | **1.34** | 9.00 | 2.75 | 1.13 | 0.2299 | 1.0 |
| 2 | `kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE` | **1.43** | 3.36 | 2.94 | 1.13 | 0.2463 | 1.5 |
| 3 | `kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE` | **1.28** | 3.35 | 2.88 | 3.71 | 0.2045 | 1.0 |
| 4 | `kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE` | **1.51** | 2.49 | 2.85 | 1.09 | 0.2408 | 1.5 |
| 5 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE` | **1.33** | 2.01 | 2.89 | 4.00 | 0.1823 | 1.5 |
| 6 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P9_T1` | **1.41** | 1.95 | 2.70 | 1.29 | 0.2210 | 1.0 |
| 7 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE` | **1.21** | 1.94 | 2.68 | 1.12 | 0.2247 | 1.0 |
| 8 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P2_T3` | **1.32** | 1.93 | 2.87 | 2.68 | 0.1574 | 1.5 |
| 9 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P8_T3` | **1.43** | 1.84 | 2.80 | 1.31 | 0.1891 | 1.0 |
| 10 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P9_T3` | **1.42** | 1.71 | 2.68 | 1.18 | 0.2201 | 1.0 |
| 11 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P8_T1` | **1.49** | 1.63 | 2.80 | 1.59 | 0.1976 | 1.0 |
| 12 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P9_T2` | **1.42** | 1.61 | 2.70 | 1.22 | 0.2196 | 1.0 |
| 13 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P3_T1` | **1.40** | 1.18 | 2.98 | 3.35 | 0.1552 | 1.0 |
| 14 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P7_T3` | **1.43** | 1.12 | 2.89 | 1.44 | 0.1932 | 1.0 |
| 15 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P1_T3` | **1.28** | 1.00 | 2.83 | 3.30 | 0.1485 | 1.5 |
| 16 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P8_T2` | **1.58** | 0.95 | 2.80 | 1.45 | 0.1815 | 1.5 |
| 17 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE` | **1.25** | 0.90 | 2.77 | 4.77 | 0.2001 | 1.5 |
| 18 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P6_T2` | **1.38** | 0.88 | 2.78 | 1.69 | 0.2380 | 1.5 |
| 19 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P5_T2` | **1.46** | 0.81 | 3.01 | 2.19 | 0.1441 | 1.5 |
| 20 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P4_T1` | **1.36** | 0.69 | 2.87 | 2.77 | 0.2321 | 1.0 |
| 21 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P5_T3` | **1.26** | 0.63 | 2.88 | 1.72 | 0.1985 | 1.5 |
| 22 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P6_T3` | **1.33** | 0.61 | 2.88 | 1.82 | 0.2016 | 1.0 |
| 23 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P7_T1` | **1.36** | 0.60 | 2.87 | 1.80 | 0.1985 | 1.5 |
| 24 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P2_T2` | **1.32** | 0.55 | 2.87 | 3.13 | 0.1771 | 1.5 |
| 25 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P2_T1` | **1.30** | 0.50 | 2.74 | 3.86 | 0.2131 | 1.5 |
| 26 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P4_T2` | **1.37** | 0.33 | 2.88 | 2.29 | 0.1969 | 1.5 |
| 27 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P4_T3` | **1.29** | 0.12 | 2.86 | 1.96 | 0.2049 | 1.5 |

#### kepler_51_b_NS_exorings_kde_delta-T14-T23-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE
- **PPC (z1)**: 1.34
- **ln Z (Evidence)**: 9.002
- **PPC (z1 min)**: 2.75
- **Ring fe (16th)**: 1.13
- **err(rho_true)**: 0.2299
- **Angle Peaks**: 1.0
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_b_cat1_GoldenSample_ord90998-lnZ_%2B09.00-kepler_51_b_NS_exorings_kde_delta-T14-T23-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE_corner.png)

![PPC](figures/kepler_51_b_cat1_GoldenSample_ord90998-lnZ_%2B09.00-kepler_51_b_NS_exorings_kde_delta-T14-T23-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE
- **PPC (z1)**: 1.43
- **ln Z (Evidence)**: 3.360
- **PPC (z1 min)**: 2.94
- **Ring fe (16th)**: 1.13
- **err(rho_true)**: 0.2463
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_b_cat1_GoldenSample_ord96640-lnZ_%2B03.36-kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE_corner.png)

![PPC](figures/kepler_51_b_cat1_GoldenSample_ord96640-lnZ_%2B03.36-kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE
- **PPC (z1)**: 1.28
- **ln Z (Evidence)**: 3.346
- **PPC (z1 min)**: 2.88
- **Ring fe (16th)**: 3.71
- **err(rho_true)**: 0.2045
- **Angle Peaks**: 1.0
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_b_cat1_GoldenSample_ord96654-lnZ_%2B03.35-kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_corner.png)

![PPC](figures/kepler_51_b_cat1_GoldenSample_ord96654-lnZ_%2B03.35-kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE
- **PPC (z1)**: 1.51
- **ln Z (Evidence)**: 2.492
- **PPC (z1 min)**: 2.85
- **Ring fe (16th)**: 1.09
- **err(rho_true)**: 0.2408
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_b_cat1_GoldenSample_ord97508-lnZ_%2B02.49-kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE_corner.png)

![PPC](figures/kepler_51_b_cat1_GoldenSample_ord97508-lnZ_%2B02.49-kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE
- **PPC (z1)**: 1.33
- **ln Z (Evidence)**: 2.008
- **PPC (z1 min)**: 2.89
- **Ring fe (16th)**: 4.00
- **err(rho_true)**: 0.1823
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_b_cat1_GoldenSample_ord97992-lnZ_%2B02.01-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_corner.png)

![PPC](figures/kepler_51_b_cat1_GoldenSample_ord97992-lnZ_%2B02.01-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P9_T1
- **PPC (z1)**: 1.41
- **ln Z (Evidence)**: 1.949
- **PPC (z1 min)**: 2.70
- **Ring fe (16th)**: 1.29
- **err(rho_true)**: 0.2210
- **Angle Peaks**: 1.0
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_b_cat1_GoldenSample_ord98051-lnZ_%2B01.95-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P9_T1_corner.png)

![PPC](figures/kepler_51_b_cat1_GoldenSample_ord98051-lnZ_%2B01.95-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P9_T1_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE
- **PPC (z1)**: 1.21
- **ln Z (Evidence)**: 1.939
- **PPC (z1 min)**: 2.68
- **Ring fe (16th)**: 1.12
- **err(rho_true)**: 0.2247
- **Angle Peaks**: 1.0
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_b_cat1_GoldenSample_ord98061-lnZ_%2B01.94-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE_corner.png)

![PPC](figures/kepler_51_b_cat1_GoldenSample_ord98061-lnZ_%2B01.94-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P2_T3
- **PPC (z1)**: 1.32
- **ln Z (Evidence)**: 1.931
- **PPC (z1 min)**: 2.87
- **Ring fe (16th)**: 2.68
- **err(rho_true)**: 0.1574
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_b_cat1_GoldenSample_ord98069-lnZ_%2B01.93-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P2_T3_corner.png)

![PPC](figures/kepler_51_b_cat1_GoldenSample_ord98069-lnZ_%2B01.93-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P2_T3_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P8_T3
- **PPC (z1)**: 1.43
- **ln Z (Evidence)**: 1.839
- **PPC (z1 min)**: 2.80
- **Ring fe (16th)**: 1.31
- **err(rho_true)**: 0.1891
- **Angle Peaks**: 1.0
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_b_cat1_GoldenSample_ord98161-lnZ_%2B01.84-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P8_T3_corner.png)

![PPC](figures/kepler_51_b_cat1_GoldenSample_ord98161-lnZ_%2B01.84-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P8_T3_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P9_T3
- **PPC (z1)**: 1.42
- **ln Z (Evidence)**: 1.710
- **PPC (z1 min)**: 2.68
- **Ring fe (16th)**: 1.18
- **err(rho_true)**: 0.2201
- **Angle Peaks**: 1.0
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_b_cat1_GoldenSample_ord98290-lnZ_%2B01.71-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P9_T3_corner.png)

![PPC](figures/kepler_51_b_cat1_GoldenSample_ord98290-lnZ_%2B01.71-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P9_T3_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P8_T1
- **PPC (z1)**: 1.49
- **ln Z (Evidence)**: 1.627
- **PPC (z1 min)**: 2.80
- **Ring fe (16th)**: 1.59
- **err(rho_true)**: 0.1976
- **Angle Peaks**: 1.0
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_b_cat1_GoldenSample_ord98373-lnZ_%2B01.63-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P8_T1_corner.png)

![PPC](figures/kepler_51_b_cat1_GoldenSample_ord98373-lnZ_%2B01.63-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P8_T1_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P9_T2
- **PPC (z1)**: 1.42
- **ln Z (Evidence)**: 1.615
- **PPC (z1 min)**: 2.70
- **Ring fe (16th)**: 1.22
- **err(rho_true)**: 0.2196
- **Angle Peaks**: 1.0
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_b_cat1_GoldenSample_ord98385-lnZ_%2B01.61-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P9_T2_corner.png)

![PPC](figures/kepler_51_b_cat1_GoldenSample_ord98385-lnZ_%2B01.61-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P9_T2_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P3_T1
- **PPC (z1)**: 1.40
- **ln Z (Evidence)**: 1.178
- **PPC (z1 min)**: 2.98
- **Ring fe (16th)**: 3.35
- **err(rho_true)**: 0.1552
- **Angle Peaks**: 1.0
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_b_cat1_GoldenSample_ord98822-lnZ_%2B01.18-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P3_T1_corner.png)

![PPC](figures/kepler_51_b_cat1_GoldenSample_ord98822-lnZ_%2B01.18-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P3_T1_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P7_T3
- **PPC (z1)**: 1.43
- **ln Z (Evidence)**: 1.116
- **PPC (z1 min)**: 2.89
- **Ring fe (16th)**: 1.44
- **err(rho_true)**: 0.1932
- **Angle Peaks**: 1.0
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_b_cat1_GoldenSample_ord98884-lnZ_%2B01.12-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P7_T3_corner.png)

![PPC](figures/kepler_51_b_cat1_GoldenSample_ord98884-lnZ_%2B01.12-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P7_T3_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P1_T3
- **PPC (z1)**: 1.28
- **ln Z (Evidence)**: 1.003
- **PPC (z1 min)**: 2.83
- **Ring fe (16th)**: 3.30
- **err(rho_true)**: 0.1485
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_b_cat1_GoldenSample_ord98997-lnZ_%2B01.00-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P1_T3_corner.png)

![PPC](figures/kepler_51_b_cat1_GoldenSample_ord98997-lnZ_%2B01.00-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P1_T3_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P8_T2
- **PPC (z1)**: 1.58
- **ln Z (Evidence)**: 0.951
- **PPC (z1 min)**: 2.80
- **Ring fe (16th)**: 1.45
- **err(rho_true)**: 0.1815
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_b_cat1_GoldenSample_ord99049-lnZ_%2B00.95-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P8_T2_corner.png)

![PPC](figures/kepler_51_b_cat1_GoldenSample_ord99049-lnZ_%2B00.95-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P8_T2_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE
- **PPC (z1)**: 1.25
- **ln Z (Evidence)**: 0.900
- **PPC (z1 min)**: 2.77
- **Ring fe (16th)**: 4.77
- **err(rho_true)**: 0.2001
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_b_cat1_GoldenSample_ord99100-lnZ_%2B00.90-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_corner.png)

![PPC](figures/kepler_51_b_cat1_GoldenSample_ord99100-lnZ_%2B00.90-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P6_T2
- **PPC (z1)**: 1.38
- **ln Z (Evidence)**: 0.884
- **PPC (z1 min)**: 2.78
- **Ring fe (16th)**: 1.69
- **err(rho_true)**: 0.2380
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_b_cat1_GoldenSample_ord99116-lnZ_%2B00.88-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P6_T2_corner.png)

![PPC](figures/kepler_51_b_cat1_GoldenSample_ord99116-lnZ_%2B00.88-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P6_T2_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P5_T2
- **PPC (z1)**: 1.46
- **ln Z (Evidence)**: 0.811
- **PPC (z1 min)**: 3.01
- **Ring fe (16th)**: 2.19
- **err(rho_true)**: 0.1441
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_b_cat1_GoldenSample_ord99189-lnZ_%2B00.81-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P5_T2_corner.png)

![PPC](figures/kepler_51_b_cat1_GoldenSample_ord99189-lnZ_%2B00.81-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P5_T2_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P4_T1
- **PPC (z1)**: 1.36
- **ln Z (Evidence)**: 0.690
- **PPC (z1 min)**: 2.87
- **Ring fe (16th)**: 2.77
- **err(rho_true)**: 0.2321
- **Angle Peaks**: 1.0
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_b_cat1_GoldenSample_ord99310-lnZ_%2B00.69-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P4_T1_corner.png)

![PPC](figures/kepler_51_b_cat1_GoldenSample_ord99310-lnZ_%2B00.69-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P4_T1_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P5_T3
- **PPC (z1)**: 1.26
- **ln Z (Evidence)**: 0.628
- **PPC (z1 min)**: 2.88
- **Ring fe (16th)**: 1.72
- **err(rho_true)**: 0.1985
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_b_cat1_GoldenSample_ord99372-lnZ_%2B00.63-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P5_T3_corner.png)

![PPC](figures/kepler_51_b_cat1_GoldenSample_ord99372-lnZ_%2B00.63-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P5_T3_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P6_T3
- **PPC (z1)**: 1.33
- **ln Z (Evidence)**: 0.610
- **PPC (z1 min)**: 2.88
- **Ring fe (16th)**: 1.82
- **err(rho_true)**: 0.2016
- **Angle Peaks**: 1.0
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_b_cat1_GoldenSample_ord99390-lnZ_%2B00.61-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P6_T3_corner.png)

![PPC](figures/kepler_51_b_cat1_GoldenSample_ord99390-lnZ_%2B00.61-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P6_T3_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P7_T1
- **PPC (z1)**: 1.36
- **ln Z (Evidence)**: 0.603
- **PPC (z1 min)**: 2.87
- **Ring fe (16th)**: 1.80
- **err(rho_true)**: 0.1985
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_b_cat1_GoldenSample_ord99397-lnZ_%2B00.60-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P7_T1_corner.png)

![PPC](figures/kepler_51_b_cat1_GoldenSample_ord99397-lnZ_%2B00.60-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P7_T1_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P2_T2
- **PPC (z1)**: 1.32
- **ln Z (Evidence)**: 0.554
- **PPC (z1 min)**: 2.87
- **Ring fe (16th)**: 3.13
- **err(rho_true)**: 0.1771
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_b_cat1_GoldenSample_ord99446-lnZ_%2B00.55-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P2_T2_corner.png)

![PPC](figures/kepler_51_b_cat1_GoldenSample_ord99446-lnZ_%2B00.55-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P2_T2_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P2_T1
- **PPC (z1)**: 1.30
- **ln Z (Evidence)**: 0.498
- **PPC (z1 min)**: 2.74
- **Ring fe (16th)**: 3.86
- **err(rho_true)**: 0.2131
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_b_cat1_GoldenSample_ord99502-lnZ_%2B00.50-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P2_T1_corner.png)

![PPC](figures/kepler_51_b_cat1_GoldenSample_ord99502-lnZ_%2B00.50-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P2_T1_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P4_T2
- **PPC (z1)**: 1.37
- **ln Z (Evidence)**: 0.328
- **PPC (z1 min)**: 2.88
- **Ring fe (16th)**: 2.29
- **err(rho_true)**: 0.1969
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_b_cat1_GoldenSample_ord99672-lnZ_%2B00.33-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P4_T2_corner.png)

![PPC](figures/kepler_51_b_cat1_GoldenSample_ord99672-lnZ_%2B00.33-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P4_T2_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P4_T3
- **PPC (z1)**: 1.29
- **ln Z (Evidence)**: 0.123
- **PPC (z1 min)**: 2.86
- **Ring fe (16th)**: 1.96
- **err(rho_true)**: 0.2049
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_b_cat1_GoldenSample_ord99877-lnZ_%2B00.12-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P4_T3_corner.png)

![PPC](figures/kepler_51_b_cat1_GoldenSample_ord99877-lnZ_%2B00.12-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P4_T3_ppc.png)

---

### Category: [Acceptable] Multimodal Angles

| Rank | Tag | PPC (z1) | ln Z | PPC (z1 min) | Ring fe (16%) | err(rho_true) | Angle Peaks |
|---|---|---|---|---|---|---|---|
| 28 | `kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE` | **1.33** | 2.74 | 2.88 | 4.75 | 0.2114 | 2.5 |
| 29 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P1_T2` | **1.36** | 2.29 | 2.93 | 3.86 | 0.1648 | 2.0 |
| 30 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P3_T3` | **1.28** | 1.42 | 2.91 | 2.29 | 0.1500 | 2.5 |
| 31 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P1_T1` | **1.38** | 0.64 | 2.87 | 4.80 | 0.2004 | 2.5 |
| 32 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P5_T1` | **1.30** | 0.42 | 2.78 | 2.38 | 0.1912 | 2.0 |
| 33 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P7_T2` | **1.33** | 0.31 | 2.82 | 1.49 | 0.2286 | 2.0 |
| 34 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P3_T2` | **1.33** | -0.07 | 2.76 | 2.61 | 0.2222 | 2.0 |

#### kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE
- **PPC (z1)**: 1.33
- **ln Z (Evidence)**: 2.738
- **PPC (z1 min)**: 2.88
- **Ring fe (16th)**: 4.75
- **err(rho_true)**: 0.2114
- **Angle Peaks**: 2.5
- **Category**: [Acceptable] Multimodal Angles

![Corner Plot](figures/kepler_51_b_cat3_MultimodalAngles_ord97262-lnZ_%2B02.74-kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_corner.png)

![PPC](figures/kepler_51_b_cat3_MultimodalAngles_ord97262-lnZ_%2B02.74-kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P1_T2
- **PPC (z1)**: 1.36
- **ln Z (Evidence)**: 2.290
- **PPC (z1 min)**: 2.93
- **Ring fe (16th)**: 3.86
- **err(rho_true)**: 0.1648
- **Angle Peaks**: 2.0
- **Category**: [Acceptable] Multimodal Angles

![Corner Plot](figures/kepler_51_b_cat3_MultimodalAngles_ord97710-lnZ_%2B02.29-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P1_T2_corner.png)

![PPC](figures/kepler_51_b_cat3_MultimodalAngles_ord97710-lnZ_%2B02.29-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P1_T2_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P3_T3
- **PPC (z1)**: 1.28
- **ln Z (Evidence)**: 1.423
- **PPC (z1 min)**: 2.91
- **Ring fe (16th)**: 2.29
- **err(rho_true)**: 0.1500
- **Angle Peaks**: 2.5
- **Category**: [Acceptable] Multimodal Angles

![Corner Plot](figures/kepler_51_b_cat3_MultimodalAngles_ord98577-lnZ_%2B01.42-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P3_T3_corner.png)

![PPC](figures/kepler_51_b_cat3_MultimodalAngles_ord98577-lnZ_%2B01.42-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P3_T3_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P1_T1
- **PPC (z1)**: 1.38
- **ln Z (Evidence)**: 0.645
- **PPC (z1 min)**: 2.87
- **Ring fe (16th)**: 4.80
- **err(rho_true)**: 0.2004
- **Angle Peaks**: 2.5
- **Category**: [Acceptable] Multimodal Angles

![Corner Plot](figures/kepler_51_b_cat3_MultimodalAngles_ord99355-lnZ_%2B00.64-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P1_T1_corner.png)

![PPC](figures/kepler_51_b_cat3_MultimodalAngles_ord99355-lnZ_%2B00.64-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P1_T1_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P5_T1
- **PPC (z1)**: 1.30
- **ln Z (Evidence)**: 0.416
- **PPC (z1 min)**: 2.78
- **Ring fe (16th)**: 2.38
- **err(rho_true)**: 0.1912
- **Angle Peaks**: 2.0
- **Category**: [Acceptable] Multimodal Angles

![Corner Plot](figures/kepler_51_b_cat3_MultimodalAngles_ord99584-lnZ_%2B00.42-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P5_T1_corner.png)

![PPC](figures/kepler_51_b_cat3_MultimodalAngles_ord99584-lnZ_%2B00.42-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P5_T1_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P7_T2
- **PPC (z1)**: 1.33
- **ln Z (Evidence)**: 0.308
- **PPC (z1 min)**: 2.82
- **Ring fe (16th)**: 1.49
- **err(rho_true)**: 0.2286
- **Angle Peaks**: 2.0
- **Category**: [Acceptable] Multimodal Angles

![Corner Plot](figures/kepler_51_b_cat3_MultimodalAngles_ord99692-lnZ_%2B00.31-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P7_T2_corner.png)

![PPC](figures/kepler_51_b_cat3_MultimodalAngles_ord99692-lnZ_%2B00.31-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P7_T2_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P3_T2
- **PPC (z1)**: 1.33
- **ln Z (Evidence)**: -0.070
- **PPC (z1 min)**: 2.76
- **Ring fe (16th)**: 2.61
- **err(rho_true)**: 0.2222
- **Angle Peaks**: 2.0
- **Category**: [Acceptable] Multimodal Angles

![Corner Plot](figures/kepler_51_b_cat3_MultimodalAngles_ord99999-lnZ_-00.07-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P3_T2_corner.png)

![PPC](figures/kepler_51_b_cat3_MultimodalAngles_ord99999-lnZ_-00.07-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P3_T2_ppc.png)

---

### Category: [Rejected] Unphysical Nuisance

| Rank | Tag | PPC (z1) | ln Z | PPC (z1 min) | Ring fe (16%) | err(rho_true) | Angle Peaks |
|---|---|---|---|---|---|---|---|
| 35 | `kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE` | **1.46** | 1.57 | 2.48 | 3.68 | 0.3170 | 1.5 |
| 36 | `kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE` | **1.33** | 1.35 | 2.54 | 4.65 | 0.3189 | 1.0 |
| 37 | `kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE` | **1.88** | 1.17 | 2.43 | 1.19 | 0.3207 | 2.0 |
| 38 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE` | **1.49** | 0.88 | 2.65 | 1.05 | 0.2582 | 1.0 |
| 39 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE` | **1.94** | 0.03 | 2.39 | 1.10 | 0.3183 | 1.5 |
| 40 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE` | **1.49** | -0.04 | 2.61 | 3.77 | 0.3226 | 1.5 |
| 41 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE` | **1.34** | -0.23 | 2.66 | 4.66 | 0.3215 | 1.0 |
| 42 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE` | **1.40** | -0.43 | 2.33 | 1.03 | 0.3220 | 1.0 |

#### kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE
- **PPC (z1)**: 1.46
- **ln Z (Evidence)**: 1.570
- **PPC (z1 min)**: 2.48
- **Ring fe (16th)**: 3.68
- **err(rho_true)**: 0.3170
- **Angle Peaks**: 1.5
- **Category**: [Rejected] Unphysical Nuisance

![Corner Plot](figures/kepler_51_b_cat5_UnphysicalNuisance_ord98430-lnZ_%2B01.57-kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_corner.png)

![PPC](figures/kepler_51_b_cat5_UnphysicalNuisance_ord98430-lnZ_%2B01.57-kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE
- **PPC (z1)**: 1.33
- **ln Z (Evidence)**: 1.353
- **PPC (z1 min)**: 2.54
- **Ring fe (16th)**: 4.65
- **err(rho_true)**: 0.3189
- **Angle Peaks**: 1.0
- **Category**: [Rejected] Unphysical Nuisance

![Corner Plot](figures/kepler_51_b_cat5_UnphysicalNuisance_ord98647-lnZ_%2B01.35-kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_corner.png)

![PPC](figures/kepler_51_b_cat5_UnphysicalNuisance_ord98647-lnZ_%2B01.35-kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE
- **PPC (z1)**: 1.88
- **ln Z (Evidence)**: 1.168
- **PPC (z1 min)**: 2.43
- **Ring fe (16th)**: 1.19
- **err(rho_true)**: 0.3207
- **Angle Peaks**: 2.0
- **Category**: [Rejected] Unphysical Nuisance

![Corner Plot](figures/kepler_51_b_cat5_UnphysicalNuisance_ord98832-lnZ_%2B01.17-kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE_corner.png)

![PPC](figures/kepler_51_b_cat5_UnphysicalNuisance_ord98832-lnZ_%2B01.17-kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE
- **PPC (z1)**: 1.49
- **ln Z (Evidence)**: 0.878
- **PPC (z1 min)**: 2.65
- **Ring fe (16th)**: 1.05
- **err(rho_true)**: 0.2582
- **Angle Peaks**: 1.0
- **Category**: [Rejected] Unphysical Nuisance

![Corner Plot](figures/kepler_51_b_cat5_UnphysicalNuisance_ord99122-lnZ_%2B00.88-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE_corner.png)

![PPC](figures/kepler_51_b_cat5_UnphysicalNuisance_ord99122-lnZ_%2B00.88-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE
- **PPC (z1)**: 1.94
- **ln Z (Evidence)**: 0.029
- **PPC (z1 min)**: 2.39
- **Ring fe (16th)**: 1.10
- **err(rho_true)**: 0.3183
- **Angle Peaks**: 1.5
- **Category**: [Rejected] Unphysical Nuisance

![Corner Plot](figures/kepler_51_b_cat5_UnphysicalNuisance_ord99971-lnZ_%2B00.03-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE_corner.png)

![PPC](figures/kepler_51_b_cat5_UnphysicalNuisance_ord99971-lnZ_%2B00.03-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE
- **PPC (z1)**: 1.49
- **ln Z (Evidence)**: -0.040
- **PPC (z1 min)**: 2.61
- **Ring fe (16th)**: 3.77
- **err(rho_true)**: 0.3226
- **Angle Peaks**: 1.5
- **Category**: [Rejected] Unphysical Nuisance

![Corner Plot](figures/kepler_51_b_cat5_UnphysicalNuisance_ord99999-lnZ_-00.04-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_corner.png)

![PPC](figures/kepler_51_b_cat5_UnphysicalNuisance_ord99999-lnZ_-00.04-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE
- **PPC (z1)**: 1.34
- **ln Z (Evidence)**: -0.228
- **PPC (z1 min)**: 2.66
- **Ring fe (16th)**: 4.66
- **err(rho_true)**: 0.3215
- **Angle Peaks**: 1.0
- **Category**: [Rejected] Unphysical Nuisance

![Corner Plot](figures/kepler_51_b_cat5_UnphysicalNuisance_ord99999-lnZ_-00.23-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_corner.png)

![PPC](figures/kepler_51_b_cat5_UnphysicalNuisance_ord99999-lnZ_-00.23-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE
- **PPC (z1)**: 1.40
- **ln Z (Evidence)**: -0.429
- **PPC (z1 min)**: 2.33
- **Ring fe (16th)**: 1.03
- **err(rho_true)**: 0.3220
- **Angle Peaks**: 1.0
- **Category**: [Rejected] Unphysical Nuisance

![Corner Plot](figures/kepler_51_b_cat5_UnphysicalNuisance_ord99999-lnZ_-00.43-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE_corner.png)

![PPC](figures/kepler_51_b_cat5_UnphysicalNuisance_ord99999-lnZ_-00.43-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE_ppc.png)

---

### Category: [Rejected] Poor Individual Fit

| Rank | Tag | PPC (z1) | ln Z | PPC (z1 min) | Ring fe (16%) | err(rho_true) | Angle Peaks |
|---|---|---|---|---|---|---|---|
| 43 | `kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_tauFREE_pFREE` | **1.28** | 1.79 | 0.95 | 1.75 | N/A | 2.0 |
| 44 | `kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026` | **1.29** | 1.70 | 0.95 | 5.08 | N/A | 1.0 |

#### kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_tauFREE_pFREE
- **PPC (z1)**: 1.28
- **ln Z (Evidence)**: 1.793
- **PPC (z1 min)**: 0.95
- **Ring fe (16th)**: 1.75
- **err(rho_true)**: N/A
- **Angle Peaks**: 2.0
- **Category**: [Rejected] Poor Individual Fit

![Corner Plot](figures/kepler_51_b_cat6_PoorIndividualFit_ord98207-lnZ_%2B01.79-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_tauFREE_pFREE_corner.png)

![PPC](figures/kepler_51_b_cat6_PoorIndividualFit_ord98207-lnZ_%2B01.79-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_tauFREE_pFREE_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026
- **PPC (z1)**: 1.29
- **ln Z (Evidence)**: 1.700
- **PPC (z1 min)**: 0.95
- **Ring fe (16th)**: 5.08
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.0
- **Category**: [Rejected] Poor Individual Fit

![Corner Plot](figures/kepler_51_b_cat6_PoorIndividualFit_ord98300-lnZ_%2B01.70-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_corner.png)

![PPC](figures/kepler_51_b_cat6_PoorIndividualFit_ord98300-lnZ_%2B01.70-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_ppc.png)

---

### Category: [Rejected] Poor Fit

| Rank | Tag | PPC (z1) | ln Z | PPC (z1 min) | Ring fe (16%) | err(rho_true) | Angle Peaks |
|---|---|---|---|---|---|---|---|
| 45 | `kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE` | **0.91** | 2.41 | 1.02 | 5.16 | N/A | 1.5 |
| 46 | `kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE` | **1.08** | 2.10 | 1.02 | 1.56 | 0.0524 | 1.5 |
| 47 | `kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE` | **0.91** | 2.09 | 1.05 | 5.07 | 0.0235 | 1.5 |
| 48 | `kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE` | **0.91** | 2.06 | 1.07 | 4.24 | 0.0509 | 1.0 |
| 49 | `kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE` | **0.89** | 2.02 | 1.07 | 1.61 | 0.0404 | 1.5 |
| 50 | `kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE` | **1.07** | 1.95 | 1.00 | 4.96 | 0.0439 | 1.5 |
| 51 | `kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_pFREE` | **1.08** | 1.90 | 0.99 | 1.79 | N/A | 2.0 |
| 52 | `kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_tauFREE` | **0.80** | 1.85 | 0.95 | 4.28 | N/A | 2.0 |
| 53 | `kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE` | **1.17** | 1.76 | 1.01 | 1.61 | 0.0587 | 1.5 |
| 54 | `kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_pFREE` | **0.79** | 1.74 | 0.95 | 1.75 | N/A | 1.5 |
| 55 | `kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE` | **0.96** | 1.63 | 1.00 | 4.45 | N/A | 1.5 |
| 56 | `kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE` | **1.10** | 1.59 | 0.97 | 4.04 | 0.0268 | 1.5 |
| 57 | `kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE` | **0.95** | 1.52 | 1.08 | 1.24 | 0.0787 | 1.0 |
| 58 | `kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_pFREE` | **0.94** | 1.40 | 1.00 | 1.93 | N/A | 3.0 |
| 59 | `kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE` | **0.52** | -1.08 | 1.97 | 5.56 | N/A | 1.0 |
| 60 | `kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE` | **0.50** | -3.09 | 1.97 | 5.46 | N/A | 1.0 |

#### kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE
- **PPC (z1)**: 0.91
- **ln Z (Evidence)**: 2.406
- **PPC (z1 min)**: 1.02
- **Ring fe (16th)**: 5.16
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.5
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_b_cat7_PoorFit_ord97594-lnZ_%2B02.41-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_corner.png)

![PPC](figures/kepler_51_b_cat7_PoorFit_ord97594-lnZ_%2B02.41-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE
- **PPC (z1)**: 1.08
- **ln Z (Evidence)**: 2.096
- **PPC (z1 min)**: 1.02
- **Ring fe (16th)**: 1.56
- **err(rho_true)**: 0.0524
- **Angle Peaks**: 1.5
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_b_cat7_PoorFit_ord97904-lnZ_%2B02.10-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE_corner.png)

![PPC](figures/kepler_51_b_cat7_PoorFit_ord97904-lnZ_%2B02.10-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE
- **PPC (z1)**: 0.91
- **ln Z (Evidence)**: 2.087
- **PPC (z1 min)**: 1.05
- **Ring fe (16th)**: 5.07
- **err(rho_true)**: 0.0235
- **Angle Peaks**: 1.5
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_b_cat7_PoorFit_ord97913-lnZ_%2B02.09-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_corner.png)

![PPC](figures/kepler_51_b_cat7_PoorFit_ord97913-lnZ_%2B02.09-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE
- **PPC (z1)**: 0.91
- **ln Z (Evidence)**: 2.062
- **PPC (z1 min)**: 1.07
- **Ring fe (16th)**: 4.24
- **err(rho_true)**: 0.0509
- **Angle Peaks**: 1.0
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_b_cat7_PoorFit_ord97938-lnZ_%2B02.06-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_corner.png)

![PPC](figures/kepler_51_b_cat7_PoorFit_ord97938-lnZ_%2B02.06-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE
- **PPC (z1)**: 0.89
- **ln Z (Evidence)**: 2.021
- **PPC (z1 min)**: 1.07
- **Ring fe (16th)**: 1.61
- **err(rho_true)**: 0.0404
- **Angle Peaks**: 1.5
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_b_cat7_PoorFit_ord97979-lnZ_%2B02.02-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE_corner.png)

![PPC](figures/kepler_51_b_cat7_PoorFit_ord97979-lnZ_%2B02.02-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE
- **PPC (z1)**: 1.07
- **ln Z (Evidence)**: 1.947
- **PPC (z1 min)**: 1.00
- **Ring fe (16th)**: 4.96
- **err(rho_true)**: 0.0439
- **Angle Peaks**: 1.5
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_b_cat7_PoorFit_ord98053-lnZ_%2B01.95-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_corner.png)

![PPC](figures/kepler_51_b_cat7_PoorFit_ord98053-lnZ_%2B01.95-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_pFREE
- **PPC (z1)**: 1.08
- **ln Z (Evidence)**: 1.902
- **PPC (z1 min)**: 0.99
- **Ring fe (16th)**: 1.79
- **err(rho_true)**: N/A
- **Angle Peaks**: 2.0
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_b_cat7_PoorFit_ord98098-lnZ_%2B01.90-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_pFREE_corner.png)

![PPC](figures/kepler_51_b_cat7_PoorFit_ord98098-lnZ_%2B01.90-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_pFREE_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_tauFREE
- **PPC (z1)**: 0.80
- **ln Z (Evidence)**: 1.854
- **PPC (z1 min)**: 0.95
- **Ring fe (16th)**: 4.28
- **err(rho_true)**: N/A
- **Angle Peaks**: 2.0
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_b_cat7_PoorFit_ord98146-lnZ_%2B01.85-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_tauFREE_corner.png)

![PPC](figures/kepler_51_b_cat7_PoorFit_ord98146-lnZ_%2B01.85-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_tauFREE_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE
- **PPC (z1)**: 1.17
- **ln Z (Evidence)**: 1.762
- **PPC (z1 min)**: 1.01
- **Ring fe (16th)**: 1.61
- **err(rho_true)**: 0.0587
- **Angle Peaks**: 1.5
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_b_cat7_PoorFit_ord98238-lnZ_%2B01.76-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE_corner.png)

![PPC](figures/kepler_51_b_cat7_PoorFit_ord98238-lnZ_%2B01.76-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_pFREE
- **PPC (z1)**: 0.79
- **ln Z (Evidence)**: 1.735
- **PPC (z1 min)**: 0.95
- **Ring fe (16th)**: 1.75
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.5
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_b_cat7_PoorFit_ord98265-lnZ_%2B01.74-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_pFREE_corner.png)

![PPC](figures/kepler_51_b_cat7_PoorFit_ord98265-lnZ_%2B01.74-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_pFREE_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE
- **PPC (z1)**: 0.96
- **ln Z (Evidence)**: 1.633
- **PPC (z1 min)**: 1.00
- **Ring fe (16th)**: 4.45
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.5
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_b_cat7_PoorFit_ord98367-lnZ_%2B01.63-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_corner.png)

![PPC](figures/kepler_51_b_cat7_PoorFit_ord98367-lnZ_%2B01.63-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE
- **PPC (z1)**: 1.10
- **ln Z (Evidence)**: 1.589
- **PPC (z1 min)**: 0.97
- **Ring fe (16th)**: 4.04
- **err(rho_true)**: 0.0268
- **Angle Peaks**: 1.5
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_b_cat7_PoorFit_ord98411-lnZ_%2B01.59-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_corner.png)

![PPC](figures/kepler_51_b_cat7_PoorFit_ord98411-lnZ_%2B01.59-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE
- **PPC (z1)**: 0.95
- **ln Z (Evidence)**: 1.524
- **PPC (z1 min)**: 1.08
- **Ring fe (16th)**: 1.24
- **err(rho_true)**: 0.0787
- **Angle Peaks**: 1.0
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_b_cat7_PoorFit_ord98476-lnZ_%2B01.52-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE_corner.png)

![PPC](figures/kepler_51_b_cat7_PoorFit_ord98476-lnZ_%2B01.52-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_pFREE
- **PPC (z1)**: 0.94
- **ln Z (Evidence)**: 1.404
- **PPC (z1 min)**: 1.00
- **Ring fe (16th)**: 1.93
- **err(rho_true)**: N/A
- **Angle Peaks**: 3.0
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_b_cat7_PoorFit_ord98596-lnZ_%2B01.40-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_pFREE_corner.png)

![PPC](figures/kepler_51_b_cat7_PoorFit_ord98596-lnZ_%2B01.40-kepler_51_b_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_pFREE_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE
- **PPC (z1)**: 0.52
- **ln Z (Evidence)**: -1.083
- **PPC (z1 min)**: 1.97
- **Ring fe (16th)**: 5.56
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.0
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_b_cat7_PoorFit_ord99999-lnZ_-01.08-kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_corner.png)

![PPC](figures/kepler_51_b_cat7_PoorFit_ord99999-lnZ_-01.08-kepler_51_b_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_ppc.png)

---

#### kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE
- **PPC (z1)**: 0.50
- **ln Z (Evidence)**: -3.089
- **PPC (z1 min)**: 1.97
- **Ring fe (16th)**: 5.46
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.0
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_b_cat7_PoorFit_ord99999-lnZ_-03.09-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_corner.png)

![PPC](figures/kepler_51_b_cat7_PoorFit_ord99999-lnZ_-03.09-kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_ppc.png)

---
