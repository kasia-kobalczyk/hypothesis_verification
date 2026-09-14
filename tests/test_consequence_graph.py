"""Milestone 2: graph schema, merging, and Bayesian propagation.

The properties tested here are the ones the paper's argument rests on. Each maps
to a clause of IMPLEMENTATION_SPEC.md §35.
"""

from __future__ import annotations

import math

import pytest

from pathlib import Path

from src.graph.merge import merge_propositions, text_similarity
from src.graph.schema import ConsequenceGraph, GraphEdge, PropositionNode, is_hypothesis
from src.inference.bayes import discriminativeness, propagate, score_hypotheses
from src.inference.parameters import load_ordinal_mappings

SRC_ROOT = Path(__file__).resolve().parents[1] / "src"


@pytest.fixture
def mappings():
    return load_ordinal_mappings("configs/ordinal_mappings.yaml")


def chain_graph(*, strengths, hypotheses=("H0", "H1")):
    """H0 -> X1 -> X2, with X1 also cross-evaluated against every hypothesis."""
    graph = ConsequenceGraph(instance_id="T", hypothesis_ids=list(hypotheses))
    graph.add_node(PropositionNode(id="X1", text="near", depth=1,
                                   generation_origin_hypothesis="H0"))
    graph.add_node(PropositionNode(id="X2", text="far", depth=2, generation_parent="X1",
                                   generation_origin_hypothesis="H0"))
    for hypothesis, strength in strengths.items():
        graph.add_edge(GraphEdge(source=hypothesis, target="X1", kind="root",
                                 ordinal_strength=strength))
        graph.add_edge(GraphEdge(source=hypothesis, target="X2", kind="root",
                                 ordinal_strength="neutral"))
    graph.add_edge(GraphEdge(source="X1", target="X2", kind="chain",
                             ordinal_strength="strongly_implied"))
    return graph.freeze()


# --------------------------------------------------------------------------- #
# §35.5  Missing evidence is not contradictory evidence
# --------------------------------------------------------------------------- #
def test_no_evidence_moves_nothing_at_all(mappings):
    graph = chain_graph(strengths={"H0": "strongly_implied", "H1": "strongly_contradicted"})
    flat = score_hypotheses(graph, {}, mappings=mappings).scores
    with_none = score_hypotheses(graph, {"X1": "no_evidence"}, mappings=mappings).scores
    assert with_none == pytest.approx(flat)
    assert with_none["H0"] == pytest.approx(0.5), "a uniform prior must survive untouched"


def test_a_no_evidence_node_contributes_exactly_zero(mappings):
    graph = chain_graph(strengths={"H0": "implied", "H1": "unlikely"})
    result = score_hypotheses(graph, {"X1": "no_evidence"}, mappings=mappings)
    assert all(c.contribution == pytest.approx(0.0) for c in result.contributions)


# --------------------------------------------------------------------------- #
# §2  Non-discriminative evidence cannot change the ranking
# --------------------------------------------------------------------------- #
def test_a_node_every_hypothesis_predicts_equally_is_inert(mappings):
    """However strong the evidence, it must not move the ranking."""
    graph = chain_graph(strengths={"H0": "implied", "H1": "implied"})
    assert discriminativeness(propagate(graph, mappings=mappings))["X1"] == 0.0
    for label in ("strong_support", "contradiction", "mixed"):
        scores = score_hypotheses(graph, {"X1": label}, mappings=mappings).scores
        assert scores["H0"] == pytest.approx(scores["H1"]), label


def test_discriminative_evidence_moves_the_ranking_the_right_way(mappings):
    graph = chain_graph(strengths={"H0": "strongly_implied", "H1": "strongly_contradicted"})
    support = score_hypotheses(graph, {"X1": "strong_support"}, mappings=mappings).scores
    contra = score_hypotheses(graph, {"X1": "strong_contradiction"}, mappings=mappings).scores
    assert support["H0"] > 0.5 > support["H1"]
    assert contra["H1"] > 0.5 > contra["H0"], "contradicting a prediction favours the rival"


# --------------------------------------------------------------------------- #
# §35.2  Graph distance is not evidence strength
# --------------------------------------------------------------------------- #
def test_depth_itself_is_never_used_as_a_discount(mappings):
    """§35.2: no term in the model reads a node's depth.

    Relabelling a node as "deeper", without touching a single edge, must change
    nothing. Attenuation is allowed to come from the edge probabilities and from
    nowhere else.
    """
    graph = chain_graph(strengths={"H0": "strongly_implied", "H1": "neutral"})
    before = score_hypotheses(graph, {"X2": "strong_support"}, mappings=mappings)

    deep = chain_graph(strengths={"H0": "strongly_implied", "H1": "neutral"})
    deep.nodes["X2"].depth = 7
    after = score_hypotheses(deep, {"X2": "strong_support"}, mappings=mappings)

    assert after.scores == pytest.approx(before.scores)
    assert after.p_matrix["X2"] == pytest.approx(before.p_matrix["X2"])


