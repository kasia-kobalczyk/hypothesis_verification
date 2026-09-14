# Evaluation protocol

The **problem definition** and the **benchmark protocol** are separate things, and
conflating them has already cost us one misleading number. This document keeps them
apart.

---

## 1. The formulation is for arbitrary k

Verification takes a scientific question, a candidate set

    H = {H_1, ..., H_k},   k >= 2

and scores every candidate from pre-cutoff literature alone. Nothing in the method
is specific to k=2: consequence generation runs per candidate, cross-evaluation
rates every proposition against every candidate, and the Bayesian propagation is
defined over the whole set. There is no scientific reason verification should only
compare two hypotheses.

`src/benchmark/loader.py` therefore supports k=2 (`kind: pairs`), the original
11-way ResearchBench task (`kind: instances`), and controlled sets at any k
(`kind: k_sets`).

## 2. Results at different k are not directly comparable

Ranking one correct candidate out of 2 is a different problem from ranking it out of
10:

* chance top-1 is **1/k**, so a pooled top-1 over mixed k has no single baseline;
* the graph grows — cross-evaluation is O(nodes x k) model calls;
* the evidence has to discriminate among more explanations at once.

**k>2 is not simply "harder".** It is a different and more constrained ranking
problem. We say that rather than calling it difficulty.

`aggregate_metrics` enforces the distinction: top-1, MRR and mean gold rank are
reported **only** inside `by_k`, each next to its own `chance_top1`. The two
pooled metrics are the ones whose chance level does not move with k.

## 3. Primary evaluation: k=2, pairwise

The headline number is pairwise accuracy over frozen gold-vs-comparable-negative
pairs:

    Acc_pair = (1/N) * sum_n [ 1{S(H+) > S(H-)} + 0.5 * 1{S(H+) = S(H-)} ]

Ties score **0.5** explicitly, in both `pair_metrics` and
`pairwise_accuracy_all_negatives`. Chance is 0.5.

Why this is the headline:

* candidate comparability is easiest to audit pair by pair;
* the chance baseline is unambiguous;
* it avoids ResearchBench rows that mix genuine alternatives with irrelevant
  distractors. (Measured: on RBV-19 the gold ranked 3rd of 11 while still beating
  all 8 *screened* negatives — the two candidates above it were unscreened
  distractors. Listwise and pairwise answer different questions on the same row.)

### Both orders, or the number is confounded

Any judge that sees two candidates as "option A" and "option B" must be asked
**both ways**, with the two outcomes averaged: credit 1.0 for right both ways, 0.5
for order-dependent, 0.0 for wrong both ways.

This is not hypothetical. Measured on the single-order runs of the question-hidden
pair judge, which chose option A far more often than option B:

| slice | chose A | accuracy when gold was A | when gold was B | reported |
| --- | --- | --- | --- | --- |
| v1 | 67% | 0.951 | 0.617 | 0.785 |
| v2 official | 61% | 0.980 | 0.760 | 0.870 |
| **canonical** | **85%** | 0.983 | **0.319** | 0.686 |
| v2 widened | 61% | 0.961 | 0.745 | 0.853 |

A per-pair seeded shuffle — which is what we had — spreads that bias around but
does not remove it. It leaves the score depending on how the coin landed: on
canonical the gold fell in position A for 58 of 105 pairs, and

    0.552 * 0.983 + 0.448 * 0.319 = 0.686

reproduces the reported accuracy exactly. An always-answer-A strategy would have
scored 0.552 on that slice. Counterbalancing cancels position preference instead of
averaging over it, and reports `position_preference_chose_a` and
`order_consistency` so the confound is visible rather than latent.

The length heuristics (shortest-/longest-text-first) are deterministic and
order-free, so they are unaffected.

## 4. Secondary evaluation: controlled k > 2

Not the raw 11-way ResearchBench task — candidate quality there is uneven. Instead
`scripts/build_k_slices.py` assembles sets

    {H+, H1-, ..., H(k-1)-}

where **every** negative independently passed the frozen R2 comparability
criterion.

Two design commitments:

* **Sampling frozen before any verifier run.** Each row's screened negatives are
  put in one deterministic seeded order at build time, recorded in
  `k_slices_manifest.json` under `frozen_negative_order`.
* **Nested across k.** The set at k takes the first k-1 negatives of that frozen
  order, so k=2 ⊂ k=3 ⊂ k=4 and a row present at the largest k is present at every
  smaller one. k is then the only thing that changes within a row; independent
  per-k sampling would confound set size with which negatives were drawn.

Built (seed 20260912), after excluding 4 review-source rows:

| k | sets | rows short of k |
| --- | --- | --- |
| 2 | 62 | 0 |
| 3 | 27 | 35 |
| 4 | 18 | 44 |
| balanced panel (every k) | **18 rows** | — |

