from __future__ import annotations
import csv,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DIR=ROOT/'data'/'gate_2_exact_wording_planning'
README=DIR/'README.md'
EXACT_TSV=DIR/'bereishis_perek_2_exact_wording_planning.tsv'
YOSSI_PACKET=DIR/'reports'/'bereishis_perek_2_exact_wording_yossi_review_packet.md'
PLANNING_REPORT=DIR/'reports'/'bereishis_perek_2_exact_wording_planning_report.md'
SKELETON_TSV=ROOT/'data'/'gate_2_template_skeleton_planning'/'bereishis_perek_2_template_skeleton_planning.tsv'
REQUIRED_COLUMNS=['exact_wording_candidate_id','template_skeleton_candidate_id','gate_2_input_candidate_id','source_ref','hebrew_token','hebrew_phrase','approved_family','exact_wording_family','non_student_facing_wording_pattern','required_placeholders','forbidden_outputs','teacher_wording_review_status','answer_key_review_status','distractor_review_status','context_display_review_status','hebrew_rendering_review_status','protected_preview_gate_review_status','exact_wording_status','question_allowed','answer_choices_allowed','answer_key_allowed','distractors_allowed','protected_preview_allowed','reviewed_bank_allowed','runtime_allowed','student_facing_allowed','cautions','yossi_exact_wording_decision','yossi_exact_wording_notes']
REVIEW_STATUS_FIELDS=['teacher_wording_review_status','answer_key_review_status','distractor_review_status','context_display_review_status','hebrew_rendering_review_status','protected_preview_gate_review_status']
GATE_FIELDS={'question_allowed':'needs_review','answer_choices_allowed':'false','answer_key_allowed':'false','distractors_allowed':'false','protected_preview_allowed':'false','reviewed_bank_allowed':'false','runtime_allowed':'false','student_facing_allowed':'false'}
REVISION_IDS={'g2skel_p2_001','g2skel_p2_007','g2skel_p2_008','g2skel_p2_009'}
EXCLUDED_GATE2_IDS={'g2p2_004','g2p2_005','g2p2_008','g2p2_011','g2p2_015','g2p2_018'}
HEBREW_RE=re.compile(r'[\u0590-\u05FF]')
def rel(p): return p.relative_to(ROOT).as_posix()
def load_tsv(p):
    with p.open('r',encoding='utf-8',newline='') as h:
        r=csv.DictReader(h,delimiter='\t'); return list(r.fieldnames or []),list(r)
def validate_gate_2_exact_wording_planning():
    errors=[]
    for p in (README,EXACT_TSV,YOSSI_PACKET,PLANNING_REPORT,SKELETON_TSV):
        if not p.exists(): errors.append(f'missing exact wording artifact: {rel(p)}')
    if errors: return {'valid':False,'errors':errors}
    fields,rows=load_tsv(EXACT_TSV)
    if fields!=REQUIRED_COLUMNS: errors.append('exact wording TSV columns do not match required schema')
    if len(rows)!=14: errors.append(f'exact wording TSV must have exactly 14 rows, found {len(rows)}')
    _,skels=load_tsv(SKELETON_TSV)
    allowed={r['template_skeleton_candidate_id']:r for r in skels if r.get('yossi_template_skeleton_decision') in {'approve_for_exact_wording_planning','approve_with_revision'}}
    for r in rows:
        cid=r.get('exact_wording_candidate_id','?'); sid=r.get('template_skeleton_candidate_id','')
        sk=allowed.get(sid)
        if not sk: errors.append(f'{cid}: must link to approved template skeleton row')
        else:
            for f in ('gate_2_input_candidate_id','source_ref','hebrew_token','hebrew_phrase','approved_family'):
                if r.get(f,'')!=sk.get(f,''): errors.append(f'{cid}: {f} must match template skeleton row')
        if r.get('gate_2_input_candidate_id') in EXCLUDED_GATE2_IDS: errors.append(f'{cid}: excluded Gate 2 row included')
        if r.get('exact_wording_family')!='basic_noun_recognition': errors.append(f'{cid}: exact_wording_family must be basic_noun_recognition')
        if r.get('non_student_facing_wording_pattern')!='What type of word is {hebrew_token}?': errors.append(f'{cid}: wording pattern must remain placeholder-only')
        for f in REVIEW_STATUS_FIELDS:
            if r.get(f)!='needs_review': errors.append(f'{cid}: {f} must be needs_review')
        if r.get('exact_wording_status')!='planning_only': errors.append(f'{cid}: exact_wording_status must be planning_only')
        for f,v in GATE_FIELDS.items():
            if r.get(f)!=v: errors.append(f'{cid}: {f} must be {v}')
        if r.get('yossi_exact_wording_decision') or r.get('yossi_exact_wording_notes'): errors.append(f'{cid}: Yossi fields must be blank')
        if sid in REVISION_IDS:
            for phrase in ('Base noun only','not article/prefix/vav recognition','answer-key review'):
                if phrase not in r.get('cautions',''): errors.append(f'{cid}: revision caution missing {phrase}')
        for f in ('hebrew_token','hebrew_phrase'):
            val=r.get(f,'')
            if not HEBREW_RE.search(val): errors.append(f'{cid}: {f} must contain Hebrew')
            if '???' in val or '×' in val or 'Ö' in val: errors.append(f'{cid}: {f} contains corruption')
    text='\n'.join(p.read_text(encoding='utf-8') for p in (README,EXACT_TSV,YOSSI_PACKET,PLANNING_REPORT))
    for phrase in ('No final questions','No answer choices','No answer keys','No distractors','No controlled drafts','No protected-preview content','No reviewed-bank entries','No runtime','student-facing','All gates remain closed'):
        if phrase not in text: errors.append(f'missing safety phrase: {phrase}')
    for bad in ('???','×','Ö'):
        if bad in text: errors.append(f'artifacts contain corrupt phrase: {bad}')
    return {'valid':not errors,'errors':errors,'exact_wording_path':rel(EXACT_TSV),'row_count':len(rows),'revision_constrained_count':sum(1 for r in rows if r.get('template_skeleton_candidate_id') in REVISION_IDS)}
def main():
    s=validate_gate_2_exact_wording_planning(); print(json.dumps(s,ensure_ascii=False,indent=2)); return 0 if s['valid'] else 1
if __name__=='__main__': raise SystemExit(main())
