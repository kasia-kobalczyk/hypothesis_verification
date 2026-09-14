"""Scientific invariants that must hold across the codebase.

IMPLEMENTATION_SPEC.md §16, §20, §30, §35. These tests guard decisions that are
easy to erode silently during refactoring.
"""

from __future__ import annotations

import re

import pytest
import yaml

from src.common.errors import ConfigError
from src.common.io import repo_root
from src.inference.parameters import (
    EDGE_LABELS,
    EVIDENCE_LABELS,
    OrdinalMappings,
    load_ordinal_mappings,
    normalise_evidence_label,
    validate_mappings,
)

SRC = repo_root() / "src"


# --------------------------------------------------------------------------- #
# Ordinal mappings
# --------------------------------------------------------------------------- #
def test_shipped_mappings_are_valid(config):
    mappings = load_ordinal_mappings(config.ordinal_mappings_path)
    assert set(mappings.evidence_log_lr) == set(EVIDENCE_LABELS)
    assert set(mappings.edge_probabilities) == set(EDGE_LABELS)


def test_no_evidence_is_neutral(config):
    """§20/§35.5: failing to retrieve evidence must not count against a hypothesis."""
    mappings = load_ordinal_mappings(config.ordinal_mappings_path)
    assert mappings.evidence_value("no_evidence") == 0.0

    broken = mappings.model_copy(deep=True)
    broken.evidence_log_lr["no_evidence"] = -1.0
    with pytest.raises(ConfigError):
        validate_mappings(broken)


def test_mixed_and_no_evidence_are_distinct_labels():
    assert "mixed" in EVIDENCE_LABELS and "no_evidence" in EVIDENCE_LABELS
    assert normalise_evidence_label("No Evidence") == "no_evidence"
    assert normalise_evidence_label("strong support") == "strong_support"
    assert normalise_evidence_label("nonsense") is None


def test_mappings_must_be_monotone(config):
    mappings = load_ordinal_mappings(config.ordinal_mappings_path)
    broken = mappings.model_copy(deep=True)
    broken.evidence_log_lr["support"] = 99.0  # now above strong_support
    with pytest.raises(ConfigError):
        validate_mappings(broken)

    broken_edges = mappings.model_copy(deep=True)
    broken_edges.edge_probabilities["implied"] = 0.99
    with pytest.raises(ConfigError):
        validate_mappings(broken_edges)


def test_incomplete_mappings_are_rejected():
    with pytest.raises(ConfigError):
        validate_mappings(OrdinalMappings(edge_probabilities={}, evidence_log_lr={}))


def test_mapping_values_are_not_duplicated_in_python(config):
    """§16: numeric mappings live in YAML, not scattered through the code."""
    mappings = load_ordinal_mappings(config.ordinal_mappings_path)
    literals = {str(v) for v in mappings.evidence_log_lr.values() if v not in (0.0,)}
    offenders = []
    for path in SRC.rglob("*.py"):
        if path.name == "parameters.py":
            continue
        text = path.read_text(encoding="utf-8")
        for label in EVIDENCE_LABELS:
            for literal in literals:
                if re.search(r"{}[\"']?\s*:\s*{}".format(label, re.escape(literal)), text):
                    offenders.append((str(path), label, literal))
    assert not offenders, "ordinal values must not be hard-coded: {}".format(offenders)


def test_calibration_is_deferred():
    from src.inference.parameters import fit_calibration

    with pytest.raises(NotImplementedError):
        fit_calibration([])


# --------------------------------------------------------------------------- #
# Graph naming invariant (§12, §30, §35.4)
# --------------------------------------------------------------------------- #
def test_no_separate_C_variable_or_node_type():
    """Proposition truth is `X_v`; retrieved literature evidence is `D_v`."""
    # Catches the plausible spellings of a reintroduced `C` node type, including
    # `class ConsequenceNode` — a tripwire, not a proof.
    pattern = re.compile(
        r"\bC_v\b"
        r"|\bclass C(?:onsequence)?[A-Za-z_]*(?:Node|Var|Variable)\b"
        r"|\bConsequenceVariable\b"
        r"|[\"']C[\"']\s*:\s*[\"']node"
    )
    offenders = [
        str(path) for path in SRC.rglob("*.py") if pattern.search(path.read_text(encoding="utf-8"))
    ]
    assert not offenders, "a separate `C` proposition type must not be reintroduced: {}".format(offenders)


