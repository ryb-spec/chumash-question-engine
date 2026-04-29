from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DISCOVERY_DIR = ROOT / "data" / "gate_2_source_discovery"
REPORT_DIR = DISCOVERY_DIR / "reports"
INVENTORY = DISCOVERY_DIR / "bereishis_perek_5_6_review_only_safe_candidate_inventory.tsv"
SUMMARY = REPORT_DIR / "bereishis_perek_5_6_source_discovery_summary_2026_04_29.json"
PROMPT = ROOT / "data" / "pipeline_rounds" / "prompts" / "bereishis_perek_5_6_review_checklist_prompt.md"
VALIDATOR = ROOT / "scripts" / "validate_perek_5_6_source_discovery.py"

REQUIRED_ARTIFACTS = [
    REPORT_DIR / "bereishis_perek_5_6_source_discovery_report.md",
    INVENTORY,
    REPORT_DIR / "bereishis_perek_5_6_excluded_risk_lanes.md",
    REPORT_DIR / "bereishis_perek_5_6_duplicate_session_balance_warnings.md",
    REPORT_DIR / "bereishis_perek_5_6_source_discovery_status_index.md",
    SUMMARY,
    PROMPT,
    ROOT / "data" / "pipeline_rounds" / "bereishis_perek_5_6_source_discovery_gate_2026_04_29.md",
]


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_perek_5_6_source_discovery", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def read_rows():
    with INVENTORY.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def test_required_artifacts_exist():
    for path in REQUIRED_ARTIFACTS:
        assert path.exists(), path


def test_summary_json_parses_and_matches_inventory_count():
    rows = read_rows()
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert summary["candidate_count"] == len(rows)
    assert summary["perek_5_candidate_count"] == sum(1 for row in rows if row["perek"] == "5")
    assert summary["perek_6_candidate_count"] == sum(1 for row in rows if row["perek"] == "6")


def test_all_inventory_gates_false():
    false_columns = [
        "runtime_allowed",
        "reviewed_bank_allowed",
        "protected_preview_allowed",
        "student_facing_allowed",
        "perek_5_activated",
        "perek_6_activated",
    ]
    for row in read_rows():
        for column in false_columns:
            assert row[column] == "false"


def test_candidate_ids_are_perek_5_or_perek_6_only():
    rows = read_rows()
    assert rows
    for row in rows:
        assert row["perek"] in {"5", "6"}
        assert row["candidate_id"].startswith(("g2srcdisc_p5_", "g2srcdisc_p6_"))
        assert not row["candidate_id"].startswith("g2srcdisc_p7_")


def test_summary_safety_booleans_are_false():
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    for field in [
        "perek_5_activated",
        "perek_6_activated",
        "runtime_scope_widened",
        "reviewed_bank_promoted",
        "protected_preview_packet_created",
        "student_facing_created",
        "fake_teacher_decisions_created",
        "fake_student_observations_created",
        "source_truth_changed",
    ]:
        assert summary[field] is False


def test_next_review_checklist_prompt_exists_and_is_guarded():
    text = PROMPT.read_text(encoding="utf-8")
    assert "compressed teacher-review checklist only" in text
    assert "create a protected-preview packet" in text
    assert "create student-facing content" in text
    assert "Keep all candidates review-only and all gates false" in text


def test_validator_passes():
    module = load_validator()
    module.validate()
