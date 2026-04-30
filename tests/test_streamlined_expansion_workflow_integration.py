from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GOVERNANCE_DIR = ROOT / "data" / "expansion_governance"
TEMPLATE = GOVERNANCE_DIR / "templates" / "governed_expansion_items_template.tsv"
CHECKLIST = GOVERNANCE_DIR / "FUTURE_EXPANSION_CHECKLIST.md"
GUARDRAILS = GOVERNANCE_DIR / "CODEX_EXPANSION_PROMPT_GUARDRAILS.md"
README = GOVERNANCE_DIR / "README.md"
DOCS = ROOT / "docs" / "streamlined_expansion_governance.md"
WORKFLOW = ROOT / ".github" / "workflows" / "python-tests.yml"
VALIDATOR_PATH = ROOT / "scripts" / "validate_streamlined_expansion_governance.py"

SPEC = importlib.util.spec_from_file_location(
    "validate_streamlined_expansion_governance", VALIDATOR_PATH
)
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


def read_template_rows() -> list[dict[str, str]]:
    with TEMPLATE.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, row: dict[str, str]) -> Path:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row), delimiter="\t")
        writer.writeheader()
        writer.writerow(row)
    return path


def validate(path: Path):
    return validator.validate_paths(
        [path],
        contract=validator.load_contract(),
        explicit_path=False,
    )


def valid_governed_row() -> dict[str, str]:
    return {
        "governance_scope": "future_test_fixture",
        "packet_type": "word_bank_review",
        "sefer": "ExampleSefer",
        "perek": "0",
        "pasuk": "0",
        "hebrew_word": "example_word",
        "hebrew_phrase": "",
        "basic_gloss": "example gloss",
        "skill_category": "single_word_vocabulary",
        "source_evidence": "example_source_only",
        "review_status": "planning_only",
        "runtime_status": "planning_only",
        "planning_only": "true",
        "runtime_allowed": "false",
        "protected_preview_allowed": "false",
        "reviewed_bank_allowed": "false",
        "runtime_active": "false",
        "word_level_approved": "false",
        "teacher_approved": "false",
        "observed_internally": "false",
        "reviewed_bank_status": "not_reviewed_bank",
        "runtime_ready": "false",
        "skill_depth_stage": "single_word_vocabulary",
        "notes": "example only",
    }


def test_future_expansion_checklist_exists() -> None:
    assert CHECKLIST.exists()
    text = CHECKLIST.read_text(encoding="utf-8")
    assert "Horizontal expansion rule" in text
    assert "Vertical depth rule" in text
    assert "Planning-only is never runtime" in text


def test_codex_guardrail_template_exists() -> None:
    assert GUARDRAILS.exists()
    assert "Streamlined Expansion Governance guardrails" in GUARDRAILS.read_text(encoding="utf-8")


def test_governed_expansion_template_exists() -> None:
    assert TEMPLATE.exists()
    rows = read_template_rows()
    assert rows
    assert "governance_scope" in rows[0]
    assert "packet_type" in rows[0]


def test_governed_expansion_template_contains_planning_only_defaults() -> None:
    rows = read_template_rows()
    first = rows[0]
    assert first["review_status"] == "planning_only"
    assert first["runtime_status"] == "planning_only"
    assert first["planning_only"] == "true"
    assert first["runtime_allowed"] == "false"
    assert first["protected_preview_allowed"] == "false"
    assert first["reviewed_bank_allowed"] == "false"
    assert first["runtime_active"] == "false"
    assert "EXAMPLE ONLY" in first["notes"]


def test_guardrail_template_contains_no_runtime_activation_rule() -> None:
    text = GUARDRAILS.read_text(encoding="utf-8")
    assert "Do not activate planning-only content" in text
    assert "Do not change runtime behavior unless explicitly requested" in text


def test_docs_include_strict_validator_release_command() -> None:
    combined = README.read_text(encoding="utf-8") + "\n" + DOCS.read_text(encoding="utf-8")
    assert "python scripts/validate_streamlined_expansion_governance.py --strict" in combined


def test_ci_workflow_runs_streamlined_expansion_validator() -> None:
    assert WORKFLOW.exists()
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "python scripts/validate_streamlined_expansion_governance.py --strict" in text


def test_future_governed_tsv_with_template_fields_is_recognized(tmp_path: Path) -> None:
    path = write_tsv(tmp_path / "future_governed.tsv", valid_governed_row())
    result = validate(path)
    assert result.ok, [error.format() for error in result.errors]
    assert result.files_checked == 1
    assert result.items_checked == 1


def test_planning_only_governed_tsv_with_runtime_active_fails(tmp_path: Path) -> None:
    row = valid_governed_row()
    row["runtime_active"] = "true"
    path = write_tsv(tmp_path / "future_governed_bad.tsv", row)

    result = validate(path)

    assert not result.ok
    assert validator.ERROR_PLANNING_ONLY_ACTIVATION in {
        error.code for error in result.errors
    }
