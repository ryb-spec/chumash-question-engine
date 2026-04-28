from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT_DIR = ROOT / "data" / "question_eligibility_audits"
README_PATH = AUDIT_DIR / "README.md"
DOC_README_PATH = ROOT / "docs" / "question_templates" / "README.md"
DOC_POLICY_PATH = ROOT / "docs" / "question_templates" / "perek_1_protected_preview_input_list_planning_policy.md"
JSON_POLICY_PATH = AUDIT_DIR / "protected_preview_input_list_planning_policy.v1.json"
REPORT_PATH = AUDIT_DIR / "reports" / "perek_1_protected_preview_input_list_planning_policy_report.md"
YOSSI_PACKET_PATH = AUDIT_DIR / "reports" / "perek_1_protected_preview_input_list_planning_policy_yossi_review_packet.md"
APPLIED_REPORT_PATH = AUDIT_DIR / "reports" / "perek_1_protected_preview_input_list_planning_policy_yossi_review_applied.md"

ALLOWED_FAMILIES = {
    "vocabulary_meaning",
    "basic_noun_recognition",
    "direct_object_marker_recognition",
    "shoresh_identification",
}
DEFERRED_FAMILIES = {"basic_verb_form_recognition"}
REQUIRED_FUTURE_FIELDS = {
    "input_candidate_id",
    "audit_id",
    "ref",
    "hebrew_token",
    "hebrew_phrase",
    "approved_family",
    "canonical_skill_id",
    "canonical_standard_anchor",
    "source_candidate_type",
    "risk_level",
    "risk_reasons",
    "required_template_family",
    "wording_policy_version",
    "teacher_wording_review_status",
    "answer_key_review_status",
    "distractor_review_status",
    "context_display_review_status",
    "protected_preview_candidate_status",
    "protected_preview_allowed",
    "reviewed_bank_allowed",
    "runtime_allowed",
    "student_facing_allowed",
    "notes",
}
REQUIRED_BATCH_BALANCE_FIELDS = {
    "total_selected_input_candidates",
    "count_by_family",
    "count_by_risk_level",
    "count_by_perek_pasuk_range",
    "duplicate_hebrew_tokens",
    "direct_object_marker_inclusion_reasons",
    "shoresh_inclusion_reasons",
}
FORBIDDEN_PHRASES = {
    "question_ready",
    "protected_preview_ready",
    "reviewed_bank_ready",
    "runtime_ready",
    "student_facing",
    "approved_for_questions",
    "approved_for_preview",
}


def repo_relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{repo_relative(path)} must contain a JSON object")
    return payload


def contains_forbidden_phrase(text: str, phrase: str) -> bool:
    for line in text.lower().splitlines():
        if phrase not in line:
            continue
        if (
            "forbidden" in line
            or "not " in line
            or "no " in line
            or "nothing marked " in line
            or "must not" in line
            or "remain false" in line
            or "= false" in line
            or "_allowed" in line
            or "_content" in line
        ):
            continue
        return True
    return False


