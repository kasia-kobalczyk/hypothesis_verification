"""The one targeted experiment: can these candidate pairs yield OPPOSING predictions?

    python3 scripts/run_opposing_diagnostic.py

Same 10 development pairs, no retrieval. A narrowed generator proposes only
measurements on which it believes both claims make determinate, conflicting
predictions -- it may return zero -- and it does NOT assign direction labels.
The same two isolated predictors from Phase 2 then adjudicate every (test,
hypothesis) pair exactly as before.

Validated opposing test: both hypotheses receive an AGREED (A == B) definite label,
and the two labels differ. Silence cannot create one.

Interpretation, fixed before running:
  roughly 1-3 validated tests per pair -> Phase 1 was badly formulated; revise it
  essentially zero                     -> these candidate pairs do not make
                                          conflicting predictions; stop using them
                                          for this verifier
"""
from __future__ import annotations

import argparse, collections, json, random, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.benchmark.loader import load_pair_instances  # noqa: E402
from src.common.config import load_config  # noqa: E402
from src.common.errors import LLMError, LLMParseError  # noqa: E402
from src.common.io import stable_hash, utc_now_iso, write_json  # noqa: E402
from src.common.logging_utils import EventLog, configure_logging, get_logger  # noqa: E402
from src.llm.client import build_llm_client  # noqa: E402
from src.llm.prompts import PromptLibrary  # noqa: E402

LOGGER = get_logger("scripts.opposing")
GEN = "diagnostic_test_opposing_v1"
PREDICTORS = {"A": "diagnostic_predict_a_v1", "B": "diagnostic_predict_judge_b_v2"}
MAP = {"up_or_appears": "positive_or_present",
       "approximately_unchanged": "neutral_or_no_change",
       "down_or_absent": "negative_or_absent",
       "claim_does_not_determine": "indeterminate"}
DEF = {"positive_or_present", "neutral_or_
