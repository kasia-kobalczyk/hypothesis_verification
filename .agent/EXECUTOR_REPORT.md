TASK_ID: BENCH-GRAPH-PILOT-001
STATUS: COMPLETED

SUMMARY:
The eight frozen explanatory cases were added to the existing experiment runner as a visible dataset plus a separate hidden-annotation file. The hidden split is enforced by a loader that rejects any field not on its whitelist. Cutoff enforcement and hidden-field isolation are tested, including adversarial tests that feed each case's real resolving study through every retrieval channel. All 8 cases ran once through the frozen `narrow_graph_v3_complete` method with no tuning: 8/8 ok, 0 errors, 784 LLM calls, $2.75. An empirical audit of every byte sent to the model found no leakage. Consequence discovery, evidence discovery and hypothesis comparison were then analysed separately after the run was frozen.

Main findings:

(1) The verifier behaves very differently on genuine competing explanations than on ResearchBench. Nodes where one hypothesis's implication label is above `neutral` and the other's below ("sign-opposed") rose from 5% to 45%, and median score margin from 0.120 to 0.389. No judge is involved in this comparison.

(2) Much of that new opposition is not real. On many propositions one hypothesis says nothing, and the verifier then gives that silent hypothesis a directional label, most often `unlikely`. The auditor classifies 51 of the 87 sign-opposed nodes as opposition manufactured from silence and 33 as genuine discriminators. Sensitivity analysis against a blind second rating gives roughly 40 vs 36. So silence-driven contrast is a large share of the opposition, but whether it is a majority is not robust.

(3) Manufactured opposition pushes in a consistent direction. On 29 of the 31 manufactured nodes that moved a score, the push favoured the hypothesis that generated the proposition. Pre-cutoff literature mostly returns `support`, so support for one hypothesis's own one-sided consequences is scored as evidence against its silent competitor.

(4) The generator did recover discriminating consequences: 11 of 23 reference discriminators, in 7 of 8 cases; fly-wing had 0. But 36 of the 44 genuine discriminators had no relevant pre-cutoff evidence, and only 8 genuine discriminators moved any score.

(5) Per-case failure attribution is provisional. The auditor has a measured bias toward calling hypotheses silent (it misses explicit denials; see UNCERTAINTIES). A PFC-storage explanation I initially drew did not survive this check and has been withdrawn from the report.

CHANGES:
Benchmark data (new):
- `benchmark/explanatory/cases_visible.jsonl`: the 8 cases, restricted to case_id, domain, phenomenon, cutoff, and hypotheses (hypothesis_id, text). Text copied verbatim from DIRECTIVE PART I.
- `benchmark/explanatory/cases_hidden.json`: source_anchors, reference_discriminators, resolver, resolving_observations, resolution, leakage_audit.

Minimal adapter and schema code (modified):
- `src/benchmark/loader.py`:
  - `BenchmarkInstance.has_gold`.
  - `VISIBLE_CASE_FIELDS` / `VISIBLE_HYPOTHESIS_FIELDS` plus `project_visible_case()`: a whitelist projection that raises on any unknown field.
  - `load_case_instances()`: frozen cutoff from the manifest, no gold, no source DOI.
- `src/common/config.py`:
  - `dataset.kind: cases`, `dataset.case_path`.
  - `dataset.status: pilot_diagnostic`.
- `src/experiments/runner.py`:
  - Wires `kind: cases`.
  - Skips gold-dependent metrics for no-gold instances instead of fabricating them.
  - `_interpretation_warning()` is now the single source for summary and log wording.
- `src/experiments/reports.py`: no gold column or gold metrics when the instance has no gold.
- `src/methods/consequence_graph.py`: gold made optional in diagnostics only (`gold_id` may be None; origin scope label "unlabelled"). No change to generation, edges, retrieval, evidence or aggregation.

Config (new):
- `configs/pilot_explanatory.yaml`: differs from `configs/mvp.yaml` only in dataset.kind, dataset.status and dataset.case_path. Verified by test.

Audit prompts (new):
- `src/llm/prompts_audit/{recovery_classify_v1,evidence_attribution_v1}.txt` plus README.
- These sit deliberately outside the verifier prompt directory. They may state the cutoff and show hidden annotations, both forbidden in verifier prompts (see DECISIONS_AND_ASSUMPTIONS).

Tests (new, 88 tests):
- `tests/test_explanatory_hidden_isolation.py`
- `tests/test_explanatory_cutoff_enforcement.py`
- `tests/test_pilot_config_is_the_frozen_method.py`
- `tests/test_pilot_recovery_analysis.py`

