from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DISCOVERY = ROOT / "data" / "gate_2_source_discovery"
REPORT = DISCOVERY / "reports"
PIPELINE = ROOT / "data" / "pipeline_rounds"

CHECKLIST_MD = REPORT / "bereishis_perek_5_6_candidate_planning_review_checklist_2026_04_29.md"
CHECKLIST_JSON = REPORT / "bereishis_perek_5_6_candidate_planning_review_checklist_2026_04_29.json"
READINESS_MD = PIPELINE / "bereishis_perek_5_6_candidate_planning_review_checklist_readiness_2026_04_29.md"
FUTURE_PROMPT = PIPELINE / "prompts" / "bereishis_perek_5_6_candidate_planning_decisions_apply_prompt.md"
PLANNING_TSV = DISCOVERY / "bereishis_perek_5_6_candidate_planning.tsv"

EXPECTED_ELIGIBLE_IDS = [
    "g2srcdisc_p5_001",
    "g2srcdisc_p5_002",
    "g2srcdisc_p5_005",
    "g2srcdisc_p6_001",
    "g2srcdisc_p6_003",
    "g2srcdisc_p6_006",
    "g2srcdisc_p6_007",
]
EXPECTED_EXCLUDED_IDS = [
    "g2srcdisc_p5_003",
    "g2srcdisc_p5_004",
    "g2srcdisc_p6_002",
    "g2srcdisc_p6_004",
    "g2srcdisc_p6_005",
]
ALLOWED_PLANNING_DECISIONS = {
    "advance_to_protected_preview_candidate_review",
    "advance_with_minor_revision",
    "hold_for_spacing_or_balance",
    "needs_source_follow_up",
    "reject",
    "source_only",
}
FALSE_FIELDS = (
    "runtime_allowed",
    "reviewed_bank_allowed",
    "protected_preview_allowed",
    "student_facing_allowed",
    "perek_5_activated",
    "perek_6_activated",
)
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
    "protected-preview packet has been created",
    "fake teacher decisions",
)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def require(path: Path, errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"missing required artifact: {path.relative_to(ROOT)}")


def check_text(paths: list[Path], errors: list[str]) -> None:
    for path in paths:
        if not path.exists():
            continue
        lowered = path.read_text(encoding="utf-8").lower()
        for snippet in FORBIDDEN_SNIPPETS:
            if snippet.lower() in lowered:
                errors.append(f"{path.relative_to(ROOT)} contains forbidden snippet: {snippet}")


def validate() -> dict:
    errors: list[str] = []
    required = [CHECKLIST_MD, CHECKLIST_JSON, READINESS_MD, FUTURE_PROMPT, PLANNING_TSV]
    for path in required:
        require(path, errors)
    if errors:
        return {"valid": False, "errors": errors}

    try:
        checklist = read_json(CHECKLIST_JSON)
    except json.JSONDecodeError as error:
        return {"valid": False, "errors": [f"invalid JSON: {error}"]}

    if checklist.get("checklist_status") != "candidate_planning_review_only":
        errors.append("checklist_status must be candidate_planning_review_only")
    if checklist.get("eligible_candidate_count") != 7:
        errors.append("eligible_candidate_count must be 7")
    if checklist.get("excluded_candidate_count") != 5:
        errors.append("excluded_candidate_count must be 5")
    if checklist.get("eligible_candidate_ids") != EXPECTED_ELIGIBLE_IDS:
        errors.append("eligible_candidate_ids do not match expected IDs")
    if checklist.get("excluded_candidate_ids") != EXPECTED_EXCLUDED_IDS:
        errors.append("excluded_candidate_ids do not match expected IDs")
    if set(checklist.get("allowed_planning_decisions", [])) != ALLOWED_PLANNING_DECISIONS:
        errors.append("allowed_planning_decisions do not match expected values")

    candidates = checklist.get("candidates")
    if not isinstance(candidates, list):
        errors.append("candidates must be a list")
        candidates = []
    if len(candidates) != 7:
        errors.append(f"expected 7 checklist candidates, found {len(candidates)}")
    candidate_ids = [candidate.get("candidate_id") for candidate in candidates]
    if candidate_ids != EXPECTED_ELIGIBLE_IDS:
        errors.append("candidate list must contain exactly the eligible IDs in expected order")

    for candidate in candidates:
        candidate_id = candidate.get("candidate_id", "<missing>")
        if candidate.get("planning_review_decision") is not None:
            errors.append(f"{candidate_id}: planning_review_decision must be null")
        if candidate.get("planning_review_notes") != "":
            errors.append(f"{candidate_id}: planning_review_notes must be blank")
        for field in FALSE_FIELDS:
            if candidate.get(field) is not False:
                errors.append(f"{candidate_id}: {field} must be false")

    planning_rows = read_tsv(PLANNING_TSV)
    planning_ids = [row.get("candidate_id") for row in planning_rows]
    if planning_ids != EXPECTED_ELIGIBLE_IDS:
        errors.append("source candidate-planning TSV must contain exactly the eligible IDs")
    for row in planning_rows:
        for field in FALSE_FIELDS:
            if row.get(field) != "false":
                errors.append(f"{row.get('candidate_id')}: planning TSV {field} must be false")

    md = CHECKLIST_MD.read_text(encoding="utf-8")
    for excluded_id in EXPECTED_EXCLUDED_IDS:
        if excluded_id not in md:
            errors.append(f"checklist Markdown missing excluded ID {excluded_id}")
    if "planning_review_decision" not in md and "Planning review decision:" not in md:
        errors.append("checklist Markdown must include blank planning-review decision fields")

    prompt = FUTURE_PROMPT.read_text(encoding="utf-8")
    if "Stop if any required planning decisions are missing." not in prompt:
        errors.append("future prompt must stop if decisions are missing")
    if "Keep runtime, reviewed-bank, protected-preview, and student-facing permission fields false." not in prompt:
        errors.append("future prompt must keep all gates false")

    check_text(required, errors)
    return {
        "valid": not errors,
        "eligible_candidate_count": len(candidates),
        "excluded_candidate_count": len(EXPECTED_EXCLUDED_IDS),
        "errors": errors,
    }


def main() -> int:
    result = validate()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
