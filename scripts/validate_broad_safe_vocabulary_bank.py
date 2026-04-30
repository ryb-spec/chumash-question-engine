from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
P4_TSV = ROOT / "data" / "vocabulary_bank" / "bereishis_perek_4_broad_safe_vocabulary_bank_2026_04_30.tsv"
P4_JSON = ROOT / "data" / "vocabulary_bank" / "bereishis_perek_4_broad_safe_vocabulary_bank_2026_04_30.json"
P56_TSV = ROOT / "data" / "vocabulary_bank" / "bereishis_perek_5_6_planning_only_vocabulary_inventory_2026_04_30.tsv"
P56_JSON = ROOT / "data" / "vocabulary_bank" / "bereishis_perek_5_6_planning_only_vocabulary_inventory_2026_04_30.json"
REPORT_MD = ROOT / "data" / "pipeline_rounds" / "broad_safe_vocabulary_bank_v1_2026_04_30.md"
CONTRACT_JSON = ROOT / "data" / "pipeline_rounds" / "broad_safe_vocabulary_bank_v1_2026_04_30.json"

REQUIRED_COLUMNS = {
    "vocabulary_id",
    "sefer",
    "perek",
    "pasuk",
    "pasuk_ref",
    "hebrew_word",
    "normalized_hebrew",
    "display_hebrew",
    "english_gloss",
    "source_type",
    "source_artifacts",
    "appears_in_canonical_text",
    "source_verified",
    "word_level_approved",
    "word_level_approval_basis",
    "skill_category",
    "subskill",
    "suggested_question_lanes",
    "question_approval_status",
    "protected_preview_candidate_status",
    "reviewed_bank_status",
    "runtime_status",
    "teacher_review_status",
    "blocker_reason",
    "revision_note",
    "safety_classification",
    "allowed_next_use",
}


def _read_json(path: Path) -> dict:
    if not path.exists():
        raise AssertionError(f"missing JSON: {path}")
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise AssertionError(f"missing TSV: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        fieldnames = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - fieldnames
        if missing:
            raise AssertionError(f"{path} missing required columns: {sorted(missing)}")
        return list(reader)


def _assert_false_flags(payload: dict, fields: list[str]) -> None:
    for field in fields:
        if payload.get(field) is not False:
            raise AssertionError(f"{field} must be false")


def validate() -> None:
    p4_rows = _read_tsv(P4_TSV)
    p4_payload = _read_json(P4_JSON)
    p56_rows = _read_tsv(P56_TSV)
    p56_payload = _read_json(P56_JSON)
    contract = _read_json(CONTRACT_JSON)
    if not REPORT_MD.exists():
        raise AssertionError(f"missing report: {REPORT_MD}")

    if len(p4_rows) != 5:
        raise AssertionError("Perek 4 vocabulary bank must contain exactly 5 rows")
    if p4_payload.get("item_count") != 5:
        raise AssertionError("Perek 4 JSON item_count must be 5")
    if len(p56_rows) != 12:
        raise AssertionError("Perek 5/6 planning-only inventory must contain exactly 12 rows")
    if p56_payload.get("planning_only") is not True:
        raise AssertionError("Perek 5/6 JSON must be planning-only")

    for row in p4_rows + p56_rows:
        if row["runtime_status"] not in {"false", "blocked", "not_runtime"}:
            raise AssertionError(f"runtime status must remain closed for {row['vocabulary_id']}")
        if row["reviewed_bank_status"] != "not_reviewed_bank":
            raise AssertionError(f"reviewed-bank status must remain closed for {row['vocabulary_id']}")
        if row["question_approval_status"] != "not_question_approved":
            raise AssertionError(f"question approval must remain closed for {row['vocabulary_id']}")
        if "approved_for_runtime" in str(row).lower() or "runtime_allowed=true" in str(row).lower():
            raise AssertionError(f"runtime approval language found in {row['vocabulary_id']}")

    word_level_rows = [row for row in p4_rows if row["word_level_approved"] == "true"]
    if len(word_level_rows) != 5:
        raise AssertionError("all 5 Perek 4 rows should be word-level approved")
    for row in word_level_rows:
        if row["question_approval_status"] != "not_question_approved":
            raise AssertionError("word-level approval must not imply question approval")

    protected_ready = [row for row in p4_rows if row["safety_classification"] == "protected_preview_ready"]
    if {row["vocabulary_id"] for row in protected_ready} != {"bsvb_p4_001", "bsvb_p4_002"}:
        raise AssertionError("protected-preview-ready rows must be only the two build-gate items")

    revision_rows = [row for row in p4_rows if row["safety_classification"] == "revision_needed"]
    if {row["vocabulary_id"] for row in revision_rows} != {"bsvb_p4_003", "bsvb_p4_004"}:
        raise AssertionError("revision-needed rows must be the two revision-watch Perek 4 items")
    for row in revision_rows:
        if row["protected_preview_candidate_status"] != "blocked_revision_needed":
            raise AssertionError("revision-needed rows must remain blocked from protected preview")

    for row in p56_rows:
        if row["safety_classification"] != "planning_only":
            raise AssertionError("Perek 5/6 inventory must stay planning-only")
        if row["word_level_approved"] != "false":
            raise AssertionError("Perek 5/6 inventory must not create word-level approval")

    _assert_false_flags(
        contract,
        [
            "question_approval_created",
            "protected_preview_promotion_performed",
            "reviewed_bank_promoted",
            "runtime_scope_widened",
            "perek_activated",
            "runtime_content_promoted",
            "source_truth_changed",
            "fake_teacher_approval_created",
            "fake_student_data_created",
            "raw_logs_exposed",
            "runtime_activation_authorized",
        ],
    )
    if contract.get("word_level_approval_created") is not True:
        raise AssertionError("contract must create word-level approval")
    if contract.get("ready_for_simple_question_candidate_lane") is not True:
        raise AssertionError("contract must prepare the simple question-candidate lane")
    if contract.get("ready_for_runtime_activation") is not False:
        raise AssertionError("contract must not authorize runtime activation")

    forbidden_text = "\n".join(
        [
            P4_TSV.read_text(encoding="utf-8-sig"),
            P4_JSON.read_text(encoding="utf-8-sig"),
            P56_TSV.read_text(encoding="utf-8-sig"),
            P56_JSON.read_text(encoding="utf-8-sig"),
            REPORT_MD.read_text(encoding="utf-8-sig"),
            CONTRACT_JSON.read_text(encoding="utf-8-sig"),
        ]
    ).lower()
    forbidden_phrases = [
        "runtime_allowed=true",
        "approved_for_runtime",
        "promoted to reviewed bank",
        "teacher approved",
        "fake student data created: yes",
        '"fake_student_data_created": true',
        "raw jsonl",
    ]
    for phrase in forbidden_phrases:
        if phrase in forbidden_text:
            raise AssertionError(f"forbidden phrase found: {phrase}")

    print("Broad safe vocabulary bank validation passed.")


if __name__ == "__main__":
    try:
        validate()
    except Exception as exc:  # pragma: no cover
        print(f"Broad safe vocabulary bank validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
