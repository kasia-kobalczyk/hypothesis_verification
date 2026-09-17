# DIRECTIVE — BENCH-GRAPH-V4-SCOPE-001

## Objective
Continue v4 development on the existing eight spent development cases by addressing the remaining failure exposed in `BENCH-GRAPH-V4-DEV-001`:

> Prediction-state gating now works, but proposition scope and evidence matching still allow broad/generic possibility claims to score while scientifically specific discriminators often receive only `partial` evidence and are excluded.

Implement and validate a new **comparative-scope + contrast-bearing-element layer** before comparative evidence aggregation.

Do not freeze v4 yet. Do not consume any held-out benchmark cases.

---

# PART I — DEVELOPMENT CONTEXT

## 1. Preserve existing v3 and v4 runs
Do not overwrite:
- the frozen v3 eight-case pilot;
- D045/D046 adjudications;
- attribution analyses;
- previous v4 development runs.

Use new versioned run IDs/directories.

## 2. Keep the current prediction-state gate
Retain the successful v4 state representation:
- `positive_or_present`
- `negative_or_absent`
- `substantive_null`
- `indeterminate`

Retain the rule:
- `indeterminate` contributes zero direct relative score;
- one-sided predictions are retained descriptively but not directly comparative;
- mixed/shared predictions do not score unless they contain a meaningful determinate contrast.

Do not regress this behavior.

---

# PART II — ADD COMPARATIVE SCOPE

## 3. Introduce a separate proposition-scope classifier
For every proposition that survives prediction-state gating as potentially comparative, classify its scientific scope independently from prediction state.

Use a schema such as:

- `hypothesis_specific`
  - proposition directly instantiates a distinctive commitment of the candidate hypothesis in the case-specific system;

- `mechanism_specific`
  - proposition tests a mechanism central to the candidate explanation and remains meaningfully diagnostic in the target system, even if phrased mechanistically rather than case-specifically;

- `broader_class_fact`
  - proposition describes a general property of a wider class/system family that may be true regardless of which candidate explanation is correct;

- `possibility_claim`
  - proposition merely states that a mechanism/event *can* occur somewhere/in some related system, without showing that it is expected to govern the target phenomenon;

- `invalid_or_underspecified`
  - proposition is too vague, weakly implied, or not operationally meaningful enough to support comparative inference.

Important:
- Scope classification must be separate from prediction-state classification.
- Do not overload the prediction-state prompt with scope judgments.
- Do not infer `hypothesis_specific` merely because the proposition was generated from one hypothesis.

## 4. Comparative scoring eligibility by scope
For direct comparative scoring, default eligibility should require:
- `hypothesis_specific` OR `mechanism_specific`;
- AND a determinate cross-hypothesis contrast from the existing prediction-state gate.

Default ineligible for direct comparative score:
- `broader_class_fact`
- `possibility_claim`
- `invalid_or_underspecified`

Preserve ineligible propositions for descriptive analysis and future work; do not delete them from the graph.

## 5. Use development labels to validate, not to hard-code
Use D045/D046 as development annotations to test whether known generic/component facts are mapped to broader/non-comparative scope and known genuine discriminators remain specific enough to score.

Do not add case-specific rules.

---

# PART III — IDENTIFY THE CONTRAST-BEARING ELEMENT

## 6. Decompose eligible propositions
For every proposition that is both:
- prediction-contrastive; and
- scope-eligible (`hypothesis_specific` or `mechanism_specific`),

extract a structured **contrast-bearing element**.

Represent, where possible:
- `shared_context`
- `contrast_variable`
- `contrast_direction_or_state`
- `system_or_population`
- `measurement_or_observable`

Example:

Proposition:
> In GlnBP, ligand binding precedes the open-to-closed conformational transition.

Possible decomposition:
- shared_context: glutamine binding to E. coli GlnBP
- contrast_variable: temporal ordering of ligand association vs conformational closure
- contrast_direction_or_state: binding occurs before closure
- measurement_or_observable: kinetic ordering / exchange measurements

The decomposition should isolate the piece that actually distinguishes the hypotheses.

