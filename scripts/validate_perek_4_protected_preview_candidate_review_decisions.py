from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_DIR = ROOT / "data/gate_2_protected_preview_candidates"
PACKET_REPORTS = ROOT / "data/gate_2_protected_preview_packets/reports"
REPORTS = CANDIDATE_DIR / "reports"
DECISIONS_MD = REPORTS / "bereishis_perek_4_protected_preview_candidate_review_decisions_applied_2026_04_29.md"
DECISIONS_JSON = REPORTS / "bereishis_perek_4_protected_preview_candidate_review_decisions_applied_2026_04_29.json"
REVIEW_TSV = CANDIDATE_DIR / "bereishis_perek_4_protected_preview_candidate_review.tsv"
READINESS_MD = ROOT / "data/pipeline_rounds/perek_4_internal_protected_preview_packet_readiness_2026_04_29.md"
PLANNING_MD = PACKET_REPORTS / "bereishis_perek_4_internal_protected_preview_packet_planning_2026_04_29.md"

REQUIRED_FILES = (DECISIONS_MD, DECISIONS_JSON, REVIEW_TSV, READINESS_MD)
EXPECTED_DECISIONS = {
    "g2srcdisc_p4_001": "approve_for_internal_protected_preview_packet",
    "g2srcdisc_p4_002": "approve_for_internal_protected_preview_packet",
    "g2srcdisc_p4_003": "approve_with_revision",
    "g2srcdisc_p4_004": "approve_with_revision",
    "g2srcdisc_p4_005": "needs_source_follow_up",
}
ELIGIBLE_IDS = ["g2srcdisc_p4_001", "g2srcdisc_p4_002", "g2srcdisc_p4_003", "g2srcdisc_p4_004"]
BLOCKED_ID = "g2srcdisc_p4_005"
FALSE_FIELDS = ("runtime_allowed", "reviewed_bank_allowed", "student_facing_allowed", "perek_4_activated")
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
    "Perek 4 runtime activation is approved",
)


def _relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


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


def _validate_decisions_json(payload: dict, errors: list[str]) -> dict[str, dict]:
    decisions = payload.get("decisions")
    if not isinstance(decisions, list) or len(decisions) != 5:
        errors.append("decisions JSON must include exactly five decisions")
        decisions = []
    decisions_by_id = {str(decision.get("candidate_id", "")): decision for decision in decisions if isinstance(decision, dict)}
    if set(decisions_by_id) != set(EXPECTED_DECISIONS):
        errors.append("decision IDs must match the expected five Perek 4 candidates")
    if payload.get("candidate_count") != 5:
        errors.append("candidate_count must be 5")
    if payload.get("approved_for_internal_packet_count") != 2:
        errors.append("approved_for_internal_packet_count must be 2")
    if payload.get("approve_with_revision_count") != 2:
        errors.append("approve_with_revision_count must be 2")
    if payload.get("blocked_count") != 1:
        errors.append("blocked_count must be 1")
    if payload.get("eligible_candidate_ids") != ELIGIBLE_IDS:
        errors.append("eligible_candidate_ids must be the four expected IDs")
    if payload.get("blocked_candidate_ids") != [BLOCKED_ID]:
        errors.append("blocked_candidate_ids must be [g2srcdisc_p4_005]")
    if payload.get("protected_preview_packet_created") is not False:
        errors.append("protected_preview_packet_created must be false")
    if payload.get("fake_teacher_decisions_created") is not False:
        errors.append("fake_teacher_decisions_created must be false")
    if payload.get("fake_student_data_created") is not False:
        errors.append("fake_student_data_created must be false")
    for field in FALSE_FIELDS:
        _require_false(payload, field, errors, "decisions JSON")

    for candidate_id, expected_decision in EXPECTED_DECISIONS.items():
        decision = decisions_by_id.get(candidate_id, {})
        if decision.get("decision") != expected_decision:
            errors.append(f"{candidate_id}: expected decision {expected_decision}")
        for field in FALSE_FIELDS:
            _require_false(decision, field, errors, candidate_id)
        if candidate_id == BLOCKED_ID:
            if decision.get("eligible_for_internal_protected_preview_packet") is not False:
                errors.append("g2srcdisc_p4_005 must not be eligible for an internal protected-preview packet")
        elif decision.get("eligible_for_internal_protected_preview_packet") is not True:
            errors.append(f"{candidate_id}: must be eligible for later internal packet planning")
    return decisions_by_id


