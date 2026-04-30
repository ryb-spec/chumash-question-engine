from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
P4_TSV = ROOT / "data" / "vocabulary_bank" / "bereishis_perek_4_broad_safe_vocabulary_bank_2026_04_30.tsv"
P4_JSON = ROOT / "data" / "vocabulary_bank" / "bereishis_perek_4_broad_safe_vocabulary_bank_2026_04_30.json"
P56_TSV = ROOT / "data" / "vocabulary_bank" / "bereishis_perek_5_6_planning_only_vocabulary_inventory_2026_04_30.tsv"
P56_JSON = ROOT / "data" / "vocabulary_bank" / "bereishis_perek_5_6_planning_only_vocabulary_inventory_2026_04_30.json"
CONTRACT_JSON = ROOT / "data" / "pipeline_rounds" / "broad_safe_vocabulary_bank_v1_2026_04_30.json"


def _read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def test_perek_4_tsv_parses_with_required_columns():
    rows = _read_tsv(P4_TSV)
    assert len(rows) == 5
    required = {
        "vocabulary_id",
        "pasuk_ref",
        "hebrew_word",
        "english_gloss",
        "word_level_approved",
        "question_approval_status",
        "protected_preview_candidate_status",
        "reviewed_bank_status",
        "runtime_status",
        "safety_classification",
        "allowed_next_use",
    }
    assert required <= set(rows[0])


def test_perek_4_json_parses_and_matches_counts():
    payload = json.loads(P4_JSON.read_text(encoding="utf-8-sig"))
    assert payload["item_count"] == 5
    assert payload["counts_by_classification"] == {
        "protected_preview_ready": 2,
        "revision_needed": 2,
        "teacher_review_ready": 1,
    }


def test_word_level_approved_rows_do_not_become_question_approved():
    rows = _read_tsv(P4_TSV)
    approved = [row for row in rows if row["word_level_approved"] == "true"]
    assert len(approved) == 5
    assert {row["question_approval_status"] for row in approved} == {"not_question_approved"}
    assert {row["runtime_status"] for row in approved} == {"not_runtime"}


def test_revision_needed_rows_remain_blocked_from_protected_preview():
    rows = _read_tsv(P4_TSV)
    revision_rows = [row for row in rows if row["safety_classification"] == "revision_needed"]
    assert {row["hebrew_word"] for row in revision_rows} == {"אֲדָמָה", "מִנְחָה"}
    assert {row["protected_preview_candidate_status"] for row in revision_rows} == {
        "blocked_revision_needed"
    }


def test_runtime_and_reviewed_bank_approval_false_for_all_rows():
    rows = _read_tsv(P4_TSV) + _read_tsv(P56_TSV)
    assert rows
    assert {row["runtime_status"] for row in rows} == {"not_runtime"}
    assert {row["reviewed_bank_status"] for row in rows} == {"not_reviewed_bank"}
    assert {row["question_approval_status"] for row in rows} == {"not_question_approved"}


def test_perek_5_6_inventory_is_planning_only():
    rows = _read_tsv(P56_TSV)
    payload = json.loads(P56_JSON.read_text(encoding="utf-8-sig"))
    assert len(rows) == 12
    assert payload["planning_only"] is True
    assert {row["safety_classification"] for row in rows} == {"planning_only"}
    assert {row["word_level_approved"] for row in rows} == {"false"}


def test_contract_safety_flags_remain_closed():
    payload = json.loads(CONTRACT_JSON.read_text(encoding="utf-8-sig"))
    assert payload["word_level_approval_created"] is True
    assert payload["question_approval_created"] is False
    assert payload["reviewed_bank_promoted"] is False
    assert payload["runtime_scope_widened"] is False
    assert payload["perek_activated"] is False
    assert payload["runtime_activation_authorized"] is False
    assert payload["ready_for_runtime_activation"] is False


def test_no_fake_teacher_approval_language_appears():
    text = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in [P4_TSV, P4_JSON, P56_TSV, P56_JSON, CONTRACT_JSON]
    ).lower()
    assert "teacher approved" not in text
    assert "approved_for_runtime" not in text
    assert "runtime_allowed=true" not in text
    assert "raw jsonl" not in text


def test_validator_passes():
    result = subprocess.run(
        [sys.executable, "scripts/validate_broad_safe_vocabulary_bank.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr + result.stdout
    assert "Broad safe vocabulary bank validation passed." in result.stdout
