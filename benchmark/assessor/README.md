# Assessor label set

`labelset_candidates.jsonl` — real assessment cases pulled from the consequence-graph
runs, one per line, with the retrieved abstracts included so a judgment can be made
without re-running retrieval. Regenerate with:

```bash
python3 scripts/build_assessor_labelset.py --n-per-stratum 4
```

Selection is deterministic and stratified by the current label, **over-sampling the
`no_evidence`-that-concedes-related-work stratum** — that is where the construct
question lives (82% of all `no_evidence` verdicts are in it).

## Status of the labels

Six cases carry `labelled_by: "proposed-unreviewed"`. **These are proposals from the
implementing agent, not ground truth**, and one of them (`K-0038-K4::X45`) disagrees
with the current assessor. They exist to make the rubric in `docs/ASSESSOR_RUBRIC.md`
concrete and testable, and they need the research owner's adjudication before any
prompt is judged against them. The remaining cases are unlabelled
(`gold_label: null`).

## Fields

| field | meaning |
| --- | --- |
| `proposition` | the node text the assessor saw |
| `papers` | exactly the records shown, with abstracts |
| `current_label` / `current_rationale` | what `evidence_assess_v1` returned |
| `rationale_invokes_directness` / `rationale_concedes_related_work` | regex flags used for the stratification |
| `gold_label` | adjudicated label, or null |
| `gold_directness` | `direct` \| `indirect` \| null |
| `gold_link_type` | one of the rubric's enumerated link types |
| `gold_link` | the one-sentence inferential link; required for `indirect` |
| `proposition_unassessable` | the proposition cannot be checked as written (a generation defect) |
| `disagrees_with_current` | the adjudicated label differs from `current_label` |

## Do not

Do not label cases by running a model over them and calling the output gold. The
instrument and the thing being measured would then be the same, and the agreement
number would be meaningless.
