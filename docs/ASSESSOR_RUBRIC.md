# Evidence-assessment rubric — what counts as evidence bearing on a proposition

> **FROZEN 2026-09-12T12:05:00Z** — sha256/16 `5d8465ae0088c1ee`.
> The construct below is fixed and must **not** be tuned against validation results.
> If it changes, the freeze stamp changes and every validation run against the old
> stamp is void. `scripts/validate_assessor.py` records the stamp it ran under and
> refuses to compare runs made under different ones.

**Status: PROPOSAL. Not wired into any config.** `evidence_assess_v1` is unchanged
and remains the running assessor. This document defines the construct; the labelled
seed set in `benchmark/assessor/` is the instrument for checking that a prompt
actually implements it. Both need the research owner's sign-off before any prompt
change or large sweep.

---

## Why this document exists

The measured problem, over **528 assessments** from the consequence-graph debug runs:

| | n | share of `no_evidence` |
| --- | --- | --- |
| `no_evidence` verdicts | 343 | — |
| …whose rationale invokes *directness* | 340 | **99%** |
| …saying the literature "does not **directly**" address the proposition | 331 | 97% |
| …that **concede related work was retrieved** before declining it | 280 | 82% |

So `no_evidence` in the current system does not mean *"the retrieved literature does
not bear on this proposition."* It means *"no retrieved paper directly investigates
this proposition."* Those are different constructs, and the method is built on the
second one: a consequence graph exists precisely to accumulate **indirect** evidence
about claims nobody has tested head-on.

`evidence_assess_v1` never states which construct it wants. It lists "how direct the
reported measurements are" as one consideration among several and leaves
"bear on the proposition" undefined; the model resolves that ambiguity
conservatively and consistently. This is under-specification in the prompt, not
misbehaviour by the model.

The risk of simply loosening it is manufacturing signal from topical adjacency,
which would be worse than the current conservatism. The rubric below is an attempt
to widen what counts **without** letting topic overlap become evidence.

---

## Two orthogonal axes

The judgment factorises, and keeping the axes separate is conceptually load-bearing:

    direction  in {supports, contradicts, neutral/no evidence}
    directness in {direct, indirect}

**How much weight indirect evidence deserves is a later, separate decision.** It must
not be baked into the label taxonomy — which is why there is no `indirect_support`
label. The label vocabulary carries direction and strength only; `evidence_directness`
is its own field; and the weighting lives in one calibratable number in
`configs/ordinal_mappings.yaml`.

## The quantity being judged

For proposition `X` and the retrieved body of literature `D`:

> Does `D` change the probability that `X` is true, and in which direction?

Not "does `D` study `X`". Not "is `D` about the same topic as `X`".

## The three-way judgment

**DIRECT** — the record explicitly tests, measures, reports, or states the
proposition or its negation.

**INDIRECT** — the record does not test the proposition itself, but **establishes a
specific intermediate fact** that changes belief in the proposition through a
**named mechanistic, causal, logical, or quantitative link**.

**NO EVIDENCE** — no such proposition-specific link can be stated from the record.

The load-bearing phrase is *specific intermediate fact*. An indirect judgment is a
claim that the record established some concrete `F`, and that `F` bears on `X`. If
`F` cannot be named, there is no indirect evidence — there is a topic in common.

### The forms an admissible link usually takes

A taxonomy of the links seen in practice, subordinate to the definition above, not a
substitute for it. A case fitting one of these labels still fails unless a specific
intermediate fact is named.

| form | the intermediate fact |
| --- | --- |
| `adjacent_system` | the same relation holds in a different tissue, organism, cell type or material |
| `mechanism_component` | a necessary step of the mechanism `X` asserts is established, or ruled out |
| `upstream_downstream` | the immediate cause, or immediate effect, that `X`'s relation would produce |
| `related_entity` | the relation holds for an entity of the same class, with a reason the substitution is sound |
| `quantitative_precondition` | a magnitude or threshold that makes `X`'s asserted magnitude more or less plausible |

## The discipline that keeps this honest

