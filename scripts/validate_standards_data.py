from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STRUCTURED_STANDARD_3_PATH = (
    ROOT / "data" / "standards" / "zekelman" / "structured" / "zekelman_2025_standard_3_vocabulary_language_skills.json"
)
SUPPLEMENTAL_CROSSWALK_PATH = (
    ROOT / "data" / "standards" / "zekelman" / "crosswalks" / "zekelman_2025_standard_3_supplemental_crosswalk.json"
)
SKILL_MAPPING_DRAFT_PATH = (
    ROOT / "data" / "standards" / "zekelman" / "crosswalks" / "zekelman_2025_standard_3_skill_mapping_draft.json"
)
REVIEW_TRACKING_PATH = (
    ROOT / "data" / "standards" / "zekelman" / "review" / "zekelman_2025_standard_3_review_tracking.json"
)

JSON_INPUT_PATHS = (
    STRUCTURED_STANDARD_3_PATH,
    SUPPLEMENTAL_CROSSWALK_PATH,
    SKILL_MAPPING_DRAFT_PATH,
    REVIEW_TRACKING_PATH,
)

REVIEW_ITEM_REQUIRED_FIELDS = (
    "review_item_id",
    "standard_id",
    "strand",
    "level_range",
    "related_skill_ids",
    "canonical_source_path",
    "supplemental_source_paths",
    "review_priority",
    "diagnostic_relevance",
    "question_generation_relevance",
    "current_review_status",
    "reviewer_decision",
    "reviewer_notes",
    "unresolved_questions",
    "recommended_next_action",
)

ALLOWED_REVIEW_PRIORITIES = {"high", "medium", "low"}
ALLOWED_CURRENT_REVIEW_STATUSES = {
    "needs_teacher_review",
    "source_match_needs_verification",
    "hebrew_needs_verification",
    "level_mapping_needs_review",
    "not_runtime_ready",
    "not_question_ready",
}
ALLOWED_REVIEWER_DECISIONS = {
    "approve_as_foundational_skill",
    "approve_with_wording_revision",
    "approve_with_level_adjustment",
    "needs_more_source_review",
    "not_suitable_for_diagnostic_use_yet",
    "defer_to_later_phase",
}
ALLOWED_EMPTY_REVIEWER_DECISIONS = {None, "", "unset"}
FORBIDDEN_READY_TOKENS = {
    "runtime_ready",
    "question_ready",
    "production_ready",
    "approved_for_runtime",
    "active_question_template",
}


def repo_relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def ensure_object_with_list(
    payload: Any,
    *,
    path: Path,
    list_key: str,
    errors: list[str],
) -> list[Any]:
    relative = repo_relative(path)
    if not isinstance(payload, dict):
        errors.append(f"{relative}: top-level JSON must be an object")
        return []
    records = payload.get(list_key)
    if not isinstance(records, list):
        errors.append(f"{relative}: expected '{list_key}' to be a list")
        return []
    return records


def is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def has_meaningful_strings(values: Any) -> bool:
    return isinstance(values, list) and any(is_non_empty_string(value) for value in values)


