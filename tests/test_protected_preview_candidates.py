from __future__ import annotations
import csv, unittest
from pathlib import Path
import scripts.validate_protected_preview_candidates as validator
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'data'/'protected_preview_candidates'
TSV=BASE/'bereishis_perek_1_first_protected_preview_candidates.tsv'
PACKET=BASE/'reports'/'bereishis_perek_1_first_protected_preview_candidate_review_packet.md'
GEN=BASE/'reports'/'bereishis_perek_1_first_protected_preview_candidate_generation_report.md'
EXC=BASE/'reports'/'bereishis_perek_1_first_protected_preview_candidate_excluded_preserved_report.md'
def rows():
    with TSV.open('r',encoding='utf-8',newline='') as f: return list(csv.DictReader(f,delimiter='\t'))
class ProtectedPreviewCandidatesTests(unittest.TestCase):
    def test_validator_passes(self):
        s=validator.validate_protected_preview_candidates(); self.assertTrue(s['valid'],s['errors']); self.assertEqual(s['row_count'],18)
    def test_tsv_exists_and_has_18_rows(self): self.assertTrue(TSV.exists()); self.assertEqual(len(rows()),18)
    def test_excluded_rows_absent(self):
        rs=rows(); self.assertNotIn('cdraft_b1_016',{r['draft_item_id'] for r in rs}); toks={r['hebrew_token'] for r in rs}; self.assertNotIn(validator.CHAYAH,toks); self.assertNotIn(validator.ET,toks); self.assertNotIn(validator.HIBDIL,toks); self.assertNotIn(validator.BDL,toks)
    def test_gates_false_and_decisions_blank(self):
        for r in rows():
            for f in validator.GATES: self.assertEqual(r[f],'false')
            self.assertEqual(r['yossi_protected_preview_decision'],'approve_for_internal_protected_preview_packet'); self.assertIn('not reviewed-bank approval', r['yossi_protected_preview_notes'])
            self.assertEqual(r['protected_preview_candidate_status'],'yossi_approved_for_internal_protected_preview_packet')
    def test_reports_exist(self): self.assertTrue(PACKET.exists()); self.assertTrue(GEN.exists()); self.assertTrue(EXC.exists())
    def test_hebrew_integrity(self):
        self.assertTrue(all(validator.has_hebrew(r['hebrew_token']) for r in rows()))
        text=PACKET.read_text(encoding='utf-8')+GEN.read_text(encoding='utf-8')+EXC.read_text(encoding='utf-8')
        self.assertIn(validator.ET,text); self.assertIn(validator.HIBDIL,text); self.assertIn(validator.BDL,text); self.assertIn(validator.CHAYAH,text); self.assertNotIn('??',text)
if __name__=='__main__': unittest.main()
