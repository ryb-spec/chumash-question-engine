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
PACKET_TSV = PACKET_DIR / "bereishis_perek_4_internal_protected_preview_packet.tsv"
PACKET_MD = REPORTS / "bereishis_perek_4_internal_protected_preview_packet_2026_04_29.md"
PACKET_JSON = REPORTS / "bereishis_perek_4_internal_protected_preview_packet_2026_04_29.json"
GENERATION_REPORT = REPORTS / "bereishis_perek_4_internal_protected_preview_packet_generation_report_2026_04_29.md"
REVIEW_CHECKLIST = REPORTS / "bereishis_perek_4_internal_protected_preview_review_checklist_2026_04_29.md"
PIPELINE_STATUS = ROOT / "data/pipeline_rounds/perek_4_internal_protected_preview_packet_created_2026_04_29.md"

REQUIRED_FILES = (PACKET_TSV, PACKET_MD, PACKET_JSON, GENERATION_REPORT, REVIEW_CHECKLIST, PIPELINE_STATUS)
EXPECTED_IDS = ["g2srcdisc_p4_001", "g2srcdisc_p4_002", "g2srcdisc_p4_003", "g2srcdisc_p4_004"]
BLOCKED_ID = "g2srcdisc_p4_005"
EXPECTED_INTERNAL_REVIEW_DECISIONS = {
    "g2ppacket_p4_001": "approve_for_limited_internal_preview",
    "g2ppacket_p4_002": "approve_for_limited_internal_preview",
    "g2ppacket_p4_003": "approve_with_revision",
    "g2ppacket_p4_004": "approve_with_revision",
}
FALSE_FIELDS = ("runtime_allowed", "reviewed_bank_allowed", "student_facing_allowed", "perek_4_activated")
REQUIRED_TSV_COLUMNS = [
    "packet_item_id",
    "source_candidate_id",
    "pasuk_ref",
    "hebrew_target",
    "proposed_question",
    "expected_answer",
    "distractors",
    "skill_family",
    "canonical_skill_id",
    "prior_teacher_decision",
    "revision_note",
    "spacing_session_balance_note",
    "source_or_alias_note",
    "internal_packet_allowed",
    "internal_packet_status",
    "internal_review_decision",
    "runtime_allowed",
    "reviewed_bank_allowed",
    "student_facing_allowed",
    "perek_4_activated",
]
FORBIDDEN_PATTERNS = (
    "runtime_allowed=true",
    "runtime_allowed: true",
    '"runtime_allowed": true',
    "reviewed_bank_allowed=true",
    "reviewed_bank_allowed: true",
    '"reviewed_bank_allowed": true',
    "promoted_to_runtime",
    "approved_for_runtime",
    "Perek 4 is active runtime",
    "Perek 4 runtime is active",
    "reviewed-bank promotion occurred",
    "student-facing launch",
    "public launch",
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
        errors.append("packet TSV columns do not match required Perek 4 internal packet schema")
    if len(rows) != 4:
        errors.append(f"packet TSV must have exactly 4 rows, found {len(rows)}")
    ids = [row.get("source_candidate_id", "") for row in rows]
    if ids != EXPECTED_IDS:
        errors.append(f"packet TSV source IDs must be exactly {EXPECTED_IDS}")
    if BLOCKED_ID in ids:
        errors.append("g2srcdisc_p4_005 must not appear in packet TSV")
    for row in rows:
        context = row.get("packet_item_id", "packet row")
        if row.get("internal_packet_allowed") != "true":
            errors.append(f"{context}: internal_packet_allowed must be true")
        if row.get("internal_packet_status") != "internal_protected_preview_only":
            errors.append(f"{context}: internal_packet_status must be internal_protected_preview_only")
        decision = row.get("internal_review_decision", "")
        if decision and decision != EXPECTED_INTERNAL_REVIEW_DECISIONS.get(context):
            errors.append(f"{context}: internal_review_decision must be blank or the expected applied decision")
        for field in FALSE_FIELDS:
            if row.get(field) != "false":
                errors.append(f"{context}: {field} must be false")
        for field in ("hebrew_target", "proposed_question", "expected_answer", "distractors", "revision_note"):
            if not row.get(field):
                errors.append(f"{context}: {field} must be populated")
    return ids


def _validate_json(payload: dict, errors: list[str]) -> list[str]:
    if payload.get("packet_status") != "internal_protected_preview_only":
        errors.append("packet_status must be internal_protected_preview_only")
    if payload.get("perek") != 4:
        errors.append("perek must be 4")
    if payload.get("item_count") != 4:
        errors.append("item_count must be 4")
    if payload.get("blocked_candidate_ids") != [BLOCKED_ID]:
        errors.append("blocked_candidate_ids must list only g2srcdisc_p4_005")
    if payload.get("reviewed_bank_promoted") is not False:
        errors.append("reviewed_bank_promoted must be false")
    if payload.get("fake_review_decisions_created") is not False:
        errors.append("fake_review_decisions_created must be false")
    if payload.get("internal_review_decisions_applied") not in (None, True):
        errors.append("internal_review_decisions_applied must be absent or true")
    if payload.get("fake_student_data_created") is not False:
        errors.append("fake_student_data_created must be false")
    for field in FALSE_FIELDS:
        _require_false(payload, field, errors, "packet JSON")
    items = payload.get("items")
    if not isinstance(items, list) or len(items) != 4:
        errors.append("packet JSON items must contain exactly 4 items")
        items = []
    ids = [str(item.get("source_candidate_id", "")) for item in items if isinstance(item, dict)]
    if ids != EXPECTED_IDS:
        errors.append(f"packet JSON source IDs must be exactly {EXPECTED_IDS}")
    if BLOCKED_ID in ids:
        errors.append("g2srcdisc_p4_005 must not appear in packet JSON items")
    for item in items:
        if not isinstance(item, dict):
            continue
        context = str(item.get("packet_item_id", "packet JSON item"))
        decision = item.get("internal_review_decision")
        if decision is not None and decision != EXPECTED_INTERNAL_REVIEW_DECISIONS.get(context):
            errors.append(f"{context}: internal_review_decision must be null or the expected applied decision")
        for field in FALSE_FIELDS:
            _require_false(item, field, errors, context)
        if item.get("source_candidate_id") == "g2srcdisc_p4_001" and "In this phrase" not in str(item.get("question", "")):
            errors.append("g2srcdisc_p4_001 must preserve revised In this phrase wording")
        if item.get("source_candidate_id") == "g2srcdisc_p4_003" and "spacing/session-balance" not in str(item.get("spacing_note", "")).lower():
            errors.append("g2srcdisc_p4_003 must preserve spacing/session-balance note")
        if item.get("source_candidate_id") == "g2srcdisc_p4_004":
            combined = f"{item.get('revision_note', '')} {item.get('source_or_alias_note', '')}"
            if "Minchah/offering alias" not in combined or "part-of-speech only" not in combined:
                errors.append("g2srcdisc_p4_004 must preserve Minchah/offering alias and part-of-speech-only notes")
    return ids


def _scan_text_artifacts(errors: list[str]) -> None:
    required_phrases = {
        PACKET_MD: ["internal protected-preview packet", BLOCKED_ID, "No Perek 4 runtime activation", "Internal reviewer decision"],
        GENERATION_REPORT: ["Source decision chain", "Why g2srcdisc_p4_005 is excluded", "No review decision has been applied"],
        REVIEW_CHECKLIST: ["approve_for_limited_internal_preview", BLOCKED_ID, "does not apply decisions"],
        PIPELINE_STATUS: ["still not runtime", "still not reviewed bank", "not public/student-facing", "Perek 5-6 source discovery should wait"],
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
        "blocked_candidate_ids": payload.get("blocked_candidate_ids", []),
    }


def main() -> int:
    result = validate()
    if not result["ok"]:
        for error in result["errors"]:
            print(f"ERROR: {error}")
        return 1
    print("Perek 4 internal protected-preview packet validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
