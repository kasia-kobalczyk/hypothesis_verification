# Score attribution under D045 + D046 labels

Same deterministic method as `../attribution/ATTRIBUTION_REPORT.md` (D045 only), now with the 12 D046 nodes added: 52 reviewed score-moving nodes in total. Labels are *model-based Research Director review, not external expert ground truth*. Orientation: log-odds = log-score(H2) − log-score(H1). Frozen scores reproduce exactly; no model was called.

## 1. Coverage

Reviewed 52 of 78 score-moving nodes, **87.2%** of absolute influence (D045 alone: 80.1%).

| case | score-moving | reviewed | reviewed share (D045 → D045+D046) |
| --- | --- | --- | --- |
| eukaryogenesis_mito_timing | 15 | 8 | 79.5% → **79.5%** |
| fly_wing_constraint_vs_selection | 2 | 2 | 97.7% → **100.0%** |
| forest_fragmentation_resilience | 18 | 9 | 67.5% → **76.2%** |
| gcn4_med15_complex_vs_condensate | 11 | 7 | 70.5% → **84.9%** |
| glnbp_induced_fit_vs_conformational_selection | 11 | 9 | 96.0% → **96.0%** |
| pfc_interhemispheric_architecture | 3 | 3 | 67.7% → **100.0%** |
| pfc_storage_vs_control | 11 | 7 | 90.9% → **90.9%** |
| spider_orb_web_origin | 7 | 7 | 45.4% → **100.0%** |

Cases still below the packet-wide reviewed share (87.2%): `eukaryogenesis_mito_timing`, `forest_fragmentation_resilience`, `gcn4_med15_complex_vs_condensate`.

## 2. Influence by reviewed category

| category | nodes (D045 → +D046) | share of all influence (D045 → +D046) |
| --- | --- | --- |
| genuine | 4 → 4 | 8.1% → **8.1%** |
| silence err | 8 → 10 | 20.2% → **22.3%** |
| generic comp. | 14 → 14 | 25.8% → **25.8%** |
| compatible | 8 → 12 | 15.2% → **17.0%** |
| construct mism. | 3 → 8 | 4.0% → **7.1%** |
| weak impl. | 3 → 4 | 6.8% → **6.8%** |
| UNREVIEWED | 38 → 26 | 19.9% → **12.8%** |

| case | frozen | genuine | silence err | generic comp. | compatible | construct mism. | weak impl. | UNREVIEWED |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| eukaryogenesis_mito_timing | +2.42 | · | -0.24 (1) | +2.02 (6) | · | · | +0.85 (1) | -0.20 (7) |
| fly_wing_constraint_vs_selection | +0.31 | · | +0.30 (1) | · | +0.01 (1) | · | · | · |
| forest_fragmentation_resilience | -1.63 | · | -0.41 (2) | · | -1.50 (5) | +0.15 (1) | +0.19 (1) | -0.07 (9) |
| gcn4_med15_complex_vs_condensate | +0.00 | · | -0.37 (2) | -0.25 (3) | +0.28 (1) | +0.13 (1) | · | +0.22 (4) |
| glnbp_induced_fit_vs_conformational_selection | +1.84 | -0.38 (2) | +1.63 (2) | +0.92 (4) | -0.19 (1) | · | · | -0.13 (2) |
| pfc_interhemispheric_architecture | -0.48 | · | · | · | -0.53 (2) | +0.05 (1) | · | · |
| pfc_storage_vs_control | -1.21 | +0.58 (2) | -0.89 (1) | · | -0.24 (1) | -0.72 (3) | · | +0.05 (4) |
| spider_orb_web_origin | +0.31 | · | -0.19 (1) | +0.21 (1) | +0.05 (1) | +0.03 (2) | +0.20 (2) | · |

## 3. Counterfactual views

Views as defined in the D045 report. Evidence-zeroed log-odds, top, and relation to the later resolution (`lean` for non-directional cases); graph-deletion value in brackets where it differs by > 0.05.

| case | original | A1 genuine + unrev. | A2 genuine only | B1 errors removed | B2 errors removed, reviewed only | R unreviewed only |
| --- | --- | --- | --- | --- | --- | --- |
| eukaryogenesis_mito_timing | +2.42 H2 agrees | -0.20 H1 **opposes** [del -0.26 H1] | +0.00 tie no ordering | +1.82 H2 agrees [del +1.53 H2] | +2.02 H2 agrees | -0.20 H1 **opposes** [del -0.26 H1] |
| fly_wing_constraint_vs_selection | +0.31 H2 agrees | +0.00 tie no ordering | +0.00 tie no ordering | +0.01 H2 agrees | +0.01 H2 agrees | +0.00 tie no ordering |
| forest_fragmentation_resilience | -1.63 H1 lean | -0.07 H1 lean [del -0.39 H1] | +0.00 tie lean | -1.56 H1 lean | -1.50 H1 lean | -0.07 H1 lean [del -0.39 H1] |
| gcn4_med15_complex_vs_condensate | +0.00 H2 lean | +0.22 H2 lean [del +0.40 H2] | +0.00 tie lean | +0.24 H2 lean | +0.03 H2 lean | +0.22 H2 lean [del +0.40 H2] |
| glnbp_induced_fit_vs_conformational_selection | +1.84 H2 agrees | -0.52 H1 **opposes** [del -1.00 H1] | -0.38 H1 **opposes** | +0.21 H2 agrees | +0.35 H2 agrees | -0.13 H1 **opposes** [del -0.36 H1] |
| pfc_interhemispheric_architecture | -0.48 H1 lean | +0.00 tie lean | +0.00 tie lean | -0.53 H1 lean | -0.53 H1 lean | +0.00 tie lean |
| pfc_storage_vs_control | -1.21 H1 **opposes** | +0.63 H2 agrees [del +0.53 H2] | +0.58 H2 agrees | +0.39 H2 agrees | +0.33 H2 agrees | +0.05 H2 agrees |
| spider_orb_web_origin | +0.31 H2 lean | +0.00 tie lean | +0.00 tie lean | +0.26 H2 lean | +0.26 H2 lean | +0.00 tie lean |

