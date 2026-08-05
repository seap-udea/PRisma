# Kepler_51 D Retrievals Classification Report

This report groups retrievals into strict physical categories based on a Decision Tree logic. Within each category, retrievals are ranked by their PPC ($z_1$) score.

## Category Summary
- **[Excellent] Golden Sample**: 15 retrievals
- **[Acceptable] Multimodal Angles**: 4 retrievals
- **[Rejected] Unphysical Nuisance**: 8 retrievals
- **[Rejected] Poor Fit**: 13 retrievals

## Detailed Results

### Category: [Excellent] Golden Sample

| Rank | Tag | PPC (z1) | PPC (z1 min) | Ring fe (16%) | err(rho_true) | Angle Peaks |
|---|---|---|---|---|---|---|
| 1 | `kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE` | **2.23** | 2.65 | 1.40 | 0.1481 | 1.5 |
| 2 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE` | **1.88** | 3.12 | 1.17 | 0.1472 | 1.5 |
| 3 | `kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE` | **1.65** | 2.89 | 1.07 | 0.1317 | 1.5 |
| 4 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_pFREE` | **1.61** | 2.76 | 2.42 | N/A | 1.5 |
| 5 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE` | **1.60** | 2.67 | 5.12 | 0.1711 | 1.0 |
| 6 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE` | **1.53** | 2.62 | 6.40 | 0.1579 | 1.5 |
| 7 | `kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE` | **1.51** | 2.47 | 5.42 | N/A | 1.0 |
| 8 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE` | **1.46** | 2.36 | 5.45 | N/A | 1.0 |
| 9 | `kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_pFREE` | **1.44** | 2.43 | 2.63 | N/A | 1.5 |
| 10 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE` | **1.36** | 2.31 | 7.10 | N/A | 1.0 |
| 11 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE` | **1.32** | 1.20 | 1.14 | 0.0662 | 1.5 |
| 12 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE` | **1.30** | 1.19 | 5.16 | 0.0677 | 1.0 |
| 13 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE` | **1.30** | 1.12 | 6.58 | 0.0407 | 1.0 |
| 14 | `kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_pFREE` | **1.29** | 2.19 | 1.37 | N/A | 1.0 |
| 15 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE` | **1.20** | 1.10 | 6.75 | N/A | 1.5 |

#### kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE
- **PPC (z1)**: 2.23
- **PPC (z1 min)**: 2.65
- **Ring fe (16th)**: 1.40
- **err(rho_true)**: 0.1481
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_ord97772-z1_02.23-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_ord97772-z1_02.23-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE
- **PPC (z1)**: 1.88
- **PPC (z1 min)**: 3.12
- **Ring fe (16th)**: 1.17
- **err(rho_true)**: 0.1472
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_ord98115-z1_01.88-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_ord98115-z1_01.88-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE
- **PPC (z1)**: 1.65
- **PPC (z1 min)**: 2.89
- **Ring fe (16th)**: 1.07
- **err(rho_true)**: 0.1317
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_ord98346-z1_01.65-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_ord98346-z1_01.65-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_pFREE
- **PPC (z1)**: 1.61
- **PPC (z1 min)**: 2.76
- **Ring fe (16th)**: 2.42
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_ord98387-z1_01.61-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_ord98387-z1_01.61-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE
- **PPC (z1)**: 1.60
- **PPC (z1 min)**: 2.67
- **Ring fe (16th)**: 5.12
- **err(rho_true)**: 0.1711
- **Angle Peaks**: 1.0
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_ord98396-z1_01.60-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_corner.png)

![PPC](figures/kepler_51_d_ord98396-z1_01.60-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE
- **PPC (z1)**: 1.53
- **PPC (z1 min)**: 2.62
- **Ring fe (16th)**: 6.40
- **err(rho_true)**: 0.1579
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_ord98472-z1_01.53-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_corner.png)

![PPC](figures/kepler_51_d_ord98472-z1_01.53-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE
- **PPC (z1)**: 1.51
- **PPC (z1 min)**: 2.47
- **Ring fe (16th)**: 5.42
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.0
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_ord98486-z1_01.51-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_corner.png)

![PPC](figures/kepler_51_d_ord98486-z1_01.51-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE
- **PPC (z1)**: 1.46
- **PPC (z1 min)**: 2.36
- **Ring fe (16th)**: 5.45
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.0
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_ord98538-z1_01.46-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_corner.png)

![PPC](figures/kepler_51_d_ord98538-z1_01.46-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_pFREE
- **PPC (z1)**: 1.44
- **PPC (z1 min)**: 2.43
- **Ring fe (16th)**: 2.63
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_ord98564-z1_01.44-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_ord98564-z1_01.44-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE
- **PPC (z1)**: 1.36
- **PPC (z1 min)**: 2.31
- **Ring fe (16th)**: 7.10
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.0
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_ord98640-z1_01.36-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_corner.png)

