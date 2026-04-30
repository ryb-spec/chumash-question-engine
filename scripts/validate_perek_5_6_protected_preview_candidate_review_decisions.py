from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PPC = ROOT / "data" / "gate_2_protected_preview_candidates"
PPC_REPORTS = PPC / "reports"
PIPELINE = ROOT / "data" / "pipeline_rounds"
PACKET_REPORTS = ROOT / "data" / "gate_2_protected_preview_packets" / "reports"

DECISIONS_MD = PPC_REPORTS / "bereishis_perek_5_6_protected_preview_candidate_review_decisions_applied_2026_04_29.md"
DECISIONS_JSON = PPC_REPORTS / "bereishis_perek_5_6_protected_preview_candidate_review_decisions_applied_2026_04_29.json"
REVIEW_TSV = PPC / "bereishis_perek_5_6_protected_preview_candidate_review.tsv"
READINESS_MD = PIPELINE / "bereishis_perek_5_6_internal_protected_preview_packet_readiness_2026_04_29.md"
FUTURE_PROMPT = PIPELINE / "prompts" / "bereishis_perek_5_6_internal_protected_preview_packet_prompt.md"
PLANNING_ONLY = PACKET_REPORTS / "bereishis_perek_5_6_internal_protected_preview_packet_planning_2026_04_29.md"
PACKET_TSV = ROOT / "data" / "gate_2_protected_preview_packets" / "bereishis_perek_5_6_internal_protected_preview_packet.tsv"

EXPECTED_IDS = [
    "g2srcdisc_p5_001",
    "g2srcdisc_p5_002",
    "g2srcdisc_p5_005",
    "g2srcdisc_p6_001",
    "g2srcdisc_p6_003",
    "g2srcdisc_p6_006",
    "g2srcdisc_p6_007",
]
EXPECTED_EXCLUDED = [
    "g2srcdisc_p5_003",
    "g2srcdisc_p5_004",
    "g2srcdisc_p6_002",
    "g2srcdisc_p6_004",
    "g2srcdisc_p6_005",
]
EXPECTED_COUNTS = {
    "approve_for_internal_protected_preview_packet": 2,
    "approve_with_revision": 5,
    "needs_follow_up": 0,
    "reject": 0,
    "source_only": 0,
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
    required = [DECISIONS_MD, DECISIONS_JSON, REVIEW_TSV, READINESS_MD, FUTURE_PROMPT, PLANNING_ONLY]
    for path in required:
        require(path, errors)
    if errors:
        return {"valid": False, "errors": errors}

    try:
        payload = read_json(DECISIONS_JSON)
    except json.JSONDecodeError as error:
        return {"valid": False, "errors": [f"invalid JSON: {error}"]}

    decisions = payload.get("decisions", [])
    if len(decisions) != 7:
        errors.append(f"expected seven decisions, found {len(decisions)}")
    if [decision.get("candidate_id") for decision in decisions] != EXPECTED_IDS:
        errors.append("decision IDs do not match expected seven candidates")
    counts = Counter(decision.get("review_decision") for decision in decisions)
    if {key: counts.get(key, 0) for key in EXPECTED_COUNTS} != EXPECTED_COUNTS:
        errors.append("decision counts do not match expected values")
    if payload.get("decision_counts") != EXPECTED_COUNTS:
        errors.append("decision_counts JSON does not match expected values")
    if payload.get("clean_approved_count") != 2:
        errors.append("clean_approved_count must be 2")
    if payload.get("approve_with_revision_count") != 5:
        errors.append("approve_with_revision_count must be 5")
    if payload.get("excluded_candidate_count") != 5:
        errors.append("excluded_candidate_count must be 5")

    clean = [decision["candidate_id"] for decision in decisions if decision.get("clean_ready_for_internal_packet")]
    if clean != ["g2srcdisc_p5_001", "g2srcdisc_p5_005"]:
        errors.append("clean-approved candidates do not match expected IDs")
    revision = [decision["candidate_id"] for decision in decisions if decision.get("revision_required")]
    if revision != ["g2srcdisc_p5_002", "g2srcdisc_p6_001", "g2srcdisc_p6_003", "g2srcdisc_p6_006", "g2srcdisc_p6_007"]:
        errors.append("approve-with-revision candidates do not match expected IDs")

    for decision in decisions:
        candidate_id = decision.get("candidate_id", "<missing>")
        for field in FALSE_FIELDS:
            if decision.get(field) is not False:
                errors.append(f"{candidate_id}: {field} must be false")

    rows = read_tsv(REVIEW_TSV)
    if [row.get("candidate_id") for row in rows] != EXPECTED_IDS:
        errors.append("review TSV must contain exactly the seven expected candidates")
    if set(EXPECTED_EXCLUDED) & {row.get("candidate_id") for row in rows}:
        errors.append("review TSV includes an excluded candidate")
    for row in rows:
        candidate_id = row.get("candidate_id", "<missing>")
        for field in FALSE_FIELDS:
            if row.get(field) != "false":
                errors.append(f"{candidate_id}: review TSV {field} must be false")

    for excluded_id in EXPECTED_EXCLUDED:
        if excluded_id in REVIEW_TSV.read_text(encoding="utf-8"):
            errors.append(f"excluded candidate leaked into review TSV: {excluded_id}")
    if PACKET_TSV.exists():
        errors.append(f"internal packet TSV must not be created in this task: {PACKET_TSV.relative_to(ROOT)}")

    check_text(required, errors)
    return {
        "valid": not errors,
        "decision_count": len(decisions),
        "clean_approved_count": len(clean),
        "approve_with_revision_count": len(revision),
        "packet_created": PACKET_TSV.exists(),
        "errors": errors,
    }


def main() -> int:
    result = validate()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
