from __future__ import annotations
import csv
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'data'/'protected_preview_packets'; REPORTS=BASE/'reports'
README=BASE/'README.md'; TSV=BASE/'bereishis_perek_1_first_internal_protected_preview_packet.tsv'
PACKET=REPORTS/'bereishis_perek_1_first_internal_protected_preview_packet.md'
GEN=REPORTS/'bereishis_perek_1_first_internal_protected_preview_packet_generation_report.md'
ROUND=REPORTS/'bereishis_perek_1_round_1_completion_report.md'
EXC=REPORTS/'bereishis_perek_1_first_internal_protected_preview_packet_excluded_preserved_report.md'
CAND=ROOT/'data'/'protected_preview_candidates'/'bereishis_perek_1_first_protected_preview_candidates.tsv'
REQ={'protected_preview_packet_item_id','protected_preview_candidate_id','draft_item_id','ref','approved_family','hebrew_token','hebrew_phrase','prompt','answer_choices','expected_answer','correct_answer','explanation','source_evidence_note','caution_note','internal_packet_status','internal_preview_review_status','reviewed_bank_allowed','runtime_allowed','student_facing_allowed','post_preview_review_status','yossi_internal_preview_decision','yossi_internal_preview_notes'}
GATES={'reviewed_bank_allowed','runtime_allowed','student_facing_allowed'}
FORBIDDEN={'reviewed_bank_ready','runtime_ready','student_facing','approved_for_reviewed_bank','approved_for_runtime','approved_for_student_facing'}
ET='\u05d0\u05ea'; HIBDIL='\u05d4\u05d1\u05d3\u05d9\u05dc'; BDL='\u05d1\u05d3\u05dc'; CHAYAH='\u05d7\u05d9\u05d4'
def rel(p:Path)->str: return p.relative_to(ROOT).as_posix()
def read_tsv(p:Path):
    with p.open('r',encoding='utf-8',newline='') as f:
        r=csv.DictReader(f,delimiter='\t'); return r.fieldnames or [], list(r)
def has_hebrew(v:str)->bool: return any('\u0590'<=c<='\u05ff' for c in v)
def bad_phrase(text:str, phrase:str)->bool:
    for line in text.lower().splitlines():
        if phrase in line and not any(m in line for m in ('not ','no ','false','closed','does not','still requires','requires post-preview')):
            return True
    return False
def validate_protected_preview_packet()->dict[str,object]:
    errors=[]; paths=(README,TSV,PACKET,GEN,ROUND,EXC,CAND)
    for p in paths:
        if not p.exists(): errors.append(f'missing artifact: {rel(p)}')
    if errors: return {'valid':False,'errors':errors}
    fields, rows=read_tsv(TSV)
    if missing:=sorted(REQ-set(fields)): errors.append(f'packet TSV missing columns: {missing}')
    if len(rows)!=18: errors.append(f'packet TSV must contain exactly 18 rows; found {len(rows)}')
    _, cand_rows=read_tsv(CAND); cand={r['protected_preview_candidate_id']:r for r in cand_rows}
    fam=Counter(r.get('approved_family','') for r in rows); toks={r.get('hebrew_token','') for r in rows}; drafts={r.get('draft_item_id','') for r in rows}
    if 'cdraft_b1_016' in drafts: errors.append('cdraft_b1_016 must not be included')
    for tok,name in ((CHAYAH,'chayah'),(ET,'et'),(HIBDIL,'hibdil'),(BDL,'bdl')):
        if tok in toks: errors.append(f'excluded Hebrew token included: {name}')
    for r in rows:
        rid=r.get('protected_preview_packet_item_id','unknown'); source=cand.get(r.get('protected_preview_candidate_id',''))
        if not source: errors.append(f'{rid} links to missing protected-preview candidate')
        elif source.get('yossi_protected_preview_decision')!='approve_for_internal_protected_preview_packet': errors.append(f'{rid} source candidate is not approved for internal packet')
        if r.get('approved_family')=='basic_verb_form_recognition': errors.append(f'{rid} must not be verb-form')
        if r.get('internal_packet_status')!='internal_protected_preview_packet_only': errors.append(f'{rid} must be internal packet only')
        if r.get('internal_preview_review_status')!='needs_internal_review': errors.append(f'{rid} internal review status must be needs_internal_review')
        if r.get('post_preview_review_status')!='not_started': errors.append(f'{rid} post-preview review must be not_started')
        for g in GATES:
            if r.get(g)!='false': errors.append(f'{rid} {g} must remain false')
        if r.get('yossi_internal_preview_decision') or r.get('yossi_internal_preview_notes'): errors.append(f'{rid} internal preview decision fields must be blank')
        if not has_hebrew(r.get('hebrew_token','')) or not has_hebrew(r.get('hebrew_phrase','')): errors.append(f'{rid} must contain real Hebrew')
        if any('??' in r.get(f,'') for f in REQ if f in r): errors.append(f'{rid} contains placeholder corruption')
    text='\n'.join(p.read_text(encoding='utf-8') for p in (README,PACKET,GEN,ROUND,EXC))
    for phrase in ('internal protected-preview packet only','Packet item count: 18','Round 1 is complete',ET,HIBDIL,BDL,CHAYAH):
        if phrase not in text: errors.append(f'required phrase missing: {phrase!r}')
    if '??' in text or '????' in text: errors.append('reports must not contain placeholder corruption')
    for phrase in FORBIDDEN:
        if bad_phrase(text,phrase): errors.append(f'forbidden phrase appears without clear negation: {phrase}')
    readme=README.read_text(encoding='utf-8')
    for p in (TSV,PACKET,GEN,ROUND,EXC):
        if rel(p) not in readme: errors.append(f'README must link {rel(p)}')
    return {'valid':not errors,'errors':errors,'row_count':len(rows),'family_counts':dict(fam)}
def main()->int:
    s=validate_protected_preview_packet()
    if s['valid']:
        print('Protected-preview packet validation passed.'); print(f"Rows: {s['row_count']}"); print(f"Family counts: {s['family_counts']}"); return 0
    print('Protected-preview packet validation failed:')
    for e in s['errors']: print(f'- {e}')
    return 1
if __name__=='__main__': raise SystemExit(main())
