# DIRECTIVE — BENCH-GRAPH-V4-DEV-001

## Objective
Implement and validate a **v4 discrimination-gated consequence-graph verifier** using the existing eight explanatory-hypothesis pilot cases as an explicit DEVELOPMENT SET.

The purpose is to repair the structural failure identified in the frozen v3 pilot:

1. hypotheses that are merely silent/indeterminate about a proposition are sometimes labeled `unlikely`/contradicted;
2. even when silence is correctly labeled `neutral`, the current ordinal probability mapping lets one-sided propositions move relative hypothesis scores;
3. generic/component-level truths and compatible facts can accumulate literature support and influence rankings despite not genuinely distinguishing the candidate explanations;
4. evidence about a related construct can be scored as if it directly bears on the proposition.

The v4 experiment should test whether an explicit **cross-hypothesis prediction-state gate** can preserve useful consequence discovery while preventing non-discriminative propositions from driving comparative scores.

The eight existing pilot cases are now spent and may be used freely for method development/debugging. They must NOT later be treated as held-out evidence of generalization.

---

# PART I — DEVELOPMENT-SET STATUS

## 1. Development cases
Use exactly the existing eight frozen ACCEPT cases already materialized in the repository:

1. `pfc_storage_vs_control`
2. `gcn4_med15_complex_vs_condensate`
3. `eukaryogenesis_mito_timing`
4. `pfc_interhemispheric_architecture`
5. `glnbp_induced_fit_vs_conformational_selection`
6. `spider_orb_web_origin`
7. `forest_fragmentation_resilience`
8. `fly_wing_constraint_vs_selection`

Continue using the same frozen cutoffs and hidden annotations.

These eight cases may be inspected during development. They are not a holdout.

## 2. Preserve v3 baseline
Do not overwrite the frozen v3 pilot.

All v4 runs must live under new run IDs/directories and preserve direct comparability with:
- the original frozen v3 eight-case pilot;
- the D045/D046 human adjudications;
- the deterministic attribution analysis.

---

# PART II — V4 DESIGN PRINCIPLE

## 3. Separate prediction state from prediction strength
Replace the current single ordinal edge interpretation for comparative scoring with an explicit two-stage representation.

For every `(hypothesis, proposition)` pair, first classify **prediction state** as one of:

- `positive_or_present`
  - the hypothesis substantively predicts/increases/expects the proposition;
- `negative_or_absent`
  - the hypothesis substantively predicts the opposite/incompatibility;
- `substantive_null`
  - the hypothesis positively predicts no effect / baseline / no change;
- `indeterminate`
  - the hypothesis does not determine the proposition.

Important:
- `indeterminate` is NOT a null prediction.
- `neutral` from the old ordinal scheme must not automatically be treated as `substantive_null`.
- A hypothesis may be compatible with a proposition while still being `indeterminate` about it.

After state classification, assess **prediction strength/confidence** only for determinate states (`positive_or_present`, `negative_or_absent`, `substantive_null`) if the existing architecture needs graded strength.

Do not map `indeterminate` to a pseudo-likelihood such as 0.5 for comparative scoring.

## 4. Cross-hypothesis prediction profile
For every proposition, construct an explicit prediction profile across ALL candidate hypotheses before literature evidence can affect relative hypothesis scores.

Example:

`X -> {H1: positive_or_present, H2: indeterminate}`

must be represented differently from:

`X -> {H1: positive_or_present, H2: negative_or_absent}`

## 5. Discrimination gate
A proposition is eligible to contribute to **relative hypothesis comparison** only when at least two candidate hypotheses make determinate, meaningfully different predictions.

Eligible examples:
- positive vs negative
- positive vs substantive_null
- negative vs substantive_null
- two positive predictions with explicitly different quantitative/range/directional commitments, if the architecture supports such comparisons and the distinction is scientifically meaningful

Ineligible for direct comparative scoring:
- positive vs indeterminate
- negative vs indeterminate
- substantive_null vs indeterminate
- indeterminate vs indeterminate
- positive vs positive where both predict the same relevant outcome

Do not delete ineligible propositions from the graph. Preserve them for:
- consequence-generation analysis;
- descriptive support for a single hypothesis;
- future probabilistic/background-rate work.

But they must not generate a likelihood ratio or otherwise move **relative** hypothesis scores in v4.

## 6. One-sided evidence bucket
Create an explicit non-comparative bucket for propositions where one hypothesis makes a determinate prediction and another is indeterminate.

Record:
- which hypothesis predicts the proposition;
- evidence support/contradiction for that proposition;
- why it was gated out of relative scoring.

Do not silently discard this information.

The report should make clear that one-sided support may become informative in a future explicit background-probability model, but v4 intentionally does not treat it as comparative evidence.

---

# PART III — GENERIC / COMPONENT FACT CONTROL

## 7. Distinguish discrimination from mere assessability
Add an explicit proposition-level comparative classification after cross-hypothesis prediction states are known.

Suggested labels:
- `comparative_discriminator`
- `one_sided_prediction`
- `shared_prediction`
- `generic_component_fact`
- `invalid_or_unsupported`

