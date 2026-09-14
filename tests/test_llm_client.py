"""Language-model client behaviour (IMPLEMENTATION_SPEC.md §29, §9).

The Azure client is exercised with an injected fake SDK object, so the real
request-building, parameter-fallback, usage-accounting and parsing code runs
without network access or credentials.
"""

from __future__ import annotations

import json
from types import SimpleNamespace
from typing import Any, Dict, List

import pytest

from src.common.errors import LLMError, LLMParseError
from src.common.logging_utils import EventLog
from src.llm.client import (
    DEFAULT_DEPLOYMENT,
    AzureOpenAIClient,
    MockLLMClient,
    extract_json,
    resolve_deployment,
)


class FakeCompletions:
    def __init__(self, behaviours: List[Any]):
        self.behaviours = list(behaviours)
        self.calls: List[Dict[str, Any]] = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        item = self.behaviours.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


class FakeAzureSDK:
    def __init__(self, behaviours: List[Any]):
        self.completions = FakeCompletions(behaviours)
        self.chat = SimpleNamespace(completions=self.completions)


def completion(text: str, *, tokens: int = 30):
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=text), finish_reason="stop")],
        usage=SimpleNamespace(prompt_tokens=tokens, completion_tokens=tokens, total_tokens=2 * tokens),
        model="gpt-4.1-test",
    )


# Every real prompt asks for JSON, and Azure requires the word in the messages
# when response_format=json_object, so the shared fixture does too.
MESSAGES = [{"role": "user", "content": "hello, reply with a json object"}]


# --------------------------------------------------------------------------- #
def test_json_extraction_handles_fences_and_prose():
    assert extract_json('{"a": 1}') == {"a": 1}
    assert extract_json('```json\n{"a": 2}\n```') == {"a": 2}
    assert extract_json('Sure!\n{"a": 3}\nHope that helps.') == {"a": 3}
    with pytest.raises(LLMParseError):
        extract_json("no json here")


def test_successful_call_records_usage_and_logs(config, tmp_path):
    log = EventLog(tmp_path / "events.jsonl", mirror_to_memory=True)
    client = AzureOpenAIClient(config.llm, event_log=log, client=FakeAzureSDK([completion('{"ok": 1}')]))
    response = client.complete_json(MESSAGES, purpose="test", prompt_version="v1")

    assert response.parsed == {"ok": 1}
    assert response.model == "gpt-4.1-test"
    assert client.usage_totals["total_tokens"] == 60
    assert client.n_calls == 1
    events = [e for e in log.events if e["kind"] == "llm_call"]
    assert events and events[0]["prompt_version"] == "v1"
    assert events[0]["messages"] == MESSAGES  # the exact prompt is recoverable


def test_unsupported_parameter_is_dropped_and_retried(config):
    sdk = FakeAzureSDK(
        [Exception("Unsupported value: 'temperature' is not supported with this model"),
         completion('{"ok": 1}')]
    )
    client = AzureOpenAIClient(config.llm, client=sdk)
    client.complete_json(MESSAGES, purpose="test")

    assert "temperature" in sdk.completions.calls[0]
    assert "temperature" not in sdk.completions.calls[1]
    # The drop is remembered for subsequent calls.
    sdk.completions.behaviours.append(completion('{"ok": 2}'))
    client.complete_json(MESSAGES, purpose="test")
    assert "temperature" not in sdk.completions.calls[2]


def test_api_errors_are_retried_then_raised_as_llm_error(config):
    cfg = config.llm.model_copy(update={"max_retries": 2, "backoff_base_s": 0.0})
    sdk = FakeAzureSDK([Exception("boom"), Exception("boom")])
    client = AzureOpenAIClient(cfg, client=sdk)
    with pytest.raises(LLMError):
        client.complete_json(MESSAGES, purpose="test")
    assert len(sdk.completions.calls) == 2


def test_malformed_completion_payload_is_an_error(config):
    cfg = config.llm.model_copy(update={"max_retries": 1, "backoff_base_s": 0.0})
    client = AzureOpenAIClient(cfg, client=FakeAzureSDK([SimpleNamespace(choices=[])]))
    with pytest.raises(LLMError):
        client.complete_json(MESSAGES, purpose="test")


def test_parse_failures_trigger_a_bounded_repair_loop(config):
    cfg = config.llm.model_copy(update={"parse_retries": 2, "backoff_base_s": 0.0})
    sdk = FakeAzureSDK([completion("nope"), completion("still nope"), completion('{"ok": 1}')])
    client = AzureOpenAIClient(cfg, client=sdk)
    response = client.complete_json(MESSAGES, purpose="test")

    assert response.parsed == {"ok": 1}
    assert client.n_parse_failures == 2
    # The repair turn feeds the bad reply back for correction.
    assert sdk.completions.calls[1]["messages"][-1]["content"].startswith("Your previous reply")


def test_repair_budget_is_finite(config):
    cfg = config.llm.model_copy(update={"parse_retries": 1, "backoff_base_s": 0.0})
    sdk = FakeAzureSDK([completion("nope"), completion("nope again")])
    client = AzureOpenAIClient(cfg, client=sdk)
    with pytest.raises(LLMParseError):
        client.complete_json(MESSAGES, purpose="test")


def test_validator_rejection_counts_as_a_parse_failure(config):
    cfg = config.llm.model_copy(update={"parse_retries": 1, "backoff_base_s": 0.0})
    sdk = FakeAzureSDK([completion('{"wrong": 1}'), completion('{"right": 1}')])
    client = AzureOpenAIClient(cfg, client=sdk)

    def validator(parsed):
        if "right" not in parsed:
            raise ValueError("missing 'right'")

    assert client.complete_json(MESSAGES, purpose="test", validator=validator).parsed == {"right": 1}


