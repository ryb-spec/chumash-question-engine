from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "pipeline_rounds" / "round_2_fast_track_pipeline.md"
CONTRACT = ROOT / "data" / "pipeline_rounds" / "round_2_fast_track_pipeline_contract.v1.json"
CHECKLIST = ROOT / "data" / "pipeline_rounds" / "reports" / "round_2_starter_checklist.md"
AUDIT = ROOT / "data" / "pipeline_rounds" / "reports" / "perek_1_round_1_pipeline_audit.md"
PEREK2_SOURCE_AUDIT = (
    ROOT / "data" / "pipeline_rounds" / "reports" / "bereishis_perek_2_gate_1_source_readiness_audit.md"
)
PEREK2_GATE1_REPORT = (
    ROOT / "data" / "pipeline_rounds" / "reports" / "bereishis_perek_2_gate_1_source_enrichment_eligibility_report.md"
)
PEREK2_COMPRESSED_REVIEW_PACKET = (
    ROOT / "data" / "source_skill_enrichment" / "reports" / "bereishis_perek_2_enrichment_compressed_yossi_review_packet.md"
)
PEREK2_COMPRESSED_REVIEW_SUMMARY = (
    ROOT / "data" / "source_skill_enrichment" / "reports" / "bereishis_perek_2_enrichment_compressed_review_summary.md"
)
PEREK2_CLEAN_GROUP_REVIEW_PACKET = (
    ROOT / "data" / "source_skill_enrichment" / "reports" / "bereishis_perek_2_clean_group_yossi_review_packet.md"
)
PEREK2_CLEAN_GROUP_REVIEW_SUMMARY = (
    ROOT / "data" / "source_skill_enrichment" / "reports" / "bereishis_perek_2_clean_group_evidence_strengthening_summary.md"
)
PEREK2_CLEAN_GROUP_APPLIED_REPORT = (
    ROOT / "data" / "source_skill_enrichment" / "reports" / "bereishis_perek_2_clean_group_yossi_review_applied.md"
)
PEREK2_GATE1_ENRICHMENT_DECISION_STATUS = (
    ROOT / "data" / "pipeline_rounds" / "reports" / "bereishis_perek_2_gate_1_enrichment_decision_status_report.md"
)
PEREK2_GATE2_CANDIDATE_POOL_SUMMARY = (
    ROOT / "data" / "pipeline_rounds" / "reports" / "bereishis_perek_2_gate_2_candidate_pool_summary.md"
)
PROMPTS = [
    ROOT / "docs" / "pipeline_rounds" / "codex_prompts" / "gate_1_source_enrichment_eligibility_prompt.md",
    ROOT / "docs" / "pipeline_rounds" / "codex_prompts" / "gate_2_input_planning_template_controls_prompt.md",
    ROOT / "docs" / "pipeline_rounds" / "codex_prompts" / "gate_3_controlled_draft_packet_prompt.md",
    ROOT / "docs" / "pipeline_rounds" / "codex_prompts" / "gate_4_internal_protected_preview_packet_prompt.md",
]
REQUIRED_GATES = {
    "gate_1_source_enrichment_eligibility_readiness",
    "gate_2_input_planning_template_controls",
    "gate_3_controlled_draft_packet",
    "gate_4_internal_protected_preview_packet",
}
PROMPT_PLACEHOLDERS = {
    "{SCOPE_NAME}",
    "{START_REF}",
    "{END_REF}",
    "{SOURCE_MAP_FILE}",
    "{TARGET_ROW_COUNT}",
    "{BATCH_SIZE}",
}
CLOSED_GATE_FIELDS = {
    "protected_preview_allowed",
    "reviewed_bank_allowed",
    "runtime_allowed",
    "student_facing_allowed",
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_contract(errors: list[str]) -> dict:
    try:
        return json.loads(CONTRACT.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"missing artifact: {rel(CONTRACT)}")
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON in {rel(CONTRACT)}: {exc}")
    return {}


def validate_pipeline_rounds() -> dict[str, object]:
    errors: list[str] = []
    for path in (
        DOC,
        CHECKLIST,
        AUDIT,
        PEREK2_SOURCE_AUDIT,
        PEREK2_GATE1_REPORT,
        PEREK2_COMPRESSED_REVIEW_PACKET,
        PEREK2_COMPRESSED_REVIEW_SUMMARY,
        PEREK2_CLEAN_GROUP_REVIEW_PACKET,
        PEREK2_CLEAN_GROUP_REVIEW_SUMMARY,
        PEREK2_CLEAN_GROUP_APPLIED_REPORT,
        PEREK2_GATE1_ENRICHMENT_DECISION_STATUS,
        PEREK2_GATE2_CANDIDATE_POOL_SUMMARY,
        *PROMPTS,
    ):
        if not path.exists():
            errors.append(f"missing artifact: {rel(path)}")
    contract = load_contract(errors)
    if errors:
        return {"valid": False, "errors": errors}

    doc_text = DOC.read_text(encoding="utf-8")
    checklist_text = CHECKLIST.read_text(encoding="utf-8")
    stop_text = f"{doc_text}\n{checklist_text}".lower()
    audit_text = AUDIT.read_text(encoding="utf-8")
    perek2_text = PEREK2_GATE1_REPORT.read_text(encoding="utf-8")
    perek2_compressed_text = PEREK2_COMPRESSED_REVIEW_PACKET.read_text(encoding="utf-8")
    perek2_clean_text = PEREK2_CLEAN_GROUP_REVIEW_PACKET.read_text(encoding="utf-8")
    perek2_clean_applied_text = PEREK2_CLEAN_GROUP_APPLIED_REPORT.read_text(encoding="utf-8")
    perek2_decision_status_text = PEREK2_GATE1_ENRICHMENT_DECISION_STATUS.read_text(encoding="utf-8")
    perek2_pool_summary_text = PEREK2_GATE2_CANDIDATE_POOL_SUMMARY.read_text(encoding="utf-8")
    prompt_texts = [path.read_text(encoding="utf-8") for path in PROMPTS]

    for phrase in ("Stop conditions", "unverified source-to-skill", "Hebrew corruption", "batch balance table"):
        if phrase.lower() not in stop_text:
            errors.append(f"stop-condition language missing: {phrase}")
    for phrase in ("Round 1 gate inventory", "Validators", "Review decision fields", "Manual review"):
        if phrase not in audit_text:
            errors.append(f"audit missing required section/phrase: {phrase}")
    for phrase in (
        "Bereishis Perek 2 Gate 1",
        "Source-to-skill readiness",
        "Enrichment candidate counts",
        "Question-eligibility decisions and approved input-candidate planning are not ready",
    ):
        if phrase not in perek2_text:
            errors.append(f"Perek 2 Gate 1 report missing required phrase: {phrase}")
    for phrase in (
        "Bereishis Perek 2 Enrichment Compressed Yossi Review Packet",
        "raw candidate count: 1083",
        "no safety gates opened",
        "This is enrichment review only.",
    ):
        if phrase not in perek2_compressed_text:
            errors.append(f"Perek 2 compressed review packet missing required phrase: {phrase}")
    for phrase in (
        "Bereishis Perek 2 Clean-Group Yossi Review Packet",
        "groups reviewed: 69",
        "raw candidates covered: 191",
        "This is enrichment review only",
    ):
        if phrase not in perek2_clean_text:
            errors.append(f"Perek 2 clean-group review packet missing required phrase: {phrase}")
    for phrase in (
        "Bereishis Perek 2 Clean-Group Yossi Review Applied",
        "verified groups: 31",
        "verified raw candidates: 91",
        "needs_follow_up groups: 38",
        "needs_follow_up raw candidates: 100",
    ):
        if phrase not in perek2_clean_applied_text:
            errors.append(f"Perek 2 clean-group applied report missing required phrase: {phrase}")
    for phrase in (
        "Bereishis Perek 2 Gate 1 Enrichment-Decision Status Report",
        "verified enrichment subset",
        "Gate 2 has not started",
        "31 token-split clean noun standards groups",
        "91 raw token-split standards candidates",
        "38 clean vocabulary/noun and clean shoresh groups",
        "100 raw vocabulary/shoresh candidates",
        "only the 91 verified token-split clean noun standards raw candidates",
        "no follow-up groups",
        "no morphology",
        "no verb forms",
        "no prefix/preposition",
        "no direct-object-marker",
        "no shoresh",
        "no phrase-level standards",
    ):
        if phrase not in perek2_decision_status_text:
            errors.append(f"Perek 2 enrichment-decision status report missing required phrase: {phrase}")
    for phrase in (
        "Bereishis Perek 2 Gate 2 Candidate-Pool Summary",
        "This is not a Gate 2 batch selection",
        "Available pool size: 91 verified raw candidates",
        "Verified group count: 31 token-split clean noun standards groups",
        "Candidate Source Files",
        "Count by Token/Group",
        "Count by Pasuk",
        "No input-candidate batch TSV was created",
    ):
        if phrase not in perek2_pool_summary_text:
            errors.append(f"Perek 2 Gate 2 candidate-pool summary missing required phrase: {phrase}")

    if contract.get("status") != "planning_contract_only":
        errors.append("contract status must be planning_contract_only")
    gate_ids = {gate.get("gate_id") for gate in contract.get("gate_definitions", []) if isinstance(gate, dict)}
    if gate_ids != REQUIRED_GATES:
        errors.append(f"contract gates mismatch: {sorted(gate_ids)}")
    if "basic_verb_form_recognition" not in contract.get("deferred_families", []):
        errors.append("verb-form family must remain deferred")
    safety = contract.get("safety_gate_defaults", {})
    for field in CLOSED_GATE_FIELDS:
        if safety.get(field) is not False:
            errors.append(f"contract safety default must keep {field}=false")
    for gate in REQUIRED_GATES:
        if gate not in contract.get("required_artifacts_by_gate", {}):
            errors.append(f"contract missing required artifacts for {gate}")
        if gate not in contract.get("required_validators_by_gate", {}):
            errors.append(f"contract missing required validators for {gate}")
    if len(contract.get("stop_conditions", [])) < 7:
        errors.append("contract must include stop conditions")

    for path, text in zip(PROMPTS, prompt_texts):
        for placeholder in PROMPT_PLACEHOLDERS:
            if placeholder not in text:
                errors.append(f"{rel(path)} missing placeholder {placeholder}")
        for phrase in ("reviewed-bank", "runtime", "student-facing", "Validators/tests to run", "validate_", "pytest"):
            if phrase not in text:
                errors.append(f"{rel(path)} missing required prompt phrase: {phrase}")

    return {
        "valid": not errors,
        "errors": errors,
        "contract_path": rel(CONTRACT),
        "gate_count": len(gate_ids),
        "prompt_count": len(PROMPTS),
        "perek2_gate1_report_path": rel(PEREK2_GATE1_REPORT),
        "perek2_compressed_review_packet_path": rel(PEREK2_COMPRESSED_REVIEW_PACKET),
        "perek2_clean_group_review_packet_path": rel(PEREK2_CLEAN_GROUP_REVIEW_PACKET),
        "perek2_clean_group_applied_report_path": rel(PEREK2_CLEAN_GROUP_APPLIED_REPORT),
        "perek2_gate1_enrichment_decision_status_path": rel(PEREK2_GATE1_ENRICHMENT_DECISION_STATUS),
        "perek2_gate2_candidate_pool_summary_path": rel(PEREK2_GATE2_CANDIDATE_POOL_SUMMARY),
    }


def main() -> int:
    summary = validate_pipeline_rounds()
    if summary["valid"]:
        print("Pipeline rounds validation passed.")
        print(f"Contract: {summary['contract_path']}")
        print(f"Gate count: {summary['gate_count']}")
        print(f"Prompt count: {summary['prompt_count']}")
        return 0
    print("Pipeline rounds validation failed:")
    for error in summary["errors"]:
        print(f"- {error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
