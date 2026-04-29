from __future__ import annotations
import unittest
import scripts.validate_gate_2_exact_wording_planning as validator
class Gate2ExactWordingPlanningTests(unittest.TestCase):
    def test_validator_passes(self):
        s=validator.validate_gate_2_exact_wording_planning(); self.assertTrue(s['valid'],s['errors']); self.assertEqual(s['row_count'],14); self.assertEqual(s['revision_constrained_count'],4)
    def test_schema_and_rows(self):
        f,r=validator.load_tsv(validator.EXACT_TSV); self.assertEqual(f,validator.REQUIRED_COLUMNS); self.assertEqual(len(r),14)
    def test_links_to_skeleton_rows(self):
        _,r=validator.load_tsv(validator.EXACT_TSV); _,s=validator.load_tsv(validator.SKELETON_TSV); self.assertEqual({x['template_skeleton_candidate_id'] for x in r},{x['template_skeleton_candidate_id'] for x in s})
    def test_gates_and_decisions_closed(self):
        _,rows=validator.load_tsv(validator.EXACT_TSV)
        for row in rows:
            for f in validator.REVIEW_STATUS_FIELDS: self.assertEqual(row[f],'needs_review')
            for f,v in validator.GATE_FIELDS.items(): self.assertEqual(row[f],v)
            self.assertEqual(row['yossi_exact_wording_decision'],''); self.assertEqual(row['yossi_exact_wording_notes'],'')
    def test_revision_cautions_exist(self):
        _,rows=validator.load_tsv(validator.EXACT_TSV); by={r['template_skeleton_candidate_id']:r for r in rows}
        for sid in validator.REVISION_IDS: self.assertIn('Base noun only',by[sid]['cautions']); self.assertIn('answer-key review',by[sid]['cautions'])
    def test_reports_exist(self):
        for p in (validator.README,validator.YOSSI_PACKET,validator.PLANNING_REPORT): self.assertTrue(p.exists())
if __name__=='__main__': unittest.main()
