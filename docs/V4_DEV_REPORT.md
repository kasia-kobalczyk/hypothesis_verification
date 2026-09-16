# v4 development report — BENCH-GRAPH-V4-DEV-001

**Status: NOT FROZEN — evidence-directness policy escalated to the Research Director.** The eight cases are a spent development set; nothing here is held-out evidence. D045/D046 are model-based Research Director development labels, used to diagnose behaviour, not as ground truth or an optimisation target.

Design: `docs/V4_DESIGN.md`. Metrics: `benchmark/v4_dev/`. Every stage-A iteration was replayed twice on the frozen v3 pilot (same propositions, same retrieved records, same evidence labels), so v3 and v4 are compared node by node.

## 1. Iteration log

| iteration | commit | state prompt | construct prompt | change | why |
| --- | --- | --- | --- | --- | --- |
| iter01 | `83b707f` | `prediction_state_v1` | `construct_match_v1` | Initial v4: prediction states with strength only for determinate states; deterministic discrimination gate; holistic construct match; direct-only; gated scoring without chain routes. | Directive design. |
| iter02 | `7f4718b` | `prediction_state_v2` | `construct_match_v2` | State prompt: general scope rule (a candidate about one system does not determine claims about a broader class or another member). Construct match: element-wise; the gating label is derived in code ('direct' only if every asserted element is established); the holistic impression is recorded, never used. | Iteration 1: reviewed generic component facts scored through contrasting states on class-level propositions; a reviewed construct mismatch (PFC storage X15, 'store and represent') was judged 'direct'; single construct flips swung case outcomes between replicates. |
| iter03 | `6817782` | `prediction_state_v3` | `construct_match_v2` | State prompt: explicit, required proposition scope (within / broader than candidates / possibility only); the gate classifies out-of-scope propositions as generic_or_possibility_claim regardless of states. | Iteration 2: 5 of 14 reviewed generic facts stayed comparatively eligible despite the advisory scope rule (family-level and 'can / is possible' claims). Human decision after iteration 2: fix the state side only, keep direct-only, do not freeze, escalate the evidence policy. |
| head | `a770f94` | `prediction_state_v2` | `construct_match_v2` | Development head reverted to iteration 2's state prompt; the v3 prompt and scope gate remain implemented and tested but inactive. No new replay needed: iteration 2 already has two replicates. | Iteration 3 regressed on both replicates (more manufactured contrasts, lower stability, only failure-category nodes scored). Further state-side tuning stopped per the human decision. |

No case-specific rule, no benchmark answer in any prompt, no change to numeric mappings, and no change to the construct policy (direct only, human decision) in any iteration.

## 2. Structural metrics per iteration (stage A, both replicates)

| iteration · replicate | pairs indeterminate | comparative | one-sided | shared | out-of-scope | eligible | scored | construct direct / partial / mismatch (informative evidence) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| iter01 · rep1 | 33% | 47 | 113 | 26 | 0 | 47 | 5 | 10 / 63 / 6 |
| iter01 · rep2 | 33% | 44 | 119 | 26 | 0 | 44 | 5 | 9 / 64 / 6 |
| iter02 · rep1 | 33% | 43 | 120 | 25 | 0 | 43 | 0 | 5 / 71 / 3 |
| iter02 · rep2 | 33% | 48 | 117 | 23 | 0 | 48 | 0 | 6 / 69 / 4 |
| iter03 · rep1 | 30% | 62 | 92 | 26 | 10 | 62 | 3 | 8 / 68 / 3 |
| iter03 · rep2 | 30% | 64 | 89 | 25 | 12 | 64 | 2 | 6 / 70 / 3 |

v3 reference (its direct edge labels read as states, on the 78 score-moving nodes): 19% of pairs `neutral`; profiles {'comparative_discriminator': 40, 'one_sided_prediction': 29, 'shared_prediction': 9}. v3 scored every node with an evidence label.

**Stability between replicates**

| iteration | state pairs | profile class | scored / not | construct label |
| --- | --- | --- | --- | --- |
| iter01 | 366/384 | 176/192 | 190/192 | 76/79 |
| iter02 | 365/384 | 173/192 | 192/192 | 75/79 |
| iter03 | 354/384 | 163/192 | 189/192 | 75/79 |

## 3. Alignment with D045/D046 development labels

Per reviewed category: comparatively eligible (before construct gating) / scored, over the two replicates.

| category (n) | iter01 | iter02 | iter03 |
| --- | --- | --- | --- |
| genuine (4) | 3/1 · 2/0 | 3/0 · 4/0 | 4/0 · 4/0 |
| silence err (10) | 4/1 · 4/1 | 4/0 · 4/0 | 6/0 · 6/0 |
| generic fact (14) | 5/2 · 6/3 | 5/0 · 5/0 | 8/1 · 8/2 |
| compatible (12) | 0/0 · 0/0 | 0/0 · 0/0 | 2/1 · 2/0 |
| construct mism. (8) | 3/1 · 1/1 | 3/0 · 3/0 | 3/1 · 3/0 |
| weak impl. (4) | 2/0 · 2/0 | 1/0 · 1/0 | 3/0 · 2/0 |

D046 per-hypothesis state agreement (12 nodes × 2 hypotheses; 4 states were qualified by the reviewer):

- iter01: unqualified 20/20 / 20/20 · all 22/24 / 22/24
- iter02: unqualified 20/20 / 20/20 · all 21/24 / 21/24
- iter03: unqualified 20/20 / 20/20 · all 22/24 / 22/24

