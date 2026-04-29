
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_DIR = ROOT / "data" / "template_skeleton_planning"
REPORTS_DIR = BASE_DIR / "reports"
DOCS_DIR = ROOT / "docs" / "question_templates"
README_PATH = BASE_DIR / "README.md"
SKELETON_DOC_POLICY_PATH = DOCS_DIR / "perek_1_first_batch_template_skeleton_policy.md"
SKELETON_JSON_POLICY_PATH = BASE_DIR / "template_skeleton_policy.v1.json"
SKELETON_TSV_PATH = BASE_DIR / "bereishis_perek_1_first_batch_template_skeleton_planning.tsv"
SKELETON_PACKET_PATH = REPORTS_DIR / "bereishis_perek_1_first_batch_template_skeleton_yossi_review_packet.md"
SKELETON_REPORT_PATH = REPORTS_DIR / "bereishis_perek_1_first_batch_template_skeleton_planning_report.md"
SKELETON_APPLIED_PATH = REPORTS_DIR / "bereishis_perek_1_first_batch_template_skeleton_yossi_review_applied.md"
EXACT_DOC_POLICY_PATH = DOCS_DIR / "perek_1_first_batch_exact_template_wording_policy.md"
EXACT_JSON_POLICY_PATH = BASE_DIR / "exact_template_wording_policy.v1.json"
EXACT_TSV_PATH = BASE_DIR / "bereishis_perek_1_first_batch_exact_template_wording_planning.tsv"
EXACT_PACKET_PATH = REPORTS_DIR / "bereishis_perek_1_first_batch_exact_template_wording_yossi_review_packet.md"
EXACT_REPORT_PATH = REPORTS_DIR / "bereishis_perek_1_first_batch_exact_template_wording_planning_report.md"
EXACT_APPLIED_PATH = REPORTS_DIR / "bereishis_perek_1_first_batch_exact_template_wording_yossi_review_applied.md"
ANSWER_DOC_PATH = DOCS_DIR / "perek_1_first_batch_answer_key_planning_policy.md"
ANSWER_JSON_PATH = BASE_DIR / "answer_key_planning_policy.v1.json"
DISTRACTOR_DOC_PATH = DOCS_DIR / "perek_1_first_batch_distractor_planning_policy.md"
DISTRACTOR_JSON_PATH = BASE_DIR / "distractor_planning_policy.v1.json"
CONTEXT_DOC_PATH = DOCS_DIR / "perek_1_first_batch_context_display_hebrew_policy.md"
CONTEXT_JSON_PATH = BASE_DIR / "context_display_hebrew_policy.v1.json"
READINESS_REPORT_PATH = REPORTS_DIR / "bereishis_perek_1_first_batch_pre_generation_readiness_report.md"
POLICY_PACKET_PATH = REPORTS_DIR / "bereishis_perek_1_first_batch_answer_distractor_context_policy_yossi_review_packet.md"
POLICY_APPLIED_PATH = REPORTS_DIR / "bereishis_perek_1_first_batch_answer_distractor_context_policy_yossi_review_applied.md"
INPUT_PLANNING_TSV_PATH = ROOT / "data" / "protected_preview_input_planning" / "bereishis_perek_1_first_input_candidate_planning.tsv"

