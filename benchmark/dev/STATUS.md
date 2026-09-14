# v1 dev20 — DEVELOPMENT / DEBUGGING SET

This slice (`researchbench_dev20_v1.jsonl`, and the `pairs_v1.jsonl` subset
derived from it) is for **building and debugging the method**. It is not an
evaluation benchmark, and aggregate accuracy on it is not evidence for the
method.

## Why

Measured on the frozen v1 pair subset (121 pairs), with no model, no question
and no literature:

| baseline | pair accuracy |
| --- | --- |
| rank by **shortest text first** | **0.988** |
| `question_hidden_judge` (two texts, no question) | 0.785 |
| `direct_judge` (closed book, gpt-4.1) | 0.264 |

The gold hypothesis is the shorter candidate in 98% of pairs, because
ResearchBench golds are short prose summaries and the negatives are
multi-paragraph LLM proposals. Any ranking number on this slice is dominated by
that.

## What it is still good for

Everything that does not depend on aggregate accuracy:

- is the generated consequence graph scientifically sensible?
- is the retrieved literature actually relevant to the proposition?
- does Bayesian propagation behave as specified (no_evidence inert,
  non-discriminative nodes inert, attenuation through weak edges)?
- do the temporal, caching and cost mechanisms work end to end?

## See also

- `benchmark/v2/` — length-controlled pair slice. Also a development set: the
  length artifact is reduced but a question-hidden judge still recovers most
  labels.
- `benchmark/canonical/` — the style-controlled evaluation benchmark, built by
  symmetric candidate canonicalisation with its protocol frozen in advance.
- `docs/DECISIONS.md` — why each of these exists.
