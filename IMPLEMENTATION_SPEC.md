# MVP Implementation Specification

## Project

**Working title:** What Else Should Be True? Verifying Scientific Hypotheses from Indirect Evidence

This document specifies the first implementation milestone for the consequence-based scientific hypothesis verification system described in the accompanying paper draft.

The implementation should follow the paper's current scientific framing. It should not introduce new methodological assumptions simply to make the code easier to write. Where a design choice is not yet scientifically settled, expose it through configuration or leave a clear TODO.

---

## 1. Scope of the MVP

The MVP should establish an end-to-end experimental pipeline for ranking competing scientific hypotheses using only literature available before a fixed temporal cutoff.

The first milestone is not intended to maximize benchmark performance. It should provide:

1. a reliable benchmark/data layer;
2. a temporally safe literature-search interface;
3. reproducible caching and experiment logging;
4. direct-judge and direct-RAG baselines;
5. a first consequence-graph verifier;
6. interpretable intermediate artifacts for debugging;
7. simple ranking metrics.

The implementation must make temporal leakage difficult or impossible by construction.

---

## 2. Benchmark input

Use the frozen 20-case ResearchBench development slice already prepared for this project.

Each benchmark item should contain at least:

```json
{
  "id": "RBV-01",
  "researchbench_sample_id": "...",
  "question": "...",
  "hypotheses": [
    {
      "id": "H0",
      "text": "...",
      "gold": true
    },
    {
      "id": "H1",
      "text": "...",
      "gold": false
    }
  ],
  "source_doi": "...",
  "cutoff_date": "YYYY-MM-DD"
}
```

Requirements:

- Preserve ResearchBench hypothesis text verbatim.
- Do not rewrite, simplify, or canonicalize hypotheses during experiments.
- Preserve original ResearchBench identifiers and source DOI.
- The system should support more than two candidate hypotheses.
- Pairwise evaluation may be derived from listwise scores.

The current 20-case slice was selected before any literature audit or consequence-graph inspection. Do not alter this slice based on observed method performance.

---

## 3. Temporal metadata resolution

Before running literature-based methods, resolve publication metadata for the source paper associated with each benchmark item.

Implement a script that accepts source DOIs and records all available date fields.

Suggested record:

```json
{
  "doi": "...",
  "online_date": "YYYY-MM-DD",
  "print_date": "YYYY-MM-DD",
  "posted_date": "YYYY-MM-DD",
  "other_dates": {},
  "selected_public_date": "YYYY-MM-DD",
  "selected_cutoff_basis": "online_date",
  "cutoff_date": "YYYY-MM-DD",
  "ambiguous": false,
  "notes": null
}
```

Policy for the MVP:

- Define `cutoff_date` as the day immediately before the earliest eligible public availability of the source paper.
- Keep the inclusion of preprints configurable.
- If metadata are ambiguous, do not guess silently. Flag the item for manual inspection.
- Store the raw provider response when possible.

Suggested metadata source:

- Crossref as the primary DOI/date metadata source.
- Additional sources may be added if needed, but provenance should always be logged.

---

## 4. Literature-search service

Build a thin literature-search layer that the agent can query, while the benchmark harness enforces temporal constraints.

The agent should **not** be able to set or override the cutoff date.

Preferred interface:

```python
search_literature(
    query: str,
    instance_id: str,
    top_k: int = 10,
) -> list[Paper]
```

The service should:

1. look up the benchmark instance;
2. obtain its frozen cutoff date;
3. issue the external search query;
4. normalize returned metadata;
5. remove post-cutoff results;
6. deduplicate versions of the same work;
7. return only eligible results.

Preferred search provider for the MVP:

- Semantic Scholar for literature retrieval and relevance ranking.
- Crossref for DOI and publication-date verification.

The internal flow should resemble:

```text
query
  -> Semantic Scholar search
  -> DOI/title/author normalization
  -> metadata verification
  -> temporal filtering
  -> version deduplication
  -> eligible results
```

---

## 5. Paper schema

Use a stable structured representation for all literature results.

Suggested schema:

```json
{
  "paper_id": "...",
  "provider": "semantic_scholar",
  "provider_id": "...",
  "doi": "...",
  "title": "...",
  "abstract": "...",
  "authors": [],
  "year": 2020,
  "publication_date": "YYYY-MM-DD",
  "eligible_date": "YYYY-MM-DD",
  "venue": "...",
  "url": "...",
  "is_preprint": false,
  "open_access_pdf": "...",
  "retrieval_query": "...",
  "retrieval_rank": 1,
  "cutoff_date": "YYYY-MM-DD",
  "temporal_eligible": true
}
```

Store enough provenance to reproduce why a paper was returned.

---

## 6. Preprints and version deduplication

Preprints should be configurable.

Recommended default for scientific validity:

- include publicly available preprints if they were available before the cutoff;
- treat a preprint and later journal publication as versions of the same scientific work where possible.

Do not count the preprint and journal article as independent pieces of evidence if they represent the same work.

Version linking may use:

- DOI relations;
- title similarity;
- overlapping author lists;
- explicit preprint/version metadata.

For the MVP, prefer conservative deduplication. If uncertain, retain the records but mark them as potentially related.

---

## 7. Temporal leakage protection

Temporal safety is a core benchmark requirement.

Every literature access path must apply the same cutoff policy:

- search results;
- citation expansion;
- reference expansion;
- paper metadata lookup;
- full-text lookup;
- open-access PDF resolution.

Add unit tests where the provider returns papers both before and after the cutoff and verify that only eligible results are exposed to the agent.

Post-cutoff results may be stored internally for debugging, but they must never enter model context.

---

## 8. Caching and reproducibility

External literature search is time-varying. Cache aggressively from the beginning.

Cache key should include at least:

```text
provider
query
instance_id
cutoff_date
top_k
provider configuration/version
```

Store:

- raw provider response;
- normalized results;
- filtered results;
- timestamp of retrieval.

A repeated run should be able to operate entirely from cache.

Provide a `--refresh-cache` or equivalent option for intentional refreshes.

---

## 9. Experiment logging

Every run should create a self-contained artifact directory.

Suggested structure:

```text
runs/
  <run_id>/
    config.yaml
    summary.json
    instances/
      RBV-01/
        input.json
        graph.json
        edge_judgments.json
        queries.json
        retrieval.json
        evidence.json
        scores.json
        report.md
```

Log at minimum:

- benchmark instance;
- model/provider configuration;
- prompts or prompt version IDs;
- all queries issued;
- raw search results;
- eligible search results;
- generated proposition graph;
- edge judgments;
- evidence judgments;
- final scores and ranking;
- token usage;
- API usage;
- errors/retries.

---

## 10. Baseline 1: Direct LLM judge

Implement the simplest baseline first.

Input:

```text
scientific question Q
candidate hypotheses H_1 ... H_k
```

Output:

```text
scalar score or ranking over hypotheses
```

No literature retrieval.

Requirements:

- use the same language-model backend as the proposed method where possible;
- support listwise ranking;
- optionally expose pairwise ranking;
- save raw model output and parsed scores;
- make prompt templates versioned.

---

## 11. Baseline 2: Direct RAG verifier

Implement a literature-grounded baseline that searches directly for evidence about each candidate hypothesis.

Pipeline:

```text
for each H_i:
    generate outcome-neutral search queries about H_i
    retrieve eligible pre-cutoff literature
    assess evidence for H_i
rank hypotheses
```

The retrieval service must be identical to the one used by the proposed method.

This baseline is important because the central scientific claim is not merely that retrieval helps, but that searching through consequences can recover evidence when direct hypothesis retrieval is weak.

---

## 12. Consequence graph representation

Represent the scientific consequence structure explicitly.

Use one categorical root variable conceptually:

```text
H in {1, ..., k}
```

where each value corresponds to a candidate hypothesis.

Every non-hypothesis proposition node is represented as:

```text
X_v
```

There is no separate `C` variable or node type.

Suggested node schema:

```json
{
  "id": "X7",
  "text": "...",
  "empirically_assessable": true,
  "generation_parent": "X3",
  "generation_origin_hypothesis": "H1",
  "metadata": {}
}
```

Suggested edge schema:

```json
{
  "source": "X3",
  "target": "X7",
  "ordinal_strength": null
}
```

Hypothesis roots may also be edge sources.

---

## 13. Consequence graph generation

Interface:

```python
build_graph(
    question,
    hypotheses,
    config,
) -> ConsequenceGraph
```

The graph builder should:

1. generate scientific propositions that should become more or less likely if a hypothesis or parent proposition holds;
2. recursively expand selected propositions;
3. pool propositions from all hypotheses into one shared graph;
4. merge semantically equivalent propositions;
5. cross-evaluate generated propositions against all hypotheses;
6. freeze the graph before any literature outcome is observed.

Important scientific constraints:

- direct evidence is allowed;
- do not enforce an "indirect only" rule;
- observable/searchable propositions may occur at any depth;
- graph depth itself is not evidence strength;
- do not preferentially retain propositions after seeing favorable literature outcomes;
- shared propositions across hypotheses are allowed and important.

---

## 14. Graph-generation configuration

Keep v0 simple and configurable.

Suggested initial configuration:

```yaml
graph:
  max_depth: 2
  max_nodes: 20
  max_children_per_node: 3
  semantic_merge: true
  merge_threshold: TODO
```

Do not implement expected-information-gain search or adaptive graph expansion in the MVP.

Do not search repeatedly until favorable evidence is found.

---

## 15. Inferential edge judgments

Each graph edge represents an uncertain scientific implication.

For edge:

```text
u -> v
```

ask the LLM how strongly the truth of `u` implies the truth of `v`.

Use placeholder ordinal labels:

```text
strongly_implied
implied
weakly_implied
neutral
unlikely
strongly_contradicted
```

The exact labels may change later.

Store both:

- the ordinal category;
- a short textual rationale.

The edge assessor must not see retrieved literature evidence for the target proposition.

---

## 16. Ordinal-to-probability mapping

Keep numerical mappings outside prompts and outside core logic.

Example placeholder config:

```yaml
edge_probabilities:
  strongly_implied: 0.95
  implied: 0.80
  weakly_implied: 0.65
  neutral: 0.50
  unlikely: 0.30
  strongly_contradicted: 0.10
```

These are placeholders only.

The mapping must be replaceable later by validation-set calibration.

Do not hard-code values throughout the codebase.

---

## 17. Outcome-neutral proposition retrieval

For each empirically assessable proposition `X_v`, generate literature queries that search for the underlying entities, interventions, comparisons, and measurements without encoding the desired outcome.

Example proposition:

```text
M-mutant cells exhibit increased phospho-RPA.
```

Acceptable queries:

```text
M mutation phospho-RPA cells
M mutant RPA phosphorylation
```

Avoid:

```text
evidence that M increases phospho-RPA
proof that M causes replication stress
```

Freeze generated queries before inspecting retrieval outcomes.

Store query text and provenance for every proposition.

---

## 18. Evidence representation

For an empirically assessable proposition `X_v`, let:

```text
D_v = literature evidence retrieved for X_v
```

`D_v` may contain zero, one, or multiple studies.

The evidence assessor should jointly evaluate the retrieved set rather than simply count papers.

---

## 19. Evidence assessment

Input:

```text
proposition X_v
eligible retrieved literature D_v
```

Output one placeholder ordinal category:

```text
strong_support
support
weak_support
mixed
weak_contradiction
contradiction
strong_contradiction
no_evidence
```

Keep `mixed` and `no_evidence` semantically distinct.

The assessor should consider:

- relevance to the proposition;
- directness of the measurement;
- methodological quality where inferable;
- consistency across studies;
- whether multiple papers are independent or repeated reports of the same result;
- contradictory findings.

Also return a structured explanation identifying which papers drove the judgment.

---

## 20. Evidence-strength mapping

Map the evidence category to a log-likelihood contribution.

Conceptually:

```text
lambda(s_v) =
    log P(D_v | X_v = 1)
      / P(D_v | X_v = 0)
```

Use configurable placeholder values for the MVP.

Important:

```text
lambda(no_evidence) ~= 0
```

Failure to retrieve evidence must not automatically count against a hypothesis.

---

## 21. Evidence dependence

The method should not blindly treat correlated observations or repeated papers as independent confirmations.

For the MVP:

- record explicit shared graph parents;
- deduplicate versions of the same study;
- allow downstream observations sharing a latent proposition to update through that shared node.

Do not implement a complex learned correlation model.

If exact dependence handling becomes difficult, keep the approximation explicit and documented.