![PPC](figures/kepler_51_d_ord98640-z1_01.36-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE
- **PPC (z1)**: 1.32
- **PPC (z1 min)**: 1.20
- **Ring fe (16th)**: 1.14
- **err(rho_true)**: 0.0662
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_ord98684-z1_01.32-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_ord98684-z1_01.32-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE
- **PPC (z1)**: 1.30
- **PPC (z1 min)**: 1.19
- **Ring fe (16th)**: 5.16
- **err(rho_true)**: 0.0677
- **Angle Peaks**: 1.0
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_ord98700-z1_01.30-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_corner.png)

![PPC](figures/kepler_51_d_ord98700-z1_01.30-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE
- **PPC (z1)**: 1.30
- **PPC (z1 min)**: 1.12
- **Ring fe (16th)**: 6.58
- **err(rho_true)**: 0.0407
- **Angle Peaks**: 1.0
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_ord98700-z1_01.30-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_corner.png)

![PPC](figures/kepler_51_d_ord98700-z1_01.30-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_pFREE
- **PPC (z1)**: 1.29
- **PPC (z1 min)**: 2.19
- **Ring fe (16th)**: 1.37
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.0
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_ord98713-z1_01.29-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_ord98713-z1_01.29-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE
- **PPC (z1)**: 1.20
- **PPC (z1 min)**: 1.10
- **Ring fe (16th)**: 6.75
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.5
- **Category**: [Excellent] Golden Sample

![Corner Plot](figures/kepler_51_d_ord98797-z1_01.20-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_corner.png)

![PPC](figures/kepler_51_d_ord98797-z1_01.20-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_ppc.png)

---

### Category: [Acceptable] Multimodal Angles

| Rank | Tag | PPC (z1) | PPC (z1 min) | Ring fe (16%) | err(rho_true) | Angle Peaks |
|---|---|---|---|---|---|---|
| 16 | `kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE` | **1.90** | 2.63 | 5.21 | 0.1744 | 2.0 |
| 17 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE` | **1.75** | 2.98 | 1.06 | 0.1543 | 2.0 |
| 18 | `kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE` | **1.65** | 2.76 | 6.29 | 0.1914 | 2.0 |
| 19 | `kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE` | **1.46** | 2.60 | 7.11 | N/A | 2.0 |

#### kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE
- **PPC (z1)**: 1.90
- **PPC (z1 min)**: 2.63
- **Ring fe (16th)**: 5.21
- **err(rho_true)**: 0.1744
- **Angle Peaks**: 2.0
- **Category**: [Acceptable] Multimodal Angles

![Corner Plot](figures/kepler_51_d_ord98098-z1_01.90-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_corner.png)

![PPC](figures/kepler_51_d_ord98098-z1_01.90-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE
- **PPC (z1)**: 1.75
- **PPC (z1 min)**: 2.98
- **Ring fe (16th)**: 1.06
- **err(rho_true)**: 0.1543
- **Angle Peaks**: 2.0
- **Category**: [Acceptable] Multimodal Angles

![Corner Plot](figures/kepler_51_d_ord98250-z1_01.75-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_ord98250-z1_01.75-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE
- **PPC (z1)**: 1.65
- **PPC (z1 min)**: 2.76
- **Ring fe (16th)**: 6.29
- **err(rho_true)**: 0.1914
- **Angle Peaks**: 2.0
- **Category**: [Acceptable] Multimodal Angles

![Corner Plot](figures/kepler_51_d_ord98346-z1_01.65-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_corner.png)

![PPC](figures/kepler_51_d_ord98346-z1_01.65-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE
- **PPC (z1)**: 1.46
- **PPC (z1 min)**: 2.60
- **Ring fe (16th)**: 7.11
- **err(rho_true)**: N/A
- **Angle Peaks**: 2.0
- **Category**: [Acceptable] Multimodal Angles

![Corner Plot](figures/kepler_51_d_ord98544-z1_01.46-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_corner.png)

![PPC](figures/kepler_51_d_ord98544-z1_01.46-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_ppc.png)

---

### Category: [Rejected] Unphysical Nuisance

| Rank | Tag | PPC (z1) | PPC (z1 min) | Ring fe (16%) | err(rho_true) | Angle Peaks |
|---|---|---|---|---|---|---|
| 20 | `kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE` | **1.97** | 2.56 | 6.22 | 0.2875 | 1.5 |
| 21 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE` | **1.94** | 2.69 | 1.47 | 0.2886 | 1.5 |
| 22 | `kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE` | **1.80** | 2.11 | 1.62 | 0.2863 | 2.0 |
| 23 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE` | **1.72** | 2.24 | 2.30 | 0.2843 | 2.0 |
| 24 | `kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE` | **1.70** | 2.09 | 1.17 | 0.2837 | 1.5 |
| 25 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE` | **1.69** | 2.73 | 6.19 | 0.2899 | 1.0 |
| 26 | `kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE` | **1.62** | 2.12 | 5.03 | 0.2839 | 1.0 |
| 27 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE` | **1.59** | 2.14 | 4.92 | 0.2851 | 1.0 |

#### kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE
- **PPC (z1)**: 1.97
- **PPC (z1 min)**: 2.56
- **Ring fe (16th)**: 6.22
- **err(rho_true)**: 0.2875
- **Angle Peaks**: 1.5
- **Category**: [Rejected] Unphysical Nuisance

![Corner Plot](figures/kepler_51_d_ord98033-z1_01.97-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_corner.png)

![PPC](figures/kepler_51_d_ord98033-z1_01.97-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE
- **PPC (z1)**: 1.94
- **PPC (z1 min)**: 2.69
- **Ring fe (16th)**: 1.47
- **err(rho_true)**: 0.2886
- **Angle Peaks**: 1.5
- **Category**: [Rejected] Unphysical Nuisance

![Corner Plot](figures/kepler_51_d_ord98056-z1_01.94-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_ord98056-z1_01.94-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE
- **PPC (z1)**: 1.80
- **PPC (z1 min)**: 2.11
- **Ring fe (16th)**: 1.62
- **err(rho_true)**: 0.2863
- **Angle Peaks**: 2.0
- **Category**: [Rejected] Unphysical Nuisance

![Corner Plot](figures/kepler_51_d_ord98196-z1_01.80-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_ord98196-z1_01.80-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE
- **PPC (z1)**: 1.72
- **PPC (z1 min)**: 2.24
- **Ring fe (16th)**: 2.30
- **err(rho_true)**: 0.2843
- **Angle Peaks**: 2.0
- **Category**: [Rejected] Unphysical Nuisance

![Corner Plot](figures/kepler_51_d_ord98278-z1_01.72-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_ord98278-z1_01.72-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE
- **PPC (z1)**: 1.70
- **PPC (z1 min)**: 2.09
- **Ring fe (16th)**: 1.17
- **err(rho_true)**: 0.2837
- **Angle Peaks**: 1.5
- **Category**: [Rejected] Unphysical Nuisance

![Corner Plot](figures/kepler_51_d_ord98299-z1_01.70-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_ord98299-z1_01.70-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE
- **PPC (z1)**: 1.69
- **PPC (z1 min)**: 2.73
- **Ring fe (16th)**: 6.19
- **err(rho_true)**: 0.2899
- **Angle Peaks**: 1.0
- **Category**: [Rejected] Unphysical Nuisance

![Corner Plot](figures/kepler_51_d_ord98315-z1_01.69-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_corner.png)

![PPC](figures/kepler_51_d_ord98315-z1_01.69-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE
- **PPC (z1)**: 1.62
- **PPC (z1 min)**: 2.12
- **Ring fe (16th)**: 5.03
- **err(rho_true)**: 0.2839
- **Angle Peaks**: 1.0
- **Category**: [Rejected] Unphysical Nuisance

![Corner Plot](figures/kepler_51_d_ord98379-z1_01.62-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_corner.png)

![PPC](figures/kepler_51_d_ord98379-z1_01.62-kepler_51_d_NS_exorings_kde_delta-T14-T23_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE
- **PPC (z1)**: 1.59
- **PPC (z1 min)**: 2.14
- **Ring fe (16th)**: 4.92
- **err(rho_true)**: 0.2851
- **Angle Peaks**: 1.0
- **Category**: [Rejected] Unphysical Nuisance

![Corner Plot](figures/kepler_51_d_ord98409-z1_01.59-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_corner.png)

![PPC](figures/kepler_51_d_ord98409-z1_01.59-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_ppc.png)

---

### Category: [Rejected] Poor Fit

| Rank | Tag | PPC (z1) | PPC (z1 min) | Ring fe (16%) | err(rho_true) | Angle Peaks |
|---|---|---|---|---|---|---|
| 28 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE` | **1.19** | 1.20 | 1.19 | 0.0776 | 1.0 |
| 29 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE` | **1.18** | 1.10 | 5.35 | N/A | 1.0 |
| 30 | `kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_pFREE` | **1.17** | 2.09 | 1.56 | N/A | 1.5 |
| 31 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE` | **1.10** | 1.03 | 6.50 | 0.0455 | 1.0 |
| 32 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_pFREE` | **1.04** | 1.06 | 1.38 | N/A | 1.5 |
| 33 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE` | **1.04** | 1.04 | 5.29 | 0.0558 | 1.0 |
| 34 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE` | **1.03** | 1.04 | 1.22 | 0.0459 | 1.0 |
| 35 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_pFREE` | **1.00** | 1.07 | 1.27 | N/A | 1.0 |
| 36 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE` | **0.97** | 1.00 | 1.21 | 0.0354 | 1.0 |
| 37 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026` | **0.83** | 0.97 | 6.63 | N/A | 1.5 |
| 38 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_tauFREE` | **0.82** | 0.97 | 5.31 | N/A | 1.0 |
| 39 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_pFREE` | **0.79** | 0.97 | 1.37 | N/A | 1.5 |
| 40 | `kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_tauFREE_pFREE` | **0.77** | 0.97 | 1.33 | N/A | 1.0 |

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE
- **PPC (z1)**: 1.19
- **PPC (z1 min)**: 1.20
- **Ring fe (16th)**: 1.19
- **err(rho_true)**: 0.0776
- **Angle Peaks**: 1.0
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_d_ord98808-z1_01.19-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_ord98808-z1_01.19-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE
- **PPC (z1)**: 1.18
- **PPC (z1 min)**: 1.10
- **Ring fe (16th)**: 5.35
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.0
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_d_ord98822-z1_01.18-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_corner.png)

