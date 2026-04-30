from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


ROOT = Path(__file__).resolve().parents[1]
PLANNING_DIR = ROOT / "data" / "reviewed_bank_candidate_planning"
PIPELINE = ROOT / "data" / "pipeline_rounds"

PLANNING_TSV = PLANNING_DIR / "bereishis_perek_4_broad_vocabulary_reviewed_bank_candidate_planning_2026_04_30.tsv"
PLANNING_JSON = PLANNING_DIR / "bereishis_perek_4_broad_vocabulary_reviewed_bank_candidate_planning_2026_04_30.json"
EVIDENCE_MD = PLANNING_DIR / "bereishis_perek_4_broad_vocabulary_reviewed_bank_candidate_evidence_map_2026_04_30.md"
EVIDENCE_JSON = PLANNING_DIR / "bereishis_perek_4_broad_vocabulary_reviewed_bank_candidate_evidence_map_2026_04_30.json"
BLOCKED_MD = PLANNING_DIR / "bereishis_perek_4_broad_vocabulary_reviewed_bank_candidate_blocked_register_2026_04_30.md"
BLOCKED_JSON = PLANNING_DIR / "bereishis_perek_4_broad_vocabulary_reviewed_bank_candidate_blocked_register_2026_04_30.json"
REPORT_MD = PIPELINE / "perek_4_broad_vocabulary_reviewed_bank_candidate_planning_2026_04_30.md"
REPORT_JSON = PIPELINE / "perek_4_broad_vocabulary_reviewed_bank_candidate_planning_2026_04_30.json"
NEXT_PROMPT = PIPELINE / "next_codex_prompt_perek_4_broad_vocabulary_reviewed_bank_decision_packet_2026_04_30.md"

FINAL_OBSERVATION_JSON = (
    "data/gate_2_protected_preview_packets/reports/"
    "bereishis_perek_4_broad_vocabulary_final_observation_evidence_2026_04_30.json"
)

EXPECTED_INCLUDED = {
    "svqcl_p4_001",
    "svqcl_p4_002",
    "svqcl_p4_003",
    "svqcl_p4_005",
    "svqcl_p4_006",
}

EXPECTED_BLOCKED_REVISION = {"bsvb_p4_002", "svqcl_p4_004"}
EXPECTED_BLOCKED_HELD = {"bsvb_p4_003", "bsvb_p4_004", "svqcl_p4_007", "svqcl_p4_008", "svqcl_p4_009"}
EXPECTED_BLOCKED = EXPECTED_BLOCKED_REVISION | EXPECTED_BLOCKED_HELD

FORBIDDEN_PHRASES = (
    "reviewed bank promoted",
    "runtime active",
    "runtime activated",
    "student-facing released",
    "mastery proven",
    "source truth changed",
)

FALSE_FIELDS = (
    "reviewed_bank_promoted",
    "reviewed_bank_entries_created",
    "runtime_scope_widened",
    "perek_activated",
    "runtime_questions_created",
    "student_facing_content_created",
    "source_truth_changed",
)


def _fail(message: str) -> None:
    raise SystemExit(f"Perek 4 broad vocabulary reviewed-bank candidate planning validation failed: {message}")