---

## 22. Bayesian aggregation

The intended conceptual model is:

```text
P(H, X, D | G)
  = P(H)
    * product_v P(X_v | parents(v), H)
    * product_v P(D_v | X_v)
```

The final score for hypothesis `H_i` is:

```text
P(H = i | D, G)
```

after marginalizing unobserved proposition variables.

For the MVP:

- use a uniform prior unless configured otherwise;
- implement exact inference if straightforward for the chosen DAG restrictions;
- otherwise implement a clearly documented approximation;
- do not introduce arbitrary depth penalties;
- inferential attenuation should arise from edge probabilities.

If multiple parents make exact semantics ambiguous, expose the composition rule in configuration and document it.

---

## 23. Do not implement calibration yet

The paper proposes later validation-set calibration of the small global ordinal mappings.

Do **not** train or calibrate the verifier in the first MVP.

The code should nevertheless make later calibration possible through interfaces such as:

```python
fit_calibration(validation_runs)
```

All ordinal mappings should therefore be centralized.

---

## 24. Experiment runner

Provide a common experiment interface.

Example:

```bash
python -m experiments.run \
    --method direct_judge \
    --dataset data/researchbench_dev20.jsonl \
    --config configs/mvp.yaml
```

```bash
python -m experiments.run \
    --method direct_rag \
    --dataset data/researchbench_dev20.jsonl \
    --config configs/mvp.yaml
```

```bash
python -m experiments.run \
    --method consequence_graph \
    --dataset data/researchbench_dev20.jsonl \
    --config configs/mvp.yaml
```

Support selecting a subset of instance IDs for debugging.

---

## 25. Metrics

At minimum report:

- top-1 accuracy;
- gold hypothesis rank;
- mean reciprocal rank;
- pairwise gold-vs-negative accuracy;
- per-instance score vector;
- number of generated graph nodes;
- number of searchable nodes;
- number of nodes with informative evidence;
- number of search queries;
- number of retrieved eligible papers.

Do not interpret the 20-case development result as final benchmark performance.

---

## 26. Diagnostic reports

Decomposability is a central property of the method.

For every instance, generate a human-readable report containing:

```text
Question
Hypotheses

Generated consequence graph

For every edge:
    ordinal implication judgment
    rationale

For every searchable proposition:
    generated queries
    retrieved eligible literature
    evidence judgment
    evidence rationale

Per-hypothesis evidence contributions

Final scores
Final ranking
Gold hypothesis
```

A failed case should be inspectable without rerunning the model.

---

## 27. Suggested repository structure

```text
hypothesis-verification/
├── configs/
│   ├── mvp.yaml
│   └── ordinal_mappings.yaml
├── data/
│   ├── researchbench_dev20.jsonl
│   └── metadata/
├── src/
│   ├── benchmark/
│   │   ├── loader.py
│   │   └── temporal.py
│   ├── literature/
│   │   ├── base.py
│   │   ├── semantic_scholar.py
│   │   ├── crossref.py
│   │   ├── temporal_filter.py
│   │   ├── dedup.py
│   │   └── cache.py
│   ├── llm/
│   │   ├── client.py
│   │   └── prompts/
│   ├── graph/
│   │   ├── schema.py
│   │   ├── generate.py
│   │   └── merge.py
│   ├── evidence/
│   │   ├── queries.py
│   │   ├── retrieve.py
│   │   └── assess.py
│   ├── inference/
│   │   ├── parameters.py
│   │   └── bayes.py
│   ├── baselines/
│   │   ├── direct_judge.py
│   │   └── direct_rag.py
│   └── experiments/
│       ├── runner.py
│       ├── metrics.py
│       └── reports.py
├── tests/
│   ├── test_temporal_filter.py
│   ├── test_version_dedup.py
│   ├── test_graph_schema.py
│   └── test_cache.py
└── runs/
```

---

## 28. Configuration philosophy

Anything likely to change scientifically should be configurable.

Examples:

```yaml
literature:
  provider: semantic_scholar
  include_preprints: true
  top_k: 10

graph:
  max_depth: 2
  max_nodes: 20
  max_children_per_node: 3

retrieval:
  queries_per_node: 2

inference:
  prior: uniform
  multi_parent_rule: TODO
```

