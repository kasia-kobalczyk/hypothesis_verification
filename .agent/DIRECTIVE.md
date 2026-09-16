# DIRECTIVE — BENCH-GRAPH-REVIEW-001

## Objective
Prepare the completed eight-case explanatory-benchmark graph pilot for rigorous human scientific review **without modifying the verifier**.

The immediate goal is to identify, preserve, and package the score-moving graph propositions so the Research Director can manually adjudicate whether each proposition represents:

1. a genuine discriminating consequence;
2. a generic/component fact;
3. an invalid or weak implication;
4. a silence-as-null / manufactured-opposition error;
5. or another clearly documented category.

This task is **forensic preparation only**. Do not tune or change the consequence generator, edge assessor, evidence assessor, priors, mappings, aggregation, retrieval, or prompts.

---

## Context
The completed eight-case pilot showed:
- substantially more contrastive graph structure than the historical ResearchBench reserve;
- meaningful recovery of hidden scientific discriminators;
- but a large apparent failure mode in which propositions generated from one hypothesis were scored directionally against hypotheses that may simply be silent about them.

The current post-hoc LLM auditor is useful diagnostically but is not authoritative enough to serve as scientific ground truth.

We therefore need a compact, reproducible, human-reviewable packet derived from the **already frozen pilot run**.

Treat the eight pilot cases as spent for method tuning. Do not rerun them with changed settings.

---

# PART I — PRESERVE THE EXACT PILOT STATE

## 1. Identify the exact completed run
Locate the completed eight-case pilot run and all associated artifacts.

Expected run family:
- `runs/pilot_explanatory_001`

Verify the exact path rather than assuming it.

Record:
- run ID / directory;
- timestamp(s);
- model/provider configuration for each API-backed role;
- repository HEAD at time of preservation;
- whether the original run was produced from a dirty working tree;
- any local uncommitted files that materially affected the run;
- environment/config files relevant to reproducibility.

## 2. Preserve artifacts before doing anything else
The executor report indicated that the full run may live under gitignored `runs/` and that the original run manifest did not capture a git commit.

Before analysis:
- copy or archive the complete forensic run artifacts into a durable repository-tracked or otherwise explicitly preserved location;
- do not overwrite or regenerate the original artifacts;
- compute checksums for the preserved archive or key files;
- document the mapping from original path to preserved path;
- commit any code/config state needed to reproduce the analysis tooling.

If exact source reconstruction of the original dirty working tree is impossible, state that clearly and preserve everything that remains available.

Do **not** rerun the verifier merely to make the artifacts cleaner.

---

# PART II — EXTRACT THE HUMAN REVIEW SET

## 3. Define score-moving propositions from the frozen run
Using the frozen pilot artifacts, identify all generated proposition nodes that have non-negligible influence on final hypothesis comparison.

Prefer to reuse the influence/contribution calculations already produced by the pilot analysis if they are available.

At minimum produce:

### A. Full score-moving set
All nodes whose evidence/edge contributions changed any hypothesis log-odds / score relative to the no-node baseline or otherwise affected ranking/support under the existing aggregation.

### B. High-influence subset
A compact subset explaining approximately 80% of total absolute score influence across the eight cases.

The previous executor summary suggested roughly:
- ~78 score-moving nodes total;
- ~40 nodes accounting for ~80% of influence.

Do not force those counts if the actual frozen artifacts differ. Recompute transparently from source artifacts and report exact counts.

## 4. Do not pre-filter by the old LLM auditor
The human packet must not contain only nodes already labeled “manufactured” or “genuine” by the automated auditor.

Selection must be based on score influence / structural relevance from the frozen verifier output, not on the post-hoc auditor’s scientific judgment.

The old auditor labels may be included as **non-authoritative metadata** for comparison, but they must not determine which nodes are reviewed.

---

# PART III — BUILD THE REVIEW PACKET

## 5. Create one machine-readable record per review node
For every node in the full score-moving set, create a structured record containing enough context for an independent human scientific judgment.

Required fields:

### Identity
- `review_id`
- `case_id`
- `node_id`
- `origin_hypothesis_id` (if applicable)
- proposition text exactly as generated
- proposition abstraction level/type if recorded by the pipeline

### Case context
- phenomenon / scientific question
- all competing hypothesis texts exactly as shown to the verifier
- historical cutoff

### Graph context
- parent node(s), if any
- edge path from originating hypothesis/root to the proposition
- edge labels/strengths along that path
- cross-hypothesis edge judgments for the proposition against **every** hypothesis
- whether each hypothesis was the origin of the proposition or only cross-evaluated

### Evidence context
For every evidence item that materially affected the node score:
- paper title
- authors/year
- DOI / PMID / Semantic Scholar ID / URL if available
- publication/public date used by the cutoff filter
- retrieved abstract/snippet/span actually shown to the evidence assessor
- evidence judgment and direction
- assessor rationale if stored
- contribution to node / hypothesis score

Do not provide only paper IDs. The reviewer must see the exact textual evidence used by the system.

### Score influence
- node-level contribution to each hypothesis score/log-odds
- absolute influence measure used for ranking review priority
- rank among nodes within the case
- rank globally if useful
- whether removing this node alone would change case ranking/support ordering, if straightforward to calculate without rerunning the LLM

### Existing automated audit metadata
Include, clearly labeled as non-authoritative:
- prior auditor category, if any
- whether the auditor called the opposition genuine/manufactured/silent
- second-auditor judgment if available
- disagreement flag between auditors

### Human-review fields — initially blank
Include fields to be filled manually:
- `human_primary_category`
- `human_prediction_for_each_hypothesis`
- `human_is_genuinely_discriminative`
- `human_silence_as_null_error`
- `human_implication_validity`
- `human_evidence_relevance`
- `human_notes`
- `human_confidence`