Analysis scripts (new):
- `scripts/audit_pilot_leakage.py`
- `scripts/analyze_pilot_recovery.py` (supports `--workers` and `--resummarise`)
- `scripts/analyze_pilot_evidence.py`
- `scripts/analyze_pilot_comparison.py`
- `scripts/analyze_pilot_attribution.py`
- `scripts/build_pilot_report.py`

Report (new):
- `docs/PILOT_REPORT.md`: generated entirely from JSON artifacts.

Incidental:
- `data/cost/ledger.jsonl` and `scan_index.json` were appended by the cost tracker.

Not modified: `.agent/DIRECTIVE.md`, `.agent/PROJECT_STATE.md`, `.agent/DECISIONS.md` (identical to HEAD), any verifier prompt (SHAs match the freeze), and `configs/ordinal_mappings.yaml`.

RESULTS:
Provenance and settings:
- Git HEAD is `c18edc29f93afaa4b9683bfed9473bb3fb659329`. The pilot code was an uncommitted working tree on top of it; the run manifest records no commit (see PROBLEMS_OR_RISKS).
- Config: `configs/pilot_explanatory.yaml`. Run: `runs/pilot_explanatory_001`, 2026-09-15 15:28–16:38Z.
- Every LLM role used Azure OpenAI deployment `gpt-4.1-kasia`, api_version 2024-05-01-preview, temperature 0.0, top_p 1.0, seed 20260911, json_mode.

  | Role | Calls |
  |---|---|
  | graph.generate | 64 |
  | graph.root_edge | 192 |
  | graph.chain_edge | 144 |
  | graph.proposition_query | 192 |
  | graph.evidence_assess | 192 |
  | Post-hoc recovery judge (`recovery_classify_v1`) | 192 |
  | Post-hoc evidence judge (`evidence_attribution_v1`) | 192 |

- Literature came from Semantic Scholar (356 provider calls, 0 errors), with Crossref date verification set to `always`.

Per-case cutoff, graph and outcome (every graph has 24 nodes, fixed by the frozen size caps):

| case | cutoff | informative nodes | ref discriminators recovered | top-ranked (margin) | resolution |
|---|---|---|---|---|---|
| pfc_storage_vs_control | 2024-01-01 | 11 | 1/3 | H1 (0.542) | favored H2 |
| gcn4_med15_complex_vs_condensate | 2024-01-01 | 11 | 1/3 | H2 (0.002) | mixed |
| eukaryogenesis_mito_timing | 2025-01-01 | 15 | 3/3 | H2 (0.837) | favored H2 |
| pfc_interhemispheric_architecture | 2024-12-01 | 3 | 2/3 | H1 (0.236) | regime_dependent |
| glnbp_induced_fit_vs_conformational_selection | 2024-01-01 | 11 | 2/3 | H2 (0.726) | favored H2 |
| spider_orb_web_origin | 2026-01-01 | 7 | 1/2 | H2 (0.152) | component_wise |
| forest_fragmentation_resilience | 2024-01-01 | 18 | 1/3 | H1 (0.673) | regime_dependent |
| fly_wing_constraint_vs_selection | 2025-01-01 | 3 | 0/3 | H2 (0.154) | favored H2 |

A. Consequence discovery (auditor, 192 propositions):
- Categories: reference_discriminator_recovered 41, novel_plausible_discriminator 3, compatible_non_discriminative 20, generic_component_fact 5, invalid_or_unsupported 0, silence_as_null_error 123.
- 11/23 reference discriminators recovered, in 7 of 8 cases.
- Fly-wing produced 12 compatible/generic alignment propositions and no discriminator. The directional pattern it generated is the phenomenon itself, which both hypotheses predict.
- The auditor's `silence_as_null_error` label identifies one-sided propositions (one hypothesis predicts, the other is silent). It cannot show that the verifier erred, because the auditor never sees edge labels; the next section joins the two.

Silence as a null prediction (auditor joined to verifier edge labels):
- 127/192 propositions are one-sided.
- Across 131 silent (hypothesis, proposition) pairs, the verifier labelled the silent hypothesis:
  - `neutral` (correct): 57 (44%)
  - as absence (`unlikely`/`strongly_contradicted`): 51 (39%)
  - as presence (`*implied`): 23 (18%)
- Note: `edge_assess_v1` already defines `neutral` as "says nothing either way" and tells the model to use it freely. This is behavioural, not a missing label.
- Sign-opposed nodes: 87 in total, of which 33 are genuine and 51 manufactured by the auditor's count; about 36 vs 40 under the second-rater sensitivity analysis.
- Manufactured nodes that moved a score: 29 favoured the generating hypothesis (8.52 log-odds) and 2 favoured the other (1.72).

