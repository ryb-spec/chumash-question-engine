from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data" / "expansion_governance" / "streamlined_expansion_contract.json"


def load_contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def test_contract_file_exists() -> None:
    assert CONTRACT.exists()


def test_approval_status_ladder_is_present() -> None:
    data = load_contract()
    assert data["approval_status_ladder"] == [
        "planning_only",
        "word_level_candidate",
        "word_level_approved",
        "simple_question_candidate",
        "teacher_review_ready",
        "teacher_approved",
        "protected_preview_ready",
        "observed_internally",
        "reviewed_bank_candidate",
        "reviewed_bank_approved",
        "runtime_ready",
        "runtime_active",
    ]


def test_required_traceability_fields_are_present() -> None:
    data = load_contract()
    required = set(data["required_minimum_traceability_fields"])
    assert {
        "sefer",
        "perek",
        "pasuk",
        "hebrew_word_or_hebrew_phrase",
        "basic_gloss",
        "skill_category",
        "source_evidence",
        "review_status",
        "runtime_status",
    } <= required
    assert set(data["traceability_field_aliases"]["hebrew_word_or_hebrew_phrase"]) == {"hebrew_word", "hebrew_phrase"}


def test_forbidden_shortcuts_are_represented() -> None:
    data = load_contract()
    shortcuts = {(rule["from"], rule["to"]) for rule in data["forbidden_shortcuts"]}
    assert ("planning_only", "runtime_ready") in shortcuts
    assert ("planning_only", "runtime_active") in shortcuts
    assert ("word_level_approved", "runtime_active") in shortcuts
    assert ("simple_question_candidate", "runtime_active") in shortcuts
    assert ("protected_preview_ready", "runtime_active") in shortcuts
    assert ("reviewed_bank_candidate", "runtime_active") in shortcuts
    assert data["runtime_active_requirements"]["runtime_active_true_requires"] == [
        "reviewed_bank_approved",
        "runtime_ready",
    ]


def test_depth_ladder_is_ordered() -> None:
    data = load_contract()
    assert [item["id"] for item in data["depth_ladder"]] == [
        "single_word_vocabulary",
        "word_function",
        "shoresh_or_morphology",
        "phrase_translation",
        "pasuk_comprehension",
        "rashi_or_deeper_pshat",
    ]
    assert [item["stage"] for item in data["depth_ladder"]] == [1, 2, 3, 4, 5, 6]
    assert data["depth_ladder"][-1]["late_stage_only"] is True
    assert data["depth_gate"]["stage_2_plus_minimum_base_word_evidence"] == [
        "word_level_approved",
        "simple_question_reviewed_or_teacher_approved",
        "observed_internally",
    ]


def test_planning_only_defaults_are_represented() -> None:
    data = load_contract()
    rule = data["planning_only_rule"]
    assert rule["future_perek_discovery_files_allowed"] is True
    assert rule["default_status"] == "planning_only"
    assert rule["required_closed_fields"] == {
        "runtime_allowed": False,
        "protected_preview_allowed": False,
        "reviewed_bank_allowed": False,
        "runtime_active": False,
    }
    assert rule["activation_may_not_run_ahead"] is True


def test_review_packet_types_are_represented() -> None:
    data = load_contract()
    assert set(data["review_packet_separation_rule"]["allowed_review_packet_types"]) == {
        "word_bank_review",
        "simple_question_review",
        "depth_expansion_review",
        "protected_preview_observation",
        "reviewed_bank_decision",
    }
    assert data["review_packet_separation_rule"]["mixed_packet_default_allowed"] is False
