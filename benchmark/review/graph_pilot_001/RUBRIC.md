# Human review rubric — graph pilot packet GP1

Frozen from BENCH-GRAPH-REVIEW-001 §6. Do not edit during review; if a category
proves inadequate, record that in `human_notes` and keep the original rubric so
labels stay comparable.

Assign **one** `human_primary_category`. Add any others that also apply to
`human_secondary_flags`.

## Categories

### `genuine_discriminator`
The proposition is scientifically implied/predicted by at least one hypothesis and
the competing hypothesis/hypotheses make a meaningfully different positive
prediction or are genuinely inconsistent with it.

### `compatible_non_discriminative`
The proposition may be true or supported, but it does not meaningfully distinguish
the candidates.

### `generic_component_fact`
The proposition is an abstract/component-level fact that can be supported
independently of the distinctive composite explanatory hypothesis and therefore
risks recreating the historical component-truth failure.

### `silence_as_null_error`
A hypothesis does not determine the proposition, but the system assigned it a
directional null/opposite/contradictory judgment, thereby manufacturing contrast.

### `invalid_or_weak_implication`
The proposition is not adequately licensed by the originating hypothesis or
requires an unstated scientific bridge too large to treat as an implication edge.

### `evidence_construct_mismatch`
The evidence span is grounded in the cited source but addresses a different
construct/proposition than the node.

### `valid_but_historically_uninformative`
The discriminator is scientifically valid, but pre-cutoff evidence is
absent/non-informative, so it should not materially resolve the hypotheses
historically.

## The distinction that matters most

- **Silence is not** `no change`, `negative`, `unlikely`, or `contradicted`.
- Do not infer a null prediction unless the hypothesis substantively predicts a
  baseline/no-effect outcome.

## Fields

| field | values |
| --- | --- |
| `human_primary_category` | one category above |
| `human_secondary_flags` | list of categories above |
| `human_prediction_for_each_hypothesis` | per hypothesis: `positive_or_present` \| `negative_or_absent` \| `neutral_or_no_change` (a substantive null prediction) \| `indeterminate` (silent) |
| `human_is_genuinely_discriminative` | `true` \| `false` |
| `human_silence_as_null_error` | `true` \| `false`: a hypothesis you judged `indeterminate` received a non-`neutral` verifier edge |
| `human_implication_validity` | `valid` \| `weak` \| `invalid`: is the edge from the *origin* hypothesis licensed? |
| `human_evidence_relevance` | `relevant` \| `construct_mismatch` \| `generic_compatibility` \| `not_applicable` (no informative evidence) |
| `human_confidence` | `high` \| `medium` \| `low` |
| `human_notes` | free text |
| `reviewer` | name/initials |

## Suggested order of work

1. Read the phenomenon, the hypotheses and the proposition.
2. Fill `human_prediction_for_each_hypothesis` **before** looking at the verifier's
   edge labels.
3. Compare with the verifier's cross-hypothesis judgments and fill the silence and
   validity fields.
4. Read the evidence shown to the assessor and fill `human_evidence_relevance`.
5. Only then, if wanted, open the collapsed post-hoc automated audit, and
   separately `hidden_case_context.md`. Both are non-authoritative, and the second
   reveals how the dispute was later resolved.