Comparison with ResearchBench reserve-12 (same frozen method, structural, no judge):

| measure | ResearchBench | pilot |
|---|---|---|
| sign-opposed nodes | 11/240 (5%, all in one instance) | 87/192 (45%, all 8 cases) |
| negative edges | 2% | 23% |
| neutral edges | 34% | 17% |
| informative nodes | 32% | 41% |
| median margin | 0.120 | 0.389 |
| margin > 0.5 | 0/12 | 4/8 |

"Edge labels differ at all" is 94% in both runs and is uninformative.

B. Historical evidence discovery (attribution judge):
- All 192 propositions: no_relevant_historical_evidence_exists 114, informative_evidence_found 63, generic_compatibility_only 14, retrieval_failure 1.
- The 44 genuine discriminators: 36, 7, 1 and 0 respectively.
- Assessor errors: 0. Empty retrievals: 0.
- Evidence labels overall: support 35, weak_support 19, strong_support 19, strong_contradiction 5, weak_contradiction 1, no_evidence 113.

C. Hypothesis comparison. No accuracy was computed. Each ranking was decomposed exactly into contributions (log-odds toward the top-ranked hypothesis):
- **eukaryogenesis** (top matches the resolution): genuine +0.50, manufactured +2.13.
- **fly_wing** (top matches): genuine 0.00, manufactured +0.30. The "match" has no discriminating basis.
- **glnbp** (top matches): genuine +1.01, manufactured +0.78. The best-supported case.
- **pfc_storage** (top opposes): manufactured +1.33 toward storage, genuine −0.30.
  - The auditor misclassified X15 (H2 explicitly says "rather than directly storing"). Corrected, genuine is about −0.02.
  - The drivers were strong pre-cutoff support for content-selective persistent PFC activity (X2, X14, X15). Whether that counts against a control account was the interpretive core of the dispute; the resolver settled it with a causal manipulation not yet performed at the cutoff.
  - Attribution: provisional, mixed between historical evidence pointing the other way and auditor-dependent silence calls.
- **Non-directional cases**: gcn4 cancels to zero (manufactured −0.50 vs correctly-handled one-sided +0.51). Forest leans H1 mainly on correctly-handled one-sided stress evidence (+1.00). Pfc_interhemispheric and spider are weak.

