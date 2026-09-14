# Resolved scientific decisions

The open questions from `docs/MILESTONE_1.md` §5 were decided by the research
team. This file records each decision, how it is implemented, and what it
changed. Nothing here was chosen by the implementation.

Date decided: 2026-09-11.

---

## 1. Crossref `created` is not an eligible cutoff basis

> Remove Crossref `created` from eligible cutoff-basis fields; keep it only as
> diagnostic metadata.

**Implementation.** `crossref.cutoff_basis_fields` lists the fields allowed to
set a cutoff and excludes `created`; `date_fields` still records it. When
`created` precedes the selected basis by more than 30 days, the instance is
flagged `ambiguous` with the gap in its notes — the deposit timestamp is now a
warning signal rather than a date.

**Effect.** The basis changed from `created` (18/20) to `issued` (18/20).
Cutoffs moved *later* for most instances, so more literature is now eligible.
The `created` gaps that used to set those cutoffs (49–249 days) are now the
flagged ambiguity: an article-in-press may have been public before the cutoff.

## 2. Resolve the earliest public version by title/author search

> Resolve the earliest public source version using title/author/version search,
> including unlinked preprints.

**Implementation.** `src/benchmark/versions.py` searches Crossref
bibliographically for the source title and accepts a record as another version
of the same study when the title is close **and** the author lists overlap. The
earliest accepted version sets the cutoff, and every accepted DOI is blocked
from retrieval. Every candidate — accepted or rejected, with its scores and the
reason — is stored in `version_candidates` in the frozen metadata.

**Thresholds** (`temporal.version_search`): title similarity ≥ 0.75, and ≥ 50%
of the smaller author list shared. Calibrated against the observed separation on
this slice: true preprint/journal pairs score 0.87–0.97 author overlap, while
same-author-different-study pairs score 0.20–0.33. Without the fraction rule the
search accepted three different-study records.

**Effect.** Found the unlinked bioRxiv preprint of RBV-19
(`10.1101/2023.05.07.539780`, 13/15 shared authors), moving its cutoff from
2024-02-20 to **2023-05-07** — nine months of literature that would otherwise
have been eligible alongside the source study's own preprint. RBV-12's
Crossref-linked preprint was independently rediscovered, which is a useful
check on the method.

## 3. Scores are relative support, not absolute truth

> Define model scores as relative support over the candidate set, not absolute
> scientific truth.

**Implementation.** New prompt versions `direct_judge_v2` and
`direct_rag_assess_v2` (v1 files are kept, since prompts are versioned method
artifacts). Both state that a score expresses relative support *within this
candidate set*, is comparable only inside the set, and is not a claim about
absolute scientific truth.

## 4. A frozen pair subset, screened by the R2 criterion

> Freeze a pair-level subset by applying the existing semantic-comparability
> criterion to every raw gold-negative pair; retain all passing pairs.

**Implementation.** `scripts/build_pair_subset.py` applies R2 — *addresses the
same scientific target* **and** *disagrees with a substantive part of the gold* —
to all 200 gold-negative pairs, using prompt `pair_comparability_v1`. All passing
pairs are retained in `benchmark/dev/pairs_v1.jsonl`; failing pairs are kept in
the same file with their rationale so the screen is auditable.

The two criteria are answered separately and the verdict is derived from them,
so a model that answers the criteria one way and states the opposite verdict
cannot overrule its own answers. A judge failure is recorded as `ERROR`, never
`FAIL`, so a broken run cannot silently shrink the benchmark; re-running rejudges
only errors. The screen sees `(question, gold, negative)` only — no literature,
no method output — so it is outcome-blind exactly like the slice.

## 5. Pairwise is primary; listwise is secondary

**Implementation.** `pair_accuracy` over the frozen subset is the primary
metric (micro-averaged over pairs, with `pair_accuracy_macro` alongside).
Listwise top-1, MRR and mean gold rank are reported as secondary, and the
old all-negatives pairwise number is renamed `pairwise_accuracy_all_negatives`
so it cannot be mistaken for the primary one. Run summaries and per-instance
reports print the primary block first.

## 6. Artifact baselines

> Add a question-hidden/style-artifact baseline.

**Implementation.** Two methods, both literature-free:

* `style_artifact` — ranks by a surface feature (default: character count). No
  model, no question. This is the no-science floor.
* `question_hidden_judge` — the direct judge with the scientific question
  withheld; its template has no `$question` placeholder at all.

Any method that does not clear these is ranking style, not science.

## 7. Ordinal/log-LR aggregation is the primary Direct-RAG rule

**Implementation.** `baselines.direct_rag.ranking_signal: ordinal_map` is the
default: the ordinal evidence label is mapped through the centralised log-LR
table in `configs/ordinal_mappings.yaml`. Both rules are always computed and
saved (`scores_ordinal_map`, `scores_llm`, with rankings for each), so the
scalar remains available as a secondary view. Ties are a legitimate outcome —
all-`no_evidence` instances tie at 0 — and are scored as ties (0.5 per pair)
rather than broken.

## 8. Block alternate versions, not co-authors

**Implementation.** Three layers, in order of precision: DOIs discovered by the
version search (§2); Crossref `relation` preprint links; and, at retrieval time,
a title match **plus** a shared author
(`temporal.block_source_requires_author_overlap`). Author overlap alone never
blocks anything — an earlier unrelated paper by the same group is legitimate
prior literature.

## 9. Crossref-verify every retrieved record

**Implementation.** `literature.verify_dates_with_crossref: always`. Every
retrieved record with a DOI has its date checked against Crossref (cached), not
just those near the boundary. `verify_boundary_window_days` now applies only to
the `boundary_only` mode.

## 10. The closed-book judge is the memorisation diagnostic

**Implementation.** Framing, recorded in `configs/mvp.yaml`, the method registry
and the docs: `direct_judge` sees no literature, so whatever it scores comes from
the model's training data rather than the pre-cutoff record. It is reported as a
diagnostic of parametric memorisation, not as a literature-free competitor. Read
together with the artifact baselines it bounds how much of any result is
memorisation plus style.

---

# Follow-up decisions (2026-09-11, after the pair audit)

## 11. RBV-14 is excluded from the primary metric, not repaired

> Remove it from the primary pairwise evaluation. Keep the original instance in
> the dataset and, if useful, in secondary listwise diagnostics, but mark it as
> `no_evaluable_pair`. The pair-level audit has now established that its
> row-level R2 pass was incorrect. I would not manufacture a negative for it.

**Implementation.** `PairSubset.status_for()` returns `no_evaluable_pair` for an
instance whose every negative failed R2. That status is written onto the
instance's metric row, counted in `summary.json`
(`n_instances_no_evaluable_pair`, `instances_no_evaluable_pair`), named in the
run log and stated on the instance report. The instance still loads, still runs,
and still appears in the secondary listwise metrics.

The row-level screen is a frozen artifact and is not edited. The correction is
recorded separately in `benchmark/dev/screening_corrections_v1.json`, which
keeps the original R2 rationale and the audit finding side by side.

**Not done:** no negative was written, rewritten or substituted. The slice text
stays verbatim ResearchBench (§2, §34).

**Effect.** The primary metric is computed over 121 pairs across 19 instances.
Anyone reading a result sees the nineteen, not an unexplained twenty.

## 12. Version-search thresholds are frozen for the MVP

> Freeze the current title >= 0.75 and author_overlap >= 0.50 thresholds for the
> MVP. They have a clear empirical separation on this slice and are
> configuration-visible. But before using them in a final benchmark, validate
> them on a small independently sampled set of source/preprint and
> same-author-different-study pairs. Do not tune them further on these 20.

**Implementation.** The values stay in `configs/mvp.yaml` under a `FROZEN FOR
THE MVP` banner, and `tests/test_frozen_thresholds.py` fails if either the YAML
or the code default moves — so a change has to be deliberate and documented
rather than a quiet edit or a tuning pass. A further test asserts that the
separation they were chosen on still holds, so a change to the similarity or
author-overlap computation cannot silently reclassify the known preprint pairs.

