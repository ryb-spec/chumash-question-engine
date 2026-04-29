from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from unittest import mock

from scripts import run_curriculum_quality_checks as quality
from scripts import validate_curriculum_extraction as curriculum_validator


ROOT = Path(__file__).resolve().parents[1]


def test_script_exists_and_default_summary_paths_are_stable():
    assert (ROOT / "scripts" / "run_curriculum_quality_checks.py").exists()
    assert quality.DEFAULT_SUMMARY_MD == Path("data/validation/curriculum_quality_check_summary.md")
    assert quality.DEFAULT_SUMMARY_JSON == Path("data/validation/curriculum_quality_check_summary.json")
    assert quality.SCHEMA_VERSION == "1.0"


def test_check_registry_includes_core_validators_that_exist():
    checks = quality.build_checks()
    commands = {" ".join(check.args) for check in checks if check.args}
    expected_scripts = [
        "scripts/validate_source_texts.py",
        "scripts/validate_bereishis_translations.py",
        "scripts/validate_verified_source_skill_maps.py",
        "scripts/validate_curriculum_extraction.py",
        "scripts/validate_standards_data.py",
        "scripts/validate_canonical_skill_contract.py",
        "scripts/validate_pipeline_rounds.py",
        "scripts/validate_gate_2_protected_preview_candidates.py",
        "scripts/validate_gate_2_protected_preview_packet.py",
        "scripts/validate_source_skill_enrichment.py",
        "scripts/validate_question_eligibility_audit.py",
    ]
    for script in expected_scripts:
        assert any(script in command for command in commands), script


def test_missing_optional_commands_skip_and_missing_required_commands_fail():
    optional = quality.CheckSpec(
        label="optional missing",
        category="test",
        args=[sys.executable, "scripts/not_a_real_optional_validator.py"],
        required=False,
    )
    required = quality.CheckSpec(
        label="required missing",
        category="test",
        args=[sys.executable, "scripts/not_a_real_required_validator.py"],
        required=True,
    )
    assert quality.run_check(optional).status == "SKIP"
    assert quality.run_check(required).status == "FAIL"


def test_required_failing_command_produces_fail_summary():
    result = quality.CheckResult(
        label="required failing",
        category="test",
        args=[sys.executable, "-c", "raise SystemExit(1)"],
        required=True,
        status="FAIL",
        exit_code=1,
        duration_seconds=0.0,
    )
    payload = quality.build_summary_payload(
        [result],
        strict=False,
        summary_md=quality.DEFAULT_SUMMARY_MD,
        summary_json=quality.DEFAULT_SUMMARY_JSON,
    )
    assert payload["overall_status"] == "FAIL"
    assert payload["counts"]["required_failed"] == 1


