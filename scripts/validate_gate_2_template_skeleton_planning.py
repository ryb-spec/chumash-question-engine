from __future__ import annotations
import csv,json,re
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DIR=ROOT/'data'/'gate_2_template_skeleton_planning'
README=DIR/'README.md'
TSV=DIR/'bereishis_perek_2_template_skeleton_planning.tsv'
PACKET=DIR/'reports'/'bereishis_perek_2_template_skeleton_yossi_review_packet.md'
PLAN_REPORT=DIR/'reports'/'bereishis_perek_2_template_skeleton_planning_report.md'
EXCLUDED_REPORT=DIR/'reports'/'bereishis_perek_2_template_skeleton_excluded_report.md'
APPLIED_REPORT=DIR/'reports'/'bereishis_perek_2_template_skeleton_yossi_review_applied.md'
GATE2=ROOT/'data'/'gate_2_input_planning'/'bereishis_perek_2_gate_2_input_planning_proposal.tsv'
REQUIRED_COLUMNS=['template_skeleton_candidate_id','gate_2_input_candidate_id','source_candidate_id','source_ref','hebrew_token','hebrew_phrase','approved_family','canonical_skill_id','canonical_standard_anchor','skeleton_family','skeleton_policy_version','non_student_facing_skeleton_label','required_variables','forbidden_outputs','teacher_wording_review_status','answer_key_review_status','distractor_review_status','context_display_review_status','hebrew_rendering_review_status','protected_preview_gate_review_status','template_skeleton_status','question_allowed','answer_choices_allowed','answer_key_allowed','distractors_allowed','protected_preview_allowed','reviewed_bank_allowed','runtime_allowed','student_facing_allowed','cautions','yossi_template_skeleton_decision','yossi_template_skeleton_notes']
REVIEW_STATUS_FIELDS=['teacher_wording_review_status','answer_key_review_status','distractor_review_status','context_display_review_status','hebrew_rendering_review_status','protected_preview_gate_review_status']
GATE_FIELDS={'question_allowed':'needs_review','answer_choices_allowed':'false','answer_key_allowed':'false','distractors_allowed':'false','protected_preview_allowed':'false','reviewed_bank_allowed':'false','runtime_allowed':'false','student_facing_allowed':'false'}
EXCLUDED_GATE2_IDS={'g2p2_004','g2p2_005','g2p2_008','g2p2_011','g2p2_015','g2p2_018'}
APPROVED_DECISION='approve_for_template_planning'
APPROVED_STATUS='yossi_approved_for_template_planning'
EXPECTED_STATUS_BY_DECISION={'approve_for_exact_wording_planning':'yossi_approved_for_exact_wording_planning','approve_with_revision':'yossi_approved_with_revision_for_exact_wording_planning'}
EXPECTED_COUNTS={'approve_for_exact_wording_planning':10,'approve_with_revision':4,'needs_follow_up':0,'block_for_now':0,'source_only':0}
REVISION_NOTE_PHRASES={'g2skel_p2_001':('שמים','sky/heavens','article/prefix'),'g2skel_p2_007':('זהב','gold','article/prefix'),'g2skel_p2_008':('אבן','stone','vav/prefix'),'g2skel_p2_009':('נהר','river','article/prefix')}
HEBREW_RE=re.compile(r'[\u0590-\u05FF]')

def rel(p:Path)->str: return p.relative_to(ROOT).as_posix()
def load_tsv(p:Path):
    with p.open('r',encoding='utf-8',newline='') as h:
        r=csv.DictReader(h,delimiter='\t'); return list(r.fieldnames or []),list(r)

