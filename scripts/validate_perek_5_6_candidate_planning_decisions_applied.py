from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DISCOVERY = ROOT / "data" / "gate_2_source_discovery"
REPORT = DISCOVERY / "reports"
PPC = ROOT / "data" / "gate_2_protected_preview_candidates"
PIPELINE = ROOT / "data" / "pipeline_rounds"

DECISIONS_MD = REPORT / "bereishis_perek_5_6_candidate_planning_decisions_applied_2026_04_29.md"
DECISIONS_JSON = REPORT / "bereishis_perek_5_6_candidate_planning_decisions_applied_2026_04_29.json"
CHECKLIST_MD = REPORT / "bereishis_perek_5_6_candidate_planning_review_checklist_2026_04_29.md"
CHECKLIST_JSON = REPORT / "bereishis_perek_5_6_candidate_planning_review_checklist_2026_04_29.json"
READINESS_MD = PIPELINE / "bereishis_perek_5_6_candidate_planning_decisions_next_gate_readiness_2026_04_29.md"
FUTURE_PROMPT = PIPELINE / "prompts" / "bereishis_perek_5_6_protected_preview_candidate_review_decisions_prompt.md"
REVIEW_TSV = PPC / "bereishis_perek_5_6_protected_preview_candidate_review.tsv"

EXPECTED_ADVANCING_IDS = [
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
EXPECTED_COUNTS = {
    "advance_to_protected_preview_candidate_review": 2,
    "advance_with_minor_revision": 5,
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
    required = [DECISIONS_MD, DECISIONS_JSON, CHECKLIST_MD, CHECKLIST_JSON, READINESS_MD, FUTURE_PROMPT]
    for path in required:
        require(path, errors)
    if errors:
        return {"valid": False, "errors": errors}

    try:
        payload = read_json(DECISIONS_JSON)
        checklist = read_json(CHECKLIST_JSON)
    except json.JSONDecodeError as error:
        return {"valid": False, "errors": [f"invalid JSON: {error}"]}

    decisions = payload.get("decisions", [])
    if len(decisions) != 7:
        errors.append(f"expected 7 decisions, found {len(decisions)}")
    if [decision.get("candidate_id") for decision in decisions] != EXPECTED_ADVANCING_IDS:
        errors.append("decision candidate IDs do not match the seven advancing candidates")
    counts = Counter(decision.get("planning_review_decision") for decision in decisions)
    if {key: counts.get(key, 0) for key in EXPECTED_COUNTS} != EXPECTED_COUNTS:
        errors.append("planning decision counts do not match expected counts")
    if payload.get("decision_counts") != EXPECTED_COUNTS:
        errors.append("decision_counts JSON does not match expected counts")

    excluded = payload.get("excluded_candidates", [])
    if [candidate.get("candidate_id") for candidate in excluded] != EXPECTED_EXCLUDED_IDS:
        errors.append("excluded candidate list must contain exactly the five excluded candidates")
    for candidate in excluded:
        if candidate.get("eligible_for_protected_preview_candidate_review") is not False:
            errors.append(f"{candidate.get('candidate_id')}: excluded candidate must not be eligible")

    for decision in decisions:
        candidate_id = decision.get("candidate_id", "<missing>")
        if decision.get("eligible_for_protected_preview_candidate_review") is not True:
            errors.append(f"{candidate_id}: advancing decision must be eligible for review layer")
        for field in FALSE_FIELDS:
            if decision.get(field) is not False:
                errors.append(f"{candidate_id}: {field} must be false")

    checklist_candidates = checklist.get("candidates", [])
    if [candidate.get("candidate_id") for candidate in checklist_candidates] != EXPECTED_ADVANCING_IDS:
        errors.append("updated checklist candidates must remain the seven advancing candidates")
    for candidate in checklist_candidates:
        if candidate.get("planning_review_decision") not in EXPECTED_COUNTS:
            errors.append(f"{candidate.get('candidate_id')}: checklist decision is missing or unexpected")
        for field in FALSE_FIELDS:
            if candidate.get(field) is not False:
                errors.append(f"{candidate.get('candidate_id')}: checklist {field} must be false")

    if REVIEW_TSV.exists():
        rows = read_tsv(REVIEW_TSV)
        if [row.get("candidate_id") for row in rows] != EXPECTED_ADVANCING_IDS:
            errors.append("review layer must include exactly the seven advancing candidates")
        for row in rows:
            if row.get("candidate_id") in EXPECTED_EXCLUDED_IDS:
                errors.append("review layer includes an excluded candidate")
            for field in FALSE_FIELDS:
                if row.get(field) != "false":
                    errors.append(f"{row.get('candidate_id')}: review TSV {field} must be false")

    check_text(required + ([REVIEW_TSV] if REVIEW_TSV.exists() else []), errors)
    return {
        "valid": not errors,
        "decision_count": len(decisions),
        "excluded_count": len(excluded),
        "review_layer_exists": REVIEW_TSV.exists(),
        "errors": errors,
    }


def main() -> int:
    result = validate()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
