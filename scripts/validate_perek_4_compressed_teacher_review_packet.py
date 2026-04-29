from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]

OVERRIDE_MD = ROOT / "data/pipeline_rounds/perek_3_to_perek_4_yossi_override_2026_04_29.md"
OVERRIDE_JSON = ROOT / "data/pipeline_rounds/perek_3_to_perek_4_yossi_override_2026_04_29.json"
PACKET_MD = (
    ROOT
    / "data/gate_2_protected_preview_candidates/reports/"
    "bereishis_perek_4_compressed_teacher_review_packet_2026_04_29.md"
)
PACKET_JSON = (
    ROOT
    / "data/gate_2_protected_preview_candidates/reports/"
    "bereishis_perek_4_compressed_teacher_review_packet_2026_04_29.json"
)
READINESS_MD = ROOT / "data/pipeline_rounds/perek_4_teacher_review_packet_readiness_2026_04_29.md"
SOURCE_INVENTORY = ROOT / "data/gate_2_source_discovery/bereishis_perek_4_review_only_safe_candidate_inventory.tsv"

REQUIRED_FILES = (
    OVERRIDE_MD,
    OVERRIDE_JSON,
    PACKET_MD,
    PACKET_JSON,
    READINESS_MD,
    SOURCE_INVENTORY,
)

FALSE_CANDIDATE_GATE_FIELDS = (
    "runtime_allowed",
    "reviewed_bank_allowed",
    "protected_preview_allowed",
    "student_facing_allowed",
    "broader_use_allowed",
    "perek_4_activated",
)

FORBIDDEN_PATTERNS = (
    "runtime_allowed=true",
    "runtime_allowed: true",
    "reviewed_bank_allowed=true",
    "reviewed_bank_allowed: true",
    "protected_preview_allowed=true",
    "protected_preview_allowed: true",
    "approved_for_runtime",
    "promoted_to_runtime",
    '"perek_4_activated": true',
    '"allows_perek_4_runtime_activation": true',
    '"allows_active_scope_expansion": true',
    '"allows_reviewed_bank_promotion": true',
    "Perek 4 is active runtime",
    "Perek 4 runtime is active",
    "Perek 4 runtime activation is approved",
    "fake teacher decision",
    "fake student observation",
)


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


def _read_inventory_rows(errors: list[str]) -> list[dict[str, str]]:
    if not SOURCE_INVENTORY.exists():
        errors.append(f"missing source inventory: {_relative(SOURCE_INVENTORY)}")
        return []
    with SOURCE_INVENTORY.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if not rows:
        errors.append("Perek 4 source inventory must not be empty")
    return rows


def _require_bool(payload: dict, key: str, expected: bool, errors: list[str], path: Path) -> None:
    if payload.get(key) is not expected:
        errors.append(f"{_relative(path)} must set {key} to {expected}")


