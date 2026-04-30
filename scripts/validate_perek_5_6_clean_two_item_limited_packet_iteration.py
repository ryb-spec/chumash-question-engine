from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
PACKET_DIR = ROOT / "data/gate_2_protected_preview_packets"
REPORTS = PACKET_DIR / "reports"
PIPELINE = ROOT / "data/pipeline_rounds"

TSV = PACKET_DIR / "bereishis_perek_5_6_clean_two_item_limited_packet_iteration.tsv"
MD = REPORTS / "bereishis_perek_5_6_clean_two_item_limited_packet_iteration_2026_04_30.md"
JSON_PATH = REPORTS / "bereishis_perek_5_6_clean_two_item_limited_packet_iteration_2026_04_30.json"
NEXT_GATE = PIPELINE / "bereishis_perek_5_6_clean_two_item_iteration_next_gate_2026_04_30.md"
REQUIRED_FILES = (TSV, MD, JSON_PATH, NEXT_GATE)

EXPECTED_INCLUDED_IDS = ["g2srcdisc_p5_001", "g2srcdisc_p5_005"]
EXPECTED_REVISE_IDS = ["g2srcdisc_p6_001", "g2srcdisc_p6_006"]
EXPECTED_HELD_IDS = ["g2srcdisc_p6_007"]
EXPECTED_EXCLUDED_IDS = [
    "g2srcdisc_p5_002",
    "g2srcdisc_p5_003",
    "g2srcdisc_p5_004",
    "g2srcdisc_p6_002",
    "g2srcdisc_p6_003",
    "g2srcdisc_p6_004",
    "g2srcdisc_p6_005",
]
FALSE_TOP_FIELDS = (
    "runtime_scope_widened",
    "reviewed_bank_promoted",
    "student_facing_created",
    "fake_observations_created",
    "fake_student_data_created",
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
    "runtime activation occurred",
    "reviewed-bank promotion occurred",
)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def load_json(errors: list[str]) -> dict:
    try:
        payload = json.loads(text(JSON_PATH))
    except json.JSONDecodeError as exc:
        errors.append(f"{rel(JSON_PATH)} invalid JSON: {exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"{rel(JSON_PATH)} must contain a JSON object")
        return {}
    return payload


def require_false(container: dict, field: str, errors: list[str], context: str) -> None:
    if container.get(field) is not False:
        errors.append(f"{context}: {field} must be false")


def validate_json(payload: dict, errors: list[str]) -> None:
    if payload.get("iteration_status") != "clean_two_item_limited_packet_iteration":
        errors.append("iteration_status mismatch")
    if payload.get("item_count") != 2:
        errors.append("item_count must be 2")
    if payload.get("included_candidate_ids") != EXPECTED_INCLUDED_IDS:
        errors.append("included_candidate_ids mismatch")
    if payload.get("revise_candidate_ids") != EXPECTED_REVISE_IDS:
        errors.append("revise_candidate_ids mismatch")
    if payload.get("held_candidate_ids") != EXPECTED_HELD_IDS:
        errors.append("held_candidate_ids mismatch")
    if sorted(payload.get("excluded_candidate_ids", [])) != sorted(EXPECTED_EXCLUDED_IDS):
        errors.append("excluded_candidate_ids mismatch")
    for field in FALSE_TOP_FIELDS:
        require_false(payload, field, errors, "iteration JSON")
    items = payload.get("items")
    if not isinstance(items, list) or len(items) != 2:
        errors.append("JSON items must contain exactly 2 rows")
        items = []
    ids = [item.get("source_candidate_id") for item in items if isinstance(item, dict)]
    if ids != EXPECTED_INCLUDED_IDS:
        errors.append("JSON item IDs mismatch")
    forbidden_ids = set(EXPECTED_REVISE_IDS + EXPECTED_HELD_IDS + EXPECTED_EXCLUDED_IDS)
    if forbidden_ids.intersection(ids):
        errors.append("revise/held/excluded item appeared in JSON items")
    for item in items:
        if not isinstance(item, dict):
            continue
        context = f"JSON item {item.get('source_candidate_id')}"
        if item.get("iteration_review_decision") is not None:
            errors.append(f"{context}: iteration_review_decision must be null")
        if item.get("expected_answer") != "noun":
            errors.append(f"{context}: expected_answer must be noun")
        for field in FALSE_ITEM_FIELDS:
            require_false(item, field, errors, context)


def validate_tsv(errors: list[str]) -> None:
    with TSV.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if len(rows) != 2:
        errors.append("TSV must contain exactly 2 rows")
    ids = [row.get("source_candidate_id") for row in rows]
    if ids != EXPECTED_INCLUDED_IDS:
        errors.append("TSV included IDs mismatch")
    forbidden_ids = set(EXPECTED_REVISE_IDS + EXPECTED_HELD_IDS + EXPECTED_EXCLUDED_IDS)
    if forbidden_ids.intersection(ids):
        errors.append("revise/held/excluded item appeared in TSV")
    for row in rows:
        context = f"TSV row {row.get('source_candidate_id')}"
        if row.get("prior_observation_decision") != "approve_for_later_packet_iteration":
            errors.append(f"{context}: prior_observation_decision mismatch")
        if row.get("expected_answer") != "noun":
            errors.append(f"{context}: expected_answer must be noun")
        for field in FALSE_ITEM_FIELDS:
            if row.get(field) != "false":
                errors.append(f"{context}: {field} must be false")


def scan_texts(errors: list[str]) -> None:
    for path in REQUIRED_FILES:
        body = text(path)
        for pattern in FORBIDDEN_PATTERNS:
            if pattern in body:
                errors.append(f"{rel(path)} contains forbidden phrase: {pattern}")
    report = text(MD)
    for phrase in [
        "includes only the two items",
        "סֵפֶר",
        "בֵּן",
        "בָשָׂר",
        "פֶתַח",
        "מַבּוּל",
        "No future decisions or observations are filled",
        "No Perek 5 activation",
        "No Perek 6 activation",
    ]:
        if phrase not in report:
            errors.append(f"iteration Markdown missing required phrase: {phrase}")
    gate = text(NEXT_GATE)
    if "pause Perek content expansion" not in gate:
        errors.append("next-gate report missing product/runtime improvement recommendation")
    if "cross-session scope exhaustion / repetition control" not in gate:
        errors.append("next-gate report missing repetition-control recommendation")


def validate() -> dict:
    errors: list[str] = []
    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"Missing required file: {rel(path)}")
    if errors:
        return {"ok": False, "errors": errors}
    payload = load_json(errors)
    validate_json(payload, errors)
    validate_tsv(errors)
    scan_texts(errors)
    return {"ok": not errors, "errors": errors, "json": payload}


def main() -> int:
    result = validate()
    if not result["ok"]:
        for error in result["errors"]:
            print(f"ERROR: {error}")
        return 1
    print("Perek 5-6 clean two-item limited packet iteration validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
