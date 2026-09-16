"""Hidden annotations must not be able to reach verifier context.

BENCH-GRAPH-PILOT-001 splits each case into a verifier-visible record and a hidden
annotation holding the resolving study, the resolution label and the reference
discriminators. The split is only worth something if it is enforced, so this module
attacks it from four directions:

1. the visible dataset file does not contain hidden content (textual);
2. the loader structurally refuses any non-visible field (projection);
3. a loaded instance, serialised whole, contains no hidden content (object graph);
4. the rendered prompts contain no hidden content (the thing that actually matters).

(3) and (4) are the ones with teeth: they scan for distinctive tokens taken from the
hidden file itself, so they keep working if the schema changes.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Set

import pytest

from src.benchmark.loader import (
    VISIBLE_CASE_FIELDS,
    VISIBLE_HYPOTHESIS_FIELDS,
    load_case_instances,
    project_visible_case,
)
from src.common.config import AppConfig
from src.common.errors import BenchmarkDataError

ROOT = Path(__file__).resolve().parents[1]

# The prompts the frozen pilot method (narrow_graph_v3_complete) actually sends.
# Scanning every template in the directory would test prompts the pilot never uses.
PILOT_PROMPTS = [
    "consequence_generate_v3",
    "evidence_assess_v2",
    "proposition_query_v1",
    "edge_assess_v1",
]
VISIBLE_PATH = ROOT / "benchmark" / "explanatory" / "cases_visible.jsonl"
HIDDEN_PATH = ROOT / "benchmark" / "explanatory" / "cases_hidden.json"

# Tokens shorter than this are too common to be evidence of a leak ("the", "gene",
# "PFC"). The scan uses distinctive multi-character tokens only, and even then the
# stoplist below removes the ones that legitimately appear on both sides.
MIN_TOKEN_LEN = 8

# Words that appear in hidden annotations AND may legitimately appear in a visible
# hypothesis, because both describe the same science. A leak test that flagged these
# would be measuring vocabulary overlap, not leakage.
SHARED_VOCABULARY_STOPLIST = {
    "hypothesis", "hypotheses", "mechanism", "mechanisms", "prediction",
    "predictions", "consequence", "consequences", "evidence", "observation",
    "observations", "experiment", "experimental", "measurement", "measurements",
    "different", "difference", "differences", "differential", "distinguish",
    "condition", "conditions", "conditional", "structure", "structural",
    "function", "functional", "functionally", "population", "populations",
    "selection", "selective", "correlation", "correlated", "correlational",
    "transcription", "transcriptional", "conformational", "developmental",
    "independent", "independently", "intermediate", "interhemispheric",
    "fragmentation", "productivity", "constraint", "constraints", "degradation",
    "resolution", "resolved", "unresolved", "alternative", "alternatives",
    "explanation", "explanations", "explanatory", "phenomenon", "component",
    "components", "regime", "regimes", "ancestral", "convergent", "origins",
    "lateralized", "specialized", "redundant", "reference", "references",
    "relationship", "relationships", "associated", "association", "activity",
    "increased", "decreased", "reduction", "distribution", "significant",
    "significantly", "consistent", "inconsistent", "variation", "variability",
}


def _tokens(text: str) -> Set[str]:
    return {
        tok.lower()
        for tok in re.findall(r"[A-Za-z][A-Za-z0-9\-]{%d,}" % (MIN_TOKEN_LEN - 1), text)
    }


def _walk_strings(node: object) -> List[str]:
    """Every string anywhere in a nested JSON-like structure, keys included."""
    out: List[str] = []
    if isinstance(node, str):
        out.append(node)
    elif isinstance(node, dict):
        for key, value in node.items():
            out.append(str(key))
            out.extend(_walk_strings(value))
    elif isinstance(node, (list, tuple)):
        for item in node:
            out.extend(_walk_strings(item))
    return out


@pytest.fixture(scope="module")
def hidden() -> Dict[str, dict]:
    data = json.loads(HIDDEN_PATH.read_text(encoding="utf-8"))
    return data["cases"]


@pytest.fixture(scope="module")
def visible_rows() -> List[dict]:
    rows = []
    for line in VISIBLE_PATH.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


@pytest.fixture(scope="module")
def instances():
    return load_case_instances(AppConfig(), dataset_path=VISIBLE_PATH)


def _hidden_identifiers(case: dict) -> Set[str]:
    """Identifiers that would be unambiguous proof of a leak: DOIs, URLs, accessions.

    These need no length or vocabulary filtering -- a DOI cannot appear in a visible
    hypothesis by coincidence.
    """
    ids: Set[str] = set()
    for text in _walk_strings(case):
        ids.update(m.lower() for m in re.findall(r"10\.\d{4,9}/[^\s\"'),;]+", text))
        ids.update(m.lower() for m in re.findall(r"https?://[^\s\"'),;]+", text))
        ids.update(m.lower() for m in re.findall(r"\barXiv:[\w./-]+", text))
    return ids


def _resolver_identity_strings(case: dict) -> List[str]:
    """The strings that identify the resolving study: authors, DOIs, dates.

    Two kinds of string are deliberately excluded, because including them would make
    the test fire on vocabulary rather than on leakage -- and a test that cries wolf
    gets muted:

    * `venue`: journal names are built from subject words ("Journal of Neuroscience",
      "Nature Ecology & Evolution") and those same words legitimately describe the
      case's own discipline;
    * `note` / `channel`: curator prose about the publication trail ("no preprint
      located"), whose vocabulary is about publishing, not about this case.

    What remains is the identifying content: author surnames, DOIs and dates. DOIs
    are additionally checked by `_hidden_identifiers` with no filtering at all.
    """
    identifying = ("authors", "doi", "date", "title")
    out: List[str] = []
    for entry in (case.get("resolver") or {}).values():
        if isinstance(entry, dict):
            out.extend(str(v) for k, v in entry.items() if k in identifying)
    return out


def _hidden_distinctive_tokens(case: dict) -> Set[str]:
    toks = set()
    for text in _walk_strings(case):
        toks |= _tokens(text)
    return toks - SHARED_VOCABULARY_STOPLIST


# --------------------------------------------------------------------------- #
# 1. The two files exist and are actually disjoint documents
# --------------------------------------------------------------------------- #
def test_visible_and_hidden_are_separate_files():
    assert VISIBLE_PATH.exists() and HIDDEN_PATH.exists()
    assert VISIBLE_PATH != HIDDEN_PATH


def test_every_visible_case_has_a_hidden_record_and_vice_versa(visible_rows, hidden):
    assert {row["case_id"] for row in visible_rows} == set(hidden)


def test_hidden_file_is_never_opened_by_the_loader():
    """Grep-level check: the loading path must not name the hidden file at all."""
    source = (ROOT / "src" / "benchmark" / "loader.py").read_text(encoding="utf-8")
    body = source[source.index("def load_case_instances") :]
    assert "cases_hidden" not in body
    for module in ("src/experiments/runner.py", "src/methods/consequence_graph.py"):
        text = (ROOT / module).read_text(encoding="utf-8")
        assert "cases_hidden" not in text, module


# --------------------------------------------------------------------------- #
# 2. The projection refuses non-visible fields (fails closed)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "field",
    ["resolution", "resolver", "resolving_observations", "reference_discriminators",
     "source_anchors", "leakage_audit", "gold", "answer"],
)
def test_projection_refuses_hidden_field(field):
    row = {
        "case_id": "CASE-X", "domain": "d", "phenomenon": "p", "cutoff": "2024-01-01",
        "hypotheses": [{"hypothesis_id": "H1", "text": "a"},
                       {"hypothesis_id": "H2", "text": "b"}],
        field: "SECRET",
    }
    with pytest.raises(BenchmarkDataError) as exc:
        project_visible_case(row, where="test")
    assert field in str(exc.value)


def test_projection_refuses_hidden_field_on_a_hypothesis():
    row = {
        "case_id": "CASE-X", "domain": "d", "phenomenon": "p", "cutoff": "2024-01-01",
        "hypotheses": [{"hypothesis_id": "H1", "text": "a", "is_favored": True},
                       {"hypothesis_id": "H2", "text": "b"}],
    }
    with pytest.raises(BenchmarkDataError) as exc:
        project_visible_case(row, where="test")
    assert "is_favored" in str(exc.value)


def test_projection_output_carries_only_visible_keys(visible_rows):
    for row in visible_rows:
        out = project_visible_case(row, where="test")
        assert set(out) <= VISIBLE_CASE_FIELDS
        for hyp in out["hypotheses"]:
            assert set(hyp) <= VISIBLE_HYPOTHESIS_FIELDS


def test_loader_rejects_a_dataset_with_a_hidden_field(tmp_path, visible_rows):
    """End to end: a poisoned dataset must fail the run, not taint it."""
    poisoned = dict(visible_rows[0])
    poisoned["resolution"] = {"type": "favored", "summary": "H1 wins"}
    path = tmp_path / "poisoned.jsonl"
    path.write_text(json.dumps(poisoned) + "\n", encoding="utf-8")
    with pytest.raises(BenchmarkDataError):
        load_case_instances(AppConfig(), dataset_path=path)


# --------------------------------------------------------------------------- #
# 3. No hidden content survives into the loaded object graph
# --------------------------------------------------------------------------- #
def test_visible_file_contains_no_hidden_identifiers(visible_rows, hidden):
    visible_text = VISIBLE_PATH.read_text(encoding="utf-8").lower()
    for case_id, case in hidden.items():
        for ident in _hidden_identifiers(case):
            assert ident not in visible_text, "{}: {} leaked into visible file".format(
                case_id, ident)


def test_loaded_instance_contains_no_hidden_identifiers(instances, hidden):
    for instance in instances:
        blob = json.dumps(
            instance.model_dump(mode="json"), default=str, ensure_ascii=False
        ).lower()
        for ident in _hidden_identifiers(hidden[instance.id]):
            assert ident not in blob, "{}: {} reached the instance".format(
                instance.id, ident)


def test_loaded_instance_contains_no_resolution_label(instances, hidden):
    """The label itself ("favored", "mixed", ...) must not be recoverable."""
    for instance in instances:
        blob = json.dumps(
            instance.model_dump(mode="json"), default=str, ensure_ascii=False
        ).lower()
        resolution = hidden[instance.id].get("resolution") or {}
        summary = (resolution.get("summary") or "").lower()
        assert summary not in blob or not summary
        # and no hypothesis is marked as the answer
        assert not any(h.gold for h in instance.hypotheses)
        assert not instance.has_gold


def test_resolver_title_tokens_do_not_reach_the_instance(instances, hidden):
    """Distinctive words from the resolving study's title/summary, minus vocabulary
    the two sides legitimately share."""
    for instance in instances:
        blob = json.dumps(
            instance.model_dump(mode="json"), default=str, ensure_ascii=False
        ).lower()
        visible_tokens = _tokens(blob)
        resolver_tokens = _tokens(" ".join(_resolver_identity_strings(hidden[instance.id])))
        leaked = (resolver_tokens & visible_tokens) - SHARED_VOCABULARY_STOPLIST
        # Author surnames and journal names are the realistic leak here.
        assert not leaked, "{}: resolver tokens in instance: {}".format(
            instance.id, sorted(leaked))


# --------------------------------------------------------------------------- #
# 4. No hidden content reaches a rendered prompt
# --------------------------------------------------------------------------- #
def _render_pilot_prompts(instance) -> str:
    """Render the prompts the pilot method will actually send, with real values.

    This is the test that matters. Everything upstream is about the dataset; this is
    about the bytes that reach the model. The prompts are rendered with the same
    presentation object the runner builds, and every declared placeholder is filled
    with either the real value or a marker, so a template that silently pulled case
    content from somewhere else would show up here.
    """
    from src.benchmark.presentation import build_presentation
    from src.common.config import AppConfig as _Cfg
    from src.llm.prompts import PromptLibrary

    config = _Cfg()
    presentation = build_presentation(instance, config.run)
    library = PromptLibrary(config.prompts.dir)

    values = {
        "question": instance.question,
        "phenomenon": instance.question,
        "hypotheses": presentation.render(),
        "hypothesis": presentation.items[0].text,
        "alternatives": presentation.render(),
        "cutoff": instance.cutoff_date.isoformat(),
        "cutoff_date": instance.cutoff_date.isoformat(),
        "discipline": instance.discipline or "",
    }

    chunks = [presentation.render(), json.dumps(presentation.to_record(), default=str)]
    for name in (PILOT_PROMPTS):
        template = library.get(name)
        filled = {slot: values.get(slot, "<{}>".format(slot))
                  for slot in template.placeholders}
        chunks.append(template.render(**filled))
    return "\n".join(chunks).lower()


def test_pilot_prompt_templates_declare_no_hidden_slot():
    """No prompt the pilot uses may declare a placeholder for a hidden annotation.

    Structural rather than textual: a template that does not declare the slot cannot
    be handed the value, whatever its prose says.
    """
    from src.common.config import AppConfig as _Cfg
    from src.llm.prompts import PromptLibrary

    library = PromptLibrary(_Cfg().prompts.dir)
    forbidden = {"resolution", "resolver", "resolving_observations", "resolution_type",
                 "reference_discriminators", "leakage_audit", "gold", "gold_hypothesis",
                 "answer", "correct_hypothesis", "favored"}
    for name in PILOT_PROMPTS:
        declared = {slot.lower() for slot in library.get(name).placeholders}
        overlap = declared & forbidden
        assert not overlap, "{}: declares hidden slot(s) {}".format(name, sorted(overlap))


def test_rendered_pilot_prompts_contain_no_hidden_identifiers(instances, hidden):
    for instance in instances:
        rendered = _render_pilot_prompts(instance)
        for ident in _hidden_identifiers(hidden[instance.id]):
            assert ident not in rendered, "{}: {} reached a prompt".format(
                instance.id, ident)


def test_rendered_pilot_prompts_contain_no_resolver_tokens(instances, hidden):
    for instance in instances:
        rendered_tokens = _tokens(_render_pilot_prompts(instance))
        resolver_tokens = _tokens(" ".join(_resolver_identity_strings(hidden[instance.id])))
        leaked = (resolver_tokens & rendered_tokens) - SHARED_VOCABULARY_STOPLIST
        assert not leaked, "{}: resolver tokens in prompt: {}".format(
            instance.id, sorted(leaked))


def test_rendered_pilot_prompts_contain_no_reference_discriminators(instances, hidden):
    """The reference discriminators are the graded answer key for consequence
    recovery. If one appeared in a prompt, the recovery analysis would measure
    transcription rather than discovery."""
    for instance in instances:
        rendered = _render_pilot_prompts(instance)
        for disc in hidden[instance.id].get("reference_discriminators") or []:
            assert disc.lower() not in rendered, (
                "{}: discriminator reached the prompt: {}".format(instance.id, disc))
            # also catch a paraphrase-free partial paste: any 8-word window
            words = disc.lower().split()
            for start in range(0, max(1, len(words) - 7)):
                window = " ".join(words[start:start + 8])
                assert window not in rendered, (
                    "{}: discriminator fragment reached the prompt: {!r}".format(
                        instance.id, window))


def test_rendered_pilot_prompts_contain_no_resolving_observations(instances, hidden):
    """Resolving observations are post-cutoff findings. Their presence in a prompt
    would be both an answer leak and a temporal leak."""
    for instance in instances:
        rendered = _render_pilot_prompts(instance)
        for obs in hidden[instance.id].get("resolving_observations") or []:
            words = obs.lower().split()
            for start in range(0, max(1, len(words) - 7)):
                window = " ".join(words[start:start + 8])
                assert window not in rendered, (
                    "{}: resolving observation reached the prompt".format(instance.id))


def test_rendered_pilot_prompts_contain_no_resolution_summary(instances, hidden):
    for instance in instances:
        rendered = _render_pilot_prompts(instance)
        summary = ((hidden[instance.id].get("resolution") or {}).get("summary") or "")
        if summary:
            assert summary.lower() not in rendered


# --------------------------------------------------------------------------- #
# 5. Audit prompts are physically outside the verifier's reach
# --------------------------------------------------------------------------- #
# The post-hoc analysis prompts are allowed to state the cutoff date and to show
# hidden annotations. Verifier prompts are forbidden both. Rather than exempt them
# from the invariants, they live in a directory the verifier's PromptLibrary is
# never pointed at -- so the separation survives someone forgetting about it.
AUDIT_DIR = ROOT / "src" / "llm" / "prompts_audit"


def test_audit_prompts_are_not_in_the_verifier_prompt_directory():
    from src.common.config import AppConfig as _Cfg

    verifier_dir = (ROOT / _Cfg().prompts.dir).resolve()
    assert AUDIT_DIR.resolve() != verifier_dir
    verifier_names = {p.stem for p in verifier_dir.glob("*.txt")}
    audit_names = {p.stem for p in AUDIT_DIR.glob("*.txt")}
    assert audit_names, "audit prompts missing"
    assert not (audit_names & verifier_names), (
        "audit prompt(s) {} also exist in the verifier prompt directory".format(
            sorted(audit_names & verifier_names)))


def test_no_verifier_code_path_loads_the_audit_prompts():
    """`src/` is the verifier. Only `scripts/` may name the audit directory."""
    offenders = []
    for path in (ROOT / "src").rglob("*.py"):
        if "prompts_audit" in path.read_text(encoding="utf-8"):
            offenders.append(str(path.relative_to(ROOT)))
    assert not offenders, "verifier code references the audit prompts: {}".format(offenders)


def test_audit_prompts_may_state_the_cutoff_but_verifier_prompts_may_not():
    """Documents the asymmetry, and fails if the audit prompts are ever moved back
    under the verifier directory where the invariant would then flag them."""
    from src.common.config import AppConfig as _Cfg
    from src.llm.prompts import PromptLibrary

    verifier = PromptLibrary((ROOT / _Cfg().prompts.dir))
    for name in verifier.available():
        assert "cutoff" not in verifier.get(name).text.lower(), name

    audit = PromptLibrary(AUDIT_DIR)
    assert any("cutoff" in audit.get(n).text.lower() for n in audit.available()), (
        "no audit prompt states the cutoff; if that is now intentional, delete this "
        "test rather than leaving it asserting something untrue")