def test_a_chain_attenuates_discrimination_not_the_evidence(mappings):
    """Distance costs *discriminativeness* through imperfect links.

    A strong chain still lifts every hypothesis whose parent sits at baseline,
    so the gap between hypotheses narrows with each uncertain step. That is the
    intended behaviour, and it is worth pinning down because it is what makes a
    remote consequence weaker than a near one — the edges, not the depth.
    """
    graph = chain_graph(strengths={"H0": "strongly_implied", "H1": "neutral"})
    p = propagate(graph, mappings=mappings)
    near_gap = abs(p["X1"]["H0"] - p["X1"]["H1"])
    far_gap = abs(p["X2"]["H0"] - p["X2"]["H1"])
    assert near_gap > far_gap > 0.0
    assert discriminativeness(p)["X1"] > discriminativeness(p)["X2"]


def test_a_weak_chain_attenuates(mappings):
    strong = chain_graph(strengths={"H0": "strongly_implied", "H1": "neutral"})
    weak = ConsequenceGraph(instance_id="T", hypothesis_ids=["H0", "H1"])
    weak.add_node(PropositionNode(id="X1", text="near", depth=1))
    weak.add_node(PropositionNode(id="X2", text="far", depth=2, generation_parent="X1"))
    for hypothesis, strength in (("H0", "strongly_implied"), ("H1", "neutral")):
        weak.add_edge(GraphEdge(source=hypothesis, target="X1", kind="root",
                                ordinal_strength=strength))
        weak.add_edge(GraphEdge(source=hypothesis, target="X2", kind="root",
                                ordinal_strength="neutral"))
    weak.add_edge(GraphEdge(source="X1", target="X2", kind="chain", ordinal_strength="weakly_implied"))
    weak.freeze()

    p_strong = propagate(strong, mappings=mappings)["X2"]["H0"]
    p_weak = propagate(weak, mappings=mappings)["X2"]["H0"]
    assert p_strong > p_weak


# --------------------------------------------------------------------------- #
# Structure and freezing (§13, §35.6)
# --------------------------------------------------------------------------- #
def test_a_frozen_graph_cannot_be_extended(mappings):
    graph = chain_graph(strengths={"H0": "implied", "H1": "neutral"})
    with pytest.raises(RuntimeError):
        graph.add_node(PropositionNode(id="X9", text="late addition"))
    with pytest.raises(RuntimeError):
        graph.add_edge(GraphEdge(source="H0", target="X1"))


def test_unjudged_edges_carry_no_information(mappings):
    graph = ConsequenceGraph(instance_id="T", hypothesis_ids=["H0", "H1"])
    graph.add_node(PropositionNode(id="X1", text="p"))
    graph.add_edge(GraphEdge(source="H0", target="X1", kind="root"))  # no strength
    graph.freeze()
    assert propagate(graph, mappings=mappings)["X1"]["H0"] == 0.5


def test_hypothesis_roots_may_be_edge_sources_and_never_targets():
    graph = ConsequenceGraph(instance_id="T", hypothesis_ids=["H0"])
    graph.add_node(PropositionNode(id="X1", text="p"))
    assert is_hypothesis("H0") and not is_hypothesis("X1")
    graph.add_edge(GraphEdge(source="H0", target="X1", kind="root", ordinal_strength="implied"))
    assert graph.validate() == []


def test_shared_nodes_are_detected(mappings):
    graph = ConsequenceGraph(instance_id="T", hypothesis_ids=["H0", "H1"])
    node = PropositionNode(id="X1", text="p", generation_origin_hypothesis="H0")
    node.merged_origin_hypotheses = ["H1"]
    graph.add_node(node)
    graph.add_edge(GraphEdge(source="H0", target="X1", kind="root", ordinal_strength="implied"))
    assert graph.origin_hypotheses("X1") == ["H0", "H1"]
    assert [n.id for n in graph.shared_nodes()] == ["X1"]


# --------------------------------------------------------------------------- #
# Multi-parent composition (§22) and merging (§13.4)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("rule", ["noisy_or", "max", "mean"])
def test_every_multi_parent_rule_is_implemented(mappings, rule):
    graph = ConsequenceGraph(instance_id="T", hypothesis_ids=["H0"])
    graph.add_node(PropositionNode(id="X1", text="a", depth=1))
    graph.add_node(PropositionNode(id="X2", text="b", depth=1))
    graph.add_node(PropositionNode(id="X3", text="joint", depth=2, generation_parent="X1"))
    for node_id in ("X1", "X2"):
        graph.add_edge(GraphEdge(source="H0", target=node_id, kind="root",
                                 ordinal_strength="strongly_implied"))
        graph.add_edge(GraphEdge(source=node_id, target="X3", kind="chain",
                                 ordinal_strength="implied"))
    graph.freeze()
    value = propagate(graph, mappings=mappings, multi_parent_rule=rule)["X3"]["H0"]
    assert 0.0 <= value <= 1.0