## 7. Do not require perfect symbolic parsing
This does not need to become a brittle ontology.

A compact structured representation is sufficient if it lets the evidence assessor answer:

> Does the cited evidence directly bear on the specific contrast that makes this proposition discriminative?

Preserve the original proposition text alongside the decomposition.

---

# PART IV — REWORK EVIDENCE MATCHING AROUND THE CONTRAST

## 8. Replace whole-proposition `direct/partial/mismatch` gating with contrast-focused relevance
The prior v4 `construct_match` check was too coarse: specific discriminators often received `partial` because historical studies addressed the contrast-bearing measurement without proving the full proposition wording.

Add a narrow evidence judgment focused on the contrast-bearing element.

Suggested schema:

- `contrast_direct`
  - evidence directly measures/tests the variable/state that carries the hypothesis contrast;

- `contrast_partial`
  - evidence addresses the correct variable but only incompletely, indirectly, or in a partially mismatched condition/system;

- `context_only`
  - evidence supports background/shared context but not the discriminating element;

- `construct_mismatch`
  - evidence concerns a different construct/measurement;

- `no_evidence`

For comparative scoring, default to:
- `contrast_direct` eligible;
- `contrast_partial` NOT automatically eligible in the main method, but preserve it for sensitivity analysis;
- `context_only`, `construct_mismatch`, `no_evidence` contribute zero comparative score.

## 9. Sensitivity analysis for `contrast_partial`
Run a clearly separated sensitivity analysis where `contrast_partial` is allowed with a conservative policy.

Do NOT use this sensitivity result to define the main method unless it is stable and scientifically interpretable.

Report:
- number of additional scored nodes;
- human-reviewed category composition;
- effect on score stability;
- whether generic/component facts re-enter through partial evidence.

---

# PART V — SPECIFICITY-ASSESSABILITY DIAGNOSTIC

## 10. Explicitly measure the specificity–assessability tradeoff
For every generated proposition, record:
- scope class;
- prediction-profile type;
- whether historical evidence exists;
- evidence contrast-match category;
- whether it scores.

Produce a table crossing:

`scope` × `evidence availability / contrast relevance`

Key question:
- Are hypothesis/mechanism-specific discriminators systematically less historically assessable than broad class facts?

Quantify this rather than only describing it qualitatively.

## 11. Preserve one-sided evidence separately
Continue retaining one-sided but non-comparative propositions and their evidence in a descriptive bucket.

Do not let scope changes accidentally turn one-sided support into comparative evidence.

---

# PART VI — DEVELOPMENT VALIDATION

## 12. Validate on the same eight spent cases only
Run the updated method on all eight development cases using:
- same cutoffs;
- same literature harness;
- same provider/model roles where practical;
- same consequence-generation settings unless required by the new metadata schema.

Use multiple replicates because previous development runs showed meaningful run-to-run noise.

Minimum:
- 3 independent v4-scope replicates per case if cost is manageable;
- if not, use the highest feasible number and document limitations.

## 13. Structural development metrics
Compare prior v4 vs v4-scope on:

### Prediction-state preservation
- indeterminate rate;
- one-sided profiles;
- determinate-vs-determinate contrast rate;
- regression against D046 state labels.

### Scope behavior
- counts by scope class;
- D045/D046 human-category distribution within each scope;
- proportion of reviewed `generic_component_fact` nodes rejected from comparative scoring;
- proportion of reviewed `genuine_discriminator` nodes retained.

### Contrast-bearing evidence behavior
- counts of `contrast_direct`, `contrast_partial`, `context_only`, `mismatch`;
- how often reviewed genuine discriminators receive contrast-direct evidence;
- how often generic/component facts receive only context/background support yet would previously have scored.

### Score-influence composition
Estimate share of comparative score influence attributable to reviewed:
- genuine discriminators;
- silence errors;
- generic component facts;
- compatible non-discriminative facts;
- construct mismatch;
- invalid/weak implications.

Desired direction:
- genuine share materially increases;
- invalid/non-discriminative share materially decreases.

### Consequence discovery preservation
Re-run hidden consequence-recovery analysis after runs are frozen.

