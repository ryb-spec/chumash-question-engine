import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import standard_3_local_test_harness as harness


REPO_ROOT = Path(__file__).resolve().parents[1]
ACTIVE_SCOPE_PATH = REPO_ROOT / "data" / "active_scope_reviewed_questions.json"
STAGED_REVIEWED_PATHS = tuple((REPO_ROOT / "data" / "staged").glob("*/reviewed_questions.json"))


def file_digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Standard3LocalTestHarnessTests(unittest.TestCase):
    def test_harness_refuses_to_run_when_flag_is_off(self):
        with self.assertRaises(harness.Standard3LocalHarnessError):
            harness.load_harness_records(env={})

    def test_cli_refuses_to_run_when_flag_is_off(self):
        with mock.patch("sys.stderr") as stderr:
            exit_code = harness.main(["--summary"], env={})
        self.assertEqual(exit_code, 2)
        self.assertTrue(stderr.write.called)

    def test_harness_runs_when_flag_is_on(self):
        records = harness.load_harness_records(env={"STANDARD_3_MVP_TEST_MODE": "1"})
        self.assertEqual(len(records), 10)

    def test_summary_output_includes_exactly_ten_records_and_boundaries(self):
        records = harness.load_harness_records(env={"STANDARD_3_MVP_TEST_MODE": "true"})
        output = harness.render_summary(records)

        self.assertIn("Teacher/admin review only.", output)
        self.assertIn("Runtime activation: blocked.", output)
        self.assertIn("Student-facing use: blocked.", output)
        self.assertIn("Active scope: untouched.", output)
        self.assertIn("Staged reviewed questions: untouched.", output)
        self.assertIn("Record count: 10", output)
        item_lines = [line for line in output.splitlines() if line.startswith("Record ") and "/" in line]
        self.assertEqual(len(item_lines), 10)

    def test_summary_output_includes_required_record_fields(self):
        records = harness.load_harness_records(env={"STANDARD_3_MVP_TEST_MODE": "on"})
        output = harness.render_summary(records)

        for field in harness.REQUIRED_OUTPUT_FIELDS:
            self.assertIn(f"{field}:", output)
        self.assertIn("STD3-MVP-RB-001", output)
        self.assertIn("standard_3_mvp_test_mode", output)

    def test_report_output_is_non_runtime_and_teacher_admin_only(self):
        records = harness.load_harness_records(env={"STANDARD_3_MVP_TEST_MODE": "yes"})
        report = harness.render_markdown_report(records)

        self.assertIn("Teacher/admin review only.", report)
        self.assertIn("- Runtime activation: blocked", report)
        self.assertIn("- Student-facing use: blocked", report)
        self.assertIn("- Active scope: untouched", report)
        self.assertIn("- Staged reviewed questions: untouched", report)
        self.assertIn("Record count: 10", report)
        self.assertEqual(report.count("## Record "), 10)

    def test_write_report_creates_only_requested_review_output(self):
        records = harness.load_harness_records(env={"STANDARD_3_MVP_TEST_MODE": "1"})
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "standard_3_local_review.md"
            written = harness.write_markdown_report(records, output_path)

            self.assertEqual(written, output_path)
            text = output_path.read_text(encoding="utf-8")
            self.assertIn("local review-only harness output", text)
            self.assertIn("Question-ready status: not granted", text)

    def test_active_scope_and_staged_files_are_not_modified(self):
        before = {ACTIVE_SCOPE_PATH: file_digest(ACTIVE_SCOPE_PATH)}
        before.update({path: file_digest(path) for path in STAGED_REVIEWED_PATHS})

        records = harness.load_harness_records(env={"STANDARD_3_MVP_TEST_MODE": "1"})
        harness.render_summary(records)
        with tempfile.TemporaryDirectory() as temp_dir:
            harness.write_markdown_report(records, Path(temp_dir) / "review.md")

        after = {path: file_digest(path) for path in before}
        self.assertEqual(after, before)

    def test_no_student_facing_or_runtime_active_status_appears(self):
        records = harness.load_harness_records(env={"STANDARD_3_MVP_TEST_MODE": "1"})
        statuses = "\n".join(harness.render_summary(records).splitlines())

        self.assertIn("runtime_status: not_runtime_active", statuses)
        self.assertIn("student_facing_status: not_student_facing", statuses)
        self.assertNotIn("runtime_status: runtime_active", statuses)
        self.assertNotIn("student_facing_status: student_facing", statuses)

    def test_harness_uses_loader_function(self):
        fake_records = [
            {
                "reviewed_id": "fake-1",
                "source_record_id": "fake-source-1",
                "question": "Fake local review prompt?",
                "correct_answer": "Fake answer",
                "skill": "fake_skill",
                "question_type": "fake_question_type",
                "mode": "standard_3_mvp_test_mode",
                "runtime_status": "not_runtime_active",
                "student_facing_status": "not_student_facing",
                "test_mode_only": True,
            }
        ] * 10
        with mock.patch.object(harness, "load_standard_3_test_mode_records", return_value=fake_records) as loader:
            records = harness.load_harness_records(env={"STANDARD_3_MVP_TEST_MODE": "1"})

        loader.assert_called_once_with(env={"STANDARD_3_MVP_TEST_MODE": "1"})
        self.assertEqual(records, fake_records)

    def test_harness_rejects_unexpected_record_count(self):
        with mock.patch.object(harness, "load_standard_3_test_mode_records", return_value=[]):
            with self.assertRaises(harness.Standard3LocalHarnessError):
                harness.load_harness_records(env={"STANDARD_3_MVP_TEST_MODE": "1"})


if __name__ == "__main__":
    unittest.main()
