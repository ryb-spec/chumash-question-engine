from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC_POLICY_PATH = ROOT / "docs" / "question_templates" / "perek_1_approved_input_candidate_wording_policy.md"
DOC_README_PATH = ROOT / "docs" / "question_templates" / "README.md"
AUDIT_DIR = ROOT / "data" / "question_eligibility_audits"
README_PATH = AUDIT_DIR / "README.md"
JSON_POLICY_PATH = AUDIT_DIR / "question_template_wording_policy.v1.json"
YOSSI_PACKET_PATH = AUDIT_DIR / "reports" / "perek_1_approved_input_candidate_wording_policy_yossi_review_packet.md"
POLICY_REPORT_PATH = AUDIT_DIR / "reports" / "perek_1_question_template_wording_policy_report.md"
APPLIED_REPORT_PATH = AUDIT_DIR / "reports" / "perek_1_approved_input_candidate_wording_policy_yossi_review_applied.md"

ALLOWED_FAMILIES = {
    "vocabulary_meaning",
    "basic_noun_recognition",
    "direct_object_marker_recognition",
    "shoresh_identification",
}
DEFERRED_FAMILIES = {"basic_verb_form_recognition"}
FORBIDDEN_PHRASES = {
    "question_ready",
    "protected_preview_ready",
    "reviewed_bank_ready",
    "runtime_ready",
    "student_facing",
    "approved_for_questions",
    "approved_for_preview",
}
FORBIDDEN_OUTPUT_TYPES = {
    "generated_question",
    "answer_choice_set",
    "answer_key",
    "protected_preview_input_row",
    "protected_preview_content",
    "reviewed_bank_entry",
    "runtime_payload",
    "student-facing item",
}
SAFETY_PHRASES = (
    "does not generate questions",
    "does not approve protected preview",
    "does not approve reviewed bank",
    "does not approve runtime",
    "does not approve student-facing use",
    "Every later generated item still needs separate review",
)


def repo_relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{repo_relative(path)} must contain a JSON object")
    return payload


def contains_forbidden_phrase(text: str, phrase: str) -> bool:
    lowered = text.lower()
    for match in re.finditer(re.escape(phrase), lowered):
        start = max(0, match.start() - 40)
        context = lowered[start : match.start()]
        if "forbidden" in context or "not " in context or "no " in context:
            continue
        return True
    return False