k=5 is **not** built: only 7 rows have 4 or more R2-passing negatives. That is a
limit of how much screening was done — the v2 screen stopped at its 100-pair target
after 137 of 962 rows — not of the dataset. Reaching k=5 means screening more rows,
not manufacturing negatives.

### Metrics, per k

Reported inside `by_k`, each with its own baseline:

| metric | chance | role |
| --- | --- | --- |
| top-1 (tie-aware) | 1/k | **within-k diagnostic only** |
| MRR | varies with k | **within-k diagnostic only** |
| mean gold rank | (k+1)/2 | within-k diagnostic only |
| **normalised gold rank** `1 - (rank-1)/(k-1)` | 0.5 | **principal cross-k metric** |
| **pairwise win rate** `(1/(k-1)) * sum_j 1{S(H+) > S(Hj-)}`, ties 0.5 | 0.5 | **principal cross-k metric** |

The last two are the principal cross-k metrics; top-1 and MRR are within-k
diagnostics and are never pooled.

**This is not a theoretical precaution — it changed the reading of the first nested
run.** At k=4, top-1 was **0.250, exactly chance**, while the pairwise win rate was
**0.750**: the gold ranked second on three of four rows, so it was rarely first and
almost never last. Reported as pooled top-1 this would have read "no better than
chance"; both cross-k metrics say the opposite.

## 4a. What the first nested run showed

Four rows at k=2 and k=4, nested candidates (`runs/k_sweep_report.md`):

| k | nodes | edges | median proposition words | informative | cost/instance |
| --- | --- | --- | --- | --- | --- |
| 2 | 22 | 58 | 18 | 44% | $0.30 |
| 4 | 42 | 197 | 18 | 35% | $0.62 |

The claim this supports is **not** "larger candidate sets cause proposition
degradation" — proposition length is identical at 18 words for both k, so the
degradation mechanism seen under `consequence_generate_v1` is closed. The claim is
narrower:

> **Graph growth outpaces informative-evidence growth.** Informative nodes rise in
> absolute terms (38 to 59) while total graph size rises faster (86 to 167), so the
> informative *fraction* falls from 44% to 35%.

That is a statement about the cost-effectiveness of enlarging the graph, not about
propositions getting worse.

## 5. k as a property of the method, not only of the benchmark

k changes the method's own behaviour, which makes varying it an experiment rather
than a difficulty knob. Measured on the debug runs under
`consequence_generate_v1`: informative-evidence rate was 40% at k=2 and **4%** at
k=11, because generation responded to having more alternatives by writing
increasingly conjunctive propositions that no single abstract could settle. That
finding is what motivated `consequence_generate_v2` (DECISIONS #17) — and the nested
run then showed that comparison was confounded with instance identity, and that the
proposition-length mechanism is now closed. The residual k effect is graph growth
outpacing evidence growth (§4a). See DECISIONS #24.

**A caveat on every "informative-evidence rate" in this document**: the current
assessor's `no_evidence` means "not directly investigated", not "does not bear on the
proposition" (DECISIONS #25, `docs/ASSESSOR_RUBRIC.md`). Until that construct is
settled, informativeness measures the assessor as much as the method.

So the k sweep should report, per k:

* ranking performance (normalised gold rank, pairwise win rate)
* informative-evidence rate
* number of propositions, and their token length / clause-marker count
* retrieval yield (papers shown, abstract coverage, queries needing backoff)
* graph size (nodes, edges, merges, shared nodes)
* cost and wall-clock

`scripts/graph_run_diagnostics.py` computes all of these from saved artifacts.

## 6. How to state it in the paper

> We formulate verification for arbitrary candidate sets k >= 2. Our primary
> evaluation uses pairwise comparisons to provide a controlled and interpretable
> benchmark, while additional experiments vary k to measure how verification
> quality and computational cost scale with the number of competing hypotheses.

---

## Status of each slice

| slice | k | role | usable as evidence? |
| --- | --- | --- | --- |
| `benchmark/dev/` (v1) | 11 | development | **no** — shortest-text-first scores 0.988 |
| `benchmark/v2/` | 2 | development | **no** — question-hidden judge 0.87–0.89 |
| `benchmark/v2_widened_diagnostic/` | 2 | diagnostic only | no |
| `benchmark/canonical/` | 2 | evaluation candidate | **no** — fails its own frozen style criterion |
| `benchmark/k_slices/` | 2,3,4 | scalability analysis | method scaling only, not accuracy |

Every slice is currently a development set. The evaluation benchmark does not exist
yet, and the honest blocker is that canonicalisation removed most of the style cue
but not enough of the length cue; minimal contrast pairs are the next route.
