from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DISCOVERY_DIR = ROOT / "data" / "gate_2_source_discovery"
REPORT_DIR = DISCOVERY_DIR / "reports"
INVENTORY = DISCOVERY_DIR / "bereishis_perek_5_6_review_only_safe_candidate_inventory.tsv"
CHECKLIST_JSON = REPORT_DIR / "bereishis_perek_5_6_compressed_teacher_review_checklist_2026_04_29.json"
DECISION_TEMPLATE = DISCOVERY_DIR / "bereishis_perek_5_6_teacher_review_decision_template.tsv"
APPLY_PROMPT = ROOT / "data" / "pipeline_rounds" / "prompts" / "bereishis_perek_5_6_teacher_review_decisions_apply_prompt.md"
VALIDATOR = ROOT / "scripts" / "validate_perek_5_6_teacher_review_checklist.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_perek_5_6_teacher_review_checklist", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def read_tsv(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def test_checklist_artifacts_exist():
    paths = [
        REPORT_DIR / "bereishis_perek_5_6_compressed_teacher_review_checklist_2026_04_29.md",
        CHECKLIST_JSON,
        ROOT / "data" / "pipeline_rounds" / "bereishis_perek_5_6_teacher_review_checklist_readiness_2026_04_29.md",
        DECISION_TEMPLATE,
        APPLY_PROMPT,
    ]
    for path in paths:
        assert path.exists(), path


def test_json_parses_and_count_matches_source_inventory():
    inventory_rows = read_tsv(INVENTORY)
    checklist = json.loads(CHECKLIST_JSON.read_text(encoding="utf-8"))
    assert checklist["checklist_status"] == "teacher_review_only"
    assert checklist["total_candidate_count"] == len(inventory_rows)
    assert len(checklist["candidates"]) == len(inventory_rows)


def test_all_decisions_are_null_or_blank():
    checklist = json.loads(CHECKLIST_JSON.read_text(encoding="utf-8"))
    for candidate in checklist["candidates"]:
        assert candidate["teacher_review_needed"] is True
        assert candidate["teacher_decision"] is None
        assert candidate["teacher_notes"] == ""
    for row in read_tsv(DECISION_TEMPLATE):
        assert row["teacher_decision"] == ""


def test_all_gates_false():
    checklist = json.loads(CHECKLIST_JSON.read_text(encoding="utf-8"))
    for candidate in checklist["candidates"]:
        assert candidate["runtime_allowed"] is False
        assert candidate["reviewed_bank_allowed"] is False
        assert candidate["protected_preview_allowed"] is False
        assert candidate["student_facing_allowed"] is False
        assert candidate["perek_5_activated"] is False
        assert candidate["perek_6_activated"] is False


def test_future_apply_prompt_exists_and_is_guarded():
    text = APPLY_PROMPT.read_text(encoding="utf-8")
    assert "Stop if teacher decisions are missing." in text
    assert "Do not invent decisions" in text
    assert "protected_preview_allowed false" in text


def test_validator_passes():
    module = load_validator()
    module.validate()
