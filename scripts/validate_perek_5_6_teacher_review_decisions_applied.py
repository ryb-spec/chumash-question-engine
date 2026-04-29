from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "data" / "gate_2_source_discovery" / "reports"
DECISIONS_MD = REPORT_DIR / "bereishis_perek_5_6_teacher_review_decisions_applied_2026_04_29.md"
DECISIONS_JSON = REPORT_DIR / "bereishis_perek_5_6_teacher_review_decisions_applied_2026_04_29.json"
CHECKLIST_MD = REPORT_DIR / "bereishis_perek_5_6_compressed_teacher_review_checklist_2026_04_29.md"
CHECKLIST_JSON = REPORT_DIR / "bereishis_perek_5_6_compressed_teacher_review_checklist_2026_04_29.json"
DECISION_TEMPLATE = ROOT / "data" / "gate_2_source_discovery" / "bereishis_perek_5_6_teacher_review_decision_template.tsv"
READINESS_MD = ROOT / "data" / "pipeline_rounds" / "bereishis_perek_5_6_post_teacher_review_next_gate_readiness_2026_04_29.md"
REGISTER_MD = REPORT_DIR / "bereishis_perek_5_6_hold_source_followup_register_2026_04_29.md"
FUTURE_PROMPT = ROOT / "data" / "pipeline_rounds" / "prompts" / "bereishis_perek_5_6_candidate_planning_review_prompt.md"
PLANNING_TSV = ROOT / "data" / "gate_2_source_discovery" / "bereishis_perek_5_6_candidate_planning.tsv"

EXPECTED_COUNTS = {
    "approve_for_next_candidate_planning": 2,
    "approve_with_revision": 5,
    "hold_for_spacing_or_balance": 2,
    "needs_source_follow_up": 2,
    "source_only": 1,
    "reject": 0,
}
ELIGIBLE_IDS = {
    "g2srcdisc_p5_001",
    "g2srcdisc_p5_002",
    "g2srcdisc_p5_005",
    "g2srcdisc_p6_001",
    "g2srcdisc_p6_003",
    "g2srcdisc_p6_006",
    "g2srcdisc_p6_007",
}
BLOCKED_IDS = {
    "g2srcdisc_p5_003",
    "g2srcdisc_p5_004",
    "g2srcdisc_p6_002",
    "g2srcdisc_p6_004",
    "g2srcdisc_p6_005",
}
FORBIDDEN_SNIPPETS = (
    "runtime_allowed=true",
    "runtime_allowed: true",
    '"runtime_allowed": true',
    "reviewed_bank_allowed=true",
    "reviewed_bank_allowed: true",
    '"reviewed_bank_allowed": true',
    "protected_preview_allowed=true",
    "protected_preview_allowed: true",
    '"protected_preview_allowed": true',
    "student_facing_allowed=true",
    "student_facing_allowed: true",
    '"student_facing_allowed": true',
    "promoted_to_runtime",
    "approved_for_runtime",
    "Perek 5 is runtime active",
    "Perek 6 is runtime active",
    "Perek 5 runtime activation occurred",
    "Perek 6 runtime activation occurred",
)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def require_file(path: Path, errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"missing required artifact: {path.relative_to(ROOT)}")


def check_false_flags(record: dict, context: str, errors: list[str]) -> None:
    for key in (
        "runtime_allowed",
        "reviewed_bank_allowed",
        "protected_preview_allowed",
        "student_facing_allowed",
        "perek_5_activated",
        "perek_6_activated",
    ):
        if record.get(key) is not False:
            errors.append(f"{context}: {key} must be false")


def check_text_safety(paths: list[Path], errors: list[str]) -> None:
    for path in paths:
        if not path.exists():
            continue
        lowered = path.read_text(encoding="utf-8").lower()
        for snippet in FORBIDDEN_SNIPPETS:
            if snippet.lower() in lowered:
                errors.append(f"{path.relative_to(ROOT)} contains forbidden snippet: {snippet}")


