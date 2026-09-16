TASK_ID: BENCH-GRAPH-REVIEW-001
STATUS: COMPLETED

SUMMARY:
The frozen eight-case pilot run is preserved byte-for-byte in a checksummed archive, with a provenance record. The dirty working tree it ran from was reconstructed as `9559b30` plus a one-hunk, cosmetic patch. The patch is verified against the run's own console log and the session transcript's edit history.

From that archive, a deterministic, LLM-free builder produced the human review packet:
- **Full set:** 78 score-moving nodes out of 192 generated.
- **Priority set:** 40 nodes covering 80.1% of total absolute score influence, selected from verifier contributions only.
- **Per record:** exact hypotheses, every cross-hypothesis edge route, byte-exact evidence text cut from the rendered assessor prompts, per-node contributions, exact single-node counterfactuals, non-authoritative auditor metadata, and blank human fields.
- **Hidden resolutions:** kept in a separate labelled appendix.

Twenty tests check that the packet is faithful to the frozen run. The verifier was not changed and nothing was rerun.

**Publication, per human decision:** the review packet, checksums, provenance record and tooling are pushed to `master`. The run archive itself is **private**: gitignored, never committed, and kept on the execution host. It contains full model traffic and about 3,800 third-party abstracts.

CHANGES:
Commit `3ff5a38`: preservation record.
- `.gitignore`: adds `benchmark/frozen_runs/*/*.tar.gz`, so run archives stay private.
- `benchmark/frozen_runs/pilot_explanatory_001/` (tracked):
  - `pilot_explanatory_001.tar.gz.sha256`
  - `SHA256SUMS`
  - `file_manifest.json`: per-file size, mtime and kind
  - `PROVENANCE.md`
  - `runtime_source.patch`
- `pilot_explanatory_001.tar.gz` (8.8 MB, 149 files): **private, not tracked.** It is in the same directory on the execution host, plus a second copy at `/mnt/data/knk25.data/private_artifacts/pilot_explanatory_001/` (checksum verified).

Commit `056280e`: review packet and tooling.
- `scripts/build_review_packet.py`: deterministic builder. It imports only the verifier's graph schema and scoring code (read-only), and nothing from `src/llm`.
- `tests/test_review_packet.py`: 20 sanity checks. The 18 that need the frozen run skip, with a pointer to `PROVENANCE.md`, wherever the private archive is absent; verified by removing it temporarily.
- `benchmark/review/graph_pilot_001/`:
  - `README.md`, `RUBRIC.md`
  - `review_priority.md`, `review_full.md`
  - `review_set_priority.jsonl`, `review_set_full.jsonl`
  - `hidden_case_context.md`, `hidden_case_context.json`
  - `stats.json`

Also this report (`.agent/EXECUTOR_REPORT.md`).

Not modified:
- `src/`, `configs/`: `git diff 4123d52 -- src configs` is empty.
- `.agent/DIRECTIVE.md`, `PROJECT_STATE.md`, `DECISIONS.md`.
- `runs/pilot_explanatory_001/`: still matches `SHA256SUMS`.

Outside the repository, on the execution host:
- `/mnt/data/knk25.data/private_artifacts/pilot_explanatory_001/`: second copy of the archive.
- `/mnt/data/knk25.data/pilot_explanatory_001_scratch_holding/`: loose copies of the scratch-only files, which are also inside the archive.

RESULTS:
## Preservation
- Original run path: `runs/pilot_explanatory_001` (gitignored), 2026-09-15T15:28:51Z–16:38:35Z.
- Preserved path: `benchmark/frozen_runs/pilot_explanatory_001/pilot_explanatory_001.tar.gz` (private, gitignored; second copy under `/mnt/data/knk25.data/private_artifacts/`). The checksums and manifest are tracked publicly.
  - Archive SHA-256: `dd7e13610afd5eb4bdca78bdf3a4fa91d630142e69f900c4b019a673b754568e`
  - Mapping: `runs/pilot_explanatory_001/` → `run/`; executor scratch → `supplementary_scratch/`.
  - Verified by extracting the archive and checking all 149 per-file checksums.
- File kinds in `file_manifest.json`:
  - 112 `verifier_run_output` files (written during the run);
  - 13 `post_hoc_analysis` files (written 2026-09-16; LLM auditor outputs and second-rater ratings);
  - 24 `supplementary_scratch` files. These are the only copies of the run console log, the auditor retest pass on `pfc_storage_vs_control`, and the raw blind second-rater ratings. They lived only in `/tmp` before this task.
