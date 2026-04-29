from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "data" / "gate_2_protected_preview_packets" / "reports"
PIPELINE_DIR = ROOT / "data" / "pipeline_rounds"

DECISIONS_MD = REPORT_DIR / "bereishis_perek_4_limited_internal_preview_decisions_applied_2026_04_29.md"
DECISIONS_JSON = REPORT_DIR / "bereishis_perek_4_limited_internal_preview_decisions_applied_2026_04_29.json"
READINESS_MD = PIPELINE_DIR / "perek_4_limited_internal_preview_next_packet_iteration_readiness_2026_04_29.md"
HOLD_REGISTER_MD = REPORT_DIR / "bereishis_perek_4_limited_internal_preview_hold_register_2026_04_29.md"
CHECKLIST_MD = REPORT_DIR / "bereishis_perek_4_internal_protected_preview_review_checklist_2026_04_29.md"
OBSERVATION_TEMPLATE_MD = REPORT_DIR / "bereishis_perek_4_limited_internal_preview_observation_template_2026_04_29.md"

EXPECTED_DECISIONS = {
    "g2ppacket_p4_001": "approve_for_later_packet_iteration",
    "g2ppacket_p4_002": "approve_for_later_packet_iteration",
    "g2ppacket_p4_003": "hold",
    "g2ppacket_p4_004": "hold",
    "g2srcdisc_p4_005": "needs_source_follow_up",
}
NEXT_ELIGIBLE = {"g2ppacket_p4_001", "g2ppacket_p4_002"}
HELD = {"g2ppacket_p4_003", "g2ppacket_p4_004"}
SOURCE_FOLLOW_UP = {"g2srcdisc_p4_005"}
FALSE_FIELDS = ("runtime_allowed", "reviewed_bank_allowed", "student_facing_allowed", "perek_4_activated")
FORBIDDEN = (
    "runtime_allowed=true",
    "reviewed_bank_allowed=true",
    "promoted_to_runtime",
    "approved_for_runtime",
    "Perek 4 is active runtime",
)


def _fail(message: str) -> None:
    raise SystemExit(message)


def _read(path: Path) -> str:
    if not path.exists():
        _fail(f"Missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def _load_json(path: Path) -> dict:
    try:
        return json.loads(_read(path))
    except json.JSONDecodeError as exc:
        _fail(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}")


def _scan_forbidden(paths: list[Path]) -> None:
    for path in paths:
        text = _read(path)
        compact = text.replace(" ", "").lower()
        lowered = text.lower()
        for token in FORBIDDEN:
            token_lower = token.lower()
            if "=" in token_lower:
                if token_lower in compact:
                    _fail(f"Forbidden positive gate claim in {path.relative_to(ROOT)}: {token}")
            elif token_lower in lowered:
                _fail(f"Forbidden promotion/runtime claim in {path.relative_to(ROOT)}: {token}")


def validate() -> None:
    required = [
        DECISIONS_MD,
        DECISIONS_JSON,
        READINESS_MD,
        HOLD_REGISTER_MD,
        CHECKLIST_MD,
        OBSERVATION_TEMPLATE_MD,
    ]
    for path in required:
        _read(path)

    data = _load_json(DECISIONS_JSON)
    if data.get("item_count") != 5:
        _fail("Expected item_count to be 5.")
    if data.get("approve_for_later_packet_iteration_count") != 2:
        _fail("Expected exactly two approve_for_later_packet_iteration decisions.")
    if data.get("hold_count") != 2:
        _fail("Expected exactly two hold decisions.")
    if data.get("source_follow_up_count") != 1:
        _fail("Expected exactly one source follow-up decision.")

    decisions = data.get("decisions")
    if not isinstance(decisions, list) or len(decisions) != 5:
        _fail("Expected exactly five decisions.")
    by_id = {item.get("item_id"): item for item in decisions}
    if set(by_id) != set(EXPECTED_DECISIONS):
        _fail(f"Unexpected decision IDs: {sorted(by_id)}")

    for item_id, expected in EXPECTED_DECISIONS.items():
        decision = by_id[item_id]
        if decision.get("decision") != expected:
            _fail(f"Unexpected decision for {item_id}: {decision.get('decision')}")
        for field in FALSE_FIELDS:
            if decision.get(field) is not False:
                _fail(f"{item_id} must keep {field}=false.")

    eligible = {item["item_id"] for item in decisions if item.get("eligible_for_next_packet_iteration") is True}
    if eligible != NEXT_ELIGIBLE:
        _fail(f"Only {sorted(NEXT_ELIGIBLE)} may be eligible for next packet iteration; got {sorted(eligible)}")

    for item_id in HELD:
        item = by_id[item_id]
        if item.get("held_for_spacing_or_alias_review") is not True:
            _fail(f"{item_id} must be held for spacing or alias review.")
        if item.get("eligible_for_next_packet_iteration") is not False:
            _fail(f"{item_id} must not be eligible for next packet iteration.")

    for item_id in SOURCE_FOLLOW_UP:
        item = by_id[item_id]
        if item.get("source_follow_up_required") is not True:
            _fail(f"{item_id} must require source follow-up.")
        if item.get("eligible_for_next_packet_iteration") is not False:
            _fail(f"{item_id} must not be eligible for next packet iteration.")

    checklist = _read(CHECKLIST_MD)
    template = _read(OBSERVATION_TEMPLATE_MD)
    if "Limited internal preview decisions applied - 2026-04-29" not in checklist:
        _fail("Updated review checklist must include limited preview decisions section.")
    if "Yossi/internal reviewer decisions applied after limited preview - 2026-04-29" not in template:
        _fail("Updated observation template must include limited preview decisions section.")
    if "These decisions are not student observation results" not in template:
        _fail("Observation template must distinguish decisions from student observations.")
    for line in template.splitlines():
        stripped = line.strip()
        if stripped.startswith("- Student/internal reviewer response:"):
            value = stripped.split(":", 1)[1].strip()
            if value:
                _fail("Observation template appears to contain a filled observation response.")
    if "fake observations were added" not in template:
        _fail("Observation template must explicitly guard against fake observations.")

    readiness = _read(READINESS_MD)
    for required_text in ("g2ppacket_p4_001", "g2ppacket_p4_002", "No runtime activation", "No active scope expansion"):
        if required_text not in readiness:
            _fail(f"Readiness report missing required text: {required_text}")

    hold_register = _read(HOLD_REGISTER_MD)
    for required_text in ("g2ppacket_p4_003", "g2ppacket_p4_004", "g2srcdisc_p4_005"):
        if required_text not in hold_register:
            _fail(f"Hold register missing required item: {required_text}")

    _scan_forbidden(required)
    print("Perek 4 limited internal preview decisions validation passed.")


if __name__ == "__main__":
    validate()
