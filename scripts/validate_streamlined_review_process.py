from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
if hasattr(sys.stdout,"reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT=Path(__file__).resolve().parents[1]
PROCESS_MD=ROOT/"docs/pipeline/streamlined_review_process_v1.md"
PROCESS_JSON=ROOT/"docs/pipeline/streamlined_review_process_v1.json"
ADOPTION=ROOT/"docs/pipeline/streamlined_review_process_adoption_guide.md"
COMPARISON=ROOT/"data/pipeline_rounds/streamlined_review_process_comparison_2026_04_29.md"
TEMPLATE_DIR=ROOT/"docs/pipeline/templates"
PROMPT_TEMPLATE_DIR=ROOT/"data/pipeline_rounds/prompts/templates"
REQUIRED_TEMPLATES=["source_discovery_bundle_template.md","combined_teacher_review_candidate_planning_checklist_template.md","combined_decisions_applied_template.md","protected_preview_candidate_review_and_readiness_template.md","internal_packet_review_template.md","observation_decisions_next_gate_template.md"]
REQUIRED_PROMPTS=["source_discovery_bundle_prompt_template.md","combined_teacher_review_and_candidate_planning_prompt_template.md","combined_decisions_applied_prompt_template.md","protected_preview_candidate_review_and_readiness_prompt_template.md","protected_preview_decisions_internal_packet_readiness_prompt_template.md","internal_packet_and_review_checklist_prompt_template.md","observation_decisions_next_gate_authorization_prompt_template.md"]
REQUIRED_GATES=["source discovery","teacher review","candidate planning decision","protected-preview candidate review","internal packet review","observation evidence","runtime promotion gate"]
SAFETY_FIELDS=["runtime_allowed=false","reviewed_bank_allowed=false","student_facing_allowed=false","perek_activated=false"]
PLACEHOLDERS=["PEREK_RANGE","BRANCH_NAME","SOURCE_INVENTORY_PATH","CANDIDATE_COUNT","ELIGIBLE_IDS","HELD_IDS","BLOCKED_IDS","NEXT_ALLOWED_TASK"]
RULE="No separate gate unless a human decision, student/internal observation, runtime-safety boundary, or source-confidence status changes."
TIGHTENING=["one phase validator per bundled phase","phase JSON as source of truth","no standalone prompt artifacts unless complex/reusable/high-risk"]
HISTORICAL_SENTINELS=[ROOT/"data/gate_2_protected_preview_packets/bereishis_perek_2_internal_protected_preview_packet.tsv",ROOT/"data/gate_2_protected_preview_packets/bereishis_perek_3_internal_protected_preview_packet.tsv",ROOT/"data/gate_2_source_discovery/bereishis_perek_4_review_only_safe_candidate_inventory.tsv",ROOT/"data/gate_2_source_discovery/bereishis_perek_5_6_review_only_safe_candidate_inventory.tsv"]
def rel(p:Path)->str: return p.relative_to(ROOT).as_posix()
def read(p:Path)->str: return p.read_text(encoding="utf-8-sig")
def load_json(p:Path,errors:list[str])->dict:
    try: x=json.loads(read(p))
    except json.JSONDecodeError as e: errors.append(f"{rel(p)} invalid JSON: {e}"); return {}
    if not isinstance(x,dict): errors.append(f"{rel(p)} must be a JSON object"); return {}
    return x
def changed_paths()->list[str]:
    r=subprocess.run(["git","status","--short"],cwd=ROOT,capture_output=True,text=True,check=False)
    paths=[]
    for line in r.stdout.splitlines():
        if not line.strip(): continue
        p=line[3:].strip()
        if " -> " in p: paths.extend([x.strip() for x in p.split(" -> ")])
        else: paths.append(p)
    return paths
def validate()->dict:
    errors=[]
    required=[PROCESS_MD,PROCESS_JSON,ADOPTION,COMPARISON]+[TEMPLATE_DIR/x for x in REQUIRED_TEMPLATES]+[PROMPT_TEMPLATE_DIR/x for x in REQUIRED_PROMPTS]
    for p in required:
        if not p.exists(): errors.append(f"Missing required file: {rel(p)}")
    if errors: return {"ok":False,"errors":errors}
    data=load_json(PROCESS_JSON,errors)
    phases=data.get("phases",[])
    if len(phases)!=7: errors.append("process JSON must have exactly 7 phases")
    if data.get("target_step_reduction_percent",0)<35: errors.append("target_step_reduction_percent must be at least 35")
    gates=set(data.get("non_negotiable_gates",[]))
    for g in REQUIRED_GATES:
        if g not in gates: errors.append(f"missing non-negotiable gate: {g}")
    rules=data.get("tightening_rules",[])
    for r in TIGHTENING:
        if r not in rules: errors.append(f"missing tightening rule: {r}")
    standard=read(PROCESS_MD)
    if RULE not in standard: errors.append("process standard missing core no-separate-gate rule")
    for phrase in ["Do not activate runtime by default","Do not allow active scope expansion by default","Do not allow reviewed-bank promotion by default","Do not allow student-facing content by default"]:
        if phrase not in standard: errors.append(f"process standard missing default prohibition: {phrase}")
    for p in [TEMPLATE_DIR/x for x in REQUIRED_TEMPLATES]:
        body=read(p)
        for f in SAFETY_FIELDS:
            if f not in body: errors.append(f"{rel(p)} missing safety field {f}")
    for p in [PROMPT_TEMPLATE_DIR/x for x in REQUIRED_PROMPTS]:
        body=read(p)
        for ph in PLACEHOLDERS:
            if ph not in body: errors.append(f"{rel(p)} missing placeholder {ph}")
        for phrase in ["Do not activate runtime","Do not widen active scope","Do not promote reviewed-bank content","Do not create student-facing content","Do not invent fake decisions","Do not invent fake observations","one phase validator","Create tests","Run full pytest","final safety confirmation"]:
            if phrase not in body: errors.append(f"{rel(p)} missing prompt boundary: {phrase}")
    for p in HISTORICAL_SENTINELS:
        if not p.exists(): errors.append(f"historical sentinel missing, possible deletion/rename: {rel(p)}")
    for p in changed_paths():
        if " -> " in p: errors.append(f"renamed path detected: {p}")
    return {"ok":not errors,"errors":errors,"phase_count":len(phases),"target_step_reduction_percent":data.get("target_step_reduction_percent")}
def main()->int:
    r=validate()
    if not r["ok"]:
        for e in r["errors"]: print(f"ERROR: {e}")
        return 1
    print("Streamlined review process validation passed."); return 0
if __name__=="__main__": sys.exit(main())
