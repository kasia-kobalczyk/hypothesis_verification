# What Else Should Be True? — MVP implementation

Verifying scientific hypotheses from indirect evidence.

**Milestone 1** (`IMPLEMENTATION_SPEC.md`): benchmark layer, temporally safe
literature-search service, caching and experiment logging, two baselines, the
experiment runner, the leakage/invariant test suite.

**Milestone 2** (spec §33): the consequence-graph verifier — generation,
cross-evaluation, temporally constrained evidence assessment and exact Bayesian
propagation. Runs end to end; `--method consequence_graph`. Findings and open
research questions are in `docs/MILESTONE_2.md`.

**Benchmarks.** `benchmark/dev/` (v1) and `benchmark/v2/` are **development sets** —
a question-hidden judge recovers most of their pair labels from candidate text
alone, so their aggregate accuracy is not evidence for any method.
`benchmark/canonical/` is the style-controlled evaluation slice, built by symmetric
canonicalisation under a protocol frozen in advance (`docs/CANONICAL_PROTOCOL.md`).

**Evaluation protocol.** The formulation covers arbitrary `k >= 2`; the protocol
pins **k=2 pairwise as the headline metric** (ties 0.5) and treats k>2 as a
stratified scalability analysis, never averaged — chance top-1 is 1/k. Controlled,
nested k-sets at k in {2,3,4} live in `benchmark/k_slices/`. See
`docs/EVALUATION_PROTOCOL.md`.

Start with `docs/STATUS_2026-09-11.md` for where the project actually stands,
`docs/EVALUATION_PROTOCOL.md` for what counts as a result, and
`docs/DECISIONS.md` for the choices behind both.

---

## Quick start

```bash
pip install -r requirements.txt
cp .env.example .env          # then fill in AZURE_API_KEY / AZURE_API_BASE / S2_API_KEY

python scripts/check_setup.py             # credentials, dataset, frozen cutoffs, Crossref
python scripts/check_setup.py --llm       # also makes one small Azure call
python -m pytest -q                       # 218 tests, no network needed
```

Put real credentials in `.env` (gitignored), never in `.env.example`.

Freeze the literature cutoffs (already done; re-run only to refresh):

```bash
python -m src.benchmark.resolve_dates --config configs/mvp.yaml
```

Freeze the evaluable gold-vs-negative pairs (already done; the primary metric
is computed over these):

```bash
python scripts/build_pair_subset.py --config configs/mvp.yaml
```

Build the controlled listwise slices (offline; no LLM, no literature):

```bash
python scripts/build_k_slices.py --k 2 3 4      # nested sets, sampling frozen at build time
python scripts/flag_review_sources.py --slice benchmark/ranking.jsonl --fetch
```

Run the methods:

```bash
# Baseline 1 — direct LLM judge (no literature; also the memorisation diagnostic)
python -m src.experiments.run \
    --method direct_judge \
    --dataset data/researchbench_dev20.jsonl \
    --config configs/mvp.yaml

# Baseline 2 — direct RAG verifier (same temporally constrained search service)
python -m src.experiments.run \
    --method direct_rag \
    --dataset data/researchbench_dev20.jsonl \
    --config configs/mvp.yaml

# Artifact diagnostics — the floor any method must clear
python -m src.experiments.run --method style_artifact          # no model at all
python -m src.experiments.run --method question_hidden_judge   # question withheld

# Debugging: a subset of instances, cache-only replay, config overrides
python -m src.experiments.run --method direct_rag --instances RBV-01 RBV-19
python -m src.experiments.run --method direct_rag --offline        # cache only
python -m src.experiments.run --method direct_rag --refresh-cache  # force re-fetch
python -m src.experiments.run --method direct_judge --set literature.top_k=5

# Choose the Azure deployment for one run
python -m src.experiments.run --method direct_judge --model gpt-5-mini
```

Credential-free plumbing check (synthetic LLM and synthetic literature — **never**
report these numbers):

```bash
python -m src.experiments.run --method direct_rag --llm mock --set literature.provider=mock
```

Run from the repository root, or from anywhere with
`PYTHONPATH=/path/to/hypothesis_verification` — config, dataset and cache paths
resolve against the repository root regardless of the working directory.

Each run writes `runs/<run_id>/` containing `config.yaml`, `manifest.json`,
`events.jsonl`, `errors.jsonl`, `metrics.json`, `summary.json`, and per instance
`input.json`, `presentation.json`, `prompts.json`, `queries.json`, `retrieval.json`,
`evidence.json`, `model_outputs.json`, `scores.json`, `events.jsonl`, `report.md`.

---

## Layout

