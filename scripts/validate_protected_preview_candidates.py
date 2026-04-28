from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'data'/'protected_preview_candidates'; REPORTS=BASE/'reports'
README=BASE/'README.md'; TSV=BASE/'bereishis_perek_1_first_protected_preview_candidates.tsv'
PACKET=REPORTS/'bereishis_perek_1_first_protected_preview_candidate_review_packet.md'
GEN=REPORTS/'bereishis_perek_1_first_protected_preview_candidate_generation_report.md'
EXC=REPORTS/'bereishis_perek_1_first_protected_preview_candidate_excluded_preserved_report.md'
GATE=ROOT/'data'/'protected_preview_planning_gate'/'bereishis_perek_1_first_protected_preview_planning_gate.tsv'
REQ={'protected_preview_candidate_id','preview_gate_candidate_id','draft_item_id','pre_generation_review_id','ref','approved_family','hebrew_token','hebrew_phrase','draft_prompt','answer_choices','expected_answer','correct_answer','explanation','source_evidence_note','caution_note','draft_review_status','preview_gate_candidate_status','protected_preview_candidate_status','protected_preview_review_status','answer_key_review_status','distractor_review_status','hebrew_rendering_review_status','context_display_review_status','protected_preview_allowed','reviewed_bank_allowed','runtime_allowed','student_facing_allowed','internal_protected_preview_packet_allowed','yossi_protected_preview_decision','yossi_protected_preview_notes'}
STATUS={'protected_preview_review_status','answer_key_review_status','distractor_review_status','hebrew_rendering_review_status','context_display_review_status'}
GATES={'protected_preview_allowed','reviewed_bank_allowed','runtime_allowed','student_facing_allowed'}
FORBIDDEN={'protected_preview_ready','reviewed_bank_ready','runtime_ready','student_facing','approved_for_preview','approved_for_reviewed_bank','approved_for_runtime'}
ET='\u05d0\u05ea'; HIBDIL='\u05d4\u05d1\u05d3\u05d9\u05dc'; BDL='\u05d1\u05d3\u05dc'; CHAYAH='\u05d7\u05d9\u05d4'

def rel(p:Path)->str: return p.relative_to(ROOT).as_posix()
def read_tsv(p:Path):
    with p.open('r',encoding='utf-8',newline='') as f:
        r=csv.DictReader(f,delimiter='\t'); return r.fieldnames or [], list(r)
def has_hebrew(v:str)->bool: return any('\u0590'<=c<='\u05ff' for c in v)
def bad_phrase(text:str, phrase:str)->bool:
    for line in text.lower().splitlines():
        if phrase in line and not any(m in line for m in ('not ','no ','false','closed','does not','still requires')):
            return True
    return False

def validate_protected_preview_candidates()->dict[str,object]:
    errors=[]; paths=(README,TSV,PACKET,GEN,EXC,GATE)
    for p in paths:
        if not p.exists(): errors.append(f'missing artifact: {rel(p)}')
    if errors: return {'valid':False,'errors':errors}
    fields, rows=read_tsv(TSV)
    if missing:=sorted(REQ-set(fields)): errors.append(f'candidate TSV missing columns: {missing}')
    if len(rows)!=18: errors.append(f'candidate TSV must contain exactly 18 rows; found {len(rows)}')
    _, gate_rows=read_tsv(GATE); gate={r['preview_gate_candidate_id']:r for r in gate_rows}
    fam=Counter(r.get('approved_family','') for r in rows)
    tokens={r.get('hebrew_token','') for r in rows}; draft_ids={r.get('draft_item_id','') for r in rows}
    if 'cdraft_b1_016' in draft_ids: errors.append('cdraft_b1_016 must not be included')
    for tok,name in ((CHAYAH,'chayah'),(ET,'et'),(HIBDIL,'hibdil'),(BDL,'bdl')):
        if tok in tokens: errors.append(f'excluded Hebrew token included: {name}')
    for r in rows:
        rid=r.get('protected_preview_candidate_id','unknown'); source=gate.get(r.get('preview_gate_candidate_id',''))
        if not source: errors.append(f'{rid} links to missing planning-gate row')
        elif source.get('yossi_preview_gate_decision')!='approve_for_protected_preview_candidate': errors.append(f'{rid} source gate row is not approved for candidate planning')
        if r.get('approved_family')=='basic_verb_form_recognition': errors.append(f'{rid} must not be verb-form')
        if r.get('protected_preview_candidate_status')!='yossi_approved_for_internal_protected_preview_packet': errors.append(f'{rid} must be yossi_approved_for_internal_protected_preview_packet')
        for f in STATUS:
            if r.get(f)!='needs_yossi_review': errors.append(f'{rid} {f} must be needs_yossi_review')
        for f in GATES:
            if r.get(f)!='false': errors.append(f'{rid} {f} must remain false')
        if r.get('yossi_protected_preview_decision')!='approve_for_internal_protected_preview_packet': errors.append(f'{rid} Yossi protected-preview decision must be approve_for_internal_protected_preview_packet')
        if 'not reviewed-bank approval' not in r.get('yossi_protected_preview_notes',''): errors.append(f'{rid} notes must negate downstream approval')
        if not has_hebrew(r.get('hebrew_token','')) or not has_hebrew(r.get('hebrew_phrase','')): errors.append(f'{rid} must contain real Hebrew')
        if any('??' in r.get(f,'') for f in REQ if f in r): errors.append(f'{rid} contains placeholder corruption')
    text='\n'.join(p.read_text(encoding='utf-8') for p in (README,PACKET,GEN,EXC))
    for phrase in ('protected-preview candidate review packet only','Candidate count: 18',ET,HIBDIL,BDL,CHAYAH):
        if phrase not in text: errors.append(f'required phrase missing: {phrase!r}')
    if '??' in text or '????' in text: errors.append('reports must not contain placeholder corruption')
    for phrase in FORBIDDEN:
        if bad_phrase(text,phrase): errors.append(f'forbidden phrase appears without clear negation: {phrase}')
    readme=README.read_text(encoding='utf-8')
    for p in (TSV,PACKET,GEN,EXC):
        if rel(p) not in readme: errors.append(f'README must link {rel(p)}')
    return {'valid':not errors,'errors':errors,'row_count':len(rows),'family_counts':dict(fam),'decision_counts':dict(Counter(r.get('yossi_protected_preview_decision','') for r in rows))}

def main()->int:
    s=validate_protected_preview_candidates()
    if s['valid']:
        print('Protected-preview candidates validation passed.'); print(f"Rows: {s['row_count']}"); print(f"Family counts: {s['family_counts']}"); return 0
    print('Protected-preview candidates validation failed:')
    for e in s['errors']: print(f'- {e}')
    return 1
if __name__=='__main__': raise SystemExit(main())
