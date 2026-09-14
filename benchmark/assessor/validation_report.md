# Assessor validation — provisional

Rubric freeze `5d8465ae0088c1ee`. Model `None`, judges a=assessor_judge_a_v1, b=assessor_judge_b_v1.

> **Both judges run on one deployment; they differ in prompt and reasoning scaffold only. Same-model agreement has correlated errors and is weaker evidence than cross-model agreement.**

> This measures reproducibility, grounding and robustness to adversarial controls. It does **not** measure agreement with expert judgment, because no expert labels exist. Passing makes the assessor *provisionally* validated.

## Criteria 1 and 2 — inter-assessor reproducibility

| statistic | n | value | threshold | verdict |
| --- | --- | --- | --- | --- |
| three-way (all cases) | 42 | 0.905 | — | — |
| three-way kappa | 42 | 0.628 | — | — |
| **boundary reproducibility** | 40 | **0.900** | 0.8 | **PASS** |
| boundary kappa | 40 | 0.459 | — | — |
| **direction reproducibility** | 42 | **0.952** | 0.8 | **PASS** |
| direction kappa | 42 | 0.813 | — | — |

## Criterion 3 — grounded and independently reproduced

Of the evidential judgments judge `a` makes, the share that carry a span found verbatim in the supplied abstract, need no unsupported fact, **and** are also called evidential by the other judge.

| | n |
| --- | --- |
| judge a called evidential | 7 |
| …span grounded verbatim | 7 |
| …and no unsupported fact | 7 |
| …and reproduced by the other judge | **5** |

**grounded + reproduced = 0.714**, threshold 0.9 -> **FAIL**

## Criterion 4 and the adversarial controls

| condition | judgments | informative | P(informative) | grounded spans |
| --- | --- | --- | --- | --- |
| `real` | 84 | 12 | 0.143 | 12 |
| `mismatched` | 84 | 0 | 0.000 | 0 |
| `swapped` | 84 | 2 | 0.024 | 2 |
| `negated` | 84 | 14 | 0.167 | 14 |
| `span_removed` | 12 | 10 | 0.833 | 9 |

**P(informative | mismatched abstract) = 0.000**, must be ≤ 0.1 -> **PASS**

### Direction flip under negation

Of 12 case(s) where both the original and the negated proposition drew a directional judgment, **11 flipped** and 1 kept the same direction (0.917).

A judgment that stays informative but does not move direction when the claim is negated is not reading the claim.

### Survival after the supporting span is removed

12 grounded positive(s) re-judged with the supporting sentence deleted; **10 still called the record evidential** (0.833).

| of the survivors | n |
| --- | --- |
| cited a **different** span, still verbatim | 10 |
| cited the **same** span (should be impossible) | 0 |
| cited no span at all | 0 |

**Read this as a limitation of the control, not a failure of the assessor.** Every survivor moved to a different, still-verbatim span: the abstracts carry redundant support, and deleting one sentence leaves other evidential sentences standing. To test what this control was meant to test, every span the judge could rely on has to go, or the control needs single-finding abstracts.

## Gate

| criterion | verdict |
| --- | --- |
| criterion_1_boundary_reproducibility | **PASS** |
| criterion_2_direction_reproducibility | **PASS** |
| criterion_3_grounded_and_independently_reproduced | **FAIL** |
| criterion_4_negative_control | **PASS** |

**Overall: FAIL**

Do not proceed to calibration or the sweep.

