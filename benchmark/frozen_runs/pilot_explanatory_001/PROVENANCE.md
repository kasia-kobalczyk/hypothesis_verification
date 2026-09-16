# Preserved run: `pilot_explanatory_001` (BENCH-GRAPH-PILOT-001)

Preserved under BENCH-GRAPH-REVIEW-001. Nothing here was regenerated or rerun: the
archive is a byte-level copy of the frozen run plus supplementary files that
existed only in a temporary scratch directory.

**The archive itself is private: it is not in the public repository.** It contains
full model traffic and about 3,800 retrieved third-party abstracts, and the human
decided to keep it off GitHub (BENCH-GRAPH-REVIEW-001). This directory tracks
everything needed to *verify* a copy (the archive's SHA-256, per-file checksums,
the file manifest, this record and the source patch), but not the archive bytes.

| copy | location |
| --- | --- |
| working copy (gitignored) | `benchmark/frozen_runs/pilot_explanatory_001/pilot_explanatory_001.tar.gz` on the execution host |
| second copy | `/mnt/data/knk25.data/private_artifacts/pilot_explanatory_001/pilot_explanatory_001.tar.gz` on the same host |

Both copies are on one machine. Durable off-host private storage is still to be
arranged.

## What is preserved

| file | contents |
| --- | --- |
| `pilot_explanatory_001.tar.gz` | **private, not tracked**: the whole run directory under `run/`, plus `supplementary_scratch/` |
| `pilot_explanatory_001.tar.gz.sha256` | checksum of the archive itself |
| `SHA256SUMS` | per-file SHA-256 of every archived file, paths as inside the archive |
| `file_manifest.json` | per-file size, mtime and **kind** (see below) |
| `runtime_source.patch` | the one source difference between commit `9559b30` and the code that ran |

Verify:

```bash
sha256sum -c benchmark/frozen_runs/pilot_explanatory_001/pilot_explanatory_001.tar.gz.sha256
mkdir /tmp/x && tar -xzf benchmark/frozen_runs/pilot_explanatory_001/pilot_explanatory_001.tar.gz -C /tmp/x
(cd /tmp/x && sha256sum -c "$OLDPWD/benchmark/frozen_runs/pilot_explanatory_001/SHA256SUMS")
```

Archive SHA-256: `dd7e13610afd5eb4bdca78bdf3a4fa91d630142e69f900c4b019a673b754568e`
(149 files; verified by extraction on 2026-09-16).

### Path mapping

| original path | path inside archive |
| --- | --- |
| `runs/pilot_explanatory_001/` (gitignored) | `run/` |
| executor scratch directory, copied to `/mnt/data/knk25.data/pilot_explanatory_001_scratch_holding/` | `supplementary_scratch/` |

The original `runs/pilot_explanatory_001/` was left in place and unmodified; its
files still match `SHA256SUMS`.

### File kinds (`file_manifest.json`)

- **`verifier_run_output`** (112 files): written by the verifier run between
  2026-09-15T15:28:51Z and 16:38:35Z. This is the frozen evidence: `summary.json`,
  `manifest.json`, `config.yaml`, `metrics.json`, `events.jsonl`, cost files, and
  per case `input.json`, `presentation.json`, `graph.json`, `edge_judgments.json`,
  `queries.json`, `retrieval.json`, `evidence.json`, `scores.json`,
  `model_outputs.json`, `events.jsonl`, `result.json`, `yield_by_origin.json`,
  `report.md`.
- **`post_hoc_analysis`** (13 files): written on 2026-09-16 by the post-hoc
  analysis scripts, *after* the run. Includes the LLM auditor outputs
  (`recovery.json`, `evidence_discovery.json`) and the executor's second-rater
  ratings. These are not verifier output and are not authoritative.
- **`supplementary_scratch`** (24 files): the only copies of
  - `pilot_run.log`: the run's console output;
  - `dryrun/recovery.json`: the earlier auditor pass over `pfc_storage_vs_control`
    that the reported test-retest figures depend on;
  - `manual_ratings_*.json`, `manual_review_sample.json`: raw blind second-rater
    ratings;
  - analysis logs.

## Run identity

