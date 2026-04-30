from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
PACKET_DIR = ROOT / "data/gate_2_protected_preview_packets"
REPORTS = PACKET_DIR / "reports"
PACKET_TSV = PACKET_DIR / "bereishis_perek_5_6_small_internal_protected_preview_packet.tsv"
PACKET_MD = REPORTS / "bereishis_perek_5_6_small_internal_protected_preview_packet_2026_04_29.md"
PACKET_JSON = REPORTS / "bereishis_perek_5_6_small_internal_protected_preview_packet_2026_04_29.json"
GENERATION_REPORT = REPORTS / "bereishis_perek_5_6_small_internal_protected_preview_packet_generation_report_2026_04_29.md"
REVIEW_CHECKLIST = REPORTS / "bereishis_perek_5_6_small_internal_protected_preview_review_checklist_2026_04_29.md"
EXCLUDED_REGISTER = REPORTS / "bereishis_perek_5_6_small_packet_excluded_revision_register_2026_04_29.md"
PIPELINE_STATUS = ROOT / "data/pipeline_rounds/bereishis_perek_5_6_small_internal_packet_created_2026_04_29.md"

REQUIRED_FILES = (
    PACKET_TSV,
    PACKET_MD,
    PACKET_JSON,
    GENERATION_REPORT,
    REVIEW_CHECKLIST,
    EXCLUDED_REGISTER,
    PIPELINE_STATUS,
)
EXPECTED_INCLUDED_IDS = ["g2srcdisc_p5_001", "g2srcdisc_p5_005"]
EXPECTED_EXCLUDED_IDS = [
    "g2srcdisc_p5_002",
    "g2srcdisc_p5_003",
    "g2srcdisc_p5_004",
    "g2srcdisc_p6_001",
    "g2srcdisc_p6_002",
    "g2srcdisc_p6_003",
    "g2srcdisc_p6_004",
    "g2srcdisc_p6_005",
    "g2srcdisc_p6_006",
    "g2srcdisc_p6_007",
]
FALSE_FIELDS = ("runtime_allowed", "reviewed_bank_allowed", "student_facing_allowed", "perek_5_activated", "perek_6_activated")
REQUIRED_TSV_COLUMNS = [
    "packet_item_id",
    "source_candidate_id",
    "perek",
    "pasuk_ref",
    "hebrew_target",
    "proposed_question",
    "expected_answer",
    "distractors",
    "proposed_skill",
    "canonical_skill_id",
    "prior_review_decision",
    "readiness_reason",
    "spacing_or_balance_note",
    "runtime_allowed",
    "reviewed_bank_allowed",
    "student_facing_allowed",
    "perek_5_activated",
    "perek_6_activated",
]
FORBIDDEN_PATTERNS = (
    "runtime_allowed=true",
    "runtime_allowed: true",
    '"runtime_allowed": true',
    "reviewed_bank_allowed=true",
    "reviewed_bank_allowed: true",
    '"reviewed_bank_allowed": true',
    "student_facing_allowed=true",
    "student_facing_allowed: true",
    '"student_facing_allowed": true',
    "promoted_to_runtime",
    "approved_for_runtime",
    "Perek 5 is active runtime",
    "Perek 6 is active runtime",
    "Perek 5 runtime is active",
    "Perek 6 runtime is active",
    "reviewed-bank promotion occurred",
    "public launch",
    "fake observation result",
    "fake student data",
)