def validate_protected_preview_input_list_planning_policy() -> dict[str, object]:
    errors: list[str] = []
    required_paths = (
        README_PATH,
        DOC_README_PATH,
        DOC_POLICY_PATH,
        JSON_POLICY_PATH,
        REPORT_PATH,
        YOSSI_PACKET_PATH,
        APPLIED_REPORT_PATH,
    )
    for path in required_paths:
        if not path.exists():
            errors.append(f"required protected-preview planning-policy artifact missing: {repo_relative(path)}")

    if errors:
        return {"valid": False, "errors": errors}

    try:
        policy = load_json(JSON_POLICY_PATH)
    except (json.JSONDecodeError, ValueError) as error:
        return {"valid": False, "errors": [str(error)]}

    if policy.get("status") != "planning_policy_only":
        errors.append(f"{repo_relative(JSON_POLICY_PATH)} status must be planning_policy_only")
    if policy.get("planning_policy_review_status") != "yossi_approved_with_revision":
        errors.append(f"{repo_relative(JSON_POLICY_PATH)} planning_policy_review_status must be yossi_approved_with_revision")
    if policy.get("review_decision") != "approve_with_revision":
        errors.append(f"{repo_relative(JSON_POLICY_PATH)} review_decision must be approve_with_revision")
    if policy.get("future_input_list_planning_may_proceed") is not True:
        errors.append(f"{repo_relative(JSON_POLICY_PATH)} future_input_list_planning_may_proceed must be true")
    if policy.get("batch_balance_table_required") is not True:
        errors.append(f"{repo_relative(JSON_POLICY_PATH)} batch_balance_table_required must be true")
    missing_batch_fields = sorted(REQUIRED_BATCH_BALANCE_FIELDS - set(policy.get("batch_balance_required_fields", [])))
    if missing_batch_fields:
        errors.append(f"{repo_relative(JSON_POLICY_PATH)} missing batch_balance_required_fields: {missing_batch_fields}")
    review_notes = str(policy.get("review_notes", ""))
    for phrase in (
        "total selected input candidates",
        "count by family",
        "count by risk level",
        "count by perek/pasuk range",
        "duplicate Hebrew tokens",
        "direct-object-marker",
        "shoresh",
    ):
        if phrase not in review_notes:
            errors.append(f"{repo_relative(JSON_POLICY_PATH)} review_notes missing batch-balance phrase: {phrase!r}")
    if set(policy.get("allowed_families", [])) != ALLOWED_FAMILIES:
        errors.append(f"{repo_relative(JSON_POLICY_PATH)} allowed_families must exactly match {sorted(ALLOWED_FAMILIES)}")
    if not DEFERRED_FAMILIES.issubset(set(policy.get("deferred_families", []))):
        errors.append(f"{repo_relative(JSON_POLICY_PATH)} deferred_families must include basic_verb_form_recognition")
    if not DEFERRED_FAMILIES.issubset(set(policy.get("excluded_families", []))):
        errors.append(f"{repo_relative(JSON_POLICY_PATH)} excluded_families must include basic_verb_form_recognition")

    missing_fields = sorted(REQUIRED_FUTURE_FIELDS - set(policy.get("required_future_input_fields", [])))
    if missing_fields:
        errors.append(f"{repo_relative(JSON_POLICY_PATH)} missing required_future_input_fields: {missing_fields}")

    defaults = policy.get("default_future_input_statuses", {})
    for field in (
        "teacher_wording_review_status",
        "answer_key_review_status",
        "distractor_review_status",
        "context_display_review_status",
    ):
        if defaults.get(field) != "needs_review":
            errors.append(f"default_future_input_statuses.{field} must be needs_review")
    if defaults.get("protected_preview_candidate_status") != "planning_only":
        errors.append("default_future_input_statuses.protected_preview_candidate_status must be planning_only")
    for gate in ("protected_preview_allowed", "reviewed_bank_allowed", "runtime_allowed", "student_facing_allowed"):
        if defaults.get(gate) is not False:
            errors.append(f"default_future_input_statuses.{gate} must remain false")

    safety_defaults = policy.get("safety_gate_defaults", {})
    for gate in ("protected_preview_allowed", "reviewed_bank_allowed", "runtime_allowed", "student_facing_allowed"):
        if safety_defaults.get(gate) is not False:
            errors.append(f"safety_gate_defaults.{gate} must remain false")

    if policy.get("actual_input_rows") not in ([], None):
        errors.append(f"{repo_relative(JSON_POLICY_PATH)} must not contain actual input rows")

    first_batch = policy.get("first_batch_balance_rules", {})
    for key in (
        "total_suggested_size",
        "prioritize_risk_level",
        "prioritize_families",
        "small_sample_families",
        "exclude_families",
    ):
        if key not in first_batch:
            errors.append(f"first_batch_balance_rules missing {key}")
    if first_batch.get("total_suggested_size") != "20-30":
        errors.append("first_batch_balance_rules.total_suggested_size must be 20-30")
    if "basic_verb_form_recognition" not in first_batch.get("exclude_families", []):
        errors.append("first_batch_balance_rules.exclude_families must include basic_verb_form_recognition")

    family_constraints = policy.get("family_constraints", {})
    et_constraints = " ".join(family_constraints.get("direct_object_marker_recognition", []))
    if "function, not translation" not in et_constraints:
        errors.append("direct_object_marker_recognition constraints must require function wording")
    if "basic_verb_form_recognition" not in family_constraints:
        errors.append("family_constraints must include deferred basic_verb_form_recognition")

    forbidden_outputs = set(policy.get("forbidden_outputs", []))
    for output in (
        "actual_questions",
        "answer_choices",
        "answer_keys",
        "protected_preview_input_rows",
        "protected_preview_generation",
        "reviewed_bank_entries",
        "runtime_data",
        "student_facing_content",
    ):
        if output not in forbidden_outputs:
            errors.append(f"forbidden_outputs missing {output}")

    list_files = [
        path
        for path in AUDIT_DIR.rglob("*")
        if path.is_file()
        and "planning_policy" not in path.name
        and "yossi_review_packet" not in path.name
        and "policy_report" not in path.name
        and "protected_preview_input_list" in path.name
        and path.suffix.lower() in {".tsv", ".csv", ".json", ".jsonl"}
    ]
    if list_files:
        errors.append(f"protected-preview input list files must not exist: {[repo_relative(path) for path in list_files]}")

    doc_text = DOC_POLICY_PATH.read_text(encoding="utf-8")
    for phrase in (
        "planning policy only",
        "does not create a protected-preview input list",
        "does not generate questions",
        "does not generate answer choices",
        "does not generate answer keys",
        "No input list rows allowed yet.",
        "Must ask function, not translation.",
        "Decision: `approve_with_revision`.",
        "Future input-list planning may proceed",
        "batch balance table",
        "Verb-form rows remain deferred.",
    ):
        if phrase not in doc_text:
            errors.append(f"{repo_relative(DOC_POLICY_PATH)} missing required phrase: {phrase!r}")

    report_text = REPORT_PATH.read_text(encoding="utf-8")
    for phrase in (
        "approved input candidates: 133",
        "`vocabulary_meaning`: 56",
        "`basic_noun_recognition`: 60",
        "`direct_object_marker_recognition`: 14",
        "`shoresh_identification`: 3",
        "`basic_verb_form_recognition`: 25 deferred rows",
        "no questions generated",
        "no answer choices generated",
        "no answer keys generated",
        "no protected-preview input list created",
        "no runtime changes made",
    ):
        if phrase not in report_text:
            errors.append(f"{repo_relative(REPORT_PATH)} missing required phrase: {phrase!r}")

    packet_text = YOSSI_PACKET_PATH.read_text(encoding="utf-8")
    for phrase in (
        "This packet does not create a protected-preview input list",
        "approve_planning_policy",
        "approve_with_revision",
        "needs_follow_up",
        "block_for_now",
        "All verb-form rows remain deferred.",
        "Recorded decision: `approve_with_revision`",
        "batch balance table",
        "All gates remain closed.",
    ):
        if phrase not in packet_text:
            errors.append(f"{repo_relative(YOSSI_PACKET_PATH)} missing required phrase: {phrase!r}")

    applied_text = APPLIED_REPORT_PATH.read_text(encoding="utf-8")
    for phrase in (
        "`approve_with_revision`",
        "The planning policy may proceed to a future input-list planning task",
        "batch balance table",
        "first batch size: 20-30",
        "direct-object-marker cap preserved",
        "shoresh cap preserved at 1-3 rows",
        "verb-form deferred",
        "no input list created",
        "no questions generated",
        "no answer choices generated",
        "no answer keys generated",
        "no protected-preview content created",
        "no reviewed-bank entries created",
        "no runtime changes made",
        "no student-facing use approved",
    ):
        if phrase not in applied_text:
            errors.append(f"{repo_relative(APPLIED_REPORT_PATH)} missing required phrase: {phrase!r}")

    readme_text = README_PATH.read_text(encoding="utf-8")
    for relative in (
        "docs/question_templates/perek_1_protected_preview_input_list_planning_policy.md",
        "protected_preview_input_list_planning_policy.v1.json",
        "reports/perek_1_protected_preview_input_list_planning_policy_report.md",
        "reports/perek_1_protected_preview_input_list_planning_policy_yossi_review_packet.md",
        "reports/perek_1_protected_preview_input_list_planning_policy_yossi_review_applied.md",
    ):
        if relative not in readme_text:
            errors.append(f"{repo_relative(README_PATH)} missing link/reference to {relative}")
    for phrase in (
        "no input list was created",
        "no questions were generated",
        "protected preview remains a later gate",
        "Yossi reviews planning policy",
        "Decision: `approve_with_revision`",
        "Future input-list planning may proceed",
    ):
        if phrase not in readme_text:
            errors.append(f"{repo_relative(README_PATH)} missing metadata phrase: {phrase!r}")

    docs_readme = DOC_README_PATH.read_text(encoding="utf-8")
    if "perek_1_protected_preview_input_list_planning_policy.md" not in docs_readme:
        errors.append(f"{repo_relative(DOC_README_PATH)} missing planning policy link")

    serialized_policy = json.dumps(policy, ensure_ascii=False)
    for path, text in (
        (DOC_POLICY_PATH, doc_text),
        (REPORT_PATH, report_text),
        (YOSSI_PACKET_PATH, packet_text),
        (APPLIED_REPORT_PATH, applied_text),
        (JSON_POLICY_PATH, serialized_policy),
    ):
        for phrase in FORBIDDEN_PHRASES:
            if contains_forbidden_phrase(text, phrase):
                errors.append(f"{repo_relative(path)} contains forbidden unnegated phrase: {phrase}")

    return {
        "valid": not errors,
        "policy_markdown_path": repo_relative(DOC_POLICY_PATH),
        "policy_json_path": repo_relative(JSON_POLICY_PATH),
        "report_path": repo_relative(REPORT_PATH),
        "yossi_packet_path": repo_relative(YOSSI_PACKET_PATH),
        "applied_report_path": repo_relative(APPLIED_REPORT_PATH),
        "allowed_families": sorted(policy.get("allowed_families", [])),
        "deferred_families": sorted(policy.get("deferred_families", [])),
        "required_future_input_field_count": len(policy.get("required_future_input_fields", [])),
        "batch_balance_required_field_count": len(policy.get("batch_balance_required_fields", [])),
        "actual_input_row_count": len(policy.get("actual_input_rows", [])),
        "errors": errors,
    }


def main() -> int:
    summary = validate_protected_preview_input_list_planning_policy()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
