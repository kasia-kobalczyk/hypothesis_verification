"""Benchmark loading (IMPLEMENTATION_SPEC.md §2, §36).

The frozen slice must load in full, with hypothesis text preserved byte for byte.
"""

from __future__ import annotations

import json

import pytest

from src.benchmark.loader import build_cutoff_registry, load_instances
from src.benchmark.presentation import build_presentation
from src.common.errors import BenchmarkDataError, MissingCutoffError
from src.common.io import read_jsonl, repo_root

DATASET = repo_root() / "data" / "researchbench_dev20.jsonl"


@pytest.fixture(scope="module")
def raw_rows():
    return list(read_jsonl(DATASET))


def test_all_twenty_development_cases_load(config, raw_rows):
    instances = load_instances(config)
    assert len(instances) == 20 == len(raw_rows)
    assert [i.id for i in instances] == [r["dev_id"] for r in raw_rows]
    assert len({i.id for i in instances}) == 20


def test_hypothesis_text_is_verbatim(config, raw_rows):
    """No stripping, no normalisation, no canonicalisation (§2, §34)."""
    by_id = {row["dev_id"]: row for row in raw_rows}
    for instance in load_instances(config):
        row = by_id[instance.id]
        assert instance.question == row["research_question"]
        assert instance.researchbench_sample_id == row["sample_id"]
        gold = instance.gold_hypothesis
        assert gold.text == row["gold_hypothesis"]
        negatives = [h for h in instance.hypotheses if not h.gold]
        assert [h.text for h in negatives] == row["model_negative_hypotheses"]
        for hypothesis in instance.hypotheses:
            assert hypothesis.text  # non-empty
            assert hypothesis.text == hypothesis.text.rstrip("\x00")


def test_more_than_two_hypotheses_are_supported(config):
    instances = load_instances(config)
    assert all(len(i.hypotheses) == 11 for i in instances)
    assert all(sum(1 for h in i.hypotheses if h.gold) == 1 for i in instances)
    assert all(len(set(i.hypothesis_ids)) == len(i.hypotheses) for i in instances)


def test_negative_pools_are_configurable(config, raw_rows):
    cfg = config.model_copy(
        update={
            "dataset": config.dataset.model_copy(
                update={
                    "negatives": config.dataset.negatives.model_copy(
                        update={"pools": ["model", "fake"], "max_negatives": 2}
                    )
                }
            )
        }
    )
    instance = load_instances(cfg, instance_ids=["RBV-01"])[0]
    assert len(instance.hypotheses) == 5  # gold + 2 model + 2 fake
    fields = [h.source_field for h in instance.hypotheses]
    assert fields == [
        "gold_hypothesis",
        "model_negative_hypotheses",
        "model_negative_hypotheses",
        "fake_negative_hypotheses",
        "fake_negative_hypotheses",
    ]
    row = raw_rows[0]
    assert instance.hypotheses[3].text == row["fake_negative_hypotheses"][0]


def test_instance_subset_selection(config):
    instances = load_instances(config, instance_ids=["RBV-03", "RBV-07"])
    assert [i.id for i in instances] == ["RBV-03", "RBV-07"]
    with pytest.raises(BenchmarkDataError):
        load_instances(config, instance_ids=["RBV-99"])


def test_frozen_cutoffs_are_attached(config):
    """Requires `python -m src.benchmark.resolve_dates` to have been run."""
    instances = load_instances(config)
    resolved = [i for i in instances if i.has_cutoff]
    assert len(resolved) == 20, "every development case needs a frozen cutoff (§36)"
    for instance in instances:
        assert instance.cutoff_basis
        assert instance.source_doi.lower() in instance.blocked_dois


def test_cutoff_registry_is_read_only_and_refuses_unknown_instances(config):
    registry = build_cutoff_registry(load_instances(config))
    assert len(registry) == 20
    with pytest.raises(MissingCutoffError):
        registry.get("NOPE")
    for attribute in ("set", "update", "add", "override", "__setitem__"):
        assert not hasattr(registry, attribute), attribute


