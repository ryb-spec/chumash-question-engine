from __future__ import annotations
import json,subprocess,sys
from pathlib import Path
from scripts import validate_perek_5_6_mixed_internal_review_packet as validator
ROOT=Path(__file__).resolve().parents[1]
def test_packet_files_exist():
    for path in validator.REQUIRED_FILES: assert path.exists(), path
def test_packet_json_parses_and_has_exact_five_items():
    p=json.loads(validator.PACKET_JSON.read_text(encoding="utf-8")); assert p["packet_status"]=="mixed_limited_internal_review_only"; assert p["item_count"]==5; assert p["included_candidate_ids"]==validator.EXPECTED_INCLUDED_IDS; assert [i["source_candidate_id"] for i in p["items"]]==validator.EXPECTED_INCLUDED_IDS
def test_clean_lane_has_only_sefer_and_ben():
    p=json.loads(validator.PACKET_JSON.read_text(encoding="utf-8")); clean=[i for i in p["items"] if i["lane"]=="clean_approved"]; assert [i["source_candidate_id"] for i in clean]==validator.EXPECTED_CLEAN_IDS; assert {i["hebrew_target"] for i in clean}=={"\u05e1\u05b5\u05e4\u05b6\u05e8", "\u05d1\u05bc\u05b5\u05df"}
def test_revision_watch_lane_has_only_selected_perek_6_items():
    p=json.loads(validator.PACKET_JSON.read_text(encoding="utf-8")); watch=[i for i in p["items"] if i["lane"]=="revision_watch"]; assert [i["source_candidate_id"] for i in watch]==validator.EXPECTED_REVISION_WATCH_IDS; assert {i["hebrew_target"] for i in watch}=={"\u05d1\u05b8\u05e9\u05c2\u05b8\u05e8", "\u05e4\u05b6\u05ea\u05b7\u05d7", "\u05de\u05b7\u05d1\u05bc\u05d5\u05bc\u05dc"}; assert all("not clean-approved" in i["required_caution"] for i in watch)
def test_excluded_items_are_excluded():
    p=json.loads(validator.PACKET_JSON.read_text(encoding="utf-8")); included={i["source_candidate_id"] for i in p["items"]}; assert sorted(p["excluded_candidate_ids"])==sorted(validator.EXPECTED_EXCLUDED_IDS); assert included.isdisjoint(validator.EXPECTED_EXCLUDED_IDS)
def test_all_gates_false_and_internal_decisions_null():
    p=json.loads(validator.PACKET_JSON.read_text(encoding="utf-8")); assert p["fake_review_decisions_created"] is False; assert p["fake_student_data_created"] is False; assert p["source_truth_changed"] is False; assert p["question_selection_changed"] is False; assert p["scoring_mastery_changed"] is False
    for i in p["items"]:
        assert i["internal_review_decision"] is None
        for f in validator.FALSE_FIELDS: assert i[f] is False
def test_validator_passes_as_script():
    r=subprocess.run([sys.executable,str(ROOT/"scripts/validate_perek_5_6_mixed_internal_review_packet.py")],cwd=ROOT,capture_output=True,text=True,check=False); assert r.returncode==0,r.stdout+r.stderr; assert "validation passed" in r.stdout
def test_validator_function_passes():
    r=validator.validate(); assert r["ok"], r["errors"]; assert r["tsv_candidate_ids"]==validator.EXPECTED_INCLUDED_IDS; assert r["json_candidate_ids"]==validator.EXPECTED_INCLUDED_IDS
