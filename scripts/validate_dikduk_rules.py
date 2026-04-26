from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from dikduk_rules_loader import (  # noqa: E402
    DIKDUK_RULES_DIR,
)


RULE_ID_PATTERN = re.compile(r"^DK-[A-Z]+(?:-[A-Z]+)*-\d{3}$")
TEMPLATE_ID_PATTERN = re.compile(r"^QT-DK-[A-Z]+(?:-[A-Z]+)*-\d{3}-[A-Z]$")
ERROR_ID_PATTERN = re.compile(r"^ERR-DK-[A-Z]+(?:-[A-Z]+)*-\d{3}$")
ALLOWED_STATUSES = {"draft_source_modeled", "needs_review", "blocked_ambiguous", "deprecated"}
FORBIDDEN_STATUSES = {"reviewed", "approved", "production", "runtime_active", "active"}


def _load_json(path: Path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def _load_jsonl(path: Path, errors: list[str]) -> list[dict]:
    records: list[dict] = []
    try:
        with path.open("r", encoding="utf-8") as file:
            for line_number, raw_line in enumerate(file, start=1):
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    parsed = json.loads(line)
                except json.JSONDecodeError as exc:
                    errors.append(f"{path}: line {line_number} is not valid JSON: {exc}")
                    continue
                if not isinstance(parsed, dict):
                    errors.append(f"{path}: line {line_number} must decode to a JSON object.")
                    continue
                records.append(parsed)
    except FileNotFoundError:
        errors.append(f"Missing required file: {path}")
    return records


def _require_fields(record: dict, required_fields: tuple[str, ...], label: str, errors: list[str]) -> None:
    for field in required_fields:
        if field not in record:
            errors.append(f"{label} missing required field '{field}'.")


def _validate_status(status: str | None, label: str, errors: list[str]) -> None:
    if not status:
        errors.append(f"{label} missing status.")
        return
    if status in FORBIDDEN_STATUSES:
        errors.append(f"{label} uses forbidden status '{status}'.")
    elif status not in ALLOWED_STATUSES:
        errors.append(f"{label} has unsupported status '{status}'.")


def validate_dikduk_rules(package_dir: Path | None = None) -> dict:
    package_dir = package_dir or DIKDUK_RULES_DIR
    errors: list[str] = []

    manifest_path = package_dir / "dikduk_rules_manifest.json"
    groups_path = package_dir / "rule_groups.json"
    rules_path = package_dir / "rules_loshon_foundation.jsonl"
    templates_path = package_dir / "question_templates.jsonl"
    errors_path = package_dir / "student_error_patterns.jsonl"
    schema_paths = [
        package_dir / "dikduk_rule.schema.json",
        package_dir / "dikduk_question_template.schema.json",
        package_dir / "dikduk_error_pattern.schema.json",
    ]

    manifest = {}
    groups: list[dict] = []
    if not manifest_path.exists():
        errors.append(f"Missing required file: {manifest_path}")
    else:
        manifest = _load_json(manifest_path)
        if not isinstance(manifest, dict):
            errors.append("dikduk_rules_manifest.json must be a JSON object.")

    if not groups_path.exists():
        errors.append(f"Missing required file: {groups_path}")
    else:
        groups = _load_json(groups_path)
        if not isinstance(groups, list):
            errors.append("rule_groups.json must be a JSON list.")
            groups = []

    for schema_path in schema_paths:
        if not schema_path.exists():
            errors.append(f"Missing required file: {schema_path}")
            continue
        parsed_schema = _load_json(schema_path)
        if not isinstance(parsed_schema, dict):
            errors.append(f"{schema_path} must be a JSON object.")

    rules = _load_jsonl(rules_path, errors)
    templates = _load_jsonl(templates_path, errors)
    error_patterns = _load_jsonl(errors_path, errors)

    group_ids = set()
    for index, group in enumerate(groups):
        label = f"rule_groups.json[{index}]"
        if not isinstance(group, dict):
            errors.append(f"{label} must be an object.")
            continue
        _require_fields(
            group,
            ("group_id", "display_name", "description", "typical_mastery_tags", "question_types_supported"),
            label,
            errors,
        )
        group_id = group.get("group_id")
        if isinstance(group_id, str):
            if group_id in group_ids:
                errors.append(f"Duplicate group_id '{group_id}'.")
            group_ids.add(group_id)

    rule_ids: set[str] = set()
    template_ids: set[str] = set()
    error_ids: set[str] = set()

    for index, record in enumerate(rules):
        label = f"rules_loshon_foundation.jsonl[{index}]"
        _require_fields(
            record,
            (
                "rule_id",
                "schema_version",
                "rule_group",
                "skill_name",
                "status",
                "source_reference",
                "student_facing_rule",
                "technical_rule",
                "examples",
                "common_errors",
                "question_template_ids",
                "feedback_templates",
                "mastery_tags",
                "difficulty_level",
                "prerequisite_rule_ids",
                "followup_rule_ids",
                "zekelman_alignment",
            ),
            label,
            errors,
        )
        rule_id = record.get("rule_id")
        if isinstance(rule_id, str):
            if not RULE_ID_PATTERN.match(rule_id):
                errors.append(f"{label}.rule_id '{rule_id}' does not match the expected pattern.")
            if rule_id in rule_ids:
                errors.append(f"Duplicate rule_id '{rule_id}'.")
            rule_ids.add(rule_id)
        _validate_status(record.get("status"), label, errors)
        if record.get("rule_group") not in group_ids:
            errors.append(f"{label}.rule_group '{record.get('rule_group')}' is not declared in rule_groups.json.")
        if not isinstance(record.get("examples"), list) or not record["examples"]:
            errors.append(f"{label}.examples must contain at least one example.")
        if not isinstance(record.get("common_errors"), list) or not record["common_errors"]:
            errors.append(f"{label}.common_errors must contain at least one item.")
        if not isinstance(record.get("mastery_tags"), list) or not record["mastery_tags"]:
            errors.append(f"{label}.mastery_tags must contain at least one item.")
        if not isinstance(record.get("question_template_ids"), list) or not record["question_template_ids"]:
            errors.append(f"{label}.question_template_ids must contain at least one ID.")
        if not isinstance(record.get("feedback_templates"), dict) or not record["feedback_templates"]:
            errors.append(f"{label}.feedback_templates must be a non-empty object.")
        source_reference = record.get("source_reference")
        if not isinstance(source_reference, dict):
            errors.append(f"{label}.source_reference must be an object.")
        else:
            if not source_reference.get("source_file"):
                errors.append(f"{label}.source_reference.source_file is required.")
            if not source_reference.get("source_note"):
                errors.append(f"{label}.source_reference.source_note is required.")
        zekl = record.get("zekelman_alignment")
        if not isinstance(zekl, list) or not zekl:
            errors.append(f"{label}.zekelman_alignment must contain at least one entry.")

    for index, record in enumerate(templates):
        label = f"question_templates.jsonl[{index}]"
        _require_fields(
            record,
            (
                "template_id",
                "schema_version",
                "rule_id",
                "question_type",
                "prompt_template",
                "answer_template",
                "distractor_strategy",
                "feedback_correct",
                "feedback_incorrect",
                "mastery_tags",
                "status",
            ),
            label,
            errors,
        )
        template_id = record.get("template_id")
        if isinstance(template_id, str):
            if not TEMPLATE_ID_PATTERN.match(template_id):
                errors.append(f"{label}.template_id '{template_id}' does not match the expected pattern.")
            if template_id in template_ids:
                errors.append(f"Duplicate template_id '{template_id}'.")
            template_ids.add(template_id)
        _validate_status(record.get("status"), label, errors)
        if record.get("rule_id") not in rule_ids:
            errors.append(f"{label}.rule_id '{record.get('rule_id')}' does not point to an existing rule.")
        if not isinstance(record.get("mastery_tags"), list) or not record["mastery_tags"]:
            errors.append(f"{label}.mastery_tags must contain at least one item.")

    for index, record in enumerate(error_patterns):
        label = f"student_error_patterns.jsonl[{index}]"
        _require_fields(
            record,
            (
                "error_id",
                "schema_version",
                "linked_rule_ids",
                "observed_wrong_answer",
                "expected_answer",
                "diagnosis",
                "remediation_hint",
                "mastery_penalty_tags",
                "status",
            ),
            label,
            errors,
        )
        error_id = record.get("error_id")
        if isinstance(error_id, str):
            if not ERROR_ID_PATTERN.match(error_id):
                errors.append(f"{label}.error_id '{error_id}' does not match the expected pattern.")
            if error_id in error_ids:
                errors.append(f"Duplicate error_id '{error_id}'.")
            error_ids.add(error_id)
        _validate_status(record.get("status"), label, errors)
        linked_rule_ids = record.get("linked_rule_ids")
        if not isinstance(linked_rule_ids, list) or not linked_rule_ids:
            errors.append(f"{label}.linked_rule_ids must contain at least one rule ID.")
        else:
            for linked_rule_id in linked_rule_ids:
                if linked_rule_id not in rule_ids:
                    errors.append(f"{label} references missing rule_id '{linked_rule_id}'.")

    for rule in rules:
        for template_id in rule.get("question_template_ids", []):
            if template_id not in template_ids:
                errors.append(f"Rule {rule.get('rule_id')} references missing template_id '{template_id}'.")

    manifest_counts = ((manifest or {}).get("counts") or {})
    if manifest_counts:
        if manifest_counts.get("rule_groups") != len(groups):
            errors.append("Manifest rule_groups count does not match actual rule group count.")
        if manifest_counts.get("rules") != len(rules):
            errors.append("Manifest rules count does not match actual rule count.")
        if manifest_counts.get("question_templates") != len(templates):
            errors.append("Manifest question_templates count does not match actual template count.")
        if manifest_counts.get("student_error_patterns") != len(error_patterns):
            errors.append("Manifest student_error_patterns count does not match actual error count.")

    summary = {
        "valid": not errors,
        "package_dir": str(package_dir),
        "rule_group_count": len(groups),
        "rule_count": len(rules),
        "question_template_count": len(templates),
        "student_error_pattern_count": len(error_patterns),
        "errors": errors,
    }
    return summary


def main() -> None:
    summary = validate_dikduk_rules()
    if summary["valid"]:
        print("PASS: dikduk rules package is valid.")
        print(f"package dir: {summary['package_dir']}")
        print(f"rule groups: {summary['rule_group_count']}")
        print(f"rules: {summary['rule_count']}")
        print(f"question templates: {summary['question_template_count']}")
        print(f"student error patterns: {summary['student_error_pattern_count']}")
        raise SystemExit(0)
    print("FAIL: dikduk rules package has validation errors.")
    for message in summary["errors"]:
        print(message)
    raise SystemExit(1)


if __name__ == "__main__":
    main()
