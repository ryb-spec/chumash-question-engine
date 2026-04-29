from __future__ import annotations

import csv
import unittest
from pathlib import Path

import scripts.validate_question_eligibility_audit as validator


ROOT = Path(__file__).resolve().parents[1]
AUDIT_DIR = ROOT / "data" / "question_eligibility_audits"
AUDIT_PATH = AUDIT_DIR / "bereishis_perek_1_question_eligibility_audit.tsv"
REPORT_PATH = AUDIT_DIR / "reports" / "bereishis_perek_1_question_eligibility_audit_report.md"
REVIEW_MD_PATH = AUDIT_DIR / "reports" / "bereishis_perek_1_question_eligibility_yossi_review_sheet.md"
REVIEW_CSV_PATH = AUDIT_DIR / "reports" / "bereishis_perek_1_question_eligibility_yossi_review_sheet.csv"
APPLIED_REPORT_PATH = AUDIT_DIR / "reports" / "bereishis_perek_1_question_eligibility_yossi_review_applied.md"
PLANNING_MD_PATH = AUDIT_DIR / "reports" / "bereishis_perek_1_approved_input_candidate_planning_sheet.md"
PLANNING_CSV_PATH = AUDIT_DIR / "reports" / "bereishis_perek_1_approved_input_candidate_planning_sheet.csv"


def load_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


