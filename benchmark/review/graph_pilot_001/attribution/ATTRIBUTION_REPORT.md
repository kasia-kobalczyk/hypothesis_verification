# BENCH-GRAPH-ATTRIBUTION-001 — score attribution under reviewed labels

Deterministic accounting of the frozen eight-case graph pilot (`pilot_explanatory_001`) using the Research Director's labels for the 40 priority nodes (D045). No model, retrieval or verifier code was run beyond re-scoring the frozen graphs with the verifier's own scoring function; frozen scores reproduce exactly.

**Read the four kinds of statement separately.** §1 is observed frozen verifier behaviour. §2 uses the D045 human categories, which are *model-based Research Director review, not external expert ground truth*. §3–§5 are counterfactual arithmetic and coverage. §6 is the executor's interpretation.

Orientation throughout: **log-odds = log-score(H2) − log-score(H1)**; positive supports H2. In all four `favored` cases the later resolution favours H2 (PROJECT_STATE). Ordinal mappings are placeholders (`v0-placeholder`): signs and relative sizes carry information, absolute magnitudes do not.

## 1. Observed frozen verifier output

| case | resolution | later favours | frozen scores H1 / H2 | log-odds | top |
| --- | --- | --- | --- | --- | --- |
| eukaryogenesis_mito_timing | favored | H2 | 0.081 / 0.919 | +2.42 | H2 |
| fly_wing_constraint_vs_selection | favored | H2 | 0.423 / 0.577 | +0.31 | H2 |
| forest_fragmentation_resilience | regime_dependent | — | 0.836 / 0.164 | -1.63 | H1 |
| gcn4_med15_complex_vs_condensate | mixed | — | 0.499 / 0.501 | +0.00 | H2 |
| glnbp_induced_fit_vs_conformational_selection | favored | H2 | 0.137 / 0.863 | +1.84 | H2 |
| pfc_interhemispheric_architecture | regime_dependent | — | 0.618 / 0.382 | -0.48 | H1 |
| pfc_storage_vs_control | favored | H2 | 0.771 / 0.229 | -1.21 | H1 |
| spider_orb_web_origin | component_wise | — | 0.424 / 0.576 | +0.31 | H2 |

## 2. Influence by reviewed category

Total absolute score influence across all 78 score-moving nodes: **18.07**. Reviewed (40 nodes): 14.48 (80.1%). Unreviewed (38 nodes): 3.59 (19.9%).

| category | nodes | absolute influence | share of all influence |
| --- | --- | --- | --- |
| genuine | 4 | 1.47 | 8.1% |
| silence err | 8 | 3.66 | 20.2% |
| generic comp. | 14 | 4.67 | 25.8% |
| compatible | 8 | 2.75 | 15.2% |
| construct mism. | 3 | 0.72 | 4.0% |
| weak impl. | 3 | 1.22 | 6.8% |
| UNREVIEWED | 38 | 3.59 | 19.9% |

Signed log-odds by case and category (node count in brackets; `·` = no node):

| case | frozen | genuine | silence err | generic comp. | compatible | construct mism. | weak impl. | UNREVIEWED | reviewed coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| eukaryogenesis_mito_timing | +2.42 | · | -0.24 (1) | +2.02 (6) | · | · | +0.85 (1) | -0.20 (7) | 80% |
| fly_wing_constraint_vs_selection | +0.31 | · | +0.30 (1) | · | · | · | · | +0.01 (1) | 98% |
| forest_fragmentation_resilience | -1.63 | · | -0.41 (2) | · | -1.64 (4) | · | +0.19 (1) | +0.22 (11) | 67% |
| gcn4_med15_complex_vs_condensate | +0.00 | · | -0.19 (1) | -0.25 (3) | +0.28 (1) | · | · | +0.16 (6) | 70% |
| glnbp_induced_fit_vs_conformational_selection | +1.84 | -0.38 (2) | +1.63 (2) | +0.92 (4) | -0.19 (1) | · | · | -0.13 (2) | 96% |
| pfc_interhemispheric_architecture | -0.48 | · | · | · | -0.39 (1) | · | · | -0.09 (2) | 68% |
| pfc_storage_vs_control | -1.21 | +0.58 (2) | -0.89 (1) | · | -0.24 (1) | -0.72 (3) | · | +0.05 (4) | 91% |
| spider_orb_web_origin | +0.31 | · | · | +0.21 (1) | · | · | +0.19 (1) | -0.10 (5) | 45% |

Summed over the four `favored` cases, toward the later-favoured hypothesis: genuine +0.20, silence err +0.81, generic comp. +2.94, compatible -0.44, construct mism. -0.72, weak impl. +0.85, UNREVIEWED -0.28.

How reviewed categories moved scores (mechanical counts from verifier edges and evidence):

