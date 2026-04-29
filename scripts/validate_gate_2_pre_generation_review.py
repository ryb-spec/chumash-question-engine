from __future__ import annotations
import csv,json,re
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DIR=ROOT/'data'/'gate_2_pre_generation_review'
README=DIR/'README.md'; REVIEW_TSV=DIR/'bereishis_perek_2_pre_generation_review.tsv'
REVIEW_MD=DIR/'reports'/'bereishis_perek_2_pre_generation_yossi_review_sheet.md'; REVIEW_CSV=DIR/'reports'/'bereishis_perek_2_pre_generation_yossi_review_sheet.csv'
REPORT=DIR/'reports'/'bereishis_perek_2_pre_generation_review_report.md'; APPLIED_REPORT=DIR/'reports'/'bereishis_perek_2_pre_generation_yossi_review_applied.md'
EXACT_TSV=ROOT/'data'/'gate_2_exact_wording_planning'/'bereishis_perek_2_exact_wording_planning.tsv'
REQUIRED_COLUMNS=['pre_generation_review_id','exact_wording_candidate_id','template_skeleton_candidate_id','gate_2_input_candidate_id','source_ref','hebrew_token','hebrew_phrase','approved_family','non_student_facing_wording_pattern','required_placeholders','exact_wording_review_status','answer_key_language_review_status','distractor_constraints_review_status','context_display_review_status','hebrew_rendering_review_status','protected_preview_gate_review_status','row_level_generation_status','question_allowed','answer_choices_allowed','answer_key_allowed','distractors_allowed','protected_preview_allowed','reviewed_bank_allowed','runtime_allowed','student_facing_allowed','row_level_cautions','yossi_exact_wording_decision','yossi_answer_key_decision','yossi_distractor_decision','yossi_context_display_decision','yossi_hebrew_rendering_decision','yossi_protected_preview_gate_decision','yossi_notes']
REVIEW_STATUS_FIELDS=['exact_wording_review_status','answer_key_language_review_status','distractor_constraints_review_status','context_display_review_status','hebrew_rendering_review_status','protected_preview_gate_review_status']
DECISION_FIELDS=['yossi_exact_wording_decision','yossi_answer_key_decision','yossi_distractor_decision','yossi_context_display_decision','yossi_hebrew_rendering_decision','yossi_protected_preview_gate_decision']
GATE_FIELDS={'question_allowed':'needs_review','answer_choices_allowed':'false','answer_key_allowed':'false','distractors_allowed':'false','protected_preview_allowed':'false','reviewed_bank_allowed':'false','runtime_allowed':'false','student_facing_allowed':'false'}
APPROVED={'g2p2_002','g2p2_003','g2p2_006','g2p2_007','g2p2_009','g2p2_014','g2p2_016','g2p2_017','g2p2_019','g2p2_020'}
REVISION={'g2p2_001','g2p2_010','g2p2_012','g2p2_013'}
HEBREW_RE=re.compile(r'[\u0590-\u05FF]')
def rel(p): return p.relative_to(ROOT).as_posix()
def load_tsv(p):
    with p.open('r',encoding='utf-8',newline='') as h:
        r=csv.DictReader(h,delimiter='\t'); return list(r.fieldnames or []),list(r)
