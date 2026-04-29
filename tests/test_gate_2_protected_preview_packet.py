from __future__ import annotations

import unittest

import scripts.validate_gate_2_protected_preview_packet as validator


class Gate2ProtectedPreviewPacketTests(unittest.TestCase):
    def test_validator_passes(self):
        summary = validator.validate_gate_2_protected_preview_packet()
        self.assertTrue(summary["valid"], summary["errors"])
        self.assertEqual(summary["row_count"], 10)
        self.assertEqual(summary["family_counts"], {"basic_noun_recognition": 10})

    def test_packet_tsv_exists_and_has_10_rows(self):
        fields, rows = validator.load_tsv(validator.TSV)
        self.assertEqual(fields, validator.REQUIRED_COLUMNS)
        self.assertEqual(len(rows), 10)

    def test_excluded_rows_absent(self):
        _, rows = validator.load_tsv(validator.TSV)
        _, candidates = validator.load_tsv(validator.CAND)
        by_id = {row["protected_preview_candidate_id"]: row for row in candidates}
        gate_ids = {
            by_id[row["protected_preview_candidate_id"]]["gate_2_input_candidate_id"]
            for row in rows
        }
        self.assertFalse(gate_ids.intersection(validator.EXCLUDED_GATE2))

    def test_downstream_gates_false_and_decisions_blank(self):
        _, rows = validator.load_tsv(validator.TSV)
        for row in rows:
            for gate in validator.GATES:
                self.assertEqual(row[gate], "false")
            self.assertEqual(row["yossi_internal_preview_decision"], "")
            self.assertEqual(row["yossi_internal_preview_notes"], "")
            self.assertEqual(row["internal_packet_status"], "internal_protected_preview_packet_only")
            self.assertEqual(row["internal_preview_review_status"], "needs_internal_review")

    def test_reports_exist(self):
        for path in (validator.README, validator.PACKET, validator.GEN, validator.COMPLETE, validator.EXCLUDED):
            self.assertTrue(path.exists())

    def test_hebrew_integrity(self):
        _, rows = validator.load_tsv(validator.TSV)
        self.assertTrue(
            all(validator.has_hebrew(row["hebrew_token"]) and validator.has_hebrew(row["hebrew_phrase"]) for row in rows)
        )
        text = validator.PACKET.read_text(encoding="utf-8") + validator.EXCLUDED.read_text(encoding="utf-8")
        self.assertNotIn("??", text)


if __name__ == "__main__":
    unittest.main()
