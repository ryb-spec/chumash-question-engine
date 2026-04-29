from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DISCOVERY_DIR = ROOT / "data" / "gate_2_source_discovery"
REPORT_DIR = DISCOVERY_DIR / "reports"
PIPELINE_DIR = ROOT / "data" / "pipeline_rounds"

INVENTORY = DISCOVERY_DIR / "bereishis_perek_5_6_review_only_safe_candidate_inventory.tsv"
CHECKLIST_MD = REPORT_DIR / "bereishis_perek_5_6_compressed_teacher_review_checklist_2026_04_29.md"
CHECKLIST_JSON = REPORT_DIR / "bereishis_perek_5_6_compressed_teacher_review_checklist_2026_04_29.json"
READINESS_MD = PIPELINE_DIR / "bereishis_perek_5_6_teacher_review_checklist_readiness_2026_04_29.md"
DECISION_TEMPLATE = DISCOVERY_DIR / "bereishis_perek_5_6_teacher_review_decision_template.tsv"
APPLY_PROMPT = PIPELINE_DIR / "prompts" / "bereishis_perek_5_6_teacher_review_decisions_apply_prompt.md"
DECISIONS_APPLIED_JSON = REPORT_DIR / "bereishis_perek_5_6_teacher_review_decisions_applied_2026_04_29.json"

ALLOWED_DECISIONS = {
    "approve_for_next_candidate_planning",
    "approve_with_revision",
    "needs_source_follow_up",
    "hold_for_spacing_or_balance",
    "reject",
    "source_only",
}
FALSE_FIELDS = [
    "runtime_allowed",
    "reviewed_bank_allowed",
    "protected_preview_allowed",
    "student_facing_allowed",
    "perek_5_activated",
    "perek_6_activated",
]
FORBIDDEN_COMPACT = [
    "runtime_allowed=true",
    "reviewed_bank_allowed=true",
    "protected_preview_allowed=true",
    "student_facing_allowed=true",
]
FORBIDDEN_TEXT = [
    "promoted_to_runtime",
    "approved_for_runtime",
    "Perek 5 is runtime-active",
    "Perek 6 is runtime-active",
    "protected-preview packet created",
    "fake teacher decisions created",
]


def _fail(message: str) -> None:
    raise SystemExit(message)


def _read(path: Path) -> str:
    if not path.exists():
        _fail(f"Missing required artifact: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def _load_json(path: Path) -> dict:
    try:
        return json.loads(_read(path))
    except json.JSONDecodeError as exc:
        _fail(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}")


def _read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        _fail(f"Missing required artifact: {path.relative_to(ROOT)}")
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _scan_forbidden(paths: list[Path]) -> None:
    for path in paths:
        text = _read(path)
        compact = text.replace(" ", "").lower()
        lowered = text.lower()
        for token in FORBIDDEN_COMPACT:
            if token in compact:
                _fail(f"Forbidden positive gate value in {path.relative_to(ROOT)}: {token}")
        for token in FORBIDDEN_TEXT:
            if token.lower() in lowered:
                _fail(f"Forbidden runtime/promotion/decision claim in {path.relative_to(ROOT)}: {token}")


def validate() -> None:
    required = [CHECKLIST_MD, CHECKLIST_JSON, READINESS_MD, DECISION_TEMPLATE, APPLY_PROMPT, INVENTORY]
    for path in required:
        _read(path)

    inventory_rows = _read_tsv(INVENTORY)
    checklist = _load_json(CHECKLIST_JSON)
    decisions_applied = _load_json(DECISIONS_APPLIED_JSON) if DECISIONS_APPLIED_JSON.exists() else None
    applied_decisions_by_id = {}
    if decisions_applied is not None:
        applied_decisions_by_id = {
            decision.get("candidate_id"): decision
            for decision in decisions_applied.get("decisions", [])
        }
    candidates = checklist.get("candidates")
    if checklist.get("checklist_status") != "teacher_review_only":
        _fail("Checklist status must be teacher_review_only.")
    if not isinstance(candidates, list):
        _fail("Checklist JSON candidates must be a list.")
    if checklist.get("total_candidate_count") != len(inventory_rows):
        _fail("Checklist total_candidate_count must match source inventory.")
    if len(inventory_rows) == 12 and checklist.get("total_candidate_count") != 12:
        _fail("Expected 12 checklist candidates for the current inventory.")
    if set(checklist.get("allowed_teacher_decisions", [])) != ALLOWED_DECISIONS:
        _fail("Allowed teacher decisions do not match expected values.")

    inventory_ids = {row["candidate_id"] for row in inventory_rows}
    candidate_ids = {candidate.get("candidate_id") for candidate in candidates}
    if candidate_ids != inventory_ids:
        _fail("Checklist candidate IDs must match source inventory candidate IDs.")

    for candidate in candidates:
        cid = candidate.get("candidate_id")
        if candidate.get("teacher_review_needed") is not True:
            _fail(f"{cid} must have teacher_review_needed=true.")
        if decisions_applied is None:
            if candidate.get("teacher_decision") is not None:
                _fail(f"{cid} must have teacher_decision=null.")
            if candidate.get("teacher_notes") != "":
                _fail(f"{cid} must have blank teacher_notes.")
        else:
            applied = applied_decisions_by_id.get(cid)
            if not applied:
                _fail(f"{cid} missing from decision-applied artifact.")
            if candidate.get("teacher_decision") != applied.get("teacher_decision"):
                _fail(f"{cid} checklist decision must match decision-applied artifact.")
        for field in FALSE_FIELDS:
            if candidate.get(field) is not False:
                _fail(f"{cid} must keep {field}=false.")

    template_rows = _read_tsv(DECISION_TEMPLATE)
    if len(template_rows) != len(inventory_rows):
        _fail("Decision template row count must match source inventory.")
    for row in template_rows:
        cid = row.get("candidate_id")
        if decisions_applied is None:
            if row.get("teacher_decision", "") != "":
                _fail(f"Decision template teacher_decision must be blank for {cid}.")
        else:
            applied = applied_decisions_by_id.get(cid)
            if not applied:
                _fail(f"{cid} missing from decision-applied artifact.")
            if row.get("teacher_decision", "") != applied.get("teacher_decision"):
                _fail(f"Decision template teacher_decision must match decision-applied artifact for {cid}.")
        values = set(row.get("allowed_decision_values", "").split("|"))
        if values != ALLOWED_DECISIONS:
            _fail(f"Decision template allowed values mismatch for {cid}.")

    md = _read(CHECKLIST_MD)
    for phrase in [
        "teacher-review checklist only",
        "No runtime activation",
        "No active scope expansion",
        "No reviewed-bank promotion",
        "No protected-preview packet",
        "No student-facing content",
    ]:
        if phrase not in md:
            _fail(f"Checklist Markdown missing required status phrase: {phrase}")

    prompt = _read(APPLY_PROMPT)
    if "Stop if teacher decisions are missing." not in prompt:
        _fail("Future apply prompt must stop if teacher decisions are missing.")
    if "Do not invent decisions" not in prompt:
        _fail("Future apply prompt must prohibit invented decisions.")

    _scan_forbidden(required)
    print("Perek 5-6 teacher-review checklist validation passed.")


if __name__ == "__main__":
    validate()
