# Edge-judgment validation

The consequence graph's edges carry `P(X_v | H_i)` — the scientific implication. After DECISIONS #29 they carry *all* of it, so this is the component most in need of validation.

Judge A is the production prompt; judge B is never shown the ordinal labels and is mapped onto them afterwards. Same single deployment, so the same-model caveat applies.

## Reproducibility on real edges (n=90)

| statistic | value |
| --- | --- |
| **direction reproducibility** (implies/neutral/contradicts) | **0.867** |
| direction kappa | 0.607 |
| exact ordinal agreement | 0.489 |
| agreement within one ordinal step | 0.933 |
| judge A vs the stored production label | 0.767 |
| judge B vs the stored production label | 0.378 |

Direction is the number that matters: an ordinal step between `implied` and `strongly_implied` barely moves a ranking, whereas `implies` against `neutral` does.

Distribution of judge A's labels on real edges: `implied` 41, `neutral` 24, `strongly_implied` 17, `weakly_implied` 8

## Reproducibility by abstraction level of the node

| level | edges | direction reproducibility | exact ordinal | neutral rate |
| --- | --- | --- | --- | --- |
| `class` | 27 | 0.889 | 0.370 | 0.259 |
| `mechanistic` | 31 | 0.839 | 0.484 | 0.323 |
| `specific` | 32 | 0.875 | 0.594 | 0.219 |

A *higher* neutral rate at the abstracted levels would be the warning sign: it would mean the abstraction went so far that the hypothesis no longer implies the proposition, i.e. the node carries evidence but no connection back to the claim. Lower direction reproducibility there would mean the bridge is not one two readers agree on.

## Control: a proposition paired with a hypothesis from another instance

These are unrelated claims. Both judges should answer `neutral`.

| judge | neutral rate |
| --- | --- |
| A (production prompt) | **1.000** |
| B | **1.000** |

A low neutral rate here means the edge judge is inventing implications between unrelated claims — and since the edges now carry all the scientific reasoning, that failure would not show up anywhere in the evidence numbers.