def test_merging_records_every_decision(config):
    nodes = [
        PropositionNode(id="X1", text="Serum lactate rises after exercise",
                        generation_origin_hypothesis="H0"),
        PropositionNode(id="X2", text="Serum lactate rises after exercise.",
                        generation_origin_hypothesis="H1"),
    ]
    outcome = merge_propositions(nodes, mode="lexical", threshold=0.82)
    assert [n.id for n in outcome.nodes] == ["X1"]
    assert outcome.remap["X2"] == "X1"
    assert outcome.merges[0]["similarity"] >= 0.82
    # The surviving node records that a second hypothesis also predicts it.
    assert outcome.nodes[0].merged_origin_hypotheses == ["H1"]


def test_merging_is_conservative_by_default(config):
    """Two different predictions must not collapse into one."""
    nodes = [
        PropositionNode(id="X1", text="Serum lactate rises after exercise"),
        PropositionNode(id="X2", text="Serum glucose falls during fasting"),
    ]
    outcome = merge_propositions(nodes, mode="lexical", threshold=config.graph.merge_threshold)
    assert len(outcome.nodes) == 2
    assert text_similarity(nodes[0].text, nodes[1].text) < config.graph.merge_threshold


# --------------------------------------------------------------------------- #
# Wiring
# --------------------------------------------------------------------------- #
def test_the_method_is_registered_and_needs_literature():
    from src.experiments.runner import METHODS
    from src.methods.consequence_graph import ConsequenceGraphVerifier

    assert METHODS["consequence_graph"] is ConsequenceGraphVerifier
    assert ConsequenceGraphVerifier.requires_literature is True


def test_the_method_declares_every_prompt_it_uses(config):
    from src.llm.prompts import PromptLibrary
    from src.methods.consequence_graph import ConsequenceGraphVerifier

    library = PromptLibrary(config.prompts.dir)
    for name in ConsequenceGraphVerifier(config).prompt_versions():
        assert library.get(name).sha


def test_the_evidence_assessor_never_sees_a_hypothesis(config):
    """§19: the proposition is judged on its own terms."""
    from src.llm.prompts import PromptLibrary

    text = PromptLibrary(config.prompts.dir).get("evidence_assess_v1").text.lower()
    assert "no hypothesis is at stake" in text
    assert "$hypothesis" not in text


def test_the_edge_assessor_never_sees_retrieved_literature(config):
    """§15: implication strength is judged before evidence, not in its light."""
    from src.llm.prompts import PromptLibrary

    library = PromptLibrary(config.prompts.dir)
    for name in ("edge_assess_v1", "edge_assess_chain_v1"):
        text = " ".join(library.get(name).text.lower().split())
        assert "$literature" not in text
        assert "you have no literature access" in text, name


def test_graph_diagnostics_use_the_names_the_aggregator_sums():
    """A counter the aggregator does not know about shows up as `None` in metrics.

    This actually happened: the method emitted `n_informative`, metrics summed
    `n_informative_assessments`, and the aggregate diagnostics were silently empty
    while the per-instance artifacts had the numbers all along.
    """
    import re

    source = (SRC_ROOT / "methods" / "consequence_graph.py").read_text()
    emitted = set(re.findall(r'counters\[\s*"([a-z0-9_]+)"\s*\]', source))
    assert emitted, "no counters found; the pattern above is out of date"

    metrics_source = (SRC_ROOT / "experiments" / "metrics.py").read_text()
    block = metrics_source.split("for key in (", 1)[1].split("):", 1)[0]
    aggregated = set(re.findall(r'"([a-z0-9_]+)"', block))

    missing = sorted(name for name in emitted if name not in aggregated)
    assert not missing, (
        "consequence_graph emits counters the aggregator ignores: %s" % missing
    )


# --------------------------------------------------------------------------- #
# Generation: atomicity instead of per-proposition discrimination (DECISIONS #17)
# --------------------------------------------------------------------------- #
PROMPT_DIR = SRC_ROOT / "llm" / "prompts"


def _prompt(name):
    from src.llm.prompts import PromptLibrary

    return PromptLibrary(PROMPT_DIR).get(name)


def test_v2_generation_cannot_be_shown_the_competing_candidates():
    """Non-contrastive generation is structural, not a matter of wording.

    `_generate_children` passes only the placeholders a template declares, so a
    template without `$alternatives` never receives the rival hypotheses however
    its prose is later edited.
    """
    assert "alternatives" not in _prompt("consequence_generate_v2").placeholders
    assert "alternatives" in _prompt("consequence_generate_v1").placeholders, (
        "v1 is kept for provenance and is expected to still be contrastive"
    )


