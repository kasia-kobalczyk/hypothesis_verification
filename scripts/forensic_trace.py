"""Why did the posterior move? Node-level trace for stable rows. No model calls.

    python3 scripts/forensic_trace.py --run <run> --stability <stability json>

For every informative node: the contribution difference

    delta_v = contribution(v, H+) - contribution(v, H-)

with the proposition, abstraction level, origin hypothesis, evidence label, quoted
span, and both edge probabilities P(X_v|H+), P(X_v|H-).

Plus discriminative leverage

    L_v = |P(X_v=1|H+) - P(X_v=1|H-)| * |lambda_v|

which separates "a few high-leverage well-grounded nodes" from "many tiny
contributions accumulating into a confident posterior". Confidently CORRECT and
confidently WRONG rows are reported with the same template so the comparison is not
a post-hoc story about the failures.
"""
from __future__ import annotations

import argparse, json, statistics, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def effective_n(deltas):
    """Participation ratio: how many nodes effectively carry the margin."""
    s1 = sum(abs(d) for d in deltas)
    s2 = sum(d * d for d in deltas)
    return (s1 * s1 / s2) if s2 else 0.0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run", required=True)
    ap.add_argument("--stability", required=True)
    ap.add_argument("--hi", type=float, default=0.8)
    ap.add_argument("--lo", type=float, default=0.2)
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)

    stab = {r["row"]: r for r in json.loads(Path(args.stability).read_text())}
    rows = []
    for inst in sorted((Path(args.run) / "instances").glob("*")):
        if inst.name not in stab or not (inst / "scores.json").exists():
            continue
        p = stab[inst.name]["both"]
        if args.lo < p < args.hi:
            continue  # unstable: excluded from this comparison
        sc = json.loads((inst / "scores.json").read_text())
        ev = json.loads((inst / "evidence.json").read_text())["by_node"]
        graph = json.loads((inst / "graph.json").read_text())
        gold = sc["gold_id"]
        neg = [h for h in sc["scores"] if h != gold][0]
        meta = {n["id"]: (n.get("metadata") or {}) for n in graph["nodes"]}
        origin = {n["id"]: n.get("generation_origin_hypothesis") for n in graph["nodes"]}
        contrib = {}
        for c in sc["contributions"]:
            contrib.setdefault(c["node_id"], {})[c["hypothesis_id"]] = c
        nodes = []
        for nid, byh in contrib.items():
            if gold not in byh or neg not in byh:
                continue
            g, n = byh[gold], byh[neg]
            lam = g["log_likelihood_ratio"]
            if abs(lam) < 1e-9:
                continue  # no_evidence contributes exactly 0
            nodes.append({
                "node": nid,
                "delta": g["contribution"] - n["contribution"],
                "p_gold": g["p_true_given_h"], "p_neg": n["p_true_given_h"],
                "lambda": lam, "label": g["evidence_label"],
                "leverage": abs(g["p_true_given_h"] - n["p_true_given_h"]) * abs(lam),
                "level": meta.get(nid, {}).get("abstraction_level"),
                "origin_gold": origin.get(nid) == gold,
                "text": (ev.get(nid, {}) or {}).get("text", ""),
                "spans": ((ev.get(nid, {}) or {}).get("assessment", {}) or {}).get("supporting_spans"),
            })
        nodes.sort(key=lambda x: -abs(x["delta"]))
        rows.append({"row": inst.name, "p_both": p,
                     "verdict": "CORRECT" if p >= args.hi else "WRONG",
                     "margin": sum(x["delta"] for x in nodes),
                     "nodes": nodes})

    for verdict in ("CORRECT", "WRONG"):
        sub = [r for r in rows if r["verdict"] == verdict]
        if not sub:
            continue
        allnodes = [n for r in sub for n in r["nodes"]]
        tops = [max((abs(n["leverage"]) for n in r["nodes"]), default=0) for r in sub]
        effs = [effective_n([n["delta"] for n in r["nodes"]]) for r in sub]
        disc = [abs(n["p_gold"] - n["p_neg"]) for n in allnodes]
        gold_c = sum(n["delta"] for n in allnodes if n["origin_gold"])
        neg_c = sum(n["delta"] for n in allnodes if not n["origin_gold"])
        print("=== stable %s: %d row(s), %d informative node(s) ===" % (
            verdict, len(sub), len(allnodes)))
        print("  top-node leverage (mean)        %.4f" % statistics.mean(tops))
        print("  effective # contributing nodes  %.2f" % statistics.mean(effs))
        print("  mean edge discrimination        %.4f" % (statistics.mean(disc) if disc else 0))
        print("  mean |lambda| (evidence strength) %.4f" % statistics.mean(abs(n["lambda"]) for n in allnodes))
        print("  total delta from gold-origin nodes %+.4f" % gold_c)
        print("  total delta from neg-origin nodes  %+.4f" % neg_c)
        print()
    if args.out:
        json.dump(rows, open(args.out, "w"), indent=2)
        print("wrote %s" % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
