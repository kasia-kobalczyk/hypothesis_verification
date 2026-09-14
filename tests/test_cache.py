"""Cache reproducibility (IMPLEMENTATION_SPEC.md §8, §30)."""

from __future__ import annotations

from datetime import date

import pytest

from src.common.errors import CacheMissError
from src.literature.cache import LiteratureCache
from tests.conftest import INSTANCE_ID, s2_record, search_payload

PAYLOAD = search_payload(
    [
        s2_record("a", title="Paper A", publication_date="2019-01-01"),
        s2_record("b", title="Paper B", publication_date="2020-12-01"),
    ]
)


def test_second_call_is_served_from_cache_with_identical_results(make_service):
    service, provider = make_service({"q": PAYLOAD})
    first = service.search("q", INSTANCE_ID)
    second = service.search("q", INSTANCE_ID)

    assert len(provider.calls) == 1, "cached query must not hit the provider again"
    assert second.cache_status == "hit"
    assert [p.paper_id for p in first.eligible] == [p.paper_id for p in second.eligible]
    assert [p.eligible_date for p in first.eligible] == [p.eligible_date for p in second.eligible]
    assert [p.exclusion_reason for p in first.excluded] == [p.exclusion_reason for p in second.excluded]


def test_a_fresh_service_reuses_the_cache_on_disk(make_service):
    service, _ = make_service({"q": PAYLOAD})
    expected = [p.paper_id for p in service.search("q", INSTANCE_ID).eligible]

    # New service, empty provider: results must still come back from disk.
    replay, provider = make_service({}, default=search_payload([]))
    record = replay.search("q", INSTANCE_ID)
    assert provider.calls == []
    assert [p.paper_id for p in record.eligible] == expected


def test_refresh_bypasses_the_cache(make_service, config):
    service, provider = make_service({"q": PAYLOAD})
    service.search("q", INSTANCE_ID)

    refreshed_cfg = config.model_copy(
        update={
            "literature": config.literature.model_copy(
                update={"cache": config.literature.cache.model_copy(update={"refresh": True})}
            )
        }
    )
    service2, provider2 = make_service({"q": PAYLOAD}, cfg=refreshed_cfg)
    record = service2.search("q", INSTANCE_ID)
    assert len(provider2.calls) == 1
    assert record.cache_status == "refresh"


def test_offline_mode_raises_on_a_miss_instead_of_returning_nothing(make_service, config):
    offline_cfg = config.model_copy(
        update={
            "literature": config.literature.model_copy(
                update={"cache": config.literature.cache.model_copy(update={"offline": True})}
            )
        }
    )
    service, provider = make_service({"q": PAYLOAD}, cfg=offline_cfg)
    with pytest.raises(CacheMissError):
        service.search("never-searched", INSTANCE_ID)
    assert provider.calls == []


def test_offline_mode_replays_a_warm_cache(make_service, config):
    warm, _ = make_service({"q": PAYLOAD})
    expected = [p.paper_id for p in warm.search("q", INSTANCE_ID).eligible]

    offline_cfg = config.model_copy(
        update={
            "literature": config.literature.model_copy(
                update={"cache": config.literature.cache.model_copy(update={"offline": True})}
            )
        }
    )
    offline, provider = make_service({}, cfg=offline_cfg)
    assert [p.paper_id for p in offline.search("q", INSTANCE_ID).eligible] == expected
    assert provider.calls == []


def test_cache_key_separates_instances_queries_and_top_k():
    base = dict(
        provider="semantic_scholar",
        provider_version="graph-v1",
        query="q",
        instance_id="A",
        cutoff_date=date(2020, 1, 1),
        top_k=10,
        provider_config={"fields": ["title"]},
    )
    key = LiteratureCache.build_key(**base)
    digest = LiteratureCache.digest(key)

    for field, value in [
        ("query", "other"),
        ("instance_id", "B"),
        ("cutoff_date", date(2021, 1, 1)),
        ("top_k", 20),
        ("provider", "other"),
        ("provider_version", "v2"),
        ("retrieval_path", "citations"),
        ("provider_config", {"fields": ["abstract"]}),
    ]:
        variant = dict(base)
        variant[field] = value
        assert LiteratureCache.digest(LiteratureCache.build_key(**variant)) != digest, field

    assert LiteratureCache.digest(LiteratureCache.build_key(**base)) == digest


def test_cache_stores_raw_payload_and_normalised_snapshot(make_service, config):
    service, _ = make_service({"q": PAYLOAD})
    service.search("q", INSTANCE_ID)
    files = sorted(LiteratureCache(config.literature.cache).root.rglob("*.json"))
    assert any(p.name.endswith(".normalised.json") for p in files)
    assert any(not p.name.endswith(".normalised.json") for p in files)


def test_offline_takes_precedence_over_refresh(make_service, config):
    """`--offline --refresh-cache` must not silently reach the network."""
    warm, _ = make_service({"q": PAYLOAD})
    warm.search("q", INSTANCE_ID)

    cfg = config.model_copy(
        update={
            "literature": config.literature.model_copy(
                update={
                    "cache": config.literature.cache.model_copy(
                        update={"offline": True, "refresh": True}
                    )
                }
            )
        }
    )
    service, provider = make_service({}, cfg=cfg)
    assert [p.paper_id for p in service.search("q", INSTANCE_ID).eligible] == ["s2:a"]
    assert provider.calls == []
