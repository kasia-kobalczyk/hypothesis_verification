TASK_ID: BENCH-GRAPH-V4-DEV-001
STATUS: BLOCKED

SUMMARY:
v4 (`consequence_graph_v4`) was implemented as a versioned method on top of the unchanged v3 pipeline. It adds:
- explicit per-hypothesis prediction states, kept separate from strength;
- a deterministic discrimination gate;
- element-wise construct matching;
- gated scoring through the verifier's own `score_hypotheses`.

`indeterminate` never has a likelihood. One-sided, shared and all-indeterminate propositions are kept descriptively and contribute zero.

It was developed on the eight spent cases in two stages:
- **Stage A:** three iterations, each replayed twice on the frozen v3 pilot, so propositions and evidence are identical to v3.
- **Stage B:** an end-to-end v4 run, plus an unchanged v3 re-run as a noise floor.

The directive cannot be completed (criterion 10, freeze) without a Research Director decision, so v4 was NOT frozen. The human made two decisions during the task, both recorded:
- only `direct` construct matches may score, chosen before any results;
- after iteration 2: fix the state side only, keep direct-only, do not freeze, and escalate the evidence policy to the Director.

What was learned:
1. **The state classifier gets the reviewed silence judgments right** (20/20 unqualified D046 states in every replicate), and v4 removes the categorical silence errors and neutral-mapping pseudo-discrimination by construction. Compatible propositions and weak implications drop to zero influence.
2. **It still gives determinate contrasts to class-level and possibility claims** ("ligand binding *can* occur in periplasmic binding proteins…"). An advisory scope rule (iteration 2) did not remove them. An explicit, gated scope field (iteration 3) made the classifier assign *more* contrasts and lowered stability, so the head was reverted to iteration 2.
3. **Under direct-only with element-wise construct matching, nothing scores on any development case** in either replicate. All four D045 genuine discriminators are eligible but blocked as `partial`.
4. **In the live v4 run, the only 3 propositions that scored are class-level "can occur" claims**, one of them text-identical to a pilot proposition D045 labelled `generic_component_fact`. Both of v4's live "agreements" with later resolutions (eukaryogenesis, GlnBP) rest on them. Construct gating favours generic facts, which abstracts state outright, over specific discriminators, which they rarely fully establish.
5. **Allowing `partial` evidence would not fix this:** 16–30 nodes would score per replicate, only 2–4 of them genuine discriminators.
6. **v3's case-level outcomes are not reproducible.** An unchanged v3 re-run flipped two of the four directional cases (PFC storage 0.23→0.68 toward H2; fly-wing 0.58→0.42), although generation and graph structure were stable (87 vs 84 sign-opposed nodes).
7. **Consequence discovery is unchanged:** 11/23 reference discriminators recovered in the frozen pilot, the v3 re-run and the v4 run.

CHANGES:
Commits on `master` since the directive (`3a1ca78`), with dates:
- `f9ff82f`: D046 labels transcribed mechanically; v3 attribution recomputed under D045+D046 (`attribution_d045_d046/`), including the D046 split between categorical silence errors and neutral-mapping pseudo-discrimination.
- `f95195a`: run manifests now record git state, and record the case manifest actually read for `kind: cases` (provenance only).
- `83b707f`: v4 iteration 1.
  - New: `src/inference/discrimination.py`, `src/graph/prediction_state.py`, `src/evidence/construct_match.py`, `src/methods/consequence_graph_v4.py`.
  - Prompts `prediction_state_v1`, `construct_match_v1`.
  - Runner registration and artifacts; aggregator counters.
  - `configs/v4_dev_explanatory.yaml` (differs from the pilot config only in `dataset.status: development`).
  - `scripts/replay_v4_on_frozen.py`; tests.
- `7f4718b`: iteration 2. `prediction_state_v2` adds a scope rule; `construct_match_v2` is element-wise with the gating label derived in code. Plus `scripts/analyze_v4_development.py`.
- `6817782`: iteration 3. `prediction_state_v3` adds an explicit, required scope field; the gate treats out-of-scope propositions as `generic_or_possibility_claim`. Plus iteration 1–2 metrics and `docs/V4_DESIGN.md`.
- `a770f94`: development head reverted to `prediction_state_v2` + `construct_match_v2`. The v3 prompt and scope gate remain implemented and tested but inactive.
- `fd1b248`: partial-evidence sensitivity by category, report generator, stage-B comparison script.
- Final commit (this report): stage-B comparison, `docs/V4_DEV_REPORT.md`, private-run checksum manifest.

