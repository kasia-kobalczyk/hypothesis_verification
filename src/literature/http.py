"""Shared HTTP client: rate limiting, retries, and explicit failure typing.

IMPLEMENTATION_SPEC.md §29 requires rate limits and transient failures to be
handled explicitly. A failure that survives the retry budget is raised, never
turned into an empty result set: "the provider is down" and "the literature
contains nothing" must stay distinguishable downstream.
"""

from __future__ import annotations

import json
import random
import threading
import time
from typing import Any, Dict, Optional

import requests

from src.common.config import HTTPConfig
from src.common.errors import (
    MalformedResponseError,
    ProviderError,
    RateLimitError,
    TransientProviderError,
)
from src.common.logging_utils import NULL_EVENT_LOG, EventLog, get_logger

LOGGER = get_logger("http")

RETRYABLE_STATUS = frozenset({408, 409, 425, 429, 500, 502, 503, 504})


class HttpClient:
    """Thin `requests` wrapper with a minimum inter-request interval."""

    def __init__(
        self,
        *,
        provider: str,
        config: HTTPConfig,
        headers: Optional[Dict[str, str]] = None,
        event_log: Optional[EventLog] = None,
        session: Optional[requests.Session] = None,
        sleep: Any = time.sleep,
    ):
        self.provider = provider
        self.config = config
        self.headers = dict(headers or {})
        self.event_log = event_log or NULL_EVENT_LOG
        self.session = session or requests.Session()
        self._sleep = sleep
        self._lock = threading.Lock()
        self._last_request_at = 0.0

    # ------------------------------------------------------------------ #
    def _throttle(self) -> None:
        interval = self.config.min_request_interval_s
        if interval <= 0:
            return
        with self._lock:
            wait = interval - (time.monotonic() - self._last_request_at)
            if wait > 0:
                self._sleep(wait)
            self._last_request_at = time.monotonic()

    def _backoff(self, attempt: int, retry_after: Optional[float]) -> float:
        if retry_after is not None:
            return min(retry_after, self.config.backoff_max_s)
        base = self.config.backoff_base_s * (2 ** (attempt - 1))
        return min(base, self.config.backoff_max_s) * (0.5 + random.random() / 2.0)

    @staticmethod
    def _retry_after(response: requests.Response) -> Optional[float]:
        value = response.headers.get("Retry-After")
        if not value:
            return None
        try:
            return float(value)
        except ValueError:
            return None

    # ------------------------------------------------------------------ #
    def get_json(
        self,
        url: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        endpoint: Optional[str] = None,
    ) -> Dict[str, Any]:
        """GET returning parsed JSON, retrying transient failures.

        Raises:
            RateLimitError: the retry budget was exhausted on 429s.
            TransientProviderError: exhausted on 5xx/timeouts.
            ProviderError: non-retryable HTTP error.
            MalformedResponseError: body was not JSON.
        """
        endpoint = endpoint or url
        last_exc: Optional[Exception] = None
        for attempt in range(1, self.config.max_retries + 1):
            self._throttle()
            started = time.monotonic()
            try:
                response = self.session.get(
                    url,
                    params=params,
                    headers=self.headers,
                    timeout=self.config.timeout_s,
                )
            except requests.RequestException as exc:
                elapsed = time.monotonic() - started
                last_exc = TransientProviderError(
                    "{}: request failed: {}".format(self.provider, exc), provider=self.provider
                )
                self.event_log.api_call(
                    self.provider, endpoint, params=params, error=str(exc),
                    attempt=attempt, elapsed_s=round(elapsed, 3),
                )
                LOGGER.warning("%s %s attempt %d failed: %s", self.provider, endpoint, attempt, exc)
                if attempt < self.config.max_retries:
                    self._sleep(self._backoff(attempt, None))
                    continue
                raise last_exc

            elapsed = time.monotonic() - started
            status = response.status_code

            if status in RETRYABLE_STATUS:
                retry_after = self._retry_after(response)
                self.event_log.api_call(
                    self.provider, endpoint, params=params, status=status,
                    attempt=attempt, elapsed_s=round(elapsed, 3), error="retryable",
                )
                if status == 429:
                    last_exc = RateLimitError(
                        "{}: rate limited on {}".format(self.provider, endpoint),
                        provider=self.provider,
                        retry_after_s=retry_after,
                    )
                else:
                    last_exc = TransientProviderError(
                        "{}: HTTP {} on {}".format(self.provider, status, endpoint),
                        provider=self.provider,
                        status_code=status,
                    )
                if attempt < self.config.max_retries:
                    delay = self._backoff(attempt, retry_after)
                    LOGGER.warning(
                        "%s %s HTTP %d; retrying in %.1fs (attempt %d/%d)",
                        self.provider, endpoint, status, delay, attempt, self.config.max_retries,
                    )
                    self._sleep(delay)
                    continue
                raise last_exc

            if status >= 400:
                self.event_log.api_call(
                    self.provider, endpoint, params=params, status=status,
                    attempt=attempt, elapsed_s=round(elapsed, 3), error="http_error",
                )
                raise ProviderError(
                    "{}: HTTP {} on {}: {}".format(self.provider, status, endpoint, response.text[:300]),
                    provider=self.provider,
                    status_code=status,
                )

            try:
                payload = response.json()
            except (json.JSONDecodeError, ValueError) as exc:
                self.event_log.api_call(
                    self.provider, endpoint, params=params, status=status,
                    attempt=attempt, elapsed_s=round(elapsed, 3), error="malformed_json",
                )
                raise MalformedResponseError(
                    "{}: non-JSON response from {}: {}".format(self.provider, endpoint, exc),
                    provider=self.provider,
                    status_code=status,
                )

            if not isinstance(payload, dict):
                raise MalformedResponseError(
                    "{}: expected a JSON object from {}, got {}".format(
                        self.provider, endpoint, type(payload).__name__
                    ),
                    provider=self.provider,
                    status_code=status,
                )

            self.event_log.api_call(
                self.provider, endpoint, params=params, status=status,
                attempt=attempt, elapsed_s=round(elapsed, 3),
            )
            return payload

        raise last_exc or ProviderError("{}: request failed".format(self.provider), provider=self.provider)