def test_list_checks_does_not_run_validators():
    completed = subprocess.run(
        [sys.executable, "scripts/run_curriculum_quality_checks.py", "--list-checks"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0
    assert "source text validation" in completed.stdout
    assert "diagnostic preview validation" in completed.stdout


def test_no_write_does_not_call_report_writer():
    fake_result = quality.CheckResult(
        label="fake pass",
        category="test",
        args=[sys.executable, "-c", "pass"],
        required=True,
        status="PASS",
        exit_code=0,
        duration_seconds=0.0,
    )
    with mock.patch.object(quality, "build_checks", return_value=[quality.CheckSpec("fake", "test", [])]):
        with mock.patch.object(quality, "run_check", return_value=fake_result):
            with mock.patch.object(quality, "generate_all_reports") as writer:
                assert quality.main(["--no-write"]) == 0
    writer.assert_not_called()


def test_summary_markdown_and_json_schema_include_safety_language():
    result = quality.CheckResult(
        label="fake pass",
        category="test",
        args=[sys.executable, "-c", "pass"],
        required=True,
        status="PASS",
        exit_code=0,
        duration_seconds=0.0,
    )
    payload = quality.build_summary_payload(
        [result],
        strict=False,
        summary_md=quality.DEFAULT_SUMMARY_MD,
        summary_json=quality.DEFAULT_SUMMARY_JSON,
    )
    rendered = quality.render_summary_markdown(payload)
    assert payload["schema_version"] == "1.0"
    assert isinstance(payload["checks"], list)
    assert "does not activate content" in rendered
    assert "No runtime" in rendered or "no_runtime_activation" in rendered


def test_orchestrator_does_not_run_runtime_or_generation_commands():
    forbidden_fragments = [
        "streamlit_app.py",
        "streamlit",
        "generate_question_validation_audit.py",
        "generate_diagnostic_preview.py",
        "engine/",
        "runtime/",
    ]
    for check in quality.build_checks():
        command = " ".join(check.args)
        for fragment in forbidden_fragments:
            assert fragment not in command


def test_quality_control_index_exists_and_links_reports():
    path = ROOT / "data" / "validation" / "curriculum_quality_control_index.md"
    text = path.read_text(encoding="utf-8")
    assert "Curriculum Quality Control Center" in text
    assert "curriculum_quality_check_summary.md" in text
    assert "diagnostic_preview_coverage_index.md" in text
    assert "protected_preview_source_lineage_matrix.md" in text
    assert "bereishis_perek_3_internal_protected_preview_packet_report.md" in text
    assert "bereishis_perek_3_internal_protected_preview_review_checklist.md" in text
    assert "bereishis_perek_3_internal_protected_preview_review_decisions_applied.md" in text
    assert "bereishis_perek_3_item_004_revision_plan.md" in text
    assert "non-runtime" in text
    assert "does not activate runtime" in text or "does not activate" in text


def test_perek_3_status_index_clarifies_current_status_and_packet_boundary():
    path = ROOT / "data" / "gate_2_protected_preview_candidates" / "reports" / "bereishis_perek_3_candidate_status_index.md"
    text = path.read_text(encoding="utf-8")
    assert "historical pre-decision artifact" in text
    assert "applied-decision report is the current status source" in text
    assert "four-item internal protected-preview packet now exists" in text
    assert "Internal review decisions are recorded" in text
    assert "repetition/session-balance" in text
    assert "planning-only revision plan" in text
    assert "No approve-with-revision rows were included" in text
    assert "No needs-follow-up rows were included" in text
    assert "No Perek 3 runtime activation" in text
    assert "No reviewed-bank promotion" in text
    assert "No student-facing content" in text
    assert "`approve_for_internal_protected_preview_packet`: 4" in text
    assert "`approve_with_revision`: 4" in text
    assert "`needs_follow_up`: 2" in text


def test_diagnostic_coverage_index_warnings_exist():
    text = (ROOT / "data" / "validation" / "diagnostic_preview_coverage_index.md").read_text(encoding="utf-8")
    assert "Diagnostic preview coverage index" in text
    assert "Diagnostic preview coverage does not equal runtime approval" in text
    assert "Diagnostic preview coverage does not equal reviewed-bank approval" in text


def test_source_lineage_matrix_is_audit_only_and_uses_not_available():
    text = (ROOT / "data" / "validation" / "protected_preview_source_lineage_matrix.md").read_text(encoding="utf-8")
    tsv_text = (ROOT / "data" / "validation" / "protected_preview_source_lineage_matrix.tsv").read_text(encoding="utf-8")
    assert "audit-only lineage report" in text
    assert "runtime_allowed" in tsv_text
    assert "reviewed_bank_allowed" in tsv_text
    assert "student_facing_allowed" in tsv_text
    assert "not_available" in tsv_text


def test_standards_gap_matrix_requires_teacher_review_for_final_groupings():
    text = (ROOT / "data" / "validation" / "standards_evidence_gap_matrix.md").read_text(encoding="utf-8")
    assert "Standards evidence gap matrix" in text
    assert "Canonical skill" in text
    assert "Final teacher-facing standards groupings require teacher review" in text


def test_question_quality_risk_summary_is_report_only():
    text = (ROOT / "data" / "validation" / "question_quality_risk_summary.md").read_text(encoding="utf-8")
    assert "Translation/context safe-valid rate" in text
    assert "Suffix safe-valid rate" in text
    assert "compound_morphology" in text
    assert "does not change runtime behavior" in text


def test_curriculum_extraction_allowlist_for_quality_reports_is_narrow():
    allowed = [
        "data/validation/curriculum_quality_check_summary.md",
        "data/validation/curriculum_quality_check_summary.json",
        "data/validation/curriculum_quality_control_index.md",
        "data/validation/diagnostic_preview_coverage_index.md",
        "data/validation/diagnostic_preview_coverage_index.json",
        "data/validation/protected_preview_source_lineage_matrix.md",
        "data/validation/protected_preview_source_lineage_matrix.tsv",
        "data/validation/runtime_review_exposure_index.md",
        "data/validation/runtime_review_exposure_index.json",
        "data/validation/standards_evidence_gap_matrix.md",
        "data/validation/standards_evidence_gap_matrix.json",
        "data/validation/question_quality_risk_summary.md",
        "data/validation/question_quality_risk_summary.json",
        "data/gate_2_protected_preview_candidates/reports/bereishis_perek_3_candidate_status_index.md",
    ]
    for path in allowed:
        assert curriculum_validator.is_allowed_change(path), path

    disallowed = [
        "data/validation/random_quality_report.md",
        "data/validation/random_quality_report.json",
        "AUDIT_OVERNIGHT_CURRICULUM_QUALITY_REVIEW.md",
        "streamlit_app.py",
        "engine/flow_builder.py",
        "assessment_scope.py",
    ]
    for path in disallowed:
        assert not curriculum_validator.is_allowed_change(path), path
