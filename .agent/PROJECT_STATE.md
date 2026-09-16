# PROJECT_STATE

## Active phase
Interpret BENCH-GRAPH-ATTRIBUTION-001 and decide the next human-review / method-development step.

## Frozen pilot context
Eight explanatory-hypothesis cases were run once through the frozen consequence-graph verifier. The benchmark was substantially better aligned than ResearchBench, producing much more contrastive graph structure and recovering known discriminating consequences in many cases. The eight pilot cases are now spent for method tuning.

## D045-based score attribution supersedes earlier LLM-auditor attribution
Research Director first-pass adjudication of the 40 highest-influence nodes classified:
- 4 genuine discriminators
- 8 silence-as-null errors
- 14 generic component facts
- 8 compatible non-discriminative propositions
- 3 evidence-construct mismatches
- 3 invalid/weak implications

Claude then mechanically encoded these labels and reconstructed the frozen scores exactly, with no LLM calls and no verifier rerun.

## Influence accounting across all eight cases
Total absolute score influence: 18.07.
Reviewed priority nodes: 14.48 (80.1%).
Unreviewed score-moving nodes: 3.59 (19.9%).

Share of total influence by D045 category:
- generic component facts: 25.8%
- silence errors: 20.2%
- compatible non-discriminative: 15.2%
- weak implication: 6.8%
- genuine discriminators: 8.1%
- construct mismatch: 4.0%
- unreviewed: 19.9%

Key conclusion: the method failure is broader than silence handling. Non-discriminative component and compatible facts together carry 41.0% of influence, about twice the influence of confirmed silence errors.

## Directional cases under D045 attribution
Orientation below is H2 over H1; positive favors H2. In all four favored-resolution benchmark cases, later resolution favors H2.

### Eukaryogenesis
Frozen: +2.42 H2 (agrees with later resolution).
Reviewed genuine contribution: none.
Silence: -0.24.
Generic component facts: +2.02.
Weak implication: +0.85.
Unreviewed: -0.20.
Removing confirmed errors only -> +1.82 H2, still agrees, but agreement is carried mainly by generic component facts.
Strict genuine-only reviewed view -> tie; genuine + unreviewed -> -0.20 H1.
Interpretation: apparent success is not supported by reviewed genuine discrimination.

### Fly-wing
Frozen: +0.31 H2 (agrees).
Reviewed genuine: none.
Silence: +0.30.
Unreviewed: +0.01.
Removing confirmed errors -> +0.01 H2; strict reviewed-only -> tie.
Interpretation: apparent success essentially disappears after removing reviewed silence error.

### GlnBP
Frozen: +1.84 H2 (agrees with induced-fit resolution).
Reviewed genuine discriminators: -0.38, i.e. point toward H1 overall in the frozen scoring.
Silence errors: +1.63.
Generic component facts: +0.92.
Compatible non-discriminative: -0.19.
Unreviewed: -0.13.
Removing confirmed errors only -> +0.21 H2, still agrees because generic component facts carry the remaining direction.
Strict genuine-only -> -0.38 H1; genuine + unreviewed -> -0.52 H1.
Interpretation: the frozen agreement is not a clean success; the reviewed genuine discriminators do not support the later-favored H2 under the current scoring.

### PFC storage vs control
Frozen: -1.21 H1 (opposes later control/H2 resolution).
Reviewed genuine discriminators: +0.58 H2.
Silence error: -0.89.
Evidence-construct mismatch: -0.72.
Compatible non-discriminative: -0.24.
Unreviewed: +0.05.
Removing confirmed errors -> +0.39 H2; strict genuine-only -> +0.58 H2.
Interpretation: the sole directional failure reverses after removing confirmed errors; genuine reviewed discrimination actually points toward the later-supported control account.

## Non-directional cases
Forest, Gcn4, PFC interhemispheric and spider have mixed/regime/component-wise benchmark resolutions and must not be reduced to winner accuracy. Their score leanings are reported only diagnostically.

## Mechanical pattern across categories
The non-originating hypothesis was assigned `unlikely`/`strongly_contradicted` in:
- 8/8 silence errors
- 13/14 generic component facts
- 3/3 construct mismatches
- 3/3 weak implications
- 4/4 genuine discriminators

All 14 generic component facts were literature-supported. This shows the core problem is not simply bad retrieval: true literature-backed propositions become hypothesis-specific evidence because cross-hypothesis edge judgments create artificial opposition.

## Path-mediation limitation
58/78 score-moving nodes depend on parent routes; 25 of those dependencies pass through reviewed nodes. Evidence-zeroing is the primary additive attribution. Graph-deletion sensitivity can remove inherited routes but may also remove legitimate portions. Neither uniquely isolates edge error without relabeling model judgments.

## Review coverage gaps
Reviewed share is below 80.1% for:
- spider: 45.4%
- forest: 67.5%
- PFC interhemispheric: 67.7%
- Gcn4: 70.5%
- eukaryogenesis: 79.5%

Recommended next human-review batch from executor:
- spider X7, X24, X8, X22, X17
- PFC interhemispheric X1, X23
- fly-wing X19
Then review remaining 30 nodes by influence if needed.

## Current scientific interpretation
1. Benchmark semantics were a major issue: genuine explanatory hypotheses do elicit substantially more contrastive consequence graphs than ResearchBench.
2. Consequence generation remains promising as a capability in its own right.
3. End-to-end hypothesis comparison is currently invalidated by a broader discrimination/relevance problem, not only silence-as-null.
4. Only 8.1% of total score influence in the adjudicated accounting comes from reviewed genuine discriminators; generic component facts and compatible non-discriminative propositions dominate.
5. The PFC storage/control case provides the clearest evidence that removing confirmed reasoning errors can reveal a correct underlying discriminative signal.
6. GlnBP shows that even a scientifically good benchmark case can be scored in the correct direction for the wrong reasons.

## Next step
Do not modify the verifier yet using these eight spent cases.
First, finish human review of the low-coverage cases, recording per-hypothesis prediction states for each reviewed node rather than only a primary category. This will clarify which hypothesis is silent and whether a node is genuinely one-sided versus contradictory.
After that, design and test any fix on a separate development set. Method-development priorities should include both:
- explicit silence/indeterminate handling in cross-hypothesis edge assessment;
- preventing generic/compatible component facts from counting as discriminative evidence merely because the competing hypothesis receives an `unlikely` edge.

Continue building the larger ~20-case benchmark in parallel, but keep the eight pilot cases out of tuning.