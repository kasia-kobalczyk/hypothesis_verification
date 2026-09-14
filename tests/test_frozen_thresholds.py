"""Tripwire for thresholds frozen by a research decision.

These values are not free parameters. Changing one should be a deliberate act
recorded in `docs/DECISIONS.md`, not a quiet edit during a refactor or a tuning
pass over the 20 development cases — so the test states them literally and fails
if they move.
"""

from __future__ import annotations

import pytest

from src.common.config import load_config

# Decided 2026-09-11; see docs/DECISIONS.md §2.
FROZEN_VERSION_SEARCH = {
    "title_similarity_threshold": 0.75,
    "title_similarity_threshold_no_authors": 0.92,
    "min_author_overlap": 1,
    "min_author_overlap_fraction": 0.5,
}


@pytest.fixture
def shipped():
    return load_config("configs/mvp.yaml")


@pytest.mark.parametrize("name,value", sorted(FROZEN_VERSION_SEARCH.items()))
def test_version_search_thresholds_are_frozen(shipped, name, value):
    assert getattr(shipped.temporal.version_search, name) == value, (
        "{} is frozen for the MVP at {}. If this is a deliberate change, update "
        "docs/DECISIONS.md and this test together — and do not tune it on the "
        "20 development cases.".format(name, value)
    )


def test_frozen_thresholds_match_the_code_defaults(shipped):
    """The YAML and the pydantic defaults must not drift apart."""
    from src.common.config import VersionSearchConfig

    defaults = VersionSearchConfig()
    for name, value in FROZEN_VERSION_SEARCH.items():
        assert getattr(defaults, name) == value, name


def test_the_freeze_is_documented():
    from src.common.io import repo_root

    config_text = (repo_root() / "configs" / "mvp.yaml").read_text(encoding="utf-8")
    assert "FROZEN FOR THE MVP" in config_text
    assert "DO NOT tune them further on these 20 cases" in config_text

    decisions = (repo_root() / "docs" / "DECISIONS.md").read_text(encoding="utf-8")
    assert "independently sampled" in decisions


def test_separation_observed_on_the_dev_slice_still_holds():
    """The frozen thresholds must still split the cases they were chosen on.

    Not a tuning loop: it asserts that the recorded separation survives, so a
    change to the similarity or author-overlap computation cannot silently
    reclassify the known preprint pairs.
    """
    import json

    from src.common.io import repo_root

    path = repo_root() / "data" / "metadata" / "source_dates.jsonl"
    if not path.exists():  # pragma: no cover - metadata is committed
        pytest.skip("frozen metadata not present")

    accepted, rejected_for_authors = [], []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        for candidate in record.get("version_candidates") or []:
            if candidate.get("accepted"):
                accepted.append(candidate)
            elif "author overlap fraction" in (candidate.get("reason") or ""):
                rejected_for_authors.append(candidate)

    assert accepted, "the two known preprint versions must still be accepted"
    assert all(c["author_overlap_fraction"] >= 0.5 for c in accepted)
    assert all(c["title_similarity"] >= 0.75 for c in accepted)
    # The same-author-different-study records must stay on the other side.
    assert all(c["author_overlap_fraction"] < 0.5 for c in rejected_for_authors)
