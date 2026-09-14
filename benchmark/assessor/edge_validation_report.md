# Edge-judgment validation

The consequence graph's edges carry `P(X_v | H_i)` — the scientific implication. After DECISIONS #29 they carry *all* of it, so this is the component most in need of validation.

Judge A is the production prompt; judge B is never shown the ordinal labels and is mapped onto them afterwards. Same single deployment, so the same-model caveat applies.

## Reproducibility on real edges (n=120)

| statistic | value |
| --- | --- |
| **direction reproducibility** (implies/neutral/contradicts) | **0.808** |
| direction kappa | 0.631 |
| exact ordinal agreement | 0.608 |
| agreement within one ordinal step | 0.992 |
| judge A vs the stored production label | 0.758 |
| judge B vs the stored production label | 0.583 |

Direction is the number that matters: an ordinal step between `implied` and `strongly_implied` barely moves a ranking, whereas `implies` against `neutral` does.

Distribution of judge A's labels on real edges: `neutral` 49, `implied` 32, `weakly_implied` 23, `strongly_implied` 9, `unlikely` 6, `strongly_contradicted` 1

## Control: a proposition paired with a hypothesis from another instance

These are unrelated claims. Both judges should answer `neutral`.

| judge | neutral rate |
| --- | --- |
| A (production prompt) | **1.000** |
| B | **1.000** |

A low neutral rate here means the edge judge is inventing implications between unrelated claims — and since the edges now carry all the scientific reasoning, that failure would not show up anywhere in the evidence numbers.

