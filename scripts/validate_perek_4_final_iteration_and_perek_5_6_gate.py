from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET_DIR = ROOT / "data" / "gate_2_protected_preview_packets"
REPORT_DIR = PACKET_DIR / "reports"
PIPELINE_DIR = ROOT / "data" / "pipeline_rounds"
PROMPT = PIPELINE_DIR / "prompts" / "bereishis_perek_5_6_source_discovery_prompt.md"

ITERATION_TSV = PACKET_DIR / "bereishis_perek_4_two_item_limited_internal_packet_iteration.tsv"
ITERATION_MD = REPORT_DIR / "bereishis_perek_4_two_item_limited_internal_packet_iteration_2026_04_29.md"
ITERATION_JSON = REPORT_DIR / "bereishis_perek_4_two_item_limited_internal_packet_iteration_2026_04_29.json"
GATE_MD = PIPELINE_DIR / "perek_4_final_internal_iteration_and_perek_5_6_source_discovery_gate_2026_04_29.md"
GATE_JSON = PIPELINE_DIR / "perek_4_final_internal_iteration_and_perek_5_6_source_discovery_gate_2026_04_29.json"

INCLUDED = {"g2srcdisc_p4_001", "g2srcdisc_p4_002"}
EXCLUDED = {"g2srcdisc_p4_003", "g2srcdisc_p4_004", "g2srcdisc_p4_005"}
FALSE_ITEM_FIELDS = ("runtime_allowed", "reviewed_bank_allowed", "student_facing_allowed", "perek_4_activated")
FORBIDDEN_COMPACT = ("runtime_allowed=true", "reviewed_bank_allowed=true", "student_facing_allowed=true")
FORBIDDEN_TEXT = (
    "promoted_to_runtime",
    "approved_for_runtime",
    "Perek 4 runtime activation is allowed",
    "Perek 5-6 activation is allowed",
    "Perek 5?6 activation is allowed",
)


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
                _fail(f"Forbidden positive permission in {path.relative_to(ROOT)}: {token}")
        for token in FORBIDDEN_TEXT:
            if token.lower() in lowered:
                _fail(f"Forbidden activation/promotion claim in {path.relative_to(ROOT)}: {token}")


def validate() -> None:
    required = [ITERATION_TSV, ITERATION_MD, ITERATION_JSON, GATE_MD, GATE_JSON, PROMPT]
    for path in required:
        _read(path)

    iteration = _load_json(ITERATION_JSON)
    if iteration.get("iteration_status") != "two_item_limited_internal_packet_iteration":
        _fail("Unexpected iteration_status.")
    if iteration.get("perek") != 4:
        _fail("Iteration must be for Perek 4.")
    if iteration.get("item_count") != 2:
        _fail("Iteration item_count must be 2.")
    if set(iteration.get("included_candidate_ids", [])) != INCLUDED:
        _fail("Included candidates must be exactly g2srcdisc_p4_001 and g2srcdisc_p4_002.")
    if set(iteration.get("excluded_or_held_ids", [])) != EXCLUDED:
        _fail("Excluded/held IDs must include exactly p4_003, p4_004, and p4_005.")
    items = iteration.get("items")
    if not isinstance(items, list) or len(items) != 2:
        _fail("Iteration JSON must contain exactly two item objects.")
    item_candidate_ids = {item.get("source_candidate_id") for item in items}
    if item_candidate_ids != INCLUDED:
        _fail("Iteration items must include only the two approved source candidates.")
    for item in items:
        if item.get("observation_result") is not None:
            _fail("Observation results must remain null until real observation evidence exists.")
        for field in FALSE_ITEM_FIELDS:
            if item.get(field) is not False:
                _fail(f"Item {item.get('source_candidate_id')} must keep {field}=false.")

    rows = _read_tsv(ITERATION_TSV)
    if len(rows) != 2:
        _fail("Iteration TSV must contain exactly two rows.")
    if {row.get("source_candidate_id") for row in rows} != INCLUDED:
        _fail("Iteration TSV must include only the two approved source candidates.")
    for row in rows:
        for field in FALSE_ITEM_FIELDS:
            if row.get(field) != "false":
                _fail(f"TSV row {row.get('source_candidate_id')} must keep {field}=false.")

    gate = _load_json(GATE_JSON)
    expected_gate = {
        "perek_4_two_item_iteration_created": True,
        "perek_4_full_closure": False,
        "perek_4_runtime_active": False,
        "runtime_scope_widened": False,
        "reviewed_bank_promoted": False,
        "student_facing_created": False,
        "perek_5_6_source_discovery_allowed_next": True,
        "perek_5_6_runtime_allowed": False,
        "perek_5_6_reviewed_bank_allowed": False,
        "perek_5_6_student_facing_allowed": False,
        "perek_5_6_protected_preview_packet_allowed": False,
    }
    for field, expected in expected_gate.items():
        if gate.get(field) is not expected:
            _fail(f"Gate JSON must have {field}={expected!r}.")
    if set(gate.get("unresolved_perek_4_items", [])) != EXCLUDED:
        _fail("Gate JSON must preserve the three unresolved Perek 4 items.")

    gate_md = _read(GATE_MD)
    if "This gate permits the next task to begin Perek 5-6 source discovery only. It does not permit runtime expansion." not in gate_md:
        _fail("Gate MD must include the explicit source-discovery-only permission statement.")
    if "Perek 4 is not fully closed" not in gate_md:
        _fail("Gate MD must say Perek 4 is not fully closed.")

    prompt = _read(PROMPT)
    for required_text in (
        "source discovery only",
        "Do not activate runtime.",
        "Do not widen active scope.",
        "Do not promote anything to reviewed bank.",
        "Do not create a protected-preview packet.",
        "Do not create public/student-facing content.",
        "Keep all gates false.",
    ):
        if required_text not in prompt:
            _fail(f"Prompt artifact missing required guardrail: {required_text}")

    _scan_forbidden(required)
    print("Perek 4 final iteration and Perek 5-6 source-discovery gate validation passed.")


if __name__ == "__main__":
    validate()
