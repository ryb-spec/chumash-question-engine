from __future__ import annotations

import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
REPORT_MD = ROOT / "data/pipeline_rounds/bereishis_perek_5_6_review_recommendation_report_2026_04_29.md"
REPORT_JSON = ROOT / "data/pipeline_rounds/bereishis_perek_5_6_review_recommendation_report_2026_04_29.json"

EXPECTED_CLEAN = ["g2srcdisc_p5_001", "g2srcdisc_p5_005"]
EXPECTED_REVISION_WATCH = ["g2srcdisc_p6_001", "g2srcdisc_p6_006", "g2srcdisc_p6_007"]
EXPECTED_HOLD_OR_EXCLUDE = [
    "g2srcdisc_p5_002",
    "g2srcdisc_p5_003",
    "g2srcdisc_p5_004",
    "g2srcdisc_p6_002",
    "g2srcdisc_p6_003",
    "g2srcdisc_p6_004",
    "g2srcdisc_p6_005",
]
FALSE_FIELDS = (
    "decisions_applied",
    "fake_observations_created",
    "perek_5_activated",
    "perek_6_activated",
    "runtime_scope_widened",
    "reviewed_bank_promoted",
    "student_facing_created",
)
FORBIDDEN_PHRASES = (
    "runtime_allowed=true",
    '"runtime_allowed": true',
    "reviewed_bank_allowed=true",
    '"reviewed_bank_allowed": true',
    "promoted_to_runtime",
    "approved_for_runtime",
    "Perek 5 is runtime active",
    "Perek 6 is runtime active",
    "Perek 5 runtime is active",
    "Perek 6 runtime is active",
)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def load_json(errors: list[str]) -> dict:
    try:
        payload = json.loads(read_text(REPORT_JSON))
    except json.JSONDecodeError as exc:
        errors.append(f"{rel(REPORT_JSON)} is invalid JSON: {exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"{rel(REPORT_JSON)} must be a JSON object")
        return {}
    return payload


def require_false(payload: dict, field: str, errors: list[str]) -> None:
    if payload.get(field) is not False:
        errors.append(f"{field} must be false")


def validate_json(payload: dict, errors: list[str]) -> None:
    if payload.get("report_type") != "advisory_review_recommendation":
        errors.append("report_type must be advisory_review_recommendation")
    if payload.get("recommendation_status") != "advisory_only":
        errors.append("recommendation_status must be advisory_only")
    if payload.get("clean_approved_recommended") != EXPECTED_CLEAN:
        errors.append("clean_approved_recommended must match the two clean-approved IDs exactly")
    if payload.get("revision_watch_recommended") != EXPECTED_REVISION_WATCH:
        errors.append("revision_watch_recommended must match the three selected Perek 6 IDs exactly")
    if payload.get("hold_or_exclude_recommended") != EXPECTED_HOLD_OR_EXCLUDE:
        errors.append("hold_or_exclude_recommended must match the seven held/excluded IDs exactly")
    for field in FALSE_FIELDS:
        require_false(payload, field, errors)


def validate_report_text(errors: list[str]) -> None:
    body = read_text(REPORT_MD)
    required = (
        "This is advisory only.",
        "Revision-watch items are not clean-approved.",
        "Continue with the mixed internal review packet",
        "No Perek 5 activation.",
        "No Perek 6 activation.",
        "No runtime scope expansion.",
        "No reviewed-bank promotion.",
        "No student-facing content.",
        "No fake observations.",
    )
    for phrase in required:
        if phrase not in body:
            errors.append(f"{rel(REPORT_MD)} missing required phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in body:
            errors.append(f"{rel(REPORT_MD)} contains forbidden phrase: {phrase}")
    json_body = read_text(REPORT_JSON)
    for phrase in FORBIDDEN_PHRASES:
        if phrase in json_body:
            errors.append(f"{rel(REPORT_JSON)} contains forbidden phrase: {phrase}")


def validate() -> dict:
    errors: list[str] = []
    for path in (REPORT_MD, REPORT_JSON):
        if not path.exists():
            errors.append(f"Missing required file: {rel(path)}")
    if errors:
        return {"ok": False, "errors": errors}
    payload = load_json(errors)
    validate_json(payload, errors)
    validate_report_text(errors)
    return {"ok": not errors, "errors": errors, "payload": payload}


def main() -> int:
    result = validate()
    if not result["ok"]:
        for error in result["errors"]:
            print(f"ERROR: {error}")
        return 1
    print("Perek 5–6 review recommendation report validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