**Fate of the four D045 genuine discriminators**

| node | iter01 | iter02 | iter03 |
| --- | --- | --- | --- |
| `glnbp_induced_fit_vs_conformational_selection-X5` | construct_partial · construct_partial | construct_partial · construct_partial | construct_partial · construct_partial |
| `glnbp_induced_fit_vs_conformational_selection-X9` | profile_one_sided_prediction · profile_one_sided_prediction | construct_partial · construct_partial | construct_partial · construct_partial |
| `pfc_storage_vs_control-X24` | scored · profile_one_sided_prediction | profile_one_sided_prediction · construct_partial | construct_partial · construct_partial |
| `pfc_storage_vs_control-X6` | construct_partial · construct_partial | construct_partial · construct_partial | construct_partial · construct_partial |

## 4. Score-influence composition (|log-odds|, by reviewed category)

| category | v3 (frozen) | iter01 rep1 · rep2 | iter02 rep1 · rep2 | iter03 rep1 · rep2 |
| --- | --- | --- | --- | --- |
| genuine | 1.47 (8%) | 1.46 · 0.00 | 0.00 · 0.00 | 0.00 · 0.00 |
| silence err | 4.02 (22%) | 1.63 · 1.63 | 0.00 · 0.00 | 0.00 · 0.00 |
| generic fact | 4.67 (26%) | 1.91 · 2.87 | 0.00 · 0.00 | 1.46 · 2.20 |
| compatible | 3.08 (17%) | 0.00 · 0.00 | 0.00 · 0.00 | 0.96 · 0.00 |
| construct mism. | 1.28 (7%) | 1.46 · 1.46 | 0.00 · 0.00 | 1.46 · 0.00 |
| weak impl. | 1.24 (7%) | 0.00 · 0.00 | 0.00 · 0.00 | 0.00 · 0.00 |
| unreviewed | 2.32 (13%) | 0.00 · 0.00 | 0.00 · 0.00 | 0.00 · 0.00 |
| **total** | 18.07 | 6.47 · 5.96 | 0.00 · 0.00 | 3.88 · 2.20 |

## 5. The evidence-policy question (for the Research Director)

Under the human-decided direct-only policy with element-wise construct matching (iteration 2 = development head), **no proposition scores on any development case in either replicate**: every eligible proposition's cited records establish only part of what it asserts. All four reviewed genuine discriminators are eligible but blocked as `construct_partial`.

Sensitivity only (recomputed from the recorded judgments, no model call; NOT the policy): case scores P(H2) if `partial` evidence were also allowed.

| case | iter01 rep1 · rep2 | iter02 rep1 · rep2 | iter03 rep1 · rep2 |
| --- | --- | --- | --- |
| eukaryogenesis_mito_timing | 0.42 · 0.83 | 0.20 · 0.85 | 0.32 · 0.90 |
| fly_wing_constraint_vs_selection | 0.50 · 0.50 | 0.50 · 0.50 | 0.60 · 0.60 |
| forest_fragmentation_resilience | 0.50 · 0.50 | 0.50 · 0.50 | 0.33 · 0.56 |
| gcn4_med15_complex_vs_condensate | 0.81 · 0.81 | 0.81 · 0.81 | 0.97 · 0.99 |
| glnbp_induced_fit_vs_conformational_selection | 0.96 · 0.96 | 0.93 · 0.93 | 0.77 · 0.43 |
| pfc_interhemispheric_architecture | 0.50 · 0.50 | 0.50 · 0.50 | 0.50 · 0.50 |
| pfc_storage_vs_control | 0.05 · 0.08 | 0.01 · 0.08 | 0.05 · 0.03 |
| spider_orb_web_origin | 0.87 · 0.87 | 0.72 · 0.72 | 0.65 · 0.72 |

Nodes that would score if partial were allowed, by reviewed category (all eight cases):

| iteration · replicate | total | genuine | silence err | generic fact | compatible | construct mism. | weak impl. | unreviewed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| iter01 · rep1 | 19 | 3 | 4 | 5 | 0 | 3 | 1 | 3 |
| iter01 · rep2 | 16 | 2 | 4 | 6 | 0 | 1 | 1 | 2 |
| iter02 · rep1 | 18 | 3 | 3 | 5 | 0 | 3 | 0 | 4 |
| iter02 · rep2 | 18 | 4 | 3 | 5 | 0 | 3 | 1 | 2 |
| iter03 · rep1 | 30 | 4 | 5 | 8 | 2 | 3 | 2 | 6 |
| iter03 · rep2 | 28 | 4 | 5 | 8 | 2 | 3 | 1 | 5 |

Genuine discriminators would be a minority of the scored nodes in 6 of 6 replicates, so relaxing the evidence policy alone would not meet the directive's success criteria: the state side still gives determinate contrasts to reviewed silence errors and generic facts.

## 6. End-to-end runs (stage B)

_Not yet available._

## 7. Freeze readiness

**Not ready to freeze.** Acceptance criteria 1–7 and 9 are met: states are separate from strength; `indeterminate` never scores; gating precedes aggregation; one-sided propositions are retained descriptively; construct mismatch cannot score; v3 is untouched and reproducible; v4 has been run on the eight development cases; generation is unchanged. Criterion 8 is not met in a usable form: failure categories do lose relative influence, but only because nothing scores, and the reviewed genuine discriminators are not usable. Criterion 10 (freeze) is withheld pending the Director's decision on the evidence policy.