def validate_gate_2_pre_generation_review():
    errors=[]
    for p in (README,REVIEW_TSV,REVIEW_MD,REVIEW_CSV,REPORT,APPLIED_REPORT,EXACT_TSV):
        if not p.exists(): errors.append(f'missing pre-generation artifact: {rel(p)}')
    if errors: return {'valid':False,'errors':errors}
    fields,rows=load_tsv(REVIEW_TSV)
    if fields!=REQUIRED_COLUMNS: errors.append('pre-generation TSV columns do not match required schema')
    if len(rows)!=14: errors.append(f'pre-generation TSV must have exactly 14 rows, found {len(rows)}')
    _,exact_rows=load_tsv(EXACT_TSV); exact={r['exact_wording_candidate_id']:r for r in exact_rows}
    decision_counts=Counter(); status_counts=Counter(r.get('row_level_generation_status','') for r in rows)
    for r in rows:
        cid=r.get('pre_generation_review_id','?'); gid=r.get('gate_2_input_candidate_id','')
        ex=exact.get(r.get('exact_wording_candidate_id',''))
        if not ex: errors.append(f'{cid}: must link to exact wording row')
        else:
            for f in ('template_skeleton_candidate_id','gate_2_input_candidate_id','source_ref','hebrew_token','hebrew_phrase','approved_family','non_student_facing_wording_pattern','required_placeholders'):
                if r.get(f,'')!=ex.get(f,''): errors.append(f'{cid}: {f} must match exact wording row')
        for f in REVIEW_STATUS_FIELDS:
            if r.get(f)!='needs_review': errors.append(f'{cid}: {f} must be needs_review')
        for f,v in GATE_FIELDS.items():
            if r.get(f)!=v: errors.append(f'{cid}: {f} must be {v}')
        vals={r.get(f,'') for f in DECISION_FIELDS};
        if len(vals)!=1: errors.append(f'{cid}: all Yossi decision fields must match')
        decision=next(iter(vals)) if vals else ''
        decision_counts[decision]+=1
        if gid in APPROVED:
            if decision!='approve_for_controlled_draft_generation': errors.append(f'{cid}: approved row has wrong decision')
            if r.get('row_level_generation_status')!='approved_for_controlled_draft_generation': errors.append(f'{cid}: approved row has wrong generation status')
        elif gid in REVISION:
            if decision!='approve_with_revision': errors.append(f'{cid}: revision row has wrong decision')
            if r.get('row_level_generation_status')!='blocked_pending_revision': errors.append(f'{cid}: revision row has wrong generation status')
            for phrase in ('base noun','not as','recognition'):
                if phrase not in r.get('yossi_notes',''): errors.append(f'{cid}: revision note missing {phrase}')
        else: errors.append(f'{cid}: unexpected Gate 2 row {gid}')
        if not r.get('yossi_notes'): errors.append(f'{cid}: Yossi notes must be populated')
        for f in ('hebrew_token','hebrew_phrase'):
            val=r.get(f,'')
            if not HEBREW_RE.search(val): errors.append(f'{cid}: {f} must contain Hebrew')
            if '???' in val or '×' in val or 'Ö' in val: errors.append(f'{cid}: {f} contains corruption')
    if not REVIEW_CSV.read_bytes().startswith(b'\xef\xbb\xbf'): errors.append('pre-generation Yossi CSV must be UTF-8-BOM')
    with REVIEW_CSV.open('r',encoding='utf-8-sig',newline='') as h: csv_rows=list(csv.DictReader(h))
    if len(csv_rows)!=len(rows): errors.append('pre-generation Yossi CSV row count must match review TSV')
    if decision_counts.get('approve_for_controlled_draft_generation',0)!=10: errors.append('expected 10 controlled draft approvals')
    if decision_counts.get('approve_with_revision',0)!=4: errors.append('expected 4 approve_with_revision rows')
    text='\n'.join(p.read_text(encoding='utf-8-sig' if p.suffix=='.csv' else 'utf-8') for p in (README,REVIEW_TSV,REVIEW_MD,REVIEW_CSV,REPORT,APPLIED_REPORT))
    for phrase in ('No final questions','No protected-preview content','No reviewed-bank entries','No runtime','student-facing','All gates remain closed'):
        if phrase not in text: errors.append(f'missing safety phrase: {phrase}')
    for bad in ('???','×','Ö'):
        if bad in text: errors.append(f'artifacts contain corrupt phrase: {bad}')
    return {'valid':not errors,'errors':errors,'review_path':rel(REVIEW_TSV),'row_count':len(rows),'decision_counts':dict(decision_counts),'status_counts':dict(status_counts)}
def main():
    s=validate_gate_2_pre_generation_review(); print(json.dumps(s,ensure_ascii=False,indent=2)); return 0 if s['valid'] else 1
if __name__=='__main__': raise SystemExit(main())