ALLOWED_FAMILIES = {"vocabulary_meaning", "basic_noun_recognition", "direct_object_marker_recognition", "shoresh_identification"}
DEFERRED_FAMILIES = {"basic_verb_form_recognition"}
REVIEW_STATUS_FIELDS = {"teacher_wording_review_status", "answer_key_review_status", "distractor_review_status", "context_display_review_status", "hebrew_rendering_review_status", "protected_preview_gate_review_status"}
SAFETY_FIELDS = {"final_question_allowed", "answer_choices_allowed", "answer_key_allowed", "protected_preview_allowed", "reviewed_bank_allowed", "runtime_allowed", "student_facing_allowed"}
POLICY_SAFETY_FIELDS = SAFETY_FIELDS | {"distractors_allowed"}
ROW_LEVEL_REVIEW_FIELDS = {
    "exact_wording_review_status",
    "answer_key_language_review_status",
    "distractor_constraints_review_status",
    "context_display_review_status",
    "hebrew_rendering_review_status",
    "protected_preview_gate_review_status",
}
FORBIDDEN_CONTENT_COLUMNS = {"question_text", "prompt", "prompt_text", "student_prompt", "answer_choices", "answer_key", "correct_answer", "distractors"}
FORBIDDEN_PHRASES = {"question_ready", "protected_preview_ready", "reviewed_bank_ready", "runtime_ready", "student_facing", "approved_for_questions", "approved_for_preview"}
ET = "\u05d0\u05ea"
HIBDIL = "\u05d4\u05d1\u05d3\u05d9\u05dc"
BDL = "\u05d1\u05d3\u05dc"
HAMAYIM = "\u05d4\u05de\u05d9\u05dd"
HAADAMAH = "\u05d4\u05d0\u05d3\u05de\u05d4"
HAARETZ = "\u05d4\u05d0\u05e8\u05e5"
EXPECTED_SKELETON_STATUSES = {
    "vocabulary_meaning": "yossi_skeleton_family_approved",
    "basic_noun_recognition": "yossi_approved_with_revision",
    "direct_object_marker_recognition": "yossi_approved_with_revision",
    "shoresh_identification": "yossi_approved_with_revision",
}
EXPECTED_EXACT_STATUSES = {
    "vocabulary_meaning": "yossi_exact_wording_family_approved",
    "basic_noun_recognition": "yossi_approved_with_revision",
    "direct_object_marker_recognition": "yossi_approved_with_revision",
    "shoresh_identification": "yossi_approved_with_revision",
}
SKELETON_REQUIRED_COLUMNS = {
    "skeleton_candidate_id", "input_candidate_id", "audit_id", "ref", "hebrew_token", "hebrew_phrase", "approved_family", "skeleton_family", "skeleton_policy_version", "non_student_facing_skeleton_label", "required_variables", "forbidden_outputs", "teacher_wording_review_status", "answer_key_review_status", "distractor_review_status", "context_display_review_status", "hebrew_rendering_review_status", "protected_preview_gate_review_status", "template_skeleton_status", "final_question_allowed", "answer_choices_allowed", "answer_key_allowed", "protected_preview_allowed", "reviewed_bank_allowed", "runtime_allowed", "student_facing_allowed", "cautions", "notes"
}
EXACT_REQUIRED_COLUMNS = {
    "exact_template_candidate_id", "skeleton_candidate_id", "input_candidate_id", "audit_id", "ref", "hebrew_token", "hebrew_phrase", "approved_family", "exact_template_family", "exact_wording_policy_version", "non_student_facing_wording_pattern", "required_placeholders", "forbidden_outputs", "teacher_wording_review_status", "answer_key_review_status", "distractor_review_status", "context_display_review_status", "hebrew_rendering_review_status", "protected_preview_gate_review_status", "exact_template_status", "final_question_allowed", "answer_choices_allowed", "answer_key_allowed", "protected_preview_allowed", "reviewed_bank_allowed", "runtime_allowed", "student_facing_allowed", "cautions", "notes"
}


def repo_relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return reader.fieldnames or [], list(reader)


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
        if any(marker in line for marker in ("forbidden", "not ", "no ", "nothing marked ", "does not", "must not", "remain false", "all gates remain closed", "= false", "_allowed", "_content")):
            continue
        return True
    return False


def validate_policy_gates(errors: list[str], label: str, payload: dict, gate_names: set[str] = SAFETY_FIELDS) -> None:
    for gate in gate_names:
        if gate in payload and payload.get(gate) is not False:
            errors.append(f"{label} {gate} must remain false")