TESTS_AND_EVIDENCE:
- `python3 -m pytest tests/ -q`: 459 passed, 1 xfailed (the pre-existing strict xfail, DECISIONS #23). Baseline before this directive was 371 passed.
- `tests/test_explanatory_cutoff_enforcement.py` (10):
  - Every resolver postdates its cutoff; every cutoff is frozen and ≥ 2024-01-01.
  - A provider subclass that returns each case's real resolver DOI and date via search, references, citations and lookup: nothing survives, through the real normalisation and filter.
  - A pre-cutoff decoy does survive on 8/8 cases, so the filter discriminates rather than blocking everything.
  - `render_for_prompt` raises `TemporalLeakError` on a smuggled resolver.
  - The agent-facing API exposes no cutoff or date parameter.
- `tests/test_explanatory_hidden_isolation.py` (27):
  - The projection refuses 8 hidden field names at case level and at hypothesis level; a poisoned dataset fails to load.
  - No hidden DOI, URL, resolver identity token, resolution label, discriminator (full or 8-word window), resolving observation or resolution summary appears in the loaded instance or in the rendered pilot prompts.
  - Pilot prompts declare no hidden placeholder.
  - Audit prompts are not in the verifier prompt directory, and no `src/` code references them.
- `tests/test_pilot_config_is_the_frozen_method.py` (26): the pilot differs from mvp only in 3 dataset fields; all 21 frozen method parameters match; all 5 frozen prompt SHAs match.
- `scripts/audit_pilot_leakage.py` on the frozen run: 8/8 clean. It scanned 4.79M characters of model traffic and 3,812 retrieved papers: 0 post-cutoff papers, 0 hidden DOI or phrase hits.
- Auditor reliability (`runs/pilot_explanatory_001/audit_checks.json`):
  - Internal consistency: 0 contradictions in 192 between category and per-hypothesis statuses.
  - Test-retest on one case judged twice: category 21/24, discriminative call 23/24.
  - Blind second rating (by me, an LLM, not a human expert): stratified sample of 3 per case, seed fixed before viewing, rated before seeing the judge's labels. Discriminative call 18/24, full status vector 15/24. The judge called 5/24 discriminative, I called 7/24. The judge found 16/24 one-sided, I found 11/24.
  - The 2 non-verbatim reference matches change no count.
- `--resummarise` was checked to leave all 192 raw judgments byte-identical; the pre-resummarise file is kept as `recovery.before_resummarise.json`.
- Position artifact check: the model only ever sees "Candidate A/B". The resolution-favoured H2 was displayed as B in 2 cases and A in 2.

DECISIONS_AND_ASSUMPTIONS:
- **Adapter model.** `load_k_set_instances` was the model, since it already took explicit cutoffs and arbitrary k. Gold was made optional rather than inventing a winner. Mixed and regime-dependent cases have none, and marking one in visible data would leak the answer.
- **Whitelist, not blacklist,** for visible fields. It fails closed on field names nobody anticipated.
- **No `blocked_dois`.** I relied on the cutoff date because every resolver date was verified post-cutoff (tested).
- **Audit prompts live in a separate directory** instead of being exempted from `test_no_prompt_mentions_a_cutoff_date`. That invariant fired on my first attempt, and I kept it intact.
- **Discriminativeness is measured by sign opposition** (one label above `neutral`, one below), a boundary fixed by the ordinal scale rather than tuned. The permissive "labels differ" measure is still reported.
- **No decision threshold on score margins.** The only verdict the comparison script issues is `insufficient_evidence`, and only when no node was informative (it never occurred).
- **`reconcile()` was revised after the judges ran.** The first version counted a silent hypothesis labelled `neutral` as silence inflation; `neutral` is inert and correct. It was recomputed from preserved judgments with no new model calls, and both versions are kept.
- **Judges were not tuned on these cases.** Each prompt was written once and never edited after first use; they were only moved to `src/llm/prompts_audit/`. One case was judged once in a scratch copy to validate the pipeline before the run finished; those judgments are used only for the test-retest check.
- **Judge calls ran 6 at a time** (independent, order preserved). The aborted sequential attempt's event log is kept as `recovery_events.aborted_sequential_attempt.jsonl`.
- **The resolution-favoured hypothesis** for the 4 `favored` cases was mapped by me from the resolution summaries (all H2). This is recorded in audit_checks.json.

UNCERTAINTIES_AND_LIMITATIONS:
- **Every Step-6/7 category comes from an LLM judge** on the same deployment as the verifier, and the only second rating is also an LLM (me). No human domain expert has reviewed anything.
- **The recovery auditor has a measured, directional bias.** It over-calls `indeterminate` and misses explicit denials in hypothesis text (e.g. pfc_storage X15). A plausible cause is my own prompt, which warns emphatically against reading silence as absence. Its count of manufactured contrast should be read as an upper estimate.
- **Per-case failure attribution is provisional.** 78 nodes moved rankings and 40 carry 80% of the influence; they are exported for expert review in `manual_review/score_moving_nodes_for_expert_review.json`.
- **The evidence-attribution judge only sees retrieved papers.** It cannot detect evidence that exists but was not retrieved, so `retrieval_failure` (1) is almost certainly under-counted and `no_relevant_historical_evidence_exists` over-counted.
- **n = 8, and 4 cases are non-directional.** Every aggregate here is descriptive. Ordinal mappings are `v0-placeholder`, so log-odds magnitudes only compare within this run.
- **The leak audit's post-cutoff paper check is partly circular.** It uses the same publication dates the filter used, and year-only dates are not checked. The independent part is the scan of model traffic against hidden annotations.
- **Test-retest covers only one case** (24 propositions).
- **Graph size is identical across cases** (24 nodes, from the frozen caps), so coverage differences are not confounded by size, but the caps may truncate richer cases.

PROBLEMS_OR_RISKS:
- **Reproducibility.** The run manifest records no git commit, and the pilot code is uncommitted on top of `c18edc2`. `runs/` is gitignored, so the 42 MB of forensic artifacts exist only on this disk. I recommend a commit and an artifact backup before anything else. I have not committed; the human did not ask me to.
- **Benchmark construction.** In all 4 `favored` cases the favoured hypothesis is H2 in `cases_hidden.json` and `cases_visible.jsonl`. It did not reach the model this time (shuffled A/B display), but any future id-dependent path would leak it. A larger benchmark should randomise hypothesis ids.
- **Reconciliation discrepancies with the migration summary:**
  - The method hard-required a gold hypothesis. PROJECT_STATE says it "supports arbitrary k≥2"; true for k, but not for no-gold. Fixed minimally.
  - The environment note said the directory was not a git repository. It is.
  - `.agent/CHARTER.md` exists, is empty, and is not described in CLAUDE.md.
  - PROJECT_STATE's frozen dossier schema (title, articulation_type, source_public_date, pre_cutoff_context, consequence_matrix with silence_as_null_check, construction_status, …) is not present in DIRECTIVE PART I. I materialised only what the directive provides, so the full dossiers described as the "next execution target" do not yet exist.
  - D041's GitHub-history leakage recheck for spider_orb_web_origin (cutoff 2026-01-01) remains unresolved; this directive did not ask for it.
- **The run is spent for method tuning.** Anything motivated by findings (2)–(3) (e.g. silence handling in edge assessment) would need a separate development set.

QUESTIONS_FOR_DIRECTOR:
1. Is the edge assessor's handling of silence the next method question? It gives a silent hypothesis a directional label 56% of the time, despite a prompt that defines `neutral` for exactly this case. If so, what development set may be used, given these 8 cases and the ResearchBench reserve are both spent for tuning?
2. For a ~20-case benchmark, is an LLM auditor acceptable for consequence-recovery metrics, given the measured bias? Or should reference-discriminator matching and silence calls be human-annotated, at least on the score-moving nodes?
3. Should one-sided propositions count against consequence generation? `consequence_generate_v3` generates per hypothesis and explicitly allows consequences many claims would predict, so one-sidedness is arguably by design and the issue sits in edge assessment and aggregation.
4. Should the benchmark randomise hypothesis ids relative to resolution before scaling?

RECOMMENDED_NEXT_ACTION:
(Recommendation only.)

Do not scale the frozen graph verifier to a ~20-case benchmark yet. Do scale the benchmark itself.

The pilot shows the explanatory benchmark is a much better diagnostic instrument than ResearchBench. It elicits genuine opposition, and the generator recovers about half the reference discriminators. But on the frozen method, a 20-case comparison would mostly measure the silence-to-direction behaviour and the auditor's own bias, not whether graph structure helps compare hypotheses.

Suggested order:
1. Commit the pilot code and back up `runs/pilot_explanatory_001`.
2. Have a human domain expert review the 40 nodes carrying 80% of ranking influence (file prepared). This makes the failure attribution trustworthy and yields human labels to validate or replace the recovery auditor.
3. Decide whether silence handling in edge assessment and aggregation is the method target. If so, address it on a separate development set, not these 8.
4. Construct the ~20-case benchmark with randomised hypothesis ids, and treat consequence discovery as its primary measurable capability. By construction the decisive discriminators mostly lack pre-cutoff evidence (36/44 here), so final hypothesis comparison is expected to be weak.

ARTIFACTS:
- `docs/PILOT_REPORT.md`: human-readable report, every number from the JSON below.
- `benchmark/explanatory/cases_visible.jsonl`, `benchmark/explanatory/cases_hidden.json`
- `configs/pilot_explanatory.yaml`
- `runs/pilot_explanatory_001/`:
  - `summary.json`, `manifest.json`, `config.yaml`, `metrics.json`, `events.jsonl`
  - `leak_audit.json`: empirical leak audit.
  - `recovery.json`: Step 6/7A, with raw judge output per proposition; also `recovery.before_resummarise.json` and `recovery_events.jsonl`.
  - `evidence_discovery.json`: Step 7B; also `evidence_analysis_events.jsonl`.
  - `hypothesis_comparison.json`: Step 7C.
  - `ranking_attribution.json`: exact log-odds decomposition per case, plus the mechanism test.
  - `audit_checks.json`: auditor reliability, sensitivity, the ResearchBench structural comparison, position check.
  - `manual_review/`:
    - `sample_blind.json`, `ratings_compared.json`: second rating.
    - `score_moving_nodes_for_expert_review.json`: 78 nodes, blank expert fields.
  - `instances/<case_id>/`: input.json, presentation.json, graph.json, edge_judgments.json, queries.json, retrieval.json, evidence.json, scores.json, model_outputs.json, events.jsonl, report.md.
- Comparison run: `runs/consequence_graph_20260913T170715Z_e0bed1a0` (ResearchBench reserve-12, same frozen method).
- Tests:
  - `tests/test_explanatory_hidden_isolation.py`
  - `tests/test_explanatory_cutoff_enforcement.py`
  - `tests/test_pilot_config_is_the_frozen_method.py`
  - `tests/test_pilot_recovery_analysis.py`
- Scripts:
  - `scripts/audit_pilot_leakage.py`
  - `scripts/analyze_pilot_recovery.py`
  - `scripts/analyze_pilot_evidence.py`
  - `scripts/analyze_pilot_comparison.py`
  - `scripts/analyze_pilot_attribution.py`
  - `scripts/build_pilot_report.py`
