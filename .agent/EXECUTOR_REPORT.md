TASK_ID: BENCH-GRAPH-ATTRIBUTION-001
STATUS: COMPLETED

SUMMARY:
All 40 D045 labels were encoded into the review packet by mechanical transcription. A test re-parses D045 from `.agent/DECISIONS.md` and requires exact equality.

The frozen pilot scores were then reproduced exactly, with the verifier's own scoring code on the checksummed archive and no model or retrieval call. They were decomposed by reviewed category for every node, case and hypothesis. Counterfactual views were computed two ways:

- **Exact evidence-zeroing** (primary).
- **Graph-deletion sensitivity**, because 58 of 78 score-moving nodes inherit part of P(X|H) through a parent.

The verifier was not changed and nothing was rerun.

Main results (conditional on D045, which is model-based review, not expert ground truth):
1. **None of the frozen verifier's three agreements with a later `favored` resolution rests on a reviewed genuine discriminator.**
   - Eukaryogenesis and fly-wing have none.
   - GlnBP's two genuine discriminators point against the later-favoured induced-fit account (−0.38). Its frozen +1.84 came from silence errors (+1.63) and generic component facts (+0.92).
2. **Removing only the confirmed errors keeps the favoured direction in eukaryogenesis (+1.82) and GlnBP (+0.21),** but generic component facts carry it (+2.02 and +0.92). Fly-wing collapses to +0.007, from one unreviewed node.
3. **The one failure reverses.** PFC storage-vs-control's genuine discriminators favour the later-supported control account (+0.58). One silence error (−0.89) and three construct mismatches (−0.72) outweighed them.
4. **Six of eight cases have no reviewed genuine discriminator.**
5. **Share of all score influence by category:**

   | category | share |
   |---|---|
   | generic component facts | 25.8% |
   | silence errors | 20.2% |
   | compatible non-discriminative | 15.2% |
   | weak implication | 6.8% |
   | genuine discriminators | 8.1% |
   | construct mismatch | 4.0% |
   | unreviewed | 19.9% |

   The problem is broader than silence handling: non-discriminative component and compatible facts (41.0%) outweigh silence errors (20.2%).

CHANGES:
Commit `dc13560`: D045 labels encoded.
- `benchmark/review/graph_pilot_001/human_labels_D045.json` (new): 40 labels with D045 number and key, resolved case/node/review id, and provenance.
- `scripts/build_review_packet.py`:
  - loads label files;
  - fills `human_primary_category`, `human_is_genuinely_discriminative` (true only for `genuine_discriminator`), `human_silence_as_null_error` (true only for `silence_as_null_error`), `human_reviewer`, `human_review_source` and `human_review_status`;
  - rejects labels for nodes outside the review set;
  - renders labels in the Markdown views.
  - The blank field `reviewer` became `human_reviewer`, and `human_review_source` / `human_review_status` were added.
- Regenerated: `review_set_full.jsonl`, `review_set_priority.jsonl`, `review_full.md`, `review_priority.md`.
- `RUBRIC.md`, `README.md`: field names and label provenance.
- `tests/test_review_packet.py`:
  - the blank-field test now covers unlabelled nodes only;
  - new tests check exact D045 transcription (numbering, keys, categories, stated counts);
  - D045 keys must resolve to the priority set in rank order;
  - labelled nodes carry exactly the D045 fields and nothing inferred.

Commit `b552314`: attribution.
- `scripts/analyze_review_attribution.py` (new): deterministic and LLM-free. It reuses the packet builder's archive verification, graph rebuild and reproduction check.
- `benchmark/review/graph_pilot_001/attribution/` (new):
  - `node_contributions.jsonl`
  - `case_category_attribution.json`
  - `counterfactual_views.json`
  - `coverage.json`
  - `ATTRIBUTION_REPORT.md`
- `tests/test_review_attribution.py` (new, 14 tests).

This report is in a third commit (see ARTIFACTS).