Avoid scattering experimental constants throughout Python files.

---

## 29. Error handling

External APIs will fail.

The system should handle:

- missing abstracts;
- missing publication dates;
- missing DOI;
- rate limits;
- transient HTTP failures;
- malformed provider records;
- duplicate papers;
- empty search results;
- model parse failures.

Do not silently convert failures into scientific evidence.

For example:

- API failure != `no_evidence`;
- missing abstract != contradiction;
- parse failure should be logged and surfaced.

---

## 30. Testing requirements

At minimum add tests for:

### Temporal filtering
A post-cutoff paper is never exposed.

### Boundary date
A paper exactly on the cutoff is handled according to the documented policy.

### Cache reproducibility
A cached query returns the same normalized eligible result set.

### Version deduplication
Known preprint/journal duplicates are not counted independently when linked.

### Graph schema
No proposition node is represented using a separate `C` type; proposition truth uses `X_v`.

### Missing evidence
Zero retrieved literature produces the `no_evidence` state, not contradiction.

### Baseline isolation
Direct judge must never call the literature service.

---

## 31. Prompt versioning

Prompts are part of the experimental method.

Store each prompt template as a versioned file.

Suggested prompt groups:

```text
prompts/
  direct_judge_v1.txt
  direct_rag_query_v1.txt
  direct_rag_assess_v1.txt
  consequence_generate_v1.txt
  edge_assess_v1.txt
  proposition_query_v1.txt
  evidence_assess_v1.txt
```

Every run should record which prompt version was used.

---

## 32. First implementation milestone

Do not attempt the entire research agenda in one pass.

The first milestone should complete:

1. benchmark loader;
2. temporal metadata resolution;
3. Semantic Scholar literature client;
4. Crossref metadata validation;
5. hard cutoff filtering;
6. caching;
7. direct LLM judge;
8. direct RAG baseline;
9. experiment runner;
10. leakage/unit tests.

Only once these components work should the consequence graph be added.

---

## 33. Second implementation milestone

Add:

1. consequence graph schema;
2. consequence generation;
3. semantic merging;
4. edge-strength judgments;
5. outcome-neutral proposition query generation;
6. proposition-level evidence assessment;
7. fixed ordinal mappings;
8. simple Bayesian aggregation;
9. per-instance diagnostic reports.

---

## 34. Deferred work

Do not implement yet:

- learned verifier parameters;
- validation-set calibration;
- expected information gain;
- adaptive search based on favorable outcomes;
- complex graph pruning;
- sophisticated learned evidence-dependence models;
- large-scale benchmark optimization;
- automatic benchmark rewriting;
- automatic hypothesis canonicalization.

These should be revisited only after the MVP has been inspected manually.

---

## 35. Scientific invariants

The following should be treated as non-negotiable unless the paper design explicitly changes:

1. **Direct evidence is allowed.**
   The method is not an indirect-only verifier.

2. **Graph distance is not evidence strength.**
   Strength comes from the inferential relationships.

3. **Any proposition node may be empirically assessable.**
   There is no special terminal consequence node type.

4. **Use `X_v` for proposition truth and `D_v` for retrieved literature evidence.**
   Do not reintroduce `C`.

5. **Missing evidence is not contradictory evidence.**

6. **Graph construction must be outcome-blind.**
   Do not inspect whether later literature is favorable before deciding which propositions to retain.

7. **Search queries should be outcome-neutral.**

8. **Evidence should be judged jointly at the proposition level.**
   Do not simply count papers.

9. **Shared consequences are expected.**
   The graph is not a collection of independent hypothesis trees.

10. **The output should be decomposable and auditable.**
    A final score without an inspectable trace is insufficient.

---

## 36. Definition of done for the MVP

The MVP is complete when:

- all 20 development cases load correctly;
- each case has a verified cutoff or an explicit metadata warning;
- literature search cannot leak post-cutoff papers;
- direct judge runs end-to-end;
- direct RAG runs end-to-end;
- consequence verifier runs end-to-end;
- every run is reproducible from cached artifacts;
- every hypothesis ranking is accompanied by inspectable intermediate outputs;
- tests cover temporal leakage and the main schema invariants;
- no scientific-method decisions were silently invented in implementation.

At that point, the next research task is manual failure analysis, not further engineering optimization.
