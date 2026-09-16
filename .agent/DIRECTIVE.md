# DIRECTIVE — BENCH-GRAPH-ATTRIBUTION-001

## Objective
Take the completed human adjudication of the 40-node high-influence review packet and mechanically recompute score attribution for the frozen eight-case explanatory-benchmark pilot.

This is an **analysis-only** task. Do not modify the verifier, do not rerun any LLM or literature retrieval, and do not tune the method.

The purpose is to answer:

> How much of each case’s frozen verifier score/ranking was driven by genuinely discriminative reasoning versus silence errors, generic component facts, construct mismatch, weak implications, or merely compatible non-discriminative propositions?

Use the preserved frozen pilot artifacts and the Research Director adjudication recorded in decision D045 as the source of truth for the 40 priority-node labels.

---

# PART I — LOAD AND ENCODE HUMAN ADJUDICATION

## 1. Locate the preserved review artifacts
Use the existing preserved packet under the repository review/frozen-run locations created by `BENCH-GRAPH-REVIEW-001`.

Expected review family:
- `benchmark/review/graph_pilot_001/`

Verify exact paths rather than assuming them.

## 2. Encode the 40 priority-node labels from D045
Populate the human-review fields for the 40 priority nodes exactly according to the Research Director adjudication below.

Primary category mapping:

1. `pfc_storage_vs_control-X2` — `silence_as_null_error`
2. `glnbp-X4` — `silence_as_null_error`
3. `eukaryogenesis-X7` — `invalid_or_weak_implication`
4. `glnbp-X11` — `silence_as_null_error`
5. `gcn4-X3` — `generic_component_fact`
6. `glnbp-X3` — `generic_component_fact`
7. `glnbp-X5` — `genuine_discriminator`
8. `forest-X1` — `compatible_non_discriminative`
9. `eukaryogenesis-X4` — `generic_component_fact`
10. `eukaryogenesis-X6` — `generic_component_fact`
11. `forest-X7` — `compatible_non_discriminative`
12. `pfc_interhemispheric-X2` — `compatible_non_discriminative`
13. `fly_wing-X2` — `silence_as_null_error`
14. `pfc_storage_vs_control-X6` — `genuine_discriminator`
15. `forest-X4` — `compatible_non_discriminative`
16. `forest-X5` — `compatible_non_discriminative`
17. `gcn4-X5` — `compatible_non_discriminative`
18. `glnbp-X15` — `generic_component_fact`
19. `pfc_storage_vs_control-X15` — `evidence_construct_mismatch`
20. `pfc_storage_vs_control-X24` — `genuine_discriminator`
21. `eukaryogenesis-X24` — `generic_component_fact`
22. `glnbp-X8` — `generic_component_fact`
23. `glnbp-X9` — `genuine_discriminator`
24. `pfc_storage_vs_control-X14` — `evidence_construct_mismatch`
25. `glnbp-X6` — `generic_component_fact`
26. `pfc_storage_vs_control-X3` — `compatible_non_discriminative`
27. `eukaryogenesis-X2` — `silence_as_null_error`
28. `eukaryogenesis-X10` — `generic_component_fact`
29. `eukaryogenesis-X12` — `generic_component_fact`
30. `eukaryogenesis-X22` — `generic_component_fact`
31. `forest-X23` — `silence_as_null_error`
32. `spider-X12` — `generic_component_fact`
33. `forest-X24` — `silence_as_null_error`
34. `glnbp-X17` — `compatible_non_discriminative`
35. `pfc_storage_vs_control-X13` — `evidence_construct_mismatch`
36. `forest-X15` — `invalid_or_weak_implication`
37. `gcn4-X18` — `generic_component_fact`
38. `gcn4-X23` — `generic_component_fact`
39. `gcn4-X9` — `silence_as_null_error`
40. `spider-X11` — `invalid_or_weak_implication`

Do not alter these primary categories.

## 3. Human label metadata
For each of the 40 nodes, set:
- `human_primary_category` to the frozen value above;
- `human_is_genuinely_discriminative = true` only for `genuine_discriminator`;
- `human_silence_as_null_error = true` only for `silence_as_null_error`;
- leave any more detailed per-hypothesis prediction fields blank unless they were explicitly recorded in D045 or can be transcribed from existing Research Director notes without inference.

Do not invent missing human judgments.

Mark provenance clearly, e.g.:
- `human_reviewer = "Research Director"`
- `human_review_source = "D045"`
- `human_review_status = "first_pass_model_based_review"`

Important: this review is model-based Research Director adjudication, not external expert ground truth.

---

# PART II — RECOMPUTE SCORE ATTRIBUTION MECHANICALLY

## 4. Preserve the original frozen scores
Before any counterfactual analysis, reproduce the original per-case score/log-odds contributions from the frozen run exactly within numerical tolerance.

Do not call any model.

For each case record:
- original hypothesis scores/log-odds;
- original ordering/support summary;
- total absolute node contribution;
- contribution from the 40 reviewed priority nodes;
- contribution from unreviewed score-moving nodes.

## 5. Attribute reviewed-node influence by human category
For each case and each hypothesis, sum the signed and absolute contribution of reviewed nodes in these categories:
- `genuine_discriminator`
- `silence_as_null_error`
- `generic_component_fact`
- `compatible_non_discriminative`
- `evidence_construct_mismatch`
- `invalid_or_weak_implication`

Also report totals across all eight cases.

Where the original scoring contribution is pairwise or path-mediated rather than trivially node-local, use the exact deterministic decomposition already available from the frozen-run analysis. If attribution cannot be uniquely decomposed, document the limitation rather than approximating silently.

