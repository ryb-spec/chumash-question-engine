from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "data/gate_2_protected_preview_candidates/reports"

DECISIONS_MD = REPORTS / "bereishis_perek_4_teacher_review_decisions_applied_2026_04_29.md"
DECISIONS_JSON = REPORTS / "bereishis_perek_4_teacher_review_decisions_applied_2026_04_29.json"
PACKET_MD = REPORTS / "bereishis_perek_4_compressed_teacher_review_packet_2026_04_29.md"
PACKET_JSON = REPORTS / "bereishis_perek_4_compressed_teacher_review_packet_2026_04_29.json"
OT_FOLLOWUP_MD = REPORTS / "bereishis_perek_4_ot_source_followup_2026_04_29.md"
REVISION_PLAN_MD = REPORTS / "bereishis_perek_4_teacher_review_revision_plan_2026_04_29.md"
NEXT_GATE_MD = ROOT / "data/pipeline_rounds/perek_4_post_teacher_review_next_gate_readiness_2026_04_29.md"
PLANNING_TSV = ROOT / "data/gate_2_protected_preview_candidates/bereishis_perek_4_protected_preview_candidate_planning.tsv"
SOURCE_INVENTORY = ROOT / "data/gate_2_source_discovery/bereishis_perek_4_review_only_safe_candidate_inventory.tsv"

REQUIRED_FILES = (
    DECISIONS_MD,
    DECISIONS_JSON,
    PACKET_MD,
    PACKET_JSON,
    OT_FOLLOWUP_MD,
    REVISION_PLAN_MD,
    NEXT_GATE_MD,
    SOURCE_INVENTORY,
)
EXPECTED_DECISIONS = {
    "g2srcdisc_p4_001": "approve_with_revision",
    "g2srcdisc_p4_002": "approve_for_protected_preview",
    "g2srcdisc_p4_003": "approve_with_revision",
    "g2srcdisc_p4_004": "approve_with_revision",
    "g2srcdisc_p4_005": "needs_source_follow_up",
}
ELIGIBLE_IDS = ["g2srcdisc_p4_001", "g2srcdisc_p4_002", "g2srcdisc_p4_003", "g2srcdisc_p4_004"]
BLOCKED_ID = "g2srcdisc_p4_005"
FALSE_DECISION_FIELDS = (
    "runtime_allowed",
    "reviewed_bank_allowed",
    "protected_preview_packet_allowed_now",
    "student_facing_allowed",
    "perek_4_activated",
)
FALSE_PACKET_FIELDS = (
    "runtime_allowed",
    "reviewed_bank_allowed",
    "protected_preview_allowed",
    "protected_preview_packet_allowed_now",
    "student_facing_allowed",
    "broader_use_allowed",
    "perek_4_activated",
)
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
    '"fake_teacher_decisions_created": true',
    "Perek 4 is active in runtime",
    "Active scope expansion occurred: yes",
    "active scope expansion: true",
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
        errors.append(f"{_relative(path)} must contain a JSON object")
        return {}
    return payload


def _require_false(payload: dict, key: str, errors: list[str], context: str) -> None:
    if payload.get(key) is not False:
        errors.append(f"{context}: {key} must be false")


def _validate_planning_tsv(errors: list[str]) -> list[str]:
    if not PLANNING_TSV.exists():
        return []
    with PLANNING_TSV.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    ids = [row.get("candidate_id", "") for row in rows]
    if ids != ELIGIBLE_IDS:
        errors.append(f"planning TSV must include only eligible IDs in order: {ELIGIBLE_IDS}")
    if BLOCKED_ID in ids:
        errors.append("planning TSV must exclude g2srcdisc_p4_005")
    for row in rows:
        context = row.get("candidate_id", "planning row")
        for field in (
            "runtime_allowed",
            "reviewed_bank_allowed",
            "protected_preview_allowed",
            "protected_preview_packet_allowed_now",
            "student_facing_allowed",
            "broader_use_allowed",
            "perek_4_activated",
        ):
            if row.get(field) != "false":
                errors.append(f"{context}: {field} must be false in planning TSV")
        if row.get("decision_source") != "Yossi teacher review decisions 2026-04-29":
            errors.append(f"{context}: decision_source must cite Yossi teacher review decisions")
    return ids


