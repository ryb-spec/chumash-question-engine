from __future__ import annotations

import csv
import unittest
from pathlib import Path

import scripts.validate_pre_generation_review as validator

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "pre_generation_review"
TSV = BASE / "bereishis_perek_1_first_batch_pre_generation_review.tsv"
README = BASE / "README.md"
REPORT = BASE / "reports" / "bereishis_perek_1_first_batch_pre_generation_review_report.md"
APPLIED = BASE / "reports" / "bereishis_perek_1_first_batch_pre_generation_yossi_review_applied.md"
REVIEW_MD = BASE / "reports" / "bereishis_perek_1_first_batch_pre_generation_yossi_review_sheet.md"
REVIEW_CSV = BASE / "reports" / "bereishis_perek_1_first_batch_pre_generation_yossi_review_sheet.csv"
DRAFT_TSV = ROOT / "data" / "controlled_draft_generation" / "bereishis_perek_1_first_controlled_draft.tsv"


def load_rows(path=TSV):
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


class PreGenerationReviewTests(unittest.TestCase):
    def test_validator_passes(self):
        summary = validator.validate_pre_generation_review()
        self.assertTrue(summary["valid"], summary["errors"])
        self.assertEqual(summary["row_count"], 24)

    def test_decision_counts(self):
        rows = load_rows()
        decisions = [row["yossi_exact_wording_decision"] for row in rows]
        self.assertEqual(decisions.count("approve_for_controlled_draft_generation"), 19)
        self.assertEqual(decisions.count("approve_with_revision"), 5)
        self.assertNotIn("needs_follow_up", decisions)
        self.assertNotIn("block_for_now", decisions)
        self.assertNotIn("source_only", decisions)

    def test_statuses_match_decisions(self):
        for row in load_rows():
            if row["pre_generation_review_id"] in validator.DIRECT_APPROVAL_IDS:
                expected = "approve_for_controlled_draft_generation"
                self.assertEqual(row["row_level_generation_status"], "approved_for_controlled_draft_generation")
            else:
                expected = "approve_with_revision"
                self.assertEqual(row["row_level_generation_status"], "blocked_pending_revision")
            for field in validator.REVIEW_STATUS_FIELDS | validator.YOSSI_DECISION_FIELDS:
                self.assertEqual(row[field], expected)

    def test_all_gates_false(self):
        for row in load_rows():
            for field in validator.SAFETY_FIELDS:
                self.assertEqual(row[field], "false")

    def test_controlled_draft_links_only_to_direct_approvals(self):
        draft_rows = load_rows(DRAFT_TSV)
        self.assertEqual(len(draft_rows), 19)
        draft_ids = {row["pre_generation_review_id"] for row in draft_rows}
        self.assertEqual(draft_ids, validator.DIRECT_APPROVAL_IDS)
        self.assertFalse(draft_ids & validator.REVISION_IDS)

    def test_review_sheet_and_csv_exist(self):
        self.assertTrue(REVIEW_MD.exists())
        self.assertTrue(REVIEW_CSV.exists())
        self.assertTrue(REVIEW_CSV.read_bytes().startswith(b"\xef\xbb\xbf"))

    def test_report_and_readme_links_exist(self):
        self.assertTrue(REPORT.exists())
        self.assertTrue(APPLIED.exists())
        readme = README.read_text(encoding="utf-8")
        for path in (TSV, REVIEW_MD, REVIEW_CSV, REPORT, APPLIED):
            self.assertIn(path.relative_to(ROOT).as_posix(), readme)

    def test_hebrew_integrity_and_no_placeholder_corruption(self):
        text = REPORT.read_text(encoding="utf-8") + APPLIED.read_text(encoding="utf-8")
        self.assertIn(validator.ET, text)
        self.assertIn(validator.HIBDIL, text)
        self.assertIn(validator.BDL, text)
        self.assertIn(validator.HAMAYIM, text)
        self.assertIn(validator.HAADAMAH, text)
        self.assertIn(validator.HAARETZ, text)
        self.assertNotIn("??", text)
        for row in load_rows():
            self.assertTrue(validator.has_hebrew(row["hebrew_token"]))
            self.assertNotIn("??", row["row_level_cautions"])


if __name__ == "__main__":
    unittest.main()