```
configs/           mvp.yaml, ordinal_mappings.yaml, pricing.yaml
data/
  researchbench_dev20.jsonl -> benchmark/dev/researchbench_dev20_v1.jsonl (frozen, read-only)
  metadata/        source_dates.jsonl  <- frozen cutoffs + version provenance
  cost/            ledger.jsonl  <- durable record of every priced model call
benchmark/dev/     researchbench_dev20_v1.jsonl, pairs_v1.jsonl (frozen pairs)
  cache/           raw Crossref and provider responses (gitignored)
src/
  benchmark/       loader.py, temporal.py, versions.py, pairs.py,
                   presentation.py, resolve_dates.py
  literature/      base.py, semantic_scholar.py, crossref.py, temporal_filter.py,
                   dedup.py, cache.py, http.py, service.py, mock.py
  llm/             client.py, prompts.py, prompts/*.txt (versioned)
  inference/       parameters.py (centralised ordinal mappings; calibration stub)
  baselines/       direct_judge.py, direct_rag.py, artifact_baselines.py
  experiments/     runner.py, run.py, metrics.py, reports.py, base.py,
                   costs.py, assets/cost_dashboard.html
  graph/, evidence/   MILESTONE 2 — intentionally empty
tests/             218 tests; no network access
```

---

## Temporal safety

`src.literature.service.LiteratureSearchService` is the only path by which literature
may reach a model.

* Its public API is `search_literature(query, instance_id, top_k)`. **No method takes a
  cutoff argument**, so a method or agent cannot widen its own window; a test asserts
  that no such parameter exists.
* The cutoff comes from `CutoffRegistry`, an immutable map built from the frozen
  `data/metadata/source_dates.jsonl`. It has no setter.
* Search, metadata lookup, reference expansion and citation expansion all funnel
  through one `_retrieve`, which applies the same filter.
* `render_for_prompt` re-runs the cutoff comparison, the source-paper checks and the
  undated-record policy immediately before any text becomes prompt content, using the
  same helpers as the filter, so a record whose `temporal_eligible` flag was corrupted
  downstream still cannot leak. A violation raises `TemporalLeakError`, which neither
  the runner nor any method catches.
* Post-cutoff records are kept in `RetrievalRecord.excluded` for diagnosis and are
  never returned to callers.
* The cutoff date is **not** written into any prompt (a test enforces this): the
  backend enforces the window, and disclosing the date would tell the model when the
  source paper appeared.

### Date policy

| decision | default | where |
| --- | --- | --- |
| cutoff | earliest public availability of the source − 1 day | `temporal.cutoff_offset_days` |
| boundary | eligible iff `eligible_date <= cutoff_date` | `temporal.boundary` |
| partial candidate dates | resolve to the **last** day of the period ("2020" → 2020-12-31) | `temporal.year_only_day`, `month_only_day` |
| partial source dates | resolve to the **first** day of the period | `src/benchmark/temporal.py` |
| disagreeing date sources | take the **latest** estimate | `temporal.conflict_policy` |
| undated records | excluded | `temporal.unknown_date_policy` |
| source paper + linked preprints | never returned as evidence | `temporal.block_source_doi` |
| other versions of the source study | discovered by title+author search and blocked; the earliest sets the cutoff | `temporal.version_search` (thresholds **frozen**) |
| a record whose title matches the source paper **and** shares an author | blocked | `temporal.block_source_by_title` |
| preprint postings of the source | count as public availability | `temporal.include_preprints_in_cutoff_basis` |

Every one of these shrinks the eligible set when in doubt: recall is traded for
temporal safety, deliberately.

Crossref links a preprint to its journal version for only 1 of the 20 source
papers, so the cutoff resolver searches Crossref by title and author for other
versions of the same study. It found the unlinked bioRxiv preprint of RBV-19,
moving that cutoff nine months earlier. Author overlap alone never blocks
anything: an earlier unrelated paper by the same group is prior literature, not
a version of the study.

The version-search thresholds (title ≥ 0.75, author overlap ≥ 0.50 of the smaller
list) are **frozen for the MVP** and guarded by `tests/test_frozen_thresholds.py`.
They were chosen on these 20 cases, so before a final benchmark validate them on
an independently sampled labelled set:

```bash
python scripts/validate_version_thresholds.py --template          # starter file
python scripts/validate_version_thresholds.py --labelled <file>   # report only
```

That script reports precision, recall and the score distributions at the frozen
values; it does not search for better ones.

Ten of the twenty cutoffs are flagged `ambiguous` (Crossref's deposit timestamp
long precedes the stated publication date, or the date is month-granular). They
still run by default — the flag is a warning that an article-in-press may have
been public earlier — but `summary.json["cutoffs"]` reports how many scored
instances had an unverified cutoff, and `dataset.require_unambiguous_cutoff:
true` refuses them.

### Failure semantics

