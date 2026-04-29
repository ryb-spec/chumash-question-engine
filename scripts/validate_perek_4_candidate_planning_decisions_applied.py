from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "data/gate_2_protected_preview_candidates/reports"
DECISIONS_MD = REPORTS / "bereishis_perek_4_candidate_planning_decisions_applied_2026_04_29.md"
DECISIONS_JSON = REPORTS / "bereishis_perek_4_candidate_planning_decisions_applied_2026_04_29.json"
CHECKLIST_MD = REPORTS / "bereishis_perek_4_candidate_planning_review_checklist_2026_04_29.md"
CHECKLIST_JSON = REPORTS / "bereishis_perek_4_candidate_planning_review_checklist_2026_04_29.json"
READINESS_MD = ROOT / "data/pipeline_rounds/perek_4_candidate_planning_decisions_next_gate_readiness_2026_04_29.md"
REVIEW_TSV = ROOT / "data/gate_2_protected_preview_candidates/bereishis_perek_4_protected_preview_candidate_review.tsv"

REQUIRED_FILES = (DECISIONS_MD, DECISIONS_JSON, CHECKLIST_MD, CHECKLIST_JSON, READINESS_MD)
EXPECTED_DECISIONS = {
    "g2srcdisc_p4_001": "advance_to_protected_preview_candidate_review",
    "g2srcdisc_p4_002": "advance_to_protected_preview_candidate_review",
    "g2srcdisc_p4_003": "advance_with_minor_revision",
    "g2srcdisc_p4_004": "advance_with_minor_revision",
    "g2srcdisc_p4_005": "needs_source_follow_up",
}
ADVANCING_IDS = ["g2srcdisc_p4_001", "g2srcdisc_p4_002", "g2srcdisc_p4_003", "g2srcdisc_p4_004"]
BLOCKED_ID = "g2srcdisc_p4_005"
FALSE_FIELDS = ("runtime_allowed", "reviewed_bank_allowed", "protected_preview_packet_allowed_now", "student_facing_allowed", "perek_4_activated")
FORBIDDEN_PATTERNS = (
    "runtime_allowed=true", "runtime_allowed: true", '"runtime_allowed": true',
    "reviewed_bank_allowed=true", "reviewed_bank_allowed: true", '"reviewed_bank_allowed": true',
    "promoted_to_runtime", "approved_for_runtime", "protected-preview packet created: yes",
    "protected-preview packet has been created", '"protected_preview_packet_created": true',
    "Perek 4 is active runtime", "Perek 4 runtime is active", "Perek 4 runtime activation is approved",
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


def _validate_review_tsv(errors: list[str]) -> list[str]:
    if not REVIEW_TSV.exists():
        return []
    with REVIEW_TSV.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    ids = [row.get("candidate_id", "") for row in rows]
    if ids != ADVANCING_IDS:
        errors.append(f"review TSV must include only the four advancing candidates: {ADVANCING_IDS}")
    if BLOCKED_ID in ids:
        errors.append("review TSV must exclude g2srcdisc_p4_005")
    for row in rows:
        context = row.get("candidate_id", "review row")
        allowed_review_statuses = {
            "pending_protected_preview_candidate_review",
            "protected_preview_candidate_review_decision_applied",
        }
        if row.get("teacher_review_status") not in allowed_review_statuses:
            errors.append(
                f"{context}: teacher_review_status must be one of {sorted(allowed_review_statuses)}"
            )
        if row.get("final_approval_status") != "none":
            errors.append(f"{context}: final_approval_status must be none")
        for field in FALSE_FIELDS:
            if row.get(field) != "false":
                errors.append(f"{context}: review TSV field {field} must be false")
    return ids


def validate() -> dict:
    errors: list[str] = []
    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"Missing required file: {_relative(path)}")
    if errors:
        return {"ok": False, "errors": errors}
    payload = _load_json(DECISIONS_JSON, errors)
    checklist = _load_json(CHECKLIST_JSON, errors)

    decisions = payload.get("decisions")
    if not isinstance(decisions, list) or len(decisions) != 5:
        errors.append("decisions-applied JSON must include exactly five decisions")
        decisions = []
    decisions_by_id = {str(decision.get("candidate_id", "")): decision for decision in decisions if isinstance(decision, dict)}
    if set(decisions_by_id) != set(EXPECTED_DECISIONS):
        errors.append("decision IDs must match the expected five Perek 4 candidates")
    if payload.get("candidate_count") != 5:
        errors.append("candidate_count must be 5")
    if payload.get("advancing_candidate_count") != 4:
        errors.append("advancing_candidate_count must be 4")
    if payload.get("blocked_candidate_count") != 1:
        errors.append("blocked_candidate_count must be 1")
    if payload.get("advancing_candidate_ids") != ADVANCING_IDS:
        errors.append("advancing_candidate_ids must be the four expected IDs")
    if payload.get("blocked_candidate_ids") != [BLOCKED_ID]:
        errors.append("blocked_candidate_ids must be [g2srcdisc_p4_005]")
    for field in FALSE_FIELDS:
        _require_false(payload, field, errors, "decisions JSON")
    if payload.get("protected_preview_packet_created") is not False:
        errors.append("protected_preview_packet_created must be false")

    for candidate_id, expected_decision in EXPECTED_DECISIONS.items():
        decision = decisions_by_id.get(candidate_id, {})
        if decision.get("planning_review_decision") != expected_decision:
            errors.append(f"{candidate_id}: expected planning_review_decision {expected_decision}")
        for field in FALSE_FIELDS:
            _require_false(decision, field, errors, candidate_id)
        if candidate_id == BLOCKED_ID:
            if decision.get("eligible_for_protected_preview_candidate_review") is not False:
                errors.append("g2srcdisc_p4_005 must remain ineligible for protected-preview-candidate review")
            if decision.get("source_follow_up_required") is not True:
                errors.append("g2srcdisc_p4_005 must require source follow-up")
        elif decision.get("eligible_for_protected_preview_candidate_review") is not True:
            errors.append(f"{candidate_id}: must be eligible for protected-preview-candidate review")

    checklist_candidates = checklist.get("candidates")
    if not isinstance(checklist_candidates, list) or len(checklist_candidates) != 4:
        errors.append("updated checklist must contain exactly four eligible candidates")
        checklist_candidates = []
    for candidate in checklist_candidates:
        candidate_id = str(candidate.get("candidate_id", ""))
        if candidate.get("planning_review_decision") != EXPECTED_DECISIONS.get(candidate_id):
            errors.append(f"{candidate_id}: checklist planning_review_decision does not match expected decision")
        for field in FALSE_FIELDS:
            _require_false(candidate, field, errors, f"checklist {candidate_id}")

    review_ids = _validate_review_tsv(errors)
    decisions_text = _read_text(DECISIONS_MD)
    readiness_text = _read_text(READINESS_MD)
    for required in (
        "g2srcdisc_p4_001", "advance_to_protected_preview_candidate_review",
        "g2srcdisc_p4_003", "advance_with_minor_revision", "g2srcdisc_p4_005", "needs_source_follow_up",
        "No protected-preview packet creation.",
    ):
        if required not in decisions_text:
            errors.append(f"decisions report missing required phrase: {required}")
    for required in (
        "no Perek 4 runtime activation", "no active-scope expansion", "no reviewed-bank promotion",
        "no protected-preview packet created", "no student-facing content created", "g2srcdisc_p4_005 remains blocked",
    ):
        if required not in readiness_text:
            errors.append(f"readiness report missing required phrase: {required}")
    for path in (DECISIONS_MD, DECISIONS_JSON, CHECKLIST_MD, CHECKLIST_JSON, READINESS_MD, REVIEW_TSV):
        if not path.exists():
            continue
        text = _read_text(path)
        for pattern in FORBIDDEN_PATTERNS:
            if pattern in text:
                errors.append(f"{_relative(path)} contains forbidden claim: {pattern}")
    return {"ok": not errors, "errors": errors, "advancing_candidate_ids": payload.get("advancing_candidate_ids", []), "review_tsv_candidate_ids": review_ids}


def main() -> int:
    result = validate()
    if not result["ok"]:
        for error in result["errors"]:
            print(f"ERROR: {error}")
        return 1
    print("Perek 4 candidate-planning decisions-applied validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