- Model/provider per role:
  - All 5 verifier roles (generate, root_edge, chain_edge, proposition_query, evidence_assess): Azure `gpt-4.1-kasia`, api_version 2024-05-01-preview, temperature 0.0, top_p 1.0, seed 20260911, JSON mode.
  - Prompt SHAs from the run manifest equal the freeze.
  - Literature: Semantic Scholar; Crossref date verification `always`.
  - The ordinal mappings recorded in all 8 `scores.json` equal `configs/ordinal_mappings.yaml` (`v0-placeholder`).
- Git commits created: `3ff5a38` (preservation record) and `056280e` (packet and tooling), plus this report. All are pushed to `master`. The archive bytes are in no commit, verified with `git rev-list --objects`.
- Dirty working tree:
  - The run came from uncommitted changes on `c18edc2`, and its manifest records no commit.
  - Reconstruction: `git show 9559b30:src/experiments/runner.py` plus `runtime_source.patch`, which reverts one log-message wording change made at 15:35:51Z during the run.
  - Evidence:
    - The transcript shows no other write to verifier code during the run window.
    - The run log's warning line matches the reconstructed code exactly.
    - Audit prompts were briefly present in the prompt directory (15:31–15:36Z), but the run manifest lists only the 5 frozen prompts.
  - The change is cosmetic and cannot have affected results.

## Review-set statistics (exact, recomputed from the archive)
- Total generated nodes: 192.
- Score-moving nodes: 78. A node counts when its log-likelihood contributions differ between the two hypotheses (it moves the log-odds).
  - Excluded: 1 node (`fly_wing` X4) that adds an equal, nonzero amount to both hypotheses.
  - The packet's contributions sum to each case's frozen log-odds.
- Priority set: 40 nodes, 80.1% of total absolute influence (total 18.07 log-odds units).

| case | generated | score-moving | priority | share of influence | single removals that flip ranking (withheld / deleted) |
|---|---|---|---|---|---|
| eukaryogenesis_mito_timing | 24 | 15 | 8 | 21.6% | 0 / 0 |
| fly_wing_constraint_vs_selection | 24 | 2 | 1 | 1.7% | 0 / 0 |
| forest_fragmentation_resilience | 24 | 18 | 7 | 18.3% | 0 / 0 |
| gcn4_med15_complex_vs_condensate | 24 | 11 | 5 | 11.7% | 7 / 6 |
| glnbp_induced_fit_vs_conformational_selection | 24 | 11 | 9 | 23.8% | 0 / 0 |
| pfc_interhemispheric_architecture | 24 | 3 | 1 | 3.2% | 0 / 0 |
| pfc_storage_vs_control | 24 | 11 | 7 | 14.8% | 0 / 0 |
| spider_orb_web_origin | 24 | 7 | 2 | 4.9% | 0 / 0 |

Direct edge-label pattern (the generating hypothesis's label | the other hypothesis's label):

| pattern | full set (78) | priority set (40) |
|---|---|---|
| implied \| neutral | 26 | 5 |
| implied \| unlikely | 21 | 18 |
| strongly_implied \| unlikely | 19 | 14 |
| implied \| implied | 3 | 0 |
| strongly_implied \| neutral | 2 | 1 |
| strongly_implied \| weakly_implied | 2 | 2 |
| implied \| weakly_implied | 2 | 0 |
| strongly_implied \| implied | 2 | 0 |
| neutral \| implied | 1 | 0 |

- **Hypothesis that did not generate the proposition got a non-`neutral` direct label:** 50/78 nodes in the full set, 34/40 in the priority set.
  - This is a mechanical count, not a finding of error: a non-generating hypothesis may legitimately predict or deny a proposition.
  - In the priority set, 32/40 non-generating labels are `unlikely`.

## Existing auditor comparison (non-authoritative)
- **Primary recovery auditor, within the review set:**
  - Full set (78): silence_as_null_error 62, reference_discriminator_recovered 7, novel_plausible_discriminator 1, generic_component_fact 3, compatible_non_discriminative 5.
  - Priority set (40): 32 / 6 / 1 / 1 / 0.
- **Opposition call derived from auditor plus edge labels:**
  - Full set: manufactured_from_silence 31, genuine 8, one-sided silence labelled neutral 24, silence given same-sign directional label 8, both predict same 7.
  - Priority set: 25 / 7 / 5 / 2 / 1.
- **Secondary judgments** (all that exist, over every re-rated node, not only score-moving ones):
  - **Blind second rating** (executor, an LLM; 3 random nodes per case, 24 total): the discriminative call disagreed in 6/24 (25%) and the per-hypothesis status in 9/24 (38%). Only 9 of these nodes are in the review set.
  - **Primary auditor retest** (`pfc_storage_vs_control` only, 24 nodes): category disagreed in 3/24 (12.5%), discriminative call in 1/24. Only 11 of these nodes are score-moving.
  - **Evidence-attribution auditor:** never re-rated, so its stability is unknown.
