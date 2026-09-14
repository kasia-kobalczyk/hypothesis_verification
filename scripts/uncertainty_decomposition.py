"""Decompose ranking uncertainty into edge-judgment vs evidence-judgment sources.

    python3 scripts/uncertainty_decomposition.py --run <run> --repeats <repeat json>

Holds the graph fixed and perturbs one channel at a time:

  edge      ordinal edge labels nudged at the per-abstraction-level rate the two
            edge judges actually disagreed at
  evidence  node labels resampled from the repeats actually observed under
            nuisance variation -- an empirical distribution, not an assumed one
  both      simultaneously

Reports P(gold ranks first) per row under each. That is the stability-aware output:
a row at 52/48 is not the same result as one at 99/1, and a point ranking cannot
tell them apart.
"""
from __future__ import annotations

import argparse, json, random, statistics, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.common.config import load_config  # noqa: E402
from src.experiments.metrics import ranking_from_scores  # noqa: E402
from src.graph.schema import ConsequenceGraph, GraphEdge, PropositionNode  # noqa: E402
from src.inference.bayes import score_hypotheses  # noqa: E402
from src.inference.parameters import load_ordinal_mappings  # noqa: E402

SCALE = ["strongly_implied", "implied", "weakly_implied", "neutral",
         "unlikely", "strongly_contradicted"]
IMPLY, CONTRA = set(SCALE[:3]), set(SCALE[4:])
DIS = {"specific": .406, "mechanistic": .516, "class": .630, None: .5}
NF, EF = set(PropositionNode.model_fields), set(GraphEdge.model_fields)


def build(saved, relabel=None, lv=None):
    g = ConsequenceGraph(instance_id=saved["instance_id"],
                         hypothesis_ids=list(saved["hypothesis_ids"]))
    for n in saved["nodes"]:
        g.add_node(PropositionNode(**{k: v for k, v in n.items() if k in NF}))
    for e in saved["edges"]:
        d = {k: v for k, v in e.items() if k in EF}
        if relabel and d.get("ordinal_strength") in SCALE:
            d["ordinal_strength"] = relabel(d["ordinal_strength"], (lv or {}).get(e.get("target")))
        g.add_edge(GraphEdge(**d))
    return g.freeze()


def nudge(label, level, rng):
    i = SCALE.index(label)
    same = [j for j in (i - 1, i + 1) if 0 <= j < len(SCALE)
            and (SCALE[j] in IMPLY) == (label in IMPLY)
            and (SCALE[j] in CONTRA) == (label in CONTRA)]
    return SCALE[rng.choice(same)] if same else label


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run", required=True)
    ap.add_argument("--repeats", required=True)
    ap.add_argument("--draws", type=int, default=60)
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)

    cfg = load_config("configs/mvp.yaml")
    maps = load_ordinal_mappings(cfg.ordinal_mappings_path)
    rep = {r["instance"]: r["labels"] for r in json.loads(Path(args.repeats).read_text())["rows"]}

    out = []
    for inst in sorted((Path(args.run) / "instances").glob("*")):
        if inst.name not in rep or not (inst / "graph.json").exists():
            continue
        saved = json.loads((inst / "graph.json").read_text())
        base = {k: (v.get("assessment") or {}).get("evidence_label")
                for k, v in json.loads((inst / "evidence.json").read_text())["by_node"].items()}
        base = {k: v for k, v in base.items() if v}
        gold = json.loads((inst / "scores.json").read_text())["gold_id"]
        lv = {n["id"]: (n.get("metadata") or {}).get("abstraction_level") for n in saved["nodes"]}
        ids = list(saved["hypothesis_ids"])
        obs = rep[inst.name]

        def first(labels, relabel=None):
            g = build(saved, relabel=relabel, lv=lv)
            r = score_hypotheses(g, labels, mappings=maps, aggregation=cfg.inference.aggregation)
            return ranking_from_scores(r.scores, order=ids).index(gold) == 0

        res = {"row": inst.name, "point": first(base),
               "n_inf": sum(1 for v in base.values() if v != "no_evidence")}
        for chan in ("edge", "evidence", "both"):
            hits = 0
            for s in range(args.draws):
                rng = random.Random(s)
                lab = base
                if chan in ("evidence", "both"):
                    lab = {k: (rng.choice([x for x in obs[k] if x]) if obs.get(k) else v)
                           for k, v in base.items()}
                rl = None
                if chan in ("edge", "both"):
                    rl = lambda l, L: (nudge(l, L, rng) if rng.random() < DIS.get(L, .5) else l)
                hits += first(lab, rl)
            res[chan] = hits / args.draws
        out.append(res)

    print("%-14s %6s %5s %8s %9s %7s" % ("row", "point", "inf", "P(edge)", "P(evid)", "P(both)"))
    for r in out:
        print("%-14s %6s %5d %8.2f %9.2f %7.2f" % (
            r["row"][-8:], "gold" if r["point"] else "neg", r["n_inf"],
            r["edge"], r["evidence"], r["both"]))
    print()
    for c in ("edge", "evidence", "both"):
        vals = [r[c] for r in out]
        unstable = sum(1 for v in vals if 0.2 < v < 0.8)
        print("  %-9s mean P(gold first) %.3f | rows in 0.2-0.8 (unstable): %d/%d"
              % (c, statistics.mean(vals), unstable, len(vals)))
    if args.out:
        json.dump(out, open(args.out, "w"), indent=2)
        print("\nwrote %s" % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
