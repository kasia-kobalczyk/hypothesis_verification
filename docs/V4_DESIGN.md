# v4 — discrimination-gated consequence-graph verifier

Method id: `consequence_graph_v4` · version: `consequence_graph_v4_discrimination_gated`
Directive: BENCH-GRAPH-V4-DEV-001 · Development set: the 8 spent pilot cases (not held-out evidence)

## 1. Why v4

Human review of the frozen v3 pilot (D045, D046) found that v3's comparative scores were
driven mostly by propositions that do not discriminate:

| v3 failure | Mechanism in v3 |
| --- | --- |
| categorical silence error | a hypothesis silent about a proposition got `unlikely` → P(X\|H) = 0.30 |
| neutral-mapping pseudo-discrimination | a correct `neutral` is still P = 0.50, so support for a proposition one hypothesis predicts moved relative scores |
| generic component facts | class-level truths got opposed edge labels and accumulated support |
| construct mismatch | evidence about a related construct was scored as bearing on the proposition |
| inherited routes | a child node inherited a directional prediction through its parent's chain edge |

Under D045+D046 attribution, reviewed genuine discriminators carried 8.1% of v3's score influence;
silence errors, generic/compatible facts and construct mismatches carried most of the rest.

## 2. Architecture

```text
v3 pipeline, UNCHANGED                      v4 comparative layer (replaces v3 scoring)
─────────────────────────────────────       ───────────────────────────────────────────────
consequence_generate_v3                     prediction_state      (LLM, 1 call / node)
v3 root + chain edge judgments  ──(kept for comparison, not scored)
proposition_query_v1                        discrimination gate   (deterministic)
retrieval (cutoff-enforced)                 construct_match       (LLM, informative evidence only)
evidence_assess_v2 ─────────────────────▶   gated scoring         (verifier's score_hypotheses)
```

`ConsequenceGraphV4Verifier.run_instance` calls the v3 `run_instance` and then
`run_v4_layer`. v3's source, prompts and configs are not modified. v3's scores on the same
graph are kept in the `scores_v3_reference` artifact. The same `run_v4_layer` is applied to
the frozen pilot by `scripts/replay_v4_on_frozen.py` (stage A of development).

## 3. Prediction state (separate from strength)

For every (hypothesis, proposition) pair:

| state | meaning |
| --- | --- |
| `positive_or_present` | the hypothesis's own content requires the proposition or makes it clearly expected |
| `negative_or_absent` | the hypothesis's own content is incompatible with it or makes it clearly unexpected |
| `substantive_null` | the hypothesis positively commits to no effect / baseline for the quantity concerned |
| `indeterminate` | the hypothesis does not determine it: compatible with it being true and with it being false |

- **Strength** (`strong | moderate | weak`) exists only for determinate states. An
  `indeterminate` state has no strength and no likelihood, ever.
- **One call per proposition covers every hypothesis**, using the same anonymised candidate
  labels as v3. The response must contain exactly one entry per candidate, with a valid
  state and, for determinate states, a strength. Otherwise the proposition is recorded as
  `prediction_states_unavailable` and not scored (fail closed). A missing hypothesis is
  never defaulted.
- **The prompt does not show the research question.** Neither did v3's edge assessor, and
  framing "A or B?" invites manufactured opposition.

## 4. Discrimination gate (deterministic, `src/inference/discrimination.py`)

| profile (k = 2) | class | may move relative scores |
| --- | --- | --- |
| two determinate, different states (pos/neg, pos/null, neg/null) | `comparative_discriminator` | **yes** |
| one determinate, one indeterminate | `one_sided_prediction` | no |
| two identical determinate states (e.g. pos/pos, any strengths) | `shared_prediction` | no |
| both indeterminate | `all_indeterminate` | no |
| k > 2 with any indeterminate hypothesis | `partially_indeterminate_contrast` | no (conservative; the pilot is k = 2) |

**Positive vs positive with different strengths is `shared`.** v4 has no representation of
different quantitative commitments within a state, so strength differences never create a
contrast.

**Ineligible propositions are not deleted.** They stay in the graph, with states, evidence
label and construct result, and are listed in the `one_sided_prediction`,
`shared_prediction`, `all_indeterminate` and `states_unavailable` buckets of the
`discrimination` artifact, each with the reason it was gated. One-sided support may become
informative under a future explicit background-probability model; v4 deliberately does not
treat it as comparative evidence.

