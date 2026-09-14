# Assessor validation — provisional

Rubric freeze `5d8465ae0088c1ee`. Model `None`, judges a=assessor_judge_a_v1, b=assessor_judge_b_v1.

> **Both judges run on one deployment; they differ in prompt and reasoning scaffold only. Same-model agreement has correlated errors and is weaker evidence than cross-model agreement.**

> This measures reproducibility, grounding and robustness to adversarial controls. It does **not** measure agreement with expert judgment, because no expert labels exist. Passing makes the assessor *provisionally* validated.

## Criteria 1 and 2 — inter-assessor reproducibility

| statistic | n | value | threshold | verdict |
| --- | --- | --- | --- | --- |
| three-way (all cases) | 291 | 0.883 | — | — |
| three-way kappa | 291 | 0.514 | — | — |
| **boundary reproducibility** | 287 | **0.882** | 0.8 | **PASS** |
| boundary kappa | 287 | 0.460 | — | — |
| **direction reproducibility** | 291 | **0.897** | 0.8 | **PASS** |
| direction kappa | 291 | 0.578 | — | — |

## Criterion 3 — grounded and independently reproduced

Of the evidential judgments judge `a` makes, the share that carry a span found verbatim in the supplied abstract, need no unsupported fact, **and** are also called evidential by the other judge.

| | n |
| --- | --- |
| judge a called evidential | 52 |
| …span grounded verbatim | 52 |
| …and no unsupported fact | 52 |
| …and reproduced by the other judge | **24** |

**grounded + reproduced = 0.462**, threshold 0.9 -> **FAIL**

## Criterion 4 and the adversarial controls

| condition | judgments | informative | P(informative) | grounded spans |
| --- | --- | --- | --- | --- |
| `real` | 582 | 78 | 0.134 | 78 |
| `mismatched` | 582 | 0 | 0.000 | 0 |
| `span_removed` | 78 | 42 | 0.538 | 41 |

**P(informative | mismatched abstract) = 0.000**, must be ≤ 0.1 -> **PASS**

### Direction flip under negation

Of 0 case(s) where both the original and the negated proposition drew a directional judgment, **0 flipped** and 0 kept the same direction (n/a).

A judgment that stays informative but does not move direction when the claim is negated is not reading the claim.

### Survival after the supporting span is removed

78 grounded positive(s) re-judged with the supporting sentence deleted; **42 still called the record evidential** (0.538).

| of the survivors | n |
| --- | --- |
| cited a **different** span, still verbatim | 42 |
| cited the **same** span (should be impossible) | 0 |
| cited no span at all | 0 |

**Read this as a limitation of the control, not a failure of the assessor.** Every survivor moved to a different, still-verbatim span: the abstracts carry redundant support, and deleting one sentence leaves other evidential sentences standing. To test what this control was meant to test, every span the judge could rely on has to go, or the control needs single-finding abstracts.

### Where the two judges diverge

| | judge b DIRECT | INDIRECT | NO_EVIDENCE |
| --- | --- | --- | --- |
| judge a DIRECT | 4 | 4 | 0 |
| judge a INDIRECT | 0 | 16 | 28 |
| judge a NO_EVIDENCE | 0 | 2 | 237 |

- both call it evidential: **24**
- only a does: **28**
- only b does: **2**

Agreement on **direct** evidence is 8 of 8. The divergence is almost entirely in the *indirect* category.

**This is a systematic offset, not symmetric noise.** One prompt's bar for 'this establishes a fact that changes belief' sits well below the other's, even though both were given the same frozen rubric.

## Gate

| criterion | verdict |
| --- | --- |
| criterion_1_boundary_reproducibility | **PASS** |
| criterion_2_direction_reproducibility | **PASS** |
| criterion_3_grounded_and_independently_reproduced | **FAIL** |
| criterion_4_negative_control | **PASS** |

**Overall: FAIL**

Do not proceed to calibration or the sweep.