def _read_text(path: Path) -> str:
    if not path.exists():
        _fail(f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _json(path: Path) -> dict:
    try:
        return json.loads(_read_text(path))
    except json.JSONDecodeError as exc:
        _fail(f"invalid JSON {path.relative_to(ROOT)}: {exc}")


def _require_false(payload: dict, path: Path) -> None:
    for field in FALSE_FIELDS:
        if payload.get(field) is not False:
            _fail(f"{path.relative_to(ROOT)} must keep {field}=false")


def validate() -> None:
    required_paths = [
        PLANNING_TSV,
        PLANNING_JSON,
        EVIDENCE_MD,
        EVIDENCE_JSON,
        BLOCKED_MD,
        BLOCKED_JSON,
        REPORT_MD,
        REPORT_JSON,
        NEXT_PROMPT,
    ]
    for path in required_paths:
        if not path.exists():
            _fail(f"missing required file: {path.relative_to(ROOT)}")

    rows = _rows(PLANNING_TSV)
    planning_payload = _json(PLANNING_JSON)
    evidence_payload = _json(EVIDENCE_JSON)
    blocked_payload = _json(BLOCKED_JSON)
    report_payload = _json(REPORT_JSON)

    if len(rows) != 5:
        _fail("candidate planning TSV must contain exactly five rows")
    if {row.get("source_candidate_id") for row in rows} != EXPECTED_INCLUDED:
        _fail("candidate planning TSV included source IDs mismatch")
    if EXPECTED_BLOCKED & {row.get("source_candidate_id") for row in rows}:
        _fail("blocked/revision rows must not be included as candidate rows")

    for row in rows:
        source_id = row.get("source_candidate_id", "")
        if row.get("evidence_status") != "internally_observed_and_supported":
            _fail(f"{source_id} evidence_status mismatch")
        if row.get("candidate_planning_status") != "ready_for_yossi_reviewed_bank_decision_packet":
            _fail(f"{source_id} candidate_planning_status mismatch")
        if row.get("reviewed_bank_status") != "not_reviewed_bank":
            _fail(f"{source_id} reviewed_bank_status must be not_reviewed_bank")
        if row.get("runtime_status") != "not_runtime":
            _fail(f"{source_id} runtime_status must be not_runtime")
        if row.get("student_facing_status") != "not_student_facing":
            _fail(f"{source_id} student_facing_status must be not_student_facing")
        if row.get("required_next_decision") != "yossi_reviewed_bank_decision_required":
            _fail(f"{source_id} required_next_decision mismatch")

    if planning_payload.get("planning_type") != "perek_4_broad_vocabulary_reviewed_bank_candidate_planning":
        _fail("planning JSON planning_type mismatch")
    if planning_payload.get("planning_only") is not True:
        _fail("planning JSON must set planning_only=true")
    if planning_payload.get("candidate_count") != 5:
        _fail("planning JSON candidate_count must be 5")
    if set(planning_payload.get("included_candidate_ids", [])) != EXPECTED_INCLUDED:
        _fail("planning JSON included_candidate_ids mismatch")
    if set(planning_payload.get("excluded_revision_required_ids", [])) != EXPECTED_BLOCKED_REVISION:
        _fail("planning JSON excluded_revision_required_ids mismatch")
    if set(planning_payload.get("excluded_held_ids", [])) != EXPECTED_BLOCKED_HELD:
        _fail("planning JSON excluded_held_ids mismatch")
    if planning_payload.get("ready_for_reviewed_bank_decision_packet") is not True:
        _fail("planning JSON must set ready_for_reviewed_bank_decision_packet=true")
    if planning_payload.get("ready_for_reviewed_bank_promotion") is not False:
        _fail("planning JSON must keep ready_for_reviewed_bank_promotion=false")
    if planning_payload.get("ready_for_runtime_activation") is not False:
        _fail("planning JSON must keep ready_for_runtime_activation=false")
    if planning_payload.get("runtime_activation_authorized") is not False:
        _fail("planning JSON must keep runtime_activation_authorized=false")
    _require_false(planning_payload, PLANNING_JSON)

    if evidence_payload.get("final_observation_evidence_path") != FINAL_OBSERVATION_JSON:
        _fail("evidence map JSON must reference final observation evidence")
    evidence_items = evidence_payload.get("items")
    if not isinstance(evidence_items, list) or len(evidence_items) != 5:
        _fail("evidence map JSON must contain exactly five item rows")
    if {item.get("source_candidate_id") for item in evidence_items if isinstance(item, dict)} != EXPECTED_INCLUDED:
        _fail("evidence map JSON included IDs mismatch")
    if FINAL_OBSERVATION_JSON not in _read_text(EVIDENCE_MD):
        _fail("evidence map Markdown must reference final observation evidence")
    _require_false(evidence_payload, EVIDENCE_JSON)

    blocked_items = blocked_payload.get("items")
    if not isinstance(blocked_items, list) or len(blocked_items) != 7:
        _fail("blocked register JSON must contain seven blocked rows")
    blocked_ids = {item.get("source_candidate_id") for item in blocked_items if isinstance(item, dict)}
    if blocked_ids != EXPECTED_BLOCKED:
        _fail("blocked register JSON blocked IDs mismatch")
    if {item.get("source_candidate_id") for item in blocked_items if item.get("block_type") == "revision_required"} != EXPECTED_BLOCKED_REVISION:
        _fail("blocked register JSON revision-required IDs mismatch")
    if {item.get("source_candidate_id") for item in blocked_items if item.get("block_type") == "held"} != EXPECTED_BLOCKED_HELD:
        _fail("blocked register JSON held IDs mismatch")
    _require_false(blocked_payload, BLOCKED_JSON)

    if report_payload.get("feature_name") != "perek_4_broad_vocabulary_reviewed_bank_candidate_planning":
        _fail("main report JSON feature_name mismatch")
    if report_payload.get("planning_only") is not True:
        _fail("main report JSON must set planning_only=true")
    if report_payload.get("reviewed_bank_candidate_planning_created") is not True:
        _fail("main report JSON must set reviewed_bank_candidate_planning_created=true")
    if report_payload.get("candidate_count") != 5:
        _fail("main report JSON candidate_count must be 5")
    if report_payload.get("ready_for_reviewed_bank_decision_packet") is not True:
        _fail("main report JSON must set ready_for_reviewed_bank_decision_packet=true")
    if report_payload.get("ready_for_reviewed_bank_promotion") is not False:
        _fail("main report JSON must keep ready_for_reviewed_bank_promotion=false")
    if report_payload.get("ready_for_runtime_activation") is not False:
        _fail("main report JSON must keep ready_for_runtime_activation=false")
    if report_payload.get("runtime_activation_authorized") is not False:
        _fail("main report JSON must keep runtime_activation_authorized=false")
    for field in FALSE_FIELDS + ("runtime_content_promoted", "fake_teacher_approval_created", "fake_observation_evidence_created", "raw_logs_exposed", "validators_weakened"):
        if report_payload.get(field) is not False:
            _fail(f"main report JSON must keep {field}=false")

    next_prompt = _read_text(NEXT_PROMPT)
    for option in [
        "approve_for_reviewed_bank",
        "approve_with_revision_before_reviewed_bank",
        "hold_for_follow_up",
        "reject_for_reviewed_bank",
    ]:
        if option not in next_prompt:
            _fail(f"next prompt missing decision option: {option}")

    scanned = "\n".join(_read_text(path).lower() for path in required_paths)
    for phrase in FORBIDDEN_PHRASES:
        if phrase in scanned:
            _fail(f"forbidden phrase found in artifacts: {phrase}")

    print("Perek 4 broad vocabulary reviewed-bank candidate planning validation passed.")


if __name__ == "__main__":
    validate()