## 4. D046: categorical silence errors vs neutral-mapping pseudo-discrimination

Only the 12 D046 nodes carry per-hypothesis states, so this split uses them alone. One-sided = exactly one reviewer-determinate hypothesis and one reviewer-indeterminate hypothesis; the verifier's direct edge for the indeterminate hypothesis decides the kind.

| review id | reviewer states | verifier direct edges | kind | influence | category | qualified state |
| --- | --- | --- | --- | --- | --- | --- |
| `fly_wing_constraint_vs_selection-X19` | H1 positive_or_present, H2 positive_or_present | H1 implied, H2 implied | `shared_determinate` | 0.007 | compatible_non_discriminative |  |
| `forest_fragmentation_resilience-X2` | H1 indeterminate, H2 positive_or_present | H1 neutral, H2 implied | `neutral_mapping_pseudo_discrimination` | 0.137 | compatible_non_discriminative |  |
| `forest_fragmentation_resilience-X21` | H1 negative_or_absent, H2 positive_or_present | H1 unlikely, H2 implied | `determinate_contrast` | 0.151 | evidence_construct_mismatch | yes |
| `gcn4_med15_complex_vs_condensate-X12` | H1 indeterminate, H2 positive_or_present | H1 neutral, H2 implied | `neutral_mapping_pseudo_discrimination` | 0.126 | evidence_construct_mismatch |  |
| `gcn4_med15_complex_vs_condensate-X15` | H1 positive_or_present, H2 indeterminate | H1 strongly_implied, H2 unlikely | `categorical_silence_error` | 0.179 | silence_as_null_error |  |
| `pfc_interhemispheric_architecture-X1` | H1 positive_or_present, H2 indeterminate | H1 implied, H2 neutral | `neutral_mapping_pseudo_discrimination` | 0.137 | compatible_non_discriminative |  |
| `pfc_interhemispheric_architecture-X23` | H1 indeterminate, H2 positive_or_present | H1 neutral, H2 implied | `neutral_mapping_pseudo_discrimination` | 0.051 | evidence_construct_mismatch | yes |
| `spider_orb_web_origin-X17` | H1 indeterminate, H2 indeterminate | H1 implied, H2 implied | `all_indeterminate` | 0.012 | invalid_or_weak_implication | yes |
| `spider_orb_web_origin-X22` | H1 positive_or_present, H2 positive_or_present | H1 implied, H2 implied | `shared_determinate` | 0.047 | compatible_non_discriminative |  |
| `spider_orb_web_origin-X24` | H1 negative_or_absent, H2 positive_or_present | H1 unlikely, H2 strongly_implied | `determinate_contrast` | 0.134 | evidence_construct_mismatch | yes |
| `spider_orb_web_origin-X7` | H1 positive_or_present, H2 indeterminate | H1 implied, H2 unlikely | `categorical_silence_error` | 0.186 | silence_as_null_error |  |
| `spider_orb_web_origin-X8` | H1 positive_or_present, H2 indeterminate | H1 implied, H2 unlikely | `categorical_silence_error` | 0.103 | evidence_construct_mismatch |  |

- `shared_determinate`: 2 node(s), influence 0.054
- `neutral_mapping_pseudo_discrimination`: 4 node(s), influence 0.451
- `determinate_contrast`: 2 node(s), influence 0.285
- `categorical_silence_error`: 3 node(s), influence 0.468
- `all_indeterminate`: 1 node(s), influence 0.012

Verifier-only proxy over all 78 score-moving nodes (no human judgment): **28** nodes move the score although the non-generating hypothesis's direct edge is `neutral`, carrying 4.48 (24.8%) of all influence. By reviewed category: unreviewed 18, compatible_non_discriminative 8, evidence_construct_mismatch 2. Every one of them moves the score only because a determinate label is set against `neutral` = 0.50 (or via a parent route); none involves a directional label on the non-generating hypothesis.

## 5. What changed with D046 (arithmetic)

- genuine discriminators: 8.1% of all influence; confirmed errors (silence, mismatch, weak): 36.2%; generic + compatible: 42.8%; unreviewed: 12.8%.
- D046 added 0 genuine discriminator(s); 6 of 8 cases have none.
- Among D046 nodes: 3 categorical silence error(s) and 4 neutral-mapping pseudo-discrimination case(s); because the second kind occurs with a correct `neutral` label, a fix that only makes the edge assessor output `neutral` more often would leave it scoring (D046 KEY NEW METHOD DIAGNOSIS).

