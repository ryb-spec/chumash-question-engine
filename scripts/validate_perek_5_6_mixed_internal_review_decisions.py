from __future__ import annotations
import csv,json,sys
from pathlib import Path
if hasattr(sys.stdout,"reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT=Path(__file__).resolve().parents[1]
REPORTS=ROOT/"data/gate_2_protected_preview_packets/reports"
PACKET_DIR=ROOT/"data/gate_2_protected_preview_packets"
PHASE_MD=REPORTS/"bereishis_perek_5_6_mixed_internal_review_decisions_and_next_gate_2026_04_29.md"
PHASE_JSON=REPORTS/"bereishis_perek_5_6_mixed_internal_review_decisions_and_next_gate_2026_04_29.json"
PACKET_TSV=PACKET_DIR/"bereishis_perek_5_6_mixed_limited_internal_review_packet.tsv"
PACKET_MD=REPORTS/"bereishis_perek_5_6_mixed_limited_internal_review_packet_2026_04_29.md"
PACKET_JSON=REPORTS/"bereishis_perek_5_6_mixed_limited_internal_review_packet_2026_04_29.json"
CHECKLIST=REPORTS/"bereishis_perek_5_6_mixed_limited_internal_review_checklist_2026_04_29.md"
EXCLUDED_REGISTER=REPORTS/"bereishis_perek_5_6_mixed_packet_excluded_register_2026_04_29.md"
REQUIRED_FILES=(PHASE_MD,PHASE_JSON,PACKET_TSV,PACKET_MD,PACKET_JSON,CHECKLIST,EXCLUDED_REGISTER)
EXPECTED_CLEAN_IDS=["g2srcdisc_p5_001","g2srcdisc_p5_005"]
EXPECTED_REVISION_IDS=["g2srcdisc_p6_001","g2srcdisc_p6_006","g2srcdisc_p6_007"]
EXPECTED_INCLUDED_IDS=EXPECTED_CLEAN_IDS+EXPECTED_REVISION_IDS
EXPECTED_EXCLUDED_IDS=["g2srcdisc_p5_002","g2srcdisc_p5_003","g2srcdisc_p5_004","g2srcdisc_p6_002","g2srcdisc_p6_003","g2srcdisc_p6_004","g2srcdisc_p6_005"]
EXPECTED_DECISIONS={"g2srcdisc_p5_001":"approve_for_limited_internal_preview","g2srcdisc_p5_005":"approve_for_limited_internal_preview","g2srcdisc_p6_001":"approve_with_revision","g2srcdisc_p6_006":"approve_with_revision","g2srcdisc_p6_007":"approve_with_revision"}
EXPECTED_TARGETS={"g2srcdisc_p5_001":"סֵפֶר","g2srcdisc_p5_005":"בֵּן","g2srcdisc_p6_001":"בָשָׂר","g2srcdisc_p6_006":"פֶתַח","g2srcdisc_p6_007":"מַבּוּל"}
FALSE_FIELDS=("runtime_allowed","reviewed_bank_allowed","student_facing_allowed","perek_5_activated","perek_6_activated")
FORBIDDEN=("runtime_allowed=true",'"runtime_allowed": true',"reviewed_bank_allowed=true",'"reviewed_bank_allowed": true',"student_facing_allowed=true",'"student_facing_allowed": true',"promoted_to_runtime","approved_for_runtime","Perek 5 is active runtime","Perek 6 is active runtime","Perek 5 runtime is active","Perek 6 runtime is active","fake observation result","fake student data created: true")
def rel(p:Path)->str: return p.relative_to(ROOT).as_posix()
def text(p:Path)->str: return p.read_text(encoding="utf-8-sig")
def load(p:Path,errors:list[str])->dict:
    try: x=json.loads(text(p))
    except json.JSONDecodeError as e: errors.append(f"{rel(p)} invalid JSON: {e}"); return {}
    if not isinstance(x,dict): errors.append(f"{rel(p)} must contain a JSON object"); return {}
    return x
def require_false(d:dict,k:str,errors:list[str],ctx:str):
    if d.get(k) is not False: errors.append(f"{ctx}: {k} must be false")
def validate_phase_json(payload:dict,errors:list[str])->None:
    expected_scalars={"streamlined_process_version":"v1","phase_number":7,"phase_name":"Observation Decisions + Next-Gate Authorization","item_count":5,"clean_approved_count":2,"revision_watch_count":3,"excluded_count":7,"fake_observations_created":False,"student_observation_evidence_recorded":False,"runtime_scope_widened":False,"reviewed_bank_promoted":False,"student_facing_created":False,"perek_5_activated":False,"perek_6_activated":False}
    for k,v in expected_scalars.items():
        if payload.get(k)!=v: errors.append(f"phase JSON {k} must be {v!r}")
    decisions=payload.get("decisions")
    if not isinstance(decisions,list) or len(decisions)!=5: errors.append("phase JSON must contain exactly 5 decisions"); decisions=[]
    ids=[d.get("source_candidate_id") for d in decisions if isinstance(d,dict)]
    if ids!=EXPECTED_INCLUDED_IDS: errors.append(f"decision IDs must be exactly {EXPECTED_INCLUDED_IDS}")
    clean=[d.get("source_candidate_id") for d in decisions if isinstance(d,dict) and d.get("lane")=="clean_approved"]
    revision=[d.get("source_candidate_id") for d in decisions if isinstance(d,dict) and d.get("lane")=="revision_watch"]
    if clean!=EXPECTED_CLEAN_IDS: errors.append("clean_approved lane IDs mismatch")
    if revision!=EXPECTED_REVISION_IDS: errors.append("revision_watch lane IDs mismatch")
    for d in decisions:
        if not isinstance(d,dict): continue
        cid=str(d.get("source_candidate_id")); ctx=cid
        if d.get("internal_review_decision")!=EXPECTED_DECISIONS.get(cid): errors.append(f"{ctx}: decision mismatch")
        if d.get("hebrew_target")!=EXPECTED_TARGETS.get(cid): errors.append(f"{ctx}: Hebrew target mismatch")
        expected_status="clean_limited_internal_preview_ready" if cid in EXPECTED_CLEAN_IDS else "revision_watch_internal_observation_only"
        if d.get("next_gate_status")!=expected_status: errors.append(f"{ctx}: next_gate_status mismatch")
        if d.get("observation_required_before_broader_use") is not True: errors.append(f"{ctx}: observation_required_before_broader_use must be true")
        for f in FALSE_FIELDS: require_false(d,f,errors,ctx)
    excluded=payload.get("excluded_candidates")
    if not isinstance(excluded,list) or len(excluded)!=7: errors.append("phase JSON must contain exactly 7 excluded candidates"); excluded=[]
    excluded_ids=[e.get("source_candidate_id") for e in excluded if isinstance(e,dict)]
    if sorted(excluded_ids)!=sorted(EXPECTED_EXCLUDED_IDS): errors.append("excluded candidate IDs mismatch")
    for e in excluded:
        if isinstance(e,dict) and e.get("eligible_for_next_gate") is not False: errors.append(f"{e.get('source_candidate_id')}: eligible_for_next_gate must be false")
def validate_packet_json(errors:list[str])->None:
    payload=load(PACKET_JSON,errors); items=payload.get("items",[])
    if not isinstance(items,list): errors.append("packet JSON items must be a list"); return
    for i in items:
        if not isinstance(i,dict): continue
        cid=str(i.get("source_candidate_id")); ctx=f"packet JSON {cid}"
        if cid in EXPECTED_DECISIONS and i.get("internal_review_decision")!=EXPECTED_DECISIONS[cid]: errors.append(f"{ctx}: internal decision mismatch")
        if i.get("observation_result") is not None: errors.append(f"{ctx}: observation_result must remain null")
        for f in FALSE_FIELDS: require_false(i,f,errors,ctx)
def validate_packet_tsv(errors:list[str])->None:
    with PACKET_TSV.open(encoding="utf-8-sig",newline="") as h:
        rows=list(csv.DictReader(h,delimiter="\t"))
    if len(rows)!=5: errors.append("packet TSV must contain exactly 5 rows")
    ids=[r.get("source_candidate_id") for r in rows]
    if ids!=EXPECTED_INCLUDED_IDS: errors.append("packet TSV included IDs mismatch")
    for r in rows:
        cid=str(r.get("source_candidate_id")); ctx=f"packet TSV {cid}"
        if r.get("internal_review_decision")!=EXPECTED_DECISIONS.get(cid): errors.append(f"{ctx}: internal_review_decision mismatch")
        for f in FALSE_FIELDS:
            if r.get(f)!="false": errors.append(f"{ctx}: {f} must be false")
def scan_texts(errors:list[str])->None:
    for p in REQUIRED_FILES:
        body=text(p)
        for pat in FORBIDDEN:
            if pat in body: errors.append(f"{rel(p)} contains forbidden phrase: {pat}")
    phase=text(PHASE_MD)
    required=["Phase 7 - Observation Decisions + Next-Gate Authorization","No student observation evidence is being invented","Revision-watch items are not clean-approved","No runtime activation","No reviewed-bank promotion"]
    for phrase in required:
        if phrase not in phase: errors.append(f"phase report missing required phrase: {phrase}")
    checklist=text(CHECKLIST)
    if "Observation fields are blank by design" not in checklist: errors.append("checklist must say observation fields are blank by design")
    if "Revision-watch items are not clean-approved" not in checklist: errors.append("checklist must preserve revision-watch warning")
def validate()->dict:
    errors=[]
    for p in REQUIRED_FILES:
        if not p.exists(): errors.append(f"Missing required file: {rel(p)}")
    if errors: return {"ok":False,"errors":errors}
    payload=load(PHASE_JSON,errors); validate_phase_json(payload,errors); validate_packet_json(errors); validate_packet_tsv(errors); scan_texts(errors)
    return {"ok":not errors,"errors":errors,"phase_json":payload}
def main()->int:
    result=validate()
    if not result["ok"]:
        for error in result["errors"]: print(f"ERROR: {error}")
        return 1
    print("Perek 5–6 mixed internal review decisions validation passed.")
    return 0
if __name__=="__main__": sys.exit(main())
