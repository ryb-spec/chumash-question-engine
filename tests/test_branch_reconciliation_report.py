from __future__ import annotations

import json
import subprocess
import sys

from scripts import validate_branch_reconciliation_report as validator


def test_branch_reconciliation_reports_exist():
    assert validator.REPORT_MD.exists()
    assert validator.REPORT_JSON.exists()


def test_branch_reconciliation_json_schema():
    payload = json.loads(validator.REPORT_JSON.read_text(encoding="utf-8"))
    assert validator.REQUIRED_TOP_LEVEL_FIELDS <= set(payload)
    assert payload["current_branch"] == "chore/branch-reconciliation-perek-3-4-baseline"
    assert payload["source_integrity"]["sha256"] == "4d96c615ab63e0419bff079db250d71ea9b5de266ff9ab8d589ae80e4afd0b71"
    assert payload["safety_boundaries"]["no_runtime_activation"] is True


def test_markdown_report_contains_safety_and_merge_order():
    text = validator.REPORT_MD.read_text(encoding="utf-8")
    assert "Source integrity result" in text
    assert "Proposed merge-forward order" in text
    assert "No runtime activation" in text
    assert "No reviewed-bank promotion" in text
    assert "No student-facing content" in text
    assert "feature/perek-4-source-discovery-inventory" in text


def test_report_does_not_claim_planned_branches_are_merged():
    text = validator.REPORT_MD.read_text(encoding="utf-8").lower()
    assert "all branches are merged" not in text


def test_validator_script_passes():
    completed = subprocess.run(
        [sys.executable, "scripts/validate_branch_reconciliation_report.py"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0
    assert "Branch reconciliation report validation passed." in completed.stdout