`API failure != no_evidence` (spec §29). A provider error, rate limit, or offline
cache miss raises; `direct_rag` records it and marks the instance `error` with its
partial artifacts kept, rather than scoring it from a partial vector. `no_evidence`
is produced only when a search genuinely succeeded and returned nothing eligible,
and it maps to a log-likelihood ratio of exactly 0.

---

## Caching and reproducibility

The cached artifact is the **raw provider payload**; normalisation, filtering and
deduplication re-run on every read. A fixed cache plus fixed code always yields the
same eligible set, and a fix to the filter takes effect on cached data without new
API calls. The cache key covers provider, provider version + configuration, query,
instance id, cutoff date, top_k and retrieval path. A normalised snapshot is written
alongside each entry for inspection.

`--offline` serves only from cache and raises `CacheMissError` on a miss.

---

## Configuration

`configs/mvp.yaml` holds everything experimental; `configs/ordinal_mappings.yaml`
holds the ordinal→numeric tables (placeholders, uncalibrated). Two values are
deliberately `null` with `TODO(research)` markers because the spec leaves them open:
`graph.merge_threshold` and `inference.multi_parent_rule`. Unknown YAML keys are
rejected rather than silently ignored.

Ordinal mappings are validated on load: `no_evidence` must be ~0, and both scales
must be monotone. A test also asserts no mapping value is hard-coded elsewhere.

---

## Cost tracking

```bash
python scripts/cost_dashboard.py --serve --open   # auto-refreshing site at :8787
python scripts/cost_dashboard.py                  # one-shot summary in the terminal
python scripts/cost_dashboard.py --export cost.html          # shareable snapshot
python scripts/cost_dashboard.py --estimate direct_rag --units 440   # before a big run
```

The site polls every 10 s and rescans the event logs on each poll, so a run in
progress shows up within seconds. It shows the project total as a hero figure,
today's spend and token counts as stat tiles, a column chart of spend per day,
and breakdowns by method, model and run.

Costs are merged into a **durable ledger** at `data/cost/ledger.jsonl`. Deleting a
run directory does not erase what it cost — the ledger is the record, not
`runs/`. Scanning is incremental (event logs are append-only), and instance-level
logs are deliberately excluded because the runner tees every call into both.

Two honesty rules, matching the rest of the project:

* **Rates are unverified until you say otherwise.** `configs/pricing.yaml` carries
  public list prices with `verified: false`, and every figure is labelled an
  estimate until someone checks them against the Azure agreement.
* **A model with no price is `unpriced`, never $0.00.** Its tokens and calls are
  counted and flagged, and the project total is reported as a floor. A tracker
  that silently prices unknown models at zero reads as authority while being
  wrong.

Set `cost.budget_usd` to get a spend guard: the runner logs spend to date before
every run, warns past 80% of the cap, and with `cost.on_exceed: refuse` raises
`BudgetExceededError` before a single model call is made. Each run also records
its own cost in `summary.json` under `cost`.

Known gap: Azure bills cached prompt tokens at a discount, and
`LLMResponse.usage` does not capture `prompt_tokens_details`, so runs that
benefit from prompt caching are currently over-estimated (`TODO(cost)` in
`configs/pricing.yaml`).

---

## The assessor gate

The current assessor's `no_evidence` means *"no retrieved paper directly investigates
this"*, not *"the literature does not bear on this"* — measured over 588 assessments,
99% of `no_evidence` rationales invoke directness and 82% concede related work was
found before declining it. A consequence graph is built on the second notion, so this
is a construct mismatch, and it gates everything downstream.

Nothing is calibrated and no large sweep is run until it is resolved.
`docs/ASSESSOR_RUBRIC.md` has the construct and the protocol.

```bash
# 1. build the case set (offline; stable once adjudication starts)
python3 scripts/build_assessor_labelset.py --n-per-stratum 4

# 2. blind, two-judge worksheets; v1's label and rationale are stripped
python3 scripts/build_adjudication_packet.py --judges A B

# 3. inter-judge agreement; the headline is `boundary_agreement`
python3 scripts/adjudication_agreement.py --judges A B

# 4. score a prompt against the adjudicated labels; --gate is pre-registered
#    and refuses while the thresholds in acceptance_gate.json are null
python3 scripts/assessor_agreement.py --prompt evidence_assess_v1 --gate
```

## Analysis scripts

All of these read saved artifacts only — no API calls, no cost — so they can be
re-run on any historical run directory.