def test_graph_uses_X_for_propositions_and_has_no_terminal_node_type():
    """§12, §35.3, §35.4: one proposition type, `X_v`, assessable at any depth."""
    from src.graph.schema import ConsequenceGraph, PropositionNode, is_hypothesis

    assert is_hypothesis("H0") and not is_hypothesis("X1")
    node = PropositionNode(id="X1", text="p")
    # There is no "consequence"/"terminal"/"observable" node class to choose from.
    assert node.empirically_assessable is True
    assert "C" not in type(node).model_fields
    graph = ConsequenceGraph(instance_id="T", hypothesis_ids=["H0"])
    deep = PropositionNode(id="X9", text="deep", depth=3, empirically_assessable=True)
    graph.add_node(deep)
    assert graph.assessable_nodes() == [deep], "depth must not gate assessability"


# --------------------------------------------------------------------------- #
# Prompts (§17, §31)
# --------------------------------------------------------------------------- #
def test_prompt_templates_are_versioned_and_hashed(config):
    from src.llm.prompts import PromptLibrary

    library = PromptLibrary(config.prompts.dir)
    names = library.available()
    assert names, "no prompt templates found"
    for name in names:
        assert re.search(r"_v\d+$", name), "prompt {} is not version-suffixed".format(name)
        template = library.get(name)
        assert template.sha == library.get(name).sha


def test_query_prompt_demands_outcome_neutrality(config):
    from src.llm.prompts import PromptLibrary

    raw = PromptLibrary(config.prompts.dir).get(
        config.baselines.direct_rag.query_prompt_version
    ).text.lower()
    text = " ".join(raw.split())
    assert "outcome-neutral" in text
    assert "evidence that" in text  # the negative example is present
    assert "without encoding the outcome" in text
    assert "do not include years, date ranges" in text


def test_assessment_prompt_separates_missing_from_contradictory_evidence(config):
    from src.llm.prompts import PromptLibrary

    text = PromptLibrary(config.prompts.dir).get(
        config.baselines.direct_rag.assess_prompt_version
    ).text.lower()
    assert "no_evidence" in text
    assert "not evidence against" in text
    assert "mixed" in text


def test_no_prompt_mentions_a_cutoff_date(config):
    """§7: the cutoff is enforced by the backend, not announced to the model."""
    from src.llm.prompts import PromptLibrary

    library = PromptLibrary(config.prompts.dir)
    for name in library.available():
        text = library.get(name).text.lower()
        assert "cutoff" not in text, name
        assert "$cutoff" not in text, name
        assert not re.search(r"\b(19|20)\d\d-\d\d-\d\d\b", text), name


# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
def test_unresolved_choices_stay_marked_as_placeholders():
    """§14 and §22 are still unresolved. The values now have working defaults so
    the verifier can run, but they must remain flagged as research decisions
    rather than quietly hardening into settled method."""
    text = (repo_root() / "configs" / "mvp.yaml").read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    assert data["graph"]["merge_threshold"] is not None
    assert data["inference"]["multi_parent_rule"] in ("noisy_or", "max", "mean")
    assert text.count("TODO(research)") >= 3
    graph_block = text[text.index("\ngraph:"):text.index("\nretrieval:")]
    inference_block = text[text.index("\ninference:"):]
    assert "TODO(research)" in graph_block, "merge_threshold must stay flagged"
    assert "TODO(research)" in inference_block, "inference rules must stay flagged"


def test_config_rejects_unknown_keys(tmp_path):
    from src.common.config import load_config

    path = tmp_path / "bad.yaml"
    path.write_text("literature:\n  topk: 5\n", encoding="utf-8")
    with pytest.raises(ConfigError):
        load_config(path)


def test_cli_overrides_are_typed(tmp_path):
    from src.common.config import load_config

    config = load_config(
        repo_root() / "configs" / "mvp.yaml",
        overrides=["literature.top_k=3", "literature.cache.offline=true", "llm.provider=mock"],
    )
    assert config.literature.top_k == 3
    assert config.literature.cache.offline is True
    assert config.llm.provider == "mock"
