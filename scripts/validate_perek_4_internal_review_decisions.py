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
PACKET_TSV = PACKET_DIR / "bereishis_perek_4_internal_protected_preview_packet.tsv"
PACKET_MD = REPORTS / "bereishis_perek_4_internal_protected_preview_packet_2026_04_29.md"
PACKET_JSON = REPORTS / "bereishis_perek_4_internal_protected_preview_packet_2026_04_29.json"
CHECKLIST = REPORTS / "bereishis_perek_4_internal_protected_preview_review_checklist_2026_04_29.md"
DECISIONS_MD = REPORTS / "bereishis_perek_4_internal_protected_preview_review_decisions_applied_2026_04_29.md"
DECISIONS_JSON = REPORTS / "bereishis_perek_4_internal_protected_preview_review_decisions_applied_2026_04_29.json"
READINESS_MD = REPORTS / "bereishis_perek_4_limited_internal_preview_readiness_2026_04_29.md"
BLOCKED_REGISTER = REPORTS / "bereishis_perek_4_blocked_revision_register_2026_04_29.md"
OBSERVATION_TEMPLATE = REPORTS / "bereishis_perek_4_limited_internal_preview_observation_template_2026_04_29.md"
PIPELINE_STATUS = ROOT / "data/pipeline_rounds/perek_4_internal_review_decisions_and_limited_preview_readiness_2026_04_29.md"

REQUIRED_FILES = (
    DECISIONS_MD,
    DECISIONS_JSON,
    PACKET_TSV,
    PACKET_MD,
    PACKET_JSON,
    CHECKLIST,
    READINESS_MD,
    BLOCKED_REGISTER,
    OBSERVATION_TEMPLATE,
    PIPELINE_STATUS,
)
EXPECTED_DECISIONS = {
    "g2ppacket_p4_001": "approve_for_limited_internal_preview",
    "g2ppacket_p4_002": "approve_for_limited_internal_preview",
    "g2ppacket_p4_003": "approve_with_revision",
    "g2ppacket_p4_004": "approve_with_revision",
}
CLEAN_READY = ["g2ppacket_p4_001", "g2ppacket_p4_002"]
REVISION_BLOCKED = ["g2ppacket_p4_003", "g2ppacket_p4_004", "g2srcdisc_p4_005"]
FALSE_FIELDS = ("runtime_allowed", "reviewed_bank_allowed", "student_facing_allowed", "perek_4_activated")
FORBIDDEN_PATTERNS = (
    "runtime_allowed=true",
    "runtime_allowed: true",
    '"runtime_allowed": true',
    "reviewed_bank_allowed=true",
    "reviewed_bank_allowed: true",
    '"reviewed_bank_allowed": true',
    "promoted_to_runtime",
    "approved_for_runtime",
    "Perek 4 is active runtime",
    "Perek 4 runtime is active",
)
FAKE_OBSERVATION_PATTERNS = ("fake observation", "invented observation", "synthetic observation")