Do not auto-populate the human fields.

## 6. Human review categories
Provide this frozen rubric in the packet documentation.

### `genuine_discriminator`
The proposition is scientifically implied/predicted by at least one hypothesis and the competing hypothesis/hypotheses make a meaningfully different positive prediction or are genuinely inconsistent with it.

### `compatible_non_discriminative`
The proposition may be true or supported, but it does not meaningfully distinguish the candidates.

### `generic_component_fact`
The proposition is an abstract/component-level fact that can be supported independently of the distinctive composite explanatory hypothesis and therefore risks recreating the historical component-truth failure.

### `silence_as_null_error`
A hypothesis does not determine the proposition, but the system assigned it a directional null/opposite/contradictory judgment, thereby manufacturing contrast.

### `invalid_or_weak_implication`
The proposition is not adequately licensed by the originating hypothesis or requires an unstated scientific bridge too large to treat as an implication edge.

### `evidence_construct_mismatch`
The evidence span is grounded in the cited source but addresses a different construct/proposition than the node.

### `valid_but_historically_uninformative`
The discriminator is scientifically valid, but pre-cutoff evidence is absent/non-informative, so it should not materially resolve the hypotheses historically.

Allow multiple flags where needed, but require one primary category.

Important distinction:
- `silence` is not equivalent to `no change`, `negative`, `unlikely`, or `contradicted`.
- Do not infer a null prediction unless the hypothesis substantively predicts a baseline/no-effect outcome.

---

# PART IV — CREATE REVIEW VIEWS

## 7. Produce two human-readable review artifacts

### A. Full review table/report
A readable document containing every score-moving node, grouped by case.

Each node should show, compactly but completely:
- proposition;
- origin hypothesis;
- cross-hypothesis edge judgments;
- evidence span(s);
- node score influence;
- prior automated audit metadata;
- blank human-review fields / a stable review ID.

### B. High-influence priority packet
A shorter document containing the subset responsible for ~80% of total absolute score influence.

Order by descending absolute score influence.

The Research Director should be able to adjudicate the most consequential failure modes without opening raw JSON traces.

Preferred formats:
- Markdown for easy repository review;
- JSONL/JSON for machine-readable annotations.

Use repository-native locations such as `reports/`, `benchmark/`, or an existing analysis directory after inspecting conventions. Do not invent a parallel top-level structure unnecessarily.

---

# PART V — ADD NON-LLM ANALYSIS UTILITIES ONLY

## 8. Implement deterministic analysis tooling
It is acceptable and encouraged to add deterministic scripts that:
- compute node score influence;
- extract graph/evidence context;
- generate review JSONL/Markdown;
- summarize edge-label behavior on silent hypotheses;
- calculate counterfactual score/ranking after mechanically removing selected nodes.

These scripts must operate on the frozen run artifacts and must **not call an LLM** unless explicitly necessary to reproduce already-existing audit metadata.

Do not add a new scientific classifier or automatic replacement for human judgment in this task.

## 9. Add sanity checks
Add tests/assertions where practical that verify:
- every review node maps back to a real frozen-run graph node;
- score contributions in the review packet reproduce the frozen aggregate within tolerance;
- evidence spans in the packet are exactly those used by the original assessor;
- no post-cutoff resolver or hidden benchmark annotation has been introduced into the human packet as if it were verifier evidence;
- the packet distinguishes verifier output from post-hoc hidden benchmark context.

---

# PART VI — DO NOT MODIFY THE VERIFIER

Do not, in this task:
- change edge-assessor prompts;
- change the meaning of `neutral`;
- add hard silence gates;
- change evidence-assessor prompts;
- change edge/evidence ordinal mappings;
- change aggregation;
- change priors;
- change graph generation;
- change abstraction policy;
- change retrieval;
- rerun the eight cases with altered settings;
- use the eight spent cases to select a fix.

If you discover an obvious implementation bug while extracting artifacts, document it in the report but do not repair the scientific method unless required only to read/preserve the old artifacts.

---

# PART VII — REPORT BACK

Create an executor report containing:

## Preservation
- exact original run path;
- preserved/archive path;
- checksums;
- git commit(s) created for preservation/analysis tooling;
- reproducibility limitations, especially any unresolved dirty-working-tree issue.

## Review-set statistics
- total generated nodes;
- total score-moving nodes;
- high-influence subset size covering ~80% of absolute influence;
- counts by case;
- counts by edge-label pattern;
- counts of nodes with one or more hypotheses judged non-neutral despite not originating the proposition, without interpreting that automatically as scientific error.

## Existing auditor comparison
- counts from prior primary and secondary auditors;
- disagreement rate;
- cases where automated audit is especially unstable.

## Paths
Report exact repository paths for:
- full machine-readable review set;
- high-influence review set;
- human-readable full review report;
- priority review packet;
- preservation archive / manifest;
- deterministic extraction scripts/tests.

## No scientific fix recommendation yet
You may summarize observed mechanical patterns, but do **not** choose or implement a verifier fix. The next method decision will be based on human review labels supplied after this task.

---

# Acceptance criteria
This task is complete when:
1. the exact frozen eight-case pilot artifacts are durably preserved;
2. all score-moving propositions are extracted into a reproducible machine-readable review set;
3. a high-influence subset covering roughly 80% of absolute score influence is produced;
4. each review record contains enough hypothesis, graph, evidence, and score context for manual scientific adjudication;
5. blank human-label fields and a fixed review rubric are included;
6. deterministic extraction/influence calculations are reproducible and sanity-checked;
7. no verifier behavior has been changed and no eight-case rerun has been performed.

The purpose of this directive is to create trustworthy human ground truth about the pilot failure mode before any method modification is attempted.