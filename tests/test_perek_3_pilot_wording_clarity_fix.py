import subprocess
import sys
from pathlib import Path

from assessment_scope import active_pesukim_records
from pasuk_flow_generator import generate_question

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data/pipeline_rounds/perek_3_pilot_wording_clarity_fix_report_2026_04_29.md"
VALIDATOR = ROOT / "scripts/validate_perek_3_pilot_wording_clarity_fix.py"
FLOW_BUILDER = ROOT / "engine/flow_builder.py"


def pasuk_by_ref(perek, pasuk):
    for record in active_pesukim_records():
        ref = record.get("ref", {})
        if ref.get("perek") == perek and ref.get("pasuk") == pasuk:
            return record["text"]
    raise AssertionError(f"Missing active pasuk {perek}:{pasuk}")


def test_wording_clarity_report_exists_and_has_safety_phrases():
    text = REPORT.read_text(encoding="utf-8")
    assert "No runtime scope expansion." in text
    assert "No Perek 4 activation." in text
    assert "No distractor changes in this task." in text
    assert "What tense or verb form is this word?" in text
    assert "which beginning letter is the prefix" in text


def test_active_prompt_code_no_longer_uses_old_wording():
    text = FLOW_BUILDER.read_text(encoding="utf-8")
    assert "What form is shown?" not in text
    assert "What is the prefix in" not in text
    assert "What tense or verb form is this word?" in text
    assert "which beginning letter is the prefix" in text


def test_generated_verb_tense_question_uses_clearer_wording():
    question = generate_question("identify_tense", pasuk_by_ref(1, 6))
    assert question.get("status") != "skipped"
    assert question.get("question") == "What tense or verb form is this word?"
    assert question.get("choices")


def test_generated_prefix_question_uses_clearer_wording():
    question = generate_question("identify_prefix_meaning", "לָאוֹר")
    assert question.get("status") != "skipped"
    assert question.get("question") == "In לָאוֹר, which beginning letter is the prefix?"
    assert question.get("correct_answer") == "ל"
    assert "What is the prefix in" not in question.get("question", "")


def test_perek_4_not_activated_in_runtime_scope():
    assert all(record.get("ref", {}).get("perek") != 4 for record in active_pesukim_records())


def test_validator_passes():
    result = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Perek 3 pilot wording clarity fix validation passed." in result.stdout
