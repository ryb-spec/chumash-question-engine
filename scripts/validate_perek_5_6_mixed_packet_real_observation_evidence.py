from __future__ import annotations

import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "data/gate_2_protected_preview_packets/reports"
PIPELINE = ROOT / "data/pipeline_rounds"

PHASE_MD = REPORTS / "bereishis_perek_5_6_mixed_packet_real_observation_evidence_and_next_gate_2026_04_30.md"
PHASE_JSON = REPORTS / "bereishis_perek_5_6_mixed_packet_real_observation_evidence_and_next_gate_2026_04_30.json"
POST_GATE = PIPELINE / "bereishis_perek_5_6_mixed_packet_real_observation_post_gate_2026_04_30.md"
CHECKLIST = REPORTS / "bereishis_perek_5_6_mixed_limited_internal_review_checklist_2026_04_29.md"

REQUIRED_FILES = (PHASE_MD, PHASE_JSON, POST_GATE, CHECKLIST)
EXPECTED_INCLUDED_IDS = [
    "g2srcdisc_p5_001",
    "g2srcdisc_p5_005",
    "g2srcdisc_p6_001",
    "g2srcdisc_p6_006",
    "g2srcdisc_p6_007",
]
EXPECTED_EXCLUDED_IDS = [
    "g2srcdisc_p5_002",
    "g2srcdisc_p5_003",
    "g2srcdisc_p5_004",
    "g2srcdisc_p6_002",
    "g2srcdisc_p6_003",
    "g2srcdisc_p6_004",
    "g2srcdisc_p6_005",
]
EXPECTED_DECISIONS = {
    "g2srcdisc_p5_001": "approve_for_later_packet_iteration",
    "g2srcdisc_p5_005": "approve_for_later_packet_iteration",
    "g2srcdisc_p6_001": "revise",
    "g2srcdisc_p6_006": "revise",
    "g2srcdisc_p6_007": "hold",
}
EXPECTED_NEXT_GATE_STATUS = {
    "g2srcdisc_p5_001": "clean_limited_packet_iteration_ready",
    "g2srcdisc_p5_005": "clean_limited_packet_iteration_ready",
    "g2srcdisc_p6_001": "revise_before_broader_movement",
    "g2srcdisc_p6_006": "revise_before_broader_movement",
    "g2srcdisc_p6_007": "held_after_observation",
}
EXPECTED_CLEAN_IDS = ["g2srcdisc_p5_001", "g2srcdisc_p5_005"]
EXPECTED_REVISE_IDS = ["g2srcdisc_p6_001", "g2srcdisc_p6_006"]
EXPECTED_HOLD_IDS = ["g2srcdisc_p6_007"]
FALSE_TOP_FIELDS = (
    "student_observation_evidence_recorded",
    "fake_observations_created",
    "fake_student_data_created",
    "runtime_scope_widened",
    "reviewed_bank_promoted",
    "student_facing_created",
    "source_truth_changed",
    "question_selection_changed",
    "scoring_mastery_changed",
    "perek_5_activated",
    "perek_6_activated",
)
FALSE_ITEM_FIELDS = (
    "runtime_allowed",
    "reviewed_bank_allowed",
    "student_facing_allowed",
    "perek_5_activated",
    "perek_6_activated",
)
FORBIDDEN_PATTERNS = (
    "runtime_allowed=true",
    '"runtime_allowed": true',
    "reviewed_bank_allowed=true",
    '"reviewed_bank_allowed": true',
    "student_facing_allowed=true",
    '"student_facing_allowed": true',
    "promoted_to_runtime",
    "approved_for_runtime",
    "Perek 5 is active runtime",
    "Perek 6 is active runtime",
    "Perek 5 runtime is active",
    "Perek 6 runtime is active",
    "fake observation result",
    "fake student data created: true",
)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        payload = json.loads(text(path))
    except json.JSONDecodeError as exc:
        errors.append(f"{rel(path)} invalid JSON: {exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"{rel(path)} must contain a JSON object")
        return {}
    return payload


def require_false(value: dict, field: str, errors: list[str], context: str) -> None:
    if value.get(field) is not False:
        errors.append(f"{context}: {field} must be false")


def validate_contract(payload: dict, errors: list[str]) -> None:
    expected_scalars = {
        "streamlined_process_version": "v1",
        "phase_number": 7,
        "phase_name": "Observation Decisions + Next-Gate Authorization",
        "branch_name": "feature/perek-5-6-mixed-packet-real-observation-evidence",
        "observation_date": "2026-04-30",
        "evidence_type": "internal_teacher_review",
        "reviewer": "Yossi",
        "internal_review_evidence_recorded": True,
        "item_count": 5,
        "observed_count": 5,
        "not_observed_count": 0,
        "clean_after_observation_count": 2,
        "revise_count": 2,
        "hold_count": 1,
        "excluded_count": 7,
    }
    for field, expected in expected_scalars.items():
        if payload.get(field) != expected:
            errors.append(f"phase JSON {field} must be {expected!r}")
    for field in FALSE_TOP_FIELDS:
        require_false(payload, field, errors, "phase JSON")

    items = payload.get("items")
    if not isinstance(items, list) or len(items) != 5:
        errors.append("phase JSON must contain exactly 5 observed items")
        items = []
    ids = [item.get("source_candidate_id") for item in items if isinstance(item, dict)]
    if ids != EXPECTED_INCLUDED_IDS:
        errors.append(f"observed item IDs must be exactly {EXPECTED_INCLUDED_IDS}")

    clean_ids = [item.get("source_candidate_id") for item in items if isinstance(item, dict) and item.get("next_gate_status") == "clean_limited_packet_iteration_ready"]
    revise_ids = [item.get("source_candidate_id") for item in items if isinstance(item, dict) and item.get("next_gate_status") == "revise_before_broader_movement"]
    hold_ids = [item.get("source_candidate_id") for item in items if isinstance(item, dict) and item.get("next_gate_status") == "held_after_observation"]
    if clean_ids != EXPECTED_CLEAN_IDS:
        errors.append("clean-after-observation IDs mismatch")
    if revise_ids != EXPECTED_REVISE_IDS:
        errors.append("revise-after-observation IDs mismatch")
    if hold_ids != EXPECTED_HOLD_IDS:
        errors.append("hold-after-observation IDs mismatch")

    for item in items:
        if not isinstance(item, dict):
            continue
        candidate_id = str(item.get("source_candidate_id"))
        context = f"observed item {candidate_id}"
        if item.get("observed") is not True:
            errors.append(f"{context}: observed must be true")
        if item.get("post_observation_decision") != EXPECTED_DECISIONS.get(candidate_id):
            errors.append(f"{context}: post_observation_decision mismatch")
        if item.get("next_gate_status") != EXPECTED_NEXT_GATE_STATUS.get(candidate_id):
            errors.append(f"{context}: next_gate_status mismatch")
        if item.get("lane") == "revision_watch" and candidate_id in EXPECTED_CLEAN_IDS:
            errors.append(f"{context}: clean item cannot be revision_watch")
        if candidate_id in EXPECTED_REVISE_IDS + EXPECTED_HOLD_IDS and item.get("lane") != "revision_watch":
            errors.append(f"{context}: revision/hold item must remain revision_watch")
        for field in FALSE_ITEM_FIELDS:
            require_false(item, field, errors, context)

    excluded = payload.get("excluded_candidates")
    if not isinstance(excluded, list) or len(excluded) != 7:
        errors.append("phase JSON must contain exactly 7 excluded candidates")
        excluded = []
    excluded_ids = [item.get("source_candidate_id") for item in excluded if isinstance(item, dict)]
    if sorted(excluded_ids) != sorted(EXPECTED_EXCLUDED_IDS):
        errors.append("excluded candidate IDs mismatch")
    for item in excluded:
        if isinstance(item, dict) and item.get("eligible_for_next_gate") is not False:
            errors.append(f"excluded candidate {item.get('source_candidate_id')}: eligible_for_next_gate must be false")


def scan_texts(errors: list[str]) -> None:
    for path in REQUIRED_FILES:
        body = text(path)
        for pattern in FORBIDDEN_PATTERNS:
            if pattern in body:
                errors.append(f"{rel(path)} contains forbidden phrase: {pattern}")

    report = text(PHASE_MD)
    required_report_phrases = [
        "real Yossi internal review notes",
        "internal teacher/reviewer evidence",
        "not student observation evidence",
        "No observations were invented",
        "סֵפֶר and בֵּן may proceed",
        "בָשָׂר and פֶתַח require revision",
        "מַבּוּל remains held",
        "No runtime activation",
        "No reviewed-bank promotion",
        "No public/student-facing content",
    ]
    for phrase in required_report_phrases:
        if phrase not in report:
            errors.append(f"phase report missing required phrase: {phrase}")

    checklist = text(CHECKLIST)
    required_checklist_phrases = [
        "Evidence type: internal teacher/reviewer evidence",
        "Reviewer: Yossi",
        "Student observation evidence: no",
        "No observations were invented",
        "approve_for_later_packet_iteration",
        "revise_before_broader_movement",
        "held_after_observation",
    ]
    for phrase in required_checklist_phrases:
        if phrase not in checklist:
            errors.append(f"mixed packet checklist missing real-evidence phrase: {phrase}")


def validate() -> dict:
    errors: list[str] = []
    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"Missing required file: {rel(path)}")
    if errors:
        return {"ok": False, "errors": errors}
    payload = load_json(PHASE_JSON, errors)
    validate_contract(payload, errors)
    scan_texts(errors)
    return {"ok": not errors, "errors": errors, "phase_json": payload}


def main() -> int:
    result = validate()
    if not result["ok"]:
        for error in result["errors"]:
            print(f"ERROR: {error}")
        return 1
    print("Perek 5–6 mixed packet real observation evidence validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
