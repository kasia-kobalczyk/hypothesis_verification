# Canonicalized evaluation benchmark — build report

**EVALUATION CANDIDATE — FAILED the frozen style diagnostics; NOT usable as an evaluation benchmark**

> This is a DERIVED benchmark. Every candidate was rewritten by a model. It is not untouched ResearchBench and must not be described as such.

Built 2026-09-11T21:16:56Z against `docs/CANONICAL_PROTOCOL.md (frozen before this build ran)`, which was frozen before this ran.

## What was done

1. inherited R1/R3/R5/R6 row screen + R4 cutoff (reused verbatim from the v2 build)
1. symmetric canonicalisation, blind to candidate role
1. semantic preservation check on every canonical claim
1. R2 pair comparability re-applied to the CANONICAL texts

Length is measured and reported, never filtered. If a length cue survives canonicalisation that is a finding about the transformation.

Never consulted: literature retrieval, Direct-RAG output, consequence-graph output, any verifier score, any artifact-diagnostic result, knowledge of which candidate is the gold, at any transformation step.

## Yield

| | |
| --- | --- |
| pairs | **105** |
| source rows | 21 |
| rows canonicalised | 21 |
| target | 100 (reached) |

Rows rejected: {'not_screened_for_validity': 31, 'row_screen': 8}

## Semantic preservation

Every canonical claim was checked against its original by a separate judge that was not told the candidate's role.

- not_preserved: 12 (5%)
- preserved: 219 (95%)

A candidate whose claim was not preserved is dropped, and every pair involving it with it. A judge failure is recorded as an error, never as a pass.

## Length, as a diagnostic (never a filter)

| | canonical |
| --- | --- |
| gold tokens (median) | 30 |
| negative tokens (median) | 30 |
| ratio negative/gold (min / median / max) | 0.6 / 1.042 / 1.778 |
| gold is the shorter text | 57.1% |

For comparison, the raw ResearchBench median ratio is **3.0**, and the gold is the shorter candidate in 98% of v1 pairs.

## Artifact diagnostics

The same three used on v1 and v2, so the numbers are comparable. Run after freezing; the protocol forbids adjusting anything in response to them.

| diagnostic | v1 | v2 | canonical |
| --- | --- | --- | --- |
| pairs | 121 | 100 | 105 |
| gold is the shorter text | 0.984 | 0.740 | 0.571 |
| **shortest-text-first** | 0.988 | 0.760 | **0.605** |
| longest-text-first | 0.012 | 0.240 | 0.395 |
| **question-hidden judge** | 0.777 | 0.910 | **0.643** |

### Against the criterion declared in the protocol

The protocol required, in advance: both length heuristics near 0.5, and the question-hidden judge substantially below the 0.870 it scores on v2. It put a number on neither bar. The research owner has since set both at **within 0.10 of chance**, which is the bar applied below.

- shortest-text-first **0.605** — off chance by 0.105: FAIL
- longest-text-first **0.395** — off chance by 0.105: FAIL
- question-hidden judge (counterbalanced) **0.643** — off chance by 0.143: FAIL

#### Where the remaining style cue sits

Each pair is judged in both orders, so a pure position-guesser scores exactly 0.500 and the accuracy splits cleanly into two populations.

| | share of pairs | accuracy on them |
| --- | --- | --- |
| judge answers the same way in both orders | 0.381 | 0.875 |
| answer flips with order (guessing) | 0.619 | 0.500 by construction |

Read that way, canonicalisation cut the *number of pairs carrying a usable text-only cue* rather than weakening the cue itself. The remaining signal is concentrated in a minority of pairs, which is a more tractable target than a diffuse one — though any rule for dropping them has to be declared before it is applied, not chosen from this table.

A FAIL here is a finding about what canonicalisation can remove, not a reason to rebuild the slice until the number improves.

