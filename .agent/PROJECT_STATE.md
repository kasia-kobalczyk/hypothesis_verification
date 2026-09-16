# PROJECT_STATE

## Active phase
Interpret BENCH-GRAPH-PILOT-001 and decide the next method/benchmark-development step.

## Pilot execution
Eight frozen explanatory-hypothesis cases were integrated and run once through the frozen `narrow_graph_v3_complete` / `consequence_graph` method with no benchmark-specific tuning.

Run:
- `runs/pilot_explanatory_001`
- 8/8 cases completed, 0 errors
- 784 verifier LLM calls; Azure deployment `gpt-4.1-kasia`
- estimated cost $2.75
- Semantic Scholar literature provider: 356 calls, 0 errors
- cutoff/hidden-annotation audit scanned 4.79M model-traffic characters and 3,812 retrieved papers; 0 post-cutoff papers and 0 hidden-content hits

## Robust structural result
Compared with ResearchBench reserve-12 using the same frozen method and no post-hoc judge:
- sign-opposed graph nodes: 5% -> 45%
- negative edges: 2% -> 23%
- informative-evidence nodes: 32% -> 41%
- median score margin: 0.120 -> 0.389
- margin > 0.5: 0/12 -> 4/8

Interpretation: genuine competing explanations elicit substantially more contrastive graph structure than ResearchBench did.

## Consequence discovery
Post-hoc auditor reports:
- 11/23 hidden reference discriminators recovered
- recovered in 7/8 cases
- 44/192 generated propositions classed as genuinely discriminative (41 reference matches + 3 novel plausible)
- fly-wing recovered 0/3; generated mostly shared/compatible alignment propositions

## Major method failure exposed
One-sided propositions are common: 127/192 propositions had at least one silent hypothesis.
Across 131 silent (hypothesis, proposition) pairs, frozen edge assessor labelled the silent hypothesis:
- neutral: 57 (44%)
- unlikely/strongly_contradicted: 51 (39%)
- implied/weakly/strongly implied: 23 (18%)

Thus the assessor gives a directional label to a silent hypothesis 56% of the time despite `neutral` already being defined for silence.

Of 87 sign-opposed nodes, the primary auditor classifies 33 as genuine and 51 as manufactured from silence; a blind second LLM rating gives roughly 36 genuine vs 40 manufactured. Exact majority is not robust, but silence-driven contrast is unquestionably a large share.

Manufactured opposition is directionally biased: of 31 manufactured nodes that affected a score, 29 favored the hypothesis that generated the proposition (8.52 log-odds total) and 2 favored the other (1.72). This recreates the historical component-truth failure: literature support for a one-sided consequence is converted into evidence against a silent competitor.

## Historical evidence discovery
For 44 genuine discriminators:
- 36: no relevant pre-cutoff evidence identified by attribution judge
- 7: informative evidence found
- 1: generic compatibility only
- 0 retrieval failures according to the attribution judge

Caveat: the evidence-attribution judge sees only retrieved papers, so true retrieval failures may be misclassified as no historical evidence.

Interpretation: by construction, many decisive discriminators only became observable in the post-cutoff resolving study. The graph generator can recover them, but pre-cutoff literature often cannot settle them.

## Hypothesis-comparison observations
Favored-resolution cases:
- eukaryogenesis: top H2, matches later resolution, but score heavily driven by manufactured contrast (+2.13 vs +0.50 genuine)
- GlnBP: top H2, matches later resolution; strongest case with +1.01 genuine and +0.78 manufactured contribution
- fly-wing: top H2, matches later resolution, but match has no genuine discriminating basis (0 genuine; +0.30 manufactured)
- PFC storage-vs-control: top H1, opposes later resolution; attribution is provisional, with historical evidence and auditor misclassification both relevant

Non-directional benchmark cases must not be evaluated as winner accuracy.

## Auditor limitations
All recovery/evidence attribution judgments are LLM-based; no human domain expert has reviewed them.
The recovery auditor over-calls silence/indeterminate and missed at least one explicit denial in hypothesis text.
Robust conclusions are:
1. structural behavior differs strongly from ResearchBench;
2. silence-driven contrast is a large share of graph opposition;
3. when one-sided support is treated directionally, it systematically favors the generating hypothesis.
Per-case attribution and exact genuine/manufactured counts remain provisional.

## Reproducibility / artifact risk
Executor report records that the run was performed from an uncommitted working tree on top of `c18edc29f93afaa4b9683bfed9473bb3fb659329`; run manifest had no git commit. `runs/` is gitignored and the 42 MB forensic run existed only on the execution disk at completion. Repository currently exposes the pilot report/integration, but artifact backup and exact-run preservation should be verified before further work.

## Current scientific conclusion
The explanatory benchmark is substantially better aligned with the intended task than ResearchBench. The original consequence-generation idea shows real promise: it independently recovered about half of the known discriminating consequences across 7/8 cases.

However, final hypothesis comparison is presently confounded by a specific method failure: the edge assessor often converts hypothesis silence into directional opposition, causing supported one-sided/component consequences to count against silent competitors.

## Recommended next step
Do not scale the frozen verifier unchanged to ~20 cases yet. Continue constructing the ~20-case benchmark, but treat these 8 pilot cases as spent for method tuning.

Before modifying the method:
1. preserve/commit the exact pilot code and back up the full run artifacts;
2. manually/expert-review the score-moving propositions (executor prepared 78 nodes; 40 carry ~80% of influence) to obtain trustworthy labels for genuine discrimination vs silence;
3. use a separate development set to investigate edge-assessor silence handling / aggregation;
4. randomize hypothesis IDs relative to later resolution in the larger benchmark;
5. make consequence discovery a primary benchmark capability, with end-to-end historical hypothesis comparison secondary because decisive pre-cutoff evidence is often absent.