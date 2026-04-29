from __future__ import annotations
import unittest
import scripts.validate_gate_2_pre_generation_review as validator
class Gate2PreGenerationReviewTests(unittest.TestCase):
    def test_validator_passes(self):
        s=validator.validate_gate_2_pre_generation_review(); self.assertTrue(s['valid'],s['errors']); self.assertEqual(s['row_count'],14); self.assertEqual(s['decision_counts'].get('approve_for_controlled_draft_generation'),10); self.assertEqual(s['decision_counts'].get('approve_with_revision'),4)
    def test_tsv_schema_and_rows(self):
        f,r=validator.load_tsv(validator.REVIEW_TSV); self.assertEqual(f,validator.REQUIRED_COLUMNS); self.assertEqual(len(r),14)
    def test_statuses_gates_and_decisions(self):
        _,rows=validator.load_tsv(validator.REVIEW_TSV)
        for row in rows:
            for f in validator.REVIEW_STATUS_FIELDS: self.assertEqual(row[f],'needs_review')
            for f,v in validator.GATE_FIELDS.items(): self.assertEqual(row[f],v)
            vals={row[f] for f in validator.DECISION_FIELDS}; self.assertEqual(len(vals),1)
            if row['gate_2_input_candidate_id'] in validator.APPROVED: self.assertEqual(row['row_level_generation_status'],'approved_for_controlled_draft_generation')
            if row['gate_2_input_candidate_id'] in validator.REVISION: self.assertEqual(row['row_level_generation_status'],'blocked_pending_revision')
    def test_csv_bom_and_reports_exist(self):
        self.assertTrue(validator.REVIEW_CSV.read_bytes().startswith(b'\xef\xbb\xbf'))
        for p in (validator.README,validator.REVIEW_MD,validator.REVIEW_CSV,validator.REPORT,validator.APPLIED_REPORT): self.assertTrue(p.exists())
    def test_hebrew_integrity(self):
        _,rows=validator.load_tsv(validator.REVIEW_TSV)
        for row in rows:
            self.assertRegex(row['hebrew_token'],validator.HEBREW_RE); self.assertNotIn('???',row['hebrew_token']); self.assertNotIn('×',row['hebrew_token']); self.assertNotIn('Ö',row['hebrew_token'])
if __name__=='__main__': unittest.main()
