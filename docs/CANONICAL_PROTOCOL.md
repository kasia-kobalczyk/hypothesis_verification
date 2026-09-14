# Canonicalized evaluation benchmark — construction protocol

**Status: FROZEN 2026-09-11, before the consequence verifier was run on it.**

This document is the specification. It was written and committed before any pair
existed, and the builder implements it. If the protocol has to change, the change
is recorded here with its reason and the benchmark is rebuilt from scratch — the
protocol is not edited to match what the data turned out to look like.

## Why this benchmark exists

v1 and v2 are development sets. On both, a ranker that never reads any science
performs well:

| slice | shortest-text-first | question-hidden judge |
| --- | --- | --- |
| v1 (121 pairs) | 0.988 | 0.785 |
| v2 (100 pairs, length-matched) | 0.760 | 0.870 |

v2 showed that filtering raw pairs until the length cue disappears does not work:
controlling length left the question-hidden judge *higher*, because the surviving
cue is genre, not length. A ResearchBench gold reads as a reported finding; a
ResearchBench negative reads as a multi-paragraph proposed study. No amount of
discarding raw pairs removes that, because it is a property of how the two kinds
of text were written.

So this benchmark does not filter. It **transforms**: every candidate, gold and
negative alike, is rewritten by one fixed procedure into a short declarative
scientific claim. What survives the transformation is the scientific content;
what is destroyed is the register the two kinds of text were written in.

This produces a **derived benchmark**. It does not claim to be untouched
ResearchBench, and it must not be described as such.

## The transformation

For each candidate, the canonicaliser receives exactly:

- the ResearchBench research question;
- the text of **one** candidate.

It never receives: whether the candidate is the gold, the other candidates, any
literature, any verifier output, or the source paper. The same prompt, the same
model and the same decoding parameters are applied to every candidate. This is
what "symmetric" means here and it is the property the whole benchmark rests on.

It returns one short declarative scientific claim: a single sentence stating what
is asserted about the world — direction, mechanism, or relationship — with the
methodology, the hedging, the numbered sub-proposals, the instruments, the
citations and the framing removed.

    gold      "The paper hypothesizes and concludes that GRB 221009A ... does not
               exhibit evidence of significant r-process nucleosynthesis ..."
    canonical "GRB 221009A did not produce significant r-process element yields."

    negative  "We hypothesize that the highly energetic GRB 221009A ... produced a
               significant amount of r-process elements through a dual mechanism:
               a collimated, jet-driven outflow ... [1,900 more words]"
    canonical "GRB 221009A produced significant r-process elements via a
               jet-driven outflow and a neutrino-driven wind."

## Gates, in order

1. **Scientific validity (inherited, unchanged).** The row must pass the frozen
   R1/R3/R5/R6 rubric and R4 (a temporal cutoff must be establishable). Decisions
   already made during the v2 build are reused verbatim; nothing is re-judged
   more leniently.
2. **Canonicalisation.** Applied to the gold and to every negative, blind, as
   above.
3. **Semantic preservation.** A separate judge sees (original, canonical) — and
   is not told which candidate role it came from — and decides whether the
   canonical form preserves the original's central claim: its subject, its
   direction, and its mechanism where one was asserted. A candidate whose
   canonical form fails is dropped, and any pair involving it is dropped with it.
   A judge failure is recorded as an error, never as a pass and never as a fail.
4. **Pair comparability (re-applied).** The frozen R2 criterion is applied to the
   **canonicalised** pair, not to the originals: canonicalisation can turn a pair
   that disagreed into two claims that no longer contradict, and the benchmark
   must reflect the texts a verifier will actually see.

There is **no length gate**. Length is measured and reported as a diagnostic. If
canonicalisation leaves a length cue, that is a finding about the transformation,
to be fixed in the transformation or declared — not filtered away.

## Sampling

The same deterministic order as v1 and v2: DOI-deduplicated rows sorted by
SHA256(DOI) ascending. Rows are consumed in that order until the target of 100
retained pairs is reached, or the screened pool is exhausted. All pairs passing
every gate are retained; no negative is preferred over another.

## What is forbidden during construction

- literature retrieval, Direct-RAG output, consequence-graph output, any verifier
  score, any artifact-diagnostic result;
- knowing which candidate is the gold, at any point in the transformation or the
  preservation check;
- adjusting the transformation, the prompts or the gates in response to the
  diagnostics.

## Diagnostics, run after freezing

Shortest-text-first, longest-text-first, and the question-hidden pair judge — the
same three used on v1 and v2, so the numbers are comparable.

**The success criterion is declared in advance**: for this slice to be usable as
an evaluation benchmark, shortest-text-first and longest-text-first should both
sit near 0.5, and the question-hidden judge should fall substantially below the
0.870 it scores on v2. If the diagnostics come out badly, the honest outcome is
to report that canonicalisation did not remove the cue — not to rebuild the slice
until the numbers improve.

## Files

- `benchmark/canonical/researchbench_canonical_pairs.jsonl`
- `benchmark/canonical/canonical_manifest.json`
- `benchmark/canonical/canonical_report.md`
- `benchmark/canonical/canonical_artifact_diagnostics.json`
- `benchmark/canonical/canonical_progress.jsonl` — every decision, for audit