def test_v2_generation_does_not_ask_for_discriminative_propositions():
    text = " ".join(_prompt("consequence_generate_v2").text.lower().split())
    assert "discriminative" not in text
    assert "why_discriminative" not in text
    # It must say so positively, not merely omit the instruction.
    assert "do not try to make a proposition distinguish" in text


def test_v2_generation_asks_for_atomic_propositions():
    text = " ".join(_prompt("consequence_generate_v2").text.lower().split())
    assert "atomic" in text
    assert "one relation, one mechanism, or one measurement" in text


# --------------------------------------------------------------------------- #
# Budget: per-candidate, and never silently deformed
# --------------------------------------------------------------------------- #
def _presentation(k):
    from src.benchmark.presentation import PresentedHypothesis, Presentation

    items = [
        PresentedHypothesis(label=chr(ord("A") + i), hypothesis_id="H%d" % i,
                            text="candidate %d" % i, gold=(i == 0))
        for i in range(k)
    ]
    return Presentation(instance_id="T", items=items, seed_key="k", order="fixed")


class ExplodingLLM:
    """Any call at all is a failure: the budget check must precede spending."""

    def complete_json(self, *args, **kwargs):  # pragma: no cover - must not run
        raise AssertionError("build_graph spent a model call before checking the budget")


def test_a_budget_too_small_for_depth_one_is_refused_before_any_call(config):
    from src.common.errors import GraphBudgetError
    from src.graph.generate import build_graph
    from src.llm.prompts import PromptLibrary

    config.graph.max_root_consequences_per_hypothesis = 3
    config.graph.max_nodes = 20  # 11 candidates x 3 = 33 > 20

    with pytest.raises(GraphBudgetError) as excinfo:
        build_graph(instance_id="T", question="q", presentation=_presentation(11),
                    config=config, llm=ExplodingLLM(), prompts=PromptLibrary(PROMPT_DIR))
    message = str(excinfo.value)
    assert "33" in message and "max_nodes" in message


def test_a_sufficient_budget_passes_the_check(config):
    """The same k with a cap that fits must get past the check and start calling."""
    from src.graph.generate import build_graph
    from src.llm.prompts import PromptLibrary

    config.graph.max_root_consequences_per_hypothesis = 3
    config.graph.max_nodes = 33

    with pytest.raises(AssertionError, match="spent a model call"):
        build_graph(instance_id="T", question="q", presentation=_presentation(11),
                    config=config, llm=ExplodingLLM(), prompts=PromptLibrary(PROMPT_DIR))


def test_deeper_expansion_is_interleaved_across_candidates():
    """Truncation at the node cap must not give every depth-2 slot to one candidate."""
    from src.graph.generate import _round_robin_by_origin

    nodes = [
        PropositionNode(id="X1", text="a", depth=1, generation_origin_hypothesis="H0"),
        PropositionNode(id="X2", text="b", depth=1, generation_origin_hypothesis="H0"),
        PropositionNode(id="X3", text="c", depth=1, generation_origin_hypothesis="H0"),
        PropositionNode(id="X4", text="d", depth=1, generation_origin_hypothesis="H1"),
        PropositionNode(id="X5", text="e", depth=1, generation_origin_hypothesis="H1"),
    ]
    order = [n.id for n in _round_robin_by_origin(nodes)]
    assert order == ["X1", "X4", "X2", "X5", "X3"]
    # Deterministic, and order within an origin is preserved.
    assert order == [n.id for n in _round_robin_by_origin(nodes)]
    assert [i for i in order if i in {"X1", "X2", "X3"}] == ["X1", "X2", "X3"]


# --------------------------------------------------------------------------- #
# Merge similarity: symmetric, and not distorted by difflib's autojunk
# --------------------------------------------------------------------------- #
def test_similarity_is_symmetric():
    """An asymmetric similarity makes merging depend on iteration order.

    The regression this guards: `SequenceMatcher(None, a, b)` keys its autojunk
    heuristic off `b` alone, so on texts longer than 200 characters it scored 0.460
    one way and 0.056 the other for the same pair of propositions.
    """
    # The actual worst case from the debug runs: 0.031 one way, 0.451 the other.
    long_a = ("In fetal murine tissues from diabetic pregnancies, the ratio of sorbitol "
              "to glucose is significantly higher than in controls, regardless of "
              "measured NADPH/NADP+ or NADH/NAD+ redox states.")
    long_b = ("Stable isotope tracing in fetal tissues from diabetic pregnancies reveals "
              "increased utilization of maternal amino acids for fetal protein synthesis "
              "and energy metabolism, indicating adaptive nutrient sourcing rather than a "
              "primary shift in redox-driven metabolic pathways.")
    assert len(long_b) > 200, "autojunk only engages above 200 characters"
    assert text_similarity(long_a, long_b) == pytest.approx(text_similarity(long_b, long_a))

    # And it must not be symmetric-but-junked: the old code scored this pair 0.031
    # in one direction, which is not a defensible similarity for two texts that
    # share "fetal tissues from diabetic pregnancies" verbatim.
    assert text_similarity(long_a, long_b) > 0.2


