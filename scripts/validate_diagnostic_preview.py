from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import dikduk_rules_loader
import generate_diagnostic_preview as preview_generator
import translation_sources_loader
import validate_curriculum_extraction as curriculum_validator


FORBIDDEN_STATUSES = {"active", "runtime_active", "production", "production_ready", "approved", "reviewed"}
TRANSLATION_LICENSE_WARNING = preview_generator.TRANSLATION_USAGE_STATUS
REVIEWABLE_REQUIRED_FIELDS = {
    "question_id",
    "sefer",
    "perek",
    "pasuk",
    "ref",
    "question_text",
    "answer_choices",
    "correct_answer",
    "student_explanation",
    "difficulty_level",
    "skill_category",
    "hebrew_word_or_phrase",
    "hebrew_context",
    "koren_translation_support",
    "metsudah_translation_support",
    "translation_alignment_status",
    "source_support_note",
    "dikduk_rule_id",
    "dikduk_rule_name",
    "dikduk_rule_summary",
    "student_error_pattern_id",
    "student_error_pattern_summary",
    "review_priority",
    "likely_review_status",
    "review_flags",
    "why_this_question_was_generated",
    "what_the_question_tests",
    "why_the_correct_answer_is_correct",
    "why_each_distractor_is_wrong",
    "possible_alternate_answers",
    "teacher_review_note",
    "student_readiness_risk",
    "status",
    "runtime_status",
    "production_status",
    "translation_usage_status",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, 1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path.as_posix()} line {line_number}: invalid JSON ({exc})") from exc
            if not isinstance(row, dict):
                raise ValueError(f"{path.as_posix()} line {line_number}: expected JSON object")
            rows.append(row)
    return rows


def load_hebrew_refs(path: Path) -> set[str]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return {f"Genesis {row['perek']}:{row['pasuk']}" for row in reader}