**Validation before final use.** `scripts/validate_version_thresholds.py` scores
an **independently sampled** labelled set — pairs of (source DOI, candidate DOI)
marked `same_study` true/false — at the frozen thresholds and reports precision,
recall and the score distributions on each side. It deliberately does **not**
search for better thresholds: it reports how the frozen ones perform on data
they were not chosen on. Build the labelled set from source papers outside these
20 cases.

---

# Follow-up decisions (2026-09-11, autonomous session)

## 13. Official v2 reverts to [0.75, 1.33]; the widened slice is a diagnostic

**Implementation.** `benchmark/v2/` was rebuilt at the originally specified band,
walking further down the same screening order to reach the target: **100 pairs
across 57 source rows** (the widened build reached 102 pairs across 47 rows). The
widened slice is kept verbatim at `benchmark/v2_widened_diagnostic/`. Cached row
and pair screening decisions were reused, so no row was re-judged more leniently.

**Effect.** Tighter band, weaker length cue: shortest-text-first falls from 0.809
(widened) to **0.760**, and the gold is the shorter text in 74% of pairs rather
than 79%.

## 14. v1 and v2 are development sets, stamped as such in code

**Implementation.** `dataset.status: development` is a typed config field. Every
run writes it into `manifest.json`, puts an `interpretation_warning` in
`summary.json`, logs a warning at start, and prints a banner on every instance
report. `benchmark/dev/STATUS.md` and the v2 manifest carry the same statement
with the numbers that justify it.

## 15. Milestone 2 is operational

See **`docs/MILESTONE_2.md`** for the build, the exact inference, and four
findings from the debug runs — the most consequential being that node merging
never fires and that lowering its threshold would not change that, because
propositions generated from competing hypotheses are lexically unrelated (max
cross-hypothesis similarity 0.460) rather than near-duplicates.

## 16. A canonicalized evaluation benchmark, protocol frozen first

**Implementation.** `docs/CANONICAL_PROTOCOL.md` was written and frozen before
any pair was built, including its success criterion. Every candidate — gold and
negative alike — is rewritten by one fixed transformation that never learns the
candidate's role, then checked for semantic preservation, then re-screened for
pair comparability on the *canonical* texts. There is no length gate.

**Yield.** 105 pairs across 21 source rows; 219 of 231 canonical claims (94.8%)
passed preservation.

**Effect, against the criterion declared in advance:**

| diagnostic | v1 | v2 | canonical |
| --- | --- | --- | --- |
| gold is the shorter text | 0.984 | 0.740 | **0.571** |
| shortest-text-first | 0.988 | 0.760 | **0.605** |
| question-hidden judge | 0.785 | 0.890 | **0.686** |

**Verdict: the slice FAILS the style diagnostic and is not yet usable as an
evaluation benchmark.** Both 0.605 and 0.686 sit outside a within-0.1-of-chance
band. Per the protocol this is reported, not tuned away.

This verdict supersedes an earlier, sloppier reading of the criterion, and the
correction is worth recording because it is a pre-registration failure of exactly
the kind the protocol was meant to prevent:

* The frozen protocol says "both length heuristics near 0.5, and the
  question-hidden judge substantially below the 0.870 it scores on v2". It gives a
  number for neither bar. "Near" and "substantially below" are not criteria.
* `scripts/write_canonical_report.py` operationalised them as `|acc - 0.5| <= 0.1`
  and `acc < 0.75`. **The 0.75 was chosen by me while writing the report, after
  seeing that the answer was 0.686.** That is a post-hoc threshold, however
  defensible the number looks.
* `docs/STATUS_2026-09-11.md` then compounded it by printing "within 0.1 of
  chance" as the criterion for *both* rows while marking 0.686 a pass — which is
  internally contradictory on its face.

The research owner has now set both bars explicitly at within 0.1 of chance. That
is applied to the verdict; the protocol's original text is left unedited, since
rewriting a frozen pre-registration to match a later decision is the error this
entry exists to document.

Also relevant to "substantially below": the question-hidden judge is not
deterministic. The same prompt over the same 100 official v2 pairs scored 0.870 at
20:47 and 0.890 at 21:30 — two pairs flipped. Differences of ~0.02 in these
diagnostics are noise, so any future bar should be stated with a margin wider than
that, or the diagnostic should be run with several seeds and averaged.

---

## What this leaves open

* Whether the `created`-vs-`issued` gaps (10 instances flagged) mean those
  articles were public as article-in-press before the cutoff. Deciding this
  needs a manual check of a few publisher pages; the flag stays until then.
* Version search currently queries Crossref only. arXiv records without a
  Crossref DOI are invisible to it (`temporal.version_search.provider` is the
  hook, and a Semantic Scholar provider is the obvious addition now that a key
  is available).
* The pair screen is a single LLM judgment per pair with no human adjudication.
  The decisions file records rationales for exactly this reason. RBV-14 is the
  case where that audit overturned a row-level decision; there may be others in
  the opposite direction (pairs it passed that a human would reject).
* Canonicalisation reduced both artifacts but did not eliminate the length cue
  (0.605). Either the transformation needs a length-neutralising constraint, or
  0.605 is accepted and reported alongside every result on this slice.
* The canonical slice is 105 pairs from 21 rows, so pairs are not independent and
  one discipline may dominate; report per-row numbers too.
* Whether minimal contrast pairs (changing only the scientifically relevant
  relation) are worth building is still open, and was deliberately postponed until
  the verifier was known to work. It now is.
* The frozen version-search thresholds have been validated on the 20 development
  cases only. `scripts/validate_version_thresholds.py` exists to check them on an
  independent sample, and that sample has not been collected yet.

## 17. Proposition granularity: discriminativeness vs assessability

**Status: RESOLVED and partly superseded.** Option 1 below was implemented as
`consequence_generate_v2` (see `docs/MILESTONE_2.md`). It did what it was meant to do
to proposition *shape* and raised the yield at k=2 from 40% to 49%, but the k-effect
this entry was built on turned out to be confounded with instance identity, and the
yield on the k=11 instance did not improve. See DECISIONS #24 for the withdrawal and
for what the evidence now points at. The text below is left as written.

The debug runs measured a strong trade-off (see `docs/MILESTONE_2.md`): the
fraction of propositions that yield informative evidence is 40% with two
candidates and 4% with eleven, and neither depth nor abstract availability
explains it. `consequence_generate_v1` asks for consequences that distinguish the
focal claim from the alternatives; with many alternatives the model satisfies that
by writing multi-clause conjunctions, which no single abstract can settle, so the
assessor returns `no_evidence` and the node contributes exactly zero.

Three options, none taken yet:

1. **Decompose.** Ask generation for atomic, separately-checkable propositions and
   let cross-evaluation supply the discrimination. This is the principled option —
   the two jobs are already architecturally separate — and it is what §35 implies.
   It changes the generation prompt, so it needs a new version (`_v2`) with v1 kept.
2. **Assess clause-wise.** Keep conjunctive propositions but let the assessor
   return a partial verdict. This puts the decomposition in the wrong place and
   makes the ordinal evidence scale ambiguous.
3. **Cap candidates per graph.** Build graphs pairwise and aggregate. Cheap to do,
   but it abandons the listwise formulation.

Deliberately **not** done: raising `max_nodes` further to compensate. More nodes at
the same specificity buys more zeros. The measurement is in
`runs/graph_diagnostics_pooled.json` and is reproducible with
`scripts/graph_run_diagnostics.py`.

## 18. Consequence-graph diagnostics use the shared metric key names

`consequence_graph` emitted `n_informative` / `n_no_evidence`, while
`src/experiments/metrics.py` aggregates `n_informative_assessments` /
`n_no_evidence_assessments` (the names `direct_rag` uses). Aggregate diagnostics
therefore came back `None` on graph runs even though the per-instance artifacts had
the numbers. Renamed the counters to the shared names and added
`n_nodes_unobserved`, `n_shared_nodes`, `n_merged_nodes` and
`n_nodes_with_informative_evidence` to the aggregated set. Per-instance artifacts
already written keep their old key names; `scripts/graph_run_diagnostics.py` reads
the artifacts directly and is unaffected.

## 19. `text_similarity` was asymmetric and autojunk-distorted

