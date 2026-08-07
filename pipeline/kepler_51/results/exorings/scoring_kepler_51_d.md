# Kepler_51 D Retrievals Classification Report

This report groups retrievals into strict physical categories based on a Decision Tree logic. Within each category, retrievals are ranked by their Bayesian Evidence ($\ln \mathcal{Z}$).

## Category Summary
- **[Excellent] Golden Sample**: 34 retrievals
- **[Acceptable] Low Bayesian Evidence**: 2 retrievals
- **[Acceptable] Multimodal Angles**: 10 retrievals
- **[Rejected] Unphysical Nuisance**: 8 retrievals
- **[Rejected] Poor Fit**: 13 retrievals

## Detailed Results

### Category: [Excellent] Golden Sample

| Rank | Tag | PPC (z1) | ln Z | PPC (z1 min) | Ring fe (16%) | err(rho_true) | Angle Peaks |
|---|---|---|---|---|---|---|---|
| 1 | `kepler_51_d_NS_exorings_kde_delta-T14-T23-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE` | **1.67** | 6.51 | 2.75 | 1.29 | 0.1627 | 1.5 |
| 2 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE` | **1.20** | 2.28 | 1.10 | 6.75 | N/A | 1.5 |
| 3 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE` | **1.30** | 2.24 | 1.19 | 5.16 | 0.0693 | 1.0 |
| 4 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P9_T1` | **1.70** | 2.07 | 2.21 | 1.24 | 0.1813 | 1.0 |
| 5 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE` | **1.32** | 2.04 | 1.20 | 1.14 | 0.0704 | 1.5 |
| 6 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE` | **1.30** | 2.03 | 1.12 | 6.58 | 0.0321 | 1.5 |
| 7 | `kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE` | **1.65** | 2.01 | 2.89 | 1.07 | 0.1295 | 1.5 |
| 8 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P3_T3` | **2.15** | 1.92 | 2.67 | 2.47 | 0.1324 | 1.5 |
| 9 | `kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE` | **2.23** | 1.82 | 2.65 | 1.40 | 0.1366 | 1.5 |
| 10 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P9_T2` | **2.03** | 1.82 | 2.46 | 1.19 | 0.1868 | 1.0 |
| 11 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P9_T3` | **1.78** | 1.80 | 2.28 | 1.16 | 0.1682 | 1.0 |
| 12 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE` | **1.88** | 1.71 | 3.12 | 1.17 | 0.1457 | 1.5 |
| 13 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P8_T1` | **2.16** | 1.65 | 3.08 | 1.70 | 0.1743 | 1.5 |
| 14 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE` | **1.60** | 1.64 | 2.67 | 5.12 | 0.1672 | 1.0 |
| 15 | `kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE` | **1.46** | 1.64 | 2.60 | 7.11 | N/A | 1.0 |
| 16 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P3_T2` | **1.66** | 1.60 | 2.78 | 2.84 | 0.1659 | 1.0 |
| 17 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P1_T2` | **1.66** | 1.35 | 2.83 | 4.75 | 0.1745 | 1.5 |
| 18 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE` | **1.53** | 1.34 | 2.62 | 6.40 | 0.1642 | 1.5 |
| 19 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P6_T3` | **1.67** | 1.31 | 2.69 | 1.54 | 0.1415 | 1.5 |
| 20 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE` | **1.36** | 1.19 | 2.31 | 7.10 | N/A | 1.5 |
| 21 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P4_T2` | **1.65** | 1.16 | 2.71 | 2.38 | 0.1669 | 1.5 |
| 22 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P2_T2` | **1.75** | 1.12 | 2.89 | 3.52 | 0.1578 | 1.5 |
| 23 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P8_T2` | **1.68** | 1.01 | 2.82 | 1.47 | 0.1747 | 1.5 |
| 24 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P1_T3` | **1.60** | 0.98 | 2.71 | 3.79 | 0.1814 | 1.5 |
| 25 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P7_T2` | **1.66** | 0.90 | 2.77 | 1.53 | 0.1263 | 1.5 |
| 26 | `kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE` | **1.51** | 0.88 | 2.47 | 5.42 | N/A | 1.0 |
| 27 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE` | **1.46** | 0.76 | 2.36 | 5.45 | N/A | 1.0 |
| 28 | `kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_pFREE` | **1.44** | 0.73 | 2.43 | 2.63 | N/A | 1.0 |
| 29 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P1_T1` | **1.45** | 0.70 | 2.37 | 6.03 | 0.1216 | 1.0 |
| 30 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P5_T3` | **2.14** | 0.62 | 2.89 | 1.77 | 0.1455 | 1.5 |
| 31 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P6_T1` | **1.83** | 0.61 | 2.99 | 2.12 | 0.1723 | 1.5 |
| 32 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P7_T3` | **1.67** | 0.41 | 2.29 | 1.32 | 0.1787 | 1.5 |
| 33 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P2_T1` | **1.64** | 0.37 | 2.71 | 4.59 | 0.1096 | 1.5 |
| 34 | `kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_pFREE` | **1.29** | 0.19 | 2.19 | 1.37 | N/A | 1.0 |

#### kepler_51_d_NS_exorings_kde_delta-T14-T23-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE
- **PPC (z1)**: 1.67
- **ln Z (Evidence)**: 6.508
- **PPC (z1 min)**: 2.75
- **Ring fe (16th)**: 1.29
- **err(rho_true)**: 0.1627
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord93492-lnZ_%2B06.51-kepler_51_d_NS_exorings_kde_delta-T14-T23-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord93492-lnZ_%2B06.51-kepler_51_d_NS_exorings_kde_delta-T14-T23-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE
- **PPC (z1)**: 1.20
- **ln Z (Evidence)**: 2.285
- **PPC (z1 min)**: 1.10
- **Ring fe (16th)**: 6.75
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord97715-lnZ_%2B02.28-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord97715-lnZ_%2B02.28-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE
- **PPC (z1)**: 1.30
- **ln Z (Evidence)**: 2.244
- **PPC (z1 min)**: 1.19
- **Ring fe (16th)**: 5.16
- **err(rho_true)**: 0.0693
- **Angle Peaks**: 1.0
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord97756-lnZ_%2B02.24-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord97756-lnZ_%2B02.24-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P9_T1
- **PPC (z1)**: 1.70
- **ln Z (Evidence)**: 2.065
- **PPC (z1 min)**: 2.21
- **Ring fe (16th)**: 1.24
- **err(rho_true)**: 0.1813
- **Angle Peaks**: 1.0
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord97935-lnZ_%2B02.07-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P9_T1_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord97935-lnZ_%2B02.07-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P9_T1_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE
- **PPC (z1)**: 1.32
- **ln Z (Evidence)**: 2.038
- **PPC (z1 min)**: 1.20
- **Ring fe (16th)**: 1.14
- **err(rho_true)**: 0.0704
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord97962-lnZ_%2B02.04-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord97962-lnZ_%2B02.04-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE
- **PPC (z1)**: 1.30
- **ln Z (Evidence)**: 2.029
- **PPC (z1 min)**: 1.12
- **Ring fe (16th)**: 6.58
- **err(rho_true)**: 0.0321
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord97971-lnZ_%2B02.03-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord97971-lnZ_%2B02.03-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE
- **PPC (z1)**: 1.65
- **ln Z (Evidence)**: 2.009
- **PPC (z1 min)**: 2.89
- **Ring fe (16th)**: 1.07
- **err(rho_true)**: 0.1295
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord97991-lnZ_%2B02.01-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord97991-lnZ_%2B02.01-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P3_T3
- **PPC (z1)**: 2.15
- **ln Z (Evidence)**: 1.920
- **PPC (z1 min)**: 2.67
- **Ring fe (16th)**: 2.47
- **err(rho_true)**: 0.1324
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord98080-lnZ_%2B01.92-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P3_T3_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord98080-lnZ_%2B01.92-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P3_T3_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE
- **PPC (z1)**: 2.23
- **ln Z (Evidence)**: 1.822
- **PPC (z1 min)**: 2.65
- **Ring fe (16th)**: 1.40
- **err(rho_true)**: 0.1366
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord98178-lnZ_%2B01.82-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord98178-lnZ_%2B01.82-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P9_T2
- **PPC (z1)**: 2.03
- **ln Z (Evidence)**: 1.821
- **PPC (z1 min)**: 2.46
- **Ring fe (16th)**: 1.19
- **err(rho_true)**: 0.1868
- **Angle Peaks**: 1.0
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord98179-lnZ_%2B01.82-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P9_T2_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord98179-lnZ_%2B01.82-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P9_T2_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P9_T3
- **PPC (z1)**: 1.78
- **ln Z (Evidence)**: 1.805
- **PPC (z1 min)**: 2.28
- **Ring fe (16th)**: 1.16
- **err(rho_true)**: 0.1682
- **Angle Peaks**: 1.0
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord98195-lnZ_%2B01.80-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P9_T3_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord98195-lnZ_%2B01.80-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P9_T3_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE
- **PPC (z1)**: 1.88
- **ln Z (Evidence)**: 1.711
- **PPC (z1 min)**: 3.12
- **Ring fe (16th)**: 1.17
- **err(rho_true)**: 0.1457
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord98289-lnZ_%2B01.71-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord98289-lnZ_%2B01.71-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P8_T1
- **PPC (z1)**: 2.16
- **ln Z (Evidence)**: 1.654
- **PPC (z1 min)**: 3.08
- **Ring fe (16th)**: 1.70
- **err(rho_true)**: 0.1743
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord98346-lnZ_%2B01.65-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P8_T1_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord98346-lnZ_%2B01.65-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P8_T1_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE
- **PPC (z1)**: 1.60
- **ln Z (Evidence)**: 1.641
- **PPC (z1 min)**: 2.67
- **Ring fe (16th)**: 5.12
- **err(rho_true)**: 0.1672
- **Angle Peaks**: 1.0
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord98359-lnZ_%2B01.64-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord98359-lnZ_%2B01.64-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE
- **PPC (z1)**: 1.46
- **ln Z (Evidence)**: 1.640
- **PPC (z1 min)**: 2.60
- **Ring fe (16th)**: 7.11
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.0
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord98360-lnZ_%2B01.64-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord98360-lnZ_%2B01.64-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P3_T2
- **PPC (z1)**: 1.66
- **ln Z (Evidence)**: 1.596
- **PPC (z1 min)**: 2.78
- **Ring fe (16th)**: 2.84
- **err(rho_true)**: 0.1659
- **Angle Peaks**: 1.0
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord98404-lnZ_%2B01.60-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P3_T2_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord98404-lnZ_%2B01.60-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P3_T2_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P1_T2
- **PPC (z1)**: 1.66
- **ln Z (Evidence)**: 1.345
- **PPC (z1 min)**: 2.83
- **Ring fe (16th)**: 4.75
- **err(rho_true)**: 0.1745
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord98655-lnZ_%2B01.35-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P1_T2_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord98655-lnZ_%2B01.35-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P1_T2_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE
- **PPC (z1)**: 1.53
- **ln Z (Evidence)**: 1.343
- **PPC (z1 min)**: 2.62
- **Ring fe (16th)**: 6.40
- **err(rho_true)**: 0.1642
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord98657-lnZ_%2B01.34-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord98657-lnZ_%2B01.34-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P6_T3
- **PPC (z1)**: 1.67
- **ln Z (Evidence)**: 1.307
- **PPC (z1 min)**: 2.69
- **Ring fe (16th)**: 1.54
- **err(rho_true)**: 0.1415
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord98693-lnZ_%2B01.31-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P6_T3_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord98693-lnZ_%2B01.31-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P6_T3_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE
- **PPC (z1)**: 1.36
- **ln Z (Evidence)**: 1.192
- **PPC (z1 min)**: 2.31
- **Ring fe (16th)**: 7.10
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord98808-lnZ_%2B01.19-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord98808-lnZ_%2B01.19-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P4_T2
- **PPC (z1)**: 1.65
- **ln Z (Evidence)**: 1.161
- **PPC (z1 min)**: 2.71
- **Ring fe (16th)**: 2.38
- **err(rho_true)**: 0.1669
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord98839-lnZ_%2B01.16-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P4_T2_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord98839-lnZ_%2B01.16-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P4_T2_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P2_T2
- **PPC (z1)**: 1.75
- **ln Z (Evidence)**: 1.118
- **PPC (z1 min)**: 2.89
- **Ring fe (16th)**: 3.52
- **err(rho_true)**: 0.1578
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord98882-lnZ_%2B01.12-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P2_T2_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord98882-lnZ_%2B01.12-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P2_T2_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P8_T2
- **PPC (z1)**: 1.68
- **ln Z (Evidence)**: 1.013
- **PPC (z1 min)**: 2.82
- **Ring fe (16th)**: 1.47
- **err(rho_true)**: 0.1747
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord98987-lnZ_%2B01.01-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P8_T2_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord98987-lnZ_%2B01.01-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P8_T2_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P1_T3
- **PPC (z1)**: 1.60
- **ln Z (Evidence)**: 0.984
- **PPC (z1 min)**: 2.71
- **Ring fe (16th)**: 3.79
- **err(rho_true)**: 0.1814
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord99016-lnZ_%2B00.98-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P1_T3_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord99016-lnZ_%2B00.98-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P1_T3_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P7_T2
- **PPC (z1)**: 1.66
- **ln Z (Evidence)**: 0.898
- **PPC (z1 min)**: 2.77
- **Ring fe (16th)**: 1.53
- **err(rho_true)**: 0.1263
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord99102-lnZ_%2B00.90-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P7_T2_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord99102-lnZ_%2B00.90-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P7_T2_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE
- **PPC (z1)**: 1.51
- **ln Z (Evidence)**: 0.878
- **PPC (z1 min)**: 2.47
- **Ring fe (16th)**: 5.42
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.0
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord99122-lnZ_%2B00.88-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord99122-lnZ_%2B00.88-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE
- **PPC (z1)**: 1.46
- **ln Z (Evidence)**: 0.761
- **PPC (z1 min)**: 2.36
- **Ring fe (16th)**: 5.45
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.0
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord99239-lnZ_%2B00.76-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord99239-lnZ_%2B00.76-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_pFREE
- **PPC (z1)**: 1.44
- **ln Z (Evidence)**: 0.727
- **PPC (z1 min)**: 2.43
- **Ring fe (16th)**: 2.63
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.0
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord99273-lnZ_%2B00.73-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord99273-lnZ_%2B00.73-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P1_T1
- **PPC (z1)**: 1.45
- **ln Z (Evidence)**: 0.697
- **PPC (z1 min)**: 2.37
- **Ring fe (16th)**: 6.03
- **err(rho_true)**: 0.1216
- **Angle Peaks**: 1.0
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord99303-lnZ_%2B00.70-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P1_T1_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord99303-lnZ_%2B00.70-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P1_T1_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P5_T3
- **PPC (z1)**: 2.14
- **ln Z (Evidence)**: 0.624
- **PPC (z1 min)**: 2.89
- **Ring fe (16th)**: 1.77
- **err(rho_true)**: 0.1455
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord99376-lnZ_%2B00.62-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P5_T3_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord99376-lnZ_%2B00.62-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P5_T3_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P6_T1
- **PPC (z1)**: 1.83
- **ln Z (Evidence)**: 0.607
- **PPC (z1 min)**: 2.99
- **Ring fe (16th)**: 2.12
- **err(rho_true)**: 0.1723
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord99393-lnZ_%2B00.61-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P6_T1_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord99393-lnZ_%2B00.61-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P6_T1_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P7_T3
- **PPC (z1)**: 1.67
- **ln Z (Evidence)**: 0.414
- **PPC (z1 min)**: 2.29
- **Ring fe (16th)**: 1.32
- **err(rho_true)**: 0.1787
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord99586-lnZ_%2B00.41-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P7_T3_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord99586-lnZ_%2B00.41-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P7_T3_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P2_T1
- **PPC (z1)**: 1.64
- **ln Z (Evidence)**: 0.368
- **PPC (z1 min)**: 2.71
- **Ring fe (16th)**: 4.59
- **err(rho_true)**: 0.1096
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord99632-lnZ_%2B00.37-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P2_T1_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord99632-lnZ_%2B00.37-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P2_T1_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_pFREE
- **PPC (z1)**: 1.29
- **ln Z (Evidence)**: 0.195
- **PPC (z1 min)**: 2.19
- **Ring fe (16th)**: 1.37
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.0
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_cat1_GoldenSample_ord99805-lnZ_%2B00.19-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_cat1_GoldenSample_ord99805-lnZ_%2B00.19-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_pFREE_ppc.png)

---

### Category: [Acceptable] Low Bayesian Evidence

| Rank | Tag | PPC (z1) | ln Z | PPC (z1 min) | Ring fe (16%) | err(rho_true) | Angle Peaks |
|---|---|---|---|---|---|---|---|
| 35 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_pFREE` | **1.61** | -0.04 | 2.76 | 2.42 | N/A | 1.0 |
| 36 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P5_T1` | **1.68** | -0.23 | 2.92 | 2.49 | 0.2101 | 1.5 |

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_pFREE
- **PPC (z1)**: 1.61
- **ln Z (Evidence)**: -0.039
- **PPC (z1 min)**: 2.76
- **Ring fe (16th)**: 2.42
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.0
- **Category**: [Acceptable] Low Bayesian Evidence

![Corner Plot](figures/kepler_51_d_cat2_LowEvidence_ord99999-lnZ_-00.04-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_cat2_LowEvidence_ord99999-lnZ_-00.04-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P5_T1
- **PPC (z1)**: 1.68
- **ln Z (Evidence)**: -0.225
- **PPC (z1 min)**: 2.92
- **Ring fe (16th)**: 2.49
- **err(rho_true)**: 0.2101
- **Angle Peaks**: 1.5
- **Category**: [Acceptable] Low Bayesian Evidence

![Corner Plot](figures/kepler_51_d_cat2_LowEvidence_ord99999-lnZ_-00.23-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P5_T1_corner.png)

![PPC](figures/kepler_51_d_cat2_LowEvidence_ord99999-lnZ_-00.23-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P5_T1_ppc.png)

---

### Category: [Acceptable] Multimodal Angles

| Rank | Tag | PPC (z1) | ln Z | PPC (z1 min) | Ring fe (16%) | err(rho_true) | Angle Peaks |
|---|---|---|---|---|---|---|---|
| 37 | `kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE` | **1.90** | 2.30 | 2.63 | 5.21 | 0.1729 | 2.0 |
| 38 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE` | **1.75** | 1.93 | 2.98 | 1.06 | 0.1474 | 2.0 |
| 39 | `kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE` | **1.65** | 1.62 | 2.76 | 6.29 | 0.1918 | 2.5 |
| 40 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P8_T3` | **1.89** | 1.30 | 2.47 | 1.37 | 0.1972 | 2.0 |
| 41 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P6_T2` | **1.75** | 1.26 | 2.90 | 1.69 | 0.2085 | 2.0 |
| 42 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P4_T3` | **1.65** | 1.22 | 2.91 | 2.03 | 0.1876 | 2.0 |
| 43 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P4_T1` | **1.53** | 1.15 | 2.51 | 3.00 | 0.1387 | 2.0 |
| 44 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P2_T3` | **1.75** | 0.70 | 2.96 | 2.97 | 0.1576 | 2.0 |
| 45 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P3_T1` | **1.57** | 0.65 | 2.70 | 3.63 | 0.1419 | 2.5 |
| 46 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P7_T1` | **1.61** | 0.27 | 2.68 | 1.82 | 0.1429 | 2.5 |

#### kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE
- **PPC (z1)**: 1.90
- **ln Z (Evidence)**: 2.299
- **PPC (z1 min)**: 2.63
- **Ring fe (16th)**: 5.21
- **err(rho_true)**: 0.1729
- **Angle Peaks**: 2.0
- **Category**: [Acceptable] Multimodal Angles

![Corner Plot](figures/kepler_51_d_cat3_MultimodalAngles_ord97701-lnZ_%2B02.30-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_corner.png)

![PPC](figures/kepler_51_d_cat3_MultimodalAngles_ord97701-lnZ_%2B02.30-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE
- **PPC (z1)**: 1.75
- **ln Z (Evidence)**: 1.928
- **PPC (z1 min)**: 2.98
- **Ring fe (16th)**: 1.06
- **err(rho_true)**: 0.1474
- **Angle Peaks**: 2.0
- **Category**: [Acceptable] Multimodal Angles

![Corner Plot](figures/kepler_51_d_cat3_MultimodalAngles_ord98072-lnZ_%2B01.93-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_cat3_MultimodalAngles_ord98072-lnZ_%2B01.93-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE
- **PPC (z1)**: 1.65
- **ln Z (Evidence)**: 1.624
- **PPC (z1 min)**: 2.76
- **Ring fe (16th)**: 6.29
- **err(rho_true)**: 0.1918
- **Angle Peaks**: 2.5
- **Category**: [Acceptable] Multimodal Angles

![Corner Plot](figures/kepler_51_d_cat3_MultimodalAngles_ord98376-lnZ_%2B01.62-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_corner.png)

![PPC](figures/kepler_51_d_cat3_MultimodalAngles_ord98376-lnZ_%2B01.62-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P8_T3
- **PPC (z1)**: 1.89
- **ln Z (Evidence)**: 1.298
- **PPC (z1 min)**: 2.47
- **Ring fe (16th)**: 1.37
- **err(rho_true)**: 0.1972
- **Angle Peaks**: 2.0
- **Category**: [Acceptable] Multimodal Angles

![Corner Plot](figures/kepler_51_d_cat3_MultimodalAngles_ord98702-lnZ_%2B01.30-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P8_T3_corner.png)

![PPC](figures/kepler_51_d_cat3_MultimodalAngles_ord98702-lnZ_%2B01.30-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P8_T3_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P6_T2
- **PPC (z1)**: 1.75
- **ln Z (Evidence)**: 1.256
- **PPC (z1 min)**: 2.90
- **Ring fe (16th)**: 1.69
- **err(rho_true)**: 0.2085
- **Angle Peaks**: 2.0
- **Category**: [Acceptable] Multimodal Angles

![Corner Plot](figures/kepler_51_d_cat3_MultimodalAngles_ord98744-lnZ_%2B01.26-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P6_T2_corner.png)

![PPC](figures/kepler_51_d_cat3_MultimodalAngles_ord98744-lnZ_%2B01.26-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P6_T2_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P4_T3
- **PPC (z1)**: 1.65
- **ln Z (Evidence)**: 1.221
- **PPC (z1 min)**: 2.91
- **Ring fe (16th)**: 2.03
- **err(rho_true)**: 0.1876
- **Angle Peaks**: 2.0
- **Category**: [Acceptable] Multimodal Angles

![Corner Plot](figures/kepler_51_d_cat3_MultimodalAngles_ord98779-lnZ_%2B01.22-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P4_T3_corner.png)

![PPC](figures/kepler_51_d_cat3_MultimodalAngles_ord98779-lnZ_%2B01.22-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P4_T3_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P4_T1
- **PPC (z1)**: 1.53
- **ln Z (Evidence)**: 1.150
- **PPC (z1 min)**: 2.51
- **Ring fe (16th)**: 3.00
- **err(rho_true)**: 0.1387
- **Angle Peaks**: 2.0
- **Category**: [Acceptable] Multimodal Angles

![Corner Plot](figures/kepler_51_d_cat3_MultimodalAngles_ord98850-lnZ_%2B01.15-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P4_T1_corner.png)

![PPC](figures/kepler_51_d_cat3_MultimodalAngles_ord98850-lnZ_%2B01.15-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P4_T1_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P2_T3
- **PPC (z1)**: 1.75
- **ln Z (Evidence)**: 0.695
- **PPC (z1 min)**: 2.96
- **Ring fe (16th)**: 2.97
- **err(rho_true)**: 0.1576
- **Angle Peaks**: 2.0
- **Category**: [Acceptable] Multimodal Angles

![Corner Plot](figures/kepler_51_d_cat3_MultimodalAngles_ord99305-lnZ_%2B00.70-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P2_T3_corner.png)

![PPC](figures/kepler_51_d_cat3_MultimodalAngles_ord99305-lnZ_%2B00.70-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P2_T3_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P3_T1
- **PPC (z1)**: 1.57
- **ln Z (Evidence)**: 0.652
- **PPC (z1 min)**: 2.70
- **Ring fe (16th)**: 3.63
- **err(rho_true)**: 0.1419
- **Angle Peaks**: 2.5
- **Category**: [Acceptable] Multimodal Angles

![Corner Plot](figures/kepler_51_d_cat3_MultimodalAngles_ord99348-lnZ_%2B00.65-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P3_T1_corner.png)

![PPC](figures/kepler_51_d_cat3_MultimodalAngles_ord99348-lnZ_%2B00.65-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P3_T1_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P7_T1
- **PPC (z1)**: 1.61
- **ln Z (Evidence)**: 0.267
- **PPC (z1 min)**: 2.68
- **Ring fe (16th)**: 1.82
- **err(rho_true)**: 0.1429
- **Angle Peaks**: 2.5
- **Category**: [Acceptable] Multimodal Angles

![Corner Plot](figures/kepler_51_d_cat3_MultimodalAngles_ord99733-lnZ_%2B00.27-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P7_T1_corner.png)

![PPC](figures/kepler_51_d_cat3_MultimodalAngles_ord99733-lnZ_%2B00.27-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_P7_T1_ppc.png)

---

### Category: [Rejected] Unphysical Nuisance

| Rank | Tag | PPC (z1) | ln Z | PPC (z1 min) | Ring fe (16%) | err(rho_true) | Angle Peaks |
|---|---|---|---|---|---|---|---|
| 47 | `kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE` | **1.62** | 0.91 | 2.12 | 5.03 | 0.2842 | 1.0 |
| 48 | `kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE` | **1.70** | 0.83 | 2.09 | 1.17 | 0.2829 | 1.5 |
| 49 | `kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE` | **1.97** | 0.78 | 2.56 | 6.22 | 0.2868 | 1.5 |
| 50 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE` | **1.59** | 0.72 | 2.14 | 4.92 | 0.2846 | 1.0 |
| 51 | `kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE` | **1.80** | 0.20 | 2.11 | 1.62 | 0.2864 | 2.0 |
| 52 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE` | **1.94** | -0.00 | 2.69 | 1.47 | 0.2884 | 1.5 |
| 53 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE` | **1.69** | -0.09 | 2.73 | 6.19 | 0.2893 | 1.0 |
| 54 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE` | **1.72** | -0.36 | 2.24 | 2.30 | 0.2841 | 2.0 |

#### kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE
- **PPC (z1)**: 1.62
- **ln Z (Evidence)**: 0.915
- **PPC (z1 min)**: 2.12
- **Ring fe (16th)**: 5.03
- **err(rho_true)**: 0.2842
- **Angle Peaks**: 1.0
- **Category**: [Rejected] Unphysical Nuisance

![Corner Plot](figures/kepler_51_d_cat5_UnphysicalNuisance_ord99085-lnZ_%2B00.91-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_corner.png)

![PPC](figures/kepler_51_d_cat5_UnphysicalNuisance_ord99085-lnZ_%2B00.91-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE
- **PPC (z1)**: 1.70
- **ln Z (Evidence)**: 0.835
- **PPC (z1 min)**: 2.09
- **Ring fe (16th)**: 1.17
- **err(rho_true)**: 0.2829
- **Angle Peaks**: 1.5
- **Category**: [Rejected] Unphysical Nuisance

![Corner Plot](figures/kepler_51_d_cat5_UnphysicalNuisance_ord99165-lnZ_%2B00.83-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_cat5_UnphysicalNuisance_ord99165-lnZ_%2B00.83-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE
- **PPC (z1)**: 1.97
- **ln Z (Evidence)**: 0.777
- **PPC (z1 min)**: 2.56
- **Ring fe (16th)**: 6.22
- **err(rho_true)**: 0.2868
- **Angle Peaks**: 1.5
- **Category**: [Rejected] Unphysical Nuisance

![Corner Plot](figures/kepler_51_d_cat5_UnphysicalNuisance_ord99223-lnZ_%2B00.78-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_corner.png)

![PPC](figures/kepler_51_d_cat5_UnphysicalNuisance_ord99223-lnZ_%2B00.78-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE
- **PPC (z1)**: 1.59
- **ln Z (Evidence)**: 0.718
- **PPC (z1 min)**: 2.14
- **Ring fe (16th)**: 4.92
- **err(rho_true)**: 0.2846
- **Angle Peaks**: 1.0
- **Category**: [Rejected] Unphysical Nuisance

![Corner Plot](figures/kepler_51_d_cat5_UnphysicalNuisance_ord99282-lnZ_%2B00.72-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_corner.png)

![PPC](figures/kepler_51_d_cat5_UnphysicalNuisance_ord99282-lnZ_%2B00.72-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE
- **PPC (z1)**: 1.80
- **ln Z (Evidence)**: 0.196
- **PPC (z1 min)**: 2.11
- **Ring fe (16th)**: 1.62
- **err(rho_true)**: 0.2864
- **Angle Peaks**: 2.0
- **Category**: [Rejected] Unphysical Nuisance

![Corner Plot](figures/kepler_51_d_cat5_UnphysicalNuisance_ord99804-lnZ_%2B00.20-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_cat5_UnphysicalNuisance_ord99804-lnZ_%2B00.20-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE
- **PPC (z1)**: 1.94
- **ln Z (Evidence)**: -0.000
- **PPC (z1 min)**: 2.69
- **Ring fe (16th)**: 1.47
- **err(rho_true)**: 0.2884
- **Angle Peaks**: 1.5
- **Category**: [Rejected] Unphysical Nuisance

![Corner Plot](figures/kepler_51_d_cat5_UnphysicalNuisance_ord99999-lnZ_-00.00-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_cat5_UnphysicalNuisance_ord99999-lnZ_-00.00-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE
- **PPC (z1)**: 1.69
- **ln Z (Evidence)**: -0.094
- **PPC (z1 min)**: 2.73
- **Ring fe (16th)**: 6.19
- **err(rho_true)**: 0.2893
- **Angle Peaks**: 1.0
- **Category**: [Rejected] Unphysical Nuisance

![Corner Plot](figures/kepler_51_d_cat5_UnphysicalNuisance_ord99999-lnZ_-00.09-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_corner.png)

![PPC](figures/kepler_51_d_cat5_UnphysicalNuisance_ord99999-lnZ_-00.09-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE
- **PPC (z1)**: 1.72
- **ln Z (Evidence)**: -0.364
- **PPC (z1 min)**: 2.24
- **Ring fe (16th)**: 2.30
- **err(rho_true)**: 0.2841
- **Angle Peaks**: 2.0
- **Category**: [Rejected] Unphysical Nuisance

![Corner Plot](figures/kepler_51_d_cat5_UnphysicalNuisance_ord99999-lnZ_-00.36-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_cat5_UnphysicalNuisance_ord99999-lnZ_-00.36-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE_ppc.png)

---

### Category: [Rejected] Poor Fit

| Rank | Tag | PPC (z1) | ln Z | PPC (z1 min) | Ring fe (16%) | err(rho_true) | Angle Peaks |
|---|---|---|---|---|---|---|---|
| 55 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE` | **1.19** | 2.33 | 1.20 | 1.19 | 0.0815 | 1.0 |
| 56 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_pFREE` | **1.00** | 2.19 | 1.07 | 1.27 | N/A | 1.0 |
| 57 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE` | **1.10** | 2.04 | 1.03 | 6.50 | 0.0495 | 1.0 |
| 58 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_tauFREE` | **0.82** | 2.03 | 0.97 | 5.31 | N/A | 1.0 |
| 59 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_pFREE` | **0.79** | 2.02 | 0.97 | 1.37 | N/A | 1.5 |
| 60 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE` | **0.97** | 1.99 | 1.00 | 1.21 | 0.0330 | 1.0 |
| 61 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE` | **1.18** | 1.94 | 1.10 | 5.35 | N/A | 1.5 |
| 62 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE` | **1.04** | 1.91 | 1.04 | 5.29 | 0.0588 | 1.0 |
| 63 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026` | **0.83** | 1.85 | 0.97 | 6.63 | N/A | 2.0 |
| 64 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_tauFREE_pFREE` | **0.77** | 1.79 | 0.97 | 1.33 | N/A | 1.0 |
| 65 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE` | **1.03** | 1.75 | 1.04 | 1.22 | 0.0493 | 1.5 |
| 66 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_pFREE` | **1.04** | 1.73 | 1.06 | 1.38 | N/A | 1.5 |
| 67 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_pFREE` | **1.17** | 0.03 | 2.09 | 1.56 | N/A | 2.0 |

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE
- **PPC (z1)**: 1.19
- **ln Z (Evidence)**: 2.331
- **PPC (z1 min)**: 1.20
- **Ring fe (16th)**: 1.19
- **err(rho_true)**: 0.0815
- **Angle Peaks**: 1.0
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_d_cat7_PoorFit_ord97669-lnZ_%2B02.33-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_cat7_PoorFit_ord97669-lnZ_%2B02.33-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_pFREE
- **PPC (z1)**: 1.00
- **ln Z (Evidence)**: 2.192
- **PPC (z1 min)**: 1.07
- **Ring fe (16th)**: 1.27
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.0
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_d_cat7_PoorFit_ord97808-lnZ_%2B02.19-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_cat7_PoorFit_ord97808-lnZ_%2B02.19-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE
- **PPC (z1)**: 1.10
- **ln Z (Evidence)**: 2.038
- **PPC (z1 min)**: 1.03
- **Ring fe (16th)**: 6.50
- **err(rho_true)**: 0.0495
- **Angle Peaks**: 1.0
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_d_cat7_PoorFit_ord97962-lnZ_%2B02.04-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_corner.png)