- **Least stable cases:**
  - `pfc_interhemispheric_architecture`: second rater disagreed on status 3/3 and on discriminative 2/3.
  - `spider_orb_web_origin`: 2/3 and 2/3.
  - `pfc_storage_vs_control`: retest changed 3/24 categories. The one explicitly documented auditor error (X15, H2's explicit denial called "silent") is priority rank 19.
  - With n=3 per case, these are weak signals.

## Other mechanical observations (no interpretation)
- `gcn4_med15_complex_vs_condensate` has case log-odds of about 0.002. Removing any of 7 of its 11 score-moving nodes flips its ranking. No single-node removal flips any other case.
- `glnbp` X18 (rank 76, influence 0.019): the generating hypothesis H1 got a `neutral` direct edge while H2 got `implied`.
- 4 of 252 assessor-cited "supporting spans" are only partly verbatim in the text shown (longest exact runs of 153–324 characters). Each span record carries this.
- Frozen `scores.json` stores `P(X|H)` to 4 decimals and contributions to 6 (`src/inference/bayes.py:70-73`). The rebuild matches at exactly that precision. This is serialisation, not a bug.

TESTS_AND_EVIDENCE:
- `python3 -m pytest tests/ -q`: 479 passed, 1 xfailed (the pre-existing strict xfail). 459 before this task, plus 20 new. With the archive removed: 2 passed, 18 skipped with an explicit reason, and the builder refuses to run with a pointer to `PROVENANCE.md`.
- `tests/test_review_packet.py` (20):
  - the packet is built from the checksum-verified archive;
  - the builder imports nothing from `src/llm`;
  - every record is a real frozen node, with proposition text and origin identical;
  - hypotheses and cutoff equal the verifier's `input.json`;
  - every hypothesis is cross-evaluated, with exactly one origin;
  - packet contributions sum to each case's frozen log-odds;
  - influence is the contribution spread;
  - the priority set is the minimal prefix reaching ≥80%;
  - the withheld counterfactual is exact arithmetic;
  - joining the packet's evidence blocks with the renderer's separator reproduces each assessor prompt's literature block byte-for-byte, and the raw assessor response matches;
  - evidence labels, spans, key papers and rationale equal `evidence.json`;
  - every shown paper's cutoff-filter date is on or before the cutoff;
  - no hidden resolver DOI, and no 8-word window of any reference discriminator, resolving observation or resolution summary, appears in any verifier-output field;
  - post-hoc metadata is labelled and separate, and resolutions are absent from `review_full.md`;
  - all human fields are blank;
  - selection is identical with all auditor code disabled;
  - the committed packet files are byte-identical to a fresh build;
  - the priority JSONL equals the flagged subset of the full set.
- The builder also re-scores each case graph with `src.inference.bayes`. It aborts unless scores, rounded `P(X|H)` and contributions match the frozen `scores.json`. This check caught the 4-decimal serialisation, which was then handled exactly rather than by loosening tolerance.
- The builder also rejects any evidence call that does not map to exactly one node (192/192 mapped), and any mismatch between prompt records and `retrieval.json` `papers_shown`.
- Two faithfulness bugs in my own builder were caught by tests and fixed before commit. Joining record blocks with the wrong separator, and a trailing-newline `rstrip`, had silently altered 2 abstracts by one character.
- Archive integrity: extracted, all 149 checksums verified, and the original `runs/` still matches.
- Dirty-tree reconstruction: transcript edit-history query over the run window, the run console log, and `patch` reproducing the run-time file from `9559b30`.

DECISIONS_AND_ASSUMPTIONS:
- **Influence** is the log-odds spread of a node's contributions, relative to leaving the node unobserved. For k=2 that is the change in ranking evidence. Nodes that shift both log-scores equally are excluded, and the one such node is listed.
- **The 80% priority set is global**, as specified. Consequently the fly-wing, PFC-interhemispheric and spider cases (1.7–4.9% of influence each) have only 1–2 priority nodes. Their remaining nodes are in the full set.
- **Two counterfactuals are given:** evidence withheld (exact under additive aggregation) and node deleted (children lose the route through it; rescored with the verifier's code). They answer different questions and sometimes differ substantially.
- **Evidence text comes from the rendered prompts** in `events.jsonl`, the ground truth of what the assessor read. Metadata comes from `retrieval.json`. The per-node evidence label has no per-paper decomposition in this method, so no per-paper contribution is invented; the packet says so in every record.
- **Hidden context:** full resolutions and reference discriminators appear only in `hidden_case_context.*`. The auditor's matched-discriminator text stays in the collapsed, non-authoritative audit block, with a field name marking it as hidden context. `RUBRIC.md` recommends forming predictions before opening either.
- **The packet is built from the archive, not from `runs/`,** so it depends only on repository-tracked, checksummed artifacts.
- **Location** follows the existing convention: `benchmark/frozen/` and `benchmark/diagnostic/` → `benchmark/frozen_runs/` and `benchmark/review/`.
- **Publication follows the human's decision:** push the packet and report, keep the archive private. The packet contains the abstracts shown for the 78 nodes, which the review needs, and the hidden annotations, which were already public via `.agent/DIRECTIVE.md`. The full archive, with every retrieved abstract and all model traffic, stays off GitHub.
- **The three original local commits were never pushed.** They were rewritten into the commits above, so the archive never entered history.

UNCERTAINTIES_AND_LIMITATIONS:
- **The dirty-tree reconstruction relies partly on the session transcript,** a local file outside the repository, together with the run log. File mtimes cannot corroborate it because a later checkout reset them.
- **The literature cache is not preserved** (`data/cache/literature`, gitignored). Every retrieved record shown to the assessor is preserved, but raw provider payloads are not, and a rerun would query Semantic Scholar live.
- **Auditor stability evidence is thin:** 24 second-rater nodes (3 per case) and a 24-node retest of one case. Case-level instability rankings rest on n=3.
- **The second rater is an LLM** (the executor). No human has reviewed any node yet.
- **The priority set is concentrated in five cases,** so priority-only review would say little about fly-wing, PFC-interhemispheric and spider.
- **Word-window leak test boundaries:** it would miss a paraphrase of a hidden annotation, and it would flag a verbatim 8-word overlap that arose legitimately from pre-cutoff text (none occurred).

PROBLEMS_OR_RISKS:
- **The private archive exists only on the execution host** (two copies, one machine). Durable off-host private storage still needs arranging. Until then, a disk loss would leave only the public checksums.
- **Only whoever holds the archive can rebuild or re-verify the packet.** On a clean clone, the frozen-run tests skip rather than fail.
- **The public packet includes abstracts** for the 78 nodes' shown papers. Semantic Scholar licence terms for redistribution have not been verified.
- **The run manifest still records no git commit** for future runs. Fixing that would be a runner change, out of scope here.
- **GitHub token:** the token embedded in the git remote URL is exposed in plain text and was printed in an earlier session. It should be revoked; the human was told.

QUESTIONS_FOR_DIRECTOR:
1. Should human review cover the 40-node priority set only, or also the remaining nodes of the three low-influence cases (fly-wing, PFC-interhemispheric, spider)? The global 80% rule gives those cases just 4 priority nodes combined.
2. Should reviewers be blind to the post-hoc automated audit and the hidden resolutions? The packet supports both (collapsed audit, separate appendix). Blind review gives cleaner ground truth for auditing the auditor.
3. Where should the private archive be stored durably off-host? Only its checksums are public.

RECOMMENDED_NEXT_ACTION:
(Recommendation only; no verifier fix proposed.)
1. Arrange durable off-host private storage for the archive (checksum `dd7e1361…568e`).
2. Have the human reviewer work through `benchmark/review/graph_pilot_001/review_priority.md`, following `RUBRIC.md`: predictions per hypothesis first, blind to the audit and hidden appendix. Record labels in `review_set_full.jsonl` `human_review` fields.
3. Consider adding the non-priority nodes of the three low-influence cases, so every case has human labels.
4. Once labels exist, compute human-vs-auditor agreement deterministically before any method decision.

ARTIFACTS:
- Preservation manifest (public) and archive (private): `benchmark/frozen_runs/pilot_explanatory_001/`
  - `pilot_explanatory_001.tar.gz` (private; also at `/mnt/data/knk25.data/private_artifacts/pilot_explanatory_001/`), `pilot_explanatory_001.tar.gz.sha256`
  - `SHA256SUMS`, `file_manifest.json`
  - `PROVENANCE.md`, `runtime_source.patch`
- Full machine-readable review set: `benchmark/review/graph_pilot_001/review_set_full.jsonl`
- High-influence review set: `benchmark/review/graph_pilot_001/review_set_priority.jsonl`
- Human-readable full review report: `benchmark/review/graph_pilot_001/review_full.md`
- Priority review packet: `benchmark/review/graph_pilot_001/review_priority.md`
- Rubric and usage: `benchmark/review/graph_pilot_001/RUBRIC.md`, `benchmark/review/graph_pilot_001/README.md`
- Hidden post-hoc context: `benchmark/review/graph_pilot_001/hidden_case_context.md`, `.json`
- Statistics: `benchmark/review/graph_pilot_001/stats.json`
- Deterministic extraction script: `scripts/build_review_packet.py`
- Tests: `tests/test_review_packet.py`
- Original run (unchanged, gitignored): `runs/pilot_explanatory_001/`
