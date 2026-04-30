"""Validate Perek 4 limited protected-preview build gate artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TSV = ROOT / "data/gate_2_protected_preview_packets/bereishis_perek_4_limited_protected_preview_build_gate_2026_04_30.tsv"
MD = ROOT / "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_limited_protected_preview_build_gate_2026_04_30.md"
JSON_PATH = ROOT / "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_limited_protected_preview_build_gate_2026_04_30.json"
PLANNING_JSON = ROOT / "data/pipeline_rounds/content_expansion_planning_gate_2026_04_30.json"
CANDIDATE_PLAN = ROOT / "data/content_expansion_planning/content_expansion_candidate_plan_2026_04_30.json"
PACKET_README = ROOT / "data/gate_2_protected_preview_packets/README.md"
PIPELINE_README = ROOT / "data/pipeline_rounds/README.md"

EXPECTED_SELECTED = ["g2srcdisc_p4_001", "g2srcdisc_p4_002"]
EXPECTED_REVISION = ["g2srcdisc_p4_003", "g2srcdisc_p4_004"]
SAFETY_FALSE_KEYS = [
    "runtime_scope_widened",
    "perek_activated",
    "perek_4_activated",
    "reviewed_bank_promoted",
    "runtime_content_promoted",
    "student_facing_content_created",
    "scoring_mastery_changed",
    "question_generation_changed",
    "question_selection_changed",
    "question_selection_weighting_changed",
    "source_truth_changed",
    "fake_teacher_approval_created",
    "fake_student_data_created",
    "raw_logs_exposed",
    "validators_weakened",
    "ready_for_runtime_activation",
    "runtime_activation_authorized",
    "reviewed_bank_promotion_authorized",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig") if path.exists() else ""


def validate() -> list[str]:
    errors: list[str] = []
    for path in [TSV, MD, JSON_PATH, PLANNING_JSON, CANDIDATE_PLAN, PACKET_README, PIPELINE_README]:
        if not path.exists():
            errors.append(f"missing required file: {path.relative_to(ROOT)}")
    if errors:
        return errors

    try:
        payload = json.loads(_read(JSON_PATH))
        planning = json.loads(_read(PLANNING_JSON))
        candidate_plan = json.loads(_read(CANDIDATE_PLAN))
    except Exception as exc:  # pragma: no cover
        return [f"JSON parse failed: {exc}"]

    if payload.get("feature_name") != "perek_4_limited_protected_preview_build_gate":
        errors.append("feature_name mismatch")
    if payload.get("source_planning_candidate_id") != "cepg_primary_bereishis_perek_4_limited_protected_preview_build":
        errors.append("source planning candidate mismatch")
    if planning.get("runtime_activation_authorized") is not False:
        errors.append("planning gate must not authorize runtime activation")
    if candidate_plan.get("ready_for_runtime_activation") is not False:
        errors.append("candidate plan must not be runtime-ready")
    if payload.get("packet_item_count") != 2:
        errors.append("packet item count must be 2")
    if payload.get("selected_candidate_ids") != EXPECTED_SELECTED:
        errors.append("selected candidate ids mismatch")
    if payload.get("revision_watch_candidate_ids") != EXPECTED_REVISION:
        errors.append("revision-watch candidate ids mismatch")
    for key in SAFETY_FALSE_KEYS:
        if payload.get(key) is not False:
            errors.append(f"{key} must be false")

    with TSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if len(rows) != 2:
        errors.append("TSV must contain exactly 2 packet rows")
    row_ids = [row.get("source_candidate_id") for row in rows]
    if row_ids != EXPECTED_SELECTED:
        errors.append("TSV selected rows mismatch")
    for row in rows:
        for gate in ["runtime_allowed", "reviewed_bank_allowed", "student_facing_allowed", "perek_4_activated"]:
            if row.get(gate) != "false":
                errors.append(f"TSV {gate} must be false for {row.get('source_candidate_id')}")
        if row.get("build_gate_status") != "limited_protected_preview_build_ready":
            errors.append("TSV build gate status mismatch")

    text = _read(MD) + "\n" + json.dumps(payload, ensure_ascii=False) + "\n" + _read(PACKET_README) + "\n" + _read(PIPELINE_README)
    lowered_text = text.lower()
    for fragment in [
        "bounded perek 4 limited protected-preview",
        "revision-watch items preserved",
        "runtime scope widened: no",
        "reviewed-bank promoted: no",
        "student-facing content created: no",
    ]:
        if fragment not in lowered_text:
            errors.append(f"missing required text fragment: {fragment}")
    forbidden = [
        "runtime_allowed\ttrue",
        "reviewed_bank_allowed\ttrue",
        "student_facing_allowed\ttrue",
        "approved for runtime",
        "runtime activation authorized",
        '"reviewed_bank_promoted": true',
        "Perek 4 activated",
    ]
    for phrase in forbidden:
        if phrase.lower() in lowered_text:
            errors.append(f"forbidden phrase found: {phrase}")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Perek 4 limited protected-preview build gate validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
