"""The pilot must run the EXISTING method, not a variant of it.

BENCH-GRAPH-PILOT-001 asks whether the consequence-graph pipeline behaves more
appropriately on genuine competing explanations than it did on ResearchBench-style
parallel proposals. That question is only answerable if the pipeline is the same one.
A single quietly-changed threshold would turn the pilot from a diagnostic into an
uncontrolled comparison, and nobody would be able to tell from the artifacts.

So this module pins two things:

* every method parameter in `configs/pilot_explanatory.yaml` equals the value frozen
  in `benchmark/frozen/narrow_graph_v3_complete.json`;
* the pilot config differs from `configs/mvp.yaml` ONLY in the dataset fields it is
  allowed to differ in.

The second check is the one that catches drift, because it fails on changes nobody
thought to freeze.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterator, Tuple

import pytest

from src.common.config import load_config
from src.llm.prompts import PromptLibrary

ROOT = Path(__file__).resolve().parents[1]
PILOT_CONFIG = ROOT / "configs" / "pilot_explanatory.yaml"
MVP_CONFIG = ROOT / "configs" / "mvp.yaml"
FROZEN = ROOT / "benchmark" / "frozen" / "narrow_graph_v3_complete.json"

# The pilot is allowed to differ from mvp.yaml here and nowhere else: it points at a
# different dataset and labels the run honestly. Anything else is method drift.
ALLOWED_DIFFERENCES = {
    "source_path",
    "dataset.kind",
    "dataset.status",
    "dataset.case_path",
}


def _flatten(node: Any, prefix: str = "") -> Iterator[Tuple[str, Any]]:
    if isinstance(node, dict):
        for key, value in node.items():
            path = "{}.{}".format(prefix, key) if prefix else str(key)
            for item in _flatten(value, path):
                yield item
    else:
        yield prefix, node


@pytest.fixture(scope="module")
def pilot() -> Dict[str, Any]:
    return load_config(str(PILOT_CONFIG)).model_dump()


@pytest.fixture(scope="module")
def mvp() -> Dict[str, Any]:
    return load_config(str(MVP_CONFIG)).model_dump()


@pytest.fixture(scope="module")
def frozen() -> Dict[str, Any]:
    return json.loads(FROZEN.read_text(encoding="utf-8"))


def _lookup(config: Dict[str, Any], dotted: str) -> Any:
    node: Any = config
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            return KeyError
        node = node[part]
    return node


def test_pilot_differs_from_mvp_only_in_dataset_selection(pilot, mvp):
    flat_pilot = dict(_flatten(pilot))
    flat_mvp = dict(_flatten(mvp))
    assert set(flat_pilot) == set(flat_mvp), "config shape diverged"
    differing = {k for k in flat_pilot if flat_pilot[k] != flat_mvp[k]}
    unexpected = differing - ALLOWED_DIFFERENCES
    assert not unexpected, (
        "pilot config diverges from the frozen method in {}. The pilot runs the "
        "EXISTING method; changing a parameter here makes the run uninterpretable "
        "as a diagnostic.".format(sorted(unexpected)))


# Where each frozen leaf lives in the loaded config. Frozen artifacts were written
# from the method's own view of its settings, which is flatter than the config tree.
FROZEN_TO_CONFIG = {
    "graph.max_depth": "graph.max_depth",
    "graph.generate_prompt": "graph.generate_prompt",
    "graph.max_root_consequences_per_hypothesis": "graph.max_root_consequences_per_hypothesis",
    "graph.max_nodes": "graph.max_nodes",
    "graph.max_children_per_node": "graph.max_children_per_node",
    "graph.semantic_merge_mode": "graph.semantic_merge_mode",
    "graph.merge_threshold": "graph.merge_threshold",
    "retrieval_query_policy.max_terms": "retrieval.query_policy.max_terms",
    "retrieval_query_policy.min_terms": "retrieval.query_policy.min_terms",
    "retrieval_query_policy.backoff_steps": "retrieval.query_policy.backoff_steps",
    "retrieval_query_policy.strip_direction_words": "retrieval.query_policy.strip_direction_words",
    "inference.aggregation": "inference.aggregation",
    "inference.prior": "inference.prior",
    "inference.multi_parent_rule": "inference.multi_parent_rule",
    "inference.parent_false_baseline": "inference.parent_false_baseline",
    "dedup.enabled": "literature.dedup.enabled",
    "dedup.title_similarity_threshold": "literature.dedup.title_similarity_threshold",
    "dedup.possibly_related_threshold": "literature.dedup.possibly_related_threshold",
    "dedup.require_author_overlap": "literature.dedup.require_author_overlap",
    "max_papers_in_prompt": "baselines.direct_rag.max_papers_in_prompt",
    "ordinal_mappings_path": "ordinal_mappings_path",
}


def test_every_frozen_method_parameter_is_covered_by_the_mapping(frozen):
    """If the frozen artifact grows a parameter, this test fails until someone maps
    it -- rather than the parameter silently going unchecked."""
    frozen_leaves = {
        key for key, _ in _flatten(frozen["config"])
        if not key.startswith("retrieval_query_policy.direction_words")
        and not key.startswith("retrieval_query_policy.protected_phrases")
        and not key.startswith("retrieval_query_policy.stopwords")
    }
    assert frozen_leaves <= set(FROZEN_TO_CONFIG), (
        "unmapped frozen parameter(s): {}".format(
            sorted(frozen_leaves - set(FROZEN_TO_CONFIG))))


@pytest.mark.parametrize("frozen_key,config_key", sorted(FROZEN_TO_CONFIG.items()))
def test_pilot_matches_frozen_method_parameter(pilot, frozen, frozen_key, config_key):
    expected = _lookup(frozen["config"], frozen_key)
    actual = _lookup(pilot, config_key)
    assert actual == expected, "{}: pilot={!r} frozen={!r}".format(
        frozen_key, actual, expected)


def test_pilot_uses_the_frozen_assessor_prompt(pilot, frozen):
    assert pilot["evidence"]["assess_prompt"] == frozen["evidence_assess_prompt"]


def test_prompt_shas_match_the_freeze(frozen):
    """The strongest check available: the prompts on disk are byte-identical to the
    ones the freeze recorded. Config parameters can be matched while the prompt text
    underneath has changed, and the prompt text is most of the method."""
    library = PromptLibrary(ROOT / "src" / "llm" / "prompts")
    for name, record in frozen["prompt_shas"].items():
        assert library.get(name).sha == record["sha256_16"], (
            "prompt {} has changed since the method was frozen".format(name))


def test_pilot_dataset_points_at_the_frozen_case_manifest(pilot):
    assert pilot["dataset"]["kind"] == "cases"
    assert pilot["dataset"]["status"] == "pilot_diagnostic"
    assert pilot["dataset"]["case_path"].endswith("cases_visible.jsonl")
    assert "hidden" not in json.dumps(pilot["dataset"])
