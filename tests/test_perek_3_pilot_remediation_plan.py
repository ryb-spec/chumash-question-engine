import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN_MD = ROOT / "data/pipeline_rounds/perek_3_pilot_remediation_plan_2026_04_29.md"
PLAN_JSON = ROOT / "data/pipeline_rounds/perek_3_pilot_remediation_plan_2026_04_29.json"
CHECKLIST_MD = ROOT / "data/pipeline_rounds/perek_3_pilot_teacher_decision_checklist_2026_04_29.md"
SEQUENCE_MD = ROOT / "data/pipeline_rounds/perek_3_pilot_remediation_sequence_2026_04_29.md"
VALIDATOR = ROOT / "scripts/validate_perek_3_pilot_remediation_plan.py"

REQUIRED_ISSUE_IDS = {
    "p3_pilot_001_form_wording",
    "p3_pilot_002_prefix_prompt_wording",
    "p3_pilot_003_ashis_shis_source_followup",
    "p3_pilot_004_derech_distractors",
    "p3_pilot_005_arurah_distractors",
    "p3_pilot_006_phrase_translation_distractor_audit",
}


def test_remediation_artifacts_exist():
    for path in [PLAN_MD, PLAN_JSON, CHECKLIST_MD, SEQUENCE_MD, VALIDATOR]:
        assert path.exists(), path


def test_remediation_json_safety_and_issue_ids():
    data = json.loads(PLAN_JSON.read_text(encoding="utf-8"))
    assert data["no_runtime_change_in_this_task"] is True
    assert data["perek_4_activated"] is False
    assert data["runtime_scope_widened"] is False
    assert data["fake_data_created"] is False
    issue_ids = {issue["issue_id"] for issue in data["remediation_issues"]}
    assert REQUIRED_ISSUE_IDS <= issue_ids


def test_required_examples_are_present():
    text = PLAN_MD.read_text(encoding="utf-8")
    required = [
        "What form is shown?",
        "בְּאִשְׁתּוֹ",
        "אָשִׁית",
        "שית",
        "דֶּרֶךְ",
        "אֲרוּרָה",
        "phrase-translation",
    ]
    for phrase in required:
        assert phrase in text


def test_validator_passes():
    result = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Perek 3 pilot remediation plan validation passed." in result.stdout
