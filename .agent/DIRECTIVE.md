# DIRECTIVE — BENCH-GRAPH-PILOT-001

## Objective
Integrate the first frozen tranche of eight accepted explanatory-hypothesis benchmark cases into the existing `kasia-kobalczyk/hypothesis_verification` experiment framework and run the existing agentic consequence-graph verifier on them as a **diagnostic pilot**.

The scientific question is:

> Does the existing “what else should be true?” consequence-graph pipeline behave more appropriately when evaluated on genuine competing explanations of the same phenomenon, rather than ResearchBench-style parallel research proposals?

This is a method-diagnosis experiment, not a tuning exercise and not a claim of benchmark-scale performance.

## Critical architecture assumptions
- You are the implementation/execution agent, not the scientific verifier.
- The verifier consists of the existing API-backed agents already used by the repository.
- Use the repository’s existing `LiteratureSearchService` / `CutoffRegistry` temporal controls. Do not replace them with prompt-only cutoff instructions.
- Agents must not be able to choose, relax, or override benchmark cutoffs.
- Hidden benchmark annotations must never enter verifier prompts, retrieval queries, graph generation, evidence assessment, or scoring inputs.

## Frozen benchmark tranche
Run only these eight ACCEPT cases in this pilot:

1. PFC working-memory storage vs top-down control.
2. Gcn4/Med15 soluble-complex vs transcriptional-condensate mechanisms.
3. Eukaryogenesis mitochondria-early vs mitochondria-intermediate/late.
4. Interhemispheric PFC specialized/lateralized vs redundant/shared storage.
5. GlnBP conformational selection vs induced fit.
6. Spider orb-web ancestral single origin/loss vs convergent independent origins.
7. Forest fragmentation edge-stress/degradation vs resource-release/productivity mechanisms.
8. Fly-wing developmental/genetic constraint vs correlational-selection explanation.

Do not add BORDERLINE or REJECT cases to the main pilot.

## Step 1 — Inspect and reuse existing repository conventions
Before changing code:

1. Inspect the current benchmark/data schemas, experiment runner, cutoff registry, consequence-graph implementation, literature-search service, scoring/inference code, and run-artifact/report formats.
2. Reuse existing abstractions wherever possible.
3. Do not create a parallel benchmark framework if a small adapter or schema extension is sufficient.
4. Preserve compatibility with historical ResearchBench experiments and existing run artifacts.

Document the exact existing paths/components reused.

## Step 2 — Integrate the eight benchmark cases
Create repository-native machine-readable records for the eight cases using the frozen benchmark material supplied by the Research Director.

At minimum, verifier-visible inputs should include only:
- `case_id`
- phenomenon / scientific question
- source-faithful competing hypothesis texts
- frozen historical cutoff
- any explicitly approved pre-cutoff framing/context required by the existing runner

Keep evaluation-only material separate, including:
- reference consequence matrix / discriminating observations
- resolving study/result
- resolution label
- leakage audit
- construction rationale
- any post-cutoff source information

If the repository requires a single record containing both visible and hidden fields, implement a hard projection so only the visible subset can flow into the verifier. Add a test for this.

Do not rewrite hypotheses to make them more contrastive. Preserve their source-grounded scientific meaning.

## Step 3 — Register and verify temporal cutoffs
Register the frozen cutoff for each case in the existing cutoff machinery.

Required cutoffs:
- PFC storage vs control: `2024-01-01`
- Gcn4/Med15 soluble complex vs condensate: `2024-01-01`
- Eukaryogenesis mitochondrial timing: `2025-01-01`
- Interhemispheric PFC architecture: `2024-12-01`
- GlnBP induced fit vs conformational selection: `2024-01-01`
- Spider orb-web origin: `2026-01-01`
- Forest fragmentation/resilience: `2024-01-01`
- Fly-wing constraint vs correlational selection: `2025-01-01`

Before running the verifier, add or run checks demonstrating that:
1. literature searches are filtered by the case cutoff;
2. citation/reference expansion is also cutoff-filtered;
3. metadata/title/abstract retrieval cannot reintroduce post-cutoff records;
4. prompt rendering contains no hidden resolving annotations;
5. resolving-paper identifiers from the hidden annotations are unavailable to the verifier context.

Do not weaken existing temporal controls to accommodate a case.

## Step 4 — Run the existing consequence-graph method WITHOUT tuning
Run the existing graph-based verification method on all eight cases.

Important constraints:
- Do not tune prompts on these eight cases.
- Do not change edge-label mappings, evidence-label mappings, priors, aggregation rules, graph depth, retrieval thresholds, proposition abstraction policy, or stopping criteria in response to pilot outcomes.
- Do not inspect hidden benchmark consequences before or during graph generation.
- Do not use the old spent ResearchBench reserve for any tuning or comparison.
- If a minimal code change is required solely to support `k >= 2` hypotheses or the new input schema, make the smallest general change possible and document it.
- Preserve deterministic/frozen settings where the existing experiment framework provides them.

The purpose is to test the pre-existing scientific method on a better-aligned task, not to optimize performance.

## Step 5 — Preserve full run artifacts
For every case, retain the normal repository artifacts needed for forensic analysis, including where supported:
- rendered verifier input
- generated propositions/consequence nodes
- graph edges and implication judgments
- cross-hypothesis proposition evaluations
- literature queries
- retrieved papers and cutoff metadata
- evidence spans/judgments
- aggregation inputs
- final hypothesis scores/ranking/support summary
- model/provider/configuration identifiers
- errors/retries