Not modified: v3 code path (`src/methods/consequence_graph.py`, v3 prompts; frozen prompt SHAs still pass), `configs/mvp.yaml`, `configs/pilot_explanatory.yaml`, `configs/ordinal_mappings.yaml`, `.agent/DIRECTIVE.md`, `PROJECT_STATE.md`, `DECISIONS.md`, and hidden benchmark annotations. No held-out case was used.

RESULTS:
Configuration:
- All LLM roles: Azure `gpt-4.1-kasia`, api_version 2024-05-01-preview, temperature 0, seed 20260911.
- Literature: Semantic Scholar with Crossref date verification.
- Development head: `prediction_state_v2`, `construct_match_v2`, construct policy direct-only, frozen `v0-placeholder` mappings, `independent` aggregation passed explicitly.

Development iterations: 3, plus a revert of the head. Every stage-A iteration was replayed twice.

| iteration | change | why |
|---|---|---|
| 1 | initial design | — |
| 2 | scope rule; element-wise construct match, label derived in code | reviewed generic facts scored via class-level contrasts; PFC X15 (a D045 mismatch) judged `direct`; single construct flips swung cases |
| 3 | explicit, gated scope field | 5/14 reviewed generic facts still eligible |
| head | back to iteration 2 | iteration 3 regressed on both replicates |

No case-specific rule, no answer leakage, no numeric change, no policy change.

Stage A, per replicate (192 nodes):

| iteration | pairs indeterminate | comparative / one-sided / shared / out-of-scope | scored | construct direct/partial/mismatch | stability: states / construct |
|---|---|---|---|---|---|
| 1 | 33% | 47/113/26/0 · 44/119/26/0 | 5 · 5 | 10/63/6 · 9/64/6 | 366/384 · 76/79 |
| 2 | 33% | 43/120/25/0 · 48/117/23/0 | 0 · 0 | 5/71/3 · 6/69/4 | 365/384 · 75/79 |
| 3 | 30% | 62/92/26/10 · 64/89/25/12 | 3 · 2 | 8/68/3 · 6/70/3 | 354/384 · 75/79 |

v3 on the same 78 score-moving nodes (edges read as states): 19% `neutral`; 40 sign-opposed, 29 one-sided, 9 shared. v3 scored every node with an evidence label.

Alignment with D045/D046 (eligible / scored, rep1 · rep2):

| category (n) | iteration 1 | iteration 2 (head) | iteration 3 |
|---|---|---|---|
| genuine (4) | 3/1 · 2/0 | 3/0 · 4/0 | 4/0 · 4/0 |
| silence error (10) | 4/1 · 4/1 | 4/0 · 4/0 | 6/0 · 6/0 |
| generic fact (14) | 5/2 · 6/3 | 5/0 · 5/0 | 8/1 · 8/2 |
| compatible (12) | 0/0 · 0/0 | 0/0 · 0/0 | 2/1 · 2/0 |
| construct mismatch (8) | 3/1 · 1/1 | 3/0 · 3/0 | 3/1 · 3/0 |
| weak implication (4) | 2/0 · 2/0 | 1/0 · 1/0 | 3/0 · 2/0 |

- **Prediction-state confusion against D046:** unqualified states 20/20 in all six replicates; all states including the 4 qualified ones, 21–22/24.
- **Silence errors now gated:** 9/10 (iteration 1), 10/10 (iteration 2).
- **Genuine discriminators:**
  - Head: all 4 eligible in rep2, 3 in rep1 (PFC X24 was one-sided once), all blocked `construct_partial`.
  - Iteration 1: PFC X24 scored once.

Score-influence composition (|log-odds|):