def validate_gate_2_template_skeleton_planning():
    errors=[]
    for p in (README,TSV,PACKET,PLAN_REPORT,EXCLUDED_REPORT,APPLIED_REPORT,GATE2):
        if not p.exists(): errors.append(f'missing artifact: {rel(p)}')
    if errors: return {'valid':False,'errors':errors}
    fields,rows=load_tsv(TSV)
    if fields!=REQUIRED_COLUMNS: errors.append('template-skeleton TSV columns do not match required schema')
    if len(rows)!=14: errors.append(f'template-skeleton TSV must have exactly 14 rows, found {len(rows)}')
    _,grows=load_tsv(GATE2)
    gate2={r['gate_2_input_candidate_id']:r for r in grows}
    approved={r['gate_2_input_candidate_id'] for r in grows if r.get('yossi_gate_2_decision')==APPROVED_DECISION and r.get('gate_2_candidate_status')==APPROVED_STATUS}
    included=set(); counts=Counter(r.get('yossi_template_skeleton_decision','') for r in rows)
    for r in rows:
        cid=r.get('template_skeleton_candidate_id','?'); gid=r.get('gate_2_input_candidate_id','')
        included.add(gid)
        if gid not in approved: errors.append(f'{cid}: linked Gate 2 row must be approved for template planning')
        if gid in EXCLUDED_GATE2_IDS: errors.append(f'{cid}: excluded Gate 2 row included')
        src=gate2.get(gid,{})
        for f in ('source_candidate_id','source_ref','hebrew_token','hebrew_phrase','approved_family','canonical_skill_id','canonical_standard_anchor'):
            if src and r.get(f,'')!=src.get(f,''): errors.append(f'{cid}: {f} must match linked Gate 2 row')
        if r.get('approved_family')!='basic_noun_recognition' or r.get('skeleton_family')!='basic_noun_recognition': errors.append(f'{cid}: family must remain basic_noun_recognition')
        for f in REVIEW_STATUS_FIELDS:
            if r.get(f)!='needs_review': errors.append(f'{cid}: {f} must be needs_review')
        for f,v in GATE_FIELDS.items():
            if r.get(f)!=v: errors.append(f'{cid}: {f} must be {v}')
        dec=r.get('yossi_template_skeleton_decision',''); status=EXPECTED_STATUS_BY_DECISION.get(dec)
        if not status: errors.append(f'{cid}: unexpected decision {dec}')
        elif r.get('template_skeleton_status')!=status: errors.append(f'{cid}: template_skeleton_status must be {status}')
        if not r.get('yossi_template_skeleton_notes'): errors.append(f'{cid}: Yossi notes must be populated')
        if dec=='approve_with_revision':
            for phrase in REVISION_NOTE_PHRASES.get(cid,()):
                if phrase not in (r.get('yossi_template_skeleton_notes','')+r.get('cautions','')): errors.append(f'{cid}: missing revision phrase {phrase}')
        elif cid in REVISION_NOTE_PHRASES: errors.append(f'{cid}: expected approve_with_revision')
        for f in ('hebrew_token','hebrew_phrase'):
            val=r.get(f,'')
            if not HEBREW_RE.search(val): errors.append(f'{cid}: {f} must contain Hebrew')
            if '???' in val or '×' in val or 'Ö' in val: errors.append(f'{cid}: {f} contains corruption')
    if included!=approved: errors.append('included Gate 2 IDs must exactly match approved Gate 2 IDs')
    for d,n in EXPECTED_COUNTS.items():
        if counts.get(d,0)!=n: errors.append(f'expected {n} {d} rows')
    text='\n'.join(p.read_text(encoding='utf-8') for p in (README,TSV,PACKET,PLAN_REPORT,EXCLUDED_REPORT,APPLIED_REPORT))
    for phrase in ('No final questions','No answer choices','No answer keys','No distractors','No controlled drafts','No protected-preview content','No reviewed-bank entries','No runtime','student-facing','All gates remain closed'):
        if phrase not in text: errors.append(f'missing safety phrase: {phrase}')
    for bad in ('???','×','Ö'):
        if bad in text: errors.append(f'artifacts contain corrupt phrase: {bad}')
    return {'valid':not errors,'errors':errors,'skeleton_path':rel(TSV),'row_count':len(rows),'decision_counts':dict(counts),'included_gate_2_ids':sorted(included)}

def main():
    s=validate_gate_2_template_skeleton_planning(); print(json.dumps(s,ensure_ascii=False,indent=2)); return 0 if s['valid'] else 1
if __name__=='__main__': raise SystemExit(main())