1. **State the link or lose the claim.** An indirect judgment must carry a
   one-sentence `inference_link` naming the record. **No link stated ⇒
   `no_evidence`.** Machine-checkable, and it is the whole safeguard: if the chain
   cannot be written down, it is not evidence, it is association.

2. **The minimal chain must be explicit and self-contained.** Every indirect
   judgment must also emit

   ```
   paper finding  ->  intermediate fact  ->  target proposition
   ```

   as three separate strings, plus `requires_unsupported_facts`. **If the chain
   cannot be completed without adding a fact that neither the record nor the
   proposition supplies, the case stays `no_evidence`.** This is what makes
   "indirect" auditable rather than rhetorical: a reader can check each arrow
   against the abstract. It is also cheap to audit in bulk, which is the point.

3. **`no_evidence` keeps a log-likelihood-ratio of exactly 0** (§35.5). Widening
   what counts as evidence must not weaken what `no_evidence` means.

4. **Absence is still never contradiction.**

5. **`proposition_unassessable` is an upstream quality signal, not an evidence
   verdict.** A proposition that cannot be checked as written is a *generation*
   defect. "Retrieval found nothing that bears on this" and "this proposition was
   underspecified" imply completely different fixes — corpus/retrieval work versus
   the generation prompt — so they are counted on separate channels and never share
   a label. The assessor is merely the place with both the proposition and the
   literature in view, so it is where the flag is raised; it is routed to generation
   diagnostics, not to the evidence tally.

## Worked cases, from real runs

These are the cases the rubric was written against. **The proposed labels are mine,
not adjudicated** — they are in `benchmark/assessor/labelset_candidates.jsonl` with
`labelled_by: "proposed-unreviewed"` and need the research owner's sign-off before
they are used to judge any prompt.

### A false negative the rubric would catch

`K-0038-K4::X45` — *"NADPH concentrations are higher in fetal tissues from diabetic
pregnancies at mid-gestation than in those from non-diabetic pregnancies."*

Retrieved: *"Fetal chronic hypoxia and oxidative stress in diabetic pregnancy"* —
chronic hypoxia and hyperglycaemia increase oxidative stress and decrease antioxidant
enzyme activity.

Current label: `no_evidence` ("None of the retrieved studies directly measure…").

Proposed: **`weak_contradiction`, indirect, `mechanism_component`.** Link: *increased
fetal oxidative stress with reduced antioxidant capacity implies greater NADPH
consumption for glutathione regeneration, which argues against elevated NADPH.* The
evidence points **against** the proposition — exactly the refuting signal the method
is short of (5 refutations in 144 early assessments), and it is currently discarded.

### A true negative the rubric must keep

`K-0038-K2::X1` — *"Fetuses from diabetic pregnancies at mid-gestation exhibit
altered NADPH/NADP+ ratios…"*, retrieved against a paper cloning mouse
20α-hydroxysteroid dehydrogenase cDNA and localising its mRNA.

Proposed: **`no_evidence`, agrees with current.** The enzyme is NADPH-dependent, so
there is topical adjacency — and that is the point: adjacency is not a link. Nothing
in an mRNA-localisation study changes the probability of a fetal redox ratio.

`K-0113-K4::X19` — *"Neutral-atom quantum processors controlled by deep Q-networks
exhibit longer average qubit coherence times…"* against papers on neutral-atom
processors used for graph machine learning and financial risk. Same shape, same
verdict: shared apparatus, no bearing.

### A generation defect currently hidden inside `no_evidence`

`K-0095-K4::X34` — *"KRAS-mutant PDAC cells with **specific genetic alterations
identified by CRISPR-Cas9 screening** exhibit reduced sensitivity to Lonafarnib."*

The alterations are never named, so no literature could settle it. Proposed:
`no_evidence` **plus `proposition_unassessable: true`**. Today this is recorded
identically to a genuine retrieval failure, which means the generation prompt never
gets the feedback.

---

## Adjudication protocol — frozen before any case is adjudicated

