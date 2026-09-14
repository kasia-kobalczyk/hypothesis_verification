# Milestone 2 — the consequence verifier, first working version

Status: **operational and debugged on a handful of development cases.** Not
evaluated, because no slice we have yet supports an evaluation claim.

## What was built

| spec | component | where |
| --- | --- | --- |
| §12 | graph schema: `X_v` propositions, `D_v` evidence, no separate `C` type | `src/graph/schema.py` |
| §13 | recursive generation, pooling, cross-evaluation against every hypothesis | `src/graph/generate.py` |
| §13.4 | semantic merging (lexical; `llm` mode deliberately unimplemented) | `src/graph/merge.py` |
| §15 | ordinal edge judgments, root and chain | `edge_assess_v1`, `edge_assess_chain_v1` |
| §17 | outcome-neutral proposition queries | `src/evidence/queries.py`, `proposition_query_v1` |
| §19 | joint proposition-level evidence assessment | `src/evidence/assess.py`, `evidence_assess_v1` |
| §20-22 | ordinal mappings and Bayesian propagation | `src/inference/parameters.py`, `bayes.py` |
| §26 | per-instance diagnostic reports with the full trace | `src/experiments/reports.py` |

The method runs as `--method consequence_graph`, over 11-candidate instances or
over the v2 pair slice (`--pairs`, k=2).

## The inference, stated exactly

For an observed proposition `v` with `p = P(X_v=1 | H=i)` and evidence likelihood
ratio `L_v`, marginalising `X_v` gives hypothesis `i` a contribution of

    log(p * L_v + (1 - p))

after the hypothesis-independent factor `P(D_v | X_v=0)` cancels. That step is
exact. Observed nodes are then combined as if conditionally independent given
`H`; where two observed nodes share a parent that is an approximation, and
`score_hypotheses` counts and reports those pairs per instance rather than
assuming them away (§21).

Three properties follow and are tested:

- `no_evidence` gives `L=1`, so the contribution is exactly `log(1) = 0`. Missing
  evidence moves nothing (§20, §35.5).
- A node every hypothesis predicts equally contributes equally to all of them, so
  it cannot change the ranking however strong its evidence.
- Depth appears nowhere in the arithmetic. Relabelling a node "deeper" changes
  nothing; attenuation comes only from edge probabilities (§35.2).

## What the debug runs show

Five v2 pairs (k=2) and one v1 instance (k=11), **144 propositions**, 0
retrieval failures, 0 unassessed nodes. Every number below is recomputed from
saved artifacts by `scripts/graph_run_diagnostics.py 'runs/consequence_graph_*/'`
-- no re-running, no API calls.

**The graph is sensible.** Propositions are specific and checkable, and
cross-evaluation produces genuinely differentiated predictions:
discriminativeness (spread of `P(X_v|H)` across candidates) has median 0.23,
range 0.02-0.85, and is never exactly zero.

**Evidence assessment is subtler than expected, and correct.** The clearest
example: proposition `X3` of `RBV2-0012-N00` asserted that proteomics shows
mitochondrial/autophagy markers *and no* aberrant actin disulfide bonding. The
retrieved paper shows actin disulfide bonding does occur, and the assessor
returned `contradiction` with a rationale naming exactly that clause. A
label-only reading looks like an error; it is right.

**Most propositions retrieve nothing informative.** 102 of 144 nodes came back
`no_evidence`; 42 informative. This is the regime the method is supposed to be
good in, and it is worth knowing that it is the common case rather than the
exception.

**Informative evidence is almost always corroborating, never refuting.** Pooled
label distribution over 144 assessments:

| label | n |
| --- | --- |
| `no_evidence` | 102 |
| `weak_support` | 19 |
| `support` | 17 |
| `weak_contradiction` | 3 |
| `contradiction` | 2 |
| `mixed` | 1 |

Five refutations in 144 assessments. A method whose discriminative power is
supposed to come from *ruling candidates out* currently gets almost all of its
signal from ruling them in. Whether that is a property of the domain (published
abstracts rarely state that something does not happen) or of
`evidence_assess_v1`'s thresholds is not yet separable from six instances, and it
is the first thing to look at once the ordinal mappings are calibrated.

### Finding: assessment yield collapses as the candidate count rises