def _validate_review_tsv(decisions_by_id: dict[str, dict], errors: list[str]) -> list[str]:
    with REVIEW_TSV.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    ids = [row.get("candidate_id", "") for row in rows]
    if ids != ELIGIBLE_IDS:
        errors.append(f"review TSV must include only the four eligible candidates: {ELIGIBLE_IDS}")
    if BLOCKED_ID in ids:
        errors.append("review TSV must exclude g2srcdisc_p4_005")
    required_columns = {
        "protected_preview_candidate_review_decision",
        "revision_required",
        "revision_note",
        "eligible_for_internal_protected_preview_packet",
        "source_follow_up_required",
    }
    if rows:
        missing = required_columns.difference(rows[0])
        if missing:
            errors.append(f"review TSV missing decision columns: {sorted(missing)}")
    for row in rows:
        candidate_id = row.get("candidate_id", "")
        expected_decision = EXPECTED_DECISIONS.get(candidate_id)
        if row.get("protected_preview_candidate_review_decision") != expected_decision:
            errors.append(f"{candidate_id}: review TSV decision must be {expected_decision}")
        if row.get("eligible_for_internal_protected_preview_packet") != "true":
            errors.append(f"{candidate_id}: review TSV eligible_for_internal_protected_preview_packet must be true")
        if row.get("source_follow_up_required") != "false":
            errors.append(f"{candidate_id}: review TSV source_follow_up_required must be false")
        if row.get("final_approval_status") != "none":
            errors.append(f"{candidate_id}: final_approval_status must remain none")
        for field in FALSE_FIELDS:
            if row.get(field) != "false":
                errors.append(f"{candidate_id}: review TSV field {field} must be false")
        if row.get("reviewed_bank_allowed") != "false":
            errors.append(f"{candidate_id}: reviewed_bank_allowed must be false")
        if row.get("protected_preview_packet_allowed_now") != "false":
            errors.append(f"{candidate_id}: protected_preview_packet_allowed_now must be false")
        if candidate_id in decisions_by_id:
            expected_revision = "true" if decisions_by_id[candidate_id].get("revision_required") is True else "false"
            if row.get("revision_required") != expected_revision:
                errors.append(f"{candidate_id}: review TSV revision_required must be {expected_revision}")
    return ids


def _validate_planning_artifact(errors: list[str]) -> None:
    if not PLANNING_MD.exists():
        return
    text = _read_text(PLANNING_MD)
    for candidate_id in ELIGIBLE_IDS:
        if candidate_id not in text:
            errors.append(f"planning artifact must include {candidate_id}")
    if BLOCKED_ID not in text or "excluded" not in text.lower():
        errors.append("planning artifact must clearly exclude g2srcdisc_p4_005")
    for required in ("planning-only", "not a packet", "Protected-preview packet created: no"):
        if required not in text:
            errors.append(f"planning artifact missing required phrase: {required}")


def _scan_forbidden(errors: list[str]) -> None:
    for path in (*REQUIRED_FILES, PLANNING_MD):
        if not path.exists():
            continue
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

    payload = _load_json(DECISIONS_JSON, errors)
    decisions_by_id = _validate_decisions_json(payload, errors)
    review_ids = _validate_review_tsv(decisions_by_id, errors)

    decisions_text = _read_text(DECISIONS_MD)
    readiness_text = _read_text(READINESS_MD)
    for required in (
        "approve_for_internal_protected_preview_packet",
        "approve_with_revision",
        "needs_source_follow_up",
        "g2srcdisc_p4_005",
        "Protected-preview packet created: no",
    ):
        if required not in decisions_text:
            errors.append(f"decisions report missing required phrase: {required}")
    for required in (
        "No Perek 4 runtime activation.",
        "No active scope expansion.",
        "No reviewed-bank promotion.",
        "No student-facing content.",
        "Internal protected-preview packet creation requires a later explicit task",
    ):
        if required not in readiness_text:
            errors.append(f"readiness report missing required phrase: {required}")
    _validate_planning_artifact(errors)
    _scan_forbidden(errors)
    return {
        "ok": not errors,
        "errors": errors,
        "eligible_candidate_ids": payload.get("eligible_candidate_ids", []),
        "review_tsv_candidate_ids": review_ids,
        "blocked_candidate_ids": payload.get("blocked_candidate_ids", []),
    }


def main() -> int:
    result = validate()
    if not result["ok"]:
        for error in result["errors"]:
            print(f"ERROR: {error}")
        return 1
    print("Perek 4 protected-preview candidate review decisions validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