Verify that reference-discriminator recovery does not collapse relative to v3/v4.

---

# PART VII — DEVELOPMENT SUCCESS CRITERIA

## 14. Main criteria
Do not use raw 8-case accuracy as the primary objective.

A successful iteration should show:

1. prediction-state performance from prior v4 remains intact;
2. broad class/possibility claims are largely excluded from comparative scoring;
3. reviewed genuine discriminators are retained when scientifically specific;
4. evidence must bear on the contrast-bearing element, not merely shared context;
5. score influence from generic/component facts and construct mismatch drops materially;
6. genuine-discriminator share of score influence increases;
7. consequence-generation breadth/recovery remains substantially preserved;
8. replicate behavior is more stable or at least no less interpretable.

## 15. It is acceptable for cases to become ties/uncertain
If no pre-cutoff contrast-direct evidence exists, the correct v4-scope outcome may be:
- tie;
- weak support;
- insufficient evidence.

Do not force directional conclusions to match later resolvers.

---

# PART VIII — ITERATION POLICY

## 16. Limited iteration allowed
These eight cases remain an explicit development set.

You may:
- fix implementation bugs;
- refine the scope-classification prompt/schema;
- refine contrast-element extraction;
- refine the narrow evidence-relevance prompt;
- rerun the eight development cases.

But:
- document every change;
- do not encode case-specific rules;
- do not tune numeric mappings to maximize later-resolution agreement;
- do not expose hidden resolver observations to verifier prompts;
- do not consume held-out cases.

## 17. Do not freeze unless criteria are met
If the method still scores mostly generic facts, loses genuine discriminators, or is unstable, leave v4 unfrozen and report the blocker.

---

# PART IX — REQUIRED OUTPUTS

Create repository-native artifacts for:

1. scope-classification schema and prompt/spec.
2. contrast-bearing-element schema/extractor.
3. contrast-focused evidence-relevance schema/prompt.
4. deterministic comparative gating updates.
5. tests covering:
   - scope separation from prediction state;
   - broad-class/possibility gating;
   - contrast-element extraction;
   - context-only evidence excluded from score;
   - prediction-state regression against D046 examples.
6. replicated development runs on the eight spent cases.
7. prior-v4 vs v4-scope structural comparison.
8. scope × evidence-assessability table.
9. score-influence composition report using D045/D046 labels.
10. consequence-recovery comparison.
11. development recommendation: freeze or continue iterating.

Report must include:
- exact git commit(s);
- model/provider/configuration;
- run paths;
- number of iterations/replicates;
- every methodological change;
- confusion/coverage against D045/D046 reviewed nodes;
- which reviewed generic facts were successfully gated;
- which reviewed genuine discriminators remained eligible;
- how many scored nodes are hypothesis/mechanism-specific versus broad/possibility claims;
- evidence contrast-match distribution;
- score-influence composition;
- replicate stability;
- whether the method is ready to freeze for held-out evaluation.

---

# DO NOT

Do not:
- modify or consume held-out cases;
- freeze automatically at the end;
- combine scope classification into the prediction-state prompt unless a documented experiment proves separation is impossible;
- treat `broader_class_fact` or `possibility_claim` as comparative evidence merely because literature directly supports them;
- treat context/background evidence as support for the contrast-bearing element;
- allow `indeterminate` to contribute direct relative score;
- use hidden resolver observations in verifier context;
- reuse the spent ResearchBench reserve;
- optimize on final case-level correctness.

---

# Acceptance criteria
This task is complete when:
1. proposition scope is explicitly classified separately from prediction state;
2. only hypothesis/mechanism-specific, determinate contrasts are eligible for direct comparative scoring;
3. each scored proposition has an explicit contrast-bearing element;
4. evidence relevance is judged against that contrast-bearing element rather than whole-proposition/background context;
5. context-only and construct-mismatch evidence contribute zero comparative score;
6. replicated development runs are completed on the eight spent cases;
7. score influence shifts away from generic/component facts toward genuine discriminators without collapsing consequence discovery;
8. the report makes a clear freeze-vs-continue recommendation based on structural criteria, not 8-case accuracy.