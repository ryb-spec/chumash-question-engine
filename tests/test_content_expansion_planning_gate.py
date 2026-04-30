from __future__ import annotations

import csv
import json
from pathlib import Path

from scripts import validate_content_expansion_planning_gate as validator
from scripts.build_content_expansion_inventory import build_inventory_rows, build_candidate_plan

ROOT = Path(__file__).resolve().parents[1]
PLANNING_JSON = ROOT / "data/pipeline_rounds/content_expansion_planning_gate_2026_04_30.json"
INVENTORY_TSV = ROOT / "data/content_expansion_planning/content_expansion_inventory_2026_04_30.tsv"
INVENTORY_JSON = ROOT / "data/content_expansion_planning/content_expansion_inventory_2026_04_30.json"
GAP_JSON = ROOT / "data/content_expansion_planning/content_expansion_gap_map_2026_04_30.json"
PLAN_JSON = ROOT / "data/content_expansion_planning/content_expansion_candidate_plan_2026_04_30.json"
NEXT_PROMPT = ROOT / "data/pipeline_rounds/next_codex_prompt_content_build_candidate_2026_04_30.md"


def test_planning_json_parses_and_safety_flags_are_closed():
    payload = json.loads(PLANNING_JSON.read_text(encoding="utf-8"))
    assert payload["planning_only"] is True
    for key in [
        "content_expansion_performed",
        "runtime_scope_widened",
        "perek_activated",
        "reviewed_bank_promoted",
        "runtime_content_promoted",
        "question_generation_changed",
        "question_selection_changed",
        "question_selection_weighting_changed",
        "scoring_mastery_changed",
        "source_truth_changed",
        "fake_teacher_approval_created",
        "fake_student_data_created",
        "raw_logs_exposed",
        "validators_weakened",
        "ready_for_runtime_activation",
        "runtime_activation_authorized",
    ]:
        assert payload[key] is False


def test_primary_recommended_candidate_exists():
    payload = json.loads(PLANNING_JSON.read_text(encoding="utf-8"))
    primary = payload["primary_recommended_candidate"]
    assert primary["candidate_id"] == "cepg_primary_bereishis_perek_4_limited_protected_preview_build"
    assert primary["future_branch_name"] == "feature/perek-4-limited-protected-preview-build-gate"
    assert primary["risk_level"] == "low_to_medium"


def test_inventory_file_exists_and_has_required_columns():
    with INVENTORY_TSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert rows
    for column in [
        "source_area",
        "source_file",
        "perek",
        "skill",
        "question_type",
        "runtime_status",
        "blocker_reason",
        "safe_next_use",
        "recommended_next_gate",
    ]:
        assert column in rows[0]


def test_inventory_json_has_fail_closed_classifications():
    payload = json.loads(INVENTORY_JSON.read_text(encoding="utf-8"))
    counts = payload["classification_counts"]
    assert counts["blocked"] >= 1
    assert counts["pending_teacher_review"] >= 1
    assert payload["content_expansion_performed"] is False


def test_gap_map_candidate_plan_and_next_prompt_exist():
    assert json.loads(GAP_JSON.read_text(encoding="utf-8"))["slice_summaries"]
    assert json.loads(PLAN_JSON.read_text(encoding="utf-8"))["primary_recommended_candidate"]
    assert NEXT_PROMPT.exists()
    assert "Do not widen runtime scope" in NEXT_PROMPT.read_text(encoding="utf-8")


def test_no_forbidden_activation_or_fake_approval_language():
    artifact_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [
            ROOT / "data/pipeline_rounds/content_expansion_planning_gate_2026_04_30.md",
            ROOT / "data/content_expansion_planning/content_expansion_gap_map_2026_04_30.md",
            ROOT / "data/content_expansion_planning/content_expansion_candidate_plan_2026_04_30.md",
            NEXT_PROMPT,
        ]
    )
    for phrase in [
        "activated runtime scope",
        "perek activated",
        "promoted to reviewed bank",
        "approved for runtime",
        "teacher approved",
        "mastery proven",
        "raw JSONL",
        "scope widened",
    ]:
        assert phrase not in artifact_text


def test_builder_functions_are_planning_only_and_repeatable():
    rows = build_inventory_rows()
    plan = build_candidate_plan()
    assert rows
    assert any(row["safe_next_use"] == "blocked" for row in rows)
    assert plan["ready_for_runtime_activation"] is False


def test_validator_passes():
    assert validator.validate() == []