| category | nodes | direct edges sign-opposed | non-origin hypothesis labelled unlikely/contradicted | push toward generating hypothesis | evidence support / contradiction |
| --- | --- | --- | --- | --- | --- |
| genuine | 4 | 4 | 4 | 4 | 4 / 0 |
| silence err | 8 | 8 | 8 | 6 | 6 / 2 |
| generic comp. | 14 | 13 | 13 | 14 | 14 / 0 |
| compatible | 8 | 1 | 1 | 6 | 6 / 2 |
| construct mism. | 3 | 3 | 3 | 3 | 3 / 0 |
| weak impl. | 3 | 3 | 3 | 2 | 2 / 1 |

## 3. Counterfactual views

- **original**: frozen verifier: every node kept
- **A1 genuine + unrev.**: directive views A1 and D (identical here): reviewed genuine discriminators kept, all other reviewed nodes removed, unreviewed score-moving nodes untouched
- **A2 genuine only**: directive views A2 and C (identical here): strict. Reviewed genuine discriminators only; unreviewed score-moving nodes set aside
- **B1 errors removed**: directive view B: reviewed silence errors, construct mismatches and weak implications removed; reviewed genuine, generic and compatible kept; unreviewed untouched
- **B2 errors removed, reviewed only**: view B, strict: as B1 but unreviewed score-moving nodes set aside
- **R unreviewed only**: reference: all reviewed nodes removed; unreviewed score-moving nodes only

Each cell: log-odds, top, relation to the later resolution (`agrees` / `opposes` / `no ordering`; non-directional cases show the lean only). *Evidence zeroed* is exact and additive. The bracketed *graph deleted* value also removes routes to descendants and is shown only where it differs by more than 0.05.

| case | original | A1 genuine + unrev. | A2 genuine only | B1 errors removed | B2 errors removed, reviewed only | R unreviewed only |
| --- | --- | --- | --- | --- | --- | --- |
| eukaryogenesis_mito_timing | +2.42 H2 agrees | -0.20 H1 **opposes** [del -0.26 H1] | +0.00 tie no ordering | +1.82 H2 agrees [del +1.53 H2] | +2.02 H2 agrees | -0.20 H1 **opposes** [del -0.26 H1] |
| fly_wing_constraint_vs_selection | +0.31 H2 agrees | +0.01 H2 agrees | +0.00 tie no ordering | +0.01 H2 agrees | +0.00 tie no ordering | +0.01 H2 agrees |
| forest_fragmentation_resilience | -1.63 H1 lean | +0.22 H2 lean [del -0.47 H1] | +0.00 tie lean | -1.41 H1 lean | -1.64 H1 lean | +0.22 H2 lean [del -0.47 H1] |
| gcn4_med15_complex_vs_condensate | +0.00 H2 lean | +0.16 H2 lean [del +0.35 H2] | +0.00 tie lean | +0.19 H2 lean | +0.03 H2 lean | +0.16 H2 lean [del +0.35 H2] |
| glnbp_induced_fit_vs_conformational_selection | +1.84 H2 agrees | -0.52 H1 **opposes** [del -1.00 H1] | -0.38 H1 **opposes** | +0.21 H2 agrees | +0.35 H2 agrees | -0.13 H1 **opposes** [del -0.36 H1] |
| pfc_interhemispheric_architecture | -0.48 H1 lean | -0.09 H1 lean | +0.00 tie lean | -0.48 H1 lean | -0.39 H1 lean | -0.09 H1 lean |
| pfc_storage_vs_control | -1.21 H1 **opposes** | +0.63 H2 agrees [del +0.53 H2] | +0.58 H2 agrees | +0.39 H2 agrees | +0.33 H2 agrees | +0.05 H2 agrees |
| spider_orb_web_origin | +0.31 H2 lean | -0.10 H1 lean | +0.00 tie lean | +0.12 H2 lean | +0.21 H2 lean | -0.10 H1 lean |

Cases with **no reviewed genuine discriminator** (A2 has nothing to order on): 6 of 8 — `eukaryogenesis_mito_timing`, `fly_wing_constraint_vs_selection`, `forest_fragmentation_resilience`, `gcn4_med15_complex_vs_condensate`, `pfc_interhemispheric_architecture`, `spider_orb_web_origin`.

Where the two decompositions disagree on the top hypothesis (path-mediated effects large enough to change the ordering): `forest_fragmentation_resilience` (view A1).

## 4. Focus cases

### GlnBP (later resolution: induced fit, H2)

- frozen: +1.84 toward induced fit. Silence errors contribute +1.63, generic component facts +0.92, genuine discriminators **-0.38**, compatible -0.19, unreviewed -0.13.
- genuine discriminators only (A2): -0.38 → **H1** (opposes).
- confirmed errors removed (B1): +0.21 → H2 (agrees), carried by generic component facts (+0.92) against the genuine discriminators (-0.38).

### Eukaryogenesis (later resolution: complex host before mitochondria, H2)

- frozen: +2.42. Generic component facts +2.02, weak implication +0.85, silence error -0.24, unreviewed -0.20; no reviewed genuine discriminator.
- after removing reviewed invalid, generic and silence contributions, what remains is genuine (+0.00) plus compatible (+0.00) plus unreviewed (-0.20) = **-0.20**; A1 top **H1**.
- errors removed only (B1): +1.82 (agrees), carried by generic component facts.

### Fly-wing (later resolution: correlational selection, H2)