**Fixed.** `src/graph/merge.py` used `SequenceMatcher(None, a, b).ratio()`. Two
defects, both measured over the 1,323 within-instance cross-hypothesis proposition
pairs in the Milestone 2 debug runs:

* **autojunk.** `SequenceMatcher` treats elements occurring in more than 1% of its
  second argument as junk once that argument exceeds 200 characters. Propositions
  run to ~300 characters, so this was always on. It shifted similarity by a mean of
  **0.234** (max 0.473) and depressed the cross-hypothesis maximum from 0.677 to
  0.460.
* **asymmetry.** Because the heuristic keys off the second argument alone,
  `sim(a, b) != sim(b, a)` for **95%** of pairs. Worst observed case: 0.031 one way
  and 0.451 the other, for two propositions sharing the phrase "fetal tissues from
  diabetic pregnancies" verbatim. A similarity used for deduplication must not
  depend on iteration order.

Now `autojunk=False`, with the pair sorted before comparison so symmetry is
structural rather than incidental. Two tests pin both properties, using the real
worst-case pair.

**What this changed in the conclusions.** `docs/MILESTONE_2.md` had claimed that a
threshold of 0.60 would still merge nothing. With the corrected function, 0.60
would merge 3 cross-hypothesis pairs and 0.50 would merge 44. The frozen threshold
of 0.82 still merges nothing (cross-hypothesis max 0.677), so no previously
reported run is affected — zero merges was the right answer for the wrong reason.

`merge_threshold` is left at 0.82, by instruction.

## 20. Review articles are excluded as source papers (task validity)

**Implemented as a construction gate for evaluation benchmarks; frozen development
slices are flagged, not edited.**

A review's "gold hypothesis" summarises work already published, so the finding sits
in the pre-cutoff literature by construction and retrieval can return the primary
paper that established it. Observed directly: `RBV2-0012-N00`'s source is a *Trends
in Cell Biology* review, and the consequence-graph debug run retrieved the primary
paper. ResearchBench's R3 criterion ("presented as supported by the source study")
does not exclude reviews.

**This is not a rare case.** Full audit of the 962 deduplicated ranking rows, using
Crossref metadata resolved for every DOI (free, no LLM cost):

| slice | review-source DOIs | of | share |
| --- | --- | --- | --- |
| full ranking set | **94** | 962 | **9.8%** |
| official v2 | 4 | 57 | 7.0% |
| canonical | 3 | 21 | 14.3% |
| v1 dev20 | 0 | 20 | 0% |

Detected by venue and title patterns in `configs/mvp.yaml`, because **Crossref
types review articles as `journal-article`** — the disulfidptosis review above is
typed exactly that, so there is no authoritative field to read.

**Two calibration decisions, both made against measured output:**

* `"Advances in "` and `"Progress in "` were in the first pattern list and matched
  *Advances in Space Research* and *Progress in Natural Science: Materials
  International*, both primary-research journals. Removed. Excluding them would
  have dropped valid rows and skewed the surviving set by discipline, which is a
  worse failure than missing a review. A test pins this.
* A DOI with no cached Crossref record yields **no verdict**, and the row is kept.
  A missing lookup is not evidence of "not a review", in the same way an API
  failure is never read as `no_evidence` in the verifier.

**Known gap, not patched:** a review published in a general-purpose journal with a
title that does not announce itself is not detected. Closing it needs the abstract
and probably a classifier. `TODO(research)`.

## 21. Pair judgments must be scored in both orders

**Fixed in `scripts/v2_artifact_diagnostics.py`; affects an already-reported number.**

Every pair-judge diagnostic so far presented each pair once, with a seeded per-pair
coin flip deciding whether the gold was option A or option B. That removes
*positional identifiability of the gold*, which is what it was designed for, but it
does not remove **position preference in the judge**. Measured on the existing
single-order runs:

| slice | chose A | acc when gold@A | acc when gold@B | reported acc |
| --- | --- | --- | --- | --- |
| v1 | 67% | 0.951 | 0.617 | 0.785 |
| v2 official | 61% | 0.980 | 0.760 | 0.870 |
| **canonical** | **85%** | 0.983 | **0.319** | 0.686 |
| v2 widened | 61% | 0.961 | 0.745 | 0.853 |

On canonical the judge answered "A" for 89 of 105 pairs. The gold happened to sit in
A for 58 of 105, and `0.552 * 0.983 + 0.448 * 0.319 = 0.686` reproduces the reported
accuracy to three decimals. An always-answer-A baseline scores 0.552 on that slice,
so of the reported 0.686 only a modest part is content.

Now every pair is judged in **both** orders and the two outcomes averaged: credit
1.0 (right both ways), 0.5 (order-dependent), 0.0 (wrong both ways). Position
preference then cancels exactly rather than approximately. The result also carries
`position_preference_chose_a` (0.5 = unbiased) and `order_consistency` (fraction of
pairs answered the same way both ways) so the confound stays visible.
`--single-order` reproduces the old behaviour for provenance.

**Consequence for the canonical verdict:** its question-hidden number is confounded
and the counterbalanced re-run supersedes it. The length diagnostics are unaffected
— they are deterministic and order-free.

**Not yet addressed:** the consequence verifier's own edge assessor sees all
candidates in one list, so it has the same exposure. The per-instance shuffle
decorrelates position from gold, but a full fix means running each instance in
several candidate orders, which multiplies cost by that factor. `TODO(research)`.

## 22. k=2 pairwise is the primary metric; k>2 is stratified, never averaged

Recorded in full in `docs/EVALUATION_PROTOCOL.md`. The decisions:

* The **formulation** is for arbitrary `H = {H_1..H_k}`, k >= 2. The **protocol** is
  a separate matter and pins k=2 as the headline.
* Ties in pairwise accuracy score **0.5** explicitly (already the case in
  `pair_metrics`; now also stated and tested).
* Top-1, MRR and mean gold rank appear **only** inside `by_k`, each beside its own
  `chance_top1 = 1/k`. Averaging top-1 across mixed k has no single baseline and is
  now impossible to do by accident.
* Two metrics are pooled across k because their chance level is k-independent:
  normalised gold rank `1 - (rank-1)/(k-1)` and the pairwise win rate inside a
  listwise task (ties 0.5).
* Controlled k-sets are built from R2-screened negatives only, **nested** across k
  (the set at k takes the first k-1 of a frozen per-row order), with the sampling
  frozen before any verifier runs.
* k=5 is not built: 7 rows have >= 4 screened negatives. Reported, not manufactured.
* We do not describe k>2 as "harder" but as a different, more constrained ranking
  problem.

## 23. Lexical merging is unsafe for atomic propositions — 8 of 9 merges were wrong

**Blocking finding. Needs a research decision; nothing silently changed.**

Under `consequence_generate_v1` merging never fired, and DECISIONS #19 / MILESTONE_2
called it inert. Under `consequence_generate_v2` it fires readily — 9 merges across
5 k=2 instances — and **8 of the 9 are scientifically wrong**:

| similarity | kept | merged away |
| --- | --- | --- |
| **0.944** | "**Autophagy** is activated in cancer cells undergoing disulfidptosis…" | "**Necroptosis** is activated in cancer cells undergoing disulfidptosis…" |
| 0.903 | "**Amino acid** concentrations in fetal tissues differ…" | "**Serine** in fetal **brain** tissue differs…" |
| 0.898 | "altered NADPH/NADP+ ratios" (generic) | "altered NADPH/NADP+ in **placental** tissue" |
| 0.893 | "altered NADPH/NADP+ ratios" | "**lower** NADPH/NADP+ in **heart** tissue" |
| 0.883 | "altered NADPH/NADP+ ratios" | "**higher** NADPH/NADP+ in **liver** tissue" |
| 0.853 | "**G6PD** activity is lower in fetal liver…" | "**IDH** activity is different in fetal liver…" |
| 0.852 | "**G6PD** activity is reduced in fetal tissues…" | "**IDH** activity is altered in fetal tissues…" |
| 0.844 | "**glutamine** in fetal **liver** is higher…" | "**branched-chain amino acids** in fetal **muscle** is altered…" |
| 0.882 | "Pulp … incorporating 5-10 wt% CNFs … exhibits higher tensile strength" | "Pulp … with 5-10 wt% CNFs … has higher tensile strength" — **the one genuine duplicate** |

