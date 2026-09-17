# BENCH-GRAPH-V4-SCOPE-001 development runs (private archive)

| file | tracked? | contents |
| --- | --- | --- |
| `v4_scope_runs.tar.gz` | **no** (private, gitignored) | 10 run directories + 13 driver logs, 473 files, 27.8 MB |
| `v4_scope_runs.tar.gz.sha256` | yes | `d09257cb65df80a6ea7fd69cc836b6557538e6752817b0cc04e6b6d78b1cddda` |
| `SHA256SUMS` | yes | per-file checksums, paths relative to `runs/` |

Private copies are on the execution host: the working copy here, plus
`/mnt/data/knk25.data/private_artifacts/v4_scope_runs/`. The archive was verified by
extraction (every file against `SHA256SUMS`) on 2026-09-17. It is kept private for the same
reason as the pilot archive: it contains full model traffic and retrieved third-party abstracts.

| run | kind | git commit at start | dirty paths at start relevant to the run |
| --- | --- | --- | --- |
| `v4scope_replay_smoke_glnbp` | stage-A wiring smoke test, one case, before the layer was committed | `890c9fa` | the uncommitted v4-scope layer, committed as `b05c35e` after adding call-id recording (no `has_contrast` gate yet) |
| `v4scope_replay_iter01`, `_rep2`, `_rep3` | stage A, iteration 1 | `a2f34d3` | none (cost ledger, docs, analysis scripts/tests only) |
| `v4scope_replay_iter02`, `_rep2`, `_rep3` | stage A, iteration 2 (final version) | `222d4fa` | none (cost ledger, analysis outputs/scripts only) |
| `v4scope_explanatory_001`, `_002`, `_003` | stage B, final version end-to-end | `753a86c` | none (cost ledger, docs, report scripts only); method code identical to `222d4fa` |

A first launch of `v4scope_replay_iter01` at `b05c35e` was stopped after about a minute,
before any case finished, to add the `has_contrast` gate; its partial directory was deleted
and is not archived.

Recovery-auditor outputs (`recovery.json`, `recovery_events.jsonl`) inside the three
end-to-end runs were added after those runs finished. Driver logs: `v4scope_iter0*.log`
(replays), `v4scope_explanatory_00*.log` (runs), `v4scope_recovery_00*.log` (auditor),
`v4scope_analysis_iter01.log`.
