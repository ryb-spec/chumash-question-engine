from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "data/gate_2_protected_preview_candidates/reports"
CHECKLIST_MD = REPORTS / "bereishis_perek_4_candidate_planning_review_checklist_2026_04_29.md"
CHECKLIST_JSON = REPORTS / "bereishis_perek_4_candidate_planning_review_checklist_2026_04_29.json"
READINESS_MD = ROOT / "data/pipeline_rounds/perek_4_candidate_planning_review_checklist_readiness_2026_04_29.md"
SOURCE_PLANNING_TSV = ROOT / "data/gate_2_protected_preview_candidates/bereishis_perek_4_protected_preview_candidate_planning.tsv"

REQUIRED_FILES = (CHECKLIST_MD, CHECKLIST_JSON, READINESS_MD, SOURCE_PLANNING_TSV)
EXPECTED_ELIGIBLE_IDS = ["g2srcdisc_p4_001", "g2srcdisc_p4_002", "g2srcdisc_p4_003", "g2srcdisc_p4_004"]
BLOCKED_ID = "g2srcdisc_p4_005"
EXPECTED_DECISIONS = {
    "g2srcdisc_p4_001": "advance_to_protected_preview_candidate_review",
    "g2srcdisc_p4_002": "advance_to_protected_preview_candidate_review",
    "g2srcdisc_p4_003": "advance_with_minor_revision",
    "g2srcdisc_p4_004": "advance_with_minor_revision",
}
EXPECTED_ALLOWED_DECISIONS = [
    "advance_to_protected_preview_candidate_review",
    "advance_with_minor_revision",
    "hold_for_spacing_or_balance",
    "needs_source_follow_up",
    "reject",
    "source_only",
]
FALSE_FIELDS = ("runtime_allowed", "reviewed_bank_allowed", "protected_preview_packet_allowed_now", "student_facing_allowed", "perek_4_activated")
FORBIDDEN_PATTERNS = (
    "runtime_allowed=true", "runtime_allowed: true", '"runtime_allowed": true',
    "reviewed_bank_allowed=true", "reviewed_bank_allowed: true", '"reviewed_bank_allowed": true',
    "promoted_to_runtime", "approved_for_runtime", "Perek 4 is active runtime", "Perek 4 runtime is active",
    "Perek 4 runtime activation is approved", "protected-preview packet has been created",
    "protected-preview packet created: yes", '"protected_preview_packet_created": true',
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


def _read_planning_ids(errors: list[str]) -> list[str]:
    with SOURCE_PLANNING_TSV.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    ids = [row.get("candidate_id", "") for row in rows]
    if ids != EXPECTED_ELIGIBLE_IDS:
        errors.append(f"source planning TSV must include only eligible candidates: {EXPECTED_ELIGIBLE_IDS}")
    if BLOCKED_ID in ids:
        errors.append(f"source planning TSV must exclude blocked candidate {BLOCKED_ID}")
    for row in rows:
        context = row.get("candidate_id", "planning row")
        for field in FALSE_FIELDS:
            if row.get(field) != "false":
                errors.append(f"{context}: source planning TSV field {field} must be false")
    return ids


def validate() -> dict:
    errors: list[str] = []
    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"Missing required file: {_relative(path)}")
    if errors:
        return {"ok": False, "errors": errors}

    payload = _load_json(CHECKLIST_JSON, errors)
    if payload.get("checklist_status") != "planning_review_decisions_applied":
        errors.append("checklist_status must be planning_review_decisions_applied")
    if payload.get("source_planning_tsv") != _relative(SOURCE_PLANNING_TSV):
        errors.append("checklist JSON source_planning_tsv must point to the source planning TSV")
    if payload.get("eligible_candidate_ids") != EXPECTED_ELIGIBLE_IDS:
        errors.append(f"eligible_candidate_ids must be exactly {EXPECTED_ELIGIBLE_IDS}")
    if payload.get("blocked_candidate_ids") != [BLOCKED_ID]:
        errors.append(f"blocked_candidate_ids must include only {BLOCKED_ID}")
    if payload.get("allowed_planning_decisions") != EXPECTED_ALLOWED_DECISIONS:
        errors.append("allowed_planning_decisions do not match the expected planning-review options")
    for field in FALSE_FIELDS:
        _require_false(payload, field, errors, "checklist JSON")
    if payload.get("protected_preview_packet_created") is not False:
        errors.append("checklist JSON must keep protected_preview_packet_created false")

    candidates = payload.get("candidates")
    if not isinstance(candidates, list) or len(candidates) != 4:
        errors.append("checklist JSON must include exactly 4 eligible candidates")
        candidates = []
    candidate_ids = [str(candidate.get("candidate_id", "")) for candidate in candidates if isinstance(candidate, dict)]
    if candidate_ids != EXPECTED_ELIGIBLE_IDS:
        errors.append(f"checklist candidate IDs must be exactly {EXPECTED_ELIGIBLE_IDS}")
    if BLOCKED_ID in candidate_ids:
        errors.append(f"{BLOCKED_ID} must not be in the eligible checklist candidates")
    for candidate in candidates:
        if not isinstance(candidate, dict):
            errors.append("candidate entry must be an object")
            continue
        context = candidate.get("candidate_id", "candidate")
        if candidate.get("planning_review_decision") != EXPECTED_DECISIONS.get(context):
            errors.append(f"{context}: planning_review_decision does not match Yossi's applied decision")
        for field in FALSE_FIELDS:
            _require_false(candidate, field, errors, context)
        for field in ("pasuk_ref", "hebrew_target", "prior_teacher_decision", "proposed_question", "expected_answer", "remaining_risk_note", "required_note"):
            if not candidate.get(field):
                errors.append(f"{context}: {field} must be populated")
        distractors = candidate.get("distractors")
        if not isinstance(distractors, list) or len(distractors) != 3:
            errors.append(f"{context}: distractors must include exactly three choices")

    planning_ids = _read_planning_ids(errors)
    checklist_text = _read_text(CHECKLIST_MD)
    readiness_text = _read_text(READINESS_MD)
    for required in ("not runtime content", "not reviewed-bank content", "not an internal protected-preview packet", "g2srcdisc_p4_005", "Planning review decision:", "Fake teacher decisions created: no"):
        if required not in checklist_text:
            errors.append(f"checklist Markdown missing required phrase: {required}")
    for required in ("This checklist does not create a protected-preview packet, does not activate Perek 4, and does not create student-facing content.", "g2srcdisc_p4_005", "Perek 4 runtime activation remains blocked.", "Internal protected-preview packet creation remains blocked."):
        if required not in readiness_text:
            errors.append(f"readiness report missing required phrase: {required}")
    for path in (CHECKLIST_MD, CHECKLIST_JSON, READINESS_MD):
        text = _read_text(path)
        for pattern in FORBIDDEN_PATTERNS:
            if pattern in text:
                errors.append(f"{_relative(path)} contains forbidden claim: {pattern}")
    return {"ok": not errors, "errors": errors, "eligible_candidate_ids": candidate_ids, "planning_tsv_candidate_ids": planning_ids}


def main() -> int:
    result = validate()
    if not result["ok"]:
        for error in result["errors"]:
            print(f"ERROR: {error}")
        return 1
    print("Perek 4 candidate-planning review checklist validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
