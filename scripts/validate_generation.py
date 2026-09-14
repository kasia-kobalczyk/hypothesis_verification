"""Structural validation of a generation revision. No ranking, by design.

    python3 scripts/validate_generation.py --run runs/... --baseline runs/...

Answers only: did the revision do what it was meant to do, and did it introduce
dubious nodes? Ranking is deliberately excluded -- a generation prompt tuned against
ranking on a development slice is how a benchmark artifact gets learned.

Reports abstraction-level spread, the why_implied constraint, evidence yield by
level, zero-yield rows against the baseline, discriminativeness by level (an
abstracted node that every candidate predicts equally is inert even when evidenced),
and the gold-vs-negative yield asymmetry.
"""

from __future__ import annotations

import argparse
import collections
import json
import statistics
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.common.io import utc_now_iso, write_json  # noqa: E402

LEVELS = ("specific", "mechanistic", "class")


def rows_of(run: Path) -> Dict[str, Dict[str, Any]]:
    out = {}
    for d in sorted((run / "instances").glob("*")):
        if not (d / "graph.json").exists():
            continue
        graph = json.loads((d / "graph.json").read_text())
        ev = json.loads((d / "evidence.json").read_text())["by_node"]
        scores = json.loads((d / "scores.json").read_text())
        disc = scores.get("discriminativeness", {})
        nodes = []
        for n in graph["nodes"]:
            meta = n.get("metadata") or {}
            label = (ev.get(n["id"], {}).get("assessment", {}) or {}).get("evidence_label")
            nodes.append({
                "id": n["id"],
                "level": meta.get("abstraction_level"),
                "why_implied": (meta.get("why_implied") or "").strip(),
                "informative": bool(label and label != "no_evidence"),
                "label": label,
                "disc": disc.get(n["id"], 0.0),
                "origin_is_gold": n.get("generation_origin_hypothesis") == scores["gold_id"],
            })
        vals = sorted(scores["scores"].values(), reverse=True)
        out[d.name] = {"nodes": nodes, "spread": vals[0] - vals[-1]}
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", required=True)
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--out", default=None)
    args = parser.parse_args(argv)

    new = rows_of(Path(args.run))
    base = rows_of(Path(args.baseline))
    shared = sorted(set(new) & set(base))
    nodes = [n for r in shared for n in new[r]["nodes"]]
    rep = {"generated_at": utc_now_iso(), "run": args.run,
           "baseline": args.baseline, "n_rows": len(shared)}
    print("rows compared: %d" % len(shared))

    levels = collections.Counter(n["level"] for n in nodes)
    per_row = [collections.Counter(n["level"] for n in new[r]["nodes"]) for r in shared]
    even = sum(1 for c in per_row if len(set(c.get(l, 0) for l in LEVELS)) == 1)
    print("")
    print("1. levels: %s" % dict(levels))
    print("   rows with a perfectly even split: %d/%d (quota-following check)"
          % (even, len(shared)))
    rep["levels"] = dict(levels)
    rep["rows_perfectly_even"] = even

    abstracted = [n for n in nodes if n["level"] in ("mechanistic", "class")]
    unlinked = [n for n in abstracted if not n["why_implied"]]
    print("")
    print("2. abstracted nodes: %d | missing why_implied: %d" % (len(abstracted), len(unlinked)))
    rep["abstracted"] = len(abstracted)
    rep["abstracted_without_why_implied"] = len(unlinked)

    print("")
    print("3. yield and discriminativeness by level")
    rep["by_level"] = {}
    for lv in LEVELS:
        sub = [n for n in nodes if n["level"] == lv]
        if not sub:
            continue
        inf = sum(n["informative"] for n in sub)
        dmed = statistics.median(n["disc"] for n in sub)
        inert = sum(1 for n in sub if n["informative"] and n["disc"] == 0)
        print("   %-11s nodes %4d  informative %3d (%4.0f%%)  median disc %.3f  "
              "evidenced-but-inert %d" % (lv, len(sub), inf, 100.0 * inf / len(sub), dmed, inert))
        rep["by_level"][lv] = {"nodes": len(sub), "informative": inf,
                               "median_disc": dmed, "evidenced_but_inert": inert}

    zb = [r for r in shared if not any(n["informative"] for n in base[r]["nodes"])]
    zn = [r for r in shared if not any(n["informative"] for n in new[r]["nodes"])]
    rescued = sorted(set(zb) - set(zn))
    lost = sorted(set(zn) - set(zb))
    print("")
    print("4. zero-yield rows: baseline %d -> revision %d" % (len(zb), len(zn)))
    print("   rescued: %s" % (" ".join(r[-8:] for r in rescued) or "none"))
    print("   newly zero: %s" % (" ".join(r[-8:] for r in lost) or "none"))
    cb = sum(1 for r in shared if base[r]["spread"] > 0) / max(len(shared), 1)
    cn = sum(1 for r in shared if new[r]["spread"] > 0) / max(len(shared), 1)
    print("   coverage (posterior moved): baseline %.2f -> revision %.2f" % (cb, cn))
    rep["zero_yield"] = {"baseline": len(zb), "revision": len(zn),
                         "rescued": rescued, "newly_zero": lost,
                         "coverage_baseline": cb, "coverage_revision": cn}

    print("")
    print("5. yield by node origin (the broad-assessor bias check)")
    for label, rows in (("baseline", base), ("revision", new)):
        ns = [n for r in shared for n in rows[r]["nodes"]]
        for scope, want in (("gold", True), ("negative", False)):
            s = [n for n in ns if n["origin_is_gold"] == want]
            if not s:
                continue
            inf = sum(n["informative"] for n in s)
            con = sum(1 for n in s if n["label"] and "contradiction" in str(n["label"]))
            print("   %-9s %-9s nodes %4d  informative %4.0f%%  contradiction %4.1f%%"
                  % (label, scope, len(s), 100.0 * inf / len(s), 100.0 * con / len(s)))

    if args.out:
        write_json(args.out, rep)
        print("")
        print("wrote %s" % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
