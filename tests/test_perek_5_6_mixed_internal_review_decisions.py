from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
from scripts import validate_perek_5_6_mixed_internal_review_decisions as validator
ROOT=Path(__file__).resolve().parents[1]
def load_contract():
    return json.loads(validator.PHASE_JSON.read_text(encoding="utf-8"))
def test_json_parses_and_phase_7_contract():
    payload=load_contract(); assert payload["streamlined_process_version"]=="v1"; assert payload["phase_number"]==7; assert payload["phase_name"]=="Observation Decisions + Next-Gate Authorization"; assert payload["item_count"]==5; assert payload["clean_approved_count"]==2; assert payload["revision_watch_count"]==3; assert payload["excluded_count"]==7
def test_exact_decisions():
    decisions={d["source_candidate_id"]:d["internal_review_decision"] for d in load_contract()["decisions"]}; assert decisions==validator.EXPECTED_DECISIONS
def test_clean_approved_lane_has_only_sefer_and_ben():
    clean=[d for d in load_contract()["decisions"] if d["lane"]=="clean_approved"]; assert [d["source_candidate_id"] for d in clean]==validator.EXPECTED_CLEAN_IDS; assert {d["hebrew_target"] for d in clean}=={"סֵפֶר","בֵּן"}; assert all(d["next_gate_status"]=="clean_limited_internal_preview_ready" for d in clean)
def test_revision_watch_lane_has_only_selected_perek_6_items():
    watch=[d for d in load_contract()["decisions"] if d["lane"]=="revision_watch"]; assert [d["source_candidate_id"] for d in watch]==validator.EXPECTED_REVISION_IDS; assert {d["hebrew_target"] for d in watch}=={"בָשָׂר","פֶתַח","מַבּוּל"}; assert all(d["next_gate_status"]=="revision_watch_internal_observation_only" for d in watch)
def test_excluded_items_remain_excluded():
    payload=load_contract(); excluded={e["source_candidate_id"] for e in payload["excluded_candidates"]}; included={d["source_candidate_id"] for d in payload["decisions"]}; assert excluded==set(validator.EXPECTED_EXCLUDED_IDS); assert included.isdisjoint(excluded); assert all(e["eligible_for_next_gate"] is False for e in payload["excluded_candidates"])
def test_no_fake_observations_and_all_gates_false():
    payload=load_contract(); assert payload["fake_observations_created"] is False; assert payload["student_observation_evidence_recorded"] is False; assert payload["runtime_scope_widened"] is False; assert payload["reviewed_bank_promoted"] is False; assert payload["student_facing_created"] is False; assert payload["perek_5_activated"] is False; assert payload["perek_6_activated"] is False
    for decision in payload["decisions"]:
        for field in validator.FALSE_FIELDS: assert decision[field] is False
        assert decision["observation_required_before_broader_use"] is True
def test_validator_function_passes():
    result=validator.validate(); assert result["ok"], result["errors"]
def test_validator_script_passes():
    result=subprocess.run([sys.executable,str(ROOT/"scripts/validate_perek_5_6_mixed_internal_review_decisions.py")],cwd=ROOT,capture_output=True,text=True,check=False,encoding="utf-8"); assert result.returncode==0,result.stdout+result.stderr; assert "Perek 5–6 mixed internal review decisions validation passed." in result.stdout