def collect_forbidden_tokens(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, nested_value in value.items():
            if key in FORBIDDEN_READY_TOKENS:
                found.add(key)
            found.update(collect_forbidden_tokens(nested_value))
    elif isinstance(value, list):
        for nested_value in value:
            found.update(collect_forbidden_tokens(nested_value))
    elif isinstance(value, str):
        if value in FORBIDDEN_READY_TOKENS:
            found.add(value)
    return found


def validate_review_item(
    item: Any,
    *,
    index: int,
    standard_ids: set[str],
    draft_skill_ids: set[str],
    errors: list[str],
) -> None:
    context = f"review_items[{index}]"
    if not isinstance(item, dict):
        errors.append(f"{context}: review item must be an object")
        return

    for field_name in REVIEW_ITEM_REQUIRED_FIELDS:
        if field_name not in item:
            errors.append(f"{context}: missing required field '{field_name}'")

    review_item_id = item.get("review_item_id")
    if not is_non_empty_string(review_item_id):
        errors.append(f"{context}: review_item_id must be a non-empty string")

    standard_id = item.get("standard_id")
    if not is_non_empty_string(standard_id):
        errors.append(f"{context}: standard_id must be a non-empty string")
    elif standard_id not in standard_ids:
        errors.append(f"{context}: standard_id '{standard_id}' does not match an existing Standard 3 record")

    if not is_non_empty_string(item.get("strand")):
        errors.append(f"{context}: strand must be a non-empty string")
    if not is_non_empty_string(item.get("level_range")):
        errors.append(f"{context}: level_range must be a non-empty string")
    if not is_non_empty_string(item.get("canonical_source_path")):
        errors.append(f"{context}: canonical_source_path must be a non-empty string")

    supplemental_source_paths = item.get("supplemental_source_paths")
    if not isinstance(supplemental_source_paths, list) or not supplemental_source_paths:
        errors.append(f"{context}: supplemental_source_paths must be a non-empty list")
    else:
        for path_index, supplemental_path in enumerate(supplemental_source_paths):
            if not is_non_empty_string(supplemental_path):
                errors.append(
                    f"{context}: supplemental_source_paths[{path_index}] must be a non-empty string"
                )

    related_skill_ids = item.get("related_skill_ids")
    if not isinstance(related_skill_ids, list) or not related_skill_ids:
        errors.append(f"{context}: related_skill_ids must be a non-empty list")
    else:
        for skill_index, skill_id in enumerate(related_skill_ids):
            if not is_non_empty_string(skill_id):
                errors.append(f"{context}: related_skill_ids[{skill_index}] must be a non-empty string")
                continue
            if skill_id not in draft_skill_ids:
                errors.append(f"{context}: related_skill_id '{skill_id}' does not match an existing draft skill mapping")

    review_priority = item.get("review_priority")
    if review_priority not in ALLOWED_REVIEW_PRIORITIES:
        errors.append(
            f"{context}: review_priority must be one of {sorted(ALLOWED_REVIEW_PRIORITIES)}, got {review_priority!r}"
        )

    if not is_non_empty_string(item.get("diagnostic_relevance")):
        errors.append(f"{context}: diagnostic_relevance must be a non-empty string")
    if not is_non_empty_string(item.get("question_generation_relevance")):
        errors.append(f"{context}: question_generation_relevance must be a non-empty string")

    current_review_status = item.get("current_review_status")
    if not isinstance(current_review_status, list) or not current_review_status:
        errors.append(f"{context}: current_review_status must be a non-empty list")
    else:
        for status_index, status in enumerate(current_review_status):
            if status not in ALLOWED_CURRENT_REVIEW_STATUSES:
                errors.append(
                    f"{context}: current_review_status[{status_index}] must be one of "
                    f"{sorted(ALLOWED_CURRENT_REVIEW_STATUSES)}, got {status!r}"
                )

    reviewer_decision = item.get("reviewer_decision")
    if reviewer_decision not in ALLOWED_EMPTY_REVIEWER_DECISIONS and reviewer_decision not in ALLOWED_REVIEWER_DECISIONS:
        errors.append(
            f"{context}: reviewer_decision must be blank/null/unset or one of "
            f"{sorted(ALLOWED_REVIEWER_DECISIONS)}, got {reviewer_decision!r}"
        )

    reviewer_notes = item.get("reviewer_notes")
    if not isinstance(reviewer_notes, str):
        errors.append(f"{context}: reviewer_notes must be a string")

    unresolved_questions = item.get("unresolved_questions")
    if not isinstance(unresolved_questions, list):
        errors.append(f"{context}: unresolved_questions must be a list")

    recommended_next_action = item.get("recommended_next_action")
    if not isinstance(recommended_next_action, str):
        errors.append(f"{context}: recommended_next_action must be a string")

    if review_priority == "high":
        if not has_meaningful_strings(unresolved_questions):
            errors.append(f"{context}: high-priority items must have unresolved_questions populated")
        if not is_non_empty_string(recommended_next_action):
            errors.append(f"{context}: high-priority items must have recommended_next_action populated")

    forbidden_hits = sorted(collect_forbidden_tokens(item))
    if forbidden_hits:
        errors.append(f"{context}: contains forbidden readiness token(s): {forbidden_hits}")


def validate_standards_data() -> dict[str, Any]:
    errors: list[str] = []
    payloads: dict[Path, Any] = {}

    summary: dict[str, Any] = {
        "valid": False,
        "status": "fail",
        "checked_json_files": [repo_relative(path) for path in JSON_INPUT_PATHS],
        "json_file_count": len(JSON_INPUT_PATHS),
        "standard_record_count": 0,
        "draft_skill_count": 0,
        "review_item_count": 0,
        "errors": errors,
    }

    for path in JSON_INPUT_PATHS:
        relative = repo_relative(path)
        if not path.exists():
            errors.append(f"{relative}: file is missing")
            continue
        try:
            payloads[path] = load_json(path)
        except json.JSONDecodeError as error:
            errors.append(f"{relative}: invalid JSON ({error})")
        except OSError as error:
            errors.append(f"{relative}: unable to read file ({error})")

    structured_records = ensure_object_with_list(
        payloads.get(STRUCTURED_STANDARD_3_PATH),
        path=STRUCTURED_STANDARD_3_PATH,
        list_key="substandards",
        errors=errors,
    )
    ensure_object_with_list(
        payloads.get(SUPPLEMENTAL_CROSSWALK_PATH),
        path=SUPPLEMENTAL_CROSSWALK_PATH,
        list_key="crosswalk_records",
        errors=errors,
    )
    skill_mappings = ensure_object_with_list(
        payloads.get(SKILL_MAPPING_DRAFT_PATH),
        path=SKILL_MAPPING_DRAFT_PATH,
        list_key="mappings",
        errors=errors,
    )
    review_items = ensure_object_with_list(
        payloads.get(REVIEW_TRACKING_PATH),
        path=REVIEW_TRACKING_PATH,
        list_key="review_items",
        errors=errors,
    )

    standard_ids = {
        item.get("standard_id")
        for item in structured_records
        if isinstance(item, dict) and is_non_empty_string(item.get("standard_id"))
    }
    draft_skill_ids = {
        item.get("skill_id_draft")
        for item in skill_mappings
        if isinstance(item, dict) and is_non_empty_string(item.get("skill_id_draft"))
    }

    summary["standard_record_count"] = len(standard_ids)
    summary["draft_skill_count"] = len(draft_skill_ids)
    summary["review_item_count"] = len(review_items)

    for index, item in enumerate(review_items):
        validate_review_item(
            item,
            index=index,
            standard_ids=standard_ids,
            draft_skill_ids=draft_skill_ids,
            errors=errors,
        )

    summary["valid"] = not errors
    summary["status"] = "pass" if summary["valid"] else "fail"
    summary["error_count"] = len(errors)
    return summary


def print_summary(summary: dict[str, Any]) -> None:
    status_label = "PASS" if summary["valid"] else "FAIL"
    status_text = "passed" if summary["valid"] else "failed"
    print(f"{status_label}: standards-data validation {status_text}.")
    print(f"checked JSON files: {summary['json_file_count']}")
    print(f"standard records: {summary['standard_record_count']}")
    print(f"draft skill mappings: {summary['draft_skill_count']}")
    print(f"review items: {summary['review_item_count']}")
    print(f"errors: {summary['error_count']}")
    if summary["errors"]:
        print("error details:")
        for error in summary["errors"]:
            print(f"- {error}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Zekelman Standard 3 review-layer data.")
    parser.parse_args(argv)
    summary = validate_standards_data()
    print_summary(summary)
    return 0 if summary["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
