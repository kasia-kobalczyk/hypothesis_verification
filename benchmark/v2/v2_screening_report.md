# v2 screening report — length-controlled ResearchBench pair slice

Frozen 2026-09-11T20:34:28Z. 100 pairs across 57 source rows.

## Why v2 exists

v1 artifact diagnostics: ranking candidates by shortest text alone scored 1.000 on the frozen v1 pair subset. Across the full ranking set the median negative is 3x the gold's length. v2 controls that confound by construction.

## What was inherited from v1, and what is new

- inherited: the R1-R6 scientific-validity rubric text (benchmark/dev/README-3.md)
- inherited: the deterministic DOI screening order
- inherited: verbatim hypothesis text; nothing is rewritten
- **new**: length ratio `tokens(negative)/tokens(gold) in [0.75, 1.33]` — per gold-negative pair; all passing pairs retained

The band was specified as [0.75, 1.33] before any pair was screened, widened once to [0.67, 1.5] by the research owner on the interpretive ground "neither text more than 1.5x the other", and then **re-frozen at the original [0.75, 1.33]**. The widened slice is kept as a diagnostic artifact only (`benchmark/v2_widened_diagnostic/`); it is not the official v2. Both bands were fixed before any diagnostic was run, and neither was chosen on the basis of a diagnostic result.

Not used anywhere in selection: literature retrieval, Direct-RAG output, consequence-graph output, any verifier score, any artifact-diagnostic result.

> **Provenance caveat.** v1's R1-R6 rubric TEXT is frozen and quoted verbatim in row_screen_v1, but v1's screening PROMPT was not preserved in this repository. R1/R3/R5/R6 are therefore re-implemented, not replayed; R2 uses the prompt frozen during the v1 pair audit.

## Tokenizer

`regex_word_punct_v1` — pattern `\w+|[^\w\s]`. tiktoken is unavailable offline; this tokenizer needs no download

## The length artifact in the full dataset

| statistic | value |
| --- | --- |
| gold-negative pairs in the 962 deduped rows | 9620 |
| median ratio tokens(negative)/tokens(gold) | **3.0** |
| negative shorter than the band | 1.1% |
| inside the band | 6.0% |
| negative longer than the band | 92.8% |

The median ResearchBench negative is three times the length of the gold it competes with.

## Selection funnel

Rows are walked in v1's deterministic screening order and gates applied cheapest first. The gates are conjunctive, so the order does not change which pairs survive.

| gate | rows rejected |
| --- | --- |
| no negative inside the length band | 203 |
| R1/R3/R5/R6 row screen | 20 |
| R4 temporal cutoff not establishable | 0 |
| R2 no comparable pair among length-passing negatives | 37 |
| **rows contributing at least one pair** | **57** |

317 rows were walked; 35 were screened with a model. Target of 100 pairs reached.

## The slice

| property | value |
| --- | --- |
| pairs | 100 |
| distinct source rows | 57 |
| pairs per row (min/median/max) | 1/1/5 |
| length ratio (min/median/max) | 0.75/1.15/1.33 |
| most common discipline | Energy Science (31% of pairs) |

Disciplines: Energy Science 31, Physics 12, Cell Biology 11, Law 10, Material Science 10, Business 6, Astronomy 5, Environmental Science 4, Math 4, Biology 3, Earth Science 3, Chemistry 1.

## Artifact diagnostics

Counterbalanced question-hidden judge: every pair scored in BOTH orders and averaged, so a pure position-guesser scores exactly 0.500. Extracted from the canonical diagnostics run, which covered v1, v2 and canonical in one pass. The length heuristics are copied from the single-order file unchanged -- they are deterministic and order-free.

| diagnostic | v1 | v2 |
| --- | --- | --- |
| pairs | 121 | 100 |
| median length ratio | 3.452 | 1.148 |
| max length ratio | 40.642 | 1.329 |
| gold is the shorter text | 0.984 | 0.740 |
| **shortest-text-first** | **0.988** | **0.760** |
| longest-text-first | 0.012 | 0.240 |
| **question-hidden judge** | **0.777** | **0.910** |

### Reading these

1. **The length artifact is reduced, not removed.** Shortest-text-first falls from 0.988 on v1 to 0.760 on v2, but stays well above chance: inside the band the gold is still the shorter text in 0.740 of pairs (median ratio 1.148).

   Sensitivity of the residual signal to the band, computed on the frozen slice (reported so the band can be reconsidered deliberately — it was **not** used to choose the band):

   | band | pairs | shortest-text-first |
   | --- | --- | --- |
   | as frozen [0.75, 1.33] | 100 | 0.760 |
   | original proposal [0.75, 1.33] | 100 | 0.760 |
   | [0.90, 1.11] | 30 | 0.633 |

2. **A second artifact is now visible, and it is larger.** The question-hidden judge *rises* from 0.777 on v1 to 0.910 on v2. With length controlled, a model still recovers the gold in most pairs from the two texts alone — no question, no literature. Length was not the only surface cue; genre is a candidate (a reported finding reads differently from a proposal), and v2's discipline concentration may also contribute.

3. **Concentration.** 31% of v2 pairs come from one discipline and 57 rows supply 100 pairs, so pairs are not independent. Report per-row as well as per-pair numbers.

## Files

- `researchbench_v2_pairs.jsonl` — the frozen slice, one record per retained pair
- `v2_manifest.json` — rules, prompts with hashes, funnel counts, provenance
- `v2_artifact_diagnostics_counterbalanced.json` — the three diagnostics with every pair judged in BOTH orders (authoritative)
- `v2_artifact_diagnostics.json` — the earlier single-order run, kept for provenance; its question-hidden number is confounded by position preference
- `v2_row_outcomes.jsonl` — every row walked and the gate it was rejected at
- `v2_progress.jsonl` — raw screening decisions, for resuming and auditing
