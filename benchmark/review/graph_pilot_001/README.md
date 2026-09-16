# Graph pilot review packet (GP1)

Human-review packet for the frozen eight-case explanatory-benchmark pilot
(`pilot_explanatory_001`, BENCH-GRAPH-PILOT-001), built under BENCH-GRAPH-REVIEW-001.

Everything here is derived deterministically, **with no LLM calls**, from the
preserved archive of the run. The build verifies every archived file's checksum
first. Regenerate with:

```bash
python scripts/build_review_packet.py
```

The archive is **private** and not in this repository (it holds full model traffic and
about 3,800 third-party abstracts); see
`benchmark/frozen_runs/pilot_explanatory_001/PROVENANCE.md` for its checksum and where
it is stored. Without it, the builder refuses to run and the frozen-run tests in
`tests/test_review_packet.py` skip. The packet files here are what a reviewer needs,
and they are complete as committed.

## Files

| file | what it is |
| --- | --- |
| `RUBRIC.md` | frozen review categories and field definitions — read first |
| `review_priority.md` | **start here**: the high-influence subset, by descending influence |
| `review_full.md` | every score-moving node, grouped by case |
| `review_set_priority.jsonl` | machine-readable priority subset |
| `review_set_full.jsonl` | machine-readable full set; fill the `human_review` fields here |
| `hidden_case_context.md` / `.json` | **post-hoc only**: later resolutions and reference discriminators |
| `stats.json` | review-set statistics |

## How nodes were selected

Selection uses **only the verifier's frozen score contributions**. The post-hoc
auditor outputs are loaded *after* selection, and the build asserts they did not
change it.

- **Score-moving (full set).** Under the configured `independent` aggregation, each
  node adds `log(p·LR + 1 − p)` to each hypothesis's log-score, where `p = P(X|H)`
  and `LR` is the evidence likelihood ratio. A node is score-moving when those
  additions differ between the two hypotheses, i.e. it moves the log-odds.
  `absolute_influence` is that difference. One node (fly-wing X4) adds an equal,
  nonzero amount to both hypotheses; it changes neither the normalised scores nor
  the ranking and is listed in `stats.json` as excluded.
- **Priority set.** The smallest set of top-influence nodes, ranked across all eight
  cases, whose influence sums to at least 80% of the total.
- **Counterfactuals,** per node:
  - *evidence withheld*: the node is treated as unobserved, which is exact because
    contributions are additive;
  - *node deleted*: the node and its edges are removed, so its children lose the
    route through it, and the case is rescored with `src.inference.bayes`.

## What each record contains

- `proposition`, `case_context`: hypotheses exactly as given to the verifier (from
  `input.json`), the display labels it used, and the cutoff.
- `verifier_graph`: for every hypothesis, the direct edge label and rationale, every
  route through a parent (parent's edge label, parent's `P(X|H)`, chain edge label
  and rationale), and the resulting `P(X|H)`. `P(X|H)` is the noisy-OR over those
  routes, with 0.5 when there is no route.
- `verifier_evidence`: the queries; the evidence label used in the score (and
  whether the harness enforced it); the assessor's rationale, cited spans, key
  papers and raw JSON response; and **every paper shown, with the exact text block
  the assessor read**, cut from the rendered prompt in `events.jsonl`.
  - The method gives one evidence label per node, not per paper, so there are no
    per-paper contributions.
  - Each cited span records whether it appears verbatim in the shown text, and its
    longest exact run if it does not.
- `score_influence`: per-hypothesis contributions, log-odds contribution,
  influence, rank in case and overall, cumulative share, priority flag, and both
  counterfactuals.
- `posthoc_automated_audit`: **non-authoritative**. It includes:
  - the primary LLM auditor, which saw hidden reference discriminators;
  - the opposition call derived from it and the edge labels;
  - the evidence-attribution auditor;
  - where available, the blind second rating (an LLM, not a human) and the
    auditor retest;
  - disagreement flags.
- `human_review`: blank.

## Keeping verifier output apart from hidden context

Hidden benchmark annotations appear in only two places: the
`posthoc_automated_audit` object (the matched-discriminator field is suffixed
`_HIDDEN_CONTEXT`) and `hidden_case_context.*`. They never appear in `proposition`,
`case_context`, `verifier_graph`, `verifier_evidence` or `score_influence`;
`tests/test_review_packet.py` enforces this. The Markdown views collapse the
automated audit at the end of each entry and never show resolutions inline.

## Known mechanical facts (not interpretations)

- Frozen `scores.json` stores `P(X|H)` to 4 decimal places and contributions to 6
  (`src/inference/bayes.py`). The rebuild matches at exactly that precision.
- `gcn4_med15_complex_vs_condensate` has case log-odds of about 0.002, so single-node
  removals flip its ranking easily (see `stats.json`).
- A few assessor-cited "supporting spans" are only partly verbatim in the shown text;
  each span record carries the evidence.
