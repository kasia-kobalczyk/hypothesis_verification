"""Stage B of BENCH-GRAPH-V4-SCOPE-001: fresh end-to-end runs compared (deterministic, no LLM).

Runs compared:
  * `pilot_explanatory_001`         frozen v3 pilot (read from the checksummed archive)
  * `v3_rerun_explanatory_001`      unchanged v3, fresh run (V4-DEV noise floor)
  * `v4_dev_explanatory_001`        prior v4 head, fresh run
  * `v4scope_explanatory_00{1,2,3}` v4-scope final development version, 3 fresh runs

Generation is unchanged in every run after the pilot, so structure and consequence-discovery
differences are run-to-run noise unless they exceed the v3-rerun spread. Consequence
discovery reads each run's `recovery.json` from the post-hoc auditor
(`scripts/analyze_pilot_recovery.py`), applied identically to every run.

Live runs regenerate propositions, so D045/D046 labels apply only to scored propositions
whose text is IDENTICAL to a reviewed pilot proposition; nothing fuzzier is attempted.

Usage:
    python scripts/compare_v4_scope_runs.py
"""
from __future__ import annotations

import json
import sys
import tempfile
from collections import Counter, OrderedDict
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import build_review_packet as bp  # noqa: E402
import compare_v3_v4_runs as cmp  # noqa: E402

OUT = ROOT / "benchmark" / "v4_scope" / "stage_b"
SCOPE_RUNS = ["v4scope_explanatory_001", "v4scope_explanatory_002", "v4scope_explanatory_003"]


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def generation_summary(run: Path) -> Dict[str, Any]:
    """cmp.run_summary without its v4 construct-match view (v4-scope layers have no construct)."""
    with tempfile.TemporaryDirectory() as tmp:
        shadow = Path(tmp) / "run" / "instances"
        for inst in sorted(p for p in (run / "instances").iterdir() if p.is_dir()):
            dest = shadow / inst.name
            dest.mkdir(parents=True)
            for name in ("graph.json", "edge_judgments.json", "scores.json"):
                (dest / name).write_bytes((inst / name).read_bytes())
        out = cmp.run_summary(shadow.parent)
    return out


def scope_layer_summary(run: Path, reviewed: Dict[str, Dict[str, str]]) -> Dict[str, Any]:
    cases = OrderedDict()
    scope_counts, relevance_counts, scored_scope, scored_reviewed = Counter(), Counter(), Counter(), Counter()
    for inst in sorted(p for p in (run / "instances").iterdir() if p.is_dir()):
        layer = _load(inst / "discrimination.json")
        scores = _load(inst / "scores.json")
        scored = []
        for nid, r in layer["nodes"].items():
            scope_counts[(r.get("scope") or {}).get("scope")] += 1
            if r.get("contrast_relevance"):
                relevance_counts[r["contrast_relevance"]["contrast_relevance"]] += 1
            if not r["used_in_score"]:
                continue
            match = reviewed.get(r["text"])
            scored_scope[r["scope"]["scope"]] += 1
            scored_reviewed[(match or {}).get("category", "no_identical_reviewed_text")] += 1
            scored.append(OrderedDict([
                ("node_id", nid), ("text", r["text"]), ("scope", r["scope"]["scope"]),
                ("states", {h: "{}/{}".format(s["state"], s["strength"]) for h, s in r["states"].items()}),
                ("contrast_variable", r["contrast_element"]["contrast_variable"]),
                ("evidence_label", r["evidence_label"]),
                ("log_odds_H2_over_H1", r["contribution"]["H2"] - r["contribution"]["H1"]),
                ("identical_text_reviewed_in_pilot", match),
            ]))
        cases[inst.name] = OrderedDict([
            ("scores", scores["scores"]), ("v3_reference_scores_same_graph", scores.get("v3_reference_scores")),
            ("sensitivity_contrast_partial_allowed_scores", scores.get("sensitivity_contrast_partial_allowed_scores")),
            ("summary", layer["summary"]), ("scored_nodes", scored), ("n_layer_errors", len(layer["errors"])),
        ])
    return OrderedDict([
        ("scope_counts", {str(k): v for k, v in scope_counts.items()}),
        ("relevance_counts", dict(relevance_counts)),
        ("n_scored", sum(scored_scope.values())),
        ("scored_by_scope", dict(scored_scope)),
        ("scored_by_identical_reviewed_text", dict(scored_reviewed)),
        ("cases", cases),
    ])


def main() -> int:
    reviewed = cmp.reviewed_texts()
    result = OrderedDict()
    with tempfile.TemporaryDirectory() as tmp:
        frozen = bp.extract_verified(Path(tmp)) / "run"
        runs = OrderedDict([("pilot_explanatory_001 (frozen v3)", frozen),
                            ("v3_rerun_explanatory_001", ROOT / "runs" / "v3_rerun_explanatory_001"),
                            ("v4_dev_explanatory_001", ROOT / "runs" / "v4_dev_explanatory_001")]
                           + [(name, ROOT / "runs" / name) for name in SCOPE_RUNS])
        for name, path in runs.items():
            if not (path / "summary.json").exists():
                result[name] = {"available": False}
                continue
            s = _load(path / "summary.json")
            is_scope = name in SCOPE_RUNS
            entry = OrderedDict([
                ("run", s.get("run_id")), ("llm_calls", s.get("llm_calls")),
                ("cost_usd", (s.get("cost") or {}).get("cost_usd")), ("n_ok", s.get("n_ok")),
                ("n_error", s.get("n_error")),
                ("generation_and_structure", generation_summary(path) if is_scope else cmp.run_summary(path)),
                ("consequence_discovery", cmp.discovery(path)),
            ])
            if is_scope:
                entry["v4_scope_layer"] = scope_layer_summary(path, reviewed)
            result[name] = entry
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "run_comparison.json").write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
    print("wrote", (OUT / "run_comparison.json").relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
