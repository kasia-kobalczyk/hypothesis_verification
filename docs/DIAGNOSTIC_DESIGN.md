# Diagnostic prediction tests — frozen design

**Status: FROZEN before implementation.** A new experimental branch, not v4 of the
consequence-graph method. That method, its artifacts and its results are preserved
unchanged; this reuses only infrastructure (benchmark loading, temporally safe
retrieval, caching, logging, reporting).

## Why a different formulation

The consequence-graph verifier reached complete evidence coverage (1.00 on the
reserve) and chance ranking (0.500 selective). Forensics on the nine stable reserve
rows found the failures were not noise-driven and not one thing:

| row | cause |
| --- | --- |
| `0159-N04` | pre-cutoff literature genuinely favoured the negative |
| `0063-N05` | weak bridge: an off-topic paper accepted as support |
| `0193-N06` | contradiction scored on a non-matching construct (purchases, not authenticity) |
| `0226-N06` | gold outnumbered by a fabricated hypothesis assembled from true generalities |

Two failure modes recur and both are structural to *accumulating support*:

1. **Relevance without measurement match.** A verbatim span about an adjacent
   construct passes grounding. Grounding proved necessary and not sufficient.
2. **Generic truths as evidence.** Abstraction (v3) fixed coverage precisely by
   licensing class-level propositions -- and a plausible-but-false hypothesis
   decomposes into established generalities, each of which finds literature.

Both follow from asking *what evidence is compatible with H?*. This branch asks a
different question.

## Core principle

> What observable test would distinguish the competing hypotheses, and has that
> observation already been made in the pre-cutoff literature?

**No test belongs to a hypothesis.** Tests are generated jointly for
`H_1..H_k`, and every hypothesis predicts the outcome of the *same* test before any
literature is seen. An observation contributes only because candidates predicted it
differently -- which structurally removes the candidate-origin asymmetry that the
previous branch had to measure and correct for.

## The unit: a diagnostic test

```
test_id
system                    what is being studied
context                   conditions under which
intervention_or_exposure  what is varied or applied
measured_outcome          the quantity actually measured
rationale                 why this discriminates
predictions_by_hypothesis one coarse direction per candidate
```

`measured_outcome` is the load-bearing field. Study matching turns on it, because
the `0193-N06` failure was precisely a correct-sounding span measuring the wrong
thing.

## Prediction vocabulary -- coarse, deliberately

    positive_or_present
    neutral_or_no_change
    negative_or_absent
    indeterminate

No ordinal strength. The previous branch measured `weak_support` reproducing at
0.51 -- a coin flip -- and exact ordinal edge agreement falling to 0.370 at class
level. Fine gradations were not reproducible there, so they are not assumed here.
Finer scales are introduced only if coarse directions prove insufficient AND
reproducible.

## Compatibility vocabulary (Phase 5)

    match | approximate_match | indeterminate | mismatch

Compared against each hypothesis's precommitted prediction. There is no generic
'support for H' judgment anywhere in this design.

## Component validation criteria

Each phase is validated before the next is trusted. Thresholds are development
targets for judging whether a component works, not acceptance gates on a held-out
set.

| phase | component | validated by |
| --- | --- | --- |
| 1 | test generation | share empirically observable; share discriminative; rejection reasons |
| 2 | prediction | coarse direction agreement between independent assessors; confusion matrix |
| 3 | retrieval | queries contain no direction/outcome/hypothesis wording (mechanical check) |
| 4 | study matching | adversarial cases: wrong measurement, wrong system, wrong intervention, unrelated paper, null effect, opposite direction |
| 5 | comparison | applied only to accepted observations; frozen label set |
| 6 | aggregation | observation_coverage, diagnostic_resolution; 'not distinguishable' permitted |

## Failure attribution

Every instance failure must be attributable to exactly one of:

    test_generation | prediction | retrieval | study_matching |
    observation_extraction | aggregation