def test_similarity_does_not_discard_common_characters_on_long_texts():
    """autojunk off: a near-duplicate long text must score high, not be junked apart."""
    base = ("Ferroptosis in glioma cells is driven by accumulation of lipid peroxides "
            "following inhibition of the cystine-glutamate antiporter, measured by "
            "malondialdehyde levels in cell lysates after twenty-four hours.")
    near = base.replace("twenty-four", "forty-eight")
    assert len(base) > 200
    assert text_similarity(base, near) > 0.9


def test_identical_and_empty_texts_are_handled():
    assert text_similarity("same text", "same text") == 1.0
    assert text_similarity("", "anything") == 0.0
    assert text_similarity("!!!", "???") == 0.0, "normalisation strips to empty"


# --------------------------------------------------------------------------- #
# Known defect: lexical merging cannot see the entity that carries the science
# --------------------------------------------------------------------------- #
ENTITY_SWAP_PAIRS = [
    # Every one of these was actually merged in the consequence_generate_v2 A/B run.
    ("Autophagy is activated in cancer cells undergoing disulfidptosis induced by "
     "SLC7A11-mediated cystine uptake during chronic glucose starvation.",
     "Necroptosis is activated in cancer cells undergoing disulfidptosis induced by "
     "SLC7A11-mediated cystine uptake during chronic glucose starvation."),
    ("Glucose-6-phosphate dehydrogenase (G6PD) activity is reduced in fetal tissues "
     "during mid-gestation in diabetic pregnancies.",
     "Isocitrate dehydrogenase (IDH) activity is altered in fetal tissues during "
     "mid-gestation in diabetic pregnancies."),
    ("Fetuses from diabetic pregnancies at mid-gestation have a higher NADPH/NADP+ "
     "ratio in liver tissue compared to fetuses from non-diabetic pregnancies.",
     "Fetuses from diabetic pregnancies at mid-gestation have a lower NADPH/NADP+ "
     "ratio in heart tissue compared to fetuses from non-diabetic pregnancies."),
]


@pytest.mark.xfail(strict=True, reason=(
    "Known, measured defect (DECISIONS #23). Atomic propositions share a syntactic "
    "template and differ only in the entity or direction -- exactly the tokens that "
    "carry the science -- so character-level similarity scores them 0.85-0.94 and the "
    "merger collapses them. Fixing this needs a content-aware matcher, not a "
    "threshold. The test is strict-xfail so it flips to a failure the moment the "
    "matcher improves, which is when this expectation should be deleted."))
def test_propositions_differing_only_in_the_entity_are_not_merged():
    from src.common.config import load_config

    threshold = load_config("configs/mvp.yaml").graph.merge_threshold
    for left, right in ENTITY_SWAP_PAIRS:
        assert text_similarity(left, right) < threshold, (
            "%.3f >= %.2f for a pair naming different entities" % (
                text_similarity(left, right), threshold))


def test_the_entity_swap_similarities_are_where_the_finding_says_they_are():
    """Pins the measurement itself, so the numbers in DECISIONS #23 stay honest."""
    scores = [text_similarity(a, b) for a, b in ENTITY_SWAP_PAIRS]
    assert max(scores) > 0.93, "the autophagy/necroptosis pair should score ~0.94"
    assert min(scores) > 0.82, "all three cleared the frozen 0.82 threshold"


# --------------------------------------------------------------------------- #
# The assessor rubric proposal (docs/ASSESSOR_RUBRIC.md)
# --------------------------------------------------------------------------- #
def test_the_running_assessor_is_still_v1():
    """v2 is a proposal. Nothing may switch to it before the rubric is signed off."""
    from src.evidence.assess import ASSESS_PROMPT

    assert ASSESS_PROMPT == "evidence_assess_v1"




def test_v2_separates_an_unassessable_proposition_from_a_retrieval_failure():
    text = _prompt("evidence_assess_v2").text
    assert "proposition_unassessable" in text
    assert "defect in the proposition" in " ".join(text.lower().split())


def test_the_ordinal_mapping_still_pins_no_evidence_to_zero():
    """Widening what counts as evidence must not weaken what no_evidence means."""
    from src.inference.parameters import load_ordinal_mappings

    mappings = load_ordinal_mappings("configs/ordinal_mappings.yaml")
    assert mappings.evidence_log_lr["no_evidence"] == 0.0


