"""Query shaping, the length cap, and lexical backoff.

Retrieval recall on this benchmark is dominated by query length, and "zero
results" is indistinguishable from "the literature is silent" unless the query
itself is controlled — so these rules are enforced in code, not requested in a
prompt, and tested here.
"""

from __future__ import annotations

import pytest

from src.common.config import load_config
from src.literature.query_policy import lexical_ladder, shape_query

WORDS = ["increase", "increases", "evidence", "supports", "causes", "reduced", "higher"]
STOP = ["that", "the", "of", "in", "for", "a", "an", "and", "with", "on"]


def shaped(text, **kwargs):
    kwargs.setdefault("max_terms", 6)
    kwargs.setdefault("direction_words", WORDS)
    kwargs.setdefault("stopwords", STOP)
    return shape_query(text, **kwargs)


# --------------------------------------------------------------------------- #
# The length cap
# --------------------------------------------------------------------------- #
def test_long_queries_are_truncated_to_the_cap():
    out = shaped("alpha beta gamma delta epsilon zeta eta theta", max_terms=4)
    assert out.query == "alpha beta gamma delta"
    assert out.truncated_from == 8


def test_short_queries_are_left_alone():
    out = shaped("Bi2O3 borate glass microhardness")
    assert out.query == "Bi2O3 borate glass microhardness"
    assert out.truncated_from is None and out.changed is False


def test_the_cap_is_applied_after_removal_so_slots_are_not_wasted():
    """Stripping first means the cap keeps six *useful* terms, not six tokens."""
    out = shaped("evidence that GRB 221009A increases r-process element abundance in ejecta")
    assert out.query == "GRB 221009A r-process element abundance ejecta"
    assert "evidence" in out.removed_direction_words
    assert "that" in out.removed_stopwords


# --------------------------------------------------------------------------- #
# Direction words (spec §17: queries must not encode the outcome)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("word", ["increases", "evidence", "supports", "causes", "higher"])
def test_direction_words_are_removed(word):
    out = shaped("mutation {} phospho-RPA".format(word))
    assert word not in out.query.split()
    assert word in out.removed_direction_words


def test_direction_words_survive_inside_a_protected_entity_name():
    out = shaped(
        "reduced graphene oxide conductivity increases",
        protected_phrases=["reduced graphene oxide"],
    )
    assert "reduced graphene oxide" in out.query
    assert out.removed_direction_words == ["increases"]
    assert out.protected_phrases == ["reduced graphene oxide"]


def test_removal_can_be_disabled_but_is_on_by_default():
    assert load_config("configs/mvp.yaml").retrieval.query_policy.strip_direction_words is True
    out = shaped("mutation increases phospho-RPA", strip_direction_words=False)
    assert "increases" in out.query


def test_shaping_is_deterministic_and_recorded():
    text = "evidence that M increases phospho-RPA in cultured cells"
    first, second = shaped(text), shaped(text)
    assert first.query == second.query
    record = first.record()
    assert record["original"] == text and record["changed"] is True
    assert record["removed_direction_words"] and record["query"] == first.query


def test_empty_query_survives_shaping():
    assert shaped("   ").query == ""


# --------------------------------------------------------------------------- #
# Lexical backoff
# --------------------------------------------------------------------------- #
def test_ladder_drops_one_trailing_term_at_a_time():
    assert lexical_ladder("a b c d e", min_terms=3, steps=2) == ["a b c d", "a b c"]


def test_ladder_never_goes_below_min_terms():
    assert lexical_ladder("a b c", min_terms=3, steps=5) == []
    assert lexical_ladder("a b c d", min_terms=3, steps=5) == ["a b c"]


def test_ladder_is_bounded_by_steps():
    assert len(lexical_ladder("a b c d e f g h", min_terms=1, steps=2)) == 2


def test_ladder_can_be_disabled():
    assert lexical_ladder("a b c d e", min_terms=2, steps=0) == []


def test_ladder_is_a_pure_function_of_the_text():
    a = lexical_ladder("GRB 221009A r-process nucleosynthesis yields", min_terms=3, steps=2)
    b = lexical_ladder("GRB 221009A r-process nucleosynthesis yields", min_terms=3, steps=2)
    assert a == b


