from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "pipeline_rounds" / "round_2_fast_track_pipeline.md"
CONTRACT = ROOT / "data" / "pipeline_rounds" / "round_2_fast_track_pipeline_contract.v1.json"
CHECKLIST = ROOT / "data" / "pipeline_rounds" / "reports" / "round_2_starter_checklist.md"
AUDIT = ROOT / "data" / "pipeline_rounds" / "reports" / "perek_1_round_1_pipeline_audit.md"
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
    for path in (DOC, CHECKLIST, AUDIT, *PROMPTS):
        if not path.exists():
            errors.append(f"missing artifact: {rel(path)}")
    contract = load_contract(errors)
    if errors:
        return {"valid": False, "errors": errors}

    doc_text = DOC.read_text(encoding="utf-8")
    checklist_text = CHECKLIST.read_text(encoding="utf-8")
    stop_text = f"{doc_text}\n{checklist_text}".lower()
    audit_text = AUDIT.read_text(encoding="utf-8")
    prompt_texts = [path.read_text(encoding="utf-8") for path in PROMPTS]

    for phrase in ("Stop conditions", "unverified source-to-skill", "Hebrew corruption", "batch balance table"):
        if phrase.lower() not in stop_text:
            errors.append(f"stop-condition language missing: {phrase}")
    for phrase in ("Round 1 gate inventory", "Validators", "Review decision fields", "Manual review"):
        if phrase not in audit_text:
            errors.append(f"audit missing required section/phrase: {phrase}")

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