```bash
# graph-run diagnostics: assessment yield, atomicity, merges, cross-hypothesis
# similarity, posterior concentration; grouped by generation prompt and by k
python scripts/graph_run_diagnostics.py 'runs/consequence_graph_*/' \
    --json-out runs/graph_diagnostics_pooled.json

# k sweep: ranking stratified by k with its own chance baseline, plus method
# scaling (graph size, yield, retrieval, cost). Reports a balanced panel when
# rows are present at every k.
python scripts/k_sweep_report.py 'runs/consequence_graph_*_2e09d5ed' 'runs/..._802860c3'

# style/length artifact diagnostics; the judge is counterbalanced by default
python scripts/v2_artifact_diagnostics.py --pairs <slice.jsonl> --label <name> \
    --out <out.json>            # add --single-order only to reproduce old runs
```

## Evaluation

The **primary** metric is `pair_accuracy` over the frozen subset in
`benchmark/dev/pairs_v1.jsonl`. Every gold-negative pair there was screened with
the slice's own R2 criterion — the negative addresses the same scientific target
and disagrees with a substantive part of the gold — so a win there is a win over
a genuine scientific disagreement. Ties score 0.5 and are reported, not broken.

Listwise metrics (top-1, MRR, mean gold rank) over all eleven candidates are
**secondary**: that set mixes screened disagreements with unscreened candidates
that may simply answer a different question.

An instance whose every negative fails the screen is marked `no_evaluable_pair`
and excluded from the primary metric — named in the run log, in
`summary.json["metrics"]["instances_no_evaluable_pair"]` and on its own report
page, never silently averaged away. **RBV-14** is such a case: the pair audit
established that its row-level R2 pass was incorrect. It stays in the dataset and
in the listwise diagnostics, and no negative was manufactured for it
(`benchmark/dev/screening_corrections_v1.json`).

Two baselines bound what a result is worth:

| method | what it measures |
| --- | --- |
| `style_artifact` | ranking from surface features alone — no model, no question |
| `question_hidden_judge` | what the candidate texts reveal without the question |
| `direct_judge` | closed-book: the model's parametric memory of the outcome |

A literature-based method that does not clear all three is not demonstrating
literature-grounded verification.

**Measured on the development slice (121 frozen pairs across 19 instances;
RBV-14 has no evaluable pair and is excluded — see below):**

| method | pair accuracy |
| --- | --- |
| `style_artifact`, shortest first | **1.000** |
| `question_hidden_judge` | 0.306 |
| `direct_judge` (closed book, gpt-4.1) | 0.264 |
| `style_artifact`, longest first | 0.000 |

The gold hypothesis is the shorter candidate in every frozen pair, so length
alone ranks perfectly, while the language model scores below chance because it
prefers the longer, more elaborate negatives. Report no result from this slice
without this table beside it. See `docs/MILESTONE_1.md` §5.

---

## Benchmark handling

Hypothesis and question text are copied **verbatim**; the frozen slice is never
rewritten. The pair subset adds a screening layer on top of it without touching
the text. Each instance is 1 gold + 10 raw ResearchBench negatives
(`dataset.negatives.pools: [model]`; `fake` negatives are available but off by
default). Candidates are presented in a deterministic per-instance permutation under
anonymised labels ("Hypothesis A"...), so the internal ids — where `H0` is always
gold — never reach the model. The permutation depends only on `(run.seed,
instance.id)`, and the label map is saved with every run.

---

## Environment variables

| variable | purpose |
| --- | --- |
| `AZURE_API_KEY`, `AZURE_API_BASE`, `AZURE_API_VERSION` | Azure OpenAI (also accepts `AZURE_OPENAI_*`) |
| `LLM_MODEL` | Azure deployment name, default `gpt-4.1-kasia` (also `LLM_DEPLOYMENT`, `AZURE_OPENAI_DEPLOYMENT`) |
| `S2_API_KEY` | Semantic Scholar. Without it the shared pool returns HTTP 429 for essentially every request from a server IP |
| `CROSSREF_MAILTO` | Crossref polite pool |

`.env` at the repository root is loaded automatically.

### Choosing the model

Resolution order, highest first:

1. `--model <name>` on the command line;
2. `llm.deployment` in the config (`null` by default, so it defers);
3. `$LLM_MODEL` / `$LLM_DEPLOYMENT` / `$AZURE_OPENAI_DEPLOYMENT`;
4. the built-in default, `gpt-4.1-kasia`.

A LiteLLM-style `azure/<name>` is accepted anywhere and the prefix is stripped, so
one `.env` can serve this project and a LiteLLM-based one. Every run records the
resolved deployment *and* where it came from in `manifest.json` under
`llm.deployment_source`.

Two Azure behaviours are handled explicitly: a deployment that rejects a
parameter (`temperature`, `seed`, ...) has it dropped and logged, and because
Azure returns HTTP 400 for `response_format: json_object` unless the messages
mention "json", the client refuses such a request *before* spending a call and
names the offending prompt. A test asserts every shipped template mentions json.
