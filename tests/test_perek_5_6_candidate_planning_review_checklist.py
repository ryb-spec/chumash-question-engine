from __future__ import annotations

import json
from pathlib import Path

from scripts import validate_perek_5_6_candidate_planning_review_checklist as validator


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data" / "gate_2_source_discovery" / "reports"
CHECKLIST_MD = REPORT / "bereishis_perek_5_6_candidate_planning_review_checklist_2026_04_29.md"
CHECKLIST_JSON = REPORT / "bereishis_perek_5_6_candidate_planning_review_checklist_2026_04_29.json"
READINESS = ROOT / "data" / "pipeline_rounds" / "bereishis_perek_5_6_candidate_planning_review_checklist_readiness_2026_04_29.md"
FUTURE_PROMPT = ROOT / "data" / "pipeline_rounds" / "prompts" / "bereishis_perek_5_6_candidate_planning_decisions_apply_prompt.md"

ELIGIBLE_IDS = [
    "g2srcdisc_p5_001",
    "g2srcdisc_p5_002",
    "g2srcdisc_p5_005",
    "g2srcdisc_p6_001",
    "g2srcdisc_p6_003",
    "g2srcdisc_p6_006",
    "g2srcdisc_p6_007",
]
EXCLUDED_IDS = [
    "g2srcdisc_p5_003",
    "g2srcdisc_p5_004",
    "g2srcdisc_p6_002",
    "g2srcdisc_p6_004",
    "g2srcdisc_p6_005",
]


def load_checklist() -> dict:
    return json.loads(CHECKLIST_JSON.read_text(encoding="utf-8"))


def test_checklist_artifacts_exist():
    for path in [CHECKLIST_MD, CHECKLIST_JSON, READINESS, FUTURE_PROMPT]:
        assert path.exists(), path


def test_json_parses_with_expected_counts_and_ids():
    payload = load_checklist()
    assert payload["checklist_status"] == "candidate_planning_review_only"
    assert payload["eligible_candidate_count"] == 7
    assert payload["excluded_candidate_count"] == 5
    assert payload["eligible_candidate_ids"] == ELIGIBLE_IDS
    assert payload["excluded_candidate_ids"] == EXCLUDED_IDS
    assert [candidate["candidate_id"] for candidate in payload["candidates"]] == ELIGIBLE_IDS


def test_decisions_are_null_and_notes_blank():
    payload = load_checklist()
    for candidate in payload["candidates"]:
        assert candidate["planning_review_decision"] is None
        assert candidate["planning_review_notes"] == ""


def test_all_gates_false():
    payload = load_checklist()
    for candidate in payload["candidates"]:
        assert candidate["runtime_allowed"] is False
        assert candidate["reviewed_bank_allowed"] is False
        assert candidate["protected_preview_allowed"] is False
        assert candidate["student_facing_allowed"] is False
        assert candidate["perek_5_activated"] is False
        assert candidate["perek_6_activated"] is False


def test_future_apply_prompt_exists_and_is_guarded():
    prompt = FUTURE_PROMPT.read_text(encoding="utf-8")
    assert "Stop if any required planning decisions are missing." in prompt
    assert "Keep runtime, reviewed-bank, protected-preview, and student-facing permission fields false." in prompt


def test_validator_passes():
    result = validator.validate()
    assert result["valid"], result["errors"]
