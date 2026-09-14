"""Typed error hierarchy.

The distinctions here are scientific, not cosmetic. IMPLEMENTATION_SPEC.md §29
requires that an external failure is never silently converted into evidence:

    ProviderError      != "no relevant literature exists"
    CacheMissError     != "the search returned nothing"
    LLMParseError      != "the model abstained"

Every call site that catches one of these must record it as an error in the run
artifacts rather than mapping it onto an evidence label.
"""

from __future__ import annotations

from typing import Optional


class HypothesisVerificationError(Exception):
    """Base class for all project errors."""


# --------------------------------------------------------------------------- #
# Configuration / data layer
# --------------------------------------------------------------------------- #
class ConfigError(HypothesisVerificationError):
    """Malformed or missing configuration."""


class BenchmarkDataError(HypothesisVerificationError):
    """The benchmark slice could not be loaded or violates its own invariants."""


class GraphBudgetError(ConfigError):
    """The graph budget cannot expand every candidate hypothesis.

    Raised before any model call is made. Truncating depth 1 instead would leave
    some candidates with no propositions of their own, and they would then be
    ranked only through other candidates' consequences -- a deformed graph that
    looks like a result.
    """


class MissingCutoffError(HypothesisVerificationError):
    """A literature-dependent method was asked to run without a frozen cutoff."""


# --------------------------------------------------------------------------- #
# Literature providers
# --------------------------------------------------------------------------- #
class ProviderError(HypothesisVerificationError):
    """Any failure of an external literature/metadata provider."""

    def __init__(self, message: str, *, provider: str = "", status_code: Optional[int] = None):
        super().__init__(message)
        self.provider = provider
        self.status_code = status_code


class TransientProviderError(ProviderError):
    """Retryable failure (5xx, connection reset, timeout)."""


class RateLimitError(TransientProviderError):
    """HTTP 429 / provider-signalled throttling."""

    def __init__(self, message: str, *, provider: str = "", retry_after_s: Optional[float] = None):
        super().__init__(message, provider=provider, status_code=429)
        self.retry_after_s = retry_after_s


class MalformedResponseError(ProviderError):
    """The provider replied, but the payload did not match the expected shape."""


class CacheMissError(HypothesisVerificationError):
    """Offline mode was requested and the query is not in the cache.

    This is deliberately an error: an empty result set would be indistinguishable
    from "the literature contains nothing", which is a scientific claim.
    """


# --------------------------------------------------------------------------- #
# Temporal safety
# --------------------------------------------------------------------------- #
class TemporalLeakError(HypothesisVerificationError):
    """A post-cutoff record reached a surface that feeds the model.

    This is a hard failure by design. It is never caught and downgraded.
    """


# --------------------------------------------------------------------------- #
# Language model
# --------------------------------------------------------------------------- #
class LLMError(HypothesisVerificationError):
    """Language-model backend failure."""


class LLMParseError(LLMError):
    """The model replied but the reply could not be parsed into the expected schema."""

    def __init__(self, message: str, *, raw_text: str = ""):
        super().__init__(message)
        self.raw_text = raw_text


class BudgetExceededError(HypothesisVerificationError):
    """The project spend cap was already exceeded when a run tried to start."""


class BaselineIsolationError(HypothesisVerificationError):
    """A method touched a capability it is not allowed to use (e.g. direct judge
    reaching for the literature service)."""