![PPC](figures/kepler_51_d_ord98822-z1_01.18-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_pFREE
- **PPC (z1)**: 1.17
- **PPC (z1 min)**: 2.09
- **Ring fe (16th)**: 1.56
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.5
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_d_ord98827-z1_01.17-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_ord98827-z1_01.17-kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE
- **PPC (z1)**: 1.10
- **PPC (z1 min)**: 1.03
- **Ring fe (16th)**: 6.50
- **err(rho_true)**: 0.0455
- **Angle Peaks**: 1.0
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_d_ord98899-z1_01.10-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_corner.png)

![PPC](figures/kepler_51_d_ord98899-z1_01.10-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_pFREE
- **PPC (z1)**: 1.04
- **PPC (z1 min)**: 1.06
- **Ring fe (16th)**: 1.38
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.5
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_d_ord98957-z1_01.04-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_ord98957-z1_01.04-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE
- **PPC (z1)**: 1.04
- **PPC (z1 min)**: 1.04
- **Ring fe (16th)**: 5.29
- **err(rho_true)**: 0.0558
- **Angle Peaks**: 1.0
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_d_ord98957-z1_01.04-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_corner.png)

![PPC](figures/kepler_51_d_ord98957-z1_01.04-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE
- **PPC (z1)**: 1.03
- **PPC (z1 min)**: 1.04
- **Ring fe (16th)**: 1.22
- **err(rho_true)**: 0.0459
- **Angle Peaks**: 1.0
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_d_ord98973-z1_01.03-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_ord98973-z1_01.03-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_pFREE
- **PPC (z1)**: 1.00
- **PPC (z1 min)**: 1.07
- **Ring fe (16th)**: 1.27
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.0
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_d_ord98995-z1_01.00-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_ord98995-z1_01.00-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_bFREE_tauFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE
- **PPC (z1)**: 0.97
- **PPC (z1 min)**: 1.00
- **Ring fe (16th)**: 1.21
- **err(rho_true)**: 0.0354
- **Angle Peaks**: 1.0
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_d_ord99026-z1_00.97-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_ord99026-z1_00.97-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_tauFREE_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026
- **PPC (z1)**: 0.83
- **PPC (z1 min)**: 0.97
- **Ring fe (16th)**: 6.63
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.5
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_d_ord99169-z1_00.83-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_corner.png)

