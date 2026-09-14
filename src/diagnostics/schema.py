"""Diagnostic prediction tests: the unit of the new verifier.

A test is generated JOINTLY for all candidates and belongs to none of them. Every
hypothesis predicts the outcome of the same test before any literature is seen, so
an observation can only contribute by being predicted differently -- which removes
candidate-origin asymmetry structurally rather than by correction.

See docs/DIAGNOSTIC_DESIGN.md (frozen 49695b5b3440818c).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

# Coarse only. The previous branch measured weak_support reproducing at 0.51 and
# exact ordinal edge agreement at 0.370 for abstracted nodes; fine gradations were
# not reproducible there and are not assumed here.
PREDICTIONS = ("positive_or_present", "neutral_or_no_change",
               "negative_or_absent", "indeterminate")

COMPATIBILITY = ("match", "approximate_match", "indeterminate", "mismatch")

DISCRIMINATIVE_PREDICTIONS = ("positive_or_present", "neutral_or_no_change",
                              "negative_or_absent")


def normalise_prediction(value: Any) -> Optional[str]:
    key = str(value or "").strip().lower().replace(" ", "_").replace("-", "_")
    return key if key in PREDICTIONS else None


class DiagnosticTest(BaseModel):
    """One observable test, with a precommitted prediction per hypothesis."""

    model_config = ConfigDict(extra="forbid")

    test_id: str
    system: str
    context: str = ""
    intervention_or_exposure: str
    measured_outcome: str
    # T = (S, C, I, Y, B). "Higher expression" is meaningless without saying higher
    # than what, and an implicit comparator is a plausible source of sign
    # disagreements between independent predictors (AMENDMENT 1).
    baseline_or_comparator: str = ""
    rationale: str = ""
    # PROVISIONAL, for debugging only (AMENDMENT 2). The generator sees all
    # candidates at once and has an incentive to make its own test look
    # discriminative -- measured: it labelled "this candidate is silent" as
    # neutral_or_no_change in 24 of 31 cases. Discriminativeness is decided from
    # `adjudicated_predictions` instead, produced by an isolated predictor that
    # never sees the competing candidates.
    predictions_by_hypothesis: Dict[str, str] = Field(default_factory=dict)
    adjudicated_predictions: Dict[str, str] = Field(default_factory=dict)
    empirically_observable: bool = True
    rejected_reason: Optional[str] = None

    def _effective(self) -> Dict[str, str]:
        """Adjudicated predictions when available; generator ones only as a fallback.

        A test whose discriminativeness has not been adjudicated is not yet known to
        be diagnostic, and `usable()` reflects that.
        """
        return self.adjudicated_predictions or self.predictions_by_hypothesis

    def is_adjudicated(self) -> bool:
        return bool(self.adjudicated_predictions)

    def distinct_predictions(self) -> int:
        """How many DIFFERENT definite directions the candidates predict.

        `indeterminate` is excluded: a candidate that makes no prediction cannot be
        distinguished by the test, and counting it would make a test look
        discriminative for the wrong reason.
        """
        definite = {v for v in self._effective().values()
                    if v in DISCRIMINATIVE_PREDICTIONS}
        return len(definite)

    def is_discriminative(self) -> bool:
        """At least two candidates predict different definite outcomes."""
        return self.distinct_predictions() >= 2

    def discriminated_pairs(self) -> List[tuple]:
        """Which candidate pairs this test would separate, if observed."""
        preds = self._effective()
        ids = sorted(preds)
        out = []
        for i, a in enumerate(ids):
            for b in ids[i + 1:]:
                pa = preds[a]
                pb = preds[b]
                if (pa in DISCRIMINATIVE_PREDICTIONS
                        and pb in DISCRIMINATIVE_PREDICTIONS and pa != pb):
                    out.append((a, b))
        return out

    def record(self) -> Dict[str, Any]:
        return self.model_dump(mode="json")


class TestSet(BaseModel):
    """All diagnostic tests generated for one instance."""

    model_config = ConfigDict(extra="forbid")

    instance_id: str
    hypothesis_ids: List[str] = Field(default_factory=list)
    tests: List[DiagnosticTest] = Field(default_factory=list)
    generation_notes: List[str] = Field(default_factory=list)

    def usable(self) -> List[DiagnosticTest]:
        return [t for t in self.tests
                if t.empirically_observable and t.is_discriminative()]

    def stats(self) -> Dict[str, Any]:
        observable = [t for t in self.tests if t.empirically_observable]
        return {
            "n_generated": len(self.tests),
            "n_empirically_observable": len(observable),
            "n_discriminative": sum(1 for t in self.tests if t.is_discriminative()),
            "n_usable": len(self.usable()),
            "n_rejected": sum(1 for t in self.tests if t.rejected_reason),
            "mean_distinct_predictions": (
                sum(t.distinct_predictions() for t in self.tests) / len(self.tests)
                if self.tests else 0.0),
        }
