# BENCH-GRAPH-PILOT-001 — diagnostic pilot report

**This is a behavioural observation, not a performance measurement.** The benchmark carries no gold hypothesis, no accuracy is computed, and nothing in the method was tuned on these eight cases. Counts below describe what the existing pipeline did; they are not a score.

## 1. Provenance

| field | value |
| --- | --- |
| git commit | `c18edc29f93afaa4b9683bfed9473bb3fb659329` |
| git status | 21 uncommitted path(s): the pilot integration, tests and analysis scripts are not yet committed; the frozen method files are unchanged (prompt SHAs verified by test) |
| run id | `pilot_explanatory_001` |
| method | `consequence_graph` |
| dataset status | `pilot_diagnostic` |
| config | `configs/pilot_explanatory.yaml` |
| frozen method | `benchmark/frozen/narrow_graph_v3_complete.json` |
| LLM provider | `azure` |
| LLM deployment | `gpt-4.1-kasia` |
| LLM calls | 784 |
| parse failures | 0 |
| estimated cost | $2.75 |
| literature provider calls | 356 |
| recovery judge | `recovery_classify_v1` via `gpt-4.1-kasia` |
| evidence judge | `evidence_attribution_v1` via `gpt-4.1-kasia` |

The pilot config differs from `configs/mvp.yaml` only in `dataset.kind`, `dataset.status` and `dataset.case_path`; every method parameter and every prompt SHA is pinned to the freeze by `tests/test_pilot_config_is_the_frozen_method.py`.

## 2. Temporal and hidden-annotation safety

Two independent lines of evidence, because they fail differently: the tests reason about the code, the audit reasons about the artifacts.

**Tests (adversarial).** `tests/test_explanatory_cutoff_enforcement.py` rigs the provider to return each case's *real resolving study* through search, reference expansion, citation expansion and metadata lookup, and asserts none of it survives; a companion test asserts a pre-cutoff decoy *does* survive, so the filter is discriminating rather than merely restrictive. `tests/test_explanatory_hidden_isolation.py` proves the loader refuses any non-visible field and that no hidden DOI, resolver identity, reference discriminator, resolving observation or resolution summary can reach a rendered prompt.

**Empirical audit of this run.** Every byte sent to the model was scanned against the hidden annotations, and every retrieved paper against the case cutoff.

| case | cutoff | papers retrieved | chars to model | post-cutoff | hidden-content hits | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| eukaryogenesis_mito_timing | 2025-01-01 | 480 | 613,060 | 0 | 0 | clean |
| fly_wing_constraint_vs_selection | 2025-01-01 | 480 | 571,689 | 0 | 0 | clean |
| forest_fragmentation_resilience | 2024-01-01 | 480 | 603,288 | 0 | 0 | clean |
| gcn4_med15_complex_vs_condensate | 2024-01-01 | 453 | 598,904 | 0 | 0 | clean |
| glnbp_induced_fit_vs_conformational_selection | 2024-01-01 | 480 | 552,550 | 0 | 0 | clean |
| pfc_interhemispheric_architecture | 2024-12-01 | 480 | 584,646 | 0 | 0 | clean |
| pfc_storage_vs_control | 2024-01-01 | 480 | 620,224 | 0 | 0 | clean |
| spider_orb_web_origin | 2026-01-01 | 479 | 645,488 | 0 | 0 | clean |

All cases clean: **True**

## 3. Behaviour compared with ResearchBench (Step 8, question 1)

Same frozen method, same model, structural measures only (no judge).

| measure | ResearchBench reserve-12 | explanatory pilot-8 |
| --- | --- | --- |
| instances / nodes | 12 / 240 | 8 / 192 |
| sign-opposed nodes (one hypothesis above `neutral`, the other below) | 11 (5%) | 87 (45%) |
| root edges labelled `unlikely`/`strongly_contradicted` | 2% | 23% |
| root edges labelled `neutral` | 34% | 17% |
| nodes with informative evidence | 77 (32%) | 79 (41%) |
| median score margin | 0.120 | 0.389 |
| instances with margin > 0.5 | 0 | 4 |

The verifier behaves very differently on genuine competing explanations: it draws opposite-signed implications nine times as often and ranks far more decisively. Section 5 shows how much of that opposition is real.

The permissive measure "edge labels differ at all" is uninformative here — it counts `implied` vs `weakly_implied` — and is 180/192 (94%) on the pilot and 225/240 (94%) on ResearchBench.

## 4. Consequence discovery (Step 7A)