![PPC](figures/kepler_51_d_ord99169-z1_00.83-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_tauFREE
- **PPC (z1)**: 0.82
- **PPC (z1 min)**: 0.97
- **Ring fe (16th)**: 5.31
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.0
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_d_ord99180-z1_00.82-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_tauFREE_corner.png)

![PPC](figures/kepler_51_d_ord99180-z1_00.82-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_tauFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_pFREE
- **PPC (z1)**: 0.79
- **PPC (z1 min)**: 0.97
- **Ring fe (16th)**: 1.37
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.5
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_d_ord99215-z1_00.79-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_pFREE_corner.png)

![PPC](figures/kepler_51_d_ord99215-z1_00.79-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_pFREE_ppc.png)

---

#### kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_tauFREE_pFREE
- **PPC (z1)**: 0.77
- **PPC (z1 min)**: 0.97
- **Ring fe (16th)**: 1.33
- **err(rho_true)**: N/A
- **Angle Peaks**: 1.0
- **Category**: [Rejected] Poor Fit

![Corner Plot](figures/kepler_51_d_ord99229-z1_00.77-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_tauFREE_pFREE_corner.png)

![PPC](figures/kepler_51_d_ord99229-z1_00.77-kepler_51_d_NS_exorings_kde_delta-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_tauFREE_pFREE_ppc.png)

---
