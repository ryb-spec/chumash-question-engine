from __future__ import annotations

import csv
import unittest
from pathlib import Path

import scripts.validate_protected_preview_input_planning as validator


ROOT = Path(__file__).resolve().parents[1]
PLANNING_DIR = ROOT / "data" / "protected_preview_input_planning"
TSV_PATH = PLANNING_DIR / "bereishis_perek_1_first_input_candidate_planning.tsv"
BALANCE_REPORT_PATH = PLANNING_DIR / "reports" / "bereishis_perek_1_first_input_candidate_batch_balance_report.md"
REVIEW_MD_PATH = PLANNING_DIR / "reports" / "bereishis_perek_1_first_input_candidate_yossi_review_sheet.md"
REVIEW_CSV_PATH = PLANNING_DIR / "reports" / "bereishis_perek_1_first_input_candidate_yossi_review_sheet.csv"
APPLIED_REPORT_PATH = PLANNING_DIR / "reports" / "bereishis_perek_1_first_input_candidate_yossi_review_applied.md"
README_PATH = PLANNING_DIR / "README.md"


class ProtectedPreviewInputPlanningTests(unittest.TestCase):
    def load_rows(self):
        with TSV_PATH.open("r", encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle, delimiter="\t"))

    def test_validator_passes(self):
        summary = validator.validate_protected_preview_input_planning()
        self.assertTrue(summary["valid"], summary["errors"])
        self.assertEqual(summary["row_count"], 24)
        self.assertEqual(summary["family_counts"]["direct_object_marker_recognition"], 2)
        self.assertEqual(summary["family_counts"]["shoresh_identification"], 2)

    def test_tsv_exists_and_row_count_is_planning_batch_size(self):
        self.assertTrue(TSV_PATH.exists())
        rows = self.load_rows()
        self.assertGreaterEqual(len(rows), 20)
        self.assertLessEqual(len(rows), 30)

    def test_allowed_families_only_and_no_high_risk(self):
        rows = self.load_rows()
        families = {row["approved_family"] for row in rows}
        risks = {row["risk_level"] for row in rows}
        self.assertTrue(families.issubset(validator.ALLOWED_FAMILIES))
        self.assertNotIn("basic_verb_form_recognition", families)
        self.assertNotIn("high", risks)

    def test_no_questions_answer_choices_or_answer_keys(self):
        rows = self.load_rows()
        columns = set(rows[0].keys())
        self.assertFalse(validator.FORBIDDEN_COLUMNS & columns)

    def test_review_statuses_and_gates_remain_closed(self):
        for row in self.load_rows():
            for field in validator.REVIEW_STATUS_FIELDS:
                self.assertEqual(row[field], "needs_review")
            self.assertEqual(row["protected_preview_candidate_status"], "planning_only")
            self.assertEqual(row["yossi_input_planning_decision"], "approve_for_template_skeleton_planning")
            self.assertIn("not question approval", row["yossi_notes"])
            for gate in validator.SAFETY_GATE_FIELDS:
                self.assertEqual(row[gate], "false")

    def test_special_wording_cautions_are_preserved(self):
        rows = {row["input_candidate_id"]: row for row in self.load_rows()}
        self.assertIn("function of את", rows["ppplan_b1_021"]["yossi_notes"])
        self.assertIn("function of את", rows["ppplan_b1_022"]["yossi_notes"])
        self.assertIn("בדל", rows["ppplan_b1_024"]["yossi_notes"])
        self.assertIn("הבדיל", rows["ppplan_b1_024"]["yossi_notes"])
        for row in rows.values():
            if row["hebrew_token"] in {"המים", "האדמה", "הארץ"}:
                self.assertIn("base meaning", row["yossi_notes"])

    def test_batch_balance_report_exists_and_contains_required_fields(self):
        self.assertTrue(BALANCE_REPORT_PATH.exists())
        text = BALANCE_REPORT_PATH.read_text(encoding="utf-8").lower()
        for phrase in validator.BALANCE_REPORT_PHRASES:
            self.assertIn(phrase, text)

    def test_review_sheet_exists_and_csv_is_utf8_bom(self):
        self.assertTrue(REVIEW_MD_PATH.exists())
        self.assertTrue(REVIEW_CSV_PATH.exists())
        self.assertTrue(validator.file_has_utf8_bom(REVIEW_CSV_PATH))

    def test_review_applied_report_exists(self):
        self.assertTrue(APPLIED_REPORT_PATH.exists())
        text = APPLIED_REPORT_PATH.read_text(encoding="utf-8")
        self.assertIn("Approved for template-skeleton planning: 24", text)
        self.assertIn("No protected-preview input list was created", text)

    def test_readme_links_artifacts(self):
        readme = README_PATH.read_text(encoding="utf-8")
        for path in (TSV_PATH, BALANCE_REPORT_PATH, REVIEW_MD_PATH, REVIEW_CSV_PATH, APPLIED_REPORT_PATH):
            self.assertIn(path.relative_to(ROOT).as_posix(), readme)


if __name__ == "__main__":
    unittest.main()
