from __future__ import annotations

import csv
import json
import subprocess
from pathlib import Path

if hasattr(__import__("sys"), "stdout"):
    import sys

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "data/gate_2_protected_preview_packets/reports"
PIPELINE = ROOT / "data/pipeline_rounds"

OBS_TSV = REPORTS / "bereishis_perek_4_broad_vocabulary_final_observation_evidence_2026_04_30.tsv"
OBS_JSON = REPORTS / "bereishis_perek_4_broad_vocabulary_final_observation_evidence_2026_04_30.json"
COMPLETION_MD = PIPELINE / "perek_4_broad_vocabulary_final_internal_completion_gate_2026_04_30.md"
COMPLETION_JSON = PIPELINE / "perek_4_broad_vocabulary_final_internal_completion_gate_2026_04_30.json"
READINESS_TSV = REPORTS / "bereishis_perek_4_broad_vocabulary_final_readiness_register_2026_04_30.tsv"
READINESS_JSON = REPORTS / "bereishis_perek_4_broad_vocabulary_final_readiness_register_2026_04_30.json"
NEXT_PROMPT_REVIEWED_BANK = PIPELINE / "next_codex_prompt_perek_4_broad_vocabulary_reviewed_bank_candidate_planning_2026_04_30.md"
NEXT_PROMPT_RUNTIME = PIPELINE / "next_codex_prompt_perek_4_broad_vocabulary_runtime_readiness_planning_2026_04_30.md"
MAIN_JSON = ROOT / "data/pipeline_rounds/perek_4_broad_vocabulary_internal_protected_preview_packet_v1_2026_04_30.json"

EXPECTED_PACKET_ITEMS = {
    "p4bv_ipp_001",
    "p4bv_ipp_002",
    "p4bv_ipp_003",
    "p4bv_ipp_004",
    "p4bv_ipp_005",
}

EXPECTED_SOURCE_IDS = {
    "svqcl_p4_001",
    "svqcl_p4_002",
    "svqcl_p4_003",
    "svqcl_p4_005",
    "svqcl_p4_006",
}

EXPECTED_BLOCKED_REVISION = {"bsvb_p4_002", "svqcl_p4_004"}
EXPECTED_BLOCKED_HELD = {"bsvb_p4_003", "bsvb_p4_004", "svqcl_p4_007", "svqcl_p4_008", "svqcl_p4_009"}
EXPECTED_BLOCKED = EXPECTED_BLOCKED_REVISION | EXPECTED_BLOCKED_HELD

FORBIDDEN_PHRASES = (
    "runtime active",
    "runtime activated",
    "reviewed bank promoted",
    "student-facing released",
    "mastery proven",
    "source truth changed",
)


def _fail(message: str) -> None:
    raise SystemExit(f"Perek 4 broad vocabulary final observation gate validation failed: {message}")