def validate_template_skeleton_planning() -> dict[str, object]:
    errors: list[str] = []
    required_paths = (
        README_PATH, SKELETON_DOC_POLICY_PATH, SKELETON_JSON_POLICY_PATH, SKELETON_TSV_PATH, SKELETON_PACKET_PATH, SKELETON_REPORT_PATH, SKELETON_APPLIED_PATH,
        EXACT_DOC_POLICY_PATH, EXACT_JSON_POLICY_PATH, EXACT_TSV_PATH, EXACT_PACKET_PATH, EXACT_REPORT_PATH, EXACT_APPLIED_PATH,
        ANSWER_DOC_PATH, ANSWER_JSON_PATH, DISTRACTOR_DOC_PATH, DISTRACTOR_JSON_PATH, CONTEXT_DOC_PATH, CONTEXT_JSON_PATH, READINESS_REPORT_PATH, POLICY_PACKET_PATH, POLICY_APPLIED_PATH,
        INPUT_PLANNING_TSV_PATH,
    )
    for path in required_paths:
        if not path.exists():
            errors.append(f"required template planning artifact missing: {repo_relative(path)}")
    if errors:
        return {"valid": False, "errors": errors}

    try:
        skeleton_policy = load_json(SKELETON_JSON_POLICY_PATH)
        exact_policy = load_json(EXACT_JSON_POLICY_PATH)
        answer_policy = load_json(ANSWER_JSON_PATH)
        distractor_policy = load_json(DISTRACTOR_JSON_PATH)
        context_policy = load_json(CONTEXT_JSON_PATH)
    except (json.JSONDecodeError, ValueError) as error:
        return {"valid": False, "errors": [str(error)]}

    if skeleton_policy.get("status") != "skeleton_policy_only":
        errors.append("template skeleton JSON status must be skeleton_policy_only")
    if exact_policy.get("status") != "exact_wording_policy_only":
        errors.append("exact wording JSON status must be exact_wording_policy_only")
    if answer_policy.get("status") != "answer_key_policy_only":
        errors.append("answer-key JSON status must be answer_key_policy_only")
    if distractor_policy.get("status") != "distractor_policy_only":
        errors.append("distractor JSON status must be distractor_policy_only")
    if context_policy.get("status") != "context_display_hebrew_policy_only":
        errors.append("context/Hebrew JSON status must be context_display_hebrew_policy_only")
    if answer_policy.get("answer_key_planning_policy_review_status") != "yossi_approved_with_revision":
        errors.append("answer-key policy review status must be yossi_approved_with_revision")
    if distractor_policy.get("distractor_planning_policy_review_status") != "yossi_approved_with_revision":
        errors.append("distractor policy review status must be yossi_approved_with_revision")
    if context_policy.get("context_display_hebrew_policy_review_status") != "yossi_policy_approved":
        errors.append("context/Hebrew policy review status must be yossi_policy_approved")
    for label, policy in (("answer-key", answer_policy), ("distractor", distractor_policy), ("context/Hebrew", context_policy)):
        if policy.get("row_level_review_required_before_generation") is not True:
            errors.append(f"{label} policy must require row-level review before generation")
        if not ROW_LEVEL_REVIEW_FIELDS.issubset(set(policy.get("required_row_level_review_fields", []))):
            errors.append(f"{label} policy missing required row-level review fields")

    for label, policy in (("skeleton", skeleton_policy), ("exact", exact_policy), ("answer", answer_policy), ("distractor", distractor_policy), ("context", context_policy)):
        if set(policy.get("allowed_families", [])) - ALLOWED_FAMILIES:
            errors.append(f"{label} policy has disallowed families")
        if not DEFERRED_FAMILIES.issubset(set(policy.get("deferred_families", []))):
            errors.append(f"{label} policy must defer basic_verb_form_recognition")

    for family, expected in EXPECTED_SKELETON_STATUSES.items():
        rule = skeleton_policy.get("family_skeleton_rules", {}).get(family, {})
        if rule.get("family_skeleton_review_status") != expected:
            errors.append(f"{family} skeleton review status must be {expected}")
        validate_policy_gates(errors, f"{family} skeleton", rule)
    if skeleton_policy.get("basic_verb_form_recognition", {}).get("family_skeleton_review_status") != "deferred":
        errors.append("basic_verb_form_recognition skeleton status must be deferred")

    for family, expected in EXPECTED_EXACT_STATUSES.items():
        rule = exact_policy.get("family_wording_patterns", {}).get(family, {})
        if rule.get("exact_wording_review_status") != expected:
            errors.append(f"{family} exact wording review status must be {expected}")
        validate_policy_gates(errors, f"{family} exact", rule)
    if exact_policy.get("basic_verb_form_recognition", {}).get("exact_wording_review_status") != "deferred":
        errors.append("basic_verb_form_recognition exact wording status must be deferred")

    if answer_policy.get("individual_row_answer_keys") not in ([], None):
        errors.append("answer-key policy must not include individual row answer keys")
    for gate in POLICY_SAFETY_FIELDS:
        if answer_policy.get(gate) is not False:
            errors.append(f"answer-key policy {gate} must remain false")
    if distractor_policy.get("individual_distractors") not in ([], None):
        errors.append("distractor policy must not include individual distractors")
    for gate in POLICY_SAFETY_FIELDS:
        if distractor_policy.get(gate) is not False:
            errors.append(f"distractor policy {gate} must remain false")
    for payload_name in ("rendered_student_items", "protected_preview_content", "runtime_content", "student_facing_content"):
        if context_policy.get(payload_name) not in ([], None):
            errors.append(f"context/Hebrew policy must not include {payload_name}")
    for gate in POLICY_SAFETY_FIELDS:
        if context_policy.get(gate) is not False:
            errors.append(f"context/Hebrew policy {gate} must remain false")

    skeleton_fields, skeleton_rows = read_tsv(SKELETON_TSV_PATH)
    exact_fields, exact_rows = read_tsv(EXACT_TSV_PATH)
    if len(skeleton_rows) != 24:
        errors.append(f"skeleton TSV must contain exactly 24 rows; found {len(skeleton_rows)}")
    if len(exact_rows) != 24:
        errors.append(f"exact wording TSV must contain exactly 24 rows; found {len(exact_rows)}")
    missing_skeleton = sorted(SKELETON_REQUIRED_COLUMNS - set(skeleton_fields))
    missing_exact = sorted(EXACT_REQUIRED_COLUMNS - set(exact_fields))
    if missing_skeleton:
        errors.append(f"skeleton TSV missing columns: {missing_skeleton}")
    if missing_exact:
        errors.append(f"exact TSV missing columns: {missing_exact}")
    if FORBIDDEN_CONTENT_COLUMNS & set(skeleton_fields):
        errors.append("skeleton TSV must not include question/prompt/answer/distractor content columns")
    if FORBIDDEN_CONTENT_COLUMNS & set(exact_fields):
        errors.append("exact TSV must not include question/prompt/answer/distractor content columns")

    skeleton_by_id = {row["skeleton_candidate_id"]: row for row in skeleton_rows}
    family_counts: Counter[str] = Counter()
    exact_family_counts: Counter[str] = Counter()
    for row in skeleton_rows:
        row_id = row.get("skeleton_candidate_id", "unknown")
        family = row.get("approved_family", "")
        family_counts[family] += 1
        if family not in ALLOWED_FAMILIES:
            errors.append(f"{row_id} uses disallowed skeleton family {family}")
        for field in REVIEW_STATUS_FIELDS:
            if row.get(field) != "needs_review":
                errors.append(f"{row_id} {field} must be needs_review")
        if row.get("template_skeleton_status") != "planning_only":
            errors.append(f"{row_id} template_skeleton_status must be planning_only")
        for gate in SAFETY_FIELDS:
            if row.get(gate) != "false":
                errors.append(f"{row_id} {gate} must remain false")
    for row in exact_rows:
        row_id = row.get("exact_template_candidate_id", "unknown")
        family = row.get("approved_family", "")
        exact_family_counts[family] += 1
        if row.get("skeleton_candidate_id") not in skeleton_by_id:
            errors.append(f"{row_id} links to missing skeleton row")
        if family not in ALLOWED_FAMILIES:
            errors.append(f"{row_id} uses disallowed exact family {family}")
        if family == "basic_verb_form_recognition":
            errors.append(f"{row_id} must not include verb-form rows")
        for field in REVIEW_STATUS_FIELDS:
            if row.get(field) != "needs_review":
                errors.append(f"{row_id} {field} must be needs_review")
        if row.get("exact_template_status") != "planning_only":
            errors.append(f"{row_id} exact_template_status must be planning_only")
        for gate in SAFETY_FIELDS:
            if row.get(gate) != "false":
                errors.append(f"{row_id} {gate} must remain false")
        cautions = row.get("cautions", "")
        pattern = row.get("non_student_facing_wording_pattern", "")
        if family == "direct_object_marker_recognition" and (f"job of {ET}" not in pattern and "function" not in pattern.lower()):
            errors.append(f"{row_id} direct-object-marker pattern must be function-based")
        if family == "direct_object_marker_recognition" and f"do not ask What does {ET} mean" not in cautions:
            errors.append(f"{row_id} must preserve direct-object-marker caution")
        if row.get("input_candidate_id") == "ppplan_b1_024" and (HIBDIL not in cautions or BDL not in cautions):
            errors.append(f"{row_id} must preserve {HIBDIL} / {BDL} caution")
        if row.get("hebrew_token") in {HAMAYIM, HAADAMAH, HAARETZ} and "base meaning vs article-inclusive meaning" not in cautions:
            errors.append(f"{row_id} must preserve article/base-meaning caution")

    text_paths = (SKELETON_DOC_POLICY_PATH, EXACT_DOC_POLICY_PATH, ANSWER_DOC_PATH, DISTRACTOR_DOC_PATH, CONTEXT_DOC_PATH, SKELETON_PACKET_PATH, EXACT_PACKET_PATH, SKELETON_APPLIED_PATH, EXACT_APPLIED_PATH, READINESS_REPORT_PATH, POLICY_PACKET_PATH, POLICY_APPLIED_PATH)
    text_blob = "\n".join(path.read_text(encoding="utf-8") for path in text_paths)
    required_phrases = (
        "No verb-form skeletons may be approved",
        "approve_exact_wording_family",
        "Wording must stay simple: noun/object/person/place/thing",
        f"function of `{ET}`",
        f"target shoresh is `{BDL}`",
        "answer-key policy approved: approve_with_revision",
        "distractor policy approved: approve_with_revision",
        "context-display/Hebrew policy approved: approve_policy",
        "Pre-generation readiness checklist approved with revision",
        "Row-level exact wording review",
        "This packet does not generate questions",
        "No final questions generated.",
        "No answer choices generated.",
        "No answer keys generated.",
        "No protected-preview content created.",
    )
    text_blob_lower = text_blob.lower()
    for phrase in required_phrases:
        if phrase.lower() not in text_blob_lower:
            errors.append(f"required planning phrase missing: {phrase!r}")

    readme_text = README_PATH.read_text(encoding="utf-8")
    for path in (SKELETON_DOC_POLICY_PATH, SKELETON_JSON_POLICY_PATH, SKELETON_TSV_PATH, EXACT_DOC_POLICY_PATH, EXACT_JSON_POLICY_PATH, EXACT_TSV_PATH, EXACT_APPLIED_PATH, ANSWER_DOC_PATH, ANSWER_JSON_PATH, DISTRACTOR_DOC_PATH, DISTRACTOR_JSON_PATH, CONTEXT_DOC_PATH, CONTEXT_JSON_PATH, READINESS_REPORT_PATH, POLICY_PACKET_PATH, POLICY_APPLIED_PATH):
        if repo_relative(path) not in readme_text:
            errors.append(f"README must link {repo_relative(path)}")

    combined_text = readme_text + "\n" + text_blob
    for phrase in FORBIDDEN_PHRASES:
        if contains_forbidden_phrase(combined_text, phrase):
            errors.append(f"forbidden approval phrase appears without clear negation: {phrase}")

    return {
        "valid": not errors,
        "errors": errors,
        "row_count": len(skeleton_rows),
        "family_counts": dict(family_counts),
        "exact_row_count": len(exact_rows),
        "exact_family_counts": dict(exact_family_counts),
    }


def main() -> int:
    summary = validate_template_skeleton_planning()
    if summary["valid"]:
        print("Template-skeleton planning validation passed.")
        print(f"Rows: {summary['row_count']}")
        print(f"Family counts: {summary['family_counts']}")
        print(f"Exact rows: {summary['exact_row_count']}")
        return 0
    print("Template-skeleton planning validation failed:")
    for error in summary["errors"]:
        print(f"- {error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
