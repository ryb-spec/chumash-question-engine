from __future__ import annotations

import unittest

import scripts.validate_gate_2_protected_preview_candidates as validator


class Gate2ProtectedPreviewCandidatesTests(unittest.TestCase):
    def test_validator_passes(self):
        summary = validator.validate_gate_2_protected_preview_candidates()
        self.assertTrue(summary["valid"], summary["errors"])
        self.assertEqual(summary["row_count"], 10)
        self.assertEqual(summary["family_counts"], {"basic_noun_recognition": 10})
        self.assertEqual(summary["decision_counts"].get(validator.DECISION), 10)

    def test_schema_and_rows(self):
        fields, rows = validator.load_tsv(validator.TSV)
        self.assertEqual(fields, validator.REQUIRED_COLUMNS)
        self.assertEqual(len(rows), 10)

    def test_links_to_approved_drafts_and_skips_excluded(self):
        _, rows = validator.load_tsv(validator.TSV)
        ids = {row["gate_2_input_candidate_id"] for row in rows}
        self.assertFalse(ids.intersection(validator.EXCLUDED))
        _, drafts = validator.load_tsv(validator.DRAFT_TSV)
        approved = {
            draft["controlled_draft_item_id"]
            for draft in drafts
            if draft["yossi_draft_decision"] == "approve_draft_item"
        }
        self.assertEqual({row["controlled_draft_item_id"] for row in rows}, approved)

    def test_gates_statuses_and_decisions_applied(self):
        _, rows = validator.load_tsv(validator.TSV)
        for row in rows:
            for field in validator.REVIEW_FIELDS:
                self.assertEqual(row[field], "needs_yossi_review")
            for gate in validator.GATES:
                self.assertEqual(row[gate], "false")
            self.assertEqual(row["protected_preview_candidate_status"], validator.STATUS)
            self.assertEqual(row["yossi_protected_preview_decision"], validator.DECISION)
            self.assertIn("internal protected-preview packet only", row["yossi_protected_preview_notes"])

    def test_reports_exist(self):
        for path in (validator.README, validator.PACKET, validator.REPORT, validator.EXCLUDED_REPORT, validator.APPLIED_REPORT):
            self.assertTrue(path.exists())


if __name__ == "__main__":
    unittest.main()
