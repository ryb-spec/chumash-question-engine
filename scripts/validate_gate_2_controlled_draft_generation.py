from __future__ import annotations
import csv,json,re
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DIR=ROOT/'data'/'gate_2_controlled_draft_generation'
README=DIR/'README.md'; DRAFT_TSV=DIR/'bereishis_perek_2_controlled_draft.tsv'
PACKET=DIR/'reports'/'bereishis_perek_2_controlled_draft_teacher_review_packet.md'; REPORT=DIR/'reports'/'bereishis_perek_2_controlled_draft_generation_report.md'; SKIPPED=DIR/'reports'/'bereishis_perek_2_controlled_draft_skipped_revision_required_report.md'; APPLIED=DIR/'reports'/'bereishis_perek_2_controlled_draft_yossi_review_applied.md'
PRE_TSV=ROOT/'data'/'gate_2_pre_generation_review'/'bereishis_perek_2_pre_generation_review.tsv'
REQUIRED_COLUMNS=['controlled_draft_item_id','pre_generation_review_id','gate_2_input_candidate_id','source_ref','approved_family','hebrew_token','hebrew_phrase','draft_prompt','answer_choices','expected_answer','correct_answer','explanation','source_evidence_note','caution_note','draft_review_status','answer_key_review_status','distractor_review_status','hebrew_rendering_review_status','protected_preview_gate_review_status','protected_preview_allowed','reviewed_bank_allowed','runtime_allowed','student_facing_allowed','yossi_draft_decision','yossi_draft_notes']
REVIEW_FIELDS=['answer_key_review_status','distractor_review_status','hebrew_rendering_review_status','protected_preview_gate_review_status']
GATES=['protected_preview_allowed','reviewed_bank_allowed','runtime_allowed','student_facing_allowed']
APPROVED={'g2p2_002','g2p2_003','g2p2_006','g2p2_007','g2p2_009','g2p2_014','g2p2_016','g2p2_017','g2p2_019','g2p2_020'}
REVISION={'g2p2_001','g2p2_010','g2p2_012','g2p2_013'}
EXCLUDED={'g2p2_004','g2p2_005','g2p2_008','g2p2_011','g2p2_015','g2p2_018'}
HEBREW_RE=re.compile(r'[\u0590-\u05FF]')
def rel(p): return p.relative_to(ROOT).as_posix()
def load_tsv(p):
    with p.open('r',encoding='utf-8',newline='') as h:
        r=csv.DictReader(h,delimiter='\t'); return list(r.fieldnames or []),list(r)
def validate_gate_2_controlled_draft_generation():
    errors=[]
    for p in (README,DRAFT_TSV,PACKET,REPORT,SKIPPED,APPLIED,PRE_TSV):
        if not p.exists(): errors.append(f'missing controlled draft artifact: {rel(p)}')
    if errors: return {'valid':False,'errors':errors}
    fields,rows=load_tsv(DRAFT_TSV)
    if fields!=REQUIRED_COLUMNS: errors.append('controlled draft TSV columns do not match required schema')
    if len(rows)!=10: errors.append(f'controlled draft TSV must have exactly 10 rows, found {len(rows)}')
    _,pre_rows=load_tsv(PRE_TSV); pre={r['pre_generation_review_id']:r for r in pre_rows}
    included=set(); decisions=Counter(r.get('yossi_draft_decision','') for r in rows)
    for r in rows:
        cid=r.get('controlled_draft_item_id','?'); gid=r.get('gate_2_input_candidate_id',''); included.add(gid)
        if gid not in APPROVED: errors.append(f'{cid}: only approved rows may be drafted')
        if gid in REVISION or gid in EXCLUDED: errors.append(f'{cid}: revision/follow-up/excluded row included')
        src=pre.get(r.get('pre_generation_review_id',''))
        if not src: errors.append(f'{cid}: missing linked pre-generation row')
        elif src.get('row_level_generation_status')!='approved_for_controlled_draft_generation': errors.append(f'{cid}: linked pre-generation row must be approved')
        if r.get('approved_family')!='basic_noun_recognition': errors.append(f'{cid}: family must be basic_noun_recognition')
        if r.get('draft_review_status')!='yossi_draft_approved': errors.append(f'{cid}: draft_review_status must be yossi_draft_approved')
        if r.get('yossi_draft_decision')!='approve_draft_item': errors.append(f'{cid}: yossi_draft_decision must be approve_draft_item')
        if not r.get('yossi_draft_notes'): errors.append(f'{cid}: yossi_draft_notes must be populated')
        if r.get('answer_choices')!='noun|action word|describing word|prefix': errors.append(f'{cid}: answer choices must be simple category labels')
        if r.get('expected_answer')!='noun' or r.get('correct_answer')!='noun': errors.append(f'{cid}: expected/correct answer must be noun')
        for f in REVIEW_FIELDS:
            if r.get(f)!='needs_yossi_review': errors.append(f'{cid}: {f} must remain needs_yossi_review')
        for f in GATES:
            if r.get(f)!='false': errors.append(f'{cid}: {f} must be false')
        for f in ('hebrew_token','hebrew_phrase'):
            val=r.get(f,'')
            if not HEBREW_RE.search(val): errors.append(f'{cid}: {f} must contain Hebrew')
            if '???' in val or '×' in val or 'Ö' in val: errors.append(f'{cid}: {f} contains corruption')
    if included!=APPROVED: errors.append('draft rows must exactly match approved Gate 2 IDs')
    if decisions.get('approve_draft_item',0)!=10: errors.append('expected 10 approve_draft_item rows')
    text='\n'.join(p.read_text(encoding='utf-8') for p in (README,DRAFT_TSV,PACKET,REPORT,SKIPPED,APPLIED))
    for phrase in ('not protected-preview','not reviewed-bank','not runtime','not student-facing','All gates closed'):
        if phrase not in text: errors.append(f'missing safety phrase: {phrase}')
    for gid in REVISION:
        if gid not in SKIPPED.read_text(encoding='utf-8'): errors.append(f'skipped report missing {gid}')
    for bad in ('???','×','Ö'):
        if bad in text: errors.append(f'artifacts contain corrupt phrase: {bad}')
    return {'valid':not errors,'errors':errors,'draft_path':rel(DRAFT_TSV),'row_count':len(rows),'decision_counts':dict(decisions),'family_counts':dict(Counter(r.get('approved_family','') for r in rows))}
def main():
    s=validate_gate_2_controlled_draft_generation(); print(json.dumps(s,ensure_ascii=False,indent=2)); return 0 if s['valid'] else 1
if __name__=='__main__': raise SystemExit(main())
