TASK_ID: BENCH-GRAPH-V4-SCOPE-001
STATUS: COMPLETED

SUMMARY:
v4-scope (`consequence_graph_v4_scope`) was implemented as a new versioned method on top of the unchanged v3 pipeline. Prior v4 stays registered and reproducible. It adds four things before comparative scoring:
- a separate proposition-scope classifier;
- a contrast-bearing-element extractor;
- evidence relevance judged against that element;
- a deterministic gate.

Only propositions that meet all of these score:
- a determinate cross-hypothesis contrast (the prior-v4 state gate, unchanged);
- `hypothesis_specific` or `mechanism_specific` scope;
- informative evidence;
- an element that carries a contrast;
- `contrast_direct` relevance.

Everything else is kept descriptively and contributes zero; `contrast_partial` is reported as a sensitivity analysis only.

Development followed the human's replicate plan (below): 2 iterations × 3 stage-A replays on the frozen v3 pilot, then 3 fresh end-to-end runs of the final version, each followed by the consequence-recovery auditor.

**Recommendation: do not freeze; continue development.** v4 was not frozen.

What was learned:
1. **Prediction-state behaviour is preserved.** Same state prompt; D046 unqualified agreement 20/20 in all 6 replicates; indeterminate rate and between-replicate agreement are within prior-v4 run-to-run noise.
2. **Scope works as intended.**
   - No broader-class or possibility proposition scored in any stage-A replicate.
   - All 14 reviewed generic component facts are unscored in every iteration-2 replicate (13/14 in iteration 1).
   - All 4 reviewed genuine discriminators are scope-eligible with a contrast-bearing element in every replicate.
   - Stage-B exception: a proposition text-identical to a reviewed generic fact (`eukaryogenesis-X6`) was classified `hypothesis_specific` and scored in 2 of 3 fresh runs.
3. **Genuine discriminators still almost never score.** Their pre-cutoff evidence is `contrast_partial`: `contrast_direct` in 1 of 24 stage-A node-replicates. Their records address the contrast variable only partly (e.g. apo/holo structures that do not show binding order).
4. **What does score (4–6 of 192 nodes) is dominated by reviewed implication errors.**
   - Iteration 2 influence: silence errors 63–84%, weak implications 16–28%, genuine discriminators 0/0/13%.
   - Generic facts, compatible facts and construct mismatches: 0%, against v3's 26%, 17% and 7%.
   - The recurring errors (`glnbp-X4`, `glnbp-X11`, `pfc_storage-X2`, `eukaryogenesis-X7`, `forest-X15`) get determinate, opposed states. gpt-4.1 reproduces the same contrast when separately asked each candidate's position on the contrast variable without seeing the states (iteration 2).
   - Prior v4 did not score these nodes only because its whole-proposition construct match rated their evidence partial or mismatch.
5. **Specificity–assessability trade-off, quantified.**
   - Specific propositions (about two thirds) have informative historical evidence less often than broad ones: 37–38% vs 48–50% in every replicate.
   - `hypothesis_specific` is the least assessable class: 30% informative, 6% contrast-direct (iteration 2).
   - The directness gap depends on the relevance prompt: broad propositions got direct evidence about twice as often under relevance v1 (17–21% vs 9–10%), but similarly often under v2 (10–13% vs 11–12%).
6. **`context_only` and `construct_mismatch` are almost never assigned** (at most 3 per stage-A replicate or stage-B run, among 77–89 judged nodes). The records the v3 assessor cited nearly always report the contrast variable at least partly, so the operative separation is `contrast_direct` vs `contrast_partial`.
7. **`contrast_partial` sensitivity.**
   - It is the only route by which genuine discriminators carry material influence: 21–35% share in iteration 2.
   - It re-admits 1–2 generic facts and leaves silence errors the largest category (35–44%).
   - It is not clean or stable enough to define the method.
8. **Stage B.**
   - Scored propositions: 4–6 per run. Six of 15 are text-identical to reviewed pilot nodes, and all six are reviewed failures.
   - Executor's reading, not labels: 4 of the other 9 closely paraphrase reviewed genuine discriminators.
   - Case directions are not stable (eukaryogenesis favours H1 in run 1 and H2 in runs 2–3); four cases tie in every run.
9. **Consequence discovery is largely preserved.** 9, 10 and 10 of 23 reference discriminators, against 11 in each of the three earlier runs. The layer runs after generation and cannot affect it, but the drop appears in all three runs.