- frozen: +0.31; the single reviewed node is a silence error (+0.30); the only other score-moving node is unreviewed (+0.01).
- errors removed (B1): +0.01 H2; strict (B2): tie.

### PFC storage vs control (later resolution: control, H2; frozen verifier favoured storage)

- frozen: -1.21 (toward storage). Silence error -0.89, construct mismatch -0.72, compatible -0.24, genuine discriminators **+0.58**, unreviewed +0.05.
- genuine only (A2): +0.58 H2 (agrees); errors removed (B1): +0.39 H2 (agrees).

## 5. Coverage and the next review batch

| case | score-moving | reviewed | reviewed share of case influence | unreviewed influence |
| --- | --- | --- | --- | --- |
| eukaryogenesis_mito_timing | 15 | 8 | 79.5% (below packet-wide 80.1%) | 0.80 |
| fly_wing_constraint_vs_selection | 2 | 1 | 97.7% | 0.01 |
| forest_fragmentation_resilience | 18 | 7 | 67.5% (below packet-wide 80.1%) | 1.08 |
| gcn4_med15_complex_vs_condensate | 11 | 5 | 70.5% (below packet-wide 80.1%) | 0.62 |
| glnbp_induced_fit_vs_conformational_selection | 11 | 9 | 96.0% | 0.17 |
| pfc_interhemispheric_architecture | 3 | 1 | 67.7% (below packet-wide 80.1%) | 0.19 |
| pfc_storage_vs_control | 11 | 7 | 90.9% | 0.24 |
| spider_orb_web_origin | 7 | 2 | 45.4% (below packet-wide 80.1%) | 0.48 |

Recommended next human-review batch (not labelled here): the 8 unreviewed nodes in the three low-influence cases — `GP1-spider_orb_web_origin-X7`, `GP1-pfc_interhemispheric_architecture-X1`, `GP1-spider_orb_web_origin-X24`, `GP1-spider_orb_web_origin-X8`, `GP1-pfc_interhemispheric_architecture-X23`, `GP1-spider_orb_web_origin-X22`, `GP1-spider_orb_web_origin-X17`, `GP1-fly_wing_constraint_vs_selection-X19` — then the remaining 30 by influence.

## 6. Interpretation (executor; for the Research Director, not a decision)

**Every judgment below is conditional on the D045 labels being correct.** They are model-based first-pass review, and 19.9% of score influence is still unreviewed.

**1. None of the frozen pilot's agreements with the later resolution rests on a reviewed genuine discriminator.** The frozen verifier agreed in 3 of the 4 `favored` cases (eukaryogenesis_mito_timing, fly_wing_constraint_vs_selection, glnbp_induced_fit_vs_conformational_selection). Restricted to reviewed genuine discriminators (A2), 0 of those agree:

- **Eukaryogenesis** and **fly-wing** have no reviewed genuine discriminator, so A2 gives no ordering.
- **GlnBP's** two genuine discriminators point the other way (-0.38, toward conformational selection). Its frozen +1.84 toward induced fit came from silence errors (+1.63) and generic component facts (+0.92).

**2. Removing only the confirmed errors (B1) keeps the right direction in two of those cases, but on component facts, not discrimination.** Eukaryogenesis stays at +1.82 and GlnBP at +0.21; generic component facts contribute +2.02 and +0.92 respectively. Fly-wing collapses to +0.007, carried by a single unreviewed node, so its apparent success disappears.

**3. The one failure reverses under reviewed attribution.** In PFC storage vs control, the two genuine discriminators favour the later-supported control account (+0.58). One silence error (-0.89) and three construct mismatches (-0.72) outweighed them. Genuine only (A2) gives +0.58; errors removed (B1) gives +0.39.

*Relation to an earlier retraction:* the pilot report withdrew a similar claim. It rested on the LLM auditor, which had miscalled X15. D045 labels X15 a construct mismatch, not genuine; the claim now rests on X6 and X24 instead.

**4. Most cases are underdetermined once non-discriminative reviewed nodes are set aside.** 6 of 8 cases have no reviewed genuine discriminator. With unreviewed nodes left in (A1), their leanings rest entirely on unreviewed nodes. Those leanings can flip (eukaryogenesis goes to -0.20) or depend on the decomposition (forest).

**5. The dominant problem is broader than silence handling.** Shares of all score influence:

| group | share |
| --- | --- |
| reviewed silence errors | 20.2% |
| generic component facts + compatible non-discriminative propositions | **41.0%** |
| all confirmed errors (silence, construct mismatch, weak implication) | 31.0% |
| reviewed genuine discriminators | **8.1%** |

Mechanically, the categories share one pathway: the hypothesis that did not generate the proposition received `unlikely`/`strongly_contradicted`. This happened in 8 of 8 silence errors and 13 of 14 generic component facts. 14 of the 14 generic component facts carried literature support.

The reviewed categories differ in *why* that opposing label is unwarranted: the competitor is silent, or the fact is not specific to the hypothesis. That supports D045's reading of a broader discrimination/relevance failure rather than a single silence bug.

Per the directive, no fix is proposed here.