Do not determine `generic_component_fact` simply from abstraction level. Use the actual cross-hypothesis relation.

A proposition should be treated as a generic/component fact when:
- it is a true/assessable mechanism/class statement;
- its literature support does not preserve what is distinctive about the candidate explanation;
- it is similarly compatible with multiple candidates or only appears discriminative because one competitor was incorrectly given a negative edge.

Generic/component facts must not influence relative hypothesis scores unless their prediction profile contains a real determinate contrast.

## 8. Preserve consequence-generation outputs
Do NOT simplify the generator so aggressively that it only proposes obvious binary discriminators.

The project still cares about rich “what else should be true?” reasoning.

The repair should happen primarily in:
- cross-hypothesis prediction-state adjudication;
- proposition comparative gating;
- aggregation eligibility.

Do not remove mechanistic/class-level generation merely because some such propositions were non-discriminative in v3.

---

# PART IV — EVIDENCE CONSTRUCT MATCH

## 9. Add proposition-level construct check before score use
Before evidence can influence a scored proposition, explicitly determine whether the cited study/span addresses the proposition as stated rather than a related construct.

Add or adapt an evidence-level field such as:
- `construct_match = direct | partial | mismatch`

Guidance:
- `direct`: study measures/tests the proposition or a scientifically equivalent construct;
- `partial`: study bears on part of the proposition but does not fully instantiate it;
- `mismatch`: evidence is grounded but addresses a different construct.

Examples from development review:
- PFC decodability / representational information is not automatically evidence that PFC is the causal storage substrate.
- Orb-weaving across multiple families is not by itself evidence that those occurrences evolved convergently.

Comparative score use should require `direct` or a clearly justified `partial` policy. A `mismatch` must contribute zero comparative evidence.

If adding this as a new LLM judgment, keep it narrow and proposition-focused. Do not ask the evidence assessor to perform hidden scientific bridging.

---

# PART V — MINIMAL IMPLEMENTATION PRINCIPLE

## 10. Reuse existing architecture
Inspect current modules and implement the smallest clean general change.

Prefer:
1. new explicit prediction-state output from the cross-hypothesis/edge assessor;
2. a deterministic discrimination gate;
3. aggregation that excludes `indeterminate` comparisons from relative scoring;
4. construct-match gating at evidence use.

Avoid rewriting the whole graph architecture.

## 11. Keep v3 intact
Do not alter historical v3 run behavior or overwrite its code path if avoidable.

Implement v4 as a versioned method/configuration so we can run v3 and v4 side-by-side on the same development cases.

Document exact differences between versions.

---

# PART VI — DEVELOPMENT VALIDATION ON THE 8 SPENT CASES

## 12. Run v4 on all eight development cases
Use the same:
- benchmark inputs;
- cutoffs;
- literature provider/harness;
- model roles/providers where practical;
- consequence-generation settings unless a minimal schema change is required.

Do not alter hidden benchmark annotations.

## 13. Primary development metrics
Compare v3 vs v4 on:

### A. Prediction-state behavior
- number/fraction of `(hypothesis, proposition)` pairs classified `indeterminate`;
- number of determinate-vs-determinate contrasting profiles;
- number of one-sided profiles;
- number of shared/non-discriminative profiles.

### B. Comparative-score eligibility
- fraction of generated nodes eligible for relative scoring;
- fraction gated as one-sided;
- fraction gated as shared;
- fraction gated as generic/component;
- fraction gated due to construct mismatch.

### C. Human-review alignment
Using D045 and D046 as DEVELOPMENT annotations only, measure:
- whether known silence-as-null errors are now `indeterminate` and gated;
- whether known generic/compatible facts stop contributing relative score;
- whether known construct mismatches are blocked;
- whether the reviewed genuine discriminators remain eligible and retain influence.

Do NOT optimize solely for reproducing the human labels node-by-node. Use them to diagnose the intended behavior.

### D. Score-influence composition
For v3 and v4, estimate/share:
- genuine reviewed discriminator influence;
- silence-error influence;
- generic/component influence;
- compatible non-discriminative influence;
- construct-mismatch influence;
- unreviewed influence.

Success means invalid/non-discriminative categories materially lose relative score influence while genuine discriminator influence is preserved or increased in share.

### E. Consequence-discovery preservation
Re-run the hidden post-hoc consequence-recovery analysis after v4 runs are frozen.

Compare v3 vs v4:
- reference discriminator recovery;
- number of plausible novel discriminators;
- total proposition diversity/count;

The repair should not achieve cleaner scoring merely by collapsing consequence generation.

---

# PART VII — DEVELOPMENT SUCCESS CRITERIA

## 14. Core success criterion
The main development criterion is NOT raw case-level accuracy.

The desired pattern is:

`share_of_score_influence_from_genuine_discriminators` increases

while:

`silence + generic/component + construct-mismatch influence` decreases substantially.