| field | value |
| --- | --- |
| run id / directory | `pilot_explanatory_001` / `runs/pilot_explanatory_001` |
| label | BENCH-GRAPH-PILOT-001 diagnostic pilot, frozen narrow_graph_v3_complete, no tuning |
| method | `consequence_graph` |
| started / finished | 2026-09-15T15:28:51Z / 2026-09-15T16:38:35Z |
| result | 8/8 ok, 0 errors, 784 LLM calls, 0 parse failures, $2.75 estimated |
| config | `configs/pilot_explanatory.yaml`; the run's `config.yaml` snapshot equals it (apart from `source_path`) |
| ordinal mappings | `configs/ordinal_mappings.yaml`, version `v0-placeholder`; the values recorded in all 8 `scores.json` equal the current file |

### API-backed roles

Every LLM role used the same settings: Azure OpenAI, deployment `gpt-4.1-kasia`
(resolved from environment), api_version `2024-05-01-preview`, temperature 0.0,
top_p 1.0, seed 20260911, JSON mode.

| role (purpose) | prompt | prompt sha256[:16] | calls |
| --- | --- | --- | --- |
| `graph.generate` | `consequence_generate_v3` | `372057495d6e182f` | 64 |
| `graph.root_edge` | `edge_assess_v1` | `86be9454752d082f` | 192 |
| `graph.chain_edge` | `edge_assess_chain_v1` | `090f6db68a221c11` | 144 |
| `graph.proposition_query` | `proposition_query_v1` | `f451df7d6ba29d65` | 192 |
| `graph.evidence_assess` | `evidence_assess_v2` | `94156c126964eb50` | 192 |

Prompt SHAs are recorded in the run manifest and equal the freeze
`benchmark/frozen/narrow_graph_v3_complete.json`.

Non-LLM services:
- **Literature:** Semantic Scholar (356 provider calls, 29 cache hits, 0 errors), top_k 10.
- **Date verification:** Crossref `always`.
- **Temporal policy:** as recorded in the run manifest.

Post-hoc only (not part of the run): the LLM auditors `recovery_classify_v1` and
`evidence_attribution_v1` (`src/llm/prompts_audit/`), same deployment, 192 calls each.

## Source state and the dirty working tree

The run was launched from an **uncommitted working tree** on top of
`c18edc29f93afaa4b9683bfed9473bb3fb659329`. The run manifest records no git commit.

**Reconstruction.** The run-time source is `9559b30` with `runtime_source.patch`
applied. The patch has one hunk, a log-message wording change in
`src/experiments/runner.py`.

```bash
git show 9559b30:src/experiments/runner.py > runner.py
patch runner.py < benchmark/frozen_runs/pilot_explanatory_001/runtime_source.patch
```

Evidence for this claim:

1. The session transcript records every file write. While the run was live
   (15:28:51Z–16:38:35Z), the only write to verifier code under `src/` or
   `configs/` was the runner log-message edit at 15:35:51Z. Two audit prompt files
   were written into `src/llm/prompts/` at 15:31Z and 15:33Z and moved out at
   15:36Z. The verifier renders prompts by name and the run manifest lists only the
   5 prompts above, so they were never used.
2. The run's own console log (`supplementary_scratch/pilot_run.log`) contains the
   pre-edit message `DEVELOPMENT SET (cases): aggregate accuracy from this run is
   for debugging, not evidence for the method`, which the reconstructed file
   produces exactly.
3. No verifier source changed between the end of the run and commit `9559b30`.
   Since then only `src/llm/prompts_audit/` has been added.
4. `configs/ordinal_mappings.yaml`, `src/inference/`, `src/literature/` and
   `src/llm/prompts/` are identical at `c18edc2` (before the pilot) and HEAD.

The change is cosmetic (a log line), so it cannot have affected any result.

## Limitations

- **The literature cache is not preserved.** `data/cache/literature` is gitignored.
  The retrieved records, with titles, abstracts and eligibility dates, are
  preserved in each `retrieval.json`, but raw provider payloads are not. A rerun
  would query Semantic Scholar live and could return different results.
- **Reconstruction relies on the session transcript,** a local file outside the
  repository, plus the run log. File mtimes in the working tree cannot corroborate
  it: a later `git checkout` reset them.
- **The archive is private.** Only its checksums and this record are public. Anyone
  holding a copy can verify it with the commands above; nobody else can rebuild the
  review packet or run the archive-dependent tests (they skip, pointing here).
