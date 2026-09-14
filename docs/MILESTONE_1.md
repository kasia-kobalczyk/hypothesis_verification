# Milestone 1 — status, assumptions, open scientific questions

Completed against `IMPLEMENTATION_SPEC.md` §32. This document records what was
decided by the implementation and what still needs a research decision. Nothing
here should be treated as settled method.

---

## 1. Implemented

| spec | component | where |
| --- | --- | --- |
| §2 | Benchmark loader for the frozen 20-case slice, verbatim text | `src/benchmark/loader.py` |
| §3 | Crossref temporal metadata resolution + frozen cutoffs | `src/benchmark/temporal.py`, `src/benchmark/resolve_dates.py`, `data/metadata/source_dates.jsonl` |
| §4, §5 | Semantic Scholar client, normalised `Paper` schema | `src/literature/semantic_scholar.py`, `base.py` |
| §4 | Crossref DOI/date verification | `src/literature/crossref.py` |
| §6 | Conservative version deduplication | `src/literature/dedup.py` |
| §7 | Hard cutoff filtering + final pre-prompt gate | `src/literature/temporal_filter.py`, `service.py` |
| §8 | Raw-payload cache, `--refresh-cache`, `--offline` | `src/literature/cache.py` |
| §9 | Self-contained run artifacts | `src/experiments/runner.py` |
| §10 | Direct LLM judge | `src/baselines/direct_judge.py` |
| §11 | Direct RAG verifier | `src/baselines/direct_rag.py` |
| §16, §20, §23 | Centralised ordinal mappings + calibration stub | `configs/ordinal_mappings.yaml`, `src/inference/parameters.py` |
| §24, §25 | Experiment runner, CLI, ranking metrics | `src/experiments/run.py`, `metrics.py` |
| §26 | Per-instance diagnostic reports | `src/experiments/reports.py` |
| §30, §31 | Test suite, versioned prompts | `tests/`, `src/llm/prompts/` |

Not implemented, by instruction: the consequence graph and everything downstream
of it (§12–§22, §33). `src/graph/` and `src/evidence/` contain only docstrings
naming the invariants that milestone 2 must preserve.

---

## 2. Frozen cutoffs (resolved 2026-09-11)

All 20 DOIs resolved against Crossref. Basis distribution:

* `created` (Crossref registration timestamp): 18
* `issued`: 1 (RBV-08, month granularity)
* linked bioRxiv preprint: 1 (RBV-12, cutoff 2022-09-25 rather than 2024-01-09)

10 items carry `ambiguous: true` and are listed in
`data/metadata/source_dates_summary.json` under `needs_manual_inspection`.

---

## 3. Post-review hardening

An independent review pass over this code against the spec produced the
following changes (regression tests in `tests/test_review_fixes.py`):

| finding | fix |
| --- | --- |
| `direct_rag` caught `HypothesisVerificationError`, the base class of `TemporalLeakError` — a detected leak became a failed instance instead of an aborted run | leak and missing-cutoff errors now propagate; only `ProviderError`/`CacheMissError` are recorded |
| `assert_no_leak` blocked `blocked_dois` but not `source_doi`, so the final gate was weaker than the filter | both now call one `blocked_dois()` helper |
| an **unlinked** preprint of the source paper was eligible (Crossref links a preprint for only 1 of 20 items) | added `temporal.block_source_by_title`: records whose title matches the source paper's are blocked at both the filter and the final gate; source titles are now in the frozen metadata |
| `literature_stats.errors` was never incremented | provider failures are counted before being re-raised |
| an ambiguous cutoff gated nothing and was invisible in aggregates | `summary.json["cutoffs"]` reports ambiguous/missing counts and names the instances; `dataset.require_unambiguous_cutoff` can refuse them |
| `queries_per_hypothesis: 0` would have produced `no_evidence` everywhere with no error | retrieval budgets are `ge=1` |
| the harness rewrote an assessor label without recording the original | `model_evidence_label` and `label_enforced_by_harness` are saved; the behaviour is configurable |
| preprints excluded by config were recorded without dates | preprint policy now runs after dating |
| dedup lost version chains on a second pass | collapsed groups carry their members across |
| `resolve_dates --instances` truncated the frozen metadata file | records are merged, never replaced |
| `created` could not be excluded from the cutoff basis without losing it as a cross-check | `crossref.cutoff_basis_fields` |
| a Crossref year-only date was recorded as day precision | the verifier returns a `PartialDate` |
| an Azure retry after dropping an unsupported parameter could escape as a bare exception | wrapped in `LLMError` |
| `direct_judge` under-reported tokens spent on parse repairs | both baselines diff `usage_totals` |
| three tests were weaker than their names (wrong monkeypatch target, assertion on a stub, a regex that could not match the likely violation) | corrected |

Two review findings were **not** acted on, deliberately: the source-blocking
question of whether companion papers by the same authors count as leakage, and
the `verify_boundary_window_days: 180` gap. Both are scientific calls, now
documented in §4 and in `configs/mvp.yaml`.

---

## 4. Implementation decisions (all reversible in configuration)

1. **Cutoff = earliest public availability − 1 day**, inclusive boundary
   (`eligible_date <= cutoff_date`).
2. **Uncertainty always shrinks the eligible set.** Partial candidate dates
   resolve to the last day of the period; partial source dates to the first day;
   disagreeing date sources collapse to the latest estimate; undated records are
   excluded. This trades recall for temporal safety.
3. **The source DOI, its linked preprints, and every discovered alternate
   version are blocked** from retrieval even when they would pass the date test
   (extended by decisions 2 and 8).
4. ~~**Crossref `created` participates in the cutoff basis.**~~ **Superseded by
   decision 1:** `created` is diagnostic only and can no longer set a cutoff. The
   basis is now `issued` for 18/20 instances, and a large `created`-to-basis gap
   flags the instance instead.
5. **Negative pool = the 10 raw `model_negative_hypotheses`.** The 5
   `fake_negative_hypotheses` are loadable (`dataset.negatives.pools`) but off by
   default, matching the R2 screening rubric that selected the slice.
6. **Candidates are presented shuffled under anonymised labels.** `H0` is always
   gold in the frozen file, so load order would be a positional giveaway. The
   permutation depends only on `(run.seed, instance.id)`.
7. **The cutoff date never appears in a prompt.** Enforcement is the backend's
   job, and printing the date would tell the model when the source paper appeared.
8. **A partial score vector is not a ranking.** If any hypothesis fails in
   `direct_rag`, the instance is `error` and unscored; artifacts are kept.
9. **`no_evidence` is only produced by a successful, empty search.** Provider
   errors, rate limits and offline cache misses raise.
10. ~~**Verification against Crossref is `boundary_only`.**~~ **Superseded by
    decision 9:** every retrieved record is Crossref-verified (`always`).

---

## 5. Open questions — RESOLVED

All ten questions below were decided by the research team on 2026-09-11 and
implemented; see **`docs/DECISIONS.md`** for each decision, how it is realised in
code and configuration, and what it changed. The original statements are kept
here for the record.

### Measured consequences of those decisions

Running the artifact diagnostics the decisions asked for produced one result
that dominates everything else on this slice:

| method | pair accuracy (121 pairs, 19 instances) |
| --- | --- |
| `style_artifact`, shortest text first | **1.000** |
| `question_hidden_judge` | 0.306 |
| `direct_judge` (closed book, gpt-4.1) | 0.264 |
| `style_artifact`, longest text first | 0.000 |

The gold hypothesis is the shorter candidate in **every** frozen pair, so a rule
with no model, no question and no literature scores perfectly. The language
model is not merely failing to beat that rule — at 0.28 it is well below the 0.5
coin flip, because it systematically prefers the long, elaborately specified
negatives. No number from this slice is interpretable without this row next to
it.

Two further findings from freezing the pairs:

* 121 of 200 gold-negative pairs pass the R2 criterion; 79 do not, mostly
  because the negative proposes a methodology without committing to an outcome.
* **RBV-14 has no evaluable pair at all.** Its original row-level R2 rationale
  cited a negative attributing variation to "tree-species composition and
  competition", but the two candidates that mention species (H4, H10) are
  reconstruction-methodology proposals that make no attribution claim. The team
  accepted the audit: its row-level R2 pass was incorrect. RBV-14 keeps its place
  in the dataset and in the secondary listwise metrics, is marked
  `no_evaluable_pair`, and is excluded from the primary metric. No negative was
  manufactured for it. See `docs/DECISIONS.md` §11 and
  `benchmark/dev/screening_corrections_v1.json`.

---

## 5b. The original questions

1. **Is Crossref `created` an acceptable cutoff basis?** It drives 18/20 cutoffs,
   and for 9 items it precedes the stated publication date by 49–249 days. If it
   is the article-in-press date, the cutoffs are right. If it is only a
   registration artifact, the cutoffs are too early and every literature method is
   handicapped (safely, but unevenly across items). A manual check of a handful of
   items would settle it.
2. **Unlinked preprints of the source papers.** Only RBV-12 exposes a preprint
   through Crossref `relation`; the other 19 records now carry an explicit
   "no preprint relation in Crossref" note. Nature/Icarus/Elsevier records
   frequently have arXiv or bioRxiv versions that Crossref does not link, and an
   unlinked preprint is the exact failure mode the cutoff exists to prevent —
   the source paper's own claims inside the eligible window.
   `temporal.block_source_by_title` now removes a retrieved record whose title
   matches the source paper, which catches the preprint *if it is retrieved*.
   It does **not** move the cutoff, so other papers published between the
   preprint posting and the journal date may still cite or build on it. Closing
   that gap needs a title/author lookup against arXiv or Semantic Scholar at
   cutoff-resolution time — a decision for the research team, not the harness.
3. **The model's parametric knowledge is post-cutoff.** Retrieval is temporally
   safe; the language model is not. For 2022–2024 source papers a current model
   may simply recall the outcome. The direct-judge baseline doubles as a
   memorisation probe — if it is already strong without literature, the benchmark
   is measuring recall rather than verification. Needs an explicit position in the
   paper (and possibly a memorisation-diagnostic experiment).
4. **What exactly is being scored?** The prompts ask for "the probability that
   this candidate is the hypothesis subsequently supported". The alternative —
   "the probability this hypothesis is true" — is a different quantity, since more
   than one candidate can be true. Confirm before the graph verifier inherits the
   convention.
5. **Listwise over 11 candidates vs a frozen pairwise subset.** The dev manifest
   anticipates "freeze a pair-level subset if experiments use pairwise". Currently
   ranking is listwise and pairwise accuracy is derived from listwise scores.
6. **Candidate-text asymmetry.** The gold hypothesis is typically one paragraph
   of plain prose; the negatives are multi-paragraph proposals with fabricated
   numbers and reference placeholders. A judge can exploit length and style
   instead of science. The slice must not be rewritten (§34), so the question is
   whether to report a length/style-bias diagnostic alongside the headline
   metrics.
7. **How should `direct_rag` turn evidence into a ranking?** `ranking_signal:
   llm_score` uses the assessor's scalar; `ordinal_map` uses the centralised
   log-LR table, under which all-`no_evidence` instances tie at 0. The second is
   closer to the paper's model, the first produces a usable ordering more often.
8. **Does source blocking go far enough?** DOI and title matching catch the
   paper itself and its preprint. Companion papers by the same authors
   describing the same work remain eligible if they predate the cutoff. Whether
   that is leakage or legitimate prior literature is a judgment call that should
   be made explicitly.
9. **Date verification is `boundary_only` (±180 days).** A provider date wrong
   by more than that window is never cross-checked against Crossref. `always`
   closes the gap at the cost of one Crossref call per retrieved record.

---

## 6. Operational note

`S2_API_KEY` is now set and Semantic Scholar search works. Its `/paper/search`
endpoint still returns intermittent 500s and 429s in bursts (the same query
succeeds on retry), so `literature.http.max_retries` is 8 with a 90 s backoff
cap: one unrecoverable query leaves a whole instance unscored, because a partial
score vector is not a ranking.

With `verify_dates_with_crossref: always` a cold `direct_rag` run costs roughly
one Crossref lookup per retrieved record on top of one Semantic Scholar search
per query, so the first pass over all 20 instances takes hours. Everything is
cached, so re-runs are fast and fully reproducible offline (`--offline`).

**Recovering a failed instance.** Because an unrecoverable query leaves the whole
instance unscored, and because Semantic Scholar fails in bursts, the recovery
path is simply to re-run that instance: the already-successful queries come back
from the cache and only the failed ones touch the network. Observed on RBV-19 —
first attempt 9 retrieval errors, second 2, third 0 and scored. Note that model
calls are *not* cached, so each re-run re-spends LLM tokens; an LLM response
cache keyed by (prompt, model, parameters) is the obvious next efficiency step
and is not implemented.
