from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
from scripts import validate_streamlined_review_process as validator
ROOT=Path(__file__).resolve().parents[1]
def test_json_parses_and_has_seven_phases():
    data=json.loads(validator.PROCESS_JSON.read_text(encoding="utf-8")); assert len(data["phases"])==7
def test_target_reduction_at_least_35():
    data=json.loads(validator.PROCESS_JSON.read_text(encoding="utf-8")); assert data["target_step_reduction_percent"]>=35
def test_required_templates_exist():
    for name in validator.REQUIRED_TEMPLATES: assert (validator.TEMPLATE_DIR/name).exists()
def test_required_prompt_templates_exist():
    for name in validator.REQUIRED_PROMPTS: assert (validator.PROMPT_TEMPLATE_DIR/name).exists()
def test_required_safety_gates_are_listed():
    data=json.loads(validator.PROCESS_JSON.read_text(encoding="utf-8")); gates=set(data["non_negotiable_gates"])
    for gate in validator.REQUIRED_GATES: assert gate in gates
def test_tightening_rules_are_included():
    data=json.loads(validator.PROCESS_JSON.read_text(encoding="utf-8")); rules=set(data["tightening_rules"])
    for rule in validator.TIGHTENING: assert rule in rules
def test_validator_function_passes():
    result=validator.validate(); assert result["ok"], result["errors"]; assert result["phase_count"]==7; assert result["target_step_reduction_percent"]>=35
def test_validator_passes_as_script():
    result=subprocess.run([sys.executable,str(ROOT/"scripts/validate_streamlined_review_process.py")],cwd=ROOT,capture_output=True,text=True,check=False)
    assert result.returncode==0, result.stdout+result.stderr
    assert "Streamlined review process validation passed." in result.stdout