Two of these collapse *opposite directional claims about different tissues* into a
single node, so the graph can no longer represent that NADPH/NADP+ rises in liver
and falls in heart. Two collapse different enzymes. One collapses two different
cell-death pathways.

**Why atomicity caused it.** Atomic propositions share a syntactic template and
differ only in the entity, tissue or direction — which is a small fraction of the
characters but all of the science. `SequenceMatcher` on normalised text is measuring
the template. This is structural, not a tuning problem: the worst case scores
**0.944**, so no threshold below ~0.95 helps, and one that high would merge nothing
at all, including the genuine duplicate at 0.882. Fixing it needs a matcher that
knows which tokens are entities.

`merge_threshold` is left at 0.82 and `semantic_merge_mode` at `lexical`, by
instruction. A strict-xfail test records the defect and will fail the moment the
matcher improves.

**Recommendation for the next iteration:** set `semantic_merge_mode: none` while
generation is atomic. Cross-evaluation already makes propositions that every
candidate predicts inert by construction, so merging is buying redundancy removal at
the price of destroying real distinctions — a bad trade at 1 good merge in 9.

**Effect on the A/B comparison.** Only `RBV2-0038-N04` merged heavily (7 of 20 nodes);
the other four instances merged 0 or 1. Excluding it, the informative-evidence rate
comparison is 42.5% (v1) against **55.1%** (v2) on the same four instances.

## 24. Assessor strictness, not proposition shape, is the binding constraint on novel-mechanism instances

**Open. Requires a decision on `evidence_assess_v1`.**

DECISIONS #17 attributed the collapse in informative-evidence rate at k=11 to
conjunctive propositions. `consequence_generate_v2` fixed the conjunctions — median
proposition length on `RBV-19` fell from 54 tokens to 18, clause markers from 2.05 to
0.07 — and the yield did **not** improve: 2 informative nodes of 44 became 1 of 40.

**The comparison behind #17 was confounded and the claim has to be withdrawn in that
form.** Both k=11 measurements are the same instance, `RBV-19`; the five k=2
measurements are five different instances. k varied together with instance identity,
so "40% at k=2 versus 4% at k=11" could always have been an instance effect. It
appears to have been one. Disentangling k from the instance is what the nested
k-slices are for (`docs/EVALUATION_PROTOCOL.md` §4): the same row at k=2, 3 and 4,
with candidates nested so nothing changes but the size of the set.

**What the evidence now points at.** On `RBV-19` under v2, propositions are atomic
("IL-10 increases sphingosine kinase activity in macrophages"), queries are clean and
outcome-neutral, and retrieval returns topically adjacent papers. The assessor
declines them all with the same reason:

> "None of the retrieved literature **directly** investigates the effect of IL-10
> stimulation on the phosphorylation of sphingosine kinase in macrophages. While some
> studies discuss sphingosine kinase phosphorylation…"

It is factually correct — `RBV-19`'s cutoff is 2023-05-07 and IL-10-driven
sphingolipid metabolism in macrophages was a novel mechanism, which is why the source
paper exists. But requiring literature that *directly* addresses the proposition
excludes exactly the indirect, adjacent evidence a consequence graph is meant to
accumulate. Four rationales on this instance turn down papers they themselves
describe as related.

**The tension is structural.** `no_evidence` must keep meaning "this moves nothing"
(§35.5), so the fix cannot be to let weak topical adjacency count as support —
that would manufacture signal. But a prompt that only accepts direct address makes
the graph useless on exactly the instances where indirect reasoning is the point.

Options, none taken:

1. Let the assessor rate evidence that bears on the proposition *through a stated
   mechanism*, with the mechanism recorded, kept distinct from direct evidence.
2. Add an explicit `indirect_support` / `indirect_contradiction` level to the ordinal
   scale, mapped to a smaller likelihood ratio than direct support.
3. Leave it, and accept that the method only works where adjacent literature is
   dense — which would need saying plainly in the paper.

Option 2 is the most honest about what the numbers would then mean, and it is a change
to `configs/ordinal_mappings.yaml` as well as to the prompt, so it needs calibration
(§23) alongside it. Not to be done on five instances.

## 25. `no_evidence` currently means "not directly investigated", which is the wrong construct

**Rubric proposed, not adopted. `evidence_assess_v1` unchanged.**
See `docs/ASSESSOR_RUBRIC.md`.

DECISIONS #24 raised this from four rationales on one instance. Measured across
**528 assessments** from every consequence-graph run, it is systematic:

| | n | share of `no_evidence` |
| --- | --- | --- |
| `no_evidence` verdicts | 343 | — |
| …invoking *directness* | 340 | **99%** |
| …saying the literature "does not **directly**" address the proposition | 331 | 97% |
| …**conceding related work was retrieved**, then declining it | 280 | **82%** |

So the label reports "no retrieved paper directly investigates this proposition",
not "the retrieved literature does not bear on this proposition". A consequence
graph is built on the second notion: its propositions are consequences, so it is
normal that nobody has tested them head-on.

This is under-specification in the prompt, not model misbehaviour.
`evidence_assess_v1` lists "how direct the reported measurements are" as one
consideration among several and never defines "bear on the proposition"; the model
resolves the ambiguity conservatively and consistently.

**What was built, and deliberately not switched on:**

* `docs/ASSESSOR_RUBRIC.md` — the construct: DIRECT / INDIRECT / NO EVIDENCE, with
  the five admissible indirect link types enumerated so "indirect" cannot quietly
  become "related".
* The safeguard against manufacturing signal: an indirect judgment must state the
  inferential link in one sentence naming the record. **No link stated ⇒
  `no_evidence`.** Machine-checkable.
* Directness as a separate field rather than new labels, so the discount is one
  calibratable number: `log_lr = evidence_log_lr[label] × directness_factor[directness]`,
  with `directness_factor.indirect` left `TODO(research)`. Setting it to 0.0
  recovers exactly today's behaviour.
* `proposition_unassessable`, separating a proposition that cannot be checked as
  written (`"specific genetic alterations"`, never named — a *generation* defect)
  from a genuine retrieval failure. Today these are indistinguishable, so the
  generation prompt never gets the feedback.
* `src/llm/prompts/evidence_assess_v2.txt` — a candidate implementation. **Not
  referenced by any config**; a test asserts the running assessor is still v1.
* `benchmark/assessor/labelset_candidates.jsonl` — 37 real cases with abstracts,
  stratified with the `no_evidence`-that-concedes-related-work stratum over-sampled.
  Six carry proposed labels; one disagrees with the current assessor.
* `scripts/assessor_agreement.py` — replays labelled cases through any assessor
  prompt without re-running retrieval, reporting direction agreement, exact
  agreement, the informative/`no_evidence` confusion matrix, and unlinked indirect
  judgments. It warns when a prompt raises the informative rate without raising
  direction agreement, which is the signature of manufacturing evidence.

**The six proposed labels are the implementing agent's, not ground truth**, and the
harness says so on every run. They make the rubric concrete; they do not settle it.

`no_evidence` keeps a log-LR of exactly 0 and absence is still never contradiction —
both invariants are unchanged and tested.

**Before any large sweep:** sign off the construct, adjudicate the labels, calibrate
`directness_factor.indirect`, and measure agreement for v1 and any v2. Until then an
"informative-evidence rate" measures the current assessor's idiosyncrasy, not method
quality.

## 26. The assessor gate: adjudicate blind, then freeze, then calibrate

**Refines #25 with the research owner's construct definitions and adjudication
protocol. Nothing is calibrated and no sweep is run until this gate passes.**

### The construct, as settled

* `DIRECT` — the record explicitly tests, measures, reports, or states the
  proposition or its negation.
* `INDIRECT` — the record does not test the proposition itself, but establishes a
  **specific intermediate fact** that changes belief in the proposition through a
  named mechanistic, causal, logical, or quantitative link.
