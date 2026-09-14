# Held-out split — status changes

The split itself (`split.json`) is frozen and never edited. This file records what
has happened to each part of it.

## 2026-09-13 — the 20 test rows are now DEVELOPMENT data

They were used once, as a genuinely held-out paired comparison (DECISIONS #31, result
in DECISIONS #32). We then **inspected their failures in detail** and are changing
consequence generation in response. That inspection consumed their held-out status:
any future number on these rows is a development number.

* `test_ids` (20 rows) -> **development**. Reported results from the single held-out
  use remain valid and are recorded; nothing further run on them is held out.
* `calibration_ids` (20 rows) -> unused. No calibration was attempted (no
  assessor-local ground truth exists; DECISIONS #31). Available as development data.
* **reserve (12 clean rows) -> UNTOUCHED.** Not in either list, never run, never
  inspected. This is the only genuinely held-out data remaining, and it is spent the
  moment it is looked at.

The reserve must not be run until a generation revision has been validated
structurally on the development rows, and until the gold-vs-negative evidence
asymmetry is understood (DECISIONS #33).