def validate_question_template_wording_policy() -> dict[str, object]:
    errors: list[str] = []
    required_paths = (
        DOC_POLICY_PATH,
        DOC_README_PATH,
        JSON_POLICY_PATH,
        YOSSI_PACKET_PATH,
        POLICY_REPORT_PATH,
        APPLIED_REPORT_PATH,
        README_PATH,
    )
    for path in required_paths:
        if not path.exists():
            errors.append(f"required wording-policy artifact missing: {repo_relative(path)}")

    if errors:
        return {"valid": False, "errors": errors}

    try:
        policy = load_json(JSON_POLICY_PATH)
    except (json.JSONDecodeError, ValueError) as error:
        return {"valid": False, "errors": [str(error)]}

    allowed = set(policy.get("allowed_families", []))
    if allowed != ALLOWED_FAMILIES:
        errors.append(
            f"{repo_relative(JSON_POLICY_PATH)} allowed_families must exactly match "
            f"{sorted(ALLOWED_FAMILIES)}, found {sorted(allowed)}"
        )

    deferred = set(policy.get("deferred_families", []))
    if not DEFERRED_FAMILIES.issubset(deferred):
        errors.append(f"{repo_relative(JSON_POLICY_PATH)} deferred_families must include {sorted(DEFERRED_FAMILIES)}")

    family_rules = policy.get("family_rules")
    if not isinstance(family_rules, dict):
        errors.append(f"{repo_relative(JSON_POLICY_PATH)} family_rules must be an object")
        family_rules = {}

    for family in sorted(ALLOWED_FAMILIES):
        rules = family_rules.get(family)
        if not isinstance(rules, dict):
            errors.append(f"{repo_relative(JSON_POLICY_PATH)} missing family_rules entry for {family}")
            continue
        if rules.get("future_template_allowed") is not False:
            errors.append(f"{family}: future_template_allowed must remain false until reviewed")
        for gate in ("protected_preview_allowed", "reviewed_bank_allowed", "runtime_allowed"):
            if rules.get(gate) is not False:
                errors.append(f"{family}: {gate} must remain false")
        if not rules.get("allowed_intents"):
            errors.append(f"{family}: allowed_intents must be populated")
        if not rules.get("forbidden_intents"):
            errors.append(f"{family}: forbidden_intents must be populated")
        if not rules.get("required_review_fields"):
            errors.append(f"{family}: required_review_fields must be populated")
        if rules.get("family_policy_review_status") != "yossi_family_policy_approved":
            errors.append(f"{family}: family_policy_review_status must be yossi_family_policy_approved")

    deferred_rules = family_rules.get("basic_verb_form_recognition", {})
    if deferred_rules.get("status") != "deferred":
        errors.append("basic_verb_form_recognition must have status=deferred")
    if deferred_rules.get("family_policy_review_status") != "deferred":
        errors.append("basic_verb_form_recognition family_policy_review_status must remain deferred")
    if deferred_rules.get("future_template_allowed") is not False:
        errors.append("basic_verb_form_recognition future_template_allowed must remain false")
    for gate in ("protected_preview_allowed", "reviewed_bank_allowed", "runtime_allowed"):
        if deferred_rules.get(gate) is not False:
            errors.append(f"basic_verb_form_recognition {gate} must remain false")

    safety_defaults = policy.get("safety_gate_defaults", {})
    if safety_defaults.get("question_allowed") != "needs_review":
        errors.append("safety_gate_defaults.question_allowed must remain needs_review")
    for gate in ("protected_preview_allowed", "reviewed_bank_allowed", "runtime_allowed", "student_use_allowed"):
        if safety_defaults.get(gate) is not False:
            errors.append(f"safety_gate_defaults.{gate} must remain false")

    forbidden_output_types = set(policy.get("forbidden_output_types", []))
    missing_output_types = sorted(FORBIDDEN_OUTPUT_TYPES - forbidden_output_types)
    if missing_output_types:
        errors.append(f"{repo_relative(JSON_POLICY_PATH)} missing forbidden_output_types: {missing_output_types}")

    serialized_policy = json.dumps(policy, ensure_ascii=False).lower()
    for phrase in FORBIDDEN_PHRASES:
        if contains_forbidden_phrase(serialized_policy, phrase):
            errors.append(f"{repo_relative(JSON_POLICY_PATH)} contains forbidden unnegated phrase: {phrase}")

    policy_text = DOC_POLICY_PATH.read_text(encoding="utf-8")
    for phrase in SAFETY_PHRASES:
        if phrase not in policy_text:
            errors.append(f"{repo_relative(DOC_POLICY_PATH)} missing safety phrase: {phrase!r}")
    for family in sorted(ALLOWED_FAMILIES | DEFERRED_FAMILIES):
        if family not in policy_text:
            errors.append(f"{repo_relative(DOC_POLICY_PATH)} missing family policy for {family}")
    for phrase in (
        'Do not ask "What does את mean?" as if it has a simple English translation.',
        'Do not translate `את` as "the."',
        'Do not translate `את` as "with."',
        "No `basic_verb_form_recognition` candidate may become an input candidate until a separate morphology-question wording policy exists.",
        "Yossi reviewed this family-level wording policy and approved these family policies:",
        "Future exact template wording review is still required. No protected-preview planning is approved yet.",
    ):
        if phrase not in policy_text:
            errors.append(f"{repo_relative(DOC_POLICY_PATH)} missing required wording rule: {phrase!r}")
    if "answer choices" not in policy_text or "answer keys" not in policy_text:
        errors.append(f"{repo_relative(DOC_POLICY_PATH)} must explicitly forbid answer choices and answer keys")

    packet_text = YOSSI_PACKET_PATH.read_text(encoding="utf-8")
    for phrase in (
        "This packet does not approve questions, answer choices, answer keys, protected-preview use, reviewed-bank use, runtime use, or student-facing use.",
        "Recorded decision: `approve_family_policy`",
        "Recorded decision: `keep_deferred`",
        "approve_family_policy",
        "approve_with_revision",
        "needs_follow_up",
        "block_family_for_now",
        "basic_verb_form_recognition",
    ):
        if phrase not in packet_text:
            errors.append(f"{repo_relative(YOSSI_PACKET_PATH)} missing required packet phrase: {phrase!r}")

    report_text = POLICY_REPORT_PATH.read_text(encoding="utf-8")
    for phrase in (
        "Why This Policy Exists",
        "Approved Input Candidate Families",
        "Deferred Families",
        "No questions generated.",
        "No answer choices generated.",
        "No answer keys generated.",
        "No protected-preview input list created.",
        "No runtime changes made.",
    ):
        if phrase not in report_text:
            errors.append(f"{repo_relative(POLICY_REPORT_PATH)} missing required report phrase: {phrase!r}")

    summary = policy.get("family_policy_review_summary", {})
    if summary.get("families_reviewed") != 5:
        errors.append("family_policy_review_summary.families_reviewed must be 5")
    if summary.get("approved_family_policies") != 4:
        errors.append("family_policy_review_summary.approved_family_policies must be 4")
    if summary.get("deferred_family_policies") != 1:
        errors.append("family_policy_review_summary.deferred_family_policies must be 1")
    if set(summary.get("approved_families", [])) != ALLOWED_FAMILIES:
        errors.append("family_policy_review_summary.approved_families must match allowed families")
    if summary.get("deferred_families") != ["basic_verb_form_recognition"]:
        errors.append("family_policy_review_summary.deferred_families must list basic_verb_form_recognition only")
    if summary.get("protected_preview_planning_approved") is not False:
        errors.append("family_policy_review_summary.protected_preview_planning_approved must remain false")
    if summary.get("question_generation_approved") is not False:
        errors.append("family_policy_review_summary.question_generation_approved must remain false")

    et_cautions = family_rules.get("direct_object_marker_recognition", {}).get("required_cautions", [])
    for phrase in (
        "must use function wording",
        "must not ask what את means as a simple translation",
        "must not translate את as the",
        "must not translate את as with",
        "must require future exact wording review",
    ):
        if phrase not in et_cautions:
            errors.append(f"direct_object_marker_recognition required_cautions missing {phrase!r}")

    applied_text = APPLIED_REPORT_PATH.read_text(encoding="utf-8")
    for phrase in (
        "families reviewed: 5",
        "approved family policies: 4",
        "deferred family policies: 1",
        "direct_object_marker_recognition",
        "basic_verb_form_recognition",
        "no questions generated",
        "no answer choices generated",
        "no answer keys generated",
        "no protected-preview input list created",
        "no protected-preview content created",
        "no reviewed-bank entries created",
        "no runtime changes made",
        "no student-facing use approved",
    ):
        if phrase not in applied_text:
            errors.append(f"{repo_relative(APPLIED_REPORT_PATH)} missing required phrase: {phrase!r}")

    readme_text = README_PATH.read_text(encoding="utf-8")
    for relative in (
        "docs/question_templates/perek_1_approved_input_candidate_wording_policy.md",
        "question_template_wording_policy.v1.json",
        "reports/perek_1_approved_input_candidate_wording_policy_yossi_review_packet.md",
        "reports/perek_1_question_template_wording_policy_report.md",
        "reports/perek_1_approved_input_candidate_wording_policy_yossi_review_applied.md",
    ):
        if relative not in readme_text:
            errors.append(f"{repo_relative(README_PATH)} missing link/reference to {relative}")
    for phrase in (
        "no questions were generated",
        "no protected-preview input list was created",
        "verb-form remains deferred",
        "Yossi reviews wording policy",
        "Exact template wording review is still required",
        "Protected preview remains a later gate",
    ):
        if phrase not in readme_text:
            errors.append(f"{repo_relative(README_PATH)} missing metadata phrase: {phrase!r}")

    docs_readme = DOC_README_PATH.read_text(encoding="utf-8")
    if "perek_1_approved_input_candidate_wording_policy.md" not in docs_readme:
        errors.append(f"{repo_relative(DOC_README_PATH)} missing Perek 1 policy link")

    for path in (DOC_POLICY_PATH, YOSSI_PACKET_PATH, POLICY_REPORT_PATH, APPLIED_REPORT_PATH, DOC_README_PATH):
        text = path.read_text(encoding="utf-8")
        for phrase in FORBIDDEN_PHRASES:
            if contains_forbidden_phrase(text, phrase):
                errors.append(f"{repo_relative(path)} contains forbidden unnegated phrase: {phrase}")

    return {
        "valid": not errors,
        "policy_markdown_path": repo_relative(DOC_POLICY_PATH),
        "policy_json_path": repo_relative(JSON_POLICY_PATH),
        "yossi_packet_path": repo_relative(YOSSI_PACKET_PATH),
        "policy_report_path": repo_relative(POLICY_REPORT_PATH),
        "applied_report_path": repo_relative(APPLIED_REPORT_PATH),
        "allowed_families": sorted(allowed),
        "deferred_families": sorted(deferred),
        "approved_family_policy_count": sum(
            1
            for family in ALLOWED_FAMILIES
            if family_rules.get(family, {}).get("family_policy_review_status") == "yossi_family_policy_approved"
        ),
        "errors": errors,
    }


def main() -> int:
    summary = validate_question_template_wording_policy()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
