"""Version deduplication (IMPLEMENTATION_SPEC.md §6, §21, §30)."""

from __future__ import annotations

from datetime import date

from src.literature.base import Author
from src.literature.dedup import deduplicate, title_similarity
from tests.conftest import INSTANCE_ID, make_paper, s2_record, search_payload


def paper(pid, title, authors, doi=None, arxiv=None, rank=1):
    p = make_paper(pid, date(2019, 1, 1), title=title, doi=doi, retrieval_rank=rank)
    p.authors = [Author(name=name) for name in authors]
    if arxiv:
        p.raw = {"externalIds": {"ArXiv": arxiv}}
    return p


def test_same_doi_is_one_piece_of_evidence(config):
    papers = [
        paper("a", "A study of things", ["Jane Smith"], doi="10.1/x"),
        paper("b", "A study of things (revised)", ["Jane Smith"], doi="10.1/X"),
    ]
    outcome = deduplicate(papers, config.literature.dedup)
    assert [p.paper_id for p in outcome.papers] == ["a"]
    assert outcome.collapsed[0].duplicate_of == "a"
    assert outcome.papers[0].versions == ["b"]


def test_preprint_and_journal_version_are_linked_by_title_and_authors(config):
    preprint = paper("arx", "Deep mechanisms of protein folding", ["A. Lee", "B. Chen"], arxiv="2001.00001")
    journal = paper("jnl", "Deep mechanisms of protein folding", ["A. Lee", "B. Chen", "C. Diaz"], doi="10.1/j")
    outcome = deduplicate([preprint, journal], config.literature.dedup)
    assert [p.paper_id for p in outcome.papers] == ["arx"]
    assert outcome.collapsed[0].paper_id == "jnl"
    assert outcome.n_collapsed == 1


def test_shared_arxiv_id_links_versions(config):
    a = paper("a", "Totally different title one", ["X Y"], arxiv="2101.99999")
    b = paper("b", "Completely other title two", ["Z W"], arxiv="2101.99999")
    outcome = deduplicate([a, b], config.literature.dedup)
    assert [p.paper_id for p in outcome.papers] == ["a"]


def test_similar_titles_without_shared_authors_are_only_flagged(config):
    a = paper("a", "Effects of X on Y in mice", ["Jane Smith"])
    b = paper("b", "Effects of X on Y in mice", ["Other Person"])
    outcome = deduplicate([a, b], config.literature.dedup)
    assert [p.paper_id for p in outcome.papers] == ["a", "b"], "independent replications must survive"
    assert outcome.papers[1].possibly_related_to == ["a"]
    assert outcome.possibly_related


def test_distinct_studies_are_not_merged(config):
    a = paper("a", "Effects of X on Y in mice", ["Jane Smith"])
    b = paper("b", "A completely unrelated investigation of Z", ["Jane Smith"])
    outcome = deduplicate([a, b], config.literature.dedup)
    assert [p.paper_id for p in outcome.papers] == ["a", "b"]
    assert not outcome.collapsed


def test_deduplication_can_be_disabled(config):
    cfg = config.literature.dedup.model_copy(update={"enabled": False})
    papers = [paper("a", "T", ["S"], doi="10.1/x"), paper("b", "T", ["S"], doi="10.1/x")]
    outcome = deduplicate(papers, cfg)
    assert len(outcome.papers) == 2


def test_service_deduplicates_within_a_query(make_service):
    records = [
        s2_record("v1", title="One mechanism, two versions", publication_date="2019-01-01",
                  authors=["A Author"], external_ids={"ArXiv": "1901.00001"}),
        s2_record("v2", title="One mechanism, two versions", publication_date="2019-06-01",
                  authors=["A Author"], doi="10.1/journal"),
    ]
    service, _ = make_service({"q": search_payload(records)})
    result = service.search("q", INSTANCE_ID)
    assert result.n_duplicates_collapsed == 1
    assert [p.paper_id for p in result.eligible] == ["s2:v1"]


def test_title_similarity_is_normalisation_insensitive():
    assert title_similarity("The Effect of X!", "the effect of x") == 1.0
    assert title_similarity(None, "x") == 0.0


def test_repeated_deduplication_is_idempotent(config):
    """Dedup runs per query and again across queries over the same objects."""
    a = paper("a", "Effects of X on Y in mice", ["Jane Smith"])
    b = paper("b", "Effects of X on Y in mice", ["Other Person"])
    c = paper("c", "Effects of X on Y in mice", ["Jane Smith"], doi="10.1/c")
    d = paper("d", "Effects of X on Y in mice", ["Jane Smith"], doi="10.1/c")

    for _ in range(3):
        outcome = deduplicate([a, b, c, d], config.literature.dedup)

    # `b` shares the title but no author, so it stays separate and is only flagged.
    assert [p.paper_id for p in outcome.papers] == ["a", "b"]
    assert a.possibly_related_to == ["b"]
    assert b.possibly_related_to == ["a"]
    # `c` merges on title+author, `d` then merges through c's DOI — each recorded once.
    assert a.versions == ["c", "d"]