Not modified: `src/`, `configs/` (`git diff 4123d52 -- src configs` is empty); `.agent/DIRECTIVE.md`, `PROJECT_STATE.md`, `DECISIONS.md`; the private archive (checksum verified).

RESULTS:
Orientation: log-odds = log-score(H2) − log-score(H1); positive supports H2. In all four `favored` cases the later resolution favours H2 (PROJECT_STATE).

Frozen scores reproduced:
- Every case's scores, rounded P(X|H) and contributions match the frozen `scores.json` (build aborts otherwise).
- Category buckets, including `non_moving`, sum to each case's frozen log-odds within 1e-9.

Coverage:
- Total absolute influence 18.07.
- Reviewed: 40 nodes, 14.48 (80.1%). Unreviewed: 38 nodes, 3.59 (19.9%).
- Below the packet-wide reviewed share:
  - spider 45.4%
  - forest 67.5%
  - PFC interhemispheric 67.7%
  - gcn4 70.5%
  - eukaryogenesis 79.5%

Signed log-odds by category (node counts in `ATTRIBUTION_REPORT.md` §2):

| case | frozen | genuine | silence | generic | compatible | mismatch | weak | unreviewed |
|---|---|---|---|---|---|---|---|---|
| eukaryogenesis (fav H2) | +2.42 | · | −0.24 | +2.02 | · | · | +0.85 | −0.20 |
| fly-wing (fav H2) | +0.31 | · | +0.30 | · | · | · | · | +0.01 |
| forest (regime) | −1.63 | · | −0.41 | · | −1.64 | · | +0.19 | +0.22 |
| gcn4 (mixed) | +0.00 | · | −0.19 | −0.25 | +0.28 | · | · | +0.16 |
| GlnBP (fav H2) | +1.84 | −0.38 | +1.63 | +0.92 | −0.19 | · | · | −0.13 |
| PFC interhemispheric (regime) | −0.48 | · | · | · | −0.39 | · | · | −0.09 |
| PFC storage (fav H2) | −1.21 | +0.58 | −0.89 | · | −0.24 | −0.72 | · | +0.05 |
| spider (component-wise) | +0.31 | · | · | +0.21 | · | · | +0.19 | −0.10 |

Counterfactual views (evidence-zeroed log-odds and top; `ATTRIBUTION_REPORT.md` §3 has graph-deletion values and relation to resolution):

| case | A1 genuine + unreviewed | A2 genuine only | B1 errors removed | B2 errors removed, reviewed only |
|---|---|---|---|---|
| eukaryogenesis | −0.20 H1 (opposes) | tie | +1.82 H2 (agrees) | +2.02 H2 (agrees) |
| fly-wing | +0.01 H2 | tie | +0.01 H2 | tie |
| forest | +0.22 H2; graph-deleted −0.47 H1 | tie | −1.41 H1 | −1.64 H1 |
| gcn4 | +0.16 H2 | tie | +0.19 H2 | +0.03 H2 |
| GlnBP | −0.52 H1 (opposes) | −0.38 H1 (opposes) | +0.21 H2 (agrees) | +0.35 H2 (agrees) |
| PFC interhemispheric | −0.09 H1 | tie | −0.48 H1 | −0.39 H1 |
| PFC storage | +0.63 H2 (agrees) | +0.58 H2 (agrees) | +0.39 H2 (agrees) | +0.33 H2 (agrees) |
| spider | −0.10 H1 | tie | +0.12 H2 | +0.21 H2 |

- Views A1 and D coincide, and so do A2 and C; each pair is implemented once (the directive allows this). View R (unreviewed only) is also reported.
- Forest is the only case where the two decompositions disagree on ordering (view A1): unreviewed children inherit routes from reviewed parents.

Directive §8 per case: does the frozen relation to the later resolution survive confirmed-error removal (B1)?
- **Eukaryogenesis:** agrees → still agrees, carried by generic component facts.
- **Fly-wing:** agrees → +0.007 from one unreviewed node; effectively disappears, and the strict view (B2) is a tie.
- **GlnBP:** agrees → still agrees (+0.21), carried by generic component facts, while genuine discriminators alone oppose.
- **PFC storage:** opposes → agrees.
- **Non-directional cases:** leans reported only.