def test_assessor_case_ids_are_unique():
    """The same instance and node recur across runs; a colliding id drops cases.

    Caught in practice: `RBV2-0012-N00::X15` existed in both the v1-prompt and
    v2-prompt A/B runs, and keying judge answers by case_id silently lost one of the
    37 cases (the harness reported "36").
    """
    import collections
    import json

    path = Path("benchmark/assessor/labelset_candidates.jsonl")
    if not path.exists():
        pytest.skip("label set not built")
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    counts = collections.Counter(r["case_id"] for r in rows)
    duplicates = {k: v for k, v in counts.items() if v > 1}
    assert not duplicates, "duplicate case_id(s): {}".format(duplicates)




def test_the_acceptance_gate_thresholds_match_what_the_research_owner_set():
    """Pin the thresholds so they cannot drift toward whatever a run happens to score.

    This test changed purpose once the owner set them: it previously asserted they
    were UNSET (so the implementation could not invent them). Now it asserts the
    specific values, which is the same guard at the next stage. Changing a number
    here must be a deliberate edit with a reason, not a side effect of tuning.
    """
    import json

    gate = json.loads(Path("benchmark/assessor/acceptance_gate.json").read_text())
    assert gate["criterion_1_boundary_reproducibility"]["threshold"] == 0.80
    assert gate["criterion_2_direction_reproducibility"]["threshold"] == 0.80
    assert gate["criterion_3_grounded_and_independently_reproduced"]["threshold"] == 0.90
    assert gate["criterion_4_negative_control_mismatched_abstract"]["threshold_max"] == 0.10


def test_the_gate_is_tied_to_a_frozen_rubric():
    """A validation result means nothing if the construct moved under it."""
    import json

    gate = json.loads(Path("benchmark/assessor/acceptance_gate.json").read_text())
    freeze = json.loads(Path("benchmark/assessor/rubric_freeze.json").read_text())
    assert gate["rubric_freeze_sha256_16"] == freeze["sha256_16_of_construct"]


def test_the_gate_does_not_claim_expert_validation():
    """The wording guidance is part of the artifact, not an afterthought."""
    import json

    gate = json.loads(Path("benchmark/assessor/acceptance_gate.json").read_text())
    assert "accurately distinguishes" in gate["paper_wording"]["do_not_claim"]
    assert "provisional" in gate["what_this_validates"].lower()
    assert "expert" in gate["what_this_validates"].lower()


def test_the_judges_cannot_see_each_other_or_the_current_assessor():
    """Both judge prompts take only a proposition and one record."""
    for name in ("assessor_judge_a_v1", "assessor_judge_b_v1"):
        assert _prompt(name).placeholders == frozenset({"proposition", "record"})


def test_judge_b_is_never_shown_the_category_vocabulary():
    """Judge B's decorrelation from A rests on this: it cannot anchor on the labels."""
    text = _prompt("assessor_judge_b_v1").text
    for label in ("DIRECT", "INDIRECT", "NO_EVIDENCE"):
        assert label not in text, "judge B must not see the label {}".format(label)


def test_both_judges_require_a_verbatim_span():
    for name in ("assessor_judge_a_v1", "assessor_judge_b_v1"):
        text = " ".join(_prompt(name).text.lower().split())
        assert "exactly" in text and "abstract" in text
        assert "paraphrase" in text


def test_span_grounding_rejects_a_paraphrase():
    """The check must not be satisfied by text that merely sounds right."""
    import sys

    sys.path.insert(0, str(Path("scripts").resolve()))
    from validate_assessor import span_is_grounded

    abstract = "Chronic hypoxia and hyperglycemia result in increased oxidative stress."
    assert span_is_grounded("hyperglycemia result in increased oxidative stress", abstract)
    assert span_is_grounded("CHRONIC   HYPOXIA and hyperglycemia", abstract), "whitespace/case ok"
    assert not span_is_grounded("hyperglycaemia raises oxidative stress", abstract)
    assert not span_is_grounded("", abstract)
    assert not span_is_grounded(None, abstract)


def test_negation_is_model_free():
    """Control generation must not depend on the thing under test."""
    import sys

    sys.path.insert(0, str(Path("scripts").resolve()))
    from validate_assessor import negate

    assert negate("NADPH is higher in diabetic fetal tissue.").startswith("It is NOT the case")
    assert "NADPH is higher" in negate("NADPH is higher in diabetic fetal tissue.")


def test_removing_the_span_removes_its_sentence():
    import sys

    sys.path.insert(0, str(Path("scripts").resolve()))
    from validate_assessor import drop_span_sentence

    abstract = ("Diabetes was induced in pregnant mice. Oxidative stress rose in fetal "
                "tissue. Litter size was unchanged.")
    out = drop_span_sentence(abstract, "Oxidative stress rose in fetal tissue")
    assert "Oxidative stress" not in out
    assert "Litter size was unchanged" in out
    assert "Diabetes was induced" in out


