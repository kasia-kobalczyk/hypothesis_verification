# BENCH-GRAPH-V4-DEV-001 development runs (private archive)

| file | tracked? | contents |
| --- | --- | --- |
| `v4_dev_runs.tar.gz` | **no** (private, gitignored) | 9 run directories, 315 files, 17.1 MB |
| `v4_dev_runs.tar.gz.sha256` | yes | `5f7f0ffec6b73de0605967a1646882a9bf7fcbd8bb011d7ec4d1aa10cfec529d` |
| `SHA256SUMS` | yes | per-file checksums, paths relative to `runs/` |

Private copies are on the execution host: the working copy here, plus
`/mnt/data/knk25.data/private_artifacts/v4_dev_runs/`. The archive was verified by
extraction on 2026-09-17. It is kept private for the same reason as the pilot archive:
it contains full model traffic and retrieved third-party abstracts.

| run | kind | git commit at start | dirty paths at start (none used by the run) |
| --- | --- | --- | --- |
| `v3_rerun_explanatory_001` | unchanged v3, end-to-end (noise floor) | `f95195a` | none |
| `v4_dev_explanatory_001` | v4 development head, end-to-end | `a770f94` | cost ledger; untracked `scripts/compare_v3_v4_runs.py` |
| `v4_replay_smoke_pfc` | stage-A wiring smoke test, one case | `83b707f` | cost ledger |
| `v4_replay_pilot_iter01`, `_rep2` | stage A, iteration 1 | `83b707f` | cost ledger; analysis outputs/scripts |
| `v4_replay_pilot_iter02`, `_rep2` | stage A, iteration 2 | `7f4718b` | cost ledger; analysis outputs/scripts, docs |
| `v4_replay_pilot_iter03`, `_rep2` | stage A, iteration 3 | `6817782` | cost ledger |

Recovery-auditor outputs (`recovery.json`, `recovery_events.jsonl`) inside the two
end-to-end runs were added after those runs finished.