CHANGES:
New method, all additive:
- `src/methods/consequence_graph_v4_scope.py`: `run_v4_scope_layer`, `ConsequenceGraphV4ScopeVerifier`, `METHOD_VERSION`, and `STATE_PROMPT="prediction_state_v2"` pinned by name. The layer records states, scope, element, relevance, gate, contribution and `sensitivity_used_in_score` per node, plus buckets by gate reason, sensitivity scores, errors and call ids.
- `src/graph/proposition_scope.py` (scope and element judgments):
  - `SCOPE_PROMPT`, `ELEMENT_PROMPT`, `ELEMENT_FIELDS`, `POSITIONS`;
  - parsers `parse_scope_class`, `parse_contrast_element` (v1), `parse_contrast_element_v2`;
  - `derive_positions_contrastive`, `positions_agree_with_states`;
  - `assess_scope`, `extract_contrast_element` (dispatches v1/v2).
- `src/evidence/contrast_relevance.py`: `RELEVANCE_PROMPT`, `parse_contrast_relevance`, `assess_contrast_relevance`.
- `src/inference/discrimination.py` (appended; existing v4 functions untouched): `SCOPE_CLASSES`, `COMPARATIVE_SCOPE_CLASSES`, `CONTRAST_RELEVANCE`, `COMPARATIVE_RELEVANCE`, `SENSITIVITY_RELEVANCE`, `normalise_scope_class`, `derive_contrast_relevance`, `gate_node_scope`.
- Prompts in `src/llm/prompts/`:
  - `proposition_scope_v1.txt` and `_v2.txt`;
  - `contrast_element_v1.txt` and `_v2.txt`;
  - `contrast_relevance_v1.txt` and `_v2.txt`.
  - The only illustration is an invented lake/algal-bloom dispute; there is no development-case content.
- `src/experiments/runner.py`: registers `consequence_graph_v4_scope` in `METHODS`.
- `src/experiments/metrics.py`: `n_v4s_*` diagnostic counters.
- `scripts/replay_v4_on_frozen.py`: `--layer v4|v4_scope`. The default `v4` path is unchanged; `v4_scope` passes the case question from the frozen `input.json`.

Analysis and reporting:
- `scripts/analyze_v4_scope.py`: deterministic stage-A metrics.
  - It re-derives every gate and score from recorded judgments as a consistency check.
  - Sections: state preservation vs prior v4 and D046; scope vs D045/D046; contrast relevance; scope × evidence table; influence composition; partial sensitivity; scored nodes; pairwise stability; per case.
- `scripts/compare_v4_scope_runs.py`: stage-B comparison.
  - It covers the frozen pilot, the v3 rerun, the prior v4 run and the 3 v4-scope runs: generation structure, consequence discovery, and the v4-scope layer with exact-text label transfer.
- `scripts/build_v4_scope_report.py`: generates `docs/V4_SCOPE_REPORT.md`.

Tests:
- `tests/test_v4_scope.py` (71 tests):
  - scope separation from states, and the state prompt pinned to the v4 head with no scope vocabulary;
  - broad, possibility and invalid scope never scores, including under the sensitivity policy;
  - only `contrast_direct` scores; context-only, mismatch, partial and no-evidence never move the main score;
  - scope never makes one-sided or shared profiles comparative;
  - fail-closed behaviour for every LLM call;
  - strict element parsing (v1 and v2); v2 positions must contrast and agree with states; the v2 extractor never sees states;
  - relevance derivation table;
  - verifier wiring through `run_instance`, with the cutoff-enforcing renderer and only cited records;
  - registration of v4 and v4-scope as distinct methods;
  - prompt invariants: no hidden placeholders, no "cutoff", no dates, JSON present, no distinctive development-case terms (the term list is checked against the visible case file);
  - no `cases_hidden` / `prompts_audit` in the new code.
- `tests/test_v4_scope_analysis.py` (11 tests): evidence column, scope × evidence rates, composition shares.

Docs:
- `docs/V4_SCOPE_DESIGN.md`: scope, element and relevance schemas, the gate, and the v1→v2 differences.
- `docs/V4_SCOPE_REPORT.md`: the full development report with all tables.

Outputs:
- `benchmark/v4_scope/iter01/development_metrics.json` and `benchmark/v4_scope/iter02/development_metrics.json`.
- `benchmark/v4_scope/stage_b/run_comparison.json`.
- `benchmark/frozen_runs/v4_scope_runs/{MANIFEST.md, SHA256SUMS, v4_scope_runs.tar.gz.sha256}`, with the tarball itself private and gitignored.