Artifacts are written per stage so attribution is mechanical rather than
reconstructed afterwards. Every generated test, query, matched study, grounding
span, prediction, observation and scoring decision is logged.

## Not forcing a winner

`not distinguishable from available literature` is a first-class output. Reporting
it is a correct answer when the literature does not separate the candidates, and
the previous branch showed why it matters: coverage 1.00 with selective accuracy
0.500 means a system that always answers is not thereby informative. Two new
metrics:

    observation_coverage   tests with a matched observation / tests generated
    diagnostic_resolution  tests that discriminate AFTER observation / tests with
                           a matched observation

## Deliberately deferred

* transportability across systems beyond the coarse system-match check;
* calibrated Bayes factors;
* fine-grained ordinal scales;
* any prompt change motivated by ranking accuracy.

## Constraints carried from the previous branch

* The temporal cutoff is enforced by the retrieval backend, never by prompting.
* Missing literature is not contradictory evidence.
* API failure is never `no observation`.
* Queries are outcome-neutral -- now mechanically checked, not merely instructed.
* Development data only. The spent reserve is not reused as evaluation, and no new
  held-out set is declared from previously used rows.

## What would make this branch worth keeping

Not higher pair accuracy. The signals that would matter:

* studies accepted only when they measured the requested outcome (Phase 4
  adversarial cases);
* generic background truths no longer accepted as evidence;
* no candidate-origin asymmetry, by construction;
* an honest `not distinguishable` rate rather than a forced winner.

---

## AMENDMENT 1 (2026-09-13) — neutral vs indeterminate, and an explicit comparator

**The frozen design did not pass Phase 2 and was amended. It did not pass.**
Original freeze `49695b5b3440818c`; this document now supersedes it and any component
validation run against the original hash is void.

### What failed

Phase 2 exact direction agreement was **0.467** over 120 (test, hypothesis) pairs.
The failure was concentrated in one cell: **26 of 31 `neutral_or_no_change`
predictions became `indeterminate`** under the independent judge, whose neutral
column was empty across the entire matrix. Excluding that cell, agreement on the
three definite directions was 54/60 = 0.90. The unrelated-test control was clean:
37/37 'claim does not determine', 0/37 'bears on quantity'.

### Diagnosis

A vocabulary collapse, not a scientific disagreement. The two labels mean different
things:

    neutral_or_no_change   H_i => Y is at baseline. A substantive prediction of nullity.
    indeterminate          H_i does not license any directional or null prediction for Y.

A test where `H1: up` and `H2: no change` is genuinely diagnostic. A test where
`H1: up` and `H2: indeterminate` is not, because H2 made no falsifiable prediction.
Collapsing them would discard exactly the structure this branch exists to exploit.

Judge B's step 3 asked only whether the claim *bears on* the quantity, and a claim
predicting nullity answers that the same way a silent claim does. The defect was in
the decision procedure, not the vocabulary.

### The amendment

1. **Vocabulary unchanged.** Still the four coarse labels.
2. **Judge B's procedure is explicit**: bears on the quantity? if no -> indeterminate;
   if yes -> increase / decrease / approximately unchanged relative to the stated
   comparator. Prompt states that `neutral_or_no_change` is a substantive prediction
   and must not be used because the hypothesis is silent, with contrastive examples,
   since the distinction is semantic rather than wording.
3. **New required test field: `baseline_or_comparator`.** `T = (S, C, I, Y, B)`.
   'Higher expression' is meaningless without saying higher than what, and an
   implicit comparator is a plausible source of sign disagreements.

### Validation required before Phase 3

Rerun on the **same fixed 60 tests** -- no regeneration. Passing means: exact
four-way agreement rising toward 0.8-0.9; the neutral/indeterminate confusion
substantially reduced; agreement on definite directions holding near 0.90; controls
still 100% indeterminate. The 11 positive->negative conflicts are reviewed
separately as genuine prediction disagreements.