def validate() -> dict:
    errors: list[str] = []
    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"Missing required file: {_relative(path)}")
    if errors:
        return {"ok": False, "errors": errors}

    override = _load_json(OVERRIDE_JSON, errors)
    packet = _load_json(PACKET_JSON, errors)
    inventory_rows = _read_inventory_rows(errors)
    inventory_ids = [row.get("candidate_id", "") for row in inventory_rows]

    _require_bool(override, "allows_perek_4_teacher_review_packet", True, errors, OVERRIDE_JSON)
    for key in (
        "allows_perek_4_runtime_activation",
        "allows_active_scope_expansion",
        "allows_reviewed_bank_promotion",
        "allows_protected_preview_packet_creation",
        "allows_student_facing_content",
        "allows_new_perek_4_candidate_discovery",
        "perek_3_full_closure_allowed_now",
        "fake_data_created",
    ):
        _require_bool(override, key, False, errors, OVERRIDE_JSON)
    _require_bool(override, "unresolved_perek_3_items_remain", True, errors, OVERRIDE_JSON)

    if packet.get("packet_status") != "teacher_review_only":
        errors.append("packet_status must be teacher_review_only")
    for key in (
        "perek_4_activated",
        "runtime_scope_widened",
        "reviewed_bank_promoted",
        "fake_teacher_decisions_created",
        "fake_student_observations_created",
        "source_truth_changed",
    ):
        _require_bool(packet, key, False, errors, PACKET_JSON)
    if packet.get("source_inventory_path") != _relative(SOURCE_INVENTORY):
        errors.append("packet JSON source_inventory_path must point to the Perek 4 source inventory")

    candidates = packet.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        errors.append("packet JSON must include a non-empty candidates list")
        candidates = []
    packet_ids = [str(candidate.get("candidate_id", "")) for candidate in candidates if isinstance(candidate, dict)]
    if packet_ids != inventory_ids:
        errors.append(f"packet candidate IDs must match source inventory order: {inventory_ids}")

    for index, candidate in enumerate(candidates, start=1):
        if not isinstance(candidate, dict):
            errors.append(f"candidate {index} must be an object")
            continue
        context = candidate.get("candidate_id", f"candidate {index}")
        if candidate.get("teacher_decision") is not None:
            errors.append(f"{context}: teacher_decision must be null")
        for field in FALSE_CANDIDATE_GATE_FIELDS:
            if candidate.get(field) is not False:
                errors.append(f"{context}: {field} must be false")
        for field in (
            "pasuk_ref",
            "hebrew_target",
            "proposed_skill",
            "proposed_question",
            "expected_answer",
            "source_artifact",
            "source_row_id",
            "risk_level",
        ):
            if not candidate.get(field):
                errors.append(f"{context}: {field} must be populated")
        distractors = candidate.get("distractors")
        if not isinstance(distractors, list) or len(distractors) != 3:
            errors.append(f"{context}: distractors must contain exactly three proposed choices")
        if candidate.get("expected_answer") != "noun":
            errors.append(f"{context}: expected_answer must remain noun for basic noun recognition")

    override_text = _read_text(OVERRIDE_MD)
    packet_text = _read_text(PACKET_MD)
    readiness_text = _read_text(READINESS_MD)
    for required in (
        "This override allows Perek 4 teacher-review packet preparation only. It does not allow runtime activation or active scope expansion.",
        "Perek 3 is not fully closed.",
        "phrase_translation remains excluded/unverified",
        "אָשִׁית",
    ):
        if required not in override_text:
            errors.append(f"override record missing required phrase: {required}")
    for required in (
        "teacher-review only",
        "not runtime content",
        "not a protected-preview packet",
        "No teacher decisions are applied by this packet.",
        "runtime_allowed=false",
        "reviewed_bank_allowed=false",
        "protected_preview_allowed=false",
    ):
        if required not in packet_text:
            errors.append(f"teacher-review packet missing required phrase: {required}")
    for required in (
        "This packet is not a protected-preview packet and is not runtime content unless later approved through the existing gates.",
        "No Perek 4 runtime activation occurred.",
        "No active scope expansion occurred.",
        "No approval is applied by this readiness report.",
    ):
        if required not in readiness_text:
            errors.append(f"readiness report missing required phrase: {required}")

    for path in (OVERRIDE_MD, OVERRIDE_JSON, PACKET_MD, PACKET_JSON, READINESS_MD):
        text = _read_text(path)
        for pattern in FORBIDDEN_PATTERNS:
            if pattern in text:
                errors.append(f"{_relative(path)} contains forbidden claim: {pattern}")

    return {
        "ok": not errors,
        "errors": errors,
        "candidate_count": len(candidates),
        "candidate_ids": packet_ids,
        "source_inventory_candidate_ids": inventory_ids,
    }


def main() -> int:
    result = validate()
    if not result["ok"]:
        for error in result["errors"]:
            print(f"ERROR: {error}")
        return 1
    print("Perek 4 compressed teacher-review packet validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
