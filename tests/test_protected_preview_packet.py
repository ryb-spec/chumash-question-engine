from __future__ import annotations
import csv, unittest
from pathlib import Path
import scripts.validate_protected_preview_packet as validator
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'data'/'protected_preview_packets'
TSV=BASE/'bereishis_perek_1_first_internal_protected_preview_packet.tsv'
PACKET=BASE/'reports'/'bereishis_perek_1_first_internal_protected_preview_packet.md'
GEN=BASE/'reports'/'bereishis_perek_1_first_internal_protected_preview_packet_generation_report.md'
ROUND=BASE/'reports'/'bereishis_perek_1_round_1_completion_report.md'
EXC=BASE/'reports'/'bereishis_perek_1_first_internal_protected_preview_packet_excluded_preserved_report.md'
def rows():
    with TSV.open('r',encoding='utf-8',newline='') as f: return list(csv.DictReader(f,delimiter='\t'))
class ProtectedPreviewPacketTests(unittest.TestCase):
    def test_validator_passes(self):
        s=validator.validate_protected_preview_packet(); self.assertTrue(s['valid'],s['errors']); self.assertEqual(s['row_count'],18)
    def test_packet_tsv_exists_and_has_18_rows(self): self.assertTrue(TSV.exists()); self.assertEqual(len(rows()),18)
    def test_excluded_rows_absent(self):
        rs=rows(); self.assertNotIn('cdraft_b1_016',{r['draft_item_id'] for r in rs}); toks={r['hebrew_token'] for r in rs}; self.assertNotIn(validator.CHAYAH,toks); self.assertNotIn(validator.ET,toks); self.assertNotIn(validator.HIBDIL,toks); self.assertNotIn(validator.BDL,toks)
    def test_gates_false_and_decisions_blank(self):
        for r in rows():
            for g in validator.GATES: self.assertEqual(r[g],'false')
            self.assertEqual(r['yossi_internal_preview_decision'],''); self.assertEqual(r['yossi_internal_preview_notes'],'')
            self.assertEqual(r['internal_packet_status'],'internal_protected_preview_packet_only')
    def test_reports_exist(self): self.assertTrue(PACKET.exists()); self.assertTrue(GEN.exists()); self.assertTrue(ROUND.exists()); self.assertTrue(EXC.exists())
    def test_hebrew_integrity(self):
        self.assertTrue(all(validator.has_hebrew(r['hebrew_token']) for r in rows()))
        text=PACKET.read_text(encoding='utf-8')+GEN.read_text(encoding='utf-8')+ROUND.read_text(encoding='utf-8')+EXC.read_text(encoding='utf-8')
        self.assertIn(validator.ET,text); self.assertIn(validator.HIBDIL,text); self.assertIn(validator.BDL,text); self.assertIn(validator.CHAYAH,text); self.assertNotIn('??',text)
if __name__=='__main__': unittest.main()