def validate() -> dict:
    errors: list[str] = []
    required = [
        DECISIONS_MD,
        DECISIONS_JSON,
        CHECKLIST_MD,
        CHECKLIST_JSON,
        DECISION_TEMPLATE,
        READINESS_MD,
        REGISTER_MD,
        FUTURE_PROMPT,
    ]
    for path in required:
        require_file(path, errors)
    if errors:
        return {"valid": False, "errors": errors}

    try:
        payload = read_json(DECISIONS_JSON)
        checklist = read_json(CHECKLIST_JSON)
    except json.JSONDecodeError as error:
        return {"valid": False, "errors": [f"invalid JSON: {error}"]}

    decisions = payload.get("decisions", [])
    if len(decisions) != 12:
        errors.append(f"expected exactly 12 decisions, found {len(decisions)}")

    counts = Counter(decision.get("teacher_decision") for decision in decisions)
    for key, expected in EXPECTED_COUNTS.items():
        if counts.get(key, 0) != expected:
            errors.append(f"decision count mismatch for {key}: expected {expected}, found {counts.get(key, 0)}")
    if payload.get("decision_counts") != EXPECTED_COUNTS:
        errors.append("decision_counts payload does not match expected counts")

    ids = {decision.get("candidate_id") for decision in decisions}
    if ids != ELIGIBLE_IDS | BLOCKED_IDS:
        errors.append(f"unexpected decision candidate IDs: {sorted(ids)}")

    eligible = {
        decision["candidate_id"]
        for decision in decisions
        if decision.get("eligible_for_next_candidate_planning") is True
    }
    if eligible != ELIGIBLE_IDS:
        errors.append(f"eligible candidate mismatch: {sorted(eligible)}")

    for decision in decisions:
        candidate_id = decision.get("candidate_id", "<missing>")
        check_false_flags(decision, candidate_id, errors)
        if candidate_id in BLOCKED_IDS and decision.get("eligible_for_next_candidate_planning"):
            errors.append(f"{candidate_id}: held/source/follow-up candidate must not be eligible")

    checklist_candidates = checklist.get("candidates", [])
    if len(checklist_candidates) != 12:
        errors.append(f"checklist should still contain 12 candidates, found {len(checklist_candidates)}")
    for candidate in checklist_candidates:
        candidate_id = candidate.get("candidate_id", "<missing>")
        if candidate.get("teacher_decision") is None:
            errors.append(f"{candidate_id}: checklist teacher_decision must be filled")
        check_false_flags(candidate, f"checklist {candidate_id}", errors)

    template_rows = read_tsv(DECISION_TEMPLATE)
    if len(template_rows) != 12:
        errors.append(f"decision template should contain 12 rows, found {len(template_rows)}")
    for row in template_rows:
        candidate_id = row.get("candidate_id", "<missing>")
        if not row.get("teacher_decision", "").strip():
            errors.append(f"{candidate_id}: decision template teacher_decision must be filled")

    if PLANNING_TSV.exists():
        planning_rows = read_tsv(PLANNING_TSV)
        planning_ids = {row.get("candidate_id") for row in planning_rows}
        if planning_ids != ELIGIBLE_IDS:
            errors.append(f"candidate-planning TSV must include exactly eligible candidates, found {sorted(planning_ids)}")
        if planning_ids & BLOCKED_IDS:
            errors.append("candidate-planning TSV includes held/source/follow-up candidate")
        for row in planning_rows:
            candidate_id = row.get("candidate_id", "<missing>")
            for key in (
                "runtime_allowed",
                "reviewed_bank_allowed",
                "protected_preview_allowed",
                "student_facing_allowed",
                "perek_5_activated",
                "perek_6_activated",
            ):
                if row.get(key) != "false":
                    errors.append(f"candidate-planning TSV {candidate_id}: {key} must be false")

    text_paths = required + ([PLANNING_TSV] if PLANNING_TSV.exists() else [])
    check_text_safety(text_paths, errors)
    return {
        "valid": not errors,
        "decision_count": len(decisions),
        "eligible_count": len(eligible),
        "candidate_planning_tsv_exists": PLANNING_TSV.exists(),
        "errors": errors,
    }


def main() -> int:
    result = validate()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
