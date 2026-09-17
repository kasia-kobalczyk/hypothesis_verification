"""Stage B of BENCH-GRAPH-V4-DEV-001: end-to-end runs compared (deterministic, no LLM).

Runs compared:
  * `pilot_explanatory_001`      frozen v3 pilot (read from the checksummed archive)
  * `v3_rerun_explanatory_001`   unchanged v3, fresh run: the run-to-run noise floor
  * `v4_dev_explanatory_001`     v4 development head, fresh run

v4 does not change generation, so generation differences between the v3 re-run and the
v4 run are expected to be of the same order as between the frozen pilot and the v3
re-run. That is the question section 1 answers.

Consequence discovery (section 4) reads `recovery.json` produced by the post-hoc recovery
auditor (`scripts/analyze_pilot_recovery.py`) on each run. It is an LLM judgment with a
known bias toward calling hypotheses silent (see the pilot report), applied identically to
every run.

Usage:
    python scripts/compare_v3_v4_runs.py
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
from collections import Counter, OrderedDict
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import build_review_packet as bp  # noqa: E402

OUT = ROOT / "benchmark" / "v4_dev" / "stage_b"
POS = {"strongly_implied", "implied", "weakly_implied"}
NEG = {"unlikely", "strongly_contradicted"}


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def reviewed_texts() -> Dict[str, Dict[str, str]]:
    """Exact proposition text -> reviewed label, from the frozen-pilot review packet.

    Exact string equality only: a live run regenerates propositions, and any fuzzier
    matching would be a judgment this deterministic script must not make.
    """
    labels = {}
    for name in ("human_labels_D045.json", "human_labels_D046.json"):
        for l in _load(ROOT / "benchmark" / "review" / "graph_pilot_001" / name)["labels"]:
            labels[l["review_id"]] = l["human_primary_category"]
    out = {}
    packet = ROOT / "benchmark" / "review" / "graph_pilot_001" / "review_set_full.jsonl"
    for line in packet.read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        if r["review_id"] in labels:
            out[r["proposition"]["text"]] = {"review_id": r["review_id"], "category": labels[r["review_id"]]}
    return out


def run_summary(run: Path) -> Dict[str, Any]:
    cases = OrderedDict()
    all_texts, levels, depths = [], Counter(), Counter()
    opposed = total = 0
    for inst in sorted(p for p in (run / "instances").iterdir() if p.is_dir()):
        graph = _load(inst / "graph.json")
        edges = _load(inst / "edge_judgments.json")
        scores = _load(inst / "scores.json")
        by_node: Dict[str, set] = {}
        for e in edges["root_edges"]:
            by_node.setdefault(e["target"], set()).add(e["ordinal_strength"])
        n_opp = sum(1 for v in by_node.values() if v & POS and v & NEG)
        opposed += n_opp
        total += len(graph["nodes"])
        for n in graph["nodes"]:
            all_texts.append(n["text"])
            levels[(n.get("metadata") or {}).get("abstraction_level")] += 1
            depths[n.get("depth")] += 1
        entry = OrderedDict([("n_nodes", len(graph["nodes"])), ("n_sign_opposed_v3_edges", n_opp),
                             ("scores", scores["scores"])])
        disc = inst / "discrimination.json"
        if disc.exists():
            layer = _load(disc)
            entry["v3_reference_scores_same_graph"] = scores.get("v3_reference_scores")
            entry["v4_summary"] = layer["summary"]
            reviewed = reviewed_texts()
            entry["v4_scored_nodes"] = [OrderedDict([
                ("node_id", nid), ("text", r["text"]),
                ("states", {h: "{}/{}".format(s["state"], s["strength"]) for h, s in r["states"].items()}),
                ("evidence_label", r["evidence_label"]),
                ("construct_elements", [(e["status"], e["element"]) for e in r["construct"]["elements"]]),
                ("log_odds_H2_over_H1", r["contribution"]["H2"] - r["contribution"]["H1"]),
                ("identical_text_reviewed_in_pilot", reviewed.get(r["text"])),
            ]) for nid, r in layer["nodes"].items() if r["used_in_score"]]
        cases[inst.name] = entry
    tokens = [t for text in all_texts for t in re.findall(r"[a-z]{4,}", text.lower())]
    return OrderedDict([
        ("n_nodes", total),
        ("unique_proposition_texts", len(set(all_texts))),
        ("abstraction_levels", {str(k): v for k, v in levels.items()}),
        ("depths", {str(k): v for k, v in depths.items()}),
        ("mean_proposition_chars", sum(len(t) for t in all_texts) / max(1, len(all_texts))),
        ("content_type_token_ratio", len(set(tokens)) / max(1, len(tokens))),
        ("sign_opposed_v3_edge_nodes", opposed),
        ("cases", cases),
    ])


def discovery(run: Path) -> Dict[str, Any]:
    path = run / "recovery.json"
    if not path.exists():
        return {"available": False}
    rec = _load(path)["summary"]
    ref_total = sum(c["n_reference_discriminators"] for c in rec["per_case"])
    return OrderedDict([
        ("available", True),
        ("categories", rec["categories"]),
        ("reference_discriminators_recovered", sum(c["n_reference_discriminators_recovered"] for c in rec["per_case"])),
        ("reference_discriminators_total", ref_total),
        ("cases_with_any_recovery", sum(1 for c in rec["per_case"] if c["n_reference_discriminators_recovered"])),
        ("per_case_recovered", {c["case_id"]: "{}/{}".format(c["n_reference_discriminators_recovered"],
                                                             c["n_reference_discriminators"]) for c in rec["per_case"]}),
        ("novel_plausible_discriminators", rec["categories"].get("novel_plausible_discriminator", 0)),
    ])


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        frozen = bp.extract_verified(Path(tmp)) / "run"
        runs = OrderedDict([
            ("pilot_explanatory_001 (frozen v3)", frozen),
            ("v3_rerun_explanatory_001", ROOT / "runs" / "v3_rerun_explanatory_001"),
            ("v4_dev_explanatory_001", ROOT / "runs" / "v4_dev_explanatory_001"),
        ])
        result = OrderedDict()
        for name, path in runs.items():
            if not (path / "summary.json").exists():
                result[name] = {"available": False}
                continue
            s = _load(path / "summary.json")
            result[name] = OrderedDict([
                ("run", s.get("run_id")), ("llm_calls", s.get("llm_calls")),
                ("cost_usd", (s.get("cost") or {}).get("cost_usd")), ("n_ok", s.get("n_ok")),
                ("n_error", s.get("n_error")), ("generation_and_structure", run_summary(path)),
                ("consequence_discovery", discovery(path)),
            ])
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "run_comparison.json").write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
    print("wrote", (OUT / "run_comparison.json").relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