Not modified: `.agent/DIRECTIVE.md`, `PROJECT_STATE.md`, `DECISIONS.md`; the v3 and prior v4 method code and prompts; ordinal mappings; configs; D045/D046 labels; earlier runs and archives. `data/cost/ledger.jsonl` and `scan_index.json` were updated automatically by the LLM client.

RESULTS:
Setup:
- Commits:
  - `b05c35e`: layer and tests;
  - `a2f34d3`: `has_contrast` gate; iteration-1 replays;
  - `222d4fa`: iteration-2 prompts; iteration-2 replays;
  - `753a86c`: metrics and stage-B script; stage-B runs, with method code identical to `222d4fa`;
  - the commit containing this report: report generator, stage-B comparison, archive checksums.
- Model: Azure OpenAI `gpt-4.1-kasia` (api 2024-05-01-preview), temperature 0, seed 20260911, JSON mode.
- Literature: Semantic Scholar + Crossref with the frozen per-case cutoffs; cache at `data/cache/literature`.
- Config and mappings: `configs/v4_dev_explanatory.yaml` (pilot config with `dataset.status: development`); ordinal mappings `v0-placeholder`.
- Replicates: 2 iterations × 3 stage-A replicates on 192 frozen-pilot nodes, plus 3 stage-B runs of iteration 2. Every stage-A gate and score re-derives exactly from the recorded judgments. LLM layer errors: 0 everywhere.

Methodological changes, in order:
- iter01: the directive's design.
  - The gate order is state profile → scope → informative evidence → element with a contrast → relevance, with `contrast_direct` only.
  - The `has_contrast` requirement was added before any replicate ran. A first launch was stopped after about 1 minute with no case finished, and deleted.
- iter02:
  - scope v2: `invalid_or_underspecified` also covers "only weakly implied", as in the directive's own definition, which v1 had omitted;
  - element v2: the extractor no longer sees states and gives each candidate's position on the contrast variable. `has_contrast` is derived in code: the positions must contrast and agree with the states;
  - relevance v2: capability shown in another setting is `partly`.
  - Motivation: in iteration 1, all 6 scored nodes per replicate were reviewed failures.
- Iteration stopped after iter02. The same errors recur in every replicate and every iteration, and a further same-model prompt change aimed at 5 contested nodes would be label-fitting.

State preservation (prior v4 ×2 → iter01 ×3 → iter02 ×3):
- Indeterminate pair rate: 33%, 33% → 30–32% → 31–33%.
- Comparative profiles: 43, 48 → 50–55 → 46–52.
- D046 agreement: unqualified 20/20 throughout; all pairs 21/24 → 22–23/24 → 22/24.
- Between-replicate state-pair agreement (of 384): prior v4 365 → iter01 361–366 → iter02 364–370.

Scope, D045/D046 category × scope (iteration 2, summed over 3 replicates; columns hypothesis-specific / mechanism-specific / broader class / possibility / invalid):

| category | hyp | mech | broad | poss | invalid |
| --- | --- | --- | --- | --- | --- |
| genuine | 3 | 9 | 0 | 0 | 0 |
| silence error | 5 | 20 | 5 | 0 | 0 |
| generic fact | 3 | 5 | 16 | 18 | 0 |
| compatible | 15 | 15 | 6 | 0 | 0 |
| construct mismatch | 4 | 14 | 3 | 3 | 0 |
| weak implication | 6 | 0 | 3 | 3 | 0 |

`invalid_or_underspecified` was never assigned.

Reviewed generic facts, successfully gated:
- 14/14 in all iteration-2 replicates (iteration 1: 13/14 in all three; `gcn4-X23` scored).
- Scope made 11–12 of the 14 non-comparative; the rest were stopped by state profile or partial relevance. Per-node detail: report §3.

Reviewed genuine discriminators (`glnbp-X5`, `glnbp-X9`, `pfc_storage-X6`, `pfc_storage-X24`):
- Scope-eligible 4/4 in all 6 replicates.
- Comparative and scope-eligible 3–4/4.
- Relevance `contrast_partial` except `glnbp-X9` in iter02 rep3 (direct, scored).

Scored nodes by scope:
- Stage A: 100% hypothesis- or mechanism-specific (iter01 4 mech + 2 hyp per replicate; iter02 3 mech + 1–3 hyp). 0 broad or possibility.
- Stage B: 10 hypothesis-specific and 5 mechanism-specific across 15.

Contrast relevance on the 79 informative-evidence nodes (stage A):

