from __future__ import annotations

import csv
import tempfile
import unittest
from collections import Counter
from pathlib import Path

import scripts.validate_gate_2_protected_preview_packet as validator


class Gate2ProtectedPreviewPacketTests(unittest.TestCase):
    def test_validator_passes(self):
        summary = validator.validate_gate_2_protected_preview_packet()
        self.assertTrue(summary["valid"], summary["errors"])
        self.assertEqual(summary["row_count"], 14)
        self.assertEqual(summary["family_counts"], {"basic_noun_recognition": 14})
        self.assertEqual(summary["perek_summaries"]["perek_2"]["row_count"], 10)
        self.assertEqual(summary["perek_summaries"]["perek_3"]["row_count"], 4)

    def test_perek_2_packet_tsv_exists_and_has_10_rows(self):
        fields, rows = validator.load_tsv(validator.TSV)
        self.assertEqual(fields, validator.REQUIRED_COLUMNS)
        self.assertEqual(len(rows), 10)

    def test_perek_2_excluded_rows_absent(self):
        _, rows = validator.load_tsv(validator.TSV)
        _, candidates = validator.load_tsv(validator.CAND)
        by_id = {row["protected_preview_candidate_id"]: row for row in candidates}
        gate_ids = {
            by_id[row["protected_preview_candidate_id"]]["gate_2_input_candidate_id"]
            for row in rows
        }
        self.assertFalse(gate_ids.intersection(validator.EXCLUDED_GATE2))

    def test_perek_3_packet_file_exists_and_has_exact_4_rows(self):
        fields, rows = validator.load_tsv(validator.P3_TSV)
        self.assertEqual(fields, validator.REQUIRED_COLUMNS)
        self.assertEqual(len(rows), 4)

    def test_perek_3_packet_id_set_is_exactly_approved_ids(self):
        _, rows = validator.load_tsv(validator.P3_TSV)
        candidate_ids = {row["protected_preview_candidate_id"] for row in rows}
        self.assertEqual(candidate_ids, validator.EXPECTED_P3_APPROVED)

    def test_perek_3_packet_excludes_revision_and_followup_ids(self):
        _, rows = validator.load_tsv(validator.P3_TSV)
        candidate_ids = {row["protected_preview_candidate_id"] for row in rows}
        self.assertFalse(candidate_ids.intersection(validator.P3_REVISION))
        self.assertFalse(candidate_ids.intersection(validator.P3_FOLLOWUP))
        self.assertFalse(candidate_ids.intersection(validator.P3_EXCLUDED))

    def test_downstream_gates_false_and_decisions_blank(self):
        for packet in (validator.TSV, validator.P3_TSV):
            _, rows = validator.load_tsv(packet)
            for row in rows:
                for gate in validator.GATES:
                    self.assertEqual(row[gate], "false")
                self.assertEqual(row["yossi_internal_preview_decision"], "")
                self.assertEqual(row["yossi_internal_preview_notes"], "")
                self.assertEqual(row["internal_packet_status"], "internal_protected_preview_packet_only")
                self.assertEqual(row["internal_preview_review_status"], "needs_internal_review")

    def test_reports_exist(self):
        for path in (
            validator.README,
            validator.PACKET,
            validator.GEN,
            validator.COMPLETE,
            validator.EXCLUDED,
            validator.P3_REPORT,
            validator.P3_STATUS_INDEX,
        ):
            self.assertTrue(path.exists(), path)

    def test_perek_3_packet_report_names_inclusions_and_exclusions(self):
        text = validator.P3_REPORT.read_text(encoding="utf-8")
        for candidate_id in validator.EXPECTED_P3_APPROVED:
            self.assertIn(candidate_id, text)
        self.assertIn("All 4 `approve_with_revision` items are excluded", text)
        self.assertIn("All 2 `needs_follow_up` items are excluded", text)
        self.assertIn("Included approved rows: 4", text)
        self.assertIn("Excluded revision rows: 4", text)
        self.assertIn("Excluded follow-up rows: 2", text)
        self.assertIn("No Perek 3 runtime activation", text)
        self.assertIn("No reviewed-bank promotion", text)

    def test_perek_3_status_index_says_packet_exists_and_gates_closed(self):
        text = validator.P3_STATUS_INDEX.read_text(encoding="utf-8")
        self.assertIn("historical pre-decision artifact", text)
        self.assertIn("applied-decision report is the current status source", text)
        self.assertIn("four-item internal protected-preview packet now exists", text)
        self.assertIn("No Perek 3 runtime activation", text)
        self.assertIn("No reviewed-bank promotion", text)
        self.assertIn("No student-facing content", text)
        self.assertIn("`approve_for_internal_protected_preview_packet`: 4", text)
        self.assertIn("`approve_with_revision`: 4", text)
        self.assertIn("`needs_follow_up`: 2", text)

    def test_hebrew_integrity(self):
        for packet in (validator.TSV, validator.P3_TSV):
            _, rows = validator.load_tsv(packet)
            self.assertTrue(
                all(validator.has_hebrew(row["hebrew_token"]) and validator.has_hebrew(row["hebrew_phrase"]) for row in rows)
            )
        text = validator.PACKET.read_text(encoding="utf-8") + validator.EXCLUDED.read_text(encoding="utf-8")
        self.assertNotIn("??", text)

    def test_validator_rejects_extra_perek_3_candidate_id(self):
        _, rows = validator.load_tsv(validator.P3_TSV)
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir) / "bad_p3_packet.tsv"
            with tmp_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=validator.REQUIRED_COLUMNS, delimiter="\t", lineterminator="\n")
                writer.writeheader()
                writer.writerows(rows + [rows[0]])
            errors: list[str] = []
            validator.validate_packet_spec(
                name="bad_perek_3",
                packet_tsv=tmp_path,
                candidate_tsv=validator.P3_CAND,
                expected_count=4,
                expected_candidate_ids=validator.EXPECTED_P3_APPROVED,
                excluded_gate_ids=set(),
                excluded_candidate_ids=validator.P3_EXCLUDED,
                errors=errors,
                family_counts=Counter(),
            )
            self.assertTrue(any("exactly 4 rows" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
