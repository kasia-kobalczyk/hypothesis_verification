"""Language-model backend (Azure OpenAI) plus a deterministic offline stub.

IMPLEMENTATION_SPEC.md §9/§29:

* every call is logged with its purpose, prompt version, full messages, raw
  response, token usage, attempt count and latency;
* a parse failure is surfaced as `LLMParseError` and recorded — never silently
  turned into an abstention or an evidence label.

The Azure client reads `AZURE_API_KEY`, `AZURE_API_BASE` and `AZURE_API_VERSION`
(the convention already used in the author's other projects), falling back to
the standard `AZURE_OPENAI_*` names. The deployment is resolved by
`resolve_deployment`: config value, else $LLM_MODEL, else the built-in default.
"""

from __future__ import annotations

import abc
import json
import random
import re
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

from src.common.config import LLMConfig
from src.common.env import (
    AZURE_BASE_VARS,
    AZURE_KEY_VARS,
    AZURE_VERSION_VARS,
    LLM_MODEL_VARS,
    ensure_env_loaded,
    get_env,
)
from src.common.errors import LLMError, LLMParseError
from src.common.io import stable_hash
from src.common.logging_utils import NULL_EVENT_LOG, EventLog, get_logger

LOGGER = get_logger("llm")

Message = Dict[str, str]

# Used when neither the config nor the environment names a deployment.
DEFAULT_DEPLOYMENT = "gpt-4.1-kasia"


def resolve_deployment(config: LLMConfig) -> Tuple[str, str]:
    """Return `(deployment, source)`.

    Resolution order, highest first:
      1. `llm.deployment` in the config (which `--model` / `--set` write to);
      2. $LLM_MODEL / $LLM_DEPLOYMENT / $AZURE_OPENAI_DEPLOYMENT;
      3. `DEFAULT_DEPLOYMENT`.

    A LiteLLM-style `azure/<name>` value is accepted and the prefix stripped, so
    one `.env` can serve this project and a LiteLLM-based one.
    """
    if config.deployment:
        return _strip_provider_prefix(config.deployment), "config"
    from_env = get_env(*LLM_MODEL_VARS)
    if from_env:
        return _strip_provider_prefix(from_env), "env"
    return DEFAULT_DEPLOYMENT, "default"


def _strip_provider_prefix(name: str) -> str:
    value = str(name).strip()
    for prefix in ("azure/", "azure_openai/", "openai/"):
        if value.lower().startswith(prefix):
            return value[len(prefix):]
    return value

_FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL)


@dataclass
class LLMResponse:
    text: str
    parsed: Optional[Dict[str, Any]] = None
    usage: Dict[str, int] = field(default_factory=dict)
    model: str = ""
    attempts: int = 1
    latency_s: float = 0.0
    purpose: str = ""
    prompt_version: Optional[str] = None
    finish_reason: Optional[str] = None
    call_id: str = ""

    def record(self, *, include_messages: Optional[List[Message]] = None) -> Dict[str, Any]:
        out: Dict[str, Any] = {
            "call_id": self.call_id,
            "purpose": self.purpose,
            "prompt_version": self.prompt_version,
            "model": self.model,
            "attempts": self.attempts,
            "latency_s": round(self.latency_s, 3),
            "usage": self.usage,
            "finish_reason": self.finish_reason,
            "response_text": self.text,
            "parsed": self.parsed,
        }
        if include_messages is not None:
            out["messages"] = include_messages
        return out


def extract_json(text: str) -> Dict[str, Any]:
    """Best-effort JSON extraction from a model reply.

    Handles bare JSON, fenced blocks, and leading/trailing prose. Raises
    `LLMParseError` rather than returning a partial or guessed structure.
    """
    if text is None:
        raise LLMParseError("empty model response", raw_text="")
    candidates: List[str] = []
    stripped = text.strip()
    if stripped:
        candidates.append(stripped)
    for match in _FENCE_RE.finditer(text):
        candidates.append(match.group(1).strip())
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end > start:
        candidates.append(text[start : end + 1])

    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
        except (json.JSONDecodeError, ValueError):
            continue
        if isinstance(parsed, dict):
            return parsed
        if isinstance(parsed, list):
            return {"items": parsed}
    raise LLMParseError("model reply was not valid JSON", raw_text=text[:4000])