> Two caveats on the criterion itself, recorded because they matter more than the verdict. (1) The protocol's bars were words, not numbers; an earlier version of this report operationalised "substantially below" as `< 0.75` *after* the result was known, which turned 0.686 into a pass. See `docs/DECISIONS.md` #16. (2) The question-hidden judge is not deterministic: the same prompt over the same 100 official v2 pairs scored 0.870 and 0.890 on two runs 43 minutes apart. Treat ~0.02 as noise.

## Worked examples

**RBC-0001-N01** (Business)

- question: How can we develop a new class of antibiotics to effectively combat carbapenem-resistant Acinetobacter baumannii (CRAB), a major global pathogen with limited treatment options?
- gold original (44 tok): Tethered macrocyclic peptide (MCP) antibiotics can block the transport of bacterial lipopolysaccharide (LPS) from the inner membrane to the outer membrane by in...
- **gold canonical**: Tethered macrocyclic peptide antibiotics inhibit the LptB2FGC complex to block LPS transport, exhibiting potent antibacterial activity against carbapenem-resistant Acinetobacter baumannii.
- negative original (167 tok): A novel class of peptidomimetic antibiotics, specifically engineered to target and disrupt the lipopolysaccharide transport (Lpt) machinery in carbapenem-resist...
- **negative canonical**: A novel class of peptidomimetic antibiotics targeting LptA and BamA disrupts cell integrity and exhibits potent antimicrobial activity against carbapenem-resistant Acinetobacter baumannii.

**RBC-0001-N02** (Business)

- question: How can we develop a new class of antibiotics to effectively combat carbapenem-resistant Acinetobacter baumannii (CRAB), a major global pathogen with limited treatment options?
- gold original (44 tok): Tethered macrocyclic peptide (MCP) antibiotics can block the transport of bacterial lipopolysaccharide (LPS) from the inner membrane to the outer membrane by in...
- **gold canonical**: Tethered macrocyclic peptide antibiotics inhibit the LptB2FGC complex to block LPS transport, exhibiting potent antibacterial activity against carbapenem-resistant Acinetobacter baumannii.
- negative original (98 tok): A novel class of peptidomimetic antibiotics will be developed by employing an optimized thanatin scaffold specifically designed through structure-activity relat...
- **negative canonical**: A novel class of peptidomimetic antibiotics targeting the Lpt machinery and silencing blaNDM and blaKPC genes effectively combats carbapenem-resistant Acinetobacter baumannii.

**RBC-0001-N03** (Business)

- question: How can we develop a new class of antibiotics to effectively combat carbapenem-resistant Acinetobacter baumannii (CRAB), a major global pathogen with limited treatment options?
- gold original (44 tok): Tethered macrocyclic peptide (MCP) antibiotics can block the transport of bacterial lipopolysaccharide (LPS) from the inner membrane to the outer membrane by in...
- **gold canonical**: Tethered macrocyclic peptide antibiotics inhibit the LptB2FGC complex to block LPS transport, exhibiting potent antibacterial activity against carbapenem-resistant Acinetobacter baumannii.
- negative original (229 tok): Designing and optimizing dual-targeting peptidomimetic antibiotics that specifically interact with both the LptA and LptC components of the lipopolysaccharide t...
- **negative canonical**: Dual-targeting peptidomimetic antibiotics that disrupt the LptA-LptC interaction in carbapenem-resistant Acinetobacter baumannii cause loss of outer membrane integrity and exhibit potent antimicrobial activity.

## Files

- `researchbench_canonical_pairs.jsonl` — the slice; canonical claims plus both originals
- `canonical_manifest.json` — gates, prompts with hashes, yield, preservation counts
- `canonical_artifact_diagnostics_counterbalanced.json` — the three diagnostics with every pair judged in BOTH orders (authoritative)
- `canonical_artifact_diagnostics.json` — the earlier single-order run, kept for provenance; its question-hidden number is confounded by position preference
- `canonical_progress.jsonl` — every canonicalisation and judgment, for audit