> **PARTLY WITHDRAWN — read the k=11 A/B section below first.** The comparison in
> this section pits one k=11 instance against five *different* k=2 instances, so k
> varies together with instance identity and the two cannot be separated. Running the
> same k=11 instance with atomic propositions left the yield at 2.5%, which is what a
> conjunctive-proposition explanation predicts should improve. The atomicity problem
> described here is real and was worth fixing; the *causal claim about k* is not
> supported by this data. Disentangling them is what the nested k-slices in
> `docs/EVALUATION_PROTOCOL.md` §4 are for. See DECISIONS #24.

This is the sharpest effect in the debug runs and it was not anticipated.

| slice | nodes | informative | abstracts shown |
| --- | --- | --- | --- |
| k=2 (five v2 pairs) | 100 | **40%** | 6.7 / 10 |
| k=11 (one v1 instance) | 44 | **4%** | 6.2 / 10 |
| depth 1 | 63 | 30% | 6.2 / 10 |
| depth 2 | 81 | 28% | 6.9 / 10 |
| nodes with >=8 abstracts | 53 | 38% | 8.8 / 10 |
| nodes with <=4 abstracts | 22 | 27% | 2.7 / 10 |

Two candidate explanations are ruled out by the table. It is **not depth** --
depth-1 and depth-2 propositions are assessed at the same rate (30% vs 28%), so
deeper consequences are no harder to find evidence for. It is **not primarily
retrieval substrate** -- abstract availability shifts the rate by 11 points, not
by 36, and the k=11 instance had normal coverage (6.2 of 10 shown papers carried
an abstract, against 6.7 at k=2).

What is left is proposition *specificity*. `consequence_generate_v1` asks for
consequences that distinguish the focal claim from the alternatives. With two
candidates a single mechanism suffices. With eleven, the model writes conjunctive
propositions that pin down one candidate against ten others -- RBV-19's `X1` is a
five-clause claim about IL-10, STAT3, sphingosine kinase, SCD2 *and* a STAT3
inhibitor control -- and no abstract speaks to all clauses at once, so the
assessor correctly returns `no_evidence`. The query was fine and outcome-neutral
(`IL-10 STAT3 phosphorylation sphingosine kinase macrophages`); 20 eligible
papers came back; none addressed the conjunction.

This couples directly to the ranking. With 2 of 44 nodes informative, 42 nodes
contribute exactly zero to every candidate by construction, and RBV-19's
posterior is nearly flat: top four scores 0.106, 0.100, 0.100, 0.094. The graph
was discriminative *a priori* -- spread of `P(X_v|H)` across the 11 candidates
has median 0.50 and max 0.85, and no node is degenerate -- so the loss is
entirely at the evidence step, not in graph construction.