Underdetermined once non-discriminative reviewed nodes are removed (A2 has no reviewed genuine discriminator): 6 of 8 cases, all except GlnBP and PFC storage.

Mechanical pathway shared across categories:
- The hypothesis that did not generate the proposition was labelled `unlikely`/`strongly_contradicted` in 8/8 silence errors, 13/14 generic component facts, 3/3 construct mismatches, 3/3 weak implications and 4/4 genuine discriminators.
- All 14 generic component facts were literature-supported.
- In GlnBP the silence errors worked through **contradiction**: evidence contradicted H1's own propositions, and the silent H2 was labelled `unlikely`, so H1's penalty became H2's gain.

Next human-review batch, listed only, not labelled:
- the 8 unreviewed nodes in the low-influence cases: spider X7, X24, X8, X22, X17; PFC interhemispheric X1, X23; fly-wing X19;
- then the remaining 30 by influence (`coverage.json`).

TESTS_AND_EVIDENCE:
- `python3 -m pytest tests/ -q`: 496 passed, 1 xfailed (the pre-existing strict xfail).
- With the private archive removed, the packet and attribution test files give 17 passed and 20 skipped (each skip explains the missing private archive), so a clean clone passes.
- `tests/test_review_attribution.py` (14):
  - no LLM imports;
  - category buckets sum to each case's frozen log-odds, and those equal the frozen scores;
  - non-moving nodes contribute zero log-odds;
  - node table sums equal the category buckets;
  - every view equals the sum of the categories it keeps (A1, A2, B1, B2, R and original checked independently of the producing code);
  - confirmed errors are exactly the three named categories;
  - scores, tops and relations are internally consistent in both decompositions;
  - the original graph-deleted view equals evidence-zeroed;
  - non-directional cases are never scored as agreement;
  - node categories equal the label file, and unreviewed nodes are unlabelled;
  - node classes equal the packet (40 / 38 / 114);
  - coverage figures and the next-review queue are consistent;
  - the report states that labels are not expert ground truth and proposes no fix;
  - the committed outputs are byte-identical to a fresh build from the archive.
- `tests/test_review_packet.py` (23): the 20 prior checks, with the blank-field test narrowed to unlabelled nodes, plus exact D045 transcription, resolution of D045 keys to the priority set in rank order, and labelled nodes carrying exactly D045 fields.
- Pre-flight checks before encoding:
  - D045 in `DECISIONS.md` and the directive list are identical (40 entries, numbered 1–40).
  - Category counts match D045's stated 4/8/14/8/3/3.
  - Every short key resolves to exactly one case.
  - The labelled set equals the packet's priority set, and each D045 number equals the node's global influence rank.

DECISIONS_AND_ASSUMPTIONS:
- **Labels are transcribed mechanically, not retyped.** D045 recorded only primary categories, so the booleans are derived exactly as the directive specifies and every other judgment field stays blank.
- **One orientation everywhere: log-odds of H2 over H1.** The packet records log-odds in each graph's own hypothesis order, which is `[H2, H1]` for GlnBP, forest and fly-wing. The packet is not wrong (each record states its definition), but its values are not summed across cases.
- **The favoured hypothesis for `favored` cases comes from PROJECT_STATE** (H2 in all four). No other case is mapped to a winner.
- **Evidence-zeroing is the primary decomposition.** It is what the directive specifies and is exact and unique under additive aggregation. Graph deletion is reported as sensitivity: it removes routes to descendants, is computed with the verifier's scoring code, is not additive across nodes, and changes no model judgment.
- **Non-moving nodes stay in every view.** They cannot change log-odds, and many are parents providing routes.
- **Strict views set unreviewed nodes aside rather than judging them.** Every view states what it does with them.
- **"Under-covered"** means a case's reviewed share is below the packet-wide reviewed share (80.1%), the packet's own design target, not a new threshold.
- **The interpretation section is generated** with every number pulled from the computed data. It is labelled as executor interpretation, not a decision.

