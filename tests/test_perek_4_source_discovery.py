from __future__ import annotations

import csv
from pathlib import Path

from scripts import validate_perek_4_source_discovery as validator


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "data/gate_2_source_discovery/bereishis_perek_4_review_only_safe_candidate_inventory.tsv"
SOURCE_REPORT = ROOT / "data/gate_2_source_discovery/reports/bereishis_perek_4_source_discovery_report.md"
DUPLICATE_REPORT = ROOT / "data/gate_2_source_discovery/reports/bereishis_perek_4_duplicate_session_balance_warnings.md"
EXCLUDED_REPORT = ROOT / "data/gate_2_source_discovery/reports/bereishis_perek_4_excluded_risk_lanes.md"
STATUS_INDEX = ROOT / "data/gate_2_source_discovery/reports/bereishis_perek_4_source_discovery_status_index.md"
NEXT_PROMPT = ROOT / "data/pipeline_rounds/prompts/bereishis_perek_4_review_checklist_prompt.md"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def test_source_discovery_report_exists_and_is_review_only():
    text = SOURCE_REPORT.read_text(encoding="utf-8")
    assert "Perek 4 source-to-skill discovery only" in text
    assert "review-only" in text
    assert "No runtime activation" in text
    assert "No reviewed-bank promotion" in text
    assert "No protected-preview packet creation" in text
    assert "No student-facing content" in text


def test_review_only_safe_candidate_inventory_exists_and_is_perek_4_only():
    rows = read_tsv(INVENTORY)
    assert len(rows) == 5
    assert {row["perek"] for row in rows} == {"4"}
    assert all(row["candidate_id"].startswith("g2srcdisc_p4_") for row in rows)
    assert {row["review_status"] for row in rows} == {"review_only"}
    assert {row["review_required"] for row in rows} == {"true"}


def test_all_inventory_gates_are_closed():
    rows = read_tsv(INVENTORY)
    for row in rows:
        assert row["runtime_allowed"] == "false"
        assert row["reviewed_bank_allowed"] == "false"
        assert row["protected_preview_allowed"] == "false"
        assert row["student_facing_allowed"] == "false"
        assert row["broader_use_allowed"] == "false"


def test_inventory_source_and_provenance_fields_are_present():
    rows = read_tsv(INVENTORY)
    for row in rows:
        assert row["source_artifact"]
        assert row["source_row_id"]
        assert row["provenance_status"]
        assert row["source_confidence"]
        assert row["hebrew_token"]
        assert row["hebrew_phrase"]
        assert (ROOT / row["source_artifact"]).exists()


def test_duplicate_session_balance_warning_report_exists_and_flags_candidates():
    text = DUPLICATE_REPORT.read_text(encoding="utf-8")
    warning_rows = read_tsv(
        ROOT / "data/gate_2_source_discovery/reports/bereishis_perek_4_duplicate_session_balance_warnings.tsv"
    )
    inventory_rows = read_tsv(INVENTORY)
    assert "duplicate עֵץ/session-balance" in text
    assert "No Perek 4 protected-preview packet was created" in text
    assert len(warning_rows) == 4
    assert sum(1 for row in inventory_rows if row["duplicate_token_warning"] == "true") == 2


def test_excluded_risk_lanes_report_exists():
    text = EXCLUDED_REPORT.read_text(encoding="utf-8")
    for lane in [
        "Translation/context",
        "Suffix/compound morphology",
        "Advanced verbs",
        "Vav hahipuch",
        "Rashi/commentary",
        "Higher-order comprehension",
    ]:
        assert lane in text
    assert "non-runtime" in text


def test_status_index_says_no_packet_or_activation():
    text = STATUS_INDEX.read_text(encoding="utf-8")
    assert "not a protected-preview packet" in text
    assert "No Perek 4 protected-preview packet exists" in text
    assert "No runtime activation" in text
    assert "No reviewed-bank promotion" in text
    assert "No student-facing content" in text
    assert "No Perek 5 expansion" in text


def test_no_perek_4_protected_preview_packet_exists():
    assert validator.perek4_packet_paths() == []


def test_next_review_checklist_prompt_exists_and_keeps_gates_closed():
    text = NEXT_PROMPT.read_text(encoding="utf-8")
    assert "teacher/source review checklist" in text
    assert "Do not create a Perek 4 protected-preview packet" in text
    assert "Do not activate runtime" in text
    assert "Do not promote anything to reviewed bank" in text
    assert "Do not create student-facing content" in text
    assert "runtime_allowed=false" in text
    assert "protected_preview_allowed=false" in text


def test_validator_passes():
    summary = validator.validate_perek_4_source_discovery()
    assert summary["valid"], summary["errors"]
    assert summary["candidate_count"] == 5
    assert summary["skill_family_counts"] == {"basic_noun_recognition": 5}