| | direct | partial | context only | mismatch | no evidence | element without contrast |
| --- | --- | --- | --- | --- | --- | --- |
| iter01 | 24–26 | 51–53 | 0–1 | 1–2 | 0–1 | 7–8 |
| iter02 | 20–24 | 55–59 | 0–1 | 0 | 0 | 57–60 |

On eligible nodes with a contrast, iteration 2 had 4–6 direct and 4–7 partial.

Influence composition (|log-odds H2−H1|):

| category | v3 frozen | iter01 | iter02 |
| --- | --- | --- | --- |
| genuine | 8% | 0% | 0 / 0 / 13% |
| silence error | 22% | 40–45% | 63–84% |
| generic fact | 26% | 18–20% | 0% |
| compatible | 17% | 0% | 0% |
| construct mismatch | 7% | 11–19% | 0% |
| weak implication | 7% | 15–31% | 16–28% |
| unreviewed | 13% | 0% | 0% |
| total | 18.1 | 7.2–8.1 | 5.6–7.5 |

Prior v4 scored no node in stage A, so it has no composition.

Specificity × assessability (iteration 2):

| | P(informative evidence) | P(contrast-direct) |
| --- | --- | --- |
| hypothesis-specific | 30% | 6% |
| mechanism-specific | 46% | 17% |
| broader class | 52% | 9% |
| possibility | 42% | 15% |
| specific, all replicates of both iterations | 37–38% | — |
| broad, all replicates of both iterations | 48–50% | — |

`contrast_partial` sensitivity, iteration 2 (not the method):
- Scored nodes 5→12, 4→9, 6→10.
- Added: genuine 4, 4 and 2; generic facts re-entering 2, 1 and 2 (`eukaryogenesis-X6`, `gcn4-X23`); construct mismatch 1, 0 and 0.
- Genuine share 28%, 35% and 21%; silence share 35%, 44% and 43%.

Stability, iteration 2 pairwise:
- scored vs not: 191, 191, 190 of 192;
- scope class: 181–189 of 192;
- relevance: 73 of 79;
- `has_contrast`: 74–75 of 79.
- Case scores were identical across replicates in 5 of 8 cases (6 of 8 in iteration 1); ties in every replicate in 4 cases.

Stage B (runs `v4scope_explanatory_001/002/003`):
- 8/8 cases ok in each run, $4.61, $4.56 and $4.49.
- Recovery: 9/23, 10/23 and 10/23 (pilot, v3 rerun and prior v4: 11/23 each). Novel plausible discriminators: 3, 4 and 5.
- Scored nodes: 5, 6 and 4. Text-identical to reviewed failures: `glnbp-X4` (silence error) in all 3 runs, `glnbp-X11` (silence error) once, `eukaryogenesis-X6` (generic fact) twice.
- Case scores are unstable across runs:
  - eukaryogenesis 0.58/0.42, 0.16/0.84 and 0.35/0.65 (H1/H2);
  - GlnBP H2 0.84, 0.99 and 0.66;
  - PFC storage H2 0.52, 0.72 and 0.72;
  - spider: tie, 0.61/0.39, tie;
  - four cases tie in all runs.

Spend (list price, unverified): about $26.5 in total.
- stage-A replays, including the 1-case smoke test: $12.44;
- stage-B runs: $13.66;
- recovery auditor: about $2.23, estimated from token usage in `recovery_events.jsonl`;
- the stopped first launch: a small amount not captured in the ledger.

TESTS_AND_EVIDENCE:
- `python3 -m pytest tests/ -q`: 651 passed, 1 xfailed (the pre-existing strict xfail on the merger defect).
- The v4-scope, v4-scope analysis and v4 discrimination test files: 142 passed.
- Stage-A replays: `python3 scripts/replay_v4_on_frozen.py --layer v4_scope --replay-id v4scope_replay_iter0{1,2}{,_rep2,_rep3}`. Before each run, the frozen pilot archive is extracted and checked against its SHA256SUMS by `build_review_packet.extract_verified`.
- Analysis: `python3 scripts/analyze_v4_scope.py --replay runs/v4scope_replay_iter0N{,_rep2,_rep3} --name iter0N`. Its consistency section reports `ok` for all 6 replicates: every gate reason, `used_in_score` and case score re-derived from recorded judgments with the committed gate code.
- Stage B: `python3 -m src.experiments.run --method consequence_graph_v4_scope --config configs/v4_dev_explanatory.yaml --run-id v4scope_explanatory_00N`, then `python3 scripts/analyze_pilot_recovery.py --run runs/v4scope_explanatory_00N --workers 6`, then `python3 scripts/compare_v4_scope_runs.py`.
- Report: `python3 scripts/build_v4_scope_report.py`.
- Run manifests were checked. At every run start, no run-relevant path was uncommitted: dirty paths were only the cost ledger, docs and analysis scripts/outputs. The exception is the 1-case wiring smoke test, which ran before the layer was committed.
- Archive:
  - `benchmark/frozen_runs/v4_scope_runs/v4_scope_runs.tar.gz`, SHA-256 `d09257cb…1cddda`, 473 files;
  - extracted into a scratch directory and verified file by file against SHA256SUMS;
  - second copy in `/mnt/data/knk25.data/private_artifacts/v4_scope_runs/` with a matching hash;
  - `git check-ignore` confirms the tarball is ignored.
  - Manifests record only true/false presence flags for API-key environment variables, no secret values.