UNCERTAINTIES_AND_LIMITATIONS:
- **All category attributions depend on D045,** a first-pass, model-based Research Director review. No per-hypothesis predictions were recorded, so silence errors cannot be split further (e.g. by which hypothesis was silent).
- **19.9% of score influence is unreviewed.** In A1, eukaryogenesis flips to H1 and forest's sign depends on the decomposition, entirely on unreviewed nodes. Spider is only 45% covered.
- **Path mediation:** 25 of the 58 parent-route dependencies run through reviewed nodes. Evidence-zeroing does not remove an erroneous parent edge's effect on children; graph deletion does, but removes the whole route, including any legitimate part. Neither isolates the error alone without relabelling edges, which would change a model judgment and was not done.
- **Magnitudes rest on placeholder ordinal mappings (`v0-placeholder`).** Only signs and relative sizes are meaningful. With n = 8 cases, 4 of them directional, all conclusions are descriptive.
- **Reliance on D045:** the analysis does not check whether D045 is correct. For example, GlnBP's reversal rests on two nodes labelled genuine (X5 at −0.64, X9 at +0.25).

PROBLEMS_OR_RISKS:
- **No bug found in the previous influence analysis.** Deterministic reconstruction matched exactly.
- **Some earlier executor-reported figures, derived from the LLM auditor, are superseded by the D045-based attribution:**
  - "GlnBP strongest case with +1.01 genuine" is now −0.38 genuine; the nodes the auditor called genuine (X4, X11) are D045 silence errors.
  - "Eukaryogenesis +0.50 genuine" is now none.
  - PROJECT_STATE currently carries the auditor-based figures.
- **The private archive is still only on the execution host** (two copies, one machine).

QUESTIONS_FOR_DIRECTOR:
1. D045 recorded primary categories only. Should the next review round also record per-hypothesis predictions for silence errors, so silence can be split by which hypothesis was silent and whether the null label was absence or presence?
2. Should the next batch be the 8 low-coverage-case nodes first, as listed, or the 30 remaining nodes by influence? The A1 results for eukaryogenesis and forest depend on the unreviewed nodes.
3. Should generic component facts be treated as errors or as weak evidence in future accounting? Excluding them from the "remove confirmed errors" view, as specified, is what keeps eukaryogenesis and GlnBP agreeing.

RECOMMENDED_NEXT_ACTION:
(Recommendation only; no fix proposed.)
1. Update PROJECT_STATE's hypothesis-comparison figures to the D045-based attribution, which supersedes the auditor-based numbers.
2. Label the next review batch, starting with the 8 low-coverage-case nodes, and record per-hypothesis predictions this time.
3. Treat the finding that non-discriminative component and compatible facts carry more influence than silence errors as a primary input to method design, alongside silence handling. Any fix should be investigated on a separate development set.

ARTIFACTS:
- Updated review set with D045 labels:
  - `benchmark/review/graph_pilot_001/review_set_full.jsonl`
  - `benchmark/review/graph_pilot_001/review_set_priority.jsonl`
  - human-readable: `review_full.md`, `review_priority.md`
- Label source: `benchmark/review/graph_pilot_001/human_labels_D045.json`
- Per-node contribution table: `benchmark/review/graph_pilot_001/attribution/node_contributions.jsonl`
- Per-case category attribution: `benchmark/review/graph_pilot_001/attribution/case_category_attribution.json`
- Counterfactual scores and orderings: `benchmark/review/graph_pilot_001/attribution/counterfactual_views.json`
- Coverage statistics and next review batch: `benchmark/review/graph_pilot_001/attribution/coverage.json`
- Human-readable report: `benchmark/review/graph_pilot_001/attribution/ATTRIBUTION_REPORT.md`
- Scripts: `scripts/analyze_review_attribution.py`, `scripts/build_review_packet.py`
- Tests: `tests/test_review_attribution.py`, `tests/test_review_packet.py`
- Git commits: `dc13560` (labels), `b552314` (attribution), plus the commit containing this report. All are on `master`.
