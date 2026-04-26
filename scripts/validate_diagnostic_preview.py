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

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "total_blueprints": len(blueprints),
        "total_questions": len(questions),
        "question_count_by_lane": dict(sorted(lane_counts.items())),
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
