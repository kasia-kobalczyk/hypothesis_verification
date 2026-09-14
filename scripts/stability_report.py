"""Ranking stability under the FROZEN judgment-noise model.

    python3 scripts/stability_report.py --run <run>

Applies benchmark/frozen/noise_model_v1.json -- estimated from development rows only
-- to any run. Nothing is estimated from the data being analysed.

  evidence  labels resampled from the frozen empirical transition matrix
  edge      direction-preserving adjacent nudges at the frozen per-level rates
  both      simultaneously

Reports P(gold ranks first) per row. This is RANKING STABILITY under model-judgment
variation, not a posterior over scientific truth (docs/UNCERTAINTY_PROTOCOL.md).
"""
from __future__ import annotations

import argparse, collections, json, random, statistics, sys
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


def nudge(label, rng):
    i = SCALE.index(label)
    same = [j for j in (i - 1, i + 1) if 0 <= j < len(SCALE)
            and (SCALE[j] in IMPLY) == (label in IMPLY)
            and (SCALE[j] in CONTRA) == (label in CONTRA)]
    return SCALE[rng.choice(same)] if same else label


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run", required=True)
    ap.add_argument("--noise", default="benchmark/frozen/noise_model_v1.json")
    ap.add_argument("--draws", type=int, default=200)
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)

    cfg = load_config("configs/mvp.yaml")
    maps = load_ordinal_mappings(cfg.ordinal_mappings_path)
    noise = json.loads(Path(args.noise).read_text())
    trans = noise["evidence_transition_matrix"]
    edge_rate = noise["edge_disagreement_by_level"]
    fallback = collections.Counter()

    def resample(label, rng):
        row = trans.get(label)
        if not row:
            fallback[label] += 1
            return label
        r, acc = rng.random(), 0.0
        for alt, p in row.items():
            acc += p
            if r <= acc:
                return alt
        return label

    out = []
    for inst in sorted((Path(args.run) / "instances").glob("*")):
        if not (inst / "graph.json").exists():
            continue
        saved = json.loads((inst / "graph.json").read_text())
        base = {k: (v.get("assessment") or {}).get("evidence_label")
                for k, v in json.loads((inst / "evidence.json").read_text())["by_node"].items()}
        base = {k: v for k, v in base.items() if v}
        gold = json.loads((inst / "scores.json").read_text())["gold_id"]
        lv = {n["id"]: (n.get("metadata") or {}).get("abstraction_level") for n in saved["nodes"]}
        ids = list(saved["hypothesis_ids"])

        def first(labels, relabel=None):
            r = score_hypotheses(build(saved, relabel, lv), labels, mappings=maps,
                                 aggregation=cfg.inference.aggregation)
            return ranking_from_scores(r.scores, order=ids).index(gold) == 0

        row = {"row": inst.name, "point_gold_first": first(base),
               "n_inf": sum(1 for v in base.values() if v != "no_evidence")}
        for chan in ("edge", "evidence", "both"):
            hits = 0
            for s in range(args.draws):
                rng = random.Random(s)
                lab = ({k: resample(v, rng) for k, v in base.items()}
                       if chan in ("evidence", "both") else base)
                rl = ((lambda l, L: (nudge(l, rng)
                                     if rng.random() < edge_rate.get(L or "unknown", 0.5) else l))
                      if chan in ("edge", "both") else None)
                hits += first(lab, rl)
            row[chan] = hits / args.draws
        out.append(row)

    print("%-14s %6s %5s %8s %9s %8s" % ("row", "point", "inf", "P(edge)", "P(evid)", "P(both)"))
    for r in out:
        print("%-14s %6s %5d %8.2f %9.2f %8.2f" % (
            r["row"][-8:], "gold" if r["point_gold_first"] else "neg", r["n_inf"],
            r["edge"], r["evidence"], r["both"]))
    print()
    for c in ("edge", "evidence", "both"):
        v = [r[c] for r in out]
        print("  %-9s mean P(gold first) %.3f | median %.3f | rows 0.2-0.8 %d/%d | rows >0.8 %d | rows <0.2 %d"
              % (c, statistics.mean(v), statistics.median(v),
                 sum(1 for x in v if 0.2 < x < 0.8), len(v),
                 sum(1 for x in v if x >= 0.8), sum(1 for x in v if x <= 0.2)))
    if fallback:
        print("\n  labels absent from the frozen matrix (left unperturbed): %s" % dict(fallback))
    if args.out:
        json.dump(out, open(args.out, "w"), indent=2)
        print("\nwrote %s" % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