class QuestionEligibilityAuditTests(unittest.TestCase):
    def test_validator_passes(self):
        summary = validator.validate_question_eligibility_audit()
        self.assertTrue(summary["valid"], summary["errors"])
        self.assertEqual(summary["audit_row_count"], 299)
        self.assertEqual(summary["verified_enrichment_rows_considered"], 164)
        self.assertEqual(
            summary["audit_path"],
            "data/question_eligibility_audits/bereishis_perek_1_question_eligibility_audit.tsv",
        )
        self.assertEqual(summary["decision_counts"]["approve_as_input_candidate"], 133)
        self.assertEqual(summary["decision_counts"]["needs_follow_up"], 155)
        self.assertEqual(summary["decision_counts"]["source_only"], 6)
        self.assertEqual(summary["decision_counts"]["block_for_questions"], 5)
        self.assertEqual(summary["planning_sheet_row_count"], 133)

    def test_artifacts_exist(self):
        self.assertTrue((AUDIT_DIR / "README.md").exists())
        self.assertTrue(AUDIT_PATH.exists())
        self.assertTrue(REPORT_PATH.exists())
        self.assertTrue(REVIEW_MD_PATH.exists())
        self.assertTrue(REVIEW_CSV_PATH.exists())
        self.assertTrue(APPLIED_REPORT_PATH.exists())
        self.assertTrue(PLANNING_MD_PATH.exists())
        self.assertTrue(PLANNING_CSV_PATH.exists())

    def test_audit_rows_keep_all_gates_closed_and_review_applied(self):
        rows = load_tsv(AUDIT_PATH)
        self.assertEqual(len(rows), 299)
        for row in rows:
            with self.subTest(audit_id=row["audit_id"]):
                self.assertEqual(row["question_allowed"], "needs_review")
                self.assertEqual(row["protected_preview_allowed"], "false")
                self.assertEqual(row["reviewed_bank_allowed"], "false")
                self.assertEqual(row["runtime_allowed"], "false")
                self.assertIn(
                    row["yossi_question_review_decision"],
                    {"approve_as_input_candidate", "needs_follow_up", "source_only", "block_for_questions"},
                )
                self.assertNotEqual(row["yossi_question_review_notes"], "")

    def test_forbidden_approval_language_does_not_appear_in_audit_rows(self):
        forbidden = {
            "question_ready",
            "protected_preview_ready",
            "reviewed_bank_ready",
            "runtime_ready",
            "student_facing",
            "approved_for_questions",
            "approved_for_preview",
        }
        for row in load_tsv(AUDIT_PATH):
            joined = " ".join(row.values()).lower()
            for phrase in forbidden:
                with self.subTest(audit_id=row["audit_id"], phrase=phrase):
                    self.assertNotIn(phrase, joined)

    def test_eligible_rows_come_only_from_verified_enrichment(self):
        rows = load_tsv(AUDIT_PATH)
        eligible = [row for row in rows if row["eligibility_recommendation"] == "eligible_candidate_for_yossi_question_review"]
        self.assertGreater(len(eligible), 0)
        for row in eligible:
            with self.subTest(audit_id=row["audit_id"]):
                self.assertEqual(row["enrichment_review_status"], "yossi_enrichment_verified")
                self.assertNotEqual(row["proposed_question_family"], "not_recommended")
                if row["source_candidate_type"] == "token_split_standards":
                    self.assertNotEqual(row["canonical_skill_id"], "")
                    self.assertNotEqual(row["canonical_standard_anchor"], "")

    def test_first_pass_decision_counts_and_deferred_verb_forms(self):
        rows = load_tsv(AUDIT_PATH)
        decisions = {}
        for row in rows:
            decisions[row["yossi_question_review_decision"]] = decisions.get(row["yossi_question_review_decision"], 0) + 1
        self.assertEqual(decisions["approve_as_input_candidate"], 133)
        self.assertEqual(decisions["needs_follow_up"], 155)
        self.assertEqual(decisions["source_only"], 6)
        self.assertEqual(decisions["block_for_questions"], 5)

        approved_families = {}
        for row in rows:
            if row["yossi_question_review_decision"] == "approve_as_input_candidate":
                approved_families[row["proposed_question_family"]] = approved_families.get(row["proposed_question_family"], 0) + 1
        self.assertEqual(approved_families["vocabulary_meaning"], 56)
        self.assertEqual(approved_families["basic_noun_recognition"], 60)
        self.assertEqual(approved_families["direct_object_marker_recognition"], 14)
        self.assertEqual(approved_families["shoresh_identification"], 3)
        self.assertNotIn("basic_verb_form_recognition", approved_families)

        verb_rows = [row for row in rows if row["proposed_question_family"] == "basic_verb_form_recognition"]
        self.assertEqual(len(verb_rows), 25)
        self.assertTrue(all(row["yossi_question_review_decision"] == "needs_follow_up" for row in verb_rows))

    def test_follow_up_rows_do_not_recommend_question_family(self):
        for row in load_tsv(AUDIT_PATH):
            if row["eligibility_recommendation"] == "needs_follow_up":
                with self.subTest(audit_id=row["audit_id"]):
                    self.assertEqual(row["proposed_question_family"], "not_recommended")

    def test_review_csv_is_utf8_bom_and_contains_eligible_and_blocked_rows(self):
        self.assertTrue(REVIEW_CSV_PATH.read_bytes().startswith(b"\xef\xbb\xbf"))
        audit_rows = load_tsv(AUDIT_PATH)
        required_ids = {
            row["audit_id"]
            for row in audit_rows
            if row["eligibility_recommendation"]
            in {"eligible_candidate_for_yossi_question_review", "blocked_for_questions"}
        }
        with REVIEW_CSV_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
            review_rows = list(csv.DictReader(handle))
        self.assertEqual(list(review_rows[0].keys()), validator.REVIEW_COLUMNS)
        self.assertTrue(required_ids.issubset({row["audit_id"] for row in review_rows}))

    def test_hebrew_integrity_checks_pass(self):
        for row in load_tsv(AUDIT_PATH):
            with self.subTest(audit_id=row["audit_id"]):
                self.assertNotIn("???", row["hebrew_token"])
                self.assertNotIn("???", row["hebrew_phrase"])
        self.assertNotIn("???", REVIEW_MD_PATH.read_text(encoding="utf-8"))

    def test_planning_sheet_is_utf8_bom_and_matches_approved_rows(self):
        self.assertTrue(PLANNING_CSV_PATH.read_bytes().startswith(b"\xef\xbb\xbf"))
        audit_rows = load_tsv(AUDIT_PATH)
        approved_ids = {
            row["audit_id"] for row in audit_rows if row["yossi_question_review_decision"] == "approve_as_input_candidate"
        }
        with PLANNING_CSV_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
            planning_rows = list(csv.DictReader(handle))
        self.assertEqual(list(planning_rows[0].keys()), validator.PLANNING_COLUMNS)
        self.assertEqual(len(planning_rows), 133)
        self.assertEqual({row["audit_id"] for row in planning_rows}, approved_ids)
        self.assertTrue(all(row["future_template_needed"] == "true" for row in planning_rows))
        self.assertTrue(all(row["future_wording_review_required"] == "true" for row in planning_rows))
        planning_text = PLANNING_MD_PATH.read_text(encoding="utf-8")
        self.assertIn("This is a planning sheet only.", planning_text)
        self.assertIn("not a protected-preview input list", planning_text)
        self.assertNotIn("protected_preview_ready", planning_text)

    def test_report_counts_match_validator_summary(self):
        summary = validator.validate_question_eligibility_audit()
        report_text = REPORT_PATH.read_text(encoding="utf-8")
        self.assertIn(f"- total enrichment candidates considered: {summary['audit_row_count']}", report_text)
        self.assertIn(
            f"- total verified enrichment candidates considered: {summary['verified_enrichment_rows_considered']}",
            report_text,
        )
        for label, count in summary["recommendation_counts"].items():
            self.assertIn(f"- {label}: {count}", report_text)
        for label, count in summary["question_family_counts"].items():
            self.assertIn(f"- {label}: {count}", report_text)
        applied_text = APPLIED_REPORT_PATH.read_text(encoding="utf-8")
        self.assertIn("- approved input-candidate count: 133", applied_text)
        self.assertIn("- needs_follow_up count: 155", applied_text)
        self.assertIn("- source_only count: 6", applied_text)
        self.assertIn("- blocked_for_questions count: 5", applied_text)
        self.assertIn("approved input candidates are not approved questions", applied_text)


if __name__ == "__main__":
    unittest.main()