Declared in advance, because this project has already been bitten once by an
operationalisation chosen after the result was known (DECISIONS #16).

**Blind.** Judges see the proposition and the retrieved abstracts. They do **not**
see `evidence_assess_v1`'s label or rationale, and they do not see each other's
judgments. `scripts/build_adjudication_packet.py` strips those fields; the key
linking a packet back to the run artifacts is held in a separate file.

**Two independent judgments per case**, disagreements resolved in a third pass
against this rubric — not by averaging, and not by whoever labelled second
deferring to the first.

**The six existing `proposed-unreviewed` labels are seed examples only.** They
illustrate the rubric; they do not determine it, they are excluded from the
agreement statistics, and they are re-adjudicated blind like everything else.

### The primary question the adjudication answers

Not "what is the right label for case 12". It is:

> **Can two people reliably tell *indirect but evidential* from *merely related*?**

If they cannot, the `indirect` category is too subjective to calibrate safely and
the honest conclusion is that the method cannot use indirect evidence in a
principled way — a finding worth having before spending on a sweep, not after.

So the headline statistic of the adjudication is **inter-judge agreement restricted
to the boundary**: cases where at least one judge said `indirect` or `no_evidence`,
excluding the easy `direct` cases that inflate a raw agreement number.
`scripts/adjudication_agreement.py` reports it as `boundary_agreement`, alongside
Cohen's kappa on the three-way judgment and on direction.

### The acceptance gate for `evidence_assess_v2` — pre-registered

v2 replaces v1 only if **all three** hold on the adjudicated set:

1. **The boundary is learnable.** Inter-judge `boundary_agreement` is high enough
   that the category is real. Threshold to be set by the research owner **before**
   adjudication begins, and recorded in `benchmark/assessor/acceptance_gate.json`.
   If this fails, the other two are not evaluated — the construct has failed, and no
   prompt can fix it.
2. **Direction agreement with the adjudicated labels is materially better than v1**,
   on the same cases.
3. **The gain in informative rate is not driven by cases the judges call merely
   related.** Concretely, of the cases v2 promotes out of `no_evidence`, the share
   the judges also call evidential must clear a pre-set bar. A prompt that promotes
   many cases and is right about few of them has manufactured signal, however good
   its aggregate informative rate looks.

`scripts/assessor_agreement.py --gate` evaluates all three and prints PASS/FAIL per
criterion. Thresholds come from the gate file and the harness refuses to invent
them.

**Until this gate passes, no evidence weight is calibrated**, `directness_factor.indirect`
stays `TODO(research)`, and no large sweep is run.

## How to check a prompt against this rubric

`scripts/assessor_agreement.py` replays labelled cases through any assessor prompt
and reports agreement, without touching retrieval:

```bash
python3 scripts/assessor_agreement.py --prompt evidence_assess_v1
python3 scripts/assessor_agreement.py --prompt evidence_assess_v2   # the proposal
```

It reports exact-label agreement, direction agreement (support / none / contradict —
the distinction that actually moves the ranking), the informative-vs-`no_evidence`
confusion matrix, and for indirect judgments whether a link was stated. **A prompt
that raises the informative rate without raising direction agreement is
manufacturing signal, and the harness is designed to make that visible rather than
flattering.**

## What must be settled before any large sweep

1. Sign-off on the construct above, or a correction to it.
2. Adjudication of the seed labels — mine are a starting point, not ground truth.
3. A value for `directness_factor.indirect`, calibrated rather than guessed. Until
   then it stays `TODO(research)` and indirect evidence cannot be scored.
4. Agreement measured for v1 and for any candidate v2, on the signed-off labels.

Until those are done, an "informative-evidence rate" is a measurement of the current
assessor's idiosyncrasy, not of method quality.

---

## Validation without domain experts

No domain experts are available to label these cases. That rules out establishing
that `INDIRECT` matches expert judgment. It does **not** rule out establishing
something narrower and still useful: that the category is **operationally coherent,
reproducible across independent assessors, grounded in the supplied text, and not
manufacturing signal**.

The rubric above is **frozen** (see the banner) and is not tuned against any of the
results below. If it changes, every validation run against the old freeze stamp is
void.

### Two independent blinded assessors

`assessor_judge_a_v1` and `assessor_judge_b_v1` share no prompt text and reason in
different orders:

* **A** decides the category first from the definitions, then justifies it.
* **B** never sees the category names at all. It is walked through five steps —
  what does the record state, what does the proposition assert, is there a link,
  does the link need an outside fact, and only then which way the evidence points —
  and its answers are mapped onto the construct afterwards by
  `scripts/validate_assessor.py`. It cannot anchor on the label vocabulary because
  it is never shown it.

Neither sees the other's output, nor `evidence_assess_v1`'s.

> **Limitation, stated plainly.** Only one model deployment is available
> (`gpt-4.1-kasia`), so the two judges differ in prompt and scaffold but **share a
> model**. Same-model agreement has correlated errors and is materially weaker
> evidence than cross-model agreement. This is why the grounding and adversarial
> criteria carry the weight rather than agreement alone, and why the eventual claim
> must say *independent-prompt* agreement unless a second model is obtained.

### Grounding: the check that needs no expert

Every `DIRECT` or `INDIRECT` judgment must quote a `supporting_span` **copied
verbatim from the supplied abstract**. It is checked mechanically by substring
match (whitespace- and case-normalised only). A span that cannot be found does not
count as evidence, whatever the judgment claims.

This reframes the task in a way that removes the need for domain knowledge: the
judge is not being asked whether a biomedical claim is true in the world, but
whether **this supplied record states the intermediate fact it is being credited
with**. That is answerable from the text.

Several components of the construct turn out to be observable from the text alone,
and the gate is built around exactly these:

* Does the record state the fact `F`?  → verbatim span check
* Is `F` explicitly named?  → `intermediate_fact` non-null
* Did the assessor introduce an unsupported bridge?  → `requires_unsupported_facts`
* Does the direction reverse when the proposition is negated?  → negation control
* Does the judgment disappear when the evidential sentence is removed?  → span-removal control

The one part that genuinely needs an expert — whether the mechanistic chain is
*scientifically* legitimate — is the part we are explicitly not claiming.

### Adversarial controls

| condition | construction | expected |
| --- | --- | --- |
| `mismatched` | the proposition paired with an unrelated record from a distant case | collapse to `NO_EVIDENCE` |
| `swapped` | the proposition paired with a record that is genuinely informative *for a different proposition* | collapse to `NO_EVIDENCE` — a harder negative than random |
| `negated` | the proposition logically negated (`"It is NOT the case that: …"`), own record | **direction flips**; informativeness persisting while direction does not move means the claim is not being read |
| `span_removed` | the sentence carrying the cited span deleted from the abstract | an indirect judgment should disappear |

Negation is a model-free prefix rather than a learned rewrite, because control
generation must not depend on the thing under test. It is clumsy prose and exact
about truth conditions, which is what the direction check needs.

`P(informative | mismatched abstract)` is the single strongest check available
here. If the assessor calls 20–30% of mismatched abstracts indirect evidence, the
rubric is too permissive regardless of how well the judges agree with each other.

### One thing the validation numbers are not

The judges see **one record per case**; the pipeline assessor sees the whole
retrieved body (ten records). So the informative rate in the validation run is not
comparable to the pipeline's node-level informative rate, and neither should be
quoted against the other. The validation asks whether a *single record* is being
read correctly, which is the right granularity for grounding and for the
adversarial controls — a mismatched-abstract control only means something if the
abstract is the whole input.

### What passing means, and the wording for the paper

Passing makes the assessor **provisionally validated**, not settled. The statistics
are *reproducibility*, and they are renamed accordingly throughout — there is no
"human agreement" number anywhere, because there are no human labels.

Do **not** write:

> The assessor accurately distinguishes indirect evidence from merely related
> literature.

Write instead:

> We operationalize indirect evidence using an explicit intermediate-fact chain and
> validate the assessor through independent-model agreement, source-grounding
> checks, and adversarial controls.

Weaker, and precise. With same-model judges, "independent-model" must be downgraded
to "independent-prompt".
