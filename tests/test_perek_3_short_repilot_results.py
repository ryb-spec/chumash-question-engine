from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts import validate_perek_3_short_repilot_results as validator


ROOT = Path(__file__).resolve().parents[1]


def test_short_repilot_result_artifacts_exist():
    for path in validator.REQUIRED_FILES:
        assert path.exists(), path


def test_short_repilot_results_json_safety_and_findings():
    payload = json.loads(validator.RESULTS_JSON.read_text(encoding="utf-8"))
    assert payload["raw_logs_used"] is True
    assert payload["raw_logs_manually_modified"] is False
    assert payload["answered_attempts_reviewed"] == 8
    assert payload["excluded_content_scope_leak_count"] == 2
    assert payload["wording_regression_event_count"] == 1
    assert payload["perek_4_content_served"] is False
    assert payload["perek_4_activated"] is False
    assert payload["runtime_scope_widened"] is False
    assert payload["reviewed_bank_promoted"] is False
    assert payload["fake_data_created"] is False
    finding_ids = {finding["finding_id"] for finding in payload["findings"]}
    assert "p3_short_repilot_leak_001" in finding_ids
    assert "p3_short_repilot_leak_002" in finding_ids
    assert "p3_short_repilot_wording_001" in finding_ids


def test_perek_4_ready_gate_is_not_open():
    payload = json.loads(validator.PEREK_4_GATE_JSON.read_text(encoding="utf-8"))
    assert payload["scope_leaks_detected"] is True
    assert payload["perek_3_full_closure_go"] is False
    assert payload["perek_3_runtime_expansion_go"] is False
    assert payload["perek_4_teacher_review_packet_go"] is False
    assert payload["perek_4_activated"] is False
    assert payload["perek_4_runtime_activation_go"] is False
    assert payload["perek_4_reviewed_bank_promotion_go"] is False
    assert payload["perek_4_student_facing_go"] is False


def test_reports_include_scope_leak_and_wording_evidence():
    results_text = validator.RESULTS_MD.read_text(encoding="utf-8")
    leak_text = validator.LEAK_REPORT.read_text(encoding="utf-8")
    assert "phrase_translation" in results_text
    assert "What is the prefix in בְּאִשְׁתּוֹ?" in results_text
    assert "Ready for full Perek 3 closure: no" in results_text
    assert "וְאֵיבָה אָשִׁית" in leak_text
    assert "Perek 4 content was not observed" in leak_text


def test_validator_passes_as_script():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_perek_3_short_repilot_results.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "validation passed" in result.stdout


def test_validator_function_passes():
    result = validator.validate()
    assert result["ok"], result["errors"]