An auditor judge (`recovery_classify_v1`, which saw the hidden reference discriminators but never the verifier's edge labels) stated each proposition's status under each hypothesis and assigned a category.

| category | n | share |
| --- | --- | --- |
| silence_as_null_error | 123 | 64% |
| reference_discriminator_recovered | 41 | 21% |
| compatible_non_discriminative | 20 | 10% |
| generic_component_fact | 5 | 3% |
| novel_plausible_discriminator | 3 | 2% |
| invalid_or_unsupported | 0 | 0% |

**Measurement caveat.** Because the auditor cannot see edge labels, its `silence_as_null_error` category identifies *one-sided propositions* (one hypothesis predicts, the other is silent) — a property of what was generated, not proof the verifier erred. Section 5 separates the two.

Reference-discriminator coverage per case (a discriminator counts once, and only on a verbatim match):

| case | reference discriminators | recovered | genuine discriminators generated | compatible / generic |
| --- | --- | --- | --- | --- |
| eukaryogenesis_mito_timing | 3 | 3 | 7 | 2 |
| fly_wing_constraint_vs_selection | 3 | 0 | 0 | 12 |
| forest_fragmentation_resilience | 3 | 1 | 4 | 0 |
| gcn4_med15_complex_vs_condensate | 3 | 1 | 6 | 0 |
| glnbp_induced_fit_vs_conformational_selection | 3 | 2 | 10 | 4 |
| pfc_interhemispheric_architecture | 3 | 2 | 9 | 4 |
| pfc_storage_vs_control | 3 | 1 | 3 | 0 |
| spider_orb_web_origin | 2 | 1 | 5 | 3 |

Overall: 11/23 (48%) reference discriminators recovered; 44/192 (23%) propositions genuinely discriminative (41 matching a reference discriminator, 3 novel).

## 5. Silence as a null prediction (Step 8, questions 2–3)

`edge_assess_v1` already defines `neutral` as "the candidate says nothing either way" and tells the model to use it freely, so this is not a missing label. Joining the auditor's statuses with the verifier's edge labels:

- one-sided propositions (≥1 hypothesis silent): **127/192 (66%)**
- a silent hypothesis was labelled `neutral` (correct, inert at 0.50): **57/131 (44%)**
- …read as **absence** (`unlikely`/`strongly_contradicted`): **51/131 (39%)**
- …read as presence (`*implied`): **23/131 (18%)**

Of the **87** sign-opposed nodes that distinguish the pilot from ResearchBench, **33** are genuine discriminators and **51** are opposition manufactured from silence, according to the auditor.

**Sensitivity.** The auditor appears to over-call silence (section 8). Extrapolating the blind second rater's disagreements gives roughly 36 genuine vs 40 manufactured. Silence-driven contrast is a large share of sign-opposed contrast under either rater (~50-60%); whether it is a majority is NOT robust.

**Which way manufactured opposition pushes.** Of 31 manufactured nodes that moved a score, 29 favoured the hypothesis that *generated* the proposition (total log-odds 8.52) and 2 favoured the other (1.72). Evidence on these nodes is overwhelmingly `support`, so literature support for a hypothesis's own one-sided consequences is scored as evidence *against* its silent competitor: component truth standing in for hypothesis truth.

## 6. Historical evidence discovery (Step 7B)

| attribution | all 192 propositions | 44 genuine discriminators |
| --- | --- | --- |
| no_relevant_historical_evidence_exists | 114 | 36 |
| informative_evidence_found | 63 | 7 |
| generic_compatibility_only | 14 | 1 |
| retrieval_failure | 1 | 0 |

Assessor errors: 0. Retrieval returning nothing: 0.

When the right discriminator was generated, the pre-cutoff literature usually did not contain the decisive observation — expected by construction, since the resolving study postdates the cutoff. Informative evidence concentrated on propositions that do not discriminate. **Caveat:** the attribution judge sees only what was retrieved, so it is structurally unable to detect evidence that exists but was never retrieved; `retrieval_failure` is likely under-counted and `no_relevant_historical_evidence_exists` over-counted.

## 7. Hypothesis comparison and failure attribution (Step 7C, Step 8 q5)

No accuracy is computed. Each score's log-odds toward the top-ranked hypothesis is decomposed exactly (from `scores.json` contributions) by what the auditor found about each node.

| case | resolution | favoured | top | top vs resolution | total | genuine | manufactured | silence one-way | one-sided (ok) | both same |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| eukaryogenesis_mito_timing | favored | H2 | H2 | matches | +2.42 | +0.50 | +2.13 | +0.03 | -0.14 | -0.09 |
| fly_wing_constraint_vs_selection | favored | H2 | H2 | matches | +0.31 | +0.00 | +0.30 | +0.00 | +0.00 | +0.01 |
| forest_fragmentation_resilience | regime_dependent | — | H1 | n/a | +1.63 | +0.32 | +0.31 | +0.00 | +1.00 | +0.00 |
| gcn4_med15_complex_vs_condensate | mixed | — | H2 | n/a | +0.00 | +0.00 | -0.50 | +0.00 | +0.51 | +0.00 |
| glnbp_induced_fit_vs_conformational_selection | favored | H2 | H2 | matches | +1.84 | +1.01 | +0.78 | -0.24 | +0.00 | +0.29 |
| pfc_interhemispheric_architecture | regime_dependent | — | H1 | n/a | +0.48 | +0.00 | +0.00 | +0.00 | +0.34 | +0.14 |
| pfc_storage_vs_control | favored | H2 | H1 | OPPOSES | +1.21 | -0.30 | +1.33 | +0.34 | -0.15 | +0.00 |
| spider_orb_web_origin | component_wise | — | H2 | n/a | +0.31 | +0.19 | -0.07 | +0.01 | +0.00 | +0.18 |

**This decomposition inherits the auditor's errors, and they matter here.** Example: in `pfc_storage_vs_control`, the auditor called H2 silent on X15 ("Regions of the prefrontal cortex can directly store and represent information about items maintained in working memory."), but H2 states '...rather than directly storing the mnemonic content itself'. Reclassified, that case's genuine-discriminator push moves from -0.30 to about -0.02 toward H1. The pre-cutoff literature strongly supported content-selective persistent PFC activity; whether that counts against a control account was the interpretive crux of the dispute itself, which the resolving study settled with a causal manipulation not yet performed at the cutoff. Treat every per-case attribution as provisional pending expert review of the score-moving nodes.

Read the directional cases by *what drove the ranking*, not by whether it matched: a match driven by manufactured opposition is not a success, and a mismatch driven by it is a method failure rather than an absence of evidence. For `mixed`, `regime_dependent` and `component_wise` cases there is no winner to match; the table shows only what the system leaned on.

Ordinal→numeric mappings are placeholders (`v0-placeholder`); magnitudes are comparable within this run only, and only their sign and relative size carry information.

## 8. How far the audit can be trusted

| check | result |
| --- | --- |
| internal consistency (category vs per-hypothesis statuses) | 0 inconsistencies in 192 |
| test-retest, one case judged twice | category 21/24, discriminative 23/24 |
| blind second rating (executor (Claude), NOT a human domain expert), stratified sample | discriminative 18/24, full status 15/24; judge 5 vs rater 7 discriminative |
| non-verbatim reference matches | 2 — none -- both referenced discriminators already counted |

The judge and the second rater are both LLMs (the judge is the same deployment as the verifier). No human domain expert has reviewed any judgment. The auditor's disagreements are not random: it over-calls `indeterminate` and misses explicit denials in hypothesis text (X15 in pfc_storage_vs_control), plausibly because its prompt warns emphatically against reading silence as absence. Its one-sided share on the sample was 16/24 vs the second rater's 11/24.

What is robust: the structural comparison (section 3, no judge involved); that silence-driven contrast is a large share of the opposition under either rater; and the direction of the mechanism (one-sided support flows to the generating hypothesis). What is not robust: whether silence-driven contrast is a majority, and every per-case failure attribution.

`/mnt/data/knk25.data/hypothesis_verification/runs/pilot_explanatory_001/manual_review/score_moving_nodes_for_expert_review.json` lists every node that moved a ranking, ordered by influence, with blank fields for a human domain expert.

## 9. Artifacts

- `/mnt/data/knk25.data/hypothesis_verification/runs/pilot_explanatory_001/summary.json`
- `/mnt/data/knk25.data/hypothesis_verification/runs/pilot_explanatory_001/leak_audit.json`
- `/mnt/data/knk25.data/hypothesis_verification/runs/pilot_explanatory_001/recovery.json`
- `/mnt/data/knk25.data/hypothesis_verification/runs/pilot_explanatory_001/evidence_discovery.json`
- `/mnt/data/knk25.data/hypothesis_verification/runs/pilot_explanatory_001/hypothesis_comparison.json`
- `/mnt/data/knk25.data/hypothesis_verification/runs/pilot_explanatory_001/ranking_attribution.json`
- `/mnt/data/knk25.data/hypothesis_verification/runs/pilot_explanatory_001/audit_checks.json`
- `/mnt/data/knk25.data/hypothesis_verification/runs/pilot_explanatory_001/manual_review/` — blind sample and compared ratings
- per-case forensics: `/mnt/data/knk25.data/hypothesis_verification/runs/pilot_explanatory_001/instances/<case_id>/` — `input.json`, `graph.json`, `edge_judgments.json`, `queries.json`, `retrieval.json`, `evidence.json`, `scores.json`, `model_outputs.json`, `events.jsonl`, `report.md`