# --------------------------------------------------------------------------- #
# Wiring
# --------------------------------------------------------------------------- #
def test_shipped_prompt_v2_states_the_cap_and_bans_direction_words():
    from src.llm.prompts import PromptLibrary

    config = load_config("configs/mvp.yaml")
    assert config.baselines.direct_rag.query_prompt_version == "direct_rag_query_v2"
    text = PromptLibrary(config.prompts.dir).get("direct_rag_query_v2").text
    assert "$max_terms" in text, "the cap must be rendered into the prompt, not hard-coded"
    assert "OUTCOME-NEUTRAL" in text
    for word in ("increase", "supports", "evidence"):
        assert word in text.lower()
    assert "reduced graphene oxide" in text, "the entity-name exception must be explained"


def test_v1_is_untouched_for_provenance():
    from src.llm.prompts import PromptLibrary

    v1 = PromptLibrary("src/llm/prompts").get("direct_rag_query_v1").text
    assert "$max_terms" not in v1, "v1 must remain exactly as it was when it produced results"
    assert v1.count("$n_queries") == 1


def test_backoff_fires_only_on_zero_results_and_is_recorded(config, tmp_path):
    """The trigger is the absence of results, never what the results say."""
    import json

    from src.baselines.direct_rag import DirectRag
    from src.benchmark.loader import load_instances
    from src.literature.service import InstanceSearchTool
    from src.llm.client import MockLLMClient
    from tests.conftest import s2_record, search_payload
    from tests.test_baselines import make_context, make_rag_service

    # Six-term query returns nothing; the five-term rung returns a paper.
    long_q = "alpha beta gamma delta epsilon zeta"
    payloads = {
        long_q: search_payload([]),
        "alpha beta gamma delta epsilon": search_payload(
            [s2_record("hit", title="Found on the first backoff rung", publication_date="2019-01-01")]
        ),
    }
    instances = load_instances(config, instance_ids=["RBV-01"])
    service, provider = make_rag_service(config, payloads, instances)
    provider.default = search_payload([])

    llm = MockLLMClient(
        config.llm,
        responder=lambda messages, cfg: json.dumps({"queries": [long_q, long_q]})
        if "search queries" in messages[0]["content"].lower()
        else json.dumps({"evidence_label": "weak_support", "score": 55,
                         "rationale": "r", "key_papers": []}),
    )
    ctx = make_context(config, tmp_path, literature=InstanceSearchTool(service, "RBV-01"), llm=llm)
    result = DirectRag(config).run_instance(ctx)

    assert result.status == "ok"
    assert result.diagnostics["n_queries_needing_backoff"] > 0
    assert result.diagnostics["n_searches"] > result.diagnostics["n_queries"], "backoff issued extra searches"
    assert result.diagnostics["n_queries_empty_after_backoff"] == 0

    entry = next(iter(result.artifacts["retrieval"]["by_hypothesis"].values()))
    attempts = entry["queries"][0]["attempts"]
    assert [a["step"] for a in attempts] == [0, 1]
    assert attempts[0]["n_results"] == 0 and attempts[1]["n_results"] == 1
    # A query that already returns results must not trigger extra searches.
    assert all(len(q.get("attempts", [])) == 2 for q in entry["queries"])


def test_a_query_with_results_does_not_back_off(config, tmp_path):
    import json

    from src.baselines.direct_rag import DirectRag
    from src.benchmark.loader import load_instances
    from src.literature.service import InstanceSearchTool
    from src.llm.client import MockLLMClient
    from tests.conftest import s2_record, search_payload
    from tests.test_baselines import make_context, make_rag_service

    instances = load_instances(config, instance_ids=["RBV-01"])
    service, provider = make_rag_service(config, {}, instances)
    provider.default = search_payload(
        [s2_record("p1", title="Immediately found", publication_date="2019-01-01")]
    )
    llm = MockLLMClient(
        config.llm,
        responder=lambda messages, cfg: json.dumps({"queries": ["alpha beta gamma delta"]})
        if "search queries" in messages[0]["content"].lower()
        else json.dumps({"evidence_label": "support", "score": 70, "rationale": "r", "key_papers": []}),
    )
    ctx = make_context(config, tmp_path, literature=InstanceSearchTool(service, "RBV-01"), llm=llm)
    result = DirectRag(config).run_instance(ctx)

    assert result.diagnostics["n_queries_needing_backoff"] == 0
    assert result.diagnostics["n_searches"] == result.diagnostics["n_queries"]
    assert result.diagnostics["query_recall"] == 1.0
