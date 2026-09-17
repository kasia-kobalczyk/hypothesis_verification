# v4-scope development report — BENCH-GRAPH-V4-SCOPE-001

**Status: NOT FROZEN. Recommendation: do not freeze; continue development (section 11).** The eight cases are a spent development set; nothing here is held-out evidence. D045/D046 are model-based Research Director development labels, used to diagnose behaviour, not as ground truth or an optimisation target.

Design: `docs/V4_SCOPE_DESIGN.md`. Metrics: `benchmark/v4_scope/`. Stage A replays the v4-scope layer on the frozen v3 pilot (192 propositions, identical retrieved records and evidence labels), three independent replicates per iteration, so behaviour is compared node by node with v3, prior v4 and the labels. Stage B runs the final version end to end three times.

Model and configuration: Azure OpenAI `gpt-4.1-kasia` (api 2024-05-01-preview), temperature 0, seed 20260911, JSON mode, for every verifier call; Semantic Scholar + Crossref literature with the frozen per-case cutoffs; ordinal mappings `v0-placeholder` (unchanged); config `configs/v4_dev_explanatory.yaml` (identical to the pilot except `dataset.status: development`).

## 1. Iteration log

| iteration | replay commit | prompts | change | why |
| --- | --- | --- | --- | --- |
| iter01 | `a2f34d3` | prediction_state_v2 · proposition_scope_v1 · contrast_element_v1 · contrast_relevance_v1 | Initial v4-scope layer: separate scope classifier over all propositions; contrast element (extractor sees the recorded states and returns `has_contrast`); three-question contrast relevance with the category derived in code; deterministic gate (profile → scope → evidence → element with a contrast → relevance) with `contrast_direct` only. | Directive design. `has_contrast` was added to the gate before any replicate was run (a first launch was stopped after ~1 minute, before any case finished, and deleted), so that no proposition can score without a contrast-bearing element. |
| iter02 | `222d4fa` | prediction_state_v2 · proposition_scope_v2 · contrast_element_v2 · contrast_relevance_v2 | Scope: `invalid_or_underspecified` also covers propositions only weakly implied (the directive's own definition, omitted in v1). Element: the extractor no longer sees the recorded states; it states each candidate's position on the contrast variable (requires_asserted / requires_other / not_required), and `has_contrast` is derived in code (positions form a contrast AND point the same way as the states). Relevance: capability shown in another setting is `partly`, not `yes`. | Iteration 1 (all 3 replicates): every scored node was a reviewed failure. Five were implication errors (silence / weak implication) with strong determinate states, one a possibility shown in a model setting read as occurrence (generic fact), one or two construct mismatches. The element positions were meant as a second, state-blind implication check. |

Iteration was stopped after iteration 2. The nodes that still score wrongly are the same in both iterations and in every replicate, and each is a strong determinate reading of the candidate texts that the same model reproduced in three separate calls (prediction states, scope, and the state-blind element positions). A further same-model prompt change aimed at five contested, model-labelled nodes would be label-fitting rather than method development. Iteration 2 is the final development version run in stage B.

No case-specific rule, no development-case content in any prompt (checked by a test against the visible phenomenon text of all eight cases), no hidden annotation in verifier context, no change to numeric mappings, and `indeterminate` contributes nothing in every iteration.

Replays: iter01: `runs/v4scope_replay_iter01`, `runs/v4scope_replay_iter01_rep2`, `runs/v4scope_replay_iter01_rep3`; iter02: `runs/v4scope_replay_iter02`, `runs/v4scope_replay_iter02_rep2`, `runs/v4scope_replay_iter02_rep3` (gitignored). Every recorded gate and score was re-derived from the recorded judgments with the committed gate code: iter01 all consistent, iter02 all consistent. LLM errors: iter01 0/0/0, iter02 0/0/0.

## 2. Prediction-state preservation

All v4-scope iterations use `prediction_state_v2`, the prior v4 head, unchanged. Differences from prior v4 are therefore run-to-run noise, which this table measures.

| run | pairs indeterminate | comparative profiles | one-sided | D046 unqualified / all | reviewed silence errors with a comparative profile |
| --- | --- | --- | --- | --- | --- |
| prior v4 `v4_replay_pilot_iter02` | 33% | 43 | 120 | 20/20 / 21/24 | 4/10 |
| prior v4 `v4_replay_pilot_iter02_rep2` | 33% | 48 | 117 | 20/20 / 21/24 | 4/10 |
| iter01 `v4scope_replay_iter01` | 30% | 50 | 111 | 20/20 / 22/24 | 4/10 |
| iter01 `v4scope_replay_iter01_rep2` | 32% | 51 | 109 | 20/20 / 23/24 | 4/10 |
| iter01 `v4scope_replay_iter01_rep3` | 30% | 55 | 103 | 20/20 / 22/24 | 4/10 |
| iter02 `v4scope_replay_iter02` | 31% | 52 | 109 | 20/20 / 22/24 | 4/10 |
| iter02 `v4scope_replay_iter02_rep2` | 31% | 49 | 111 | 20/20 / 22/24 | 4/10 |
| iter02 `v4scope_replay_iter02_rep3` | 33% | 46 | 115 | 20/20 / 22/24 | 4/10 |

State-pair agreement between replicates (of 384 hypothesis × proposition pairs): prior v4 365/384; iteration 1 361/384, 366/384, 363/384; iteration 2 370/384, 364/384, 366/384; iteration-2 replicate 1 vs prior v4 357/384. Profile-class agreement: prior v4 173/192; iteration 1 171/192, 176/192, 171/192; iteration 2 178/192, 173/192, 175/192.

**No regression.** The same four of the ten reviewed silence errors (`pfc_storage_vs_control-X2`, `glnbp_induced_fit_vs_conformational_selection-X4`, `-X11`, `eukaryogenesis_mito_timing-X2`) have a comparative profile in every run, prior v4 included. Prior v4 did not score them only because its whole-proposition construct match rated their evidence `partial` or `mismatch` (both prior-v4 replicates); v4-scope's contrast relevance rates three of them `contrast_direct`, which exposes the state error (section 6).

## 3. Scope behaviour

| iteration · replicate | hypothesis-specific | mechanism-specific | broader class | possibility | invalid | on comparative profiles: specific / broad+possibility |
| --- | --- | --- | --- | --- | --- | --- |
| iter01 · rep1 | 67 | 63 | 39 | 23 | 0 | 28 / 22 |
| iter01 · rep2 | 65 | 64 | 40 | 23 | 0 | 30 / 21 |
| iter01 · rep3 | 65 | 63 | 41 | 23 | 0 | 30 / 25 |
| iter02 · rep1 | 64 | 65 | 39 | 24 | 0 | 28 / 24 |
| iter02 · rep2 | 67 | 63 | 38 | 24 | 0 | 26 / 23 |
| iter02 · rep3 | 66 | 63 | 39 | 24 | 0 | 25 / 21 |

**Reviewed category × scope** (iteration 2, summed over 3 replicates; each node counted once per replicate)

| category (n nodes) | hypothesis_specific | mechanism_specific | broader_class_fact | possibility_claim | invalid_or_underspecified |
| --- | --- | --- | --- | --- | --- |
| genuine (4) | 3 | 9 | 0 | 0 | 0 |
| silence error (10) | 5 | 20 | 5 | 0 | 0 |
| generic fact (14) | 3 | 5 | 16 | 18 | 0 |
| compatible (12) | 15 | 15 | 6 | 0 | 0 |
| construct mismatch (8) | 4 | 14 | 3 | 3 | 0 |
| weak implication (4) | 6 | 0 | 3 | 3 | 0 |

- iter01: reviewed generic component facts not scored 13/14 · 13/14 · 13/14 (scope non-comparative 12/14 · 12/14 · 13/14); reviewed genuine discriminators scope-eligible 4/4 · 4/4 · 4/4, comparative and scope-eligible 3/4 · 4/4 · 4/4, scored 0/4 · 0/4 · 0/4.
- iter02: reviewed generic component facts not scored 14/14 · 14/14 · 14/14 (scope non-comparative 12/14 · 11/14 · 11/14); reviewed genuine discriminators scope-eligible 4/4 · 4/4 · 4/4, comparative and scope-eligible 4/4 · 4/4 · 3/4, scored 0/4 · 0/4 · 1/4.

**The 14 reviewed generic component facts, iteration 2** (scope · gate reason, per replicate)

| node | replicate 1 | replicate 2 | replicate 3 |
| --- | --- | --- | --- |
| `gcn4_med15_complex_vs_condensate-X3` | possibility_claim · profile_one_sided_prediction | possibility_claim · profile_one_sided_prediction | possibility_claim · profile_one_sided_prediction |
| `glnbp_induced_fit_vs_conformational_selection-X3` | possibility_claim · scope_possibility_claim | possibility_claim · scope_possibility_claim | possibility_claim · scope_possibility_claim |
| `eukaryogenesis_mito_timing-X4` | broader_class_fact · profile_one_sided_prediction | broader_class_fact · profile_one_sided_prediction | broader_class_fact · profile_one_sided_prediction |
| `eukaryogenesis_mito_timing-X6` | hypothesis_specific · relevance_contrast_partial | hypothesis_specific · profile_one_sided_prediction | hypothesis_specific · relevance_contrast_partial |
| `glnbp_induced_fit_vs_conformational_selection-X15` | broader_class_fact · scope_broader_class_fact | broader_class_fact · scope_broader_class_fact | broader_class_fact · scope_broader_class_fact |
| `eukaryogenesis_mito_timing-X24` | possibility_claim · scope_possibility_claim | possibility_claim · scope_possibility_claim | possibility_claim · scope_possibility_claim |
| `glnbp_induced_fit_vs_conformational_selection-X8` | possibility_claim · scope_possibility_claim | possibility_claim · scope_possibility_claim | possibility_claim · scope_possibility_claim |
| `glnbp_induced_fit_vs_conformational_selection-X6` | possibility_claim · profile_one_sided_prediction | possibility_claim · profile_shared_prediction | possibility_claim · profile_shared_prediction |
| `eukaryogenesis_mito_timing-X10` | broader_class_fact · profile_one_sided_prediction | mechanism_specific · profile_one_sided_prediction | mechanism_specific · profile_one_sided_prediction |
| `eukaryogenesis_mito_timing-X12` | broader_class_fact · profile_one_sided_prediction | broader_class_fact · profile_one_sided_prediction | broader_class_fact · profile_one_sided_prediction |
| `eukaryogenesis_mito_timing-X22` | broader_class_fact · scope_broader_class_fact | broader_class_fact · profile_one_sided_prediction | broader_class_fact · profile_one_sided_prediction |
| `spider_orb_web_origin-X12` | possibility_claim · scope_possibility_claim | possibility_claim · scope_possibility_claim | possibility_claim · profile_one_sided_prediction |
| `gcn4_med15_complex_vs_condensate-X18` | broader_class_fact · profile_one_sided_prediction | broader_class_fact · profile_one_sided_prediction | broader_class_fact · profile_one_sided_prediction |
| `gcn4_med15_complex_vs_condensate-X23` | mechanism_specific · relevance_contrast_partial | mechanism_specific · relevance_contrast_partial | mechanism_specific · relevance_contrast_partial |

**The 4 reviewed genuine discriminators** (scope · profile · contrast relevance · gate reason)

| node | iter01 rep1 | iter01 rep2 | iter01 rep3 | iter02 rep1 | iter02 rep2 | iter02 rep3 |
| --- | --- | --- | --- | --- | --- | --- |
| `glnbp_induced_fit_vs_conformational_selection-X5` | mechanism_specific · comparative_discriminator · contrast_partial · relevance_contrast_partial | mechanism_specific · comparative_discriminator · contrast_partial · relevance_contrast_partial | mechanism_specific · comparative_discriminator · contrast_partial · relevance_contrast_partial | mechanism_specific · comparative_discriminator · contrast_partial · relevance_contrast_partial | mechanism_specific · comparative_discriminator · contrast_partial · relevance_contrast_partial | mechanism_specific · comparative_discriminator · contrast_partial · relevance_contrast_partial |
| `pfc_storage_vs_control-X6` | mechanism_specific · comparative_discriminator · contrast_partial · relevance_contrast_partial | mechanism_specific · comparative_discriminator · contrast_partial · relevance_contrast_partial | mechanism_specific · comparative_discriminator · contrast_partial · relevance_contrast_partial | mechanism_specific · comparative_discriminator · contrast_partial · relevance_contrast_partial | mechanism_specific · comparative_discriminator · contrast_partial · relevance_contrast_partial | mechanism_specific · comparative_discriminator · contrast_partial · relevance_contrast_partial |
| `pfc_storage_vs_control-X24` | mechanism_specific · one_sided_prediction · contrast_partial · profile_one_sided_prediction | mechanism_specific · comparative_discriminator · contrast_partial · relevance_contrast_partial | mechanism_specific · comparative_discriminator · contrast_partial · relevance_contrast_partial | mechanism_specific · comparative_discriminator · contrast_partial · relevance_contrast_partial | mechanism_specific · comparative_discriminator · contrast_partial · relevance_contrast_partial | mechanism_specific · one_sided_prediction · contrast_partial · profile_one_sided_prediction |
| `glnbp_induced_fit_vs_conformational_selection-X9` | hypothesis_specific · comparative_discriminator · contrast_partial · relevance_contrast_partial | hypothesis_specific · comparative_discriminator · contrast_partial · relevance_contrast_partial | hypothesis_specific · comparative_discriminator · contrast_partial · relevance_contrast_partial | hypothesis_specific · comparative_discriminator · contrast_partial · relevance_contrast_partial | hypothesis_specific · comparative_discriminator · contrast_partial · relevance_contrast_partial | hypothesis_specific · comparative_discriminator · contrast_direct · scored |

## 4. Contrast-bearing evidence

| iteration · replicate | informative-evidence nodes | direct | partial | context only | construct mismatch | no evidence | element without contrast | on eligible nodes with a contrast: direct / partial | genuine discriminators direct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| iter01 · rep1 | 79 | 26 | 51 | 1 | 1 | 0 | 7 | 6 / 5 | 0/4 |
| iter01 · rep2 | 79 | 24 | 53 | 1 | 1 | 0 | 8 | 6 / 7 | 0/4 |
| iter01 · rep3 | 79 | 24 | 52 | 0 | 2 | 1 | 8 | 6 / 6 | 0/4 |
| iter02 · rep1 | 79 | 20 | 59 | 0 | 0 | 0 | 57 | 5 / 7 | 0/4 |
| iter02 · rep2 | 79 | 24 | 55 | 0 | 0 | 0 | 60 | 4 / 5 | 0/4 |
| iter02 · rep3 | 79 | 21 | 57 | 1 | 0 | 0 | 60 | 6 / 4 | 1/4 |

Relevance by reviewed category, iteration 2 (summed over replicates):

| category | contrast_direct | contrast_partial | context_only | construct_mismatch | relevance_no_evidence |
| --- | --- | --- | --- | --- | --- |
| genuine | 1 | 11 | 0 | 0 | 0 |
| silence error | 12 | 18 | 0 | 0 | 0 |
| generic fact | 17 | 25 | 0 | 0 | 0 |
| compatible | 16 | 20 | 0 | 0 | 0 |
| construct mismatch | 6 | 18 | 0 | 0 | 0 |
| weak implication | 6 | 6 | 0 | 0 | 0 |

`context_only` and `construct_mismatch` are almost never assigned: the cited records had already been judged informative by the v3 assessor, and the relevance judge almost always finds that they report the contrast variable at least partly. The separation the directive asked for therefore happens between `contrast_direct` and `contrast_partial`, not between direct and context-only.

Reviewed generic/compatible facts that v3 scored and that now receive only context-only, mismatch or no-evidence relevance: 0 · 0 · 0 per iteration-2 replicate. Generic facts are not excluded by the evidence judgment; they are excluded by scope and state profile (section 3), and when they reach the relevance judge they are usually rated `contrast_direct` or `contrast_partial`.

## 5. Specificity–assessability trade-off

Is historical evidence less able to test hypothesis/mechanism-specific propositions than broad ones? Rates over all 192 propositions per replicate: P(informative evidence), P(contrast-direct evidence), and P(contrast-direct | informative).

| iteration · replicate | specific: n · informative · direct · direct given informative | broad class + possibility: n · informative · direct · direct given informative |
| --- | --- | --- |
| iter01 · rep1 | 130 · 37% · 10% · 27% | 62 · 50% · 21% · 42% |
| iter01 · rep2 | 129 · 37% · 9% · 25% | 63 · 49% · 19% · 39% |
| iter01 · rep3 | 128 · 37% · 10% · 28% | 64 · 50% · 17% · 34% |
| iter02 · rep1 | 129 · 38% · 11% · 29% | 63 · 48% · 10% · 20% |
| iter02 · rep2 | 130 · 38% · 12% · 33% | 62 · 48% · 13% · 27% |
| iter02 · rep3 | 129 · 38% · 11% · 29% | 63 · 48% · 11% · 23% |

**Scope × evidence availability / contrast relevance**, iteration 2, counts summed over 3 replicates (so each row totals 3 × its mean node count):

| scope | n | no_evidence | mixed | contrast_direct | contrast_partial | context_only | construct_mismatch | relevance_no_evidence | element without contrast | P(informative) | P(direct) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hypothesis_specific | 197 | 138 | 0 | 12 | 47 | 0 | 0 | 0 | 49 | 30% | 6% |
| mechanism_specific | 191 | 103 | 0 | 32 | 56 | 0 | 0 | 0 | 67 | 46% | 17% |
| broader_class_fact | 116 | 56 | 0 | 10 | 49 | 1 | 0 | 0 | 47 | 52% | 9% |
| possibility_claim | 72 | 42 | 0 | 11 | 19 | 0 | 0 | 0 | 14 | 42% | 15% |
| invalid_or_underspecified | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | — |

Findings, stable across replicates:

1. **Availability.** Specific propositions (about two thirds of all) are less often reached by any informative evidence than broad ones: 37–38% vs 48–50% in every replicate of both iterations. The most case-specific class is the least assessable: in iteration 2, `hypothesis_specific` has informative evidence for 30% and contrast-direct evidence for 6% of propositions, against 46% / 17% for `mechanism_specific`.
2. **Directness depends on the relevance prompt.** Under relevance v1, broad propositions received contrast-direct evidence about twice as often as specific ones (17–21% vs 9–10%). Under v2, which downgrades capability shown in another setting, the rates are similar (10–13% vs 11–12%). The directness gap is therefore not robust; the availability gap is.
3. **Genuine discriminators.** The four reviewed genuine discriminators received contrast-direct evidence in 1 of 24 node-replicates; their records address the contrast variable only partly (for example, apo and holo structures that do not show binding order).

`invalid_or_underspecified` was never assigned, in either scope prompt version.

## 6. What scores

**iter01** — scored nodes per replicate: 6 · 6 · 6; by scope {'mechanism_specific': 4, 'hypothesis_specific': 2} · {'mechanism_specific': 4, 'hypothesis_specific': 2} · {'mechanism_specific': 4, 'hypothesis_specific': 2}.

| node | reviewed category | scope | evidence | replicates scored | log-odds H2−H1 | proposition |
| --- | --- | --- | --- | --- | --- | --- |
| `eukaryogenesis_mito_timing-X7` | weak implication | hypothesis_specific | strong_contradiction | 3/3 | +1.63 | In eukaryotic lineages, the presence of a fully developed endomembrane system is observed only in cells that also contain mitochondria. |
| `gcn4_med15_complex_vs_condensate-X23` | generic fact | mechanism_specific | strong_support | 3/3 | +1.46 | Acidic activation domains engage Mediator subunits via phase separation mechanisms. |
| `glnbp_induced_fit_vs_conformational_selection-X11` | silence error | mechanism_specific | strong_contradiction | 3/3 | +1.63 | Glutamine binding is not required for GlnBP to adopt a closed conformation. |
| `glnbp_induced_fit_vs_conformational_selection-X4` | silence error | mechanism_specific | strong_contradiction | 3/3 | +1.63 | Apo-GlnBP adopts a closed or semi-closed conformation in the absence of glutamine. |
| `pfc_storage_vs_control-X14` | construct mismatch | mechanism_specific | strong_support | 3/3 | -0.89 | Neural firing rates in prefrontal cortex encode the specific features of memorized stimuli during the delay period of a visual working memory task. |
| `forest_fragmentation_resilience-X15` | weak implication | hypothesis_specific | strong_support | 2/3 | +0.89 | Forest edge environments in fragmented landscapes tend to support higher plant productivity than interior environments. |
| `forest_fragmentation_resilience-X21` | construct mismatch | hypothesis_specific | support | 1/3 | +0.52 | Fragmented forests can display increased vegetation resilience to disturbance at their edges relative to interiors, when climatic stress is moderate. |

**iter02** — scored nodes per replicate: 5 · 4 · 6; by scope {'mechanism_specific': 3, 'hypothesis_specific': 2} · {'mechanism_specific': 3, 'hypothesis_specific': 1} · {'mechanism_specific': 3, 'hypothesis_specific': 3}.

| node | reviewed category | scope | evidence | replicates scored | log-odds H2−H1 | proposition |
| --- | --- | --- | --- | --- | --- | --- |
| `eukaryogenesis_mito_timing-X7` | weak implication | hypothesis_specific | strong_contradiction | 3/3 | +1.09 | In eukaryotic lineages, the presence of a fully developed endomembrane system is observed only in cells that also contain mitochondria. |
| `glnbp_induced_fit_vs_conformational_selection-X11` | silence error | mechanism_specific | strong_contradiction | 3/3 | +1.63 | Glutamine binding is not required for GlnBP to adopt a closed conformation. |
| `glnbp_induced_fit_vs_conformational_selection-X4` | silence error | mechanism_specific | strong_contradiction | 3/3 | +1.63 | Apo-GlnBP adopts a closed or semi-closed conformation in the absence of glutamine. |
| `pfc_storage_vs_control-X2` | silence error | mechanism_specific | strong_support | 3/3 | -1.46 | Persistent neural activity in prefrontal cortex encodes the content of items maintained in working memory. |
| `forest_fragmentation_resilience-X15` | weak implication | hypothesis_specific | strong_support | 2/3 | +0.74 | Forest edge environments in fragmented landscapes tend to support higher plant productivity than interior environments. |
| `glnbp_induced_fit_vs_conformational_selection-X9` | genuine | hypothesis_specific | support | 1/3 | +0.96 | The transition from open to closed conformation in E. coli GlnBP is triggered by glutamine binding. |

Every scored node is hypothesis- or mechanism-specific by construction; no broader-class fact or possibility claim scored in any replicate.

## 7. Score-influence composition (|log-odds H2−H1| by reviewed category)

| category | v3 frozen pilot | iter01 rep1 | iter01 rep2 | iter01 rep3 | iter02 rep1 | iter02 rep2 | iter02 rep3 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| genuine | 1.47 (8%) | 0.00 (0%) | 0.00 (0%) | 0.00 (0%) | 0.00 (0%) | 0.00 (0%) | 0.96 (13%) |
| silence error | 4.02 (22%) | 3.26 (44%) | 3.26 (45%) | 3.26 (40%) | 4.73 (72%) | 4.73 (84%) | 4.73 (63%) |
| generic fact | 4.67 (26%) | 1.46 (20%) | 1.46 (20%) | 1.46 (18%) | 0.00 (0%) | 0.00 (0%) | 0.00 (0%) |
| compatible | 3.08 (17%) | 0.00 (0%) | 0.00 (0%) | 0.00 (0%) | 0.00 (0%) | 0.00 (0%) | 0.00 (0%) |
| construct mismatch | 1.28 (7%) | 0.89 (12%) | 1.41 (19%) | 0.89 (11%) | 0.00 (0%) | 0.00 (0%) | 0.00 (0%) |
| weak implication | 1.24 (7%) | 1.83 (25%) | 1.09 (15%) | 2.52 (31%) | 1.83 (28%) | 0.88 (16%) | 1.83 (24%) |
| unreviewed | 2.32 (13%) | 0.00 (0%) | 0.00 (0%) | 0.00 (0%) | 0.00 (0%) | 0.00 (0%) | 0.00 (0%) |
| total | 18.07 | 7.44 | 7.22 | 8.13 | 6.55 | 5.60 | 7.51 |

Prior v4 (stage A, direct-only construct policy) scored no node on the frozen pilot, so its composition is empty. v3's total covers all 192 nodes, with many unreviewed contributors; the v4-scope totals come from 4–6 nodes, all reviewed.

## 8. `contrast_partial` sensitivity analysis (reporting only; not the method)

| iteration · replicate | scored: main → with partial | added nodes by category | generic facts re-entering | genuine share with partial | silence share with partial |
| --- | --- | --- | --- | --- | --- |
| iter01 · rep1 | 6 → 11 | construct mismatch 1, genuine 3, silence error 1 | none | 19% | 39% |
| iter01 · rep2 | 6 → 13 | compatible 1, construct mismatch 1, genuine 4, silence error 1 | none | 26% | 33% |
| iter01 · rep3 | 6 → 12 | construct mismatch 1, genuine 4, silence error 1 | none | 28% | 30% |
| iter02 · rep1 | 5 → 12 | construct mismatch 1, generic fact 2, genuine 4 | `eukaryogenesis_mito_timing-X6`, `gcn4_med15_complex_vs_condensate-X23` | 28% | 35% |
| iter02 · rep2 | 4 → 9 | generic fact 1, genuine 4 | `gcn4_med15_complex_vs_condensate-X23` | 35% | 44% |
| iter02 · rep3 | 6 → 10 | generic fact 2, genuine 2 | `eukaryogenesis_mito_timing-X6`, `gcn4_med15_complex_vs_condensate-X23` | 21% | 43% |

Allowing partial evidence is the only configuration in which the reviewed genuine discriminators carry material influence, but it also re-admits generic facts (iteration 2) and never removes the silence errors, which remain the largest single category. It is not stable or clean enough to define the method (directive §9).

## 9. Replicate stability and case scores (stage A)

| agreement between replicate pairs | iteration 1 | iteration 2 |
| --- | --- | --- |
| scope_class | 186/192, 184/192, 188/192 | 181/192, 184/192, 189/192 |
| scope_eligible | 189/192, 188/192, 189/192 | 189/192, 190/192, 191/192 |
| has_contrast | 78/79, 76/79, 77/79 | 74/79, 74/79, 75/79 |
| contrast_relevance | 75/79, 69/79, 73/79 | 73/79, 73/79, 73/79 |
| used_in_score | 190/192, 192/192, 190/192 | 191/192, 191/192, 190/192 |

Case scores (H1 / H2) per replicate. The later-resolution column is descriptive only and was not used for any decision.

| case | v3 frozen | iteration 1 | iteration 2 | later resolution favours |
| --- | --- | --- | --- | --- |
| eukaryogenesis_mito_timing | 0.08/0.92 | 0.25/0.75 · 0.25/0.75 · 0.16/0.84 | 0.25/0.75 · 0.29/0.71 · 0.25/0.75 | H2 |
| fly_wing_constraint_vs_selection | 0.42/0.58 | 0.50/0.50 · 0.50/0.50 · 0.50/0.50 | 0.50/0.50 · 0.50/0.50 · 0.50/0.50 | H2 |
| forest_fragmentation_resilience | 0.84/0.16 | 0.32/0.68 · 0.37/0.63 · 0.29/0.71 | 0.32/0.68 · 0.50/0.50 · 0.32/0.68 | mixed / regime-dependent |
| gcn4_med15_complex_vs_condensate | 0.50/0.50 | 0.19/0.81 · 0.19/0.81 · 0.19/0.81 | 0.50/0.50 · 0.50/0.50 · 0.50/0.50 | mixed / regime-dependent |
| glnbp_induced_fit_vs_conformational_selection | 0.14/0.86 | 0.04/0.96 · 0.04/0.96 · 0.04/0.96 | 0.04/0.96 · 0.04/0.96 · 0.01/0.99 | H2 |
| pfc_interhemispheric_architecture | 0.62/0.38 | 0.50/0.50 · 0.50/0.50 · 0.50/0.50 | 0.50/0.50 · 0.50/0.50 · 0.50/0.50 | mixed / regime-dependent |
| pfc_storage_vs_control | 0.77/0.23 | 0.71/0.29 · 0.71/0.29 · 0.71/0.29 | 0.81/0.19 · 0.81/0.19 · 0.81/0.19 | H2 |
| spider_orb_web_origin | 0.42/0.58 | 0.50/0.50 · 0.50/0.50 · 0.50/0.50 | 0.50/0.50 · 0.50/0.50 · 0.50/0.50 | mixed / regime-dependent |

## 10. Stage B — fresh end-to-end runs of the final version

| run | ok / error | LLM calls | cost (USD, list price, unverified) | nodes | unique texts | reference discriminators recovered | cases with any recovery | novel plausible discriminators |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pilot_explanatory_001 (frozen v3) | 8 / 0 | 784 | 2.75 | 192 | 192 | 11/23 | 7 | 3 |
| v3_rerun_explanatory_001 | 8 / 0 | 784 | 2.71 | 192 | 191 | 11/23 | 6 | 7 |
| v4_dev_explanatory_001 | 8 / 0 | 1052 | 3.76 | 192 | 192 | 11/23 | 7 | 6 |
| v4scope_explanatory_001 | 8 / 0 | 1348 | 4.61 | 192 | 192 | 9/23 | 7 | 3 |
| v4scope_explanatory_002 | 8 / 0 | 1342 | 4.56 | 192 | 191 | 10/23 | 7 | 4 |
| v4scope_explanatory_003 | 8 / 0 | 1323 | 4.49 | 192 | 191 | 10/23 | 6 | 5 |

| run | scored nodes | scored by scope | scored nodes whose text is identical to a reviewed pilot node | relevance counts |
| --- | --- | --- | --- | --- |
| v4scope_explanatory_001 | 5 | {'hypothesis_specific': 4, 'mechanism_specific': 1} | {'generic_component_fact': 1, 'no_identical_reviewed_text': 3, 'silence_as_null_error': 1} | {'contrast_partial': 60, 'contrast_direct': 29} |
| v4scope_explanatory_002 | 6 | {'hypothesis_specific': 4, 'mechanism_specific': 2} | {'no_identical_reviewed_text': 5, 'silence_as_null_error': 1} | {'contrast_partial': 58, 'contrast_direct': 26, 'construct_mismatch': 1} |
| v4scope_explanatory_003 | 4 | {'hypothesis_specific': 2, 'mechanism_specific': 2} | {'generic_component_fact': 1, 'silence_as_null_error': 2, 'no_identical_reviewed_text': 1} | {'contrast_partial': 56, 'contrast_direct': 17, 'construct_mismatch': 3, 'context_only': 1} |

| case | v4scope_explanatory_001 | v4scope_explanatory_002 | v4scope_explanatory_003 |
| --- | --- | --- | --- |
| eukaryogenesis_mito_timing | 0.58/0.42 (2 scored) | 0.16/0.84 (1 scored) | 0.35/0.65 (1 scored) |
| fly_wing_constraint_vs_selection | 0.50/0.50 (0 scored) | 0.50/0.50 (0 scored) | 0.50/0.50 (0 scored) |
| forest_fragmentation_resilience | 0.50/0.50 (0 scored) | 0.50/0.50 (0 scored) | 0.50/0.50 (0 scored) |
| gcn4_med15_complex_vs_condensate | 0.50/0.50 (0 scored) | 0.50/0.50 (0 scored) | 0.50/0.50 (0 scored) |
| glnbp_induced_fit_vs_conformational_selection | 0.16/0.84 (1 scored) | 0.01/0.99 (3 scored) | 0.34/0.66 (2 scored) |
| pfc_interhemispheric_architecture | 0.50/0.50 (0 scored) | 0.50/0.50 (0 scored) | 0.50/0.50 (0 scored) |
| pfc_storage_vs_control | 0.48/0.52 (2 scored) | 0.28/0.72 (1 scored) | 0.28/0.72 (1 scored) |
| spider_orb_web_origin | 0.50/0.50 (0 scored) | 0.61/0.39 (1 scored) | 0.50/0.50 (0 scored) |

Scored propositions in the fresh runs:

| run · case | node | scope | evidence | log-odds H2−H1 | reviewed identical text | proposition |
| --- | --- | --- | --- | --- | --- | --- |
| 001 · eukaryogenesis_mito_timing | X6 | hypothesis_specific | support | +0.64 | generic_component_fact (eukaryogenesis_mito_timing-X6) | Members of the Asgard archaeal superphylum exhibit eukaryote-like cellular complexity, including genes for endomembrane and phagocytic functions. |
| 001 · eukaryogenesis_mito_timing | X21 | hypothesis_specific | support | -0.96 | — | Lineages within the eukaryotic domain generally show a pattern where major cellular innovations occur after, rather than before, mitochondrial acquisition. |
| 001 · glnbp_induced_fit_vs_conformational_selection | X4 | hypothesis_specific | strong_contradiction | +1.63 | silence_as_null_error (glnbp_induced_fit_vs_conformational_selection-X4) | Apo-GlnBP adopts a closed or semi-closed conformation in the absence of glutamine. |
| 001 · pfc_storage_vs_control | X2 | mechanism_specific | strong_support | -0.89 | — | Persistent neural firing in lateral prefrontal cortex encodes the contents of visual working memory during the delay period. |
| 001 · pfc_storage_vs_control | X12 | hypothesis_specific | support | +0.96 | — | Regions of the lateral prefrontal cortex, including the superior precentral sulcus, are involved in prioritizing information stored in visual working memory rather than directly storing mnemonic content. |
| 002 · eukaryogenesis_mito_timing | X3 | hypothesis_specific | strong_contradiction | +1.63 | — | In lineages where mitochondria are absent or lost, eukaryote-specific cellular complexity is reduced compared to lineages with mitochondria. |
| 002 · glnbp_induced_fit_vs_conformational_selection | X4 | hypothesis_specific | strong_contradiction | +1.63 | silence_as_null_error (glnbp_induced_fit_vs_conformational_selection-X4) | Apo-GlnBP adopts a closed or semi-closed conformation in the absence of glutamine. |
| 002 · glnbp_induced_fit_vs_conformational_selection | X9 | mechanism_specific | strong_support | +1.46 | — | The open-to-closed conformational transition of GlnBP is triggered by the presence of bound glutamine. |
| 002 · glnbp_induced_fit_vs_conformational_selection | X11 | mechanism_specific | strong_contradiction | +1.63 | — | Glutamine binding is not required to induce the closed conformation in GlnBP. |
| 002 · pfc_storage_vs_control | X12 | hypothesis_specific | support | +0.96 | — | Regions within the prefrontal cortex are more likely to be involved in prioritization or control of visual working memory representations than in direct storage of mnemonic content. |
| 002 · spider_orb_web_origin | X4 | hypothesis_specific | weak_contradiction | -0.43 | — | Cribellate and ecribellate orb-weaving spiders do not share homologous silk-spinning structures specific to orb web construction. |
| 003 · eukaryogenesis_mito_timing | X6 | hypothesis_specific | support | +0.64 | generic_component_fact (eukaryogenesis_mito_timing-X6) | Members of the Asgard archaeal superphylum exhibit eukaryote-like cellular complexity, including genes for endomembrane and phagocytic functions. |
| 003 · glnbp_induced_fit_vs_conformational_selection | X4 | hypothesis_specific | strong_contradiction | +1.63 | silence_as_null_error (glnbp_induced_fit_vs_conformational_selection-X4) | Apo-GlnBP adopts a closed or semi-closed conformation in the absence of glutamine. |
| 003 · glnbp_induced_fit_vs_conformational_selection | X11 | mechanism_specific | support | -0.96 | silence_as_null_error (glnbp_induced_fit_vs_conformational_selection-X11) | Glutamine binding is not required for GlnBP to adopt a closed conformation. |
| 003 · pfc_storage_vs_control | X6 | mechanism_specific | support | +0.96 | — | Prefrontal cortex regions in the primate brain are more likely to influence the prioritization of working memory representations than to directly encode their content. |

**Consequence discovery.** Recovery in the three v4-scope runs is 9, 10 and 10 of 23 reference discriminators, against 11 in each of the three earlier runs (frozen pilot, v3 rerun, prior v4). Per-case recovery already moved by ±1 between those earlier runs. The v4-scope layer runs after generation and cannot influence it, and generation code, prompts and configuration are unchanged, so the difference is run-to-run variation in generation and in the post-hoc auditor, not an effect of the method. It is still lower in all three runs, which is noted rather than explained away.

**Scored propositions.** 4–6 per run (15 in total), all hypothesis- or mechanism-specific. Six are text-identical to reviewed pilot propositions, and all six are reviewed failures: `glnbp-X4` (silence error) in all three runs, `glnbp-X11` (silence error) once, and `eukaryogenesis-X6` (generic component fact, classified `hypothesis_specific`) twice. The executor's own reading of the other nine, which are NOT labels: four are close paraphrases of reviewed genuine discriminators (PFC control-vs-storage in all three runs; GlnBP "transition triggered by glutamine" once), two are close paraphrases of reviewed silence errors (`pfc_storage-X2`, `glnbp-X11`), two are looser relatives of reviewed failures, and one has no reviewed counterpart. Fresh retrieval therefore lets genuine-like discriminators score more often than in stage A, alongside the same recurring implication errors.

**Case outcomes are not stable across runs.** `eukaryogenesis_mito_timing` favours H1 in run 1 and H2 in runs 2 and 3; `glnbp` ranges from 0.66 to 0.99 for H2; `spider_orb_web_origin` is a tie in two runs and favours H1 in one; four cases tie in every run. With 4–6 scored propositions per run, a single proposition's presence or absence decides a case.

## 11. Development success criteria (directive §14) and recommendation

| # | criterion | verdict | evidence |
| --- | --- | --- | --- |
| 1 | prediction-state performance from prior v4 intact | met | same state prompt; D046 unqualified 20/20 in all 6 replicates; indeterminate rate and state-pair agreement within prior-v4 run-to-run noise (section 2) |
| 2 | broad class / possibility claims largely excluded | met | no broader-class or possibility proposition scored in any replicate; reviewed generic facts not scored 14/14 in all iteration-2 replicates (section 3) |
| 3 | reviewed genuine discriminators retained when specific | partly | all 4 scope-eligible with a contrast-bearing element in every replicate, but scored in 1 of 12 iteration-2 node-replicates: their pre-cutoff evidence is `contrast_partial` (sections 3, 4) |
| 4 | evidence must bear on the contrast-bearing element | met structurally, weak in practice | only `contrast_direct` scores; but `context_only` / `construct_mismatch` are almost never assigned, and `contrast_direct` is given to records that measure the stated variable even when the proposition overstates a candidate's commitment (section 6) |
| 5 | generic-fact and construct-mismatch influence drops materially | met (iteration 2) | v3 26% + 7% → 0% in all 3 iteration-2 replicates (iteration 1: 18–20% + 11–19%) (section 7) |
| 6 | genuine-discriminator share of influence increases | not met | v3 8% → 0% · 0% · 13% (iteration 2); silence errors rise from 22% to 72% · 84% · 63% of a much smaller total (section 7) |
| 7 | consequence discovery preserved | largely preserved | generation is unchanged; reference discriminators recovered: pilot_explanatory_001 11/23; v3_rerun_explanatory_001 11/23; v4_dev_explanatory_001 11/23; v4scope_explanatory_001 9/23; v4scope_explanatory_002 10/23; v4scope_explanatory_003 10/23 (section 10) |
| 8 | replicate behaviour no less stable | met | scored/not agreement 190–192/192 between replicate pairs; case scores identical across the 3 replicates in 6 (iteration 1) and 5 (iteration 2) of 8 cases; ties in every replicate: 3 and 4 cases (section 9) |

**Recommendation: do not freeze v4-scope for held-out evaluation; continue development.** The scope layer does what it was built for: broad-class facts and possibility claims no longer score, and generic-fact and construct-mismatch influence is gone in stage A (in stage B, one text-identical reviewed generic fact, classified `hypothesis_specific`, scored in two of three runs). But the few propositions that still score are dominated by reviewed implication errors (silence errors and weak implications), the reviewed genuine discriminators almost never score because the pre-cutoff literature addresses their contrast only partly, and in 4 of 8 cases the method abstains (tie) in every replicate. Freezing now would evaluate, on held-out cases, a verifier whose decisions rest on 4–6 propositions per 192, most of them wrong for reasons the gate cannot see.

**The residual failure is on the implication side, not scope or evidence.** For the recurring scored errors (`glnbp-X4`, `glnbp-X11`, `pfc_storage-X2`, `eukaryogenesis-X7`, and `forest-X15` in 2 of 3 replicates), gpt-4.1 gives determinate, opposed states (strong for the three silence errors) whenever they score, and reproduces the same contrast when asked separately, without seeing the states, for each candidate's position on the contrast variable. Example: `glnbp-X4` ("Apo-GlnBP *adopts* a closed or semi-closed conformation") is read as required by a candidate that says apo-GlnBP *samples* a closed conformation, and as ruled out by the induced-fit candidate; the records (no major apo closed population) are then `contrast_direct`. The proposition overstates the candidate (dominant vs sampled state), and neither the state judge nor the element judge separates the two.

Options for the Research Director (recommendations only, none implemented): (a) require agreement from an independent judge (a different model family) on determinate contrasts before a proposition may score, since same-model re-asking does not decorrelate these errors; (b) re-adjudicate the five recurring scored nodes with per-hypothesis states, ideally by a domain expert, because D045 recorded only primary categories for them and at least `glnbp-X4` is a subtle reading; (c) decide the `contrast_partial` policy explicitly (section 8 shows it is the only route by which genuine discriminators carry influence, but it re-admits generic facts and never removes silence errors); (d) accept abstention as a legitimate outcome and evaluate the verifier on coverage as well as direction.

## 12. Limitations

- D045/D046 are model-based Research Director development labels on 52 of 192 frozen-pilot propositions, with only 4 genuine discriminators; every composition share rests on these few nodes, and stage-B runs regenerate propositions, so labels transfer only through identical text.
- Stage A replays reuse the frozen v3 evidence labels; the relevance judge sees only the records the v3 assessor cited (or all shown records when none were cited).
- All judgments use one model (gpt-4.1) at temperature 0; replicate variation is sampling nondeterminism, not model diversity.
- Two iterations only; iteration 2 changed three prompts at once, so their separate effects are not identified.
- Ordinal mappings are the unchanged `v0-placeholder` values; log-odds magnitudes are not calibrated.
- Costs are list-price estimates with unverified rates.