def validate_reviewable_preview(
    hebrew_refs: set[str],
    koren_rows: dict[str, dict[str, Any]],
    metsudah_rows: dict[str, dict[str, Any]],
    rule_index: dict[str, dict[str, Any]],
    error_index: dict[str, dict[str, Any]],
    errors: list[str],
) -> dict[str, Any]:
    paths = preview_generator.reviewable_preview_paths()
    for required_path in paths.values():
        if not required_path.exists():
            errors.append(f"Missing reviewable preview artifact: {required_path.as_posix()}")
    if any(not path.exists() for path in paths.values()):
        return {"total_questions": 0}

    reviewable_questions = load_jsonl(paths["questions"])
    reviewable_summary = load_json(paths["summary_json"])
    reviewable_packet = paths["manual_review_packet"].read_text(encoding="utf-8")

    question_ids = [row["question_id"] for row in reviewable_questions]
    if len(question_ids) != len(set(question_ids)):
        errors.append("Reviewable preview question IDs must be unique.")
    if not 30 <= len(reviewable_questions) <= 45:
        errors.append("Reviewable preview must contain between 30 and 45 questions.")

    skill_counts = Counter()
    difficulty_counts = Counter()
    likely_review_status_counts = Counter()
    review_flag_counts = Counter()
    translation_alignment_counts = Counter()
    risk_counts = Counter()

    for row in reviewable_questions:
        missing = [field for field in REVIEWABLE_REQUIRED_FIELDS if field not in row]
        if missing:
            errors.append(f"Reviewable question {row.get('question_id', '<missing>')} is missing fields: {missing}")
            continue
        if row["ref"] not in hebrew_refs:
            errors.append(f"Reviewable question ref not found in canonical Hebrew source: {row['ref']}")
        if row["ref"] not in koren_rows or row["ref"] not in metsudah_rows:
            errors.append(f"Reviewable question ref missing in translation rows: {row['ref']}")
        if row["correct_answer"] not in row["answer_choices"]:
            errors.append(f"Reviewable question {row['question_id']} correct_answer is not present in answer_choices.")
        if row["difficulty_level"] not in preview_generator.REVIEWABLE_DIFFICULTY_VALUES:
            errors.append(f"Reviewable question {row['question_id']} uses invalid difficulty_level {row['difficulty_level']!r}.")
        if row["skill_category"] not in preview_generator.REVIEWABLE_SKILL_CATEGORIES:
            errors.append(f"Reviewable question {row['question_id']} uses invalid skill_category {row['skill_category']!r}.")
        if row["translation_alignment_status"] not in preview_generator.REVIEWABLE_TRANSLATION_ALIGNMENT_VALUES:
            errors.append(
                f"Reviewable question {row['question_id']} uses invalid translation_alignment_status {row['translation_alignment_status']!r}."
            )
        if row["review_priority"] not in preview_generator.REVIEWABLE_REVIEW_PRIORITY_VALUES:
            errors.append(f"Reviewable question {row['question_id']} uses invalid review_priority {row['review_priority']!r}.")
        if row["likely_review_status"] not in preview_generator.REVIEWABLE_REVIEW_STATUS_VALUES:
            errors.append(
                f"Reviewable question {row['question_id']} uses invalid likely_review_status {row['likely_review_status']!r}."
            )
        if row["student_readiness_risk"] not in preview_generator.REVIEWABLE_STUDENT_RISK_VALUES:
            errors.append(
                f"Reviewable question {row['question_id']} uses invalid student_readiness_risk {row['student_readiness_risk']!r}."
            )
        if not isinstance(row["review_flags"], list):
            errors.append(f"Reviewable question {row['question_id']} must store review_flags as a list.")
        else:
            unknown_flags = sorted(set(row["review_flags"]) - preview_generator.REVIEWABLE_REVIEW_FLAGS)
            if unknown_flags:
                errors.append(f"Reviewable question {row['question_id']} uses unknown review flags: {unknown_flags}")
        if not isinstance(row["why_each_distractor_is_wrong"], dict):
            errors.append(f"Reviewable question {row['question_id']} must store why_each_distractor_is_wrong as a dict.")
        else:
            wrong_choices = [choice for choice in row["answer_choices"] if choice != row["correct_answer"]]
            if set(row["why_each_distractor_is_wrong"]) != set(wrong_choices):
                errors.append(
                    f"Reviewable question {row['question_id']} must explain every distractor and only the distractors."
                )
        if row["status"] in FORBIDDEN_STATUSES:
            errors.append(f"Reviewable question {row['question_id']} uses forbidden status {row['status']!r}.")
        if row["runtime_status"] != preview_generator.REVIEWABLE_RUNTIME_STATUS:
            errors.append(f"Reviewable question {row['question_id']} must stay not_runtime_active.")
        if row["production_status"] != preview_generator.REVIEWABLE_PRODUCTION_STATUS:
            errors.append(f"Reviewable question {row['question_id']} must stay not_production_ready.")
        if row["translation_usage_status"] != TRANSLATION_LICENSE_WARNING:
            errors.append(f"Reviewable question {row['question_id']} must preserve the translation license warning.")
        if row["dikduk_rule_id"] and row["dikduk_rule_id"] not in rule_index:
            errors.append(f"Reviewable question {row['question_id']} references unknown dikduk_rule_id {row['dikduk_rule_id']}.")
        if row["student_error_pattern_id"] and row["student_error_pattern_id"] not in error_index:
            errors.append(
                f"Reviewable question {row['question_id']} references unknown student_error_pattern_id {row['student_error_pattern_id']}."
            )

        skill_counts[row["skill_category"]] += 1
        difficulty_counts[row["difficulty_level"]] += 1
        likely_review_status_counts[row["likely_review_status"]] += 1
        review_flag_counts.update(row["review_flags"])
        translation_alignment_counts[row["translation_alignment_status"]] += 1
        risk_counts[row["student_readiness_risk"]] += 1

    if reviewable_summary.get("total_questions") != len(reviewable_questions):
        errors.append("Reviewable preview summary total_questions does not match JSONL.")
    if reviewable_summary.get("skill_counts") != dict(sorted(skill_counts.items())):
        errors.append("Reviewable preview summary skill_counts do not match JSONL.")
    if reviewable_summary.get("difficulty_counts") != {
        key: difficulty_counts.get(key, 0) for key in ("easy", "medium", "hard")
    }:
        errors.append("Reviewable preview summary difficulty_counts do not match JSONL.")
    if reviewable_summary.get("likely_review_status_counts") != {
        key: likely_review_status_counts.get(key, 0) for key in ("likely_approve", "caution", "likely_rewrite")
    }:
        errors.append("Reviewable preview summary likely_review_status_counts do not match JSONL.")
    if reviewable_summary.get("review_flag_counts") != dict(sorted(review_flag_counts.items())):
        errors.append("Reviewable preview summary review_flag_counts do not match JSONL.")
    if reviewable_summary.get("translation_alignment_counts") != {
        key: translation_alignment_counts.get(key, 0)
        for key in (
            "koren_and_metsudah_align",
            "minor_translation_difference",
            "significant_translation_difference",
            "translation_review_required",
        )
    }:
        errors.append("Reviewable preview summary translation_alignment_counts do not match JSONL.")
    if reviewable_summary.get("low_risk_student_candidate_count") != risk_counts.get("low", 0):
        errors.append("Reviewable preview summary low_risk_student_candidate_count does not match JSONL.")
    if reviewable_summary.get("medium_risk_count") != risk_counts.get("medium", 0):
        errors.append("Reviewable preview summary medium_risk_count does not match JSONL.")
    if reviewable_summary.get("high_risk_count") != risk_counts.get("high", 0):
        errors.append("Reviewable preview summary high_risk_count does not match JSONL.")
    if reviewable_summary.get("final_recommendation") != preview_generator.REVIEWABLE_PREVIEW_FINAL_RECOMMENDATION:
        errors.append("Reviewable preview summary final_recommendation is not the expected review-only label.")
    if preview_generator.REVIEWABLE_PREVIEW_FINAL_RECOMMENDATION not in reviewable_packet:
        errors.append("Reviewable manual review packet must include the final recommendation label.")
    if TRANSLATION_LICENSE_WARNING not in reviewable_packet:
        errors.append("Reviewable manual review packet must preserve the translation license warning.")

    return {
        "total_questions": len(reviewable_questions),
        "likely_review_status_counts": dict(sorted(likely_review_status_counts.items())),
        "review_flag_counts": dict(sorted(review_flag_counts.items())),
    }