| category | v3 frozen | iteration 1 | iteration 2 (head) | iteration 3 |
|---|---|---|---|---|
| genuine | 1.47 (8%) | 1.46 · 0 | 0 · 0 | 0 · 0 |
| silence error | 4.02 (22%) | 1.63 · 1.63 | 0 · 0 | 0 · 0 |
| generic fact | 4.67 (26%) | 1.91 · 2.87 | 0 · 0 | 1.46 · 2.20 |
| compatible | 3.08 (17%) | 0 · 0 | 0 · 0 | 0.96 · 0 |
| construct mismatch | 1.28 (7%) | 1.46 · 1.46 | 0 · 0 | 1.46 · 0 |
| weak implication | 1.24 (7%) | 0 · 0 | 0 · 0 | 0 · 0 |
| unreviewed | 2.32 (13%) | 0 · 0 | 0 · 0 | 0 · 0 |
| total | 18.07 | 6.47 · 5.96 | 0 · 0 | 3.88 · 2.20 |

Counts of what was gated:
- **One-sided propositions gated (head):** 120 and 117 of 192.
- **Shared:** 25 and 23.
- **Construct blocks on eligible propositions:** 20 and 19 (18 `partial` each, plus 2 and 1 `mismatch`).
- **Construct labels over all informative evidence:** 71/69 partial, 3/4 mismatch.

Partial-evidence sensitivity (sensitivity only, not the policy): nodes that would score, by category, 16–19 in iterations 1–2 and 28–30 in iteration 3, of which genuine discriminators are 2–4. Case scores would also be unstable between replicates (eukaryogenesis 0.20 vs 0.85 in iteration 2).

Stage B, end-to-end runs:

| run | cost | ok/error | nodes | abstraction mix | v3 sign-opposed nodes | reference discriminators recovered |
|---|---|---|---|---|---|---|
| frozen pilot | $2.75 | 8/0 | 192 | 64/64/64 | 87 | 11/23 (7 cases) |
| v3 re-run | $2.71 | 8/0 | 192 | 65/63/64 | 84 | 11/23 (6 cases) |
| v4 run | $3.76 | 8/0 | 192 | 64/64/64 | 84 | 11/23 (7 cases) |

The v4 run had 3 retrieval rate-limit errors (Semantic Scholar), recorded as errors and not as no-evidence.

