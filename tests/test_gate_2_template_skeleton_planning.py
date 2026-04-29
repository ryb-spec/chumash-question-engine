from __future__ import annotations
import unittest
import scripts.validate_gate_2_template_skeleton_planning as validator
class Gate2TemplateSkeletonPlanningTests(unittest.TestCase):
    def test_validator_passes(self):
        s=validator.validate_gate_2_template_skeleton_planning(); self.assertTrue(s['valid'],s['errors']); self.assertEqual(s['row_count'],14); self.assertEqual(s['decision_counts'].get('approve_for_exact_wording_planning'),10); self.assertEqual(s['decision_counts'].get('approve_with_revision'),4)
    def test_tsv_schema_and_row_count(self):
        f,r=validator.load_tsv(validator.TSV); self.assertEqual(f,validator.REQUIRED_COLUMNS); self.assertEqual(len(r),14)
    def test_only_approved_gate_2_rows_included(self):
        _,r=validator.load_tsv(validator.TSV); _,g=validator.load_tsv(validator.GATE2); approved={x['gate_2_input_candidate_id'] for x in g if x['yossi_gate_2_decision']==validator.APPROVED_DECISION}; included={x['gate_2_input_candidate_id'] for x in r}; self.assertEqual(included,approved); self.assertFalse(included.intersection(validator.EXCLUDED_GATE2_IDS))
    def test_statuses_and_gates_closed(self):
        _,rows=validator.load_tsv(validator.TSV)
        for row in rows:
            for f in validator.REVIEW_STATUS_FIELDS: self.assertEqual(row[f],'needs_review')
            for f,v in validator.GATE_FIELDS.items(): self.assertEqual(row[f],v)
            self.assertEqual(row['template_skeleton_status'],validator.EXPECTED_STATUS_BY_DECISION[row['yossi_template_skeleton_decision']]); self.assertNotEqual(row['yossi_template_skeleton_notes'],'')
    def test_revision_notes_present(self):
        _,rows=validator.load_tsv(validator.TSV); by={r['template_skeleton_candidate_id']:r for r in rows}
        for cid,phrases in validator.REVISION_NOTE_PHRASES.items():
            self.assertEqual(by[cid]['yossi_template_skeleton_decision'],'approve_with_revision')
            for p in phrases: self.assertIn(p,by[cid]['yossi_template_skeleton_notes']+by[cid]['cautions'])
    def test_reports_exist(self):
        for p in (validator.README,validator.PACKET,validator.PLAN_REPORT,validator.EXCLUDED_REPORT,validator.APPLIED_REPORT): self.assertTrue(p.exists())
    def test_hebrew_integrity(self):
        _,rows=validator.load_tsv(validator.TSV)
        for row in rows:
            self.assertRegex(row['hebrew_token'],validator.HEBREW_RE); self.assertNotIn('???',row['hebrew_token']); self.assertNotIn('×',row['hebrew_token']); self.assertNotIn('Ö',row['hebrew_token'])
if __name__=='__main__': unittest.main()
