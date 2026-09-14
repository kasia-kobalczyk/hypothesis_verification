"""End-to-end leakage tests over the agent-facing service.

IMPLEMENTATION_SPEC.md §7/§30: the provider deliberately returns post-cutoff
papers on *every* access path, and none of them may reach the caller or a
prompt. The service must also offer no way to move the cutoff.
"""

from __future__ import annotations

import inspect
import pytest

from src.common.errors import MissingCutoffError, TemporalLeakError
from src.literature.service import InstanceSearchTool, LiteratureSearchService
from tests.conftest import CUTOFF, INSTANCE_ID, SOURCE_DOI, s2_record, search_payload


MIXED = [
    s2_record("pre-1", title="Pre-cutoff study one", publication_date="2019-03-04"),
    s2_record("post-1", title="Post-cutoff study one", publication_date="2020-06-16"),
    s2_record("pre-2", title="Pre-cutoff study two", publication_date="2020-06-15"),
    s2_record("post-2", title="Post-cutoff study two", publication_date="2021-01-01"),
    s2_record("undated", title="Undated study", publication_date=None, year=None),
]


def test_search_never_returns_post_cutoff_papers(make_service):
    service, provider = make_service({"q": search_payload(MIXED)})
    papers = service.search_literature("q", INSTANCE_ID, top_k=10)
    assert [p.paper_id for p in papers] == ["s2:pre-1", "s2:pre-2"]
    assert all(p.temporal_eligible and p.eligible_date <= CUTOFF for p in papers)


def test_excluded_papers_are_kept_for_debugging_only(make_service):
    service, _ = make_service({"q": search_payload(MIXED)})
    record = service.search("q", INSTANCE_ID)
    assert {p.paper_id for p in record.excluded} == {"s2:post-1", "s2:post-2", "s2:undated"}
    assert all(not p.temporal_eligible for p in record.excluded)
    # The public accessor exposes eligible records only.
    assert {p.paper_id for p in record.public_papers()} == {"s2:pre-1", "s2:pre-2"}


@pytest.mark.parametrize(
    "call",
    [
        lambda s: s.expand_references("X", INSTANCE_ID),
        lambda s: s.expand_citations("X", INSTANCE_ID),
    ],
)
def test_reference_and_citation_expansion_are_filtered(make_service, call):
    payloads = {
        "references:X": {"data": [{"citedPaper": r} for r in MIXED]},
        "citations:X": {"data": [{"citingPaper": r} for r in MIXED]},
    }
    service, _ = make_service(payloads)
    papers = call(service)
    assert [p.paper_id for p in papers] == ["s2:pre-1", "s2:pre-2"]


def test_metadata_lookup_of_a_post_cutoff_paper_returns_nothing(make_service):
    payloads = {
        "paper:post-1": MIXED[1],
        "paper:pre-1": MIXED[0],
    }
    service, _ = make_service(payloads)
    assert service.get_paper_details("post-1", INSTANCE_ID) is None
    assert service.get_paper_details("pre-1", INSTANCE_ID).paper_id == "s2:pre-1"


def test_source_paper_is_never_returned(make_service):
    payload = search_payload([s2_record("source", publication_date="2018-01-01", doi=SOURCE_DOI)])
    service, _ = make_service({"q": payload})
    assert service.search_literature("q", INSTANCE_ID) == []


def test_render_for_prompt_is_a_second_gate(make_service):
    """Even if a post-cutoff record is handed in directly, rendering refuses."""
    service, _ = make_service({"q": search_payload(MIXED)})
    record = service.search("q", INSTANCE_ID)
    leaked = record.excluded[0]
    leaked.temporal_eligible = True  # simulate a downstream bug
    with pytest.raises(TemporalLeakError):
        service.render_for_prompt([leaked], INSTANCE_ID)


def test_rendered_prompt_text_contains_only_eligible_papers(make_service):
    service, _ = make_service({"q": search_payload(MIXED)})
    papers = service.search_literature("q", INSTANCE_ID)
    text = service.render_for_prompt(papers, INSTANCE_ID)
    assert "Pre-cutoff study one" in text
    for title in ("Post-cutoff study one", "Post-cutoff study two", "Undated study"):
        assert title not in text


def test_service_api_exposes_no_cutoff_parameter():
    """The cutoff cannot be passed in, so it cannot be overridden."""
    for name in ("search_literature", "search", "expand_references", "expand_citations",
                 "get_paper_details", "render_for_prompt"):
        params = set(inspect.signature(getattr(LiteratureSearchService, name)).parameters)
        assert not params & {"cutoff", "cutoff_date", "max_date", "since", "until"}, name
    for name in ("search", "search_with_record", "references", "citations", "paper"):
        params = set(inspect.signature(getattr(InstanceSearchTool, name)).parameters)
        assert not params & {"cutoff", "cutoff_date", "max_date", "instance_id"}, name


def test_unknown_instance_cannot_be_searched(make_service):
    service, _ = make_service({"q": search_payload(MIXED)})
    with pytest.raises(MissingCutoffError):
        service.search_literature("q", "NOT-AN-INSTANCE")


def test_instance_tool_is_bound_to_one_instance(make_service):
    service, _ = make_service({"q": search_payload(MIXED)})
    tool = InstanceSearchTool(service, INSTANCE_ID)
    assert tool.instance_id == INSTANCE_ID
    assert [p.paper_id for p in tool.search("q")] == ["s2:pre-1", "s2:pre-2"]


def test_provider_prefilter_requests_the_cutoff_window(make_service):
    service, provider = make_service({"q": search_payload(MIXED)})
    service.search_literature("q", INSTANCE_ID)
    assert provider.calls[0]["max_date"] == CUTOFF


def test_preprints_can_be_excluded_by_configuration(config, registry, make_service):
    record = s2_record("arx", publication_date="2019-01-01", venue="arXiv")
    cfg = config.model_copy(
        update={"literature": config.literature.model_copy(update={"include_preprints": False})}
    )
    service, _ = make_service({"q": search_payload([record])}, cfg=cfg)
    assert service.search_literature("q", INSTANCE_ID) == []
    service2, _ = make_service({"q": search_payload([record])})
    assert [p.paper_id for p in service2.search_literature("q", INSTANCE_ID)] == ["s2:arx"]