## 5. Construct match (`src/evidence/construct_match.py`)

For every proposition with informative evidence (a label other than `no_evidence` or
`mixed`):
- **Inputs:** a narrow judge sees the proposition, the spans the v3 assessor quoted, and the
  records it cited, rendered by the cutoff-enforcing literature renderer. If the assessor
  cited none, all shown records are used.
- **Blind to the assessor:** it never sees the evidence label or the assessor's rationale.
- **Element-wise judgment (iteration 2):** the judge lists the elements the proposition
  asserts and marks each `established | partly | not_established`. The gating label is
  **derived in code**:
  - `direct`: every element established;
  - `mismatch`: none established even partly;
  - `partial`: otherwise.
- **The holistic impression is not used:** it is recorded as `model_overall_impression` but
  never gates.

**Policy (human decision): only `direct` may move comparative scores.** `partial` is
recorded and reported as a sensitivity analysis; `mismatch` contributes zero. A failed
construct call leaves the proposition `construct_unassessed` and unscored.

## 6. Gated scoring

- **Scored nodes:** only nodes that pass every check: comparative profile, informative
  evidence, `direct` construct match.
- **Edges:** each hypothesis gets one direct edge derived from its state, via existing
  labels of the frozen `configs/ordinal_mappings.yaml` (no new number):

  | state | strong | moderate | weak |
  | --- | --- | --- | --- |
  | positive_or_present | strongly_implied (.95) | implied (.80) | weakly_implied (.65) |
  | negative_or_absent | strongly_contradicted (.10) | unlikely (.30) | unlikely (.30) |
  | substantive_null | strongly_contradicted (.10) | unlikely (.30) | unlikely (.30) |

  `substantive_null` predicts no effect for the quantity the proposition asserts, so it
  scores like a negative prediction. The state stays distinct in every artifact. The
  negative side of the frozen scale has only two labels.
- **No chain edges.** A child never inherits a prediction from its parent.
- **Aggregation:** `score_hypotheses(..., aggregation="independent")`, passed explicitly.
  v3's method never passed `inference.aggregation` (see §8). Uniform prior.
- **No scored node** → exactly equal scores. v4 is allowed to be uncertain.

## 7. Differences from v3

| aspect | v3 | v4 |
| --- | --- | --- |
| cross-hypothesis judgment | one ordinal label (`neutral` = 0.50) | state + strength; `indeterminate` has no number |
| missing judgment | defaults to 0.50 | fail closed, node unscored |
| which nodes score | every node with an evidence label | only comparative profiles with direct evidence |
| one-sided / shared propositions | scored | retained descriptively, zero contribution |
| construct check | none | element-wise, direct only |
| chain edges | propagate into P(X\|H) | not used for scoring |
| aggregation argument | not passed (default independent) | passed explicitly (independent) |
| generation, queries, retrieval, evidence assessment | — | identical (v3 code path) |

## 8. v3 defects observed and deliberately not fixed

The directive forbids changing v3. These were found while building v4 and are avoided or
recorded in v4 only:

1. `inference.aggregation` is never passed to `score_hypotheses`, so the config value is
   ignored. v3 runs were `independent`, which matches the config.
2. `evidence_assess_v2` tells the model its supporting spans are checked automatically;
   nothing checks them. 4 of 252 pilot spans were only partly verbatim.
3. Root-edge validation does not require a judgment for every hypothesis; a missing one
   becomes 0.50.
4. `_finalise` is defined twice in `src/inference/bayes.py`, and a test pins an obsolete
   `ASSESS_PROMPT` constant.

## 9. Artifacts per instance (v4 runs)

- **`discrimination.json`:** per node, the states (with basis and rationale), profile
  class, eligibility, evidence label, construct result, gate reason and contribution; plus
  buckets, summary counts, errors, and the prompt names and policy.
- **`scores.json`:** v4 scores, ranking, log-scores, contributions and inference settings,
  plus `v3_reference_scores`.
- **`scores_v3_reference.json`:** the full v3 scores artifact on the same graph.

## 10. Development history

Iterations, every methodological change between them, and the freeze decision are in
`docs/V4_DEV_REPORT.md`.