def validate_preview(config_path: Path) -> dict[str, Any]:
    config = preview_generator.load_config(config_path)
    outputs = config["output_files"]
    blueprint_path = REPO_ROOT / outputs["blueprints"]
    question_path = REPO_ROOT / outputs["questions"]
    review_packet_path = REPO_ROOT / outputs["manual_review_packet"]
    summary_md_path = REPO_ROOT / outputs["summary_markdown"]
    summary_json_path = REPO_ROOT / outputs["summary_json"]
    registry_path = REPO_ROOT / config["translation_registry_file"]

    errors: list[str] = []
    warnings: list[str] = []
    for required_path in (
        blueprint_path,
        question_path,
        review_packet_path,
        summary_md_path,
        summary_json_path,
        registry_path,
    ):
        if not required_path.exists():
            errors.append(f"Missing required artifact: {required_path.as_posix()}")

    if errors:
        return {"valid": False, "errors": errors, "warnings": warnings}

    blueprints = load_jsonl(blueprint_path)
    questions = load_jsonl(question_path)
    summary = load_json(summary_json_path)
    registry = translation_sources_loader.load_translation_registry()
    hebrew_refs = load_hebrew_refs(REPO_ROOT / config["source_hebrew_file"])
    rule_index = dikduk_rules_loader.dikduk_rule_index()
    template_index = dikduk_rules_loader.dikduk_template_index()
    error_index = dikduk_rules_loader.dikduk_error_index()
    koren_rows = {row["ref"]: row for row in load_jsonl(REPO_ROOT / config["koren_translation_file"])}
    metsudah_rows = {row["ref"]: row for row in load_jsonl(REPO_ROOT / config["metsudah_translation_file"])}

    blueprint_ids = [row["blueprint_id"] for row in blueprints]
    if len(blueprint_ids) != len(set(blueprint_ids)):
        errors.append("Duplicate blueprint IDs detected.")
    question_ids = [row["question_id"] for row in questions]
    if len(question_ids) != len(set(question_ids)):
        errors.append("Duplicate question IDs detected.")

    blueprints_by_id = {row["blueprint_id"]: row for row in blueprints}
    for blueprint in blueprints:
        if blueprint["ref"] not in hebrew_refs:
            errors.append(f"Blueprint ref not found in canonical Hebrew source: {blueprint['ref']}")
        for rule_id in blueprint.get("dikduk_rule_ids", []):
            if rule_id not in rule_index:
                errors.append(f"Blueprint references unknown rule_id: {rule_id}")
        for template_id in blueprint.get("question_template_ids", []):
            if template_id not in template_index:
                errors.append(f"Blueprint references unknown question_template_id: {template_id}")
        if not blueprint.get("mastery_tags"):
            errors.append(f"Blueprint {blueprint['blueprint_id']} has empty mastery_tags.")
        if blueprint.get("status") in FORBIDDEN_STATUSES:
            errors.append(f"Blueprint {blueprint['blueprint_id']} uses forbidden status {blueprint.get('status')!r}.")
        if blueprint.get("translation_usage_status") != TRANSLATION_LICENSE_WARNING:
            errors.append(f"Blueprint {blueprint['blueprint_id']} is missing the required translation license warning.")

    lane_counts = Counter()
    skill_counts = Counter()
    mastery_counts = Counter()
    difficulty_counts = Counter()
    for question in questions:
        blueprint = blueprints_by_id.get(question["blueprint_id"])
        if blueprint is None:
            errors.append(f"Question {question['question_id']} points to missing blueprint {question['blueprint_id']}.")
            continue
        if question["ref"] not in hebrew_refs:
            errors.append(f"Question ref not found in canonical Hebrew source: {question['ref']}")
        if question["ref"] not in koren_rows or question["ref"] not in metsudah_rows:
            errors.append(f"Question ref missing in translation rows: {question['ref']}")
        if question.get("status") in FORBIDDEN_STATUSES:
            errors.append(f"Question {question['question_id']} uses forbidden status {question.get('status')!r}.")
        if question.get("translation_usage_status") != TRANSLATION_LICENSE_WARNING:
            errors.append(f"Question {question['question_id']} is missing the required translation license warning.")
        if not question.get("prompt") or not question.get("correct_answer") or not question.get("feedback_correct") or not question.get("feedback_incorrect"):
            errors.append(f"Question {question['question_id']} is missing prompt/answer/feedback fields.")
        choices = question.get("choices", [])
        if len(choices) < 4 or len(set(choices)) != len(choices):
            errors.append(f"Question {question['question_id']} must have four unique multiple-choice options.")
        if question.get("correct_answer") not in choices:
            errors.append(f"Question {question['question_id']} correct_answer is not present in choices.")
        if not question.get("accepted_answers"):
            errors.append(f"Question {question['question_id']} has no accepted_answers.")
        for rule_id in question.get("dikduk_rule_ids", []):
            if rule_id not in rule_index:
                errors.append(f"Question {question['question_id']} references unknown rule_id {rule_id}.")
        for error_id in question.get("student_error_pattern_ids", []):
            if error_id not in error_index:
                errors.append(f"Question {question['question_id']} references unknown error pattern {error_id}.")
        template_id = question.get("question_template_id")
        if template_id and template_id not in template_index:
            errors.append(f"Question {question['question_id']} references unknown template {template_id}.")
        if not question.get("mastery_tags"):
            errors.append(f"Question {question['question_id']} has empty mastery_tags.")
        if question.get("source_evidence", {}).get("translation_usage_status") != TRANSLATION_LICENSE_WARNING:
            errors.append(f"Question {question['question_id']} source_evidence is missing the translation warning.")
        lane_counts[question["diagnostic_lane"]] += 1
        skill_counts[question["skill_focus"]] += 1
        mastery_counts.update(question["mastery_tags"])
        difficulty_counts[str(question["difficulty_level"])] += 1

    if summary.get("total_blueprints") != len(blueprints):
        errors.append("Summary total_blueprints does not match blueprint JSONL.")
    if summary.get("total_questions") != len(questions):
        errors.append("Summary total_questions does not match question JSONL.")
    if summary.get("question_count_by_lane") != dict(sorted(lane_counts.items())):
        errors.append("Summary question_count_by_lane does not match generated questions.")
    if summary.get("question_count_by_skill") != dict(sorted(skill_counts.items())):
        errors.append("Summary question_count_by_skill does not match generated questions.")
    if summary.get("question_count_by_mastery_tag") != dict(sorted(mastery_counts.items())):
        errors.append("Summary question_count_by_mastery_tag does not match generated questions.")
    if summary.get("question_count_by_difficulty") != dict(sorted(difficulty_counts.items(), key=lambda item: int(item[0]))):
        errors.append("Summary question_count_by_difficulty does not match generated questions.")

    minimums = config["minimum_question_counts"]
    if len(questions) < minimums["total_questions"]:
        errors.append("Total question count is below configured minimum.")
    if lane_counts.get("translation", 0) < minimums["translation"]:
        errors.append("Translation lane count is below configured minimum.")
    if lane_counts.get("dikduk", 0) < minimums["dikduk"]:
        errors.append("Dikduk lane count is below configured minimum.")
    if lane_counts.get("word_analysis", 0) < minimums["word_analysis"]:
        errors.append("Word-analysis lane count is below configured minimum.")
    if lane_counts.get("error_diagnosis", 0) < minimums["error_diagnosis"]:
        errors.append("Error-diagnosis lane count is below configured minimum.")
    if skill_counts.get("mixed_skill_translation_rule", 0) < minimums["mixed_skill"]:
        errors.append("Mixed-skill count is below configured minimum.")

    if registry.get("runtime_status") != preview_generator.RUNTIME_STATUS:
        errors.append("Translation registry must stay not_runtime_active.")
    if registry.get("production_status") != preview_generator.PRODUCTION_STATUS:
        errors.append("Translation registry must stay not_production_ready.")

    curriculum_summary = curriculum_validator.validate_curriculum_extraction(check_git_diff=True)
    if not curriculum_summary.get("valid"):
        errors.extend(curriculum_summary.get("errors", []))

    reviewable_summary = validate_reviewable_preview(
        hebrew_refs=hebrew_refs,
        koren_rows=koren_rows,
        metsudah_rows=metsudah_rows,
        rule_index=rule_index,
        error_index=error_index,
        errors=errors,
    )

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "total_blueprints": len(blueprints),
        "total_questions": len(questions),
        "question_count_by_lane": dict(sorted(lane_counts.items())),
        "reviewable_preview": reviewable_summary,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate non-runtime diagnostic preview artifacts.")
    parser.add_argument("--config", required=True, help="Path to the diagnostic preview config JSON file.")
    args = parser.parse_args()
    config_path = (REPO_ROOT / args.config).resolve() if not Path(args.config).is_absolute() else Path(args.config)
    summary = validate_preview(config_path)
    if not summary["valid"]:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        raise SystemExit(1)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