## 6. Construct counterfactual score views
Without changing any underlying model judgment, generate deterministic counterfactual score summaries by zeroing/removing contributions from reviewed nodes according to category.

At minimum create these views:

### View A — `genuine_only_reviewed`
Keep contribution from reviewed `genuine_discriminator` nodes only; zero all other reviewed-node contributions.

Unreviewed score-moving nodes should be reported separately and should not be silently treated as valid or invalid.

Produce two variants if useful:
- A1: reviewed genuine only + all unreviewed contributions untouched;
- A2: reviewed genuine only, with all unreviewed score-moving contributions set aside/zeroed.

### View B — `remove_confirmed_errors`
Zero reviewed nodes in:
- `silence_as_null_error`
- `evidence_construct_mismatch`
- `invalid_or_weak_implication`

Keep reviewed:
- genuine discriminators;
- generic component facts;
- compatible non-discriminative nodes;

This isolates the effect of clearly erroneous reasoning from merely weak/non-discriminative evidence.

### View C — `discriminative_only`
Keep only reviewed `genuine_discriminator` contributions and set aside reviewed:
- silence errors;
- generic component facts;
- compatible non-discriminative;
- construct mismatch;
- weak implications.

Again, handle unreviewed nodes explicitly rather than assuming validity.

### View D — `remove_non_discriminative_reviewed`
Keep reviewed genuine discriminators only; remove reviewed generic/compatible/error categories, while leaving unreviewed contributions untouched.

If A/D overlap, simplify but preserve at least one view with unreviewed nodes untouched and one strict reviewed-only view.

## 7. Do not reinterpret mixed-resolution cases as binary accuracy
For each case, compare counterfactual support to the benchmark resolution type only descriptively.

Allowed benchmark resolutions include:
- favored;
- mixed;
- regime-dependent;
- component-wise.

Do not convert mixed/regime-dependent cases to a forced winner metric.

---

# PART III — CASE-LEVEL DIAGNOSTIC REPORT

## 8. For every case, report
- original score/order;
- total reviewed-node influence;
- genuine-discriminator contribution;
- silence-error contribution;
- generic-component contribution;
- compatible-non-discriminative contribution;
- construct-mismatch contribution;
- weak-implication contribution;
- unreviewed score-moving contribution;
- counterfactual ordering/support under each view;
- whether the original apparent agreement/disagreement with later resolution survives after confirmed-error removal;
- whether any conclusion becomes underdetermined once non-discriminative reviewed nodes are removed.

## 9. Pay special attention to four cases
### GlnBP
Determine whether its apparent successful support for induced fit survives using only genuine reviewed discriminators.

### Eukaryogenesis
The earlier analysis suggested correct final direction but substantial manufactured contrast. Quantify exactly how much support remains after removing reviewed invalid/generic/silence contributions.

### Fly-wing
Earlier analysis suggested a correct final direction with no genuine recovered discriminator in the priority set. Determine whether the apparent success disappears under reviewed attribution.

### PFC storage vs control
The frozen verifier favored the later-disfavored storage account. Determine how much of that failure is attributable to construct mismatch, silence errors, versus genuinely discriminative nodes.

---

# PART IV — OPTIONAL SENSITIVITY USING FULL 78-NODE SET

## 10. Do not invent labels for the remaining 38 score-moving nodes
The remaining score-moving nodes are not yet human-adjudicated.

However, produce a transparent influence summary showing:
- how much absolute score influence is already covered by the 40 adjudicated nodes;
- how much remains in the 38 unreviewed nodes;
- which cases are under-covered by the priority review.

If the existing packet identifies case-coverage additions previously suggested for fly-wing, interhemispheric PFC, and spider, list them as the recommended next human-review batch.

Do not auto-label these nodes in this directive.

---

# PART V — OUTPUTS

## 11. Machine-readable outputs
Create repository-native artifacts containing:
- updated review JSONL with D045 labels encoded;
- per-node contribution table;
- per-case category attribution table;
- counterfactual scores/orderings under each deterministic view;
- coverage statistics for reviewed vs unreviewed score-moving nodes.

## 12. Human-readable report
Create a concise report summarizing:
- how much frozen score influence is explained by each adjudicated category;
- which apparent pilot successes remain credible after review;
- which disappear or become underdetermined;
- which cases require review of additional nodes before firm attribution;
- whether the dominant problem is best characterized as silence handling alone or a broader discrimination/relevance problem.

The report should clearly distinguish:
- observed frozen verifier behavior;
- human-adjudicated node categories;
- deterministic counterfactual arithmetic;
- interpretive conclusions.

## 13. Update executor report/state
Report exact paths to all created artifacts and the git commit containing this analysis.

---

# PART VI — DO NOT

Do not:
- modify the verifier;
- change prompts, mappings, priors, aggregation, retrieval, or graph generation;
- rerun any of the eight pilot cases;
- call an LLM to relabel the remaining nodes;
- treat D045 as external expert ground truth;
- tune a silence fix using the eight spent cases;
- reuse the ResearchBench reserve;
- force mixed/regime-dependent benchmark cases into binary accuracy.

If deterministic score reconstruction reveals a bug in the previous influence analysis, document it and stop before changing scientific code.

---

# Acceptance criteria
Complete when:
1. all 40 D045 labels are encoded exactly into the preserved review set;
2. original frozen scores are deterministically reproduced;
3. score influence is decomposed by human category per node/case/hypothesis;
4. counterfactual score views are produced without any model rerun;
5. the report states which apparent successes/failures survive after reviewed-error removal;
6. residual influence from the 38 unreviewed score-moving nodes is quantified explicitly;
7. no verifier behavior has been changed.

The purpose is to obtain a trustworthy causal accounting of the pilot’s scores before deciding what method component, if any, should be redesigned.