def _relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def _load_json(path: Path, errors: list[str]) -> dict:
    try:
        payload = json.loads(_read_text(path))
    except json.JSONDecodeError as exc:
        errors.append(f"{_relative(path)} is invalid JSON: {exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"{_relative(path)} must be a JSON object")
        return {}
    return payload


def _read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _require_false(payload: dict, key: str, errors: list[str], context: str) -> None:
    if payload.get(key) is not False:
        errors.append(f"{context}: {key} must be false")


def _validate_decisions(payload: dict, errors: list[str]) -> dict[str, dict]:
    if payload.get("item_count") != 4:
        errors.append("item_count must be 4")
    if payload.get("approve_for_limited_internal_preview_count") != 2:
        errors.append("approve_for_limited_internal_preview_count must be 2")
    if payload.get("approve_with_revision_count") != 2:
        errors.append("approve_with_revision_count must be 2")
    if payload.get("blocked_external_candidate_count") != 1:
        errors.append("blocked_external_candidate_count must be 1")
    if payload.get("clean_readiness_lane_packet_item_ids") != CLEAN_READY:
        errors.append("clean_readiness_lane_packet_item_ids must be p4_001 and p4_002 only")
    if payload.get("revision_or_blocked_ids") != REVISION_BLOCKED:
        errors.append("revision_or_blocked_ids must list p4_003, p4_004, and g2srcdisc_p4_005")
    for field in FALSE_FIELDS:
        _require_false(payload, field, errors, "decisions JSON")
    if payload.get("fake_observations_created") is not False:
        errors.append("fake_observations_created must be false")
    if payload.get("fake_student_data_created") is not False:
        errors.append("fake_student_data_created must be false")

    decisions = payload.get("decisions")
    if not isinstance(decisions, list) or len(decisions) != 4:
        errors.append("decisions JSON must contain exactly four packet decisions")
        decisions = []
    by_packet = {str(decision.get("packet_item_id", "")): decision for decision in decisions if isinstance(decision, dict)}
    if set(by_packet) != set(EXPECTED_DECISIONS):
        errors.append("decision packet IDs must match the four Perek 4 packet items")
    for packet_id, expected in EXPECTED_DECISIONS.items():
        decision = by_packet.get(packet_id, {})
        if decision.get("decision") != expected:
            errors.append(f"{packet_id}: expected decision {expected}")
        for field in FALSE_FIELDS:
            _require_false(decision, field, errors, packet_id)
        if packet_id in CLEAN_READY and decision.get("eligible_for_limited_internal_preview") is not True:
            errors.append(f"{packet_id}: clean item must be eligible for limited internal preview")
        if packet_id not in CLEAN_READY and decision.get("eligible_for_limited_internal_preview") is not False:
            errors.append(f"{packet_id}: revision item must not be in clean readiness lane")
    return by_packet


def _validate_packet_updates(errors: list[str]) -> None:
    rows = _read_tsv(PACKET_TSV)
    decisions = {row.get("packet_item_id", ""): row.get("internal_review_decision", "") for row in rows}
    if decisions != EXPECTED_DECISIONS:
        errors.append("packet TSV internal_review_decision values must match expected decisions")
    for row in rows:
        context = row.get("packet_item_id", "packet row")
        for field in FALSE_FIELDS:
            if row.get(field) != "false":
                errors.append(f"{context}: packet TSV {field} must be false")
    packet_payload = _load_json(PACKET_JSON, errors)
    packet_decisions = {item.get("packet_item_id", ""): item.get("internal_review_decision") for item in packet_payload.get("items", []) if isinstance(item, dict)}
    if packet_decisions != EXPECTED_DECISIONS:
        errors.append("packet JSON internal_review_decision values must match expected decisions")
    for item in packet_payload.get("items", []):
        if not isinstance(item, dict):
            continue
        context = item.get("packet_item_id", "packet JSON item")
        for field in FALSE_FIELDS:
            _require_false(item, field, errors, context)
    for field in FALSE_FIELDS:
        _require_false(packet_payload, field, errors, "packet JSON")


def _validate_reports(errors: list[str]) -> None:
    decisions_text = _read_text(DECISIONS_MD)
    readiness_text = _read_text(READINESS_MD)
    blocked_text = _read_text(BLOCKED_REGISTER)
    observation_text = _read_text(OBSERVATION_TEMPLATE)
    pipeline_text = _read_text(PIPELINE_STATUS)

    for packet_id, decision in EXPECTED_DECISIONS.items():
        if packet_id not in decisions_text or decision not in decisions_text:
            errors.append(f"decisions report missing {packet_id} / {decision}")
    for packet_id in CLEAN_READY:
        if packet_id not in readiness_text:
            errors.append(f"limited readiness lane missing clean item {packet_id}")
    for blocked_id in REVISION_BLOCKED:
        if blocked_id not in blocked_text or blocked_id not in readiness_text:
            errors.append(f"blocked/revision artifacts must include {blocked_id}")
    if "g2ppacket_p4_003" in observation_text.split("## Active observation items", 1)[-1].split("## Excluded", 1)[0]:
        errors.append("observation template active section must not include g2ppacket_p4_003")
    if "g2ppacket_p4_004" in observation_text.split("## Active observation items", 1)[-1].split("## Excluded", 1)[0]:
        errors.append("observation template active section must not include g2ppacket_p4_004")
    for required in ("Observed by: ", "Observation date: ", "Student/internal reviewer response: ", "Decision after observation: "):
        if required not in observation_text:
            errors.append(f"observation template missing blank field: {required}")
    for phrase in (
        "No Perek 4 runtime activation",
        "No active scope expansion",
        "No reviewed-bank promotion",
        "No public/student-facing content",
    ):
        if phrase not in pipeline_text and phrase not in decisions_text:
            errors.append(f"safety phrase missing: {phrase}")
    for path in REQUIRED_FILES:
        text = _read_text(path)
        for pattern in FORBIDDEN_PATTERNS:
            if pattern in text:
                errors.append(f"{_relative(path)} contains forbidden claim: {pattern}")
        for pattern in FAKE_OBSERVATION_PATTERNS:
            if pattern in text.lower() and "no fake observations" not in text.lower():
                errors.append(f"{_relative(path)} contains forbidden observation claim: {pattern}")


def validate() -> dict:
    errors: list[str] = []
    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"Missing required file: {_relative(path)}")
    if errors:
        return {"ok": False, "errors": errors}
    payload = _load_json(DECISIONS_JSON, errors)
    _validate_decisions(payload, errors)
    _validate_packet_updates(errors)
    _validate_reports(errors)
    return {
        "ok": not errors,
        "errors": errors,
        "clean_ready": payload.get("clean_readiness_lane_packet_item_ids", []),
        "revision_or_blocked": payload.get("revision_or_blocked_ids", []),
    }


def main() -> int:
    result = validate()
    if not result["ok"]:
        for error in result["errors"]:
            print(f"ERROR: {error}")
        return 1
    print("Perek 4 internal review decisions validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
