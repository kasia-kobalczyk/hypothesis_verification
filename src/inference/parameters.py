"""Centralised ordinal scales and their numeric mappings.

IMPLEMENTATION_SPEC.md §16, §20, §23: the ordinal->numeric mappings live in one
configuration file and are loaded here. No numeric mapping value may appear in
any other module, so that later validation-set calibration only has to replace
this table.

Two invariants are enforced at load time rather than trusted:

* `evidence_log_lr["no_evidence"] ~= 0` — missing evidence must not count
  against a hypothesis (§20, §35.5);
* the support scale is monotone — stronger labels map to larger values (§16).
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from src.common.config import load_yaml
from src.common.errors import ConfigError

# Ordinal implication scale (spec §15). Placeholder labels; may change.
EDGE_LABELS: List[str] = [
    "strongly_implied",
    "implied",
    "weakly_implied",
    "neutral",
    "unlikely",
    "strongly_contradicted",
]

# Ordinal evidence scale (spec §19). `mixed` and `no_evidence` are distinct.
EVIDENCE_LABELS: List[str] = [
    "strong_support",
    "support",
    "weak_support",
    "mixed",
    "weak_contradiction",
    "contradiction",
    "strong_contradiction",
    "no_evidence",
]

# Monotone chain used for the ordering check (excludes `no_evidence`, which is
# not a point on the support/contradiction continuum).
_EVIDENCE_CHAIN: List[str] = [
    "strong_support",
    "support",
    "weak_support",
    "mixed",
    "weak_contradiction",
    "contradiction",
    "strong_contradiction",
]

NO_EVIDENCE_TOLERANCE = 0.05


class OrdinalMappings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    version: str = "unversioned"
    edge_probabilities: Dict[str, float] = Field(default_factory=dict)
    evidence_log_lr: Dict[str, float] = Field(default_factory=dict)
    source_path: Optional[str] = None

    # -------------------------------------------------------------- #
    def evidence_value(self, label: str) -> float:
        canonical = normalise_evidence_label(label)
        if canonical is None:
            raise ConfigError("unknown evidence label: {!r}".format(label))
        return self.evidence_log_lr[canonical]

    def edge_value(self, label: str) -> float:
        canonical = normalise_edge_label(label)
        if canonical is None:
            raise ConfigError("unknown implication label: {!r}".format(label))
        return self.edge_probabilities[canonical]

    def record(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "source_path": self.source_path,
            "edge_probabilities": dict(self.edge_probabilities),
            "evidence_log_lr": dict(self.evidence_log_lr),
        }


def _normalise(label: Optional[str], allowed: Iterable[str]) -> Optional[str]:
    if label is None:
        return None
    key = str(label).strip().lower().replace(" ", "_").replace("-", "_")
    allowed_set = set(allowed)
    return key if key in allowed_set else None


def normalise_evidence_label(label: Optional[str]) -> Optional[str]:
    """Canonicalise a model-supplied evidence label, or `None` if unrecognised."""
    return _normalise(label, EVIDENCE_LABELS)


def normalise_edge_label(label: Optional[str]) -> Optional[str]:
    return _normalise(label, EDGE_LABELS)


def validate_mappings(mappings: OrdinalMappings) -> None:
    missing_edges = [label for label in EDGE_LABELS if label not in mappings.edge_probabilities]
    if missing_edges:
        raise ConfigError("edge_probabilities is missing labels: {}".format(missing_edges))
    missing_evidence = [label for label in EVIDENCE_LABELS if label not in mappings.evidence_log_lr]
    if missing_evidence:
        raise ConfigError("evidence_log_lr is missing labels: {}".format(missing_evidence))

    no_evidence = mappings.evidence_log_lr["no_evidence"]
    if abs(no_evidence) > NO_EVIDENCE_TOLERANCE:
        raise ConfigError(
            "evidence_log_lr['no_evidence'] is {}; missing evidence must not count for or "
            "against a hypothesis (|value| <= {})".format(no_evidence, NO_EVIDENCE_TOLERANCE)
        )

    values = [mappings.evidence_log_lr[label] for label in _EVIDENCE_CHAIN]
    for earlier, later, a, b in zip(_EVIDENCE_CHAIN, _EVIDENCE_CHAIN[1:], values, values[1:]):
        if a < b:
            raise ConfigError(
                "evidence_log_lr is not monotone: {} ({}) < {} ({})".format(earlier, a, later, b)
            )

    edge_values = [mappings.edge_probabilities[label] for label in EDGE_LABELS]
    for earlier, later, a, b in zip(EDGE_LABELS, EDGE_LABELS[1:], edge_values, edge_values[1:]):
        if a < b:
            raise ConfigError(
                "edge_probabilities is not monotone: {} ({}) < {} ({})".format(earlier, a, later, b)
            )
    for label, value in mappings.edge_probabilities.items():
        if not 0.0 <= value <= 1.0:
            raise ConfigError("edge_probabilities[{!r}] = {} is not a probability".format(label, value))


def load_ordinal_mappings(path: str) -> OrdinalMappings:
    data = load_yaml(path)
    data.setdefault("source_path", str(path))
    try:
        mappings = OrdinalMappings(**data)
    except Exception as exc:
        raise ConfigError("invalid ordinal mappings in {}: {}".format(path, exc))
    validate_mappings(mappings)
    return mappings


def fit_calibration(validation_runs: Any, *, mappings: Optional[OrdinalMappings] = None) -> OrdinalMappings:
    """Fit the global ordinal mappings on a validation set (paper §5.5).

    Deliberately unimplemented: IMPLEMENTATION_SPEC.md §23 forbids calibrating
    the verifier in the first MVP. The interface exists so that later work only
    has to fill in this function — all mapping consumers already read from a
    single `OrdinalMappings` object.
    """
    raise NotImplementedError(
        "calibration is deferred (IMPLEMENTATION_SPEC.md §23); do not calibrate on the "
        "20-case development slice"
    )