![PPC](figures/kepler_51_d_cat7_PoorFit_ord97962-lnZ_%2B02.04-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_tauFREE
- **PPC (z1)**: 0.82
- **ln Z (Evidence)**: 2.025
- **PPC (z1 min)**: 0.97
- **Ring fe (16th)**: 5.31
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.0
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_d_cat7_PoorFit_ord97975-lnZ_%2B02.03-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_tauFREE_corner.png)

![PPC](figures/kepler_51_d_cat7_PoorFit_ord97975-lnZ_%2B02.03-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_tauFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_pFREE
- **PPC (z1)**: 0.79
- **ln Z (Evidence)**: 2.024
- **PPC (z1 min)**: 0.97
- **Ring fe (16th)**: 1.37
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.5
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_d_cat7_PoorFit_ord97976-lnZ_%2B02.02-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_pFREE_corner.png)

![PPC](figures/kepler_51_d_cat7_PoorFit_ord97976-lnZ_%2B02.02-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE
- **PPC (z1)**: 0.97
- **ln Z (Evidence)**: 1.988
- **PPC (z1 min)**: 1.00
- **Ring fe (16th)**: 1.21
- **err(rho_true)**: 0.0330
- **Angle Peaks**: 1.0
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_d_cat7_PoorFit_ord98012-lnZ_%2B01.99-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_cat7_PoorFit_ord98012-lnZ_%2B01.99-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE
- **PPC (z1)**: 1.18
- **ln Z (Evidence)**: 1.941
- **PPC (z1 min)**: 1.10
- **Ring fe (16th)**: 5.35
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.5
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_d_cat7_PoorFit_ord98059-lnZ_%2B01.94-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_corner.png)