# --------------------------------------------------------------------------- #
# The narrow evidence assessor (DECISIONS #29)
# --------------------------------------------------------------------------- #
def test_v2_no_longer_has_an_indirect_category():
    """Indirectness moved to the graph edges; it must not survive in the label set.

    Replaces four tests that pinned the superseded INDIRECT design. That design is
    archived unused under src/llm/prompts/superseded/ and is the subject of
    DECISIONS #28.
    """
    text = _prompt("evidence_assess_v2").text
    assert "INDIRECT" not in text
    assert "indirect evidence" not in text.lower()


def test_v2_asks_only_about_direct_bearing_on_this_proposition():
    text = " ".join(_prompt("evidence_assess_v2").text.lower().split())
    assert "report, measure, test, or state this proposition, or its negation" in text
    # And it must say that "direct" is scoped to the node, not the root hypothesis.
    assert 'it does not mean "direct evidence for some larger hypothesis"' in text


def test_v2_forbids_bridging_and_says_why():
    text = " ".join(_prompt("evidence_assess_v2").text.lower().split())
    assert "requires_external_bridge" in text
    assert "do not reason from what a finding implies" in text
    # The reason matters: an unrecorded bridge is never checked or weighted.
    assert "never gets recorded" in text


def test_v2_keeps_the_invariants_that_make_no_evidence_mean_nothing():
    text = " ".join(_prompt("evidence_assess_v2").text.lower().split())
    assert "absence of evidence is not evidence against" in text
    assert "must never be reported as a contradiction" in text
    assert "supporting_spans" in _prompt("evidence_assess_v2").text


def test_the_superseded_indirect_draft_is_archived_not_loadable_as_v2():
    archived = SRC_ROOT / "llm" / "prompts" / "superseded" / "evidence_assess_indirect_draft.txt"
    assert archived.exists(), "the failed design is kept as the record behind DECISIONS #28"
    assert "INDIRECT" in archived.read_text()
    # PromptLibrary globs one directory, so an archived prompt cannot be selected.
    from src.llm.prompts import PromptLibrary

    assert "evidence_assess_indirect_draft" not in PromptLibrary(PROMPT_DIR).available()


def test_the_narrow_judges_do_not_leak_the_category_names_to_judge_b():
    text = _prompt("assessor_narrow_judge_b_v1").text
    for label in ("DIRECT_EVIDENCE", "NO_DIRECT_EVIDENCE"):
        assert label not in text


def test_the_edge_prompt_is_where_scientific_implication_is_judged():
    """After DECISIONS #29 this is the only place a bridge between claims is made."""
    text = " ".join(_prompt("edge_assess_v1").text.lower().split())
    assert "if that candidate were true, how likely would the proposition be" in text
    assert "you have no literature access" in text


def test_the_configured_assessor_prompt_reaches_the_assessor_and_nothing_else():
    """A misplaced kwarg cost five instances of retrieval before failing.

    `assess_prompt` was appended to the first `event_log=ctx.event_log)` in the file,
    which belonged to `generate_queries`. Every instance built its graph, ran
    retrieval, then died with `generate_queries() got an unexpected keyword argument`.
    This pins the wiring without needing a live run.
    """
    import inspect

    from src.evidence.assess import assess_proposition
    from src.evidence.queries import generate_queries

    assert "assess_prompt" in inspect.signature(assess_proposition).parameters
    assert "assess_prompt" not in inspect.signature(generate_queries).parameters

    source = (SRC_ROOT / "methods" / "consequence_graph.py").read_text()
    calls = source.count("assess_prompt=config.evidence.assess_prompt")
    assert calls == 1, "expected exactly one wiring point, found %d" % calls
    # ...and it must sit inside the assess_proposition call, not a neighbouring one.
    # Naive paren-splitting fails here: the call contains a nested `(`.
    after = source.split("assess_proposition(", 1)[1]
    depth, end = 1, None
    for index, char in enumerate(after):
        depth += (char == "(") - (char == ")")
        if depth == 0:
            end = index
            break
    assert end is not None, "unbalanced parentheses around assess_proposition("
    assert "assess_prompt" in after[:end]


def test_the_narrow_assessor_is_the_method_and_broad_is_the_ablation():
    """Flipped deliberately at DECISIONS #33, on the negative-origin yield bias.

    This test previously asserted v1 was the default, when v2 was an untested
    proposal. The default moved only after 20 held-out rows showed v1 made
    negative-origin nodes informative 27% of the time against 17% for gold-origin,
    and v2 removed that asymmetry.
    """
    from src.common.config import load_config

    assert load_config("configs/mvp.yaml").evidence.assess_prompt == "evidence_assess_v2"


# --------------------------------------------------------------------------- #
# v3: multi-level abstraction (DECISIONS #34)
# --------------------------------------------------------------------------- #
def test_v3_asks_for_several_abstraction_levels():
    text = " ".join(_prompt("consequence_generate_v3").text.lower().split())
    for level in ("specific", "mechanistic", "class"):
        assert level in text
    assert "abstraction_level" in _prompt("consequence_generate_v3").text