A future reviewer should be able to reconstruct why the system favored or failed to favor a hypothesis.

## Step 6 — Add POST-HOC consequence-recovery evaluation
After each verifier run is complete and frozen, evaluate its generated graph against the hidden benchmark consequence annotations.

This evaluation must be outside the verifier loop and must not alter the run.

For generated propositions, assess at least these categories:
1. `reference_discriminator_recovered` — substantively matches a hidden benchmark discriminating consequence;
2. `novel_plausible_discriminator` — not in the reference matrix but appears scientifically capable of distinguishing hypotheses;
3. `compatible_non_discriminative` — scientifically plausible but similarly compatible with multiple candidates;
4. `generic_component_fact` — true/assessable abstraction that loses what is distinctive about the hypothesis;
5. `invalid_or_unsupported` — implication not adequately licensed by the hypothesis;
6. `silence_as_null_error` — discrimination is manufactured because one hypothesis is merely silent about the observable.

Do not count a proposition as discriminative merely because it was generated from only one hypothesis. Cross-evaluate it against all candidates.

Where automated matching is used, preserve the raw judgments and enough evidence for manual review. Do not tune the matcher on these eight cases.

## Step 7 — Analyze three separable capabilities
Report results separately for:

### A. Consequence discovery
Did the graph independently recover the kinds of discriminating consequences later used by the resolving science?

Useful outputs:
- per-case reference discriminator coverage;
- number/fraction of generated consequences in each post-hoc category;
- examples of successful non-obvious consequence derivations;
- examples of abstraction/component-support failure.

### B. Historical evidence discovery
For useful discriminating consequences, did the system retrieve genuinely relevant evidence available before cutoff?

Distinguish:
- no relevant pre-cutoff literature exists;
- retrieval failed;
- evidence assessor rejected relevant material;
- retrieved material was only generically compatible;
- proposition/evidence construct mismatch.

### C. Hypothesis comparison
Given only pre-cutoff evidence, what did the system conclude?

Compare its output with the hidden later resolution only after the run.

Allow scientifically valid outcomes such as:
- one hypothesis favored;
- one hypothesis disfavored;
- mixed support;
- different hypotheses favored in different regimes/components;
- evidence insufficient to distinguish.

Do not force mixed benchmark cases into a binary winner metric.

## Step 8 — Primary interpretation
The main question is NOT simply “how many of 8 were ranked correctly?”

The primary analysis should ask:
1. Does the system generate genuinely discriminative consequence profiles more often than it did on ResearchBench?
2. Does it still drift toward generic assessable component facts?
3. Does it manufacture contrast through silence-as-null?
4. When it generates the right discriminator, can the historical literature service find evidence for it?
5. When final assessment differs from the later resolver, is the failure due to consequence generation, retrieval, evidence relevance, aggregation, or genuinely insufficient pre-cutoff evidence?

You may report simple case-level agreement counts descriptively, but do not treat n=8 as a statistically meaningful performance estimate.

## Required outputs
Create repository-native artifacts for:

1. The eight-case verifier-visible dataset.
2. The hidden annotation/evaluation dataset, stored so it cannot be accidentally fed to the verifier.
3. Any minimal adapter/schema code required.
4. Tests for cutoff enforcement and hidden-field isolation.
5. One frozen run per case using the existing consequence-graph system.
6. A machine-readable post-hoc consequence-recovery analysis.
7. A human-readable pilot report.

The report must include:
- exact git commit / configuration used;
- model/provider settings used by each API-backed role;
- paths to all benchmark and run artifacts;
- per-case cutoff;
- per-case generated graph summary;
- per-case consequence-recovery findings;
- per-case evidence-yield/relevance findings;
- per-case final hypothesis assessment;
- comparison with hidden later resolution;
- failure attribution;
- aggregate descriptive summary across the eight cases;
- recommendation on whether the graph architecture now warrants further evaluation on a ~20-case benchmark.

## Do not
- Do not modify/tune the old verifier based on these eight outcomes.
- Do not use post-cutoff resolving papers in verifier context.
- Do not expose hidden consequence matrices before runs are frozen.
- Do not reuse the spent ResearchBench reserve for tuning.
- Do not manufacture binary labels for mixed/regime-dependent cases.
- Do not treat silence as a null prediction.
- Do not create synthetic competing hypotheses.
- Do not rewrite source-grounded hypotheses to make them easier to distinguish.
- Do not interpret stability under assessor perturbations as calibrated probability of scientific truth.

## Acceptance criteria
This task is complete when:
1. all eight cases are integrated in repository-native form;
2. cutoff enforcement and hidden-annotation isolation are tested;
3. all eight are run through the pre-existing graph verifier without benchmark-specific tuning;
4. full forensic artifacts are preserved;
5. post-hoc consequence recovery is evaluated separately from retrieval and final hypothesis comparison;
6. a concise pilot report explains where the method succeeds/fails and whether results justify scaling evaluation to the larger benchmark.

A low final ranking accuracy is not an execution failure. The experiment is intended to diagnose whether task alignment changes the behavior of the existing consequence-based verification architecture.