* `NO EVIDENCE` — no such proposition-specific link can be stated from the record.

The load-bearing phrase is *specific intermediate fact*. My first draft defined
`INDIRECT` by a taxonomy of link shapes; that taxonomy survives only as a guide,
because a shape can be asserted without naming anything. The fact must be named.

Two **orthogonal axes**, and the separation is deliberate:

    direction  in {supports, contradicts, neutral/no evidence}
    directness in {direct, indirect}

How much weight indirect evidence deserves is a later, separate decision and is
**not** baked into the label taxonomy — which is why there is no `indirect_support`
label.

### The minimal-chain requirement

Every indirect judgment must emit `paper finding -> intermediate fact -> target
proposition` as three strings, plus `requires_unsupported_facts`. If the chain needs
a fact neither the record nor the proposition supplies, the case returns
`no_evidence`. This is what makes "indirect" auditable instead of rhetorical: each
arrow is checkable against the abstract, and it is cheap to audit in bulk.
`scripts/assessor_agreement.py` counts indirect judgments with a missing or
truncated chain, and flags any that admit unsupported facts as rubric violations.

### `proposition_unassessable` is an upstream signal, not a verdict

"Retrieval found nothing that bears on this" and "this proposition was
underspecified" imply completely different fixes — corpus and retrieval work versus
the generation prompt. They are counted on separate channels and never share a
label. The assessor raises the flag only because it is the place with both the
proposition and the literature in view.

### Adjudication protocol, frozen before any case is judged

**Blind** — judges never see v1's label or rationale;
`scripts/build_adjudication_packet.py` strips them and puts the key in a separate
file. **Two independent judgments** per case, disagreements resolved in a third pass
against the rubric, never auto-resolved. The seven `proposed-unreviewed` labels are
seed examples: they illustrate the rubric, they do not determine it, and they are
re-adjudicated blind like everything else.

**The primary statistic is not accuracy on 42 cases.** It is whether two people can
reliably tell *indirect but evidential* from *merely related*, measured as
`boundary_agreement` — agreement restricted to cases where at least one judge said
`indirect` or `no_evidence`, with easy `direct` cases excluded because they inflate a
raw number. If that fails, the `indirect` category is too subjective to calibrate and
no prompt can rescue it.

### The pre-registered gate

`benchmark/assessor/acceptance_gate.json`, thresholds **to be set by the research
owner before adjudication**. v2 replaces v1 only if all three hold:

1. the boundary is learnable (if this fails, 2 and 3 are not evaluated);
2. direction agreement with the adjudicated labels is materially better than v1;
3. the informative-rate gain is not driven by cases the judges call merely related.

`scripts/assessor_agreement.py --gate` **refuses to evaluate while the thresholds are
null**, and says why. That refusal is deliberate: DECISIONS #16 is what happens when
an operationalisation is chosen after the answer is visible.

### Two bugs this work surfaced

* `case_id` was `instance::node`, which collides across runs — the same instance and
  node appear in both A/B arms. One of 37 cases was silently dropped when answers
  were keyed by it. Now includes the run id; a test asserts uniqueness.
* The label set was re-sampled from scratch on every build, so adding a run
  re-strided the selection and swapped cases out from under any adjudication in
  progress. The selection is now preserved by default; `--reshuffle` refuses if any
  case already carries a label.

## 27. Validating the assessor without domain experts

**Supersedes the human-adjudication plan in #26.** No domain experts are available,
so the two-human protocol is replaced by something narrower that is actually
obtainable — and the claim is weakened to match.

**What is no longer claimed:** that `INDIRECT` corresponds to expert judgment.
**What is claimed instead:** that the category is operationally coherent,
reproducible across independent assessors, grounded in the supplied text, and not
manufacturing signal.

### The rubric is frozen

