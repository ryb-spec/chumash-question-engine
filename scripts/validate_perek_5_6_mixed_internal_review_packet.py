from __future__ import annotations
import csv,json,sys
from pathlib import Path
if hasattr(sys.stdout,"reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT=Path(__file__).resolve().parents[1]
PACKET_DIR=ROOT/"data/gate_2_protected_preview_packets"; REPORTS=PACKET_DIR/"reports"
PACKET_TSV=PACKET_DIR/"bereishis_perek_5_6_mixed_limited_internal_review_packet.tsv"
PACKET_MD=REPORTS/"bereishis_perek_5_6_mixed_limited_internal_review_packet_2026_04_29.md"
PACKET_JSON=REPORTS/"bereishis_perek_5_6_mixed_limited_internal_review_packet_2026_04_29.json"
GENERATION_REPORT=REPORTS/"bereishis_perek_5_6_mixed_limited_internal_review_packet_generation_report_2026_04_29.md"
REVIEW_CHECKLIST=REPORTS/"bereishis_perek_5_6_mixed_limited_internal_review_checklist_2026_04_29.md"
EXCLUDED_REGISTER=REPORTS/"bereishis_perek_5_6_mixed_packet_excluded_register_2026_04_29.md"
PIPELINE_STATUS=ROOT/"data/pipeline_rounds/bereishis_perek_5_6_mixed_internal_review_packet_created_2026_04_29.md"
REQUIRED_FILES=(PACKET_TSV,PACKET_MD,PACKET_JSON,GENERATION_REPORT,REVIEW_CHECKLIST,EXCLUDED_REGISTER,PIPELINE_STATUS)
EXPECTED_INCLUDED_IDS=["g2srcdisc_p5_001","g2srcdisc_p5_005","g2srcdisc_p6_001","g2srcdisc_p6_006","g2srcdisc_p6_007"]
EXPECTED_CLEAN_IDS=["g2srcdisc_p5_001","g2srcdisc_p5_005"]
EXPECTED_REVISION_WATCH_IDS=["g2srcdisc_p6_001","g2srcdisc_p6_006","g2srcdisc_p6_007"]
EXPECTED_EXCLUDED_IDS=["g2srcdisc_p5_002","g2srcdisc_p5_003","g2srcdisc_p5_004","g2srcdisc_p6_002","g2srcdisc_p6_003","g2srcdisc_p6_004","g2srcdisc_p6_005"]
EXPECTED_DECISIONS={"g2srcdisc_p5_001":"approve_for_limited_internal_preview","g2srcdisc_p5_005":"approve_for_limited_internal_preview","g2srcdisc_p6_001":"approve_with_revision","g2srcdisc_p6_006":"approve_with_revision","g2srcdisc_p6_007":"approve_with_revision"}
FALSE_FIELDS=("runtime_allowed","reviewed_bank_allowed","student_facing_allowed","perek_5_activated","perek_6_activated")
REQUIRED_TSV_COLUMNS="packet_item_id source_candidate_id perek lane pasuk_ref hebrew_target proposed_question expected_answer distractors proposed_skill canonical_skill_id prior_review_decision internal_review_decision next_gate_status observation_required_before_broader_use readiness_reason required_caution spacing_or_balance_note runtime_allowed reviewed_bank_allowed student_facing_allowed perek_5_activated perek_6_activated".split()
FORBIDDEN=("runtime_allowed=true",'"runtime_allowed": true',"reviewed_bank_allowed=true",'"reviewed_bank_allowed": true',"student_facing_allowed=true",'"student_facing_allowed": true',"promoted_to_runtime","approved_for_runtime","Perek 5 is active runtime","Perek 6 is active runtime","Perek 5 runtime is active","Perek 6 runtime is active","reviewed-bank promotion occurred","public launch","fake observation result","fake student data created: true")
def rel(p:Path)->str: return p.relative_to(ROOT).as_posix()
def text(p:Path)->str: return p.read_text(encoding="utf-8-sig")
def rows(p:Path):
    with p.open(encoding="utf-8-sig",newline="") as h:
        r=csv.DictReader(h,delimiter="\t"); return list(r.fieldnames or []),list(r)
def load(p:Path,errors:list[str])->dict:
    try: x=json.loads(text(p))
    except json.JSONDecodeError as e: errors.append(f"{rel(p)} is invalid JSON: {e}"); return {}
    if not isinstance(x,dict): errors.append(f"{rel(p)} must be a JSON object"); return {}
    return x
def require_false(d:dict,k:str,errors:list[str],ctx:str):
    if d.get(k) is not False: errors.append(f"{ctx}: {k} must be false")
def validate_tsv(errors:list[str])->list[str]:
    fields,rs=rows(PACKET_TSV)
    if fields!=REQUIRED_TSV_COLUMNS: errors.append("packet TSV columns do not match required mixed packet schema")
    if len(rs)!=5: errors.append(f"packet TSV must have exactly 5 rows, found {len(rs)}")
    ids=[r.get("source_candidate_id","") for r in rs]
    if ids!=EXPECTED_INCLUDED_IDS: errors.append(f"packet TSV source IDs must be exactly {EXPECTED_INCLUDED_IDS}")
    clean=[r.get("source_candidate_id","") for r in rs if r.get("lane")=="clean_approved"]
    watch=[r.get("source_candidate_id","") for r in rs if r.get("lane")=="revision_watch"]
    if clean!=EXPECTED_CLEAN_IDS: errors.append(f"clean_approved lane must be exactly {EXPECTED_CLEAN_IDS}")
    if watch!=EXPECTED_REVISION_WATCH_IDS: errors.append(f"revision_watch lane must be exactly {EXPECTED_REVISION_WATCH_IDS}")
    for x in EXPECTED_EXCLUDED_IDS:
        if x in ids: errors.append(f"{x} must not appear in packet TSV")
    for r in rs:
        ctx=r.get("packet_item_id","packet row"); cid=r.get("source_candidate_id","")
        for f in FALSE_FIELDS:
            if r.get(f)!="false": errors.append(f"{ctx}: {f} must be false")
        if r.get("expected_answer")!="noun": errors.append(f"{ctx}: expected_answer must be noun")
        if r.get("internal_review_decision")!=EXPECTED_DECISIONS.get(cid): errors.append(f"{ctx}: internal_review_decision mismatch")
        if r.get("observation_required_before_broader_use")!="true": errors.append(f"{ctx}: observation_required_before_broader_use must be true")
        if r.get("lane")=="revision_watch" and "not clean-approved" not in r.get("required_caution",""): errors.append(f"{ctx}: revision-watch caution must say not clean-approved")
    return ids
def validate_json(p:dict,errors:list[str])->list[str]:
    checks={"packet_status":"mixed_limited_internal_review_only","scope":"Bereishis Perek 5-6","item_count":5,"clean_approved_count":2,"revision_watch_count":3}
    for k,v in checks.items():
        if p.get(k)!=v: errors.append(f"{k} must be {v}")
    if p.get("included_candidate_ids")!=EXPECTED_INCLUDED_IDS: errors.append("included_candidate_ids mismatch")
    if sorted(p.get("excluded_candidate_ids",[]))!=sorted(EXPECTED_EXCLUDED_IDS): errors.append("excluded_candidate_ids must include exactly the seven excluded candidates")
    for k in ("fake_review_decisions_created","fake_observations_created","fake_student_data_created","source_truth_changed","question_selection_changed","scoring_mastery_changed"): require_false(p,k,errors,"packet JSON")
    its=p.get("items")
    if not isinstance(its,list) or len(its)!=5: errors.append("packet JSON items must contain exactly 5 items"); its=[]
    ids=[str(i.get("source_candidate_id","")) for i in its if isinstance(i,dict)]
    if ids!=EXPECTED_INCLUDED_IDS: errors.append(f"packet JSON source IDs must be exactly {EXPECTED_INCLUDED_IDS}")
    clean=[str(i.get("source_candidate_id","")) for i in its if isinstance(i,dict) and i.get("lane")=="clean_approved"]
    watch=[str(i.get("source_candidate_id","")) for i in its if isinstance(i,dict) and i.get("lane")=="revision_watch"]
    if clean!=EXPECTED_CLEAN_IDS: errors.append(f"JSON clean_approved lane must be exactly {EXPECTED_CLEAN_IDS}")
    if watch!=EXPECTED_REVISION_WATCH_IDS: errors.append(f"JSON revision_watch lane must be exactly {EXPECTED_REVISION_WATCH_IDS}")
    for x in EXPECTED_EXCLUDED_IDS:
        if x in ids: errors.append(f"{x} must not appear in packet JSON items")
    for i in its:
        if not isinstance(i,dict): continue
        ctx=str(i.get("packet_item_id","packet JSON item")); cid=str(i.get("source_candidate_id",""))
        if i.get("internal_review_decision")!=EXPECTED_DECISIONS.get(cid): errors.append(f"{ctx}: internal_review_decision mismatch")
        if i.get("observation_result") is not None: errors.append(f"{ctx}: observation_result must remain null")
        for f in FALSE_FIELDS: require_false(i,f,errors,ctx)
        if i.get("expected_answer")!="noun": errors.append(f"{ctx}: expected_answer must be noun")
        if i.get("lane")=="revision_watch" and "not clean-approved" not in str(i.get("required_caution","")): errors.append(f"{ctx}: revision-watch caution must say not clean-approved")
    return ids
def scan(errors:list[str]):
    req={PACKET_MD:["Revision-watch items are not clean-approved","included only to gather internal review evidence","Perek 5 and Perek 6 remain non-runtime"],GENERATION_REPORT:["Why three Perek 6 revision-watch items are included","still excluded for now","No fake observations"],REVIEW_CHECKLIST:["blank by design","Did the item stay part-of-speech only?","Should this item remain held after observation?"],EXCLUDED_REGISTER:EXPECTED_EXCLUDED_IDS,PIPELINE_STATUS:["mixed five-item internal review packet","These items are not clean-approved","Still not runtime"]}
    for p,phrases in req.items():
        body=text(p); low=body.lower()
        for ph in phrases:
            if ph.lower() not in low: errors.append(f"{rel(p)} missing required phrase: {ph}")
    for p in REQUIRED_FILES:
        body=text(p)
        for pat in FORBIDDEN:
            if pat in body: errors.append(f"{rel(p)} contains forbidden claim: {pat}")
def validate()->dict:
    errors=[]
    for p in REQUIRED_FILES:
        if not p.exists(): errors.append(f"Missing required file: {rel(p)}")
    if errors: return {"ok":False,"errors":errors}
    tsv_ids=validate_tsv(errors); payload=load(PACKET_JSON,errors); json_ids=validate_json(payload,errors); scan(errors)
    return {"ok":not errors,"errors":errors,"tsv_candidate_ids":tsv_ids,"json_candidate_ids":json_ids}
def main()->int:
    r=validate()
    if not r["ok"]:
        for e in r["errors"]: print(f"ERROR: {e}")
        return 1
    print("Perek 5-6 mixed limited internal review packet validation passed."); return 0
if __name__=="__main__": sys.exit(main())
