# Held-out comparison — pre-registered before any test row was run

Written and frozen **before** the paired run started. The split
(`benchmark/holdout/split.json`) and both systems (`benchmark/frozen/*.json`) were
already frozen; this records what the result will be taken to mean.

## Primary hypothesis

> **Constraining the evidence channel materially reduces unsupported inferential
> bridging and informative-node yield, without materially degrading pair ranking.**

The claim of interest is **preservation under restriction**. It is explicitly *not*
"narrow outperforms broad".

With n=20 test rows, a difference of 18/20 against 16/20 is two rows and is weak
evidence of superiority in either direction. A result where narrow ranks roughly as
well as broad while provably removing a class of unrecorded inference is the
interesting outcome, and it is the one the design is powered to see.

## What will be reported

Everything **paired at the row level** — each test row is evaluated by both arms, so
the unit of analysis is the row, not the arm. Individual per-row outcomes will be
shown alongside any aggregate; a percentage over 20 rows will not be reported on its
own.

| quantity | reported as |
| --- | --- |
| pair ranking (gold first) | per row, plus the paired win/loss/tie count |
| gold rank | per row, both arms side by side |
| informative-node yield | per row, and pooled over nodes |
| posterior separation (top1 − top2) | per row, plus paired differences |
| entropy ratio | per row |
| unsupported inferential bridging | structural: possible under broad, removed under narrow |
| retrieval conditions | queries, papers returned, rate-limit events, timestamps per run |

## Design decisions that cannot be revisited afterwards

* **Row-paired, order-randomised.** Both arms run adjacent in time on each row, and
  which arm goes first is drawn per row from seed 20260912. Retrieval throughput on
  Semantic Scholar drifted from 5 to 20 minutes per instance within a single job
  today, so an arm-sequential design would let that drift load onto the arm
  comparison. Randomising the order balances any residual position effect.
* **No ordinal-mapping calibration in this experiment.** The mappings are the
  pre-specified placeholders, identical in both arms. See below.
* **Test rows are reported; calibration rows are not.** The 20 calibration rows are
  reserved and were not run for this comparison.
* **12 clean rows are held in reserve**, untouched by either split, for confirming
  anything the 20 test rows raise.

## What this benchmark cannot establish

v2 is a **development** set: a question-hidden judge recovers **0.910** of pair
labels from candidate text alone. Holding rows out removes the tuned-on-these-cases
problem; it does not remove the style artifact.

So **absolute pair accuracy on the test split is not evidence of verification
ability.** Arm-to-arm differences and method-scaling quantities are what the split
supports. Any write-up must say so in the same breath as the number.

## Calibration is deliberately NOT part of this

Fitting the ordinal mappings to maximise pair accuracy on a slice with a 0.910 style
artifact would tune the system toward exploiting that artifact, and a held-out test
set would not prevent it — it prevents leakage, not meaninglessness.

The defensible chain is:

    ordinal assessor output
      -> calibrated probability of the ASSESSOR-LEVEL event
        -> ranking system
          -> final pair ranking

which requires an **assessor-local** target, of the form `k -> P(proposition
genuinely supported | k)` or `k -> P(edge direction correct | k)`, fitted with
isotonic or ordinal regression and frozen before the test rankings are looked at.

**No such target exists in this project.** There is no human-verified support or
direction annotation; the two-judge reproducibility work measured agreement between
automated judges, which is not ground truth. Therefore the ordinal mappings stay
pre-specified and uncalibrated for the main experiment, and any task-level tuning is
reported as a separate ablation, never as calibration.

## Canonical slice: a sensitivity analysis, not a repair

The frozen systems will also be run on the low-style canonical slice, answering one
narrow question:

> Does the broad-versus-narrow conclusion persist where the candidate-text shortcut
> is much weaker?

The canonical slice failed its own style gate, so it carries its own uncertainty and
is not a substitute benchmark. It will not be used to rescue the main result
retrospectively.
