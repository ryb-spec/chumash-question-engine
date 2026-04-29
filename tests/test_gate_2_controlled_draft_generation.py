from __future__ import annotations
import unittest
import scripts.validate_gate_2_controlled_draft_generation as validator
class Gate2ControlledDraftGenerationTests(unittest.TestCase):
    def test_validator_passes(self):
        s=validator.validate_gate_2_controlled_draft_generation(); self.assertTrue(s['valid'],s['errors']); self.assertEqual(s['row_count'],10); self.assertEqual(s['decision_counts'].get('approve_draft_item'),10)
    def test_approved_rows_and_gates(self):
        _,rows=validator.load_tsv(validator.DRAFT_TSV)
        self.assertEqual({r['gate_2_input_candidate_id'] for r in rows},validator.APPROVED)
        for r in rows:
            self.assertEqual(r['yossi_draft_decision'],'approve_draft_item'); self.assertEqual(r['draft_review_status'],'yossi_draft_approved')
            for f in validator.GATES: self.assertEqual(r[f],'false')
    def test_skipped_rows_absent_and_reports_exist(self):
        _,rows=validator.load_tsv(validator.DRAFT_TSV); ids={r['gate_2_input_candidate_id'] for r in rows}; self.assertFalse(ids.intersection(validator.REVISION|validator.EXCLUDED))
        for p in (validator.README,validator.PACKET,validator.REPORT,validator.SKIPPED,validator.APPLIED): self.assertTrue(p.exists())
if __name__=='__main__': unittest.main()
