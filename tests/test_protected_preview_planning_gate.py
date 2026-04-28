from __future__ import annotations

import csv
import unittest
from pathlib import Path

import scripts.validate_protected_preview_planning_gate as validator

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "protected_preview_planning_gate"
TSV = BASE / "bereishis_perek_1_first_protected_preview_planning_gate.tsv"
PACKET = BASE / "reports" / "bereishis_perek_1_first_protected_preview_planning_gate_yossi_review_packet.md"
SUMMARY = BASE / "reports" / "bereishis_perek_1_first_protected_preview_planning_gate_report.md"
EXCLUDED = BASE / "reports" / "bereishis_perek_1_first_protected_preview_planning_gate_excluded_report.md"
APPLIED = BASE / "reports" / "bereishis_perek_1_first_protected_preview_planning_gate_yossi_review_applied.md"
READINESS = BASE / "reports" / "bereishis_perek_1_first_protected_preview_candidate_readiness_report.md"
README = BASE / "README.md"


def rows():
    with TSV.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


class ProtectedPreviewPlanningGateTests(unittest.TestCase):
    def test_validator_passes(self):
        summary = validator.validate_protected_preview_planning_gate()
        self.assertTrue(summary["valid"], summary["errors"])
        self.assertEqual(summary["row_count"], 18)

    def test_decisions_applied_to_all_rows(self):
        for row in rows():
            self.assertEqual(row["yossi_preview_gate_decision"], "approve_for_protected_preview_candidate")
            self.assertEqual(row["preview_gate_candidate_status"], "yossi_approved_for_protected_preview_candidate_planning")
            self.assertEqual(row["protected_preview_candidate_planning_allowed"], "true")

    def test_excluded_rows_absent(self):
        draft_ids = {row["draft_item_id"] for row in rows()}
        self.assertNotIn("cdraft_b1_016", draft_ids)
        tokens = {row["hebrew_token"] for row in rows()}
        self.assertNotIn(validator.ET, tokens)
        self.assertNotIn(validator.HIBDIL, tokens)
        self.assertNotIn(validator.BDL, tokens)
        self.assertNotIn(validator.CHAYAH, tokens)

    def test_release_gates_false(self):
        for row in rows():
            for field in validator.SAFETY_FIELDS:
                self.assertEqual(row[field], "false")
            self.assertIn("not protected-preview release approval", row["yossi_preview_gate_notes"])

    def test_reports_exist_and_readme_links(self):
        for path in (PACKET, SUMMARY, EXCLUDED, APPLIED, READINESS):
            self.assertTrue(path.exists())
        readme = README.read_text(encoding="utf-8")
        for path in (TSV, PACKET, SUMMARY, EXCLUDED, APPLIED, READINESS):
            self.assertIn(path.relative_to(ROOT).as_posix(), readme)

    def test_hebrew_integrity(self):
        self.assertTrue(all(validator.has_hebrew(row["hebrew_token"]) for row in rows()))
        text = PACKET.read_text(encoding="utf-8") + SUMMARY.read_text(encoding="utf-8") + EXCLUDED.read_text(encoding="utf-8") + APPLIED.read_text(encoding="utf-8") + READINESS.read_text(encoding="utf-8")
        self.assertIn(validator.ET, text)
        self.assertIn(validator.HIBDIL, text)
        self.assertIn(validator.BDL, text)
        self.assertIn(validator.CHAYAH, text)
        self.assertNotIn("??", text)


if __name__ == "__main__":
    unittest.main()