- Key claims were checked by hand against the recorded judgments:
  - `glnbp-X4` states, positions and relevance rationale (report §11), and the candidate texts in `benchmark/explanatory/cases_visible.jsonl`;
  - prior-v4 gate reasons for the four comparative silence errors (construct `partial` or `mismatch` in both prior-v4 replicates);
  - the stage-B paraphrase reading, done by listing each unmatched scored proposition beside all reviewed pilot propositions of its case.

DECISIONS_AND_ASSUMPTIONS:
- Human decision for this directive: iterate on 3 stage-A replays per iteration, then run 3 fresh end-to-end runs once for the final version. Followed.
- A new method version was built (`consequence_graph_v4_scope`) rather than modifying `consequence_graph_v4`, so prior v4 remains reproducible.
- Scope for every proposition; element and relevance for every proposition with informative evidence and states, not only eligible ones. This is so the §10 assessability table covers all scopes. Only the gate decides what scores.
- The scope prompt sees the research question, because scope is relative to the system under dispute. The state prompt still does not see it.
- Categories are derived in code from structured answers, never from a holistic label:
  - relevance comes from Q1–Q3;
  - element v2 `has_contrast` requires positions that contrast and agree with the states.
  - Q1 `yes` with Q3 `yes` is kept as `contrast_direct` and counted separately; it never occurred.
- Iteration 2 was chosen as the final version, before stage B, on stage-A structural criteria:
  - it removes generic, compatible and construct-mismatch influence;
  - it gates all 14 generic facts;
  - it keeps the genuine discriminators eligible;
  - it is equally stable.
  - Its higher silence-error share reflects the same persistent errors over a smaller total.
- Iteration was stopped at 2 because the remaining errors are identical across iterations and replicates, and further same-model prompt changes would target ≤5 contested nodes. This is a judgement, not a directive rule.
- No numeric mapping changed; `indeterminate` contributes zero; no held-out case, hidden annotation or ResearchBench reserve was used.
- Later-resolution direction appears in the report only as a descriptive column; it was not used in any decision.
- Stage-B label transfer uses exact text only. The paraphrase reading in the report is the executor's and is explicitly marked as not labels.
- Consequence discovery is judged "largely preserved" (9–10 vs 11 of 23). The drop is not attributable to the layer, but it is consistent across the 3 runs.

UNCERTAINTIES_AND_LIMITATIONS:
- **Label base.** D045/D046 are model-based development labels on 52 of 192 nodes, with only 4 genuine discriminators, so composition shares rest on very few nodes.
  - The five recurring scored errors carry primary-category labels only (all five are D045 labels, with no per-hypothesis states recorded).
  - At least `glnbp-X4` is a subtle reading. The proposition says apo-GlnBP *adopts* a closed conformation; one candidate says it *samples* one.
  - If these labels change, the influence picture changes substantially.
- **One model.** All judgments use gpt-4.1 at temperature 0, so replicate variation is sampling nondeterminism, not model diversity. The element-v2 "independent" check turned out not to be independent.
- **Evidence reuse in stage A.** Replays reuse the frozen v3 evidence labels and cited records, and the relevance judge sees only those records.
- **Confounded iteration.** Iteration 2 changed three prompts at once, so their separate effects are not identified. The relevance-v2 clause may explain why broad propositions' direct rate fell.
- **Stage-B instability.** 4–6 scored propositions per run; case outcomes flip between runs.
- **Recovery auditor.** It is an LLM judgment with a known bias toward "silence" (pilot report).
- **Costs.** List-price estimates. The auditor cost is estimated from tokens, and the stopped launch is not in the ledger.

