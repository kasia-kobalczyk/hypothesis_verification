# v2 screening report — length-controlled ResearchBench pair slice

> **DIAGNOSTIC ARTIFACT — NOT THE OFFICIAL v2.** This slice uses the widened band
> [0.67, 1.50]. The official v2 was re-frozen at [0.75, 1.33] and lives in
> `benchmark/v2/`. This directory is kept so the effect of the band on the length
> and question-hidden diagnostics stays inspectable. Do not load it as the dataset.

Frozen 2026-09-11T20:03:11Z. 102 pairs across 47 source rows.

## Why v2 exists

v1 artifact diagnostics: ranking candidates by shortest text alone scored 1.000 on the frozen v1 pair subset. Across the full ranking set the median negative is 3x the gold's length. v2 controls that confound by construction.

## What was inherited from v1, and what is new

- inherited: the R1-R6 scientific-validity rubric text (benchmark/dev/README-3.md)
- inherited: the deterministic DOI screening order
- inherited: verbatim hypothesis text; nothing is rewritten
- **new**: length ratio `tokens(negative)/tokens(gold) in [0.67, 1.5]` — per gold-negative pair; all passing pairs retained

The band was first specified as [0.75, 1.33] and widened one notch to [0.67, 1.5] by the research owner, on the interpretive ground "neither text more than 1.5x the other", after seeing the base-rate statistics and **before** any pair was screened or any diagnostic run.

Not used anywhere in selection: literature retrieval, Direct-RAG output, consequence-graph output, any verifier score, any artifact-diagnostic result.

> **Provenance caveat.** v1's R1-R6 rubric TEXT is frozen and quoted verbatim in row_screen_v1, but v1's screening PROMPT was not preserved in this repository. R1/R3/R5/R6 are therefore re-implemented, not replayed; R2 uses the prompt frozen during the v1 pair audit.

## Tokenizer

`regex_word_punct_v1` — pattern `\w+|[^\w\s]`. tiktoken is unavailable offline; this tokenizer needs no download

## The length artifact in the full dataset

| statistic | value |
| --- | --- |
| gold-negative pairs in the 962 deduped rows | 9620 |
| median ratio tokens(negative)/tokens(gold) | **3.0** |
| negative shorter than the band | 0.9% |
| inside the band | 9.5% |
| negative longer than the band | 89.6% |

The median ResearchBench negative is three times the length of the gold it competes with.

## Selection funnel

Rows are walked in v1's deterministic screening order and gates applied cheapest first. The gates are conjunctive, so the order does not change which pairs survive.

| gate | rows rejected |
| --- | --- |
| no negative inside the length band | 105 |
| R1/R3/R5/R6 row screen | 20 |
| R4 temporal cutoff not establishable | 0 |
| R2 no comparable pair among length-passing negatives | 35 |
| **rows contributing at least one pair** | **47** |

207 rows were walked; 102 were screened with a model. Target of 100 pairs reached.

## The slice

| property | value |
| --- | --- |
| pairs | 102 |
| distinct source rows | 47 |
| pairs per row (min/median/max) | 1/2/7 |
| length ratio (min/median/max) | 0.71/1.22/1.50 |
| most common discipline | Energy Science (38% of pairs) |

Disciplines: Energy Science 39, Cell Biology 14, Physics 12, Law 8, Environmental Science 7, Material Science 6, Biology 4, Astronomy 3, Business 3, Math 3, Chemistry 2, Earth Science 1.

## Artifact diagnostics

Characterisation only. These results did not influence selection and the length band was not adjusted on them.

| diagnostic | v1 | v2 |
| --- | --- | --- |
| pairs | 121 | 102 |
| median length ratio | 3.452 | 1.218 |
| max length ratio | 40.642 | 1.500 |
| gold is the shorter text | 0.984 | 0.794 |
| **shortest-text-first** | **0.988** | **0.809** |
| longest-text-first | 0.012 | 0.191 |
| **question-hidden judge** | **0.785** | **0.853** |

### Reading these

1. **The length artifact is reduced, not removed.** Shortest-text-first falls from 0.988 on v1 to 0.809 on v2, but stays well above chance: inside the band the gold is still the shorter text in 0.794 of pairs (median ratio 1.218).

   Sensitivity of the residual signal to the band, computed on the frozen slice (reported so the band can be reconsidered deliberately — it was **not** used to choose the band):

   | band | pairs | shortest-text-first |
   | --- | --- | --- |
   | as frozen [0.67, 1.5] | 102 | 0.809 |
   | original proposal [0.75, 1.33] | 71 | 0.754 |
   | [0.90, 1.11] | 23 | 0.674 |

2. **A second artifact is now visible, and it is larger.** The question-hidden judge *rises* from 0.785 on v1 to 0.853 on v2. With length controlled, a model still recovers the gold in most pairs from the two texts alone — no question, no literature. Length was not the only surface cue; genre is a candidate (a reported finding reads differently from a proposal), and v2's discipline concentration may also contribute.

3. **Concentration.** 38% of v2 pairs come from one discipline and 47 rows supply 102 pairs, so pairs are not independent. Report per-row as well as per-pair numbers.

## Files

- `researchbench_v2_pairs.jsonl` — the frozen slice, one record per retained pair
- `v2_manifest.json` — rules, prompts with hashes, funnel counts, provenance
- `v2_artifact_diagnostics.json` — the three diagnostics, per-pair rows included
- `v2_row_outcomes.jsonl` — every row walked and the gate it was rejected at
- `v2_progress.jsonl` — raw screening decisions, for resuming and auditing