def test_json_mode_is_requested_when_configured(config):
    sdk = FakeAzureSDK([completion('{"ok": 1}')])
    client = AzureOpenAIClient(config.llm, client=sdk)
    client.complete_json(MESSAGES, purpose="test")
    assert sdk.completions.calls[0]["response_format"] == {"type": "json_object"}
    assert sdk.completions.calls[0]["model"] == client.deployment
    assert sdk.completions.calls[0]["seed"] == config.llm.seed


# --------------------------------------------------------------------------- #
# Deployment selection
# --------------------------------------------------------------------------- #
def test_deployment_resolution_order(config, monkeypatch):
    """--model / llm.deployment > $LLM_MODEL > built-in default."""
    monkeypatch.setattr("src.llm.client.ensure_env_loaded", lambda: None)
    for name in ("LLM_MODEL", "LLM_DEPLOYMENT", "AZURE_OPENAI_DEPLOYMENT"):
        monkeypatch.delenv(name, raising=False)

    assert resolve_deployment(config.llm) == (DEFAULT_DEPLOYMENT, "default")

    monkeypatch.setenv("LLM_MODEL", "gpt-5-mini")
    assert resolve_deployment(config.llm) == ("gpt-5-mini", "env")

    explicit = config.llm.model_copy(update={"deployment": "gpt-4.1-other"})
    assert resolve_deployment(explicit) == ("gpt-4.1-other", "config")


def test_litellm_style_prefix_is_stripped(config, monkeypatch):
    """The author's other projects set `LLM_MODEL=azure/<name>`."""
    monkeypatch.setattr("src.llm.client.ensure_env_loaded", lambda: None)
    monkeypatch.setenv("LLM_MODEL", "azure/gpt-4.1-kasia")
    assert resolve_deployment(config.llm) == ("gpt-4.1-kasia", "env")

    explicit = config.llm.model_copy(update={"deployment": "azure/gpt-5-mini"})
    assert resolve_deployment(explicit) == ("gpt-5-mini", "config")


def test_resolved_deployment_is_what_gets_called(config, monkeypatch):
    monkeypatch.setattr("src.llm.client.ensure_env_loaded", lambda: None)
    monkeypatch.setenv("LLM_MODEL", "azure/from-env")
    sdk = FakeAzureSDK([completion('{"ok": 1}')])
    client = AzureOpenAIClient(config.llm, client=sdk)
    client.complete_json(MESSAGES, purpose="test")
    assert client.deployment == "from-env"
    assert sdk.completions.calls[0]["model"] == "from-env"


def test_cli_model_flag_wins_and_is_recorded(tmp_path, monkeypatch):
    """`--model` must reach the run manifest, not just the client."""
    from src.experiments.run import main as run_main
    from src.common.io import read_json

    monkeypatch.setattr("src.llm.client.ensure_env_loaded", lambda: None)
    monkeypatch.setenv("LLM_MODEL", "should-be-ignored")
    run_dir = tmp_path / "runs"
    assert run_main([
        "--method", "direct_judge", "--instances", "RBV-01", "--llm", "mock",
        "--model", "azure/gpt-4.1-chosen",
        "--set", "run.output_root={}".format(run_dir),
    ]) == 0
    manifest = read_json(next(run_dir.glob("*/manifest.json")))
    assert manifest["llm"]["deployment"] == "gpt-4.1-chosen"
    assert manifest["llm"]["deployment_source"] == "config"


def test_missing_azure_credentials_fail_loudly(config, monkeypatch):
    for name in ("AZURE_API_KEY", "AZURE_OPENAI_API_KEY", "AZURE_API_BASE", "AZURE_OPENAI_ENDPOINT"):
        monkeypatch.delenv(name, raising=False)
    # `client.py` imported the name, so patching `src.common.env` would miss it
    # and a developer `.env` would silently restore the credentials.
    monkeypatch.setattr("src.llm.client.ensure_env_loaded", lambda: None)
    with pytest.raises(LLMError) as excinfo:
        AzureOpenAIClient(config.llm)
    assert "AZURE_API_KEY" in str(excinfo.value)


def test_mock_client_is_deterministic(config):
    a = MockLLMClient(config.llm).complete(MESSAGES, purpose="test")
    b = MockLLMClient(config.llm).complete(MESSAGES, purpose="test")
    assert a.text == b.text
    assert json.loads(a.text)


def test_azure_json_mode_requires_the_word_json_in_the_prompt(config):
    """Azure 400s otherwise; failing here costs no API call and names the prompt."""
    sdk = FakeAzureSDK([completion('{"ok": 1}')])
    client = AzureOpenAIClient(config.llm, client=sdk)
    with pytest.raises(LLMError) as excinfo:
        client.complete_json(
            [{"role": "user", "content": "Rank these hypotheses."}],
            purpose="direct_judge",
            prompt_version="direct_judge_v1",
        )
    assert "direct_judge_v1" in str(excinfo.value)
    assert sdk.completions.calls == [], "the request must not be sent"

    client.complete_json(
        [{"role": "user", "content": "Rank these. Return a JSON object."}], purpose="direct_judge"
    )
    assert len(sdk.completions.calls) == 1


def test_shipped_prompts_satisfy_the_azure_json_rule(config):
    """Every versioned template must mention json, or runs 400 at call time."""
    from src.llm.prompts import PromptLibrary

    library = PromptLibrary(config.prompts.dir)
    for name in library.available():
        assert "json" in library.get(name).text.lower(), name
