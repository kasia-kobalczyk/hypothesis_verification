# v4-scope — comparative scope and contrast-bearing evidence

Method id: `consequence_graph_v4_scope` · version: `consequence_graph_v4_scope`
Directive: BENCH-GRAPH-V4-SCOPE-001 · Development set: the 8 spent pilot cases (not held-out evidence)
Builds on: [`V4_DESIGN.md`](V4_DESIGN.md) (prediction states and the discrimination gate, unchanged)

## 1. Why

BENCH-GRAPH-V4-DEV-001 left two coupled failures after prediction-state gating:

| failure | where it showed |
| --- | --- |
| broad class facts and "can occur" possibility claims had determinate opposed states and scored | the live v4 run scored only 3 class-level "can" propositions |
| whole-proposition construct matching rated specific discriminators `partial`, so they never scored | 0 nodes scored in stage A under direct-only; allowing `partial` re-admitted mostly generic facts |

v4-scope separates the two questions the construct match was conflating: *is this proposition
specific enough to discriminate?* (scope), and *does the evidence bear on the part of it that
discriminates?* (contrast relevance).

## 2. Architecture

```text
v3 pipeline, UNCHANGED            v4-scope comparative layer (replaces v3 scoring)
──────────────────────────        ─────────────────────────────────────────────────────────────
consequence_generate_v3           prediction_state_v2   (LLM; the v4 head prompt, pinned by name)
v3 edge judgments (not scored)    proposition_scope_v1  (LLM; separate call, every node)
proposition_query_v1              contrast_element_v1   (LLM; nodes with informative evidence)
retrieval (cutoff-enforced)       contrast_relevance_v1 (LLM; nodes with an element and records)
evidence_assess_v2 ────────────▶  gate_node_scope       (deterministic)
                                  score_gated           (verifier's score_hypotheses, unchanged)
```

`ConsequenceGraphV4ScopeVerifier` (`src/methods/consequence_graph_v4_scope.py`) calls the v3
`run_instance`, then `run_v4_scope_layer`. The previous v4 method is not modified and stays
registered as `consequence_graph_v4`. Stage A applies the same layer to the frozen v3 pilot:
`scripts/replay_v4_on_frozen.py --layer v4_scope`.

**Coverage choice.** Scope is classified for every proposition, and the contrast element and
relevance for every proposition with informative evidence, not only for otherwise eligible
ones. That costs extra calls but is what the directive's §10 specificity-assessability table
needs (scope × evidence for *all* generated propositions). Only the gate decides what scores.

## 3. Proposition scope (`proposition_scope_v1`, `src/graph/proposition_scope.py`)

| class | eligible to score | meaning |
| --- | --- | --- |
| `hypothesis_specific` | yes | directly instantiates a distinctive commitment of a candidate, in the system under dispute |
| `mechanism_specific` | yes | tests a mechanism central to a candidate and remains diagnostic for the system under dispute |
| `broader_class_fact` | no | general property of a wider class; may hold whichever candidate is right |
| `possibility_claim` | no | only that something can / may occur, somewhere, without asserting it governs the phenomenon |
| `invalid_or_underspecified` | no | too vague or not operationally meaningful |

- A **separate call**, never a field of the prediction-state response (directive §3). The
  state prompt is `prediction_state_v2`, byte-identical to the v4 head; a test pins this.
- The scope prompt **sees the research question**, because scope is relative to the system
  under dispute, which the question names. The state prompt still does not see it.
- The prompt says origin is irrelevant ("derived from one candidate" is not a reason for
  `hypothesis_specific`). The gate has no origin input at all.
- Output also records `system_under_dispute`, `proposition_is_about` and
  `asserts_actual_occurrence_in_system_under_dispute` (boolean, required) as an audit trail;
  only `scope` is used by the gate.
- The illustration is a generic invented dispute (a lake's algal blooms), not a development case;
  a test checks the new prompts for distinctive terms of all 8 development cases.

## 4. Contrast-bearing element (`contrast_element_v1`)

Given the candidates, the recorded prediction states and the proposition, the extractor returns:

```json
{"has_contrast": true,
 "shared_context": "...", "contrast_variable": "...", "contrast_direction_or_state": "...",
 "system_or_population": "...", "measurement_or_observable": "..."}
```

Every field is a required non-empty string; `has_contrast` a required boolean. The proposition
text is kept alongside. `has_contrast: false` means the extractor found no part of the proposition
that carries a disagreement between the candidates; such a proposition cannot score.

## 5. Contrast relevance (`contrast_relevance_v1`, `src/evidence/contrast_relevance.py`)

The judge sees the proposition, its element, the assessor's quoted spans and the exact cited
records (every shown record if none were cited). It never sees the evidence label or the
assessor's rationale. It answers three structured questions; the category is derived in code:

| Q1 contrast variable reported | Q2 shared context supported | Q3 different construct | category | scores |
| --- | --- | --- | --- | --- |
| yes | any | any | `contrast_direct` | yes |
| partly | any | any | `contrast_partial` | sensitivity analysis only |
| no | any | yes | `construct_mismatch` | no |
| no | yes | no | `context_only` | no |
| no | no | no | `no_evidence` | no |

Q1 = `yes` with Q3 = `yes` is kept as `contrast_direct` (records may report the variable and also
a correlate) and is counted separately in the development metrics.

## 6. Gate (`gate_node_scope`, deterministic)

A proposition scores only if all hold; the first failing check is the recorded reason:

1. prediction states exist → else `prediction_states_unavailable`;
2. the state profile is a determinate contrast → else `profile_<class>` (v4 rule, unchanged; a
   scope judgment can never make a one-sided or shared profile comparative);
3. scope was classified → else `scope_unavailable`;
4. scope ∈ {`hypothesis_specific`, `mechanism_specific`} → else `scope_<class>`;
5. the evidence assessment exists and is informative → else `no_evidence_assessment` /
   `uninformative_evidence`;
6. a contrast element exists → else `contrast_element_unavailable`;
7. it carries a contrast (`has_contrast`) → else `no_contrast_bearing_element`;
8. relevance was judged → else `contrast_relevance_unavailable`;
9. relevance ∈ allowed (main method: `contrast_direct`) → else `relevance_<category>`.

Every LLM error or malformed response fails closed at the corresponding step. Nothing is
deleted: every proposition keeps its states, scope, element, relevance and gate record, and
unscored ones are listed in buckets keyed by gate reason.

Scoring is unchanged from v4: `score_gated` builds a graph of the scored propositions only, with
state-derived edges, and calls the verifier's `score_hypotheses` with independent aggregation,
the frozen `v0-placeholder` ordinal mappings, and no chain routes. `indeterminate` contributes
nothing. The layer also records scores under the sensitivity policy (`contrast_partial` allowed),
labelled `NOT_THE_METHOD`.

## 7. Development analysis

`scripts/analyze_v4_scope.py` (deterministic) writes `benchmark/v4_scope/<iteration>/development_metrics.json`:
gate re-derivation consistency, state preservation vs prior v4 and D046, scope behaviour against
D045/D046, contrast-relevance distribution, the scope × evidence table, influence composition,
the partial sensitivity analysis, scored nodes, and replicate stability.
