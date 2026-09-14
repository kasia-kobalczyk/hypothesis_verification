# Uncertainty reporting protocol — FROZEN before the reserve was opened

Frozen 2026-09-13, after the noise models (`benchmark/frozen/noise_model_v1.json`)
and before any reserve row was run.

## What is reported

**Primary output stays the deterministic score and ranking.** Perturbation analysis
is reported alongside it, never in place of it.

For each instance, Monte Carlo perturbation using the frozen empirical noise models
gives

    p_i = P_perturbation(H_i ranks first)

and for a pair, `P(H+ ranked above H-)`. Three example dev-20 rows show why this is
not cosmetic: `0052` sits at 1.00, `0117` at 0.62, `0288` at 0.53. A point ranking
reports all three identically as 'gold first'.

## Terminology, which matters here

This is **ranking stability** or **judgment uncertainty**. It is NOT a posterior over
scientific truth and must never be described as one. The perturbation measures
sensitivity to variation in model-generated judgments, using noise distributions
measured empirically -- not a calibrated belief about the world. The ordinal mappings
remain uncalibrated placeholders (DECISIONS #31), so no quantity here carries
probabilistic meaning about the science.

## No abstention threshold

The continuous stability quantity is reported and nothing is thresholded. 'Abstain
below 0.8' would be one more arbitrary design choice of exactly the kind this project
has had to unwind twice (DECISIONS #16, #26). Coverage and selective accuracy already
handle the separate case where no informative evidence exists at all.

## Two failure modes kept apart

| | meaning |
| --- | --- |
| no evidence | the posterior never moved; nothing was found to reason from |
| unstable ranking | evidence exists and the ranking it produces is not robust to judgment noise |

These are scientifically different and are never merged into one accuracy number.

## Pre-registered for the reserve run

**Primary metric:** pair accuracy (ties 0.5).

**Secondary diagnostics:** coverage; selective accuracy;
`P_perturb(gold first)`; the full ranking-stability distribution.

**Frozen method:** `benchmark/frozen/narrow_graph_v3_complete.json` --
consequence_generate_v3, evidence_assess_v2 (narrow), edge_assess_v1 +
edge_assess_chain_v1, `inference.aggregation: independent`, uncalibrated placeholder
ordinal mappings, `semantic_merge_mode: none`.

**Frozen noise model:** `benchmark/frozen/noise_model_v1.json`, estimated from the
20 development rows only (400 nodes x 3 repeats). **Nothing is estimated from the
reserve.** Node instability 0.165; the empirical transition matrix shows where it
lives:

| observed label | stays put under nuisance variation |
| --- | --- |
| `no_evidence` | 0.96 |
| `strong_support` | 0.81 |
| `support` | 0.68 |
| `weak_support` | **0.51** |

`weak_support` is a coin flip. That is a property of the assessor worth reporting in
its own right, and it is left uncorrected: adjusting the scale to make rankings look
steadier would be tuning stability rather than measuring it.

**The reserve is used exactly once.** 12 rows, never run, never inspected. Whatever
it produces is the result; there is no second attempt and no re-freezing afterwards.

## Why uncertainty is propagated at all

Not because the graph fails to remove dependence. Three candidate dependence
mechanisms were tested and all rejected: proposition structure (family aggregation,
no effect on flip rate), shared literature (12-19% driving-paper overlap), and
correlated assessor behaviour (within-row excess covariance 0.0009 against per-node
variance 0.0305, ratio 0.031).

The instability is **accumulated independent judgment noise**. Each additional
informative node adds another noisy judgment, so noise grows as sqrt(n) while the
score margin does not grow proportionally. More evidence coverage can therefore
coexist with less ranking stability. That is the finding the protocol exists to
report honestly rather than hide.