def test_presentation_hides_gold_position_and_is_deterministic(config):
    instances = load_instances(config)
    first = [build_presentation(i, config.run) for i in instances]
    second = [build_presentation(i, config.run) for i in instances]

    for a, b in zip(first, second):
        assert a.labels == b.labels
        assert a.label_to_id == b.label_to_id

    gold_labels = {p.id_to_label[i.gold_hypothesis.id] for p, i in zip(first, instances)}
    assert len(gold_labels) > 1, "gold must not sit at a fixed presentation position"

    # Rendered text must not reveal internal ids (H0 is always the gold one).
    rendered = first[0].render()
    assert "H0" not in rendered
    assert rendered.startswith("Hypothesis A:")

    # Different seeds give different permutations.
    other = build_presentation(instances[0], config.run.model_copy(update={"seed": 999}))
    assert other.label_to_id != first[0].label_to_id


def test_presentation_can_be_disabled_for_debugging(config):
    cfg_run = config.run.model_copy(update={"hypothesis_order": "as_loaded", "anonymise_labels": False})
    instance = load_instances(config, instance_ids=["RBV-01"])[0]
    presentation = build_presentation(instance, cfg_run)
    assert presentation.labels[0] == "H0"
    assert presentation.items[0].gold is True


def test_raw_row_is_preserved_for_auditing(config, raw_rows):
    instance = load_instances(config, instance_ids=["RBV-01"])[0]
    assert instance.raw == raw_rows[0]
    assert json.dumps(instance.input_record())  # serialisable


# --------------------------------------------------------------------------- #
# Controlled listwise slices at varying k
# --------------------------------------------------------------------------- #
def test_k_set_slices_load_with_the_declared_k(config):
    from src.benchmark.loader import load_k_set_instances

    for k in (2, 3, 4):
        path = "benchmark/k_slices/k{}_sets.jsonl".format(k)
        instances = load_k_set_instances(config, dataset_path=path)
        assert instances, "no sets at k={}".format(k)
        assert {len(i.hypotheses) for i in instances} == {k}
        assert all(sum(h.gold for h in i.hypotheses) == 1 for i in instances)
        # A set without a cutoff cannot be run at all; the literature layer refuses it.
        assert all(i.cutoff_date is not None for i in instances)


def test_k_sets_are_nested_so_k_is_the_only_thing_that_changes(config):
    """H1 at k=3 must be the same hypothesis as H1 at k=2 for the same row.

    Sampling negatives independently per k would confound the size of the candidate
    set with which negatives happened to be drawn.
    """
    from src.benchmark.loader import load_k_set_instances

    smaller = {i.researchbench_sample_id: i for i in load_k_set_instances(
        config, dataset_path="benchmark/k_slices/k2_sets.jsonl")}
    larger = {i.researchbench_sample_id: i for i in load_k_set_instances(
        config, dataset_path="benchmark/k_slices/k3_sets.jsonl")}
    shared = [row for row in larger if row in smaller]
    assert shared, "no rows present at both k"
    for row in shared:
        assert smaller[row].hypotheses[0].text == larger[row].hypotheses[0].text
        assert smaller[row].hypotheses[1].text == larger[row].hypotheses[1].text


def test_a_k_set_declaring_the_wrong_k_is_refused(config, tmp_path):
    import json

    from src.benchmark.loader import load_k_set_instances
    from src.common.errors import BenchmarkDataError

    bad = tmp_path / "bad.jsonl"
    bad.write_text(json.dumps({
        "instance_id": "X-K5", "k": 5, "question": "q", "doi": "10.0/x",
        "gold_hypothesis": "g", "negatives": [{"text": "n1"}],
    }) + "\n")
    with pytest.raises(BenchmarkDataError, match="declares k=5"):
        load_k_set_instances(config, dataset_path=str(bad))