`docs/ASSESSOR_RUBRIC.md` carries a freeze banner with a content hash
(`5d8465ae0088c1ee`, recorded in `benchmark/assessor/rubric_freeze.json`). It is not
tuned against validation results; if it changes, every run against the old stamp is
void. This is the third time this project has needed a pre-commitment device
(DECISIONS #16, #26), so it is now a hash rather than a promise.

### Two independent blinded assessors, not two humans

`assessor_judge_a_v1` decides the category first, then justifies it.
`assessor_judge_b_v1` **is never shown the category names** — it is walked through
five steps (what does the record state; what does the proposition assert; is there a
link; does the link need an outside fact; only then, which way does the evidence
point) and its answers are mapped onto the construct afterwards. A test asserts the
label vocabulary does not appear in B's prompt, because that is what its
decorrelation from A rests on.

> **Only one model deployment exists** (`gpt-4.1-kasia`; `gpt-4o`, `gpt-4o-mini`,
> `o3-mini`, `gpt-4.1-mini` all 404). The judges therefore differ in prompt and
> scaffold but **share a model**, and same-model agreement has correlated errors.
> This is a real weakness, recorded in the gate file, and it is why the grounding
> and adversarial criteria carry the weight rather than agreement alone.

### Grounding is what removes the need for expertise

Every evidential judgment must quote a `supporting_span` **verbatim from the
supplied abstract**, checked by substring match. This reframes the task: the judge
is not asked whether a biomedical claim is true in the world, but whether *this
record states the fact it is being credited with* — answerable from the text.

Five components of the construct are observable without domain knowledge, and the
gate is built on exactly those: does the record state `F`; is `F` named; was an
unsupported bridge introduced; does direction reverse under negation; does the
judgment disappear when the evidential sentence is removed. The part that genuinely
needs an expert — whether the mechanism is *scientifically* legitimate — is the part
not being claimed.

### The gate, pre-registered before the run

| criterion | statistic | threshold |
| --- | --- | --- |
| 1 | boundary **reproducibility** (renamed from agreement) | ≥ 0.80 |
| 2 | direction **reproducibility** | ≥ 0.80 |
| 3 | of judgments newly called evidential: grounded span + no unsupported fact + reproduced by the other judge | ≥ 0.90 |
| 4 | `P(informative | mismatched abstract)` | ≤ 0.10 |

Criterion 3 replaces "precision against resolved human truth" and is stricter than
the 0.75 that would have applied to human adjudication, because consensus between
automated judges is weaker evidence. Criterion 4 is the strongest single check
available without experts.

Controls: `mismatched` (unrelated record), `swapped` (a record genuinely informative
for a *different* proposition — a harder negative), `negated` (direction must flip;
informativeness persisting while direction does not move means the claim is not
being read), `span_removed` (delete the cited sentence; an indirect judgment should
not survive). Negation is a model-free prefix, because control generation must not
depend on the thing under test.

### Wording for the paper

Recorded in the gate file so it cannot drift. Not *"the assessor accurately
distinguishes indirect evidence from merely related literature"*, but *"we
operationalize indirect evidence using an explicit intermediate-fact chain and
validate the assessor through independent-model agreement, source-grounding checks,
and adversarial controls"* — with "independent-model" downgraded to
"independent-prompt" while only one deployment exists.

Passing unblocks calibration and the 18-row development sweep, with the assessor
marked **provisionally validated**.

## 28. The assessor gate FAILS — and the failure is exactly where an expert was predicted to be needed

**Result of the validation run over 291 records (1,242 judgments). Rubric frozen at
`5d8465ae0088c1ee` throughout; nothing was tuned.**

| criterion | threshold | value | verdict |
| --- | --- | --- | --- |
| 1 — boundary reproducibility | ≥ 0.80 | 0.882 (κ 0.460) | PASS |
| 2 — direction reproducibility | ≥ 0.80 | 0.897 (κ 0.578) | PASS |
| 3 — grounded **and** independently reproduced | ≥ 0.90 | **0.462** (n=52) | **FAIL** |
| 4 — `P(informative \| mismatched abstract)` | ≤ 0.10 | **0.000** (0 of 582) | PASS |

**Overall: FAIL. Do not calibrate, do not run the sweep.**

### The pilot was optimistic noise

At one record per case, criterion 3 read 0.714 on **7** positives. At all 291 records
it reads **0.462** on **52**. The re-run was a pure power increase — same frozen
rubric, same prompts, same gate — and it moved the answer *down*. Reporting the pilot
as "marginal, probably underpowered" would have been wrong in the optimistic
direction.

### The failure is a one-sided offset, not fuzziness

| | judge B DIRECT | INDIRECT | NO_EVIDENCE |
| --- | --- | --- | --- |
| **judge A DIRECT** | 4 | 4 | 0 |
| **judge A INDIRECT** | 0 | 16 | **28** |
| **judge A NO_EVIDENCE** | 0 | 2 | 237 |

Only-A-says-evidential: **28**. Only-B: **2**. Agreement on *direct* evidence: **8 of
8**. The divergence is almost entirely inside the `INDIRECT` category.

### What the judges actually disagree about

Not the text. On the 28 disputed cases B's stated `connection` mirrors A's
`intermediate_fact` almost word for word — both read the same finding out of the same
abstract. B then sets `needs_outside_fact` on **20 of 28** and "same subject but no
link" on 11.

So both judges agree on **what the record says**, and diverge on **whether the step
from that fact to the proposition is licensed**. Grounding is perfect on A's side:
52/52 spans verbatim, 52/52 claiming no unsupported fact.

**This is precisely the decomposition the research owner predicted.** The observable
components reproduce:

* does the record state `F` — both judges find the same `F`;
* is a span quotable — 52/52 verbatim;
* is the record unrelated — 0 false positives in 582 mismatched abstracts.

The non-observable component does not:

* is the bridge from `F` to the proposition scientifically legitimate — **28 vs 2**.

That was named in advance as the part needing a domain expert, and the data now shows
it empirically rather than by assumption.

### What this does and does not mean

It does **not** mean the assessor hallucinates: nothing was fabricated, and the
negative controls are as clean as they could be (0 of 582). It means the rubric's bar
for *"establishes a specific intermediate fact that changes belief"* is not
operationalised tightly enough for two readers to apply it the same way — the very
question criterion 3 was built to ask, answered no.

### Options, none taken

1. **Narrow the construct** to B's stricter reading: count indirect evidence only
   where the bridging step is stated *in the record itself*. Would raise
   reproducibility and shrink the category substantially.
2. **A second model.** The judges share `gpt-4.1-kasia` (no other deployment exists),
   so some of the offset may be prompt-scaffold rather than construct. Cross-model
   judging would separate these; it cannot be done on this account today.
3. **Bounded expert input** on the bridge question alone, for a sample — the one
   component that provably needs it, now localised.
4. **Drop indirect evidence** and accept the method only works where direct evidence
   exists, saying so plainly in the paper.

The rubric stays frozen and unedited. Changing it now, after seeing this, is the
error DECISIONS #16 exists to prevent.

### Not re-measured at scale

`negated` and `swapped` were run only in the 42-case pilot (direction flipped in 11
of 12; swapped drew 2 informative of 84). They are not in the 291-record run, so those
figures stand at pilot power and are labelled as such.

## 29. Architectural correction: indirectness belongs in the graph edges, not the evidence label

**Motivated by the failure in #28, which is preserved untouched as the evidence for
this change.** Nothing was tuned to make a gate pass; the frozen rubric failed and the
failure identified a conceptual conflation.

### What #28 actually showed

The evidence assessor was being asked two questions at once:

1. *What does the paper report?* — reproducible. Both judges extracted the same fact,
   52/52 spans were verbatim, 0 of 582 mismatched abstracts drew a false positive.
2. *Does that reported fact legitimately imply the proposition?* — not reproducible.
   28 cases one way against 2 the other.

The second question is exactly what the consequence graph exists to represent. Asking
an evidence assessor to answer it collapses two distinct quantities into one label:

    P(X_v | X_pa(v))     scientific implication   -> graph edge
    P(D_v | X_v)         literature evidence      -> evidence assessor

### The correction

**`INDIRECT` is removed as an evidence-assessment category.** The assessor answers
only whether retrieved text bears **directly on the proposition node `X_v` being
assessed** — support, contradiction, mixed, or no relevant direct evidence, with the
existing ordinal strength grades retained because the propagation needs them.

"Direct" here does **not** mean direct evidence for the root hypothesis. A paper can
be direct evidence for a node three hops from `H` while being indirect evidence for
`H` overall:

    H -> X_1 -> X_2 -> X_3        a paper about X_3 is
                                  direct evidence for X_3,
                                  indirect evidence for H.

That is indirect hypothesis verification without asking an evidence assessor to make
the unstable mechanistic leap.

This also explains, after the fact, why atomic consequence generation mattered
(DECISIONS #17): propositions simple enough for papers to address directly are
exactly what makes the evidence task reproducible. The scientific reasoning moves to
the edges, where `edge_assess_v1` already asks the right question — *"if that
candidate were true, how likely would the proposition be?"* — and where it is
recorded, checkable and weighted.

### What changed in the repository

* `evidence_assess_v2` rewritten for the narrow task: direct bearing only, verbatim
  `supporting_spans`, and an explicit `requires_external_bridge` flag that forces
  `no_evidence`. It tells the model *why* the line is drawn there, so it does not try
  to be helpful by bridging — an unrecorded bridge is never checked or weighted.
* The earlier `INDIRECT` draft is archived unused at
  `src/llm/prompts/superseded/evidence_assess_indirect_draft.txt`. It was never
  executed in any run.
* `docs/ASSESSOR_RUBRIC.md` is **left frozen and unedited**. It is the record of the
  construct that failed.
* Two new decorrelated judges (`assessor_narrow_judge_a_v1`, `_b_v1`) for re-running
  reproducibility on the narrow task. Judge B is again never shown the category names.

### Still to do

* Re-run reproducibility for the narrow task (in flight).
* **Separately validate edge judgments.** The hard scientific reasoning now lives
  there explicitly, so it needs its own reproducibility study. Until that exists, the
  graph edges are the unvalidated component and should be described as such.

### A mistake worth recording

A two-case smoke test overwrote `benchmark/assessor/validation.json`, the 350-judgment
broad-task result. It was recoverable only because the event log is append-only;
`benchmark/assessor/validation_42cases.json` is the reconstruction, matching the
pre-overwrite report to three decimals (0.897/0.951/0.714/0.000 against
0.900/0.952/0.714/0.000 — the small `n` difference is one duplicate proposition text
colliding). `validate_assessor.py` now refuses to overwrite an existing result without
`--force`.

## 30. Node-level yield, and the end-to-end narrow-vs-broad comparison on the debug cases

**Two independent routes to the same answer.** The per-record assessor validation
suggested the narrow evidence rule would leave almost nothing (2.4% of records). It
was measuring the wrong unit: production shows the assessor ten records jointly, so a
node needs only one that directly addresses its proposition.

| | broad assessor | narrow + graph |
| --- | --- | --- |
| informative nodes | 56 / 100 (56%) | **32 / 100 (32%)** |
| posterior separation (top1 − top2, mean) | 0.146 | 0.122 |
| entropy ratio | 0.976 | 0.988 |
| gold ranked first | 4 / 5 | 5 / 5 |
| gold rank per instance | 2, 1, 1, 1, 1 | 1, 1, 1, 1, 1 |
| unsupported inferential bridging | possible | **removed** |

Measured twice: a **controlled** re-assessment holding graph, nodes, edges and
retrieved papers fixed (`scripts/reassess_nodes.py`), and a genuine **end-to-end**
rerun where generation and retrieval re-ran — only 1 of 20 propositions on the first
instance overlapped with the broad arm, i.e. 5%. Both give 32/100 informative. The
controlled arm showed a larger separation loss (0.146 → 0.079) than the end-to-end
one (0.146 → 0.122), so part of that loss was an artifact of forcing the narrow
assessor onto propositions written for the broad one.

Six `RateLimitError`s in the end-to-end run, all benign: zero nodes had no papers
shown and zero were left unobserved, because each node issues several queries. They
were recorded as errors rather than silently becoming `no_evidence`.

**Not claimed:** that narrow is better. Five instances, development set, uncalibrated
mappings; 5/5 against 4/5 is one row. The supported claim is that narrow **does not
degrade** ranking.

### A wiring bug that cost a full run

`assess_prompt` was threaded through by a string replacement that matched the first
`event_log=ctx.event_log)` in the file — which belonged to `generate_queries`, not
`assess_proposition`. All five instances built their graphs and ran retrieval before
dying at query generation. A static test now pins the wiring (signature present on
one function, absent on the other, exactly one call site, inside the right call), so
it fails in seconds rather than after five instances of retrieval.

## 31. Held-out comparison: frozen, row-paired, order-randomised, pre-registered

**Design fixed before any test row was run.** See
`benchmark/holdout/PREREGISTRATION.md`.

* **Systems frozen** with the sha of every prompt the method uses
  (`benchmark/frozen/narrow_graph_v1.json`, `broad_assessor_v1.json`). Re-freezing
  under an existing name is refused.
* **Held-out is row-level**: no pair from that source row has been run end-to-end and
  nothing from it fed the assessor work. Pairs from one row share a gold hypothesis
  and a literature neighbourhood, so pair-level splitting would leak. 92 clean pairs
  across 52 untouched rows → one pair per row → **20 calibration / 20 test**, with
  **12 rows held in reserve**. The split file refuses to be rewritten.
* **Row-paired and order-randomised.** The first attempt ran all 20 rows on one arm
  then all 20 on the other, and was **abandoned four minutes in** (kept as
  `runs/ABANDONED_arm_sequential_*` with a note). Semantic Scholar throughput drifted
  from 5 to 20 minutes per instance inside a single job earlier today; an
  arm-sequential design would let that drift load onto the arm comparison. Now both
  arms run adjacent in time per row, with the order drawn per row from a recorded
  seed.
* **Primary hypothesis, pre-registered:** constraining the evidence channel
  materially reduces unsupported bridging and informative-node yield *without
  materially degrading pair ranking*. Preservation under restriction — explicitly not
  "narrow outperforms broad". At n=20, 18/20 against 16/20 is two rows.
* Everything reported **paired at the row level**, with per-row outcomes shown
  alongside any aggregate.

### Calibration is deliberately not attempted

The defensible chain is `ordinal output -> calibrated probability of the
ASSESSOR-LEVEL event -> ranking -> pair ranking`, which needs an assessor-local
target such as `k -> P(proposition genuinely supported | k)`, fitted with isotonic or
ordinal regression and frozen before the test rankings are seen.

**No such target exists here.** There is no human-verified support or direction
annotation, and the two-judge reproducibility work measured agreement between
automated judges, which is not ground truth. Fitting the mappings against pair
accuracy instead would tune the system toward a benchmark where candidate text alone
recovers 0.910 of labels — a held-out split prevents leakage, not meaninglessness.

So the ordinal mappings stay **pre-specified and uncalibrated**, identical in both
arms, and any task-level tuning is reported as an ablation and never called
calibration.

The canonical slice (style signal 0.643, the lowest available) is a **sensitivity
analysis** — does the broad-vs-narrow conclusion persist where the shortcut is
weaker — not a substitute calibration set, and not a retrospective repair. It failed
its own gate and carries its own uncertainty.

## 32. Held-out result: both arms near chance, and the failure clusters by row

20 held-out rows, both frozen arms, row-paired and order-randomised. All 40 runs
`status=ok`, 0 retrieval errors, 0 unobserved nodes, and the assessor actually used
by every evidence call was verified from the LLM event logs (not the manifest).

| | broad | narrow |
| --- | --- | --- |
| pair accuracy (ties 0.5) | 0.525 | 0.600 |
| **coverage** | 0.65 (13/20) | 0.60 (12/20) |
| **selective accuracy** | **0.538** | **0.667** |
| informative-node yield | 22% | 14% |
| paired: narrow better / broad better / tied | — | 3 / 1 / 16 (exact McNemar p = 0.63) |

The debug instances had shown 4/5 and 5/5. The held-out set shows that was flattering.

**Confound checks passed:** rate-limit events balanced (106 vs 108), 11/20 rows
broad-first, accuracy by run position 0.575 vs 0.550.

**Pre-registration gap, recorded rather than papered over:** the hypothesis said
"without materially degrading pair ranking" with **no numeric margin**, so no formal
non-inferiority test is possible. Choosing a margin now would be DECISIONS #16 again.
The descriptive reading is "no detectable difference at n=20".

### Zero-yield rows

6 of 20 rows get zero informative nodes in both arms, so the posterior never moves
and the pair is a forced tie. Retrieval did not fail: ~200 eligible papers, 40
queries, near-zero empty searches.

Ruled out as separators between zero-yield and productive rows: retrieval volume,
abstract coverage (one zero-yield row at 86%), cutoff date, proposition length,
conjunctiveness (zero-yield rows are *more* atomic, 0.07 vs 0.25 clause markers),
best-paper term overlap (0.415 vs 0.444), unmatched proposition terms (45% vs 43%),
and discipline.

What the data shows instead is **row-level clustering**. Pooled per-node informative
rate is 0.221; per-row counts are `0 0 0 0 0 0 0 1 1 2 4 4 5 5 8 10 10 12 13 13`.
Observed variance 23.52 against 3.44 expected under within-row independence —
**over-dispersed 6.8x**. Independence predicts 0.14 rows at zero; 7 were observed.
So a row either has literature the assessor accepts or essentially none.

Reading the cases gives the mechanism: propositions inherit the **novelty of the
hypothesis**. `0052` retrieves work on `Ni2P-Cd0.9Zn0.1S/g-C3N4` — the same material
family, named in the title — against a proposition about carbon-coated Cd0.9Zn0.1S
with a 20-50 nm layer. The assessor declines it correctly: prior literature cannot
contain a composite that did not exist yet. Relating the neighbour requires exactly
the inferential step the narrow assessor refuses, and the graph can only carry it if
a node exists at that level — which generation never produced. **This is a
generation problem, and DECISIONS #34 is the response.**

## 33. The narrow assessor is the method; the broad assessor is an ablation

**Frozen as an architectural decision.** `evidence.assess_prompt` now defaults to
`evidence_assess_v2`. The test that pinned v1 as the default was changed
deliberately, with the reason in its docstring.

The justification is stronger than reproducibility (#28-29):

| origin of node | broad informative | narrow informative |
| --- | --- | --- |
| gold hypothesis | 34/195 (17%) | 30/195 (15%) |
| negative hypothesis | **54/203 (27%)** | 25/205 (12%) |

**The broad assessor made fabricated negatives easier to evidence than the true
gold, and the narrow assessor removes that.** The mechanism is the one the change
was made for: a generic wrong claim is easy to bridge to from neighbouring
literature, a specific novel finding is not. Requiring direct statement removes the
shortcut. Log-evidence agrees: gold-minus-negative is +0.063 under broad, +0.116
under narrow.

An earlier report of this asymmetry as 38% vs 25% was the broad arm restricted to
productive rows; the table above is all 20 rows, both arms.

This also softens the concern that ResearchBench is intrinsically stacked against
novel gold hypotheses. The effect is real but substantially **mediated by the
assessor's bridging** rather than intrinsic to the benchmark, so ResearchBench is
not abandoned on that basis. n=20; needs confirming on the reserve.

### Standard metrics from now on

Every run reports three accuracy quantities, not one:

* **coverage** - share of rows where the posterior moved (`score_spread > 0`);
* **selective accuracy** - pair accuracy on those rows only;
* **overall accuracy** - ties and abstentions counted as 0.5.

They satisfy `overall = coverage x selective + (1-coverage) x 0.5`; a test pins the
identity. Coverage keys on *discriminative* evidence, not merely informative: a node
every candidate predicts equally is informative and still inert.

This is what exposed the held-out result. Broad had HIGHER coverage and was at
chance when it spoke; the aggregate hid that completely.

### Standing diagnostic: contradiction rate by node origin

`yield_by_origin` is now written per instance, giving informative rate and
contradiction rate split by the hypothesis a node was generated from. The
near-absence of contradictions is a persistent pattern (0 gold-origin in both arms;
4 and 1 negative-origin), so all discrimination currently comes from differential
positive support. Nothing was changed to force more contradictions - it is tracked,
and may simply be a property of the literature task.

## 34. consequence_generate_v3: abstraction-aware generation (unvalidated)

Targets exactly one discovered failure. Narrow assessor, edges, retrieval and
inference are unchanged, so the run is a clean causal experiment on generation.

v3 generates atomic consequences at three levels: SPECIFIC (the claim own entities),
MECHANISTIC (the process with incidental novelty removed) and CLASS (the family the
entity belongs to). Each proposition records its abstraction_level.

The boundary that keeps it legitimate: a proposition may abstract away a novel
specific ONLY when the claim still probabilistically implies the more general
proposition, stated in why_implied. It must never be written because it is easier
to search. Otherwise v3 just moves the unsupported bridge out of the assessor and
into generation, where the edge assessor would treat it as sound.

Default stays consequence_generate_v2 until structural validation passes.

## 35. v3 is the method: structural validation on 20 development rows

Frozen as `benchmark/frozen/narrow_graph_v3.json`. The decision used structural
evidence only -- ranking was excluded by design, because the prompt was written
after inspecting these rows' failures.

| level | nodes | informative | median disc | evidenced-but-inert |
| --- | --- | --- | --- | --- |
| specific | 142 | 17 (12%) | 0.132 | 1 |
| mechanistic | 139 | 54 (39%) | 0.123 | 2 |
| class | 119 | 54 (45%) | 0.123 | 2 |

* **zero-yield rows 8 -> 0**, none newly zero; coverage 0.60 -> 1.00.
* `why_implied` missing on **0 of 258** abstracted nodes.
* level split 142/139/119 with **0 of 20 rows perfectly even** -- not quota-following.
* discriminativeness flat across levels, 5 of 258 abstracted nodes evidenced-but-inert,
  so abstraction did not buy yield by going vacuous.
* edge direction reproducibility flat by level (0.889/0.839/0.875); mismatched control
  90/90 neutral.

Specific propositions stay at 12% -- the original failure is unchanged for them, as it
should be. The gain is entirely in the abstracted levels.

Gold-vs-negative yield widened in the gold's favour (15%/12% -> 39%/24%). Kept as a
diagnostic, not a gate: the same quantity proved assessor-dependent once already.

## 36. Ordinal edge strength: ranking IS materially sensitive. Reserve stays sealed.

Perturbation analysis on saved artifacts (no LLM): graph, evidence and mappings held
fixed, only edge ordinal labels moved. Run on both 20-row sets.

| | dev-20 | calibration-20 |
| --- | --- | --- |
| gold first | 16/20 | 12/20 |
| adjacent-nudge flip rate | 17.1% | 26.1% |
| flip rate at observed judge-disagreement rates | 14.0% | 16.5% |
| direction-only collapse changes rank | 2/20 | 4/20 |
| median margin | 0.062 | 0.147 |
| rows with margin < 0.07 | 11/20 | 6/20 |

**Answer to the decision question: yes.** Pooled adjacent-nudge flip rate is ~22%, and
direction-only collapse changes 6 of 40 rows. Dev-20 alone suggested the extra ordinal
resolution was harmless noise (2/20); calibration-20 doubled that. So the edge-strength
representation has to be resolved before the reserve is spent.

**The margin relationship replicates**: below 0.07, flip rates are 23.6% / 26.7%; above,
2.2% / 12.1%.

**But it does not fully explain the sensitivity.** Calibration-20 has a median margin
more than twice dev-20's (0.147 vs 0.062) and yet flips MORE often, including 12.1% among
its well-separated rows. Compressing the scale is premised on fragility living in
near-ties; that premise is only partly true, so the remedy is not yet established.
Unexplained -- diagnose before choosing.

**Ranking fell 16/20 -> 12/20** on rows whose failures were never inspected, which is the
predicted direction and the reason 16/20 was never treated as a result.

## 37. Dependency-aware inference: implemented, tested, and a NEGATIVE result

`inference.aggregation: family` treats each root consequence family (a depth-1
proposition plus its chain descendants) as one dependent evidence unit, marginalising
exactly over its latent X values, then combines families under conditional
independence. Default stays `independent`.

It works and changes nothing that matters:

| | dev-20 indep | dev-20 family | cal-20 indep | cal-20 family |
| --- | --- | --- | --- | --- |
| gold first | 16/20 | 16/20 | 12/20 | 11/20 |
| mean flip rate | 14.0% | 14.0% | 16.5% | 18.6% |
| ranking agreement | 20/20 | | 19/20 | |

The node-count effect is untouched (cal-20: 10.8% -> 27.1% independent, 11.2% ->
32.5% family).

**Not inert:** 69-73% of informative nodes sit in families with >=2 informative
nodes. The correction is small because a family member usually has a root edge from
cross-evaluation as well as its chain edge, and the two are combined by noisy-OR --
the root edge is identical under both aggregations and dominates.

A modelling bug was caught by its own unit test: the first implementation dropped the
root edge inside the family, discarding exactly what cross-evaluation produces.
Fixed to condition on both parents with the same combination rule.

Kept as an ablation. It is a *stronger* negative result than it first appeared: it
failed because there was no dependence to remove.

## 38. The instability is accumulated independent judgment noise, not dependence

Repeated assessment on the 20 development rows: the frozen narrow assessor re-run on
saved node/paper bundles varying **only record presentation order** -- a nuisance
factor that must not change a scientific answer. 400 nodes x 3 repeats, 1200 calls,
4 parse failures (0.3%), nodes kept with >=2 usable repeats so the least-decisive
ones were not silently dropped.

| | value |
| --- | --- |
| node instability P(labels differ) | **0.165** |
| within-row pair covariance | +0.0008 |
| cross-row pair covariance (null) | -0.0001 |
| excess / per-node variance | 0.0009 / 0.0305 = **0.031** |

**No within-row co-movement.** The assessor-correlation hypothesis -- which I
proposed, and had earlier stated too confidently as the 'likeliest remaining source'
-- is rejected.

All three dependence mechanisms are now ruled out: proposition structure (#37),
shared literature (12-19% overlap), correlated assessment (ratio 0.031).

**What actually explains it:** per-node judgments are individually noisy and
INDEPENDENT. Independent noise accumulates as sqrt(n) across contributing nodes while
the margin does not grow proportionally, so more informative nodes means worse
signal-to-noise. That reproduces the node-count->fragility signature without any
double-counting, and explains why family aggregation could not help.

Instability is concentrated in the weak labels: `no_evidence` stays put 96% of the
time, `strong_support` 81%, `support` 68%, **`weak_support` 51%**.

### Uncertainty decomposition (dev-20, 60 draws per row)

| channel | mean P(gold first) | rows in 0.2-0.8 |
| --- | --- | --- |
| edge | 0.705 | 6/20 |
| evidence | 0.777 | 3/20 |
| both | 0.708 | **8/20** |

Both channels matter and compound. Edge uncertainty is the larger single contributor,
which the 16.5% evidence instability alone would not have predicted.

## 39. Method and uncertainty protocol frozen; reserve opened once

Frozen before any reserve row was run:

* **method** -- `benchmark/frozen/narrow_graph_v3_complete.json`: v3 generation,
  narrow evidence assessor, validated edge judgments, `independent` inference,
  merging off, uncalibrated placeholder ordinal mappings.
* **noise model** -- `benchmark/frozen/noise_model_v1.json`, from the 20 development
  rows only. Nothing estimated from the reserve.
* **protocol** -- `docs/UNCERTAINTY_PROTOCOL.md`.

The deterministic ranking stays the primary output; perturbation stability is reported
alongside it. The quantity is **ranking stability under model-judgment variation**,
never a posterior over scientific truth -- the ordinal mappings are uncalibrated, so
nothing here carries probabilistic meaning about the science.

No abstention threshold: the continuous stability value is reported unthresholded.
'No evidence' and 'evidence exists but the ranking is unstable' are kept apart as
distinct failure modes.

The ordinal scale was deliberately NOT compressed. It would have made rankings look
steadier without making them better founded -- tuning stability instead of measuring
it.

**The 12 reserve rows are used exactly once.** No second attempt, no re-freezing
afterwards, whatever the result.