**The implication for the method is a real one, not a bug to patch.** Discriminativeness
and assessability pull against each other: the more sharply a proposition
separates candidates, the less likely any single abstract settles it. The
principled fix is to decompose -- generate atomic, separately-checkable
propositions and let *cross-evaluation* supply the discrimination, rather than
asking one proposition to do both jobs. That is a change to the generation
prompt, so it is recorded as a decision (DECISIONS #17) rather than made here.

> **Outcome, measured after this was written.** The decomposition was implemented as
> `consequence_generate_v2` and it worked as a change to proposition shape -- length
> halved, conjunctions eliminated -- and raised the yield at k=2 from 40% to 49%. It
> did *not* raise the yield on the k=11 instance. The trade-off described above is
> real and visible (per-node discriminativeness halved); the prediction that it was
> what suppressed yield at k=11 was wrong.

### The v1 multi-candidate path works mechanically

`RBV-19`, 11 candidates, `--set graph.max_nodes=44`:

| | |
| --- | --- |
| nodes / edges | 44 / 495 |
| root edges | 484 = 44 x 11 (every node assessed against every candidate) |
| chain edges | 11 |
| depth | 33 nodes at depth 1, 11 at depth 2 |
| merges / shared nodes | 0 / 0 |
| retrieval | 88 queries, 90 searches, 2 needing backoff, 440 papers shown, 20 excluded post-cutoff |
| failures | 0 retrieval, 0 assessment, 0 unobserved |
| cost | $1.01 |

`pair_accuracy` is 1.0 while `gold_rank` is 3.0 -- gold outranked all eight
*screened* negatives, and the two candidates above it are unscreened ResearchBench
distractors that never enter the frozen pair subset. That is the intended
behaviour of the pair metric, and it is also a reminder that listwise numbers on
these instances answer a different question from the pairwise ones.

### Finding: node merging never fires, and lowering the threshold will not fix it

Across 144 propositions, **zero** merges and **zero** shared nodes.

An earlier version of this section reported a maximum cross-hypothesis similarity
of 0.460 and concluded that even a threshold of 0.60 would merge nothing. **That
was wrong, and the cause was a bug in `text_similarity` rather than anything about
the propositions** — see `DECISIONS #19`. `difflib.SequenceMatcher` was being used
with its `autojunk` heuristic on, which discards common characters in sequences
over 200 characters, and keys that decision off its second argument only, making
the function asymmetric. Corrected numbers, over the same runs, pairs taken within
an instance (merging is a within-instance operation):

| proposition pairs | n | max | p99 | p95 | median | ≥0.60 | ≥0.50 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| from *different* hypotheses | 1,323 | **0.677** | 0.554 | 0.478 | 0.320 | 3 | 44 |
| from the *same* hypothesis | 573 | 0.821 | 0.747 | 0.577 | 0.392 | 22 | 86 |

So the honest statement is narrower: at the frozen threshold of **0.82** nothing
merges, because the cross-hypothesis maximum is 0.677 — but a threshold of 0.60
*would* merge three cross-hypothesis pairs, and 0.50 would merge 44. Merging is
inert at the current setting, not intrinsically inert.

The suspected cause in the method still stands independently:
`consequence_generate_v1` instructs the model to propose consequences that
*distinguish* the focal claim from the alternatives, which suppresses the shared
consequences §35.9 says to expect. That is what `consequence_generate_v2` changes,
and the corrected similarity numbers above are the baseline it is measured
against.

The function merging was meant to serve is, however, being served elsewhere.
Cross-evaluation rates every node against every candidate, so a proposition both
candidates predict gets similar `P(X_v|H)` under each and low discriminativeness,
and is inert in the ranking by construction. Whether node-level merging is needed
*as well* is now a real research question rather than a missing feature.

**This needs a decision before evaluation:** either accept that shared nodes
arise through cross-evaluation rather than merging, or change the generation
prompt so shared consequences are generated in the first place. The threshold stays
at 0.82 for now, by instruction; the point of `consequence_generate_v2` is to see
whether near-equivalent propositions appear on their own once generation stops
being asked to make each one distinctive.

### Finding: the node budget must scale with the candidate count

`graph.max_nodes: 20` was written for the paper's three-hypothesis figure. With
11 candidates and `max_children_per_node: 3`, depth 1 alone wants 33 nodes, so
the budget truncates generation before several candidates are expanded at all —
and a candidate with no propositions of its own is judged only through other
candidates' nodes. The v1 debug run used `--set graph.max_nodes=44`. A budget
expressed per candidate would be less error-prone than a global cap.

### Finding: a review article as the source makes the task trivially easy

`RBV2-0012-N00`'s source is a *Trends in Cell Biology* review. Its "gold
hypothesis" therefore summarises work already published before the cutoff, and
retrieval duly returned the primary paper that established the phenomenon. The
R3 criterion ("presented as supported by the source study") does not exclude
reviews. For a verification benchmark this matters: a review source means the
answer is in the pre-cutoff literature by construction.

## `consequence_generate_v2`: atomic, non-contrastive generation

The change decided in DECISIONS #17: generate for **atomicity and assessability**,
and let cross-evaluation supply the discrimination. Concretely, v2 asks for one
relation/mechanism/measurement per proposition, forbids conjunctions and control
clauses, and **is not shown the competing candidates at all** — the template does
not declare `$alternatives`, so `_generate_children` cannot pass them whatever the
prose says. `consequence_generate_v1` is untouched and still selectable.

### A/B at k=2: same five instances, same node budget, only the prompt changed

| | v1 prompt | v2 prompt |
| --- | --- | --- |
| nodes | 100 | 91 |
| **informative evidence** | **40%** | **49%** |
| informative, excluding the over-merged instance | 42.5% (80 nodes) | **55.1%** (78 nodes) |
| median proposition tokens | 52 | **25** |
| clause markers per proposition | 1.44 | **0.08** |
| merges | 0 | 9 |
| per-node discriminativeness (median) | 0.235 | **0.123** |
| nodes with zero discriminativeness | 0 / 100 | 2 / 91 |
| gold ranked first | 3 / 5 | 4 / 5 |
| mean posterior entropy ratio | 0.724 | 0.964 |

Per instance, informative-evidence rate and gold rank:

| instance | v1 | v2 |
| --- | --- | --- |
| RBV2-0005-N07 | 20%, rank 2 | **47%, rank 1** |
| RBV2-0012-N00 | 60%, rank 1 | 63%, rank 2 |
| RBV2-0018-N05 | 25%, rank 2 | **50%, rank 1** |
| RBV2-0034-N04 | 65%, rank 1 | 60%, rank 1 |
| RBV2-0038-N04 | 30%, rank 1 | 15%, rank 1 (7 of 20 nodes merged away) |

**Atomicity worked, and it is not a subtle effect.** Proposition length halved and
conjunction markers went from 1.44 per proposition to 0.08 — v2 propositions are
single claims. Assessment yield rose with it, which is the causal chain DECISIONS
#17 predicted: shorter, single-clause propositions are ones an abstract can actually
settle.

**The cost is per-node discrimination, exactly as expected.** Median
discriminativeness halved, 0.235 → 0.123, and two nodes are now degenerate (zero
spread across candidates) where v1 had none. This is the designed trade: a
proposition that does not try to separate the candidates on its own is less
individually discriminative. The open question is whether *aggregate* discrimination
survives — more informative nodes each carrying less signal. On five instances the
two effects point in opposite directions: gold ranked first more often (4/5 vs 3/5),
but the posterior is flatter (entropy ratio 0.964 vs 0.724). Five instances cannot
settle that, and accuracy on this slice is not evidence anyway.

### A/B at k=11: atomicity did NOT raise the yield, and my earlier explanation was confounded

`RBV-19`, same instance, same 11 candidates, node budget matched:

| | v1 prompt | v2 prompt |
| --- | --- | --- |
| nodes | 44 | 40 |
| **informative evidence** | 2 (4.5%) | **1 (2.5%)** |
| median proposition tokens | 54 | **18** |
| clause markers | 2.05 | **0.07** |
| cross-hypothesis max similarity | 0.677 | **0.803** |
| merges / shared nodes | 0 / 0 | 4 / **1** |
| gold rank | 3 / 11 | 6 / 11 |

Atomicity landed exactly as it did at k=2 — propositions went from 54 tokens to 18,
clause markers from 2.05 to 0.07 — and the evidence yield **did not improve**. It
went from 2 informative nodes to 1.

**So the explanation I gave in DECISIONS #17 does not survive its own test, and the
comparison behind it was confounded.** Both k=11 data points are the *same instance*
(`RBV-19`); the five k=2 data points are five *different* instances. "Informative
rate falls from 40% at k=2 to 4% at k=11" was therefore a comparison of one instance
against five others, with k and instance identity varying together. The conjunctive
propositions were real and worth fixing — they are fixed — but they were not what was
suppressing yield on this instance.

**What is actually suppressing it.** The v2 propositions on `RBV-19` are short and
checkable ("IL-10 increases sphingosine kinase activity in macrophages"), the queries
are clean and outcome-neutral ("IL-10 sphingosine kinase phosphorylation"), and
retrieval returns topically adjacent work — papers on sphingosine kinase
phosphorylation, on SCD2, on IL-10 in macrophages. The assessor then returns
`no_evidence` with the same rationale every time: *"None of the retrieved literature
**directly** investigates…"*

It is right about the literature. `RBV-19`'s cutoff is 2023-05-07 and its subject is
IL-10-driven sphingolipid metabolism in macrophages — a mechanism that was novel,
which is why the source paper was published. There is no pre-cutoff paper that
addresses the proposition head-on.

**That is the regime this whole method exists for**, and it exposes a mismatch:
`evidence_assess_v1` requires literature that *directly* addresses the proposition,
which excludes precisely the indirect, adjacent evidence the consequence graph is
built to accumulate. Four separate rationales on this instance turn down papers they
describe as related but not direct.

Per instruction the assessment prompt was left alone until atomicity was fixed. It is
fixed, and this is the re-measurement: **assessor strictness, not proposition shape,
is the binding constraint on novel-mechanism instances.** Recorded as DECISIONS #24.

**The one clear win at k=11 is the shared-consequence behaviour.** Cross-hypothesis
proposition similarity rose from 0.677 to **0.803**, and the first shared node
appeared. Different candidates now independently generate the same consequence —
three of the four merges on this instance are genuine paraphrase duplicates ("IL-10
increases sphingosine kinase activity" vs "IL-10 treatment increases sphingosine
kinase activity"), unlike the entity-swap failures at k=2. That is §35.9 behaviour,
and it only appeared once generation stopped being asked to be distinctive.

### The clean k=2 comparison: merging off, budgets identical

With `semantic_merge_mode: none`, both arms carry **exactly 100 nodes** over the same
five instances, and the v1 arm never merged anyway — so this is the first
uncontaminated version of the headline comparison.

| arm | nodes | informative | merges | gold first | per-node discriminativeness (median) |
| --- | --- | --- | --- | --- | --- |
| v1 prompt, merging on | 100 | 40 (40.0%) | 0 | 3/5 | 0.235 |
| v2 prompt, merging on | 91 | 45 (49.5%) | 7 | 4/5 | 0.123 |
| **v2 prompt, merging OFF** | **100** | **56 (56.0%)** | 0 | 4/5 | 0.123 |

Per instance:

| instance | v1 (merge on) | v2 (merge OFF) |
| --- | --- | --- |
| RBV2-0005-N07 | 4/20 (20%), rank 2 | **12/20 (60%)**, rank 2 |
| RBV2-0012-N00 | 12/20 (60%), rank 1 | 14/20 (70%), rank 1 |
| RBV2-0018-N05 | 5/20 (25%), rank 2 | **12/20 (60%)**, rank 1 |
| RBV2-0034-N04 | 13/20 (65%), rank 1 | 16/20 (80%), rank 1 |
| RBV2-0038-N04 | 6/20 (30%), rank 1 | 2/20 (10%), rank 1 |

**Merging was destroying evidence, not just distinctions.** The merged v2 arm scored
49.5%; with merging off the same prompt on the same instances scores **56.0%**.
Collapsing a node removes its evidence along with it, so the earlier estimate
understated the prompt change by about six points. The clean effect is **40.0% →
56.0%**.

`RBV2-0038-N04` moved the other way (30% → 10%) and is the one instance where the
merged arm had 7 merges. Five instances, so this is variance, not a counter-finding —
recorded because it is the only arm-crossing case.

> **The caveat that matters more than the number.** "Informative evidence" here means
> *what `evidence_assess_v1` counts as informative*, and that assessor's `no_evidence`
> has been measured to mean "no retrieved paper directly investigates this" rather than
> "the literature does not bear on this" (DECISIONS #25, #26). So 40% → 56% is a real,
> cleanly measured change in a quantity whose **construct is under review**. It should
> not be read as method quality until the assessor gate in
> `docs/ASSESSOR_RUBRIC.md` is passed. Gold-rank figures on five development
> instances are not evidence of anything at all.

### The finding that blocks the next step: merging is now actively harmful

Merging fired 9 times, and **8 of the 9 collapsed scientifically distinct
propositions** — "Autophagy is activated…" into "Necroptosis is activated…" at
similarity **0.944**, G6PD into IDH, and *opposite* directional NADPH/NADP+ claims
about liver and heart into one generic node. Full table in DECISIONS #23.

The cause is the atomicity itself: atomic propositions share a syntactic template
and differ only in the entity, tissue or direction, which is a small fraction of the
characters and all of the science. No threshold fixes it — the worst case is 0.944,
and a threshold above that merges nothing, including the single genuine duplicate at
0.882.

Recorded as a strict-xfail test so it flips to a failure when the matcher improves.
**Recommendation: `semantic_merge_mode: none` while generation is atomic.**
Cross-evaluation already renders propositions that every candidate predicts inert, so
lexical merging is buying redundancy removal at the price of real distinctions, at a
rate of one good merge in nine.

## The nested k sweep: k is a real but modest effect, once the instance is held fixed

Four rows from the balanced panel, run at k=2 and k=4 with **the same rows and nested
candidates** — the k=2 negative is also present at k=4, so nothing changes but the size
of the candidate set. This is the experiment that disentangles k from instance identity.
Full tables in `runs/k_sweep_report.md`.

| k | nodes | edges | median proposition words | informative evidence | queries | eligible papers | merges/instance | cost/instance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 22 | 58 | 18 | **44%** | 43 | 215 | 1.8 | $0.30 |
| 4 | 42 | 197 | 18 | **35%** | 84 | 418 | 4.5 | $0.62 |

Per row, gold rank and yield:

| row | k=2 | k=4 |
| --- | --- | --- |
| K-0038 | rank 1/2, 6/18 informative | rank 2/4, 9/41 |
| K-0095 | rank 1/2, 10/20 | rank 1/4, 8/33 |
| K-0108 | rank 2/2, 8/24 | rank 2/4, 20/45 |
| K-0113 | rank 2/2, 14/24 | rank 2/4, 22/48 |

**There is a genuine k effect on assessment yield, and it is about nine points from
k=2 to k=4 — not the 36 points the confounded comparison suggested.** Informative
nodes rise in absolute terms (38 → 59) but node count rises faster (86 → 167), so the
rate falls. That is the honest size of the effect.

**Proposition length is flat at 18 words across both k.** Under `consequence_generate_v1`
the model answered a larger candidate set by writing longer, more conjunctive
propositions; under v2 it does not — the median is identical at k=2 and k=4. So the
mechanism blamed in DECISIONS #17 is genuinely closed, even though closing it did not
recover the yield on `RBV-19`.

### The metric design earns its keep here

At k=4: **top-1 is 0.250, exactly chance — while the pairwise win rate is 0.750.** The
gold is rarely first but almost never last. A single pooled top-1 would have reported
this as "no better than chance"; the pairwise win rate and normalised gold rank both
say the opposite, and both have a chance level of 0.5 at every k. This is precisely the
case `docs/EVALUATION_PROTOCOL.md` §4 was written for.

### Cost scales as predicted, and so does the merge damage

Nodes roughly double (22 → 42), edges more than triple (58 → 197, since cross-evaluation
is nodes × k), cost doubles ($0.30 → $0.62). Retrieval scales with nodes alone.

Merges per instance rise from 1.8 to **4.5** — 7 merges at k=2 against 18 at k=4 over the
same four rows. Given that 8 of 9 merges in the k=2 A/B were scientifically wrong
(DECISIONS #23), **the merge defect gets worse with k**, which makes it a blocker for the
scalability analysis rather than a side issue.

> Caveats on these numbers: four rows, a development slice, uncalibrated ordinal
> mappings, and every graph carries corrupted nodes from lexical merging. The scaling
> columns (graph size, retrieval, cost, proposition length) are trustworthy; the ranking
> columns are not evidence about the method's accuracy. Note also that `pair_accuracy`
> is `None` in these two runs — the fix that derives it for `kind: k_sets` landed after
> they started. At k=2 the pairwise win rate is the same quantity.

## Cost and runtime

| | k=2, 20 nodes | k=11, 44 nodes |
| --- | --- | --- |
| cost per instance | ~$0.27 | $1.01 |
| model calls | ~60 | ~140 |
| searches | ~40 | 90 |
| wall clock | 5-8 min | ~25 min |

Retrieval dominates wall-clock; cost scales roughly with `nodes x candidates`
because cross-evaluation is one call per node against all candidates, while
retrieval scales with nodes alone. Total Milestone 2 debug spend: **$2.42** across 564 model calls (four run directories).

## What is deliberately still open

- `graph.merge_threshold` (§14) — now known to be inert; see above.
- `inference.multi_parent_rule` and `parent_false_baseline` (§22) — all three
  rules implemented, none validated. Both remain `TODO(research)` in config.
- Calibration (§23) is still not done, by instruction. The ordinal mappings are
  placeholders, so the absolute posteriors mean little; the ordering does the work.
- `semantic_merge_mode: llm` raises `NotImplementedError` on purpose: what counts
  as "equivalent" is a research decision.
- Proposition granularity (the yield/discriminativeness tension above) — recorded
  as DECISIONS #17, not silently changed.
- The evidence scale's refuting half is barely exercised (5 of 144 assessments).
  Whether that is the domain or the prompt needs more than six instances.

## What must not be read from these runs

Gold ranked first in 2 of the 4 v2 debug pairs, and `pair_accuracy` was 1.0 on
the single v1 instance. **Those numbers are meaningless as evidence.** The slices
are development sets, the ordinal mappings are uncalibrated, and five instances is
not a sample. The runs establish that the pipeline works, that its parts behave as
specified, and — usefully — where it currently loses its signal. Nothing else.