def _relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def _read_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def _load_json(path: Path, errors: list[str]) -> dict:
    try:
        payload = json.loads(_read_text(path))
    except json.JSONDecodeError as exc:
        errors.append(f"{_relative(path)} is invalid JSON: {exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"{_relative(path)} must be a JSON object")
        return {}
    return payload


def _require_false(payload: dict, key: str, errors: list[str], context: str) -> None:
    if payload.get(key) is not False:
        errors.append(f"{context}: {key} must be false")


def _validate_tsv(errors: list[str]) -> list[str]:
    fields, rows = _read_tsv(PACKET_TSV)
    if fields != REQUIRED_TSV_COLUMNS:
        errors.append("packet TSV columns do not match required Perek 5-6 small packet schema")
    if len(rows) != 2:
        errors.append(f"packet TSV must have exactly 2 rows, found {len(rows)}")
    ids = [row.get("source_candidate_id", "") for row in rows]
    if ids != EXPECTED_INCLUDED_IDS:
        errors.append(f"packet TSV source IDs must be exactly {EXPECTED_INCLUDED_IDS}")
    for excluded_id in EXPECTED_EXCLUDED_IDS:
        if excluded_id in ids:
            errors.append(f"{excluded_id} must not appear in packet TSV")
    for row in rows:
        context = row.get("packet_item_id", "packet row")
        if row.get("prior_review_decision") != "approve_for_internal_protected_preview_packet":
            errors.append(f"{context}: prior_review_decision must be approve_for_internal_protected_preview_packet")
        for field in FALSE_FIELDS:
            if row.get(field) != "false":
                errors.append(f"{context}: {field} must be false")
        for field in ("hebrew_target", "proposed_question", "expected_answer", "distractors", "readiness_reason"):
            if not row.get(field):
                errors.append(f"{context}: {field} must be populated")
        if row.get("expected_answer") != "noun":
            errors.append(f"{context}: expected_answer must be noun")
    return ids


def _validate_json(payload: dict, errors: list[str]) -> list[str]:
    if payload.get("packet_status") != "small_internal_protected_preview_only":
        errors.append("packet_status must be small_internal_protected_preview_only")
    if payload.get("scope") != "Bereishis Perek 5-6":
        errors.append("scope must be Bereishis Perek 5-6")
    if payload.get("item_count") != 2:
        errors.append("item_count must be 2")
    if payload.get("included_candidate_ids") != EXPECTED_INCLUDED_IDS:
        errors.append(f"included_candidate_ids must be exactly {EXPECTED_INCLUDED_IDS}")
    excluded = payload.get("excluded_candidate_ids")
    if not isinstance(excluded, list) or sorted(excluded) != sorted(EXPECTED_EXCLUDED_IDS):
        errors.append("excluded_candidate_ids must include exactly all 10 non-clean candidates")
    for key in ("fake_review_decisions_created", "fake_student_data_created", "source_truth_changed", "question_selection_changed", "scoring_mastery_changed"):
        _require_false(payload, key, errors, "packet JSON")
    items = payload.get("items")
    if not isinstance(items, list) or len(items) != 2:
        errors.append("packet JSON items must contain exactly 2 items")
        items = []
    ids = [str(item.get("source_candidate_id", "")) for item in items if isinstance(item, dict)]
    if ids != EXPECTED_INCLUDED_IDS:
        errors.append(f"packet JSON source IDs must be exactly {EXPECTED_INCLUDED_IDS}")
    for excluded_id in EXPECTED_EXCLUDED_IDS:
        if excluded_id in ids:
            errors.append(f"{excluded_id} must not appear in packet JSON items")
    for item in items:
        if not isinstance(item, dict):
            continue
        context = str(item.get("packet_item_id", "packet JSON item"))
        if item.get("internal_review_decision") is not None:
            errors.append(f"{context}: internal_review_decision must be null")
        for field in FALSE_FIELDS:
            _require_false(item, field, errors, context)
        if item.get("expected_answer") != "noun":
            errors.append(f"{context}: expected_answer must be noun")
        if item.get("source_candidate_id") == "g2srcdisc_p5_001" and "?????" not in str(item.get("question", "")):
            errors.append("g2srcdisc_p5_001 question must target ?????")
        if item.get("source_candidate_id") == "g2srcdisc_p5_005" and "????" not in str(item.get("question", "")):
            errors.append("g2srcdisc_p5_005 question must target ????")
    return ids


def _scan_text_artifacts(errors: list[str]) -> None:
    required_phrases = {
        PACKET_MD: ["internal protected-preview packet", "g2srcdisc_p5_001", "g2srcdisc_p5_005", "Internal reviewer decision"],
        GENERATION_REPORT: ["Source decision chain", "Why the five revision candidates are excluded", "No fake observations"],
        REVIEW_CHECKLIST: ["blank by design", "Reviewer decision:", "g2srcdisc_p5_001", "g2srcdisc_p5_005"],
        EXCLUDED_REGISTER: ["g2srcdisc_p5_002", "g2srcdisc_p6_007", "g2srcdisc_p6_005"],
        PIPELINE_STATUS: ["two-item internal protected-preview packet", "Still not runtime", "Still not reviewed bank", "Still not student-facing"],
    }
    for path, phrases in required_phrases.items():
        text = _read_text(path)
        lowered = text.lower()
        for phrase in phrases:
            if phrase.lower() not in lowered:
                errors.append(f"{_relative(path)} missing required phrase: {phrase}")
    for path in REQUIRED_FILES:
        text = _read_text(path)
        for pattern in FORBIDDEN_PATTERNS:
            if pattern in text:
                errors.append(f"{_relative(path)} contains forbidden claim: {pattern}")


def validate() -> dict:
    errors: list[str] = []
    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"Missing required file: {_relative(path)}")
    if errors:
        return {"ok": False, "errors": errors}
    tsv_ids = _validate_tsv(errors)
    payload = _load_json(PACKET_JSON, errors)
    json_ids = _validate_json(payload, errors)
    _scan_text_artifacts(errors)
    return {
        "ok": not errors,
        "errors": errors,
        "tsv_candidate_ids": tsv_ids,
        "json_candidate_ids": json_ids,
        "excluded_candidate_ids": payload.get("excluded_candidate_ids", []),
    }


def main() -> int:
    result = validate()
    if not result["ok"]:
        for error in result["errors"]:
            print(f"ERROR: {error}")
        return 1
    print("Perek 5-6 small internal protected-preview packet validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