Per-case P(H2) (frozen v3 / v3 re-run / v3 scoring on the v4 run's graph / v4):

| case | frozen v3 | v3 re-run | v3 on v4 graph | v4 |
|---|---|---|---|---|
| eukaryogenesis | .92 | .82 | .86 | .71 |
| fly-wing | .58 | .42 | .56 | .50 |
| forest | .16 | .18 | .06 | .50 |
| gcn4 | .50 | .22 | .44 | .50 |
| GlnBP | .86 | .88 | .96 | .95 |
| PFC interhemispheric | .38 | .35 | .41 | .50 |
| PFC storage | .23 | .68 | .66 | .50 |
| spider | .58 | .64 | .76 | .50 |

The v4 run scored exactly 3 propositions:
- eukaryogenesis X16, "An archaeal cell lacking mitochondria can possess a dynamic actin cytoskeleton";
- GlnBP X2 and X8, "Ligand binding (to a substrate-binding protein / to the open conformation of periplasmic binding proteins) can occur before a conformational change". X8 is text-identical to pilot X8, labelled `generic_component_fact`.

Per-case qualitative changes (head, stage A):
- **PFC storage:** silence and construct-mismatch support for storage is suppressed, but the genuine control-favouring discriminators are blocked by construct `partial`, so the case ties.
- **GlnBP:** the silence-driven induced-fit advantage disappears in stage A (tie). In the live run, induced fit returns via family-level "can" claims.
- **Eukaryogenesis:** generic component facts no longer dominate in stage A (tie). In the live run, one possibility claim scores.
- **Fly-wing:** the silence-driven apparent success disappears (tie).
- **Mixed and regime-dependent cases:** all tie; none were forced into a binary.

Consequence discovery: preserved. Generation is unchanged in v4, and all generation and discovery statistics are within the v3 run-to-run range.

Freeze readiness: not ready.
- **Met:** acceptance criteria 1–7 and 9.
- **Criterion 8, not met usably:** failure categories lose influence in stage A only because nothing scores, genuine discriminators are unusable, and in the live run only generic/possibility claims scored.
- **Criterion 10:** withheld pending the Director.

TESTS_AND_EVIDENCE:
- `python3 -m pytest tests/ -q`: 569 passed, 1 xfailed (the pre-existing strict xfail).
  - `tests/test_v4_discrimination.py` (60 tests) covers:
    - profile classes per the directive; `indeterminate` is not `substantive_null`; a missing hypothesis is an error, not indeterminate;
    - k>2 with an indeterminate hypothesis is never eligible; `indeterminate` has no likelihood; determinate states need a strength; state→label mapping uses only the frozen scale;
    - only `direct` construct matches score; one-sided propositions never score, even with strong direct evidence; missing states or construct fail closed;
    - one-sided support leaves scores exactly 0.5/0.5, and the D046 neutral-mapping case moves v3 but not v4;
    - a contrast's log-odds equals the closed form; blocked nodes contribute nothing; malformed LLM output is rejected;
    - the construct label is derived from elements, and the holistic impression never overrides it;
    - the scripted-LLM layer keeps ineligible nodes descriptively and fails closed on LLM errors;
    - the scope gate (implemented, inactive at head); the head uses the iteration 2 prompt;
    - v3 and v4 are both registered and distinct; v4 prompts obey the hidden-annotation and cutoff invariants; v4 code never names hidden annotations; the dev config differs from the pilot config only in status.
  - Tests for D046 transcription and combined attribution (packet 27, attribution 22) were added earlier in this task.
- The live v4 integration was checked on the first completed case (all artifacts, no errors) and then over 8/8 cases.
- The stage-A replays are node-identical to the frozen pilot; `analyze_v4_development.py` aborts if the replay nodes differ.
- Private run archive: 9 runs, 315 files, verified by extraction.
- Spend at unverified list prices: runs $6.47 + replays $6.60 + recovery auditor $1.50 ≈ **$14.60**.

DECISIONS_AND_ASSUMPTIONS:
- **v4 wraps v3 rather than editing it.** It calls v3's `run_instance`, then replaces scoring. This is the least invasive route and keeps v3 scores on the same graph as `scores_v3_reference`.
- **The prediction-state prompt excludes the research question,** as v3's edge assessor did, to avoid "A or B?" framing pressure.
- **Chain edges are not used in v4 scoring,** so no inherited predictions. `substantive_null` scores on the negative side of the frozen scale. Positive vs positive at different strengths is `shared`. For k>2, any indeterminate hypothesis makes the proposition ineligible (the pilot is k=2).
- **Construct match sees cited records only,** or all shown records if none were cited, and never sees the evidence label or rationale.
- **Human decisions** (recorded in memory and here): direct-only, chosen before results; a v3 noise-floor re-run; after iteration 2, state-side fixes only, no freeze, escalation.
- **D045/D046 were used diagnostically.** No change targeted a specific node. Iteration choices were compared on pooled replicates because single-run case outcomes flip on single judgments.
- **The head reverted to iteration 2** by its pre-stated criterion: fewest reviewed failure-category nodes eligible while genuine discriminators stay eligible.

UNCERTAINTIES_AND_LIMITATIONS:
- **All reviewed-category metrics depend on D045/D046,** first-pass model-based review with no human expert. The live v4 run's propositions are unreviewed; the exact-text match covers only 1 of 3.
- **n = 8 development cases, 4 directional.** Magnitudes rest on placeholder mappings.
- **Run-to-run variance is large at case level for both v3 and v4.** Replicates show ~5% state flips and ~4% construct flips, enough to move a case when few nodes score.
- **The construct judge's `partial` rate (~85–90% of informative evidence)** may partly reflect abstract-only evidence (no full texts) rather than genuine construct gaps. Not tested.
- **Stage B is one v4 run and one v3 re-run;** stage-B conclusions are single-run.
- **The v4 run has 3 retrieval rate-limit errors** (eukaryogenesis X7, X9; GlnBP X14).

PROBLEMS_OR_RISKS:
- **v3 defects found, not fixed** (the directive forbids changing v3; documented in `docs/V4_DESIGN.md` §8):
  1. `inference.aggregation` is never passed to `score_hypotheses` (config ignored; runs were `independent`, as configured);
  2. `evidence_assess_v2` claims supporting spans are checked automatically, and nothing checks them;
  3. root-edge validation does not require every hypothesis, so a missing one becomes 0.5;
  4. a duplicate `_finalise` in `bayes.py`, and a stale `ASSESS_PROMPT` constant pinned by a test.
- **v3 pilot conclusions that relied on case-level direction (e.g. "3/4 agree") are within run-to-run noise.**
- **Private archives** (pilot and development runs) exist only on the execution host; off-host private storage is still needed.
- **The git remote URL still embeds a GitHub token.**

QUESTIONS_FOR_DIRECTOR:
1. **Evidence-directness policy** (the blocking decision). Direct-only with faithful element-wise matching scores nothing on the development cases, and where it scores in a live run it selects class-level "can" claims. `partial` re-admits mostly reviewed failures. Should v4 require:
   - (a) direct only, accepting abstention;
   - (b) direct or partial;
   - (c) a narrower rule, e.g. `direct` only for the element that carries the cross-hypothesis contrast (would need its own design and development);
   - (d) or should comparative scoring be paused until the state side is fixed?
2. **State-side approach.** Prompt refinement did not remove contrasts on class-level and possibility claims, and iteration 3 regressed. Should the next attempt move this out of the per-hypothesis prompt, e.g. a separate scope classifier with its own validation labels, or restricting generation of class-level "can" propositions from comparative use? The directive asks that mechanistic/class-level generation be preserved, so this needs a direction.
3. **Development labels.** Should D045/D046-style review be extended with scope labels (within / broader / possibility) for the reviewed nodes? That would let a scope classifier be validated rather than inferred from outcomes.
4. **Case-level variance.** Given v3's flips on re-run, should future evaluation use multiple runs per case, with case outcomes reported as distributions?

RECOMMENDED_NEXT_ACTION:
(Recommendation only.)
1. Decide the evidence policy (Q1) before any freeze. My recommendation is (d): keep v4's gate, and treat scoring as not yet valid until class-level and possibility claims can no longer receive determinate contrasts.
2. Collect scope labels for the reviewed nodes (Q3), then develop and validate scope classification separately from prediction states.
3. Adopt replicate runs for any case-level claim, v3 or v4.
4. Arrange off-host private storage for the run archives.

ARTIFACTS:
- Design: `docs/V4_DESIGN.md`
- Development report (generated): `docs/V4_DEV_REPORT.md` (`scripts/build_v4_dev_report.py`)
- Code:
  - `src/methods/consequence_graph_v4.py`
  - `src/inference/discrimination.py` (prediction-state schema, gate, gated scoring)
  - `src/graph/prediction_state.py`
  - `src/evidence/construct_match.py`
- Prompts: `src/llm/prompts/prediction_state_v1|v2|v3.txt`, `construct_match_v1|v2.txt` (head: v2/v2)
- Config: `configs/v4_dev_explanatory.yaml`
- Tests: `tests/test_v4_discrimination.py`, `tests/test_review_packet.py`, `tests/test_review_attribution.py`
- Stage A:
  - `scripts/replay_v4_on_frozen.py`, `scripts/analyze_v4_development.py`
  - metrics: `benchmark/v4_dev/iter01|iter02|iter03/development_metrics.json`
- Stage B: `scripts/compare_v3_v4_runs.py`, `benchmark/v4_dev/stage_b/run_comparison.json`
- D046 labels and v3 attribution:
  - `benchmark/review/graph_pilot_001/human_labels_D046.json`
  - `benchmark/review/graph_pilot_001/attribution_d045_d046/`
  - `scripts/transcribe_decision_labels.py`
- Run paths (gitignored; private archive `benchmark/frozen_runs/v4_dev_runs/`, SHA-256 `5f7f0ffe…529d`, second copy `/mnt/data/knk25.data/private_artifacts/v4_dev_runs/`):
  - `runs/v3_rerun_explanatory_001`
  - `runs/v4_dev_explanatory_001`
  - `runs/v4_replay_smoke_pfc`
  - `runs/v4_replay_pilot_iter01`, `_rep2`
  - `runs/v4_replay_pilot_iter02`, `_rep2`
  - `runs/v4_replay_pilot_iter03`, `_rep2`