def test_v3_requires_the_implication_link_before_abstracting():
    """Abstraction is only legitimate where the claim implies the general form.

    Without this, v3 would move the unsupported bridge out of the assessor and into
    generation, where the edge assessor would then treat it as sound.
    """
    text = " ".join(_prompt("consequence_generate_v3").text.lower().split())
    assert "you may only abstract away a specific when the claim still " \
           "probabilistically implies the more general proposition" in text
    assert "why_implied" in _prompt("consequence_generate_v3").text
    assert "not write a proposition because it sounds easier to find literature" in text


def test_v3_is_still_non_contrastive_and_atomic():
    assert "alternatives" not in _prompt("consequence_generate_v3").placeholders
    text = " ".join(_prompt("consequence_generate_v3").text.lower().split())
    assert "do not try to make a proposition distinguish this claim" in text
    assert "atomic" in text


def test_v3_is_the_method_after_structural_validation():
    """Flipped at DECISIONS #35, on structural evidence only.

    Yield 12% -> 39-45% by abstraction level, zero-yield rows 8 -> 0, flat
    discriminativeness, 0 of 258 abstracted nodes missing why_implied. Ranking was
    deliberately NOT part of the decision: the prompt was written after inspecting
    these rows' failures, so their ranking is not evidence.
    """
    from src.common.config import load_config

    assert load_config("configs/mvp.yaml").graph.generate_prompt == "consequence_generate_v3"


# --------------------------------------------------------------------------- #
# Dependency-aware aggregation (DECISIONS #37)
# --------------------------------------------------------------------------- #
def test_family_aggregation_preserves_no_evidence_meaning(mappings):
    """no_evidence must still move nothing, exactly, under the family path."""
    graph = chain_graph(strengths={"H0": "implied", "H1": "unlikely"})
    flat = score_hypotheses(graph, {}, mappings=mappings, aggregation="family").scores
    none = score_hypotheses(graph, {"X1": "no_evidence", "X2": "no_evidence"},
                            mappings=mappings, aggregation="family").scores
    assert none == pytest.approx(flat)
    assert none["H0"] == pytest.approx(0.5)


def test_family_aggregation_matches_independent_when_there_is_no_chain_structure():
    """With no chain edges every family is a singleton, so the two must agree.

    This is the degenerate case that shows the new path is a generalisation rather
    than a different model.
    """
    from src.inference.parameters import load_ordinal_mappings

    maps = load_ordinal_mappings("configs/ordinal_mappings.yaml")
    graph = ConsequenceGraph(instance_id="T", hypothesis_ids=["H0", "H1"])
    for node in ("X1", "X2", "X3"):
        graph.add_node(PropositionNode(id=node, text=node, depth=1,
                                       generation_origin_hypothesis="H0"))
    for node, s0, s1 in (("X1", "implied", "unlikely"),
                         ("X2", "strongly_implied", "neutral"),
                         ("X3", "weakly_implied", "unlikely")):
        graph.add_edge(GraphEdge(source="H0", target=node, kind="root", ordinal_strength=s0))
        graph.add_edge(GraphEdge(source="H1", target=node, kind="root", ordinal_strength=s1))
    graph.freeze()
    ev = {"X1": "support", "X2": "weak_support", "X3": "contradiction"}
    a = score_hypotheses(graph, ev, mappings=maps, aggregation="independent").scores
    b = score_hypotheses(graph, ev, mappings=maps, aggregation="family").scores
    assert b == pytest.approx(a, abs=1e-9)


def test_family_aggregation_discounts_a_restatement_of_the_same_claim(mappings):
    """The whole point: a chained descendant is not a second independent observation.

    Same evidence on a parent and its chain child should move the posterior LESS
    under family aggregation than under the independent shortcut, because the child
    is largely entailed by the parent.
    """
    graph = chain_graph(strengths={"H0": "strongly_implied", "H1": "unlikely"})
    ev = {"X1": "support", "X2": "support"}
    indep = score_hypotheses(graph, ev, mappings=mappings, aggregation="independent").scores
    fam = score_hypotheses(graph, ev, mappings=mappings, aggregation="family").scores
    assert fam["H0"] < indep["H0"], (
        "family aggregation should not double-count a chained restatement: "
        "independent gave %.4f, family gave %.4f" % (indep["H0"], fam["H0"])
    )
    assert fam["H0"] > 0.5, "it should still favour H0, just less emphatically"


def test_families_partition_every_node_exactly_once():
    from src.inference.bayes import consequence_families

    graph = chain_graph(strengths={"H0": "implied", "H1": "neutral"})
    fams = consequence_families(graph)
    members = [m for v in fams.values() for m in v]
    assert sorted(members) == sorted(graph.nodes), "families must partition the nodes"
    assert len(members) == len(set(members)), "a node may not appear in two families"