![PPC](figures/kepler_51_d_cat7_PoorFit_ord98059-lnZ_%2B01.94-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE
- **PPC (z1)**: 1.04
- **ln Z (Evidence)**: 1.906
- **PPC (z1 min)**: 1.04
- **Ring fe (16th)**: 5.29
- **err(rho_true)**: 0.0588
- **Angle Peaks**: 1.0
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_d_cat7_PoorFit_ord98094-lnZ_%2B01.91-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_corner.png)

![PPC](figures/kepler_51_d_cat7_PoorFit_ord98094-lnZ_%2B01.91-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026
- **PPC (z1)**: 0.83
- **ln Z (Evidence)**: 1.849
- **PPC (z1 min)**: 0.97
- **Ring fe (16th)**: 6.63
- **err(rho_true)**: N/A
- **Angle Peaks**: 2.0
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_d_cat7_PoorFit_ord98151-lnZ_%2B01.85-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_corner.png)

![PPC](figures/kepler_51_d_cat7_PoorFit_ord98151-lnZ_%2B01.85-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_tauFREE_pFREE
- **PPC (z1)**: 0.77
- **ln Z (Evidence)**: 1.786
- **PPC (z1 min)**: 0.97
- **Ring fe (16th)**: 1.33
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.0
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_d_cat7_PoorFit_ord98214-lnZ_%2B01.79-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_tauFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_cat7_PoorFit_ord98214-lnZ_%2B01.79-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_tauFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE
- **PPC (z1)**: 1.03
- **ln Z (Evidence)**: 1.754
- **PPC (z1 min)**: 1.04
- **Ring fe (16th)**: 1.22
- **err(rho_true)**: 0.0493
- **Angle Peaks**: 1.5
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_d_cat7_PoorFit_ord98246-lnZ_%2B01.75-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_cat7_PoorFit_ord98246-lnZ_%2B01.75-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_pFREE
- **PPC (z1)**: 1.04
- **ln Z (Evidence)**: 1.728
- **PPC (z1 min)**: 1.06
- **Ring fe (16th)**: 1.38
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.5
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_d_cat7_PoorFit_ord98272-lnZ_%2B01.73-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_cat7_PoorFit_ord98272-lnZ_%2B01.73-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_pFREE
- **PPC (z1)**: 1.17
- **ln Z (Evidence)**: 0.029
- **PPC (z1 min)**: 2.09
- **Ring fe (16th)**: 1.56
- **err(rho_true)**: N/A
- **Angle Peaks**: 2.0
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_d_cat7_PoorFit_ord99971-lnZ_%2B00.03-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_cat7_PoorFit_ord99971-lnZ_%2B00.03-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_pFREE_ppc.png)

---