class BaseLLMClient(abc.ABC):
    """Common call/retry/logging behaviour."""

    provider = "base"

    def __init__(self, config: LLMConfig, *, event_log: Optional[EventLog] = None):
        self.config = config
        self.event_log = event_log or NULL_EVENT_LOG
        self.usage_totals: Dict[str, int] = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        self.n_calls = 0
        self.n_parse_failures = 0

    # ------------------------------------------------------------------ #
    @abc.abstractmethod
    def _invoke(self, messages: List[Message], *, json_mode: bool) -> LLMResponse:
        """One raw model call. Retries/backoff are handled by `complete`."""

    def _validate_request(
        self,
        messages: List[Message],
        *,
        json_mode: bool,
        purpose: str,
        prompt_version: Optional[str],
    ) -> None:
        """Provider-specific preflight. Raise `LLMError` to refuse the call."""

    def complete(
        self,
        messages: List[Message],
        *,
        purpose: str,
        prompt_version: Optional[str] = None,
        json_mode: Optional[bool] = None,
    ) -> LLMResponse:
        use_json = self.config.json_mode if json_mode is None else json_mode
        self._validate_request(
            messages, json_mode=use_json, purpose=purpose, prompt_version=prompt_version
        )
        call_id = stable_hash({"purpose": purpose, "messages": messages, "n": self.n_calls}, length=12)
        last_error: Optional[Exception] = None
        started = time.monotonic()

        for attempt in range(1, self.config.max_retries + 1):
            try:
                response = self._invoke(messages, json_mode=use_json)
            except LLMError as exc:
                last_error = exc
                self.event_log.error(
                    "llm", str(exc), purpose=purpose, attempt=attempt, prompt_version=prompt_version
                )
                LOGGER.warning("llm call failed (attempt %d/%d): %s", attempt, self.config.max_retries, exc)
                if attempt < self.config.max_retries:
                    time.sleep(self.config.backoff_base_s * (2 ** (attempt - 1)) * (0.5 + random.random() / 2))
                    continue
                raise
            response.attempts = attempt
            response.purpose = purpose
            response.prompt_version = prompt_version
            response.call_id = call_id
            response.latency_s = time.monotonic() - started
            self.n_calls += 1
            for key in self.usage_totals:
                self.usage_totals[key] += int(response.usage.get(key, 0) or 0)
            self.event_log.emit(
                "llm_call",
                purpose=purpose,
                prompt_version=prompt_version,
                model=response.model,
                call_id=call_id,
                attempts=attempt,
                usage=response.usage,
                latency_s=round(response.latency_s, 3),
                messages=messages,
                response_text=response.text,
                finish_reason=response.finish_reason,
            )
            return response

        raise LLMError("model call failed: {}".format(last_error))

    def complete_json(
        self,
        messages: List[Message],
        *,
        purpose: str,
        prompt_version: Optional[str] = None,
        validator: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> LLMResponse:
        """Call the model and parse a JSON object, with bounded repair attempts."""
        attempt_messages = list(messages)
        last_error: Optional[LLMParseError] = None

        for repair in range(self.config.parse_retries + 1):
            response = self.complete(
                attempt_messages, purpose=purpose, prompt_version=prompt_version, json_mode=True
            )
            try:
                parsed = extract_json(response.text)
                if validator is not None:
                    validator(parsed)
                response.parsed = parsed
                return response
            except (LLMParseError, ValueError) as exc:
                last_error = exc if isinstance(exc, LLMParseError) else LLMParseError(str(exc), raw_text=response.text)
                self.n_parse_failures += 1
                self.event_log.error(
                    "llm_parse",
                    str(exc),
                    purpose=purpose,
                    prompt_version=prompt_version,
                    repair_attempt=repair,
                    raw_text=response.text[:2000],
                )
                LOGGER.warning("parse failure for %s (repair %d): %s", purpose, repair, exc)
                if repair < self.config.parse_retries:
                    attempt_messages = list(messages) + [
                        {"role": "assistant", "content": response.text},
                        {
                            "role": "user",
                            "content": (
                                "Your previous reply could not be parsed as JSON ({}). "
                                "Reply again with a single valid JSON object and nothing "
                                "else.".format(exc)
                            ),
                        },
                    ]
        raise last_error or LLMParseError("unparsable model reply", raw_text="")


class AzureOpenAIClient(BaseLLMClient):
    provider = "azure"

    def __init__(self, config: LLMConfig, *, event_log: Optional[EventLog] = None, client: Any = None):
        super().__init__(config, event_log=event_log)
        self._unsupported_params: set = set()
        self.deployment, self.deployment_source = resolve_deployment(config)
        if client is not None:
            self._client = client
            return
        ensure_env_loaded()
        api_key = get_env(*AZURE_KEY_VARS)
        endpoint = get_env(*AZURE_BASE_VARS)
        api_version = get_env(*AZURE_VERSION_VARS, default="2024-05-01-preview")
        missing = [
            name
            for name, value in (("AZURE_API_KEY", api_key), ("AZURE_API_BASE", endpoint))
            if not value
        ]
        if missing:
            raise LLMError(
                "missing Azure OpenAI configuration: {}. Set them in the environment or in "
                "a .env file at the repository root.".format(", ".join(missing))
            )
        try:
            from openai import AzureOpenAI
        except ImportError as exc:  # pragma: no cover
            raise LLMError("the `openai` package is required for provider=azure: {}".format(exc))
        self._client = AzureOpenAI(
            api_key=api_key,
            azure_endpoint=endpoint,
            api_version=api_version,
            timeout=config.request_timeout_s,
            max_retries=0,  # retries are handled here, so they can be logged
        )
        LOGGER.info(
            "azure openai client ready (deployment=%s [from %s], api_version=%s)",
            self.deployment, self.deployment_source, api_version,
        )

    def _validate_request(
        self,
        messages: List[Message],
        *,
        json_mode: bool,
        purpose: str,
        prompt_version: Optional[str],
    ) -> None:
        """Refuse a request Azure will reject, before spending an API call.

        Azure returns HTTP 400 for `response_format: json_object` unless the
        messages mention "json". Prompts are versioned method artifacts, so the
        harness refuses rather than silently appending an instruction to one.
        """
        if not json_mode:
            return
        text = " ".join(m.get("content", "") for m in messages).lower()
        if "json" in text:
            return
        raise LLMError(
            "Azure rejects response_format=json_object unless the prompt mentions "
            "'json'; prompt {!r} (purpose {!r}) does not. Add the word to the "
            "template, or set llm.json_mode=false.".format(prompt_version or "<none>", purpose)
        )

    def _kwargs(self, messages: List[Message], json_mode: bool) -> Dict[str, Any]:
        kwargs: Dict[str, Any] = {
            "model": self.deployment,
            "messages": messages,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "top_p": self.config.top_p,
        }
        if self.config.seed is not None:
            kwargs["seed"] = self.config.seed
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        for name in self._unsupported_params:
            kwargs.pop(name, None)
        return kwargs

    @staticmethod
    def _unsupported_param_name(message: str) -> Optional[str]:
        for name in ("temperature", "top_p", "seed", "max_tokens", "response_format"):
            if name in message and ("unsupported" in message.lower() or "not supported" in message.lower()):
                return name
        return None

    def _invoke(self, messages: List[Message], *, json_mode: bool) -> LLMResponse:
        started = time.monotonic()
        try:
            completion = self._client.chat.completions.create(**self._kwargs(messages, json_mode))
        except Exception as exc:
            name = self._unsupported_param_name(str(exc))
            if name and name not in self._unsupported_params:
                LOGGER.warning("deployment rejected parameter %r; retrying without it", name)
                self.event_log.decision("llm_param_dropped", param=name, error=str(exc)[:500])
                self._unsupported_params.add(name)
                try:
                    completion = self._client.chat.completions.create(
                        **self._kwargs(messages, json_mode)
                    )
                except Exception as retry_exc:
                    # Must stay an LLMError so `complete` can retry and log it.
                    raise LLMError(
                        "azure openai call failed after dropping {!r}: {}".format(name, retry_exc)
                    )
            else:
                raise LLMError("azure openai call failed: {}".format(exc))

        try:
            choice = completion.choices[0]
            text = choice.message.content or ""
            finish_reason = getattr(choice, "finish_reason", None)
        except (AttributeError, IndexError, TypeError) as exc:
            raise LLMError("malformed completion payload: {}".format(exc))

        usage_obj = getattr(completion, "usage", None)
        usage = {
            "prompt_tokens": int(getattr(usage_obj, "prompt_tokens", 0) or 0),
            "completion_tokens": int(getattr(usage_obj, "completion_tokens", 0) or 0),
            "total_tokens": int(getattr(usage_obj, "total_tokens", 0) or 0),
        }
        return LLMResponse(
            text=text,
            usage=usage,
            model=getattr(completion, "model", self.deployment),
            latency_s=time.monotonic() - started,
            finish_reason=finish_reason,
        )


class MockLLMClient(BaseLLMClient):
    """Deterministic offline stub.

    For plumbing tests and dry runs only. Its "judgments" are hashes, not
    science: never report numbers produced with `llm.provider: mock`.
    """

    provider = "mock"

    def __init__(
        self,
        config: LLMConfig,
        *,
        event_log: Optional[EventLog] = None,
        responder: Optional[Callable[[List[Message], LLMConfig], str]] = None,
    ):
        super().__init__(config, event_log=event_log)
        self.responder = responder or default_mock_responder
        self.calls: List[List[Message]] = []

    def _invoke(self, messages: List[Message], *, json_mode: bool) -> LLMResponse:
        self.calls.append(messages)
        text = self.responder(messages, self.config)
        return LLMResponse(
            text=text,
            usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
            model="mock",
            latency_s=0.0,
            finish_reason="stop",
        )


_LABEL_RE = re.compile(r"^Hypothesis ([A-Z]+):", re.MULTILINE)


def default_mock_responder(messages: List[Message], config: LLMConfig) -> str:
    """Shape-correct, content-free replies keyed to the prompt text."""
    prompt = "\n".join(m.get("content", "") for m in messages)

    if "search queries" in prompt.lower() or "QUERIES" in prompt:
        seed = stable_hash(prompt, length=8)
        return json.dumps({"queries": ["mock query {} a".format(seed), "mock query {} b".format(seed)]})

    if "RETRIEVED LITERATURE" in prompt or "evidence_label" in prompt:
        has_papers = "[no eligible literature" not in prompt and "[1]" in prompt
        label = "weak_support" if has_papers else "no_evidence"
        score = 50 + (int(stable_hash(prompt, length=4), 16) % 21) if has_papers else 50
        return json.dumps(
            {
                "evidence_label": label,
                "score": score,
                "rationale": "mock assessment",
                "key_papers": [],
            }
        )

    labels = _LABEL_RE.findall(prompt)
    if labels:
        scores = []
        for label in labels:
            value = int(stable_hash(label + stable_hash(prompt, length=6), length=6), 16) % 101
            scores.append({"id": label, "score": value, "rationale": "mock score"})
        ranking = [s["id"] for s in sorted(scores, key=lambda s: -s["score"])]
        return json.dumps({"scores": scores, "ranking": ranking})

    return json.dumps({"result": "mock"})


def build_llm_client(config: LLMConfig, *, event_log: Optional[EventLog] = None) -> BaseLLMClient:
    if config.provider == "azure":
        return AzureOpenAIClient(config, event_log=event_log)
    if config.provider == "mock":
        return MockLLMClient(config, event_log=event_log)
    raise LLMError("unknown llm provider: {}".format(config.provider))
