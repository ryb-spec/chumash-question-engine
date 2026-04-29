from __future__ import annotations

import csv
import unittest
from pathlib import Path

import scripts.validate_controlled_draft_generation as validator

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "controlled_draft_generation"
TSV = BASE / "bereishis_perek_1_first_controlled_draft.tsv"
README = BASE / "README.md"
PACKET = BASE / "reports" / "bereishis_perek_1_first_controlled_draft_teacher_review_packet.md"
GEN_REPORT = BASE / "reports" / "bereishis_perek_1_first_controlled_draft_generation_report.md"
SKIP_REPORT = BASE / "reports" / "bereishis_perek_1_first_controlled_draft_skipped_revision_required_report.md"
APPLIED_REPORT = BASE / "reports" / "bereishis_perek_1_first_controlled_draft_yossi_review_applied.md"
READINESS_REPORT = BASE / "reports" / "bereishis_perek_1_first_controlled_draft_preview_planning_readiness_report.md"
REVISION_REPORT = BASE / "reports" / "bereishis_perek_1_first_controlled_draft_revision_resolution_report.md"


def load_rows():
    with TSV.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


class ControlledDraftGenerationTests(unittest.TestCase):
    def test_validator_passes(self):
        summary = validator.validate_controlled_draft_generation()
        self.assertTrue(summary["valid"], summary["errors"])
        self.assertEqual(summary["row_count"], 19)

    def test_exactly_19_rows_and_only_direct_approvals(self):
        rows = load_rows()
        self.assertEqual(len(rows), 19)
        ids = {row["pre_generation_review_id"] for row in rows}
        self.assertEqual(ids, validator.DIRECT_PREGEN_IDS)
        self.assertFalse(ids & validator.SKIPPED_PREGEN_IDS)

    def test_final_decision_counts(self):
        summary = validator.validate_controlled_draft_generation()
        for decision, expected in validator.EXPECTED_DECISION_COUNTS.items():
            self.assertEqual(summary["decision_counts"].get(decision, 0), expected)
        self.assertEqual(summary["status_counts"].get("yossi_draft_approved", 0), 14)
        self.assertEqual(summary["status_counts"].get("yossi_draft_approved_after_revision", 0), 4)
        self.assertEqual(summary["status_counts"].get("source_only_not_for_preview_planning", 0), 1)

    def test_no_verb_form_rows(self):
        self.assertNotIn("basic_verb_form_recognition", {row["approved_family"] for row in load_rows()})

    def test_revised_answer_language(self):
        rows = {row["draft_item_id"]: row for row in load_rows()}
        expected = {
            "cdraft_b1_001": "expanse / firmament",
            "cdraft_b1_004": "lights / luminaries",
            "cdraft_b1_006": "swarming creature / creeping creature",
            "cdraft_b1_008": "animal / beast / domesticated animal",
        }
        for row_id, phrase in expected.items():
            self.assertIn(phrase, rows[row_id]["expected_answer"])
            self.assertIn(phrase, rows[row_id]["answer_choices"])
            self.assertEqual(rows[row_id]["yossi_draft_decision"], "approve_draft_item")
            self.assertEqual(rows[row_id]["draft_review_status"], "yossi_draft_approved_after_revision")

    def test_chayah_source_only_resolution(self):
        row = {row["draft_item_id"]: row for row in load_rows()}["cdraft_b1_016"]
        self.assertEqual(row["yossi_draft_decision"], "source_only")
        self.assertEqual(row["draft_review_status"], "source_only_not_for_preview_planning")
        self.assertIn(validator.CHAYAH, row["yossi_draft_notes"])
        self.assertIn("noun/adjective/description", row["yossi_draft_notes"])

    def test_review_statuses_and_gates(self):
        for row in load_rows():
            for field in validator.REMAINING_REVIEW_STATUS_FIELDS:
                self.assertEqual(row[field], "needs_yossi_review")
            for field in validator.SAFETY_FIELDS:
                self.assertEqual(row[field], "false")

    def test_reports_and_readme_links(self):
        for path in (PACKET, GEN_REPORT, SKIP_REPORT, APPLIED_REPORT, READINESS_REPORT, REVISION_REPORT):
            self.assertTrue(path.exists())
        readme = README.read_text(encoding="utf-8")
        for path in (TSV, PACKET, GEN_REPORT, SKIP_REPORT, APPLIED_REPORT, READINESS_REPORT, REVISION_REPORT):
            self.assertIn(path.relative_to(ROOT).as_posix(), readme)

    def test_hebrew_integrity(self):
        rows = load_rows()
        self.assertTrue(all(validator.has_hebrew(row["hebrew_token"]) for row in rows))
        text = PACKET.read_text(encoding="utf-8") + GEN_REPORT.read_text(encoding="utf-8") + SKIP_REPORT.read_text(encoding="utf-8") + APPLIED_REPORT.read_text(encoding="utf-8") + REVISION_REPORT.read_text(encoding="utf-8")
        self.assertIn(validator.ET, text)
        self.assertIn(validator.HIBDIL, text)
        self.assertIn(validator.BDL, text)
        self.assertIn(validator.CHAYAH, text)
        self.assertNotIn("??", text)


if __name__ == "__main__":
    unittest.main()
