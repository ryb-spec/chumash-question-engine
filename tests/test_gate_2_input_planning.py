from __future__ import annotations

import csv
import unittest
from pathlib import Path

import scripts.validate_gate_2_input_planning as validator


class Gate2InputPlanningTests(unittest.TestCase):
    def test_validator_passes(self):
        summary = validator.validate_gate_2_input_planning()
        self.assertTrue(summary["valid"], summary["errors"])
        self.assertTrue(20 <= summary["row_count"] <= 24)
        self.assertEqual(summary["unique_token_count"], summary["row_count"])
        self.assertEqual(summary["decision_counts"]["approve_for_template_planning"], 14)
        self.assertEqual(summary["decision_counts"]["approve_with_revision"], 4)
        self.assertEqual(summary["decision_counts"]["needs_follow_up"], 2)

    def test_proposal_tsv_exists_and_has_expected_row_count(self):
        self.assertTrue(validator.PROPOSAL_TSV.exists())
        fields, rows = validator.load_tsv(validator.PROPOSAL_TSV)
        self.assertEqual(fields, validator.REQUIRED_COLUMNS)
        self.assertEqual(len(rows), 20)

    def test_only_verified_token_split_clean_noun_standards_rows_are_included(self):
        _, rows = validator.load_tsv(validator.PROPOSAL_TSV)
        _, source_rows = validator.load_tsv(validator.TOKEN_SPLIT_SOURCE)
        source_by_id = {row["candidate_id"]: row for row in source_rows}
        with validator.CLEAN_GROUP_CROSSWALK.open("r", encoding="utf-8", newline="") as handle:
            crosswalk = list(csv.DictReader(handle, delimiter="\t"))
        verified_ids = {
            row["source_candidate_id"]
            for row in crosswalk
            if row["category"] == "token_split_clean_noun_standards"
            and row["recommended_yossi_decision"] == "verified"
        }
        for row in rows:
            with self.subTest(candidate=row["gate_2_input_candidate_id"]):
                self.assertEqual(row["source_candidate_file"], validator.EXPECTED_SOURCE_FILE)
                self.assertIn(row["source_candidate_id"], verified_ids)
                source = source_by_id[row["source_candidate_id"]]
                self.assertEqual(source["enrichment_review_status"], "yossi_enrichment_verified")
                self.assertEqual(source["yossi_decision"], "verified")
                self.assertEqual(row["approved_family"], "basic_noun_recognition")

    def test_no_unsafe_categories_or_gates_are_included(self):
        _, rows = validator.load_tsv(validator.PROPOSAL_TSV)
        for row in rows:
            self.assertNotIn(row["approved_family"], {"shoresh_identification", "basic_verb_form_recognition", "direct_object_marker_recognition"})
            self.assertNotIn(row["hebrew_token"], {"את", "אֶת"})
            self.assertEqual(row["question_allowed"], "needs_review")
            self.assertEqual(row["protected_preview_allowed"], "false")
            self.assertEqual(row["reviewed_bank_allowed"], "false")
            self.assertEqual(row["runtime_allowed"], "false")
            self.assertEqual(row["student_facing_allowed"], "false")

    def test_review_fields_and_decisions_match_expected_counts(self):
        _, rows = validator.load_tsv(validator.PROPOSAL_TSV)
        counts = {}
        for row in rows:
            for field in validator.REVIEW_STATUS_FIELDS:
                self.assertEqual(row[field], "needs_review")
            counts[row["yossi_gate_2_decision"]] = counts.get(row["yossi_gate_2_decision"], 0) + 1
            self.assertEqual(
                row["gate_2_candidate_status"],
                validator.EXPECTED_STATUS_BY_DECISION[row["yossi_gate_2_decision"]],
            )
            self.assertNotEqual(row["yossi_gate_2_notes"], "")
        self.assertEqual(counts["approve_for_template_planning"], 14)
        self.assertEqual(counts["approve_with_revision"], 4)
        self.assertEqual(counts["needs_follow_up"], 2)
        self.assertEqual(counts.get("block_for_now", 0), 0)
        self.assertEqual(counts.get("source_only", 0), 0)

    def test_reports_and_yossi_review_sheet_exist(self):
        self.assertTrue(validator.BALANCE_REPORT.exists())
        self.assertTrue(validator.YOSSI_REVIEW_MD.exists())
        self.assertTrue(validator.YOSSI_REVIEW_CSV.exists())
        self.assertTrue(validator.PROPOSAL_REPORT.exists())
        self.assertTrue(validator.REVIEW_APPLIED_REPORT.exists())
        self.assertTrue(validator.TEMPLATE_PLANNING_READINESS_REPORT.exists())
        self.assertTrue(validator.YOSSI_REVIEW_CSV.read_bytes().startswith(b"\xef\xbb\xbf"))
        text = validator.PROPOSAL_REPORT.read_text(encoding="utf-8")
        self.assertIn("91 verified token-split clean noun standards candidates", text)
        self.assertIn("No questions generated", text)

    def test_revision_and_follow_up_notes_are_present(self):
        _, rows = validator.load_tsv(validator.PROPOSAL_TSV)
        by_id = {row["gate_2_input_candidate_id"]: row for row in rows}
        for candidate_id, phrases in validator.REVISION_NOTE_PHRASES.items():
            self.assertEqual(by_id[candidate_id]["yossi_gate_2_decision"], "approve_with_revision")
            for phrase in phrases:
                self.assertIn(phrase, by_id[candidate_id]["yossi_gate_2_notes"])
        for candidate_id, phrases in validator.FOLLOW_UP_NOTE_PHRASES.items():
            self.assertEqual(by_id[candidate_id]["yossi_gate_2_decision"], "needs_follow_up")
            for phrase in phrases:
                self.assertIn(phrase, by_id[candidate_id]["yossi_gate_2_notes"])

    def test_hebrew_integrity(self):
        _, rows = validator.load_tsv(validator.PROPOSAL_TSV)
        for row in rows:
            self.assertRegex(row["hebrew_token"], validator.HEBREW_RE)
            self.assertRegex(row["hebrew_phrase"], validator.HEBREW_RE)
            self.assertNotIn("???", row["hebrew_token"])
            self.assertNotIn("×", row["hebrew_token"])
            self.assertNotIn("Ö", row["hebrew_token"])


if __name__ == "__main__":
    unittest.main()