PROBLEMS_OR_RISKS:
- **Residual failure is implication-side.** Silence errors and weak implications carry most remaining influence (63–84% silence in stage A), and the same readings recur in every replicate, iteration and stage-B run. The scope and relevance layers cannot see this failure. Prompt changes within this directive's allowed levers did not decorrelate it, because the same model reproduces the reading.
- **Evidence-policy dilemma persists.** Direct-only leaves genuine discriminators almost always unscored. Allowing partial evidence admits them but also admits generic facts and keeps silence errors dominant.
- **Scope misclassification in live runs.** A reviewed generic fact (`eukaryogenesis-X6`) was classified `hypothesis_specific` and scored in 2 of 3 fresh runs.
- **Abstention and instability.** In 4 of 8 cases the method ties in every run; where it does decide, 1–3 propositions decide the case and directions can flip between runs.
- **Consequence recovery dipped slightly.** 9–10/23 in all 3 v4-scope runs vs 11/23 in all 3 earlier runs. It is not attributable to the method, but it should be watched.
- **Token still exposed (standing).** The git remote URL still embeds a GitHub token; printed git output was redacted.

QUESTIONS_FOR_DIRECTOR:
1. Should the next iteration target the implication side directly? For example, a determinate contrast could be required to be confirmed by an independent judge (a different model family) before a proposition may score. Same-model re-asking reproduced the errors in this task.
2. Should the five recurring scored nodes (`glnbp-X4`, `glnbp-X11`, `pfc_storage-X2`, `eukaryogenesis-X7`, `forest-X15`) be re-adjudicated with per-hypothesis states, ideally by a domain expert? D045 recorded only primary categories for all five, and `glnbp-X4` turns on "adopts" vs "samples".
3. What is the evidence policy for `contrast_partial`: stay excluded, admit with a separately justified discount (a numeric-mapping decision this task did not make), or report as a secondary score?
4. Is abstention (ties when no contrast-direct pre-cutoff evidence exists) acceptable as a primary outcome? If so, should held-out evaluation measure coverage alongside direction?

RECOMMENDED_NEXT_ACTION:
Do not freeze v4-scope for held-out evaluation.

Recommendation only:
1. Keep the scope layer and the contrast-bearing element. They do what they were designed for and are stable.
2. Next, address the implication side with a decorrelated check on determinate contrasts. One option: a second model family must agree on each candidate's position on the contrast variable. Validate it on the same 8 spent cases, after the recurring contested nodes have been re-adjudicated with per-hypothesis states.
3. Keep `contrast_direct` as the main policy until a Director decision on partial evidence.

ARTIFACTS:
- Report: `docs/V4_SCOPE_REPORT.md`.
- Design: `docs/V4_SCOPE_DESIGN.md`.
- Stage-A metrics: `benchmark/v4_scope/iter01/development_metrics.json`, `benchmark/v4_scope/iter02/development_metrics.json`.
- Stage-B comparison: `benchmark/v4_scope/stage_b/run_comparison.json`.
- Method: `src/methods/consequence_graph_v4_scope.py`, `src/graph/proposition_scope.py`, `src/evidence/contrast_relevance.py`, `src/inference/discrimination.py` (gate_node_scope section).
- Prompts: `src/llm/prompts/proposition_scope_v{1,2}.txt`, `src/llm/prompts/contrast_element_v{1,2}.txt`, `src/llm/prompts/contrast_relevance_v{1,2}.txt`.
- Tests: `tests/test_v4_scope.py`, `tests/test_v4_scope_analysis.py`.
- Scripts: `scripts/analyze_v4_scope.py`, `scripts/compare_v4_scope_runs.py`, `scripts/build_v4_scope_report.py`, `scripts/replay_v4_on_frozen.py` (`--layer v4_scope`).
- Runs (gitignored, archived privately):
  - `runs/v4scope_replay_smoke_glnbp`;
  - `runs/v4scope_replay_iter01{,_rep2,_rep3}`;
  - `runs/v4scope_replay_iter02{,_rep2,_rep3}`;
  - `runs/v4scope_explanatory_00{1,2,3}`, including `recovery.json`.
- Archive checksums: `benchmark/frozen_runs/v4_scope_runs/{MANIFEST.md, SHA256SUMS, v4_scope_runs.tar.gz.sha256}`.
- Private archive: `benchmark/frozen_runs/v4_scope_runs/v4_scope_runs.tar.gz`, with a copy in `/mnt/data/knk25.data/private_artifacts/v4_scope_runs/`.