def _read_text(path: Path) -> str:
    if not path.exists():
        _fail(f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _json(path: Path) -> dict:
    try:
        return json.loads(_read_text(path))
    except json.JSONDecodeError as exc:
        _fail(f"invalid JSON {path.relative_to(ROOT)}: {exc}")


def validate() -> None:
    for path in [
        OBS_TSV,
        OBS_JSON,
        COMPLETION_MD,
        COMPLETION_JSON,
        READINESS_TSV,
        READINESS_JSON,
        NEXT_PROMPT_REVIEWED_BANK,
        NEXT_PROMPT_RUNTIME,
        MAIN_JSON,
    ]:
        if not path.exists():
            _fail(f"missing required file: {path.relative_to(ROOT)}")

    obs_rows = _rows(OBS_TSV)
    obs_payload = _json(OBS_JSON)
    completion = _json(COMPLETION_JSON)
    readiness = _json(READINESS_JSON)
    main_contract = _json(MAIN_JSON)

    if len(obs_rows) != 5:
        _fail("observation evidence TSV must contain exactly five rows")
    if obs_payload.get("packet_item_count") != 5:
        _fail("observation evidence JSON must have packet_item_count=5")
    if obs_payload.get("observed_count") != 5:
        _fail("observation evidence JSON must have observed_count=5")
    if obs_payload.get("approved_after_observation_count") != 5:
        _fail("observation evidence JSON must have approved_after_observation_count=5")
    if obs_payload.get("ready_for_reviewed_bank_candidate_planning") is not True:
        _fail("evidence JSON must set ready_for_reviewed_bank_candidate_planning=true")
    if obs_payload.get("ready_for_runtime_readiness_planning") is not True:
        _fail("evidence JSON must set ready_for_runtime_readiness_planning=true")
    if obs_payload.get("ready_for_runtime_activation") is not False:
        _fail("evidence JSON must keep ready_for_runtime_activation=false")
    if obs_payload.get("runtime_activation_authorized") is not False:
        _fail("evidence JSON must keep runtime_activation_authorized=false")

    for field in [
        "fake_observation_evidence_created",
        "runtime_scope_widened",
        "perek_activated",
        "reviewed_bank_promoted",
        "runtime_questions_created",
        "runtime_content_promoted",
        "student_facing_content_created",
        "source_truth_changed",
    ]:
        if obs_payload.get(field) is not False:
            _fail(f"observation evidence JSON field {field} must be false")

    if {row["packet_item_id"] for row in obs_rows} != EXPECTED_PACKET_ITEMS:
        _fail("observation evidence TSV packet_item_id mismatch")
    if {row["source_candidate_id"] for row in obs_rows} != EXPECTED_SOURCE_IDS:
        _fail("observation evidence TSV source_candidate_id mismatch")

    for row in obs_rows:
        if row["observed"] != "yes":
            _fail(f"{row['packet_item_id']} must be observed=yes")
        if row["reviewer_name"] != "Yossi":
            _fail(f"{row['packet_item_id']} reviewer_name must be Yossi")
        if row["recommended_decision"] != "approve_after_observation":
            _fail(f"{row['packet_item_id']} decision must be approve_after_observation")
        if row["final_internal_status"] != "approved_after_internal_observation":
            _fail(f"{row['packet_item_id']} final_internal_status must be approved_after_internal_observation")
        if row["reviewed_bank_status"] != "not_reviewed_bank":
            _fail(f"{row['packet_item_id']} reviewed_bank_status must be not_reviewed_bank")
        if row["runtime_status"] != "not_runtime":
            _fail(f"{row['packet_item_id']} runtime_status must be not_runtime")
        if row["student_facing_status"] != "not_student_facing":
            _fail(f"{row['packet_item_id']} student_facing_status must be not_student_facing")

    items = obs_payload.get("items")
    if not isinstance(items, list) or len(items) != 5:
        _fail("observation evidence JSON must contain exactly five item rows")
    for item in items:
        if item.get("packet_item_id") not in EXPECTED_PACKET_ITEMS:
            _fail("unexpected packet item in evidence JSON")
        if item.get("source_candidate_id") not in EXPECTED_SOURCE_IDS:
            _fail("unexpected source candidate in evidence JSON")
        if item.get("observed") is not True:
            _fail(f"evidence JSON item {item.get('packet_item_id')} must be observed=true")
        if item.get("reviewer_name") != "Yossi":
            _fail(f"evidence JSON item {item.get('packet_item_id')} reviewer_name must be Yossi")
        if item.get("recommended_decision") != "approve_after_observation":
            _fail(f"evidence JSON item {item.get('packet_item_id')} decision must be approve_after_observation")
        if item.get("final_internal_status") != "approved_after_internal_observation":
            _fail(f"evidence JSON item {item.get('packet_item_id')} final_internal_status mismatch")
        if item.get("reviewed_bank_status") != "not_reviewed_bank":
            _fail(f"evidence JSON item {item.get('packet_item_id')} reviewed_bank_status mismatch")
        if item.get("runtime_status") != "not_runtime":
            _fail(f"evidence JSON item {item.get('packet_item_id')} runtime_status mismatch")
        if item.get("student_facing_status") != "not_student_facing":
            _fail(f"evidence JSON item {item.get('packet_item_id')} student_facing_status mismatch")

    if completion.get("feature_name") != "perek_4_broad_vocabulary_final_internal_completion_gate":
        _fail("completion JSON feature_name mismatch")
    if completion.get("internal_observation_evidence_applied") is not True:
        _fail("completion JSON must set internal_observation_evidence_applied=true")
    if completion.get("observed_count") != 5:
        _fail("completion JSON observed_count must be 5")
    if completion.get("approved_after_observation_count") != 5:
        _fail("completion JSON approved_after_observation_count must be 5")
    if completion.get("ready_for_reviewed_bank_candidate_planning") is not True:
        _fail("completion JSON must set ready_for_reviewed_bank_candidate_planning=true")
    if completion.get("ready_for_runtime_readiness_planning") is not True:
        _fail("completion JSON must set ready_for_runtime_readiness_planning=true")
    if completion.get("ready_for_runtime_activation") is not False:
        _fail("completion JSON must keep ready_for_runtime_activation=false")
    if completion.get("runtime_activation_authorized") is not False:
        _fail("completion JSON must keep runtime_activation_authorized=false")
    if completion.get("reviewed_bank_promotion_authorized") is not False:
        _fail("completion JSON must keep reviewed_bank_promotion_authorized=false")
    if completion.get("runtime_scope_widened") is not False:
        _fail("completion JSON must keep runtime_scope_widened=false")
    if completion.get("perek_activated") is not False:
        _fail("completion JSON must keep perek_activated=false")
    if completion.get("reviewed_bank_promoted") is not False:
        _fail("completion JSON must keep reviewed_bank_promoted=false")
    if completion.get("runtime_questions_created") is not False:
        _fail("completion JSON must keep runtime_questions_created=false")
    if completion.get("runtime_content_promoted") is not False:
        _fail("completion JSON must keep runtime_content_promoted=false")
    if completion.get("student_facing_content_created") is not False:
        _fail("completion JSON must keep student_facing_content_created=false")
    if completion.get("source_truth_changed") is not False:
        _fail("completion JSON must keep source_truth_changed=false")
    if completion.get("fake_student_data_created") is not False:
        _fail("completion JSON must keep fake_student_data_created=false")
    if completion.get("raw_logs_exposed") is not False:
        _fail("completion JSON must keep raw_logs_exposed=false")
    if completion.get("validators_weakened") is not False:
        _fail("completion JSON must keep validators_weakened=false")

    included = set(completion.get("included_items", []))
    blocked = set(completion.get("still_blocked_items", []))
    if included != EXPECTED_SOURCE_IDS:
        _fail("completion JSON included_items mismatch")
    if not EXPECTED_BLOCKED.issubset(blocked):
        _fail("completion JSON still_blocked_items missing required blocked rows")

    readiness_rows = _rows(READINESS_TSV)
    if len(readiness_rows) != 12:
        _fail("readiness register TSV must contain 12 rows")

    readiness_obs = [row for row in readiness_rows if row.get("block_type") == "observed"]
    if len(readiness_obs) != 5:
        _fail("readiness register must include exactly five observed rows")

    readiness_blocked = [row for row in readiness_rows if row.get("block_type") in {"revision_required", "held"}]
    if len(readiness_blocked) != 7:
        _fail("readiness register must include exactly seven blocked rows")

    obs_payload_rows = {row["source_candidate_id"] for row in readiness_rows if row.get("block_type") == "observed"}
    if obs_payload_rows != EXPECTED_SOURCE_IDS:
        _fail("readiness register observed source IDs mismatch")

    blocked_rows = {row["source_candidate_id"] for row in readiness_rows if row.get("block_type") in {"revision_required", "held"}}
    if not EXPECTED_BLOCKED.issubset(blocked_rows):
        _fail("readiness register missing required blocked IDs")

    for row in readiness_rows:
        if row.get("block_type") == "observed":
            if row.get("gate_readiness") != "ready_for_reviewed_bank_candidate_planning":
                _fail(f"observed readiness row {row.get('source_candidate_id')} must be ready_for_reviewed_bank_candidate_planning")
            if row.get("reviewed_bank_status") != "not_reviewed_bank":
                _fail(f"observed readiness row {row.get('source_candidate_id')} reviewed_bank_status mismatch")
            if row.get("runtime_status") != "not_runtime":
                _fail(f"observed readiness row {row.get('source_candidate_id')} runtime_status mismatch")
            if row.get("runtime_activation_authorized") != "false":
                _fail(f"observed readiness row {row.get('source_candidate_id')} runtime_activation_authorized must be false")
        if row.get("block_type") in {"revision_required", "held"}:
            if row.get("reviewed_bank_status") != "not_reviewed_bank":
                _fail(f"blocked readiness row {row.get('source_candidate_id')} must keep not_reviewed_bank")
            if row.get("runtime_status") != "not_runtime":
                _fail(f"blocked readiness row {row.get('source_candidate_id')} must keep not_runtime")
            if row.get("runtime_activation_authorized") != "false":
                _fail(f"blocked readiness row {row.get('source_candidate_id')} runtime_activation_authorized must be false")

    readiness_payload_rows = readiness.get("items")
    if not isinstance(readiness_payload_rows, list) or len(readiness_payload_rows) != 12:
        _fail("readiness register JSON must contain 12 item rows")

    readiness_included = {
        item["source_candidate_id"]
        for item in readiness_payload_rows
        if isinstance(item, dict) and item.get("block_type") == "observed"
    }
    readiness_blocked_payload = {
        item["source_candidate_id"]
        for item in readiness_payload_rows
        if isinstance(item, dict) and item.get("block_type") in {"revision_required", "held"}
    }
    if readiness_included != EXPECTED_SOURCE_IDS:
        _fail("readiness JSON observed included IDs mismatch")
    if not EXPECTED_BLOCKED.issubset(readiness_blocked_payload):
        _fail("readiness JSON missing blocked IDs")

    if readiness.get("ready_for_reviewed_bank_candidate_planning") is not True:
        _fail("readiness register JSON must set ready_for_reviewed_bank_candidate_planning=true")
    if readiness.get("ready_for_runtime_readiness_planning") is not True:
        _fail("readiness register JSON must set ready_for_runtime_readiness_planning=true")
    if readiness.get("ready_for_runtime_activation") is not False:
        _fail("readiness register JSON must keep ready_for_runtime_activation=false")
    if readiness.get("runtime_activation_authorized") is not False:
        _fail("readiness register JSON must keep runtime_activation_authorized=false")

    if not (
        {"bsvb_p4_002", "svqcl_p4_004"} <= set(main_contract.get("excluded_revision_required_ids", []))
    ):
        _fail("main packet contract must preserve revision-required exclusions")
    if not (
        {"bsvb_p4_003", "bsvb_p4_004", "svqcl_p4_007", "svqcl_p4_008", "svqcl_p4_009"} <= set(main_contract.get("excluded_held_ids", []))
    ):
        _fail("main packet contract must preserve held exclusions")
    if main_contract.get("ready_for_runtime_activation") is not False:
        _fail("main packet contract must keep ready_for_runtime_activation=false")

    scanned = "\n".join([
        _read_text(path).lower()
        for path in [COMPLETION_MD, COMPLETION_JSON, OBS_TSV, OBS_JSON, READINESS_TSV, READINESS_JSON]
    ])
    for phrase in FORBIDDEN_PHRASES:
        if phrase in scanned:
            _fail(f"forbidden phrase found in artifacts: {phrase}")

    if not NEXT_PROMPT_REVIEWED_BANK.exists() or not NEXT_PROMPT_RUNTIME.exists():
        _fail("both next-branch prompts must exist")

    print("Perek 4 broad vocabulary final observation gate validation passed.")


if __name__ == "__main__":
    validate()