At minimum, verify on the D045/D046 reviewed nodes that:
- `indeterminate` competitors contribute zero direct relative score;
- propositions judged generic/compatible no longer gain relative influence solely from cross-hypothesis `unlikely` judgments;
- construct mismatches contribute zero relative score;
- the four D045 genuine discriminators remain score-eligible unless v4 provides a documented scientific reason otherwise.

## 15. Case-level expectations are diagnostic only
Pay special attention to:

### PFC storage vs control
Expected development behavior:
- construct-mismatch and silence-driven support for storage should be suppressed;
- reviewed genuine control-favoring discriminators should remain usable.

### GlnBP
Expected development behavior:
- silence-driven induced-fit advantage should disappear;
- genuine mechanistic discriminators should remain;
- if the resulting direction changes or becomes uncertain, report that honestly rather than forcing agreement with the later resolver.

### Eukaryogenesis
Expected development behavior:
- generic component facts should no longer dominate relative score;
- if no genuine pre-cutoff discriminator remains, the system should be allowed to become uncertain.

### Fly-wing
Expected development behavior:
- silence-driven apparent success should disappear;
- uncertainty/tie is preferable to a correct answer for invalid reasons.

Mixed/regime-dependent cases must not be forced into binary winners.

---

# PART VIII — ITERATION POLICY ON DEVELOPMENT SET

## 16. Limited development iteration is allowed
Because these eight cases are explicitly spent development cases, you may:
- inspect v4 failures;
- fix implementation bugs;
- make principled prompt/schema refinements directly tied to the known failure class;
- rerun the eight development cases.

However:
- document every methodological change;
- do not make case-specific rules;
- do not encode benchmark answers/resolving outcomes into prompts;
- do not add domain-specific exceptions for individual cases;
- do not tune numeric mappings to maximize eight-case final agreement.

Stop iterating once the structural success criteria are met and behavior is stable enough to freeze.

## 17. Freeze before held-out evaluation
Once v4 development is complete:
- freeze prompts;
- freeze prediction-state definitions;
- freeze gating rules;
- freeze aggregation semantics;
- freeze construct-match policy;
- freeze model/provider configuration as far as practical.

Create a clear method/version identifier, e.g.:
- `consequence_graph_v4_discrimination_gated`

Do not evaluate on future held-out cases until this freeze is recorded.

---

# PART IX — HELD-OUT PLAN (DO NOT EXECUTE YET)

## 18. Future held-out evaluation
Do not consume new benchmark cases in this directive.

After v4 freeze, the Research Director will supply additional accepted cases not used during method development.

Target eventual structure:
- 8 development cases = current spent tranche;
- ~8–12 new held-out accepted cases;
- larger ~20-case benchmark if construction permits.

The held-out set will be the first valid evidence of generalization for v4.

---

# PART X — REQUIRED OUTPUTS

Create repository-native artifacts for:

1. v4 design/specification document.
2. implementation changes with tests.
3. explicit prediction-state schema.
4. deterministic discrimination-gating logic.
5. construct-match evidence gating.
6. one or more v4 development runs on the eight spent cases.
7. v3-vs-v4 structural comparison report.
8. v3-vs-v4 score-influence composition report using D045/D046 development labels.
9. consequence-discovery comparison.
10. freeze report once development criteria are met.

The report must include:
- exact git commit(s);
- configuration/model/provider settings;
- all run paths;
- number of development iterations;
- every methodological change made between iterations;
- prediction-state confusion against D045/D046 reviewed nodes where available;
- number of one-sided propositions gated;
- number of generic/shared propositions gated;
- construct-match failures blocked;
- score-influence composition before/after;
- per-case qualitative changes;
- whether consequence discovery was preserved;
- whether v4 is ready to freeze for held-out evaluation.

---

# DO NOT

Do not:
- claim held-out performance from these eight development cases;
- use future held-out cases during this task;
- optimize final ranking accuracy on the eight as the primary objective;
- create case-specific exceptions;
- reintroduce `indeterminate` as a numeric pseudo-likelihood for comparative scoring;
- equate `indeterminate` with `substantive_null`;
- discard all one-sided predictions from the graph;
- remove mechanistic consequence generation simply to make scoring cleaner;
- expose hidden resolver material to verifier prompts;
- reuse the spent ResearchBench reserve;
- force mixed/regime-dependent benchmark items into binary winners.

---

# Acceptance criteria
This task is complete when:
1. v4 explicitly separates prediction state from prediction strength;
2. `indeterminate` hypotheses contribute zero direct relative score;
3. proposition-level discrimination gating occurs before comparative evidence aggregation;
4. one-sided predictions are retained descriptively but excluded from direct relative scoring;
5. evidence construct mismatch cannot influence relative scores;
6. v3 remains reproducible and untouched;
7. v4 is run/debugged on the eight spent development cases;
8. D045/D046 failure categories lose substantial relative-score influence while genuine discriminators remain usable;
9. consequence discovery does not collapse;
10. the resulting v4 method is frozen and documented before any held-out cases are used.

A development run becoming less decisive or more uncertain is acceptable and may be preferable if v3 confidence was driven by invalid discrimination.