def validate() -> dict:
    errors: list[str] = []
    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"Missing required file: {_relative(path)}")
    if errors:
        return {"ok": False, "errors": errors}

    decisions_payload = _load_json(DECISIONS_JSON, errors)
    packet_payload = _load_json(PACKET_JSON, errors)
    decisions = decisions_payload.get("decisions")
    if not isinstance(decisions, list):
        errors.append("decisions-applied JSON must include a decisions list")
        decisions = []
    if len(decisions) != 5:
        errors.append("decisions-applied JSON must include exactly 5 decisions")

    decisions_by_id = {str(decision.get("candidate_id", "")): decision for decision in decisions if isinstance(decision, dict)}
    if set(decisions_by_id) != set(EXPECTED_DECISIONS):
        errors.append("decisions-applied JSON candidate IDs do not match expected Perek 4 source-discovery IDs")

    for candidate_id, expected in EXPECTED_DECISIONS.items():
        decision = decisions_by_id.get(candidate_id, {})
        if decision.get("teacher_decision") != expected:
            errors.append(f"{candidate_id}: expected teacher_decision {expected}")
        for field in FALSE_DECISION_FIELDS:
            _require_false(decision, field, errors, candidate_id)
        if candidate_id == "g2srcdisc_p4_001":
            if "In this phrase" not in str(decision.get("revised_question_wording", "")):
                errors.append("g2srcdisc_p4_001 revised question must include 'In this phrase'")
            if decision.get("eligible_for_next_gate") is not True:
                errors.append("g2srcdisc_p4_001 must be eligible only after wording revision is applied")
        if candidate_id == BLOCKED_ID:
            if decision.get("eligible_for_next_gate") is not False:
                errors.append("g2srcdisc_p4_005 must not be eligible for the next gate")
            if decision.get("source_follow_up_required") is not True:
                errors.append("g2srcdisc_p4_005 must require source follow-up")
        elif decision.get("eligible_for_next_gate") is not True:
            errors.append(f"{candidate_id}: eligible_for_next_gate must be true")

    packet_candidates = packet_payload.get("candidates")
    if not isinstance(packet_candidates, list) or len(packet_candidates) != 5:
        errors.append("updated teacher-review packet must include exactly 5 candidates")
        packet_candidates = []
    for candidate in packet_candidates:
        if not isinstance(candidate, dict):
            errors.append("packet candidate must be an object")
            continue
        candidate_id = str(candidate.get("candidate_id", ""))
        expected = EXPECTED_DECISIONS.get(candidate_id)
        if candidate.get("teacher_decision") != expected:
            errors.append(f"{candidate_id}: packet teacher_decision must be {expected}")
        for field in FALSE_PACKET_FIELDS:
            _require_false(candidate, field, errors, f"packet {candidate_id}")

    planning_ids = _validate_planning_tsv(errors)

    decisions_text = _read_text(DECISIONS_MD)
    packet_text = _read_text(PACKET_MD)
    followup_text = _read_text(OT_FOLLOWUP_MD)
    revision_text = _read_text(REVISION_PLAN_MD)
    next_gate_text = _read_text(NEXT_GATE_MD)
    for required in (
        "g2srcdisc_p4_001: approve_with_revision",
        "g2srcdisc_p4_002: approve_for_protected_preview",
        "g2srcdisc_p4_003: approve_with_revision",
        "g2srcdisc_p4_004: approve_with_revision",
        "g2srcdisc_p4_005: needs_source_follow_up",
    ):
        if required not in decisions_text:
            errors.append(f"decisions report missing explicit decision phrase: {required}")
    if "????" not in followup_text or "???" not in followup_text:
        errors.append("???? source follow-up report must mention ???? and ???")
    if "In this phrase" not in revision_text:
        errors.append("revision plan must include revised g2srcdisc_p4_001 wording")
    for required in (
        "Perek 4 runtime activation remains blocked.",
        "Active scope expansion remains blocked.",
        "Reviewed-bank promotion remains blocked.",
        "Student-facing content remains blocked.",
        "g2srcdisc_p4_005` remains source-follow-up",
    ):
        if required not in next_gate_text:
            errors.append(f"next-gate readiness report missing required phrase: {required}")
    if "Yossi's decisions are now applied" not in packet_text:
        errors.append("updated teacher-review packet must state Yossi decisions are applied")

    for path in (DECISIONS_MD, DECISIONS_JSON, PACKET_MD, PACKET_JSON, OT_FOLLOWUP_MD, REVISION_PLAN_MD, NEXT_GATE_MD, PLANNING_TSV):
        if not path.exists():
            continue
        text = _read_text(path)
        for pattern in FORBIDDEN_PATTERNS:
            if pattern in text:
                errors.append(f"{_relative(path)} contains forbidden claim: {pattern}")

    return {"ok": not errors, "errors": errors, "decision_count": len(decisions), "planning_candidate_ids": planning_ids}


def main() -> int:
    result = validate()
    if not result["ok"]:
        for error in result["errors"]:
            print(f"ERROR: {error}")
        return 1
    print("Perek 4 teacher-review decisions-applied validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
