from __future__ import annotations

import argparse
import json
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "curriculum_extraction"
MANIFEST_PATH = DATA_DIR / "curriculum_extraction_manifest.json"
REGISTRY_PATH = DATA_DIR / "source_resource_registry.json"

COMMON_REQUIRED_FIELDS = (
    "id",
    "schema_version",
    "record_type",
    "extraction_batch_id",
    "source_package_id",
    "source_trace",
    "review_status",
    "runtime_status",
    "confidence",
    "extraction_quality_flags",
)

SOURCE_TRACE_REQUIRED_FIELDS = (
    "source_name",
    "source_file",
    "source_page_start",
    "source_page_end",
    "source_section",
    "source_ref",
    "source_snippet_raw",
    "source_snippet_normalized",
    "extraction_method",
    "extraction_note",
    "source_has_answer_key",
    "review_status",
)

ANSWER_STATUS_VALUES = {
    "source_provided",
    "inferred_needs_review",
    "not_provided",
    "not_extracted",
    "not_applicable",
}

EXPECTED_RECORD_TYPES = {
    "data/curriculum_extraction/samples/pasuk_segments.sample.jsonl": "pasuk_segment",
    "data/curriculum_extraction/samples/word_parse.sample.jsonl": "word_parse",
    "data/curriculum_extraction/samples/word_parse_tasks.sample.jsonl": "word_parse_task",
    "data/curriculum_extraction/samples/vocab_entries.sample.jsonl": "vocab_entry",
    "data/curriculum_extraction/samples/comprehension_questions.sample.jsonl": "comprehension_question",
    "data/curriculum_extraction/samples/question_templates.sample.jsonl": "question_template",
    "data/curriculum_extraction/samples/skill_tags.sample.jsonl": "skill_tag",
    "data/curriculum_extraction/samples/translation_rules.sample.jsonl": "translation_rule",
    "data/curriculum_extraction/normalized/linear_chumash_bereishis_1_1_to_1_5_pasuk_segments.seed.jsonl": "pasuk_segment",
    "data/curriculum_extraction/normalized/linear_chumash_translation_rules.seed.jsonl": "translation_rule",
    "data/curriculum_extraction/normalized/pasuk_coming_to_teach_word_parse.seed.jsonl": "word_parse",
    "data/curriculum_extraction/normalized/bacharach_shemos_prefix_suffix_tasks.seed.jsonl": "word_parse_task",
    "data/curriculum_extraction/normalized/bacharach_vaeira_comprehension_questions.seed.jsonl": "comprehension_question",
    "data/curriculum_extraction/normalized/vocabulary_priority_pack.seed.jsonl": "vocab_entry",
}

PASUK_SEGMENT_REQUIRED_FIELDS = (
    "canonical_ref",
    "sefer",
    "parsha",
    "perek",
    "pasuk",
    "pasuk_range",
    "segment_order",
    "segment_level",
    "hebrew_raw",
    "hebrew_normalized",
    "english_raw",
    "english_normalized",
    "missing_hebrew_flag",
    "missing_translation_flag",
    "translation_type",
    "parenthetical_clarification",
    "translation_rule_tags",
    "source_footnote_refs",
    "skill_tags",
    "linked_vocab_ids",
    "linked_word_parse_ids",
)

WORD_PARSE_REQUIRED_FIELDS = (
    "canonical_ref",
    "sefer",
    "parsha",
    "perek",
    "pasuk",
    "word_in_pasuk_raw",
    "word_in_pasuk_normalized",
    "base_word",
    "target_shoresh_raw",
    "target_shoresh_normalized",
    "shoresh_meaning",
    "prefixes",
    "suffixes",
    "grammar_features",
    "literal_translation",
    "contextual_translation",
    "answer_status",
    "skill_tags",
)

WORD_PARSE_TASK_REQUIRED_FIELDS = (
    "task_type",
    "sefer",
    "parsha",
    "perek",
    "pasuk",
    "pasuk_range",
    "target_shoresh_raw",
    "target_shoresh_normalized",
    "expected_word_in_pasuk",
    "prefixes",
    "suffixes",
    "answer_status",
    "skill_tags",
)

VOCAB_ENTRY_REQUIRED_FIELDS = (
    "hebrew",
    "normalized_hebrew",
    "entry_type",
    "english_glosses",
    "needs_gloss_review",
    "sefer_scope",
    "frequency_source",
    "frequency_band",
    "global_frequency_band",
    "priority_level",
    "skill_tags",
)

COMPREHENSION_REQUIRED_FIELDS = (
    "question_type",
    "sefer",
    "parsha",
    "perek",
    "pasuk",
    "quoted_phrase_raw",
    "question_text",
    "expected_answer",
    "answer_status",
    "skill_tags",
)

QUESTION_TEMPLATE_REQUIRED_FIELDS = (
    "template_key",
    "template_title",
    "question_family",
    "prompt_template",
    "expected_answer_type",
    "supported_record_types",
    "skill_tags",
)

SKILL_TAG_REQUIRED_FIELDS = (
    "skill_key",
    "display_name",
    "category",
    "description",
    "normalized_terms",
    "linked_record_types",
)

TRANSLATION_RULE_REQUIRED_FIELDS = (
    "rule_key",
    "rule_name",
    "applies_to_record_type",
    "trigger_text",
    "guidance",
    "example_source_ref",
    "skill_tags",
)

SAMPLE_ALLOWED_METHODS = {"manual_sample"}
NORMALIZED_ALLOWED_METHODS = {"manual_cleaned_excerpt", "manual_sample"}
ALLOWED_REVIEW_STATUSES = {"needs_review", "reviewed"}

SKILL_TAG_ALIASES = {
    "phrase_translation": {"translation_context", "skill_tag.translation_context"},
    "translation_context": {"translation_context", "skill_tag.translation_context"},
    "word_translation": {"translation_context", "skill_tag.translation_context"},
    "shoresh": {"shoresh_identification", "skill_tag.shoresh_identification"},
    "prefix_suffix": {
        "prefix_meaning",
        "skill_tag.prefix_meaning",
        "suffix_meaning",
        "skill_tag.suffix_meaning",
    },
    "vocabulary": {"vocabulary_priority", "skill_tag.vocabulary_priority"},
    "pasuk_comprehension": {"text_comprehension", "skill_tag.text_comprehension"},
    "al_mi_neemar": {
        "text_comprehension",
        "skill_tag.text_comprehension",
        "phrase_intent",
        "skill_tag.phrase_intent",
    },
    "mi_amar_el_mi": {
        "text_comprehension",
        "skill_tag.text_comprehension",
        "phrase_intent",
        "skill_tag.phrase_intent",
    },
}

ALLOWED_CHANGE_PREFIXES = (
    "data/curriculum_extraction/",
)

ALLOWED_CHANGE_EXACT = {
    "docs/curriculum_extraction_factory.md",
    "docs/curriculum_extraction_integration_plan.md",
    "scripts/validate_curriculum_extraction.py",
    "scripts/load_curriculum_extraction.py",
    "tests/test_curriculum_extraction_schemas.py",
    "tests/test_curriculum_extraction_validation.py",
    "tests/test_curriculum_extraction_loader.py",
    "README_CHROMEBOOK.md",
}

FORBIDDEN_CHANGE_PREFIXES = (
    "streamlit_app.py",
    "runtime/",
    "engine/",
    "assessment_scope.py",
    "data/corpus_manifest.json",
    "data/active_scope_reviewed_questions.json",
    "data/active_scope_gold_annotations.json",
    "data/active_scope_overrides.json",
    "ui/",
    "skill_tracker.py",
    "progress_store.py",
)


def repo_relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path: Path) -> list[dict]:
    records: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                payload = json.loads(stripped)
            except json.JSONDecodeError as error:
                raise ValueError(f"{repo_relative(path)} line {line_number}: invalid JSON ({error})") from error
            if not isinstance(payload, dict):
                raise ValueError(f"{repo_relative(path)} line {line_number}: expected JSON object")
            payload["_meta_source_file"] = repo_relative(path)
            payload["_meta_line_number"] = line_number
            records.append(payload)
    return records


def meaningful_value(value: object) -> bool:
    if value is None:
        return False
    if isinstance(value, bool):
        return True
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, set, dict)):
        return bool(value)
    return True


def require_fields(record: dict, fields: tuple[str, ...], errors: list[str], context: str) -> None:
    for field_name in fields:
        if field_name not in record:
            errors.append(f"{context}: missing required field '{field_name}'")


def validate_declared_files(manifest: dict, key: str, errors: list[str]) -> list[Path]:
    paths: list[Path] = []
    for relative in manifest.get(key, []):
        path = ROOT / relative
        paths.append(path)
        if not path.exists():
            errors.append(f"manifest file missing under {key}: {relative}")
    return paths


def expected_batch_review_status(record: dict, record_origin: str, batch_lookup: dict[str, dict]) -> str:
    batch = batch_lookup.get(str(record.get("extraction_batch_id", "")), {})
    review_status = batch.get("review_status")
    if review_status in ALLOWED_REVIEW_STATUSES:
        return str(review_status)
    return "needs_review" if record_origin == "sample" else "needs_review"


def validate_resource_batches(manifest: dict, errors: list[str]) -> dict[str, dict]:
    batch_lookup: dict[str, dict] = {}
    for batch in manifest.get("resource_batches", []):
        if not isinstance(batch, dict):
            errors.append("curriculum_extraction_manifest.json: each resource batch must be an object")
            continue
        batch_id = batch.get("batch_id")
        if not batch_id:
            errors.append("curriculum_extraction_manifest.json: resource batch missing batch_id")
            continue
        if batch.get("runtime_active") is not False:
            errors.append(f"curriculum_extraction_manifest.json: {batch_id} must have runtime_active=false")
        if batch.get("integration_status") != "not_runtime_active":
            errors.append(f"curriculum_extraction_manifest.json: {batch_id} must have integration_status=not_runtime_active")
        review_status = batch.get("review_status")
        if review_status is not None and review_status not in ALLOWED_REVIEW_STATUSES:
            errors.append(f"curriculum_extraction_manifest.json: {batch_id} has invalid review_status '{review_status}'")
        batch_lookup[str(batch_id)] = batch
    return batch_lookup


def validate_source_trace(
    record: dict,
    errors: list[str],
    context: str,
    *,
    record_origin: str,
    expected_review_status: str,
) -> None:
    source_trace = record.get("source_trace")
    if not isinstance(source_trace, dict):
        errors.append(f"{context}: source_trace must be an object")
        return
    require_fields(source_trace, SOURCE_TRACE_REQUIRED_FIELDS, errors, f"{context} source_trace")

    extraction_method = source_trace.get("extraction_method")
    if record_origin == "sample":
        if extraction_method not in SAMPLE_ALLOWED_METHODS:
            errors.append(
                f"{context}: sample records must use extraction_method in {sorted(SAMPLE_ALLOWED_METHODS)}"
            )
    elif record_origin == "normalized":
        if extraction_method not in NORMALIZED_ALLOWED_METHODS:
            errors.append(
                f"{context}: normalized records must use extraction_method in {sorted(NORMALIZED_ALLOWED_METHODS)}"
            )

    if source_trace.get("review_status") != expected_review_status:
        errors.append(f"{context}: source_trace.review_status must be '{expected_review_status}'")
    page_start = source_trace.get("source_page_start")
    page_end = source_trace.get("source_page_end")
    if isinstance(page_start, int) and isinstance(page_end, int) and page_end < page_start:
        errors.append(f"{context}: source_page_end must be >= source_page_start")


def validate_review_flags(record: dict, errors: list[str], context: str, *, expected_review_status: str) -> None:
    if record.get("review_status") != expected_review_status:
        errors.append(f"{context}: review_status must be '{expected_review_status}'")
    if record.get("runtime_status") != "not_runtime_active":
        errors.append(f"{context}: runtime_status must be 'not_runtime_active'")
    if record.get("confidence") == "high":
        errors.append(f"{context}: confidence must not be 'high'")
    if expected_review_status == "reviewed" and record.get("confidence") == "low":
        errors.append(f"{context}: reviewed records must not stay at low confidence")


def validate_skill_tags(record: dict, valid_skill_refs: set[str], errors: list[str], context: str) -> None:
    skill_tags = record.get("skill_tags", [])
    if skill_tags is None:
        skill_tags = []
    if not isinstance(skill_tags, list):
        errors.append(f"{context}: skill_tags must be a list")
        return
    for skill_tag in skill_tags:
        skill_tag = str(skill_tag)
        if skill_tag in valid_skill_refs:
            continue
        alias_targets = SKILL_TAG_ALIASES.get(skill_tag, set())
        if alias_targets and any(target in valid_skill_refs for target in alias_targets):
            continue
        errors.append(f"{context}: unknown skill tag '{skill_tag}'")


def validate_answer_status(record: dict, answer_fields: tuple[str, ...], errors: list[str], context: str) -> None:
    answer_status = record.get("answer_status")
    if answer_status not in ANSWER_STATUS_VALUES:
        errors.append(f"{context}: invalid answer_status '{answer_status}'")
        return
    if answer_status == "source_provided":
        if not any(meaningful_value(record.get(field_name)) for field_name in answer_fields):
            errors.append(f"{context}: source_provided records need a non-empty answer/translation/parse field")
    if answer_status == "inferred_needs_review" and record.get("review_status") != "needs_review":
        errors.append(f"{context}: inferred_needs_review records must stay needs_review")
    if answer_status in {"not_provided", "not_extracted", "not_applicable"}:
        answer_values = [record.get(field_name) for field_name in answer_fields]
        if any(meaningful_value(value) for value in answer_values):
            errors.append(f"{context}: {answer_status} records must not invent answer content")


def validate_record_type_specific(record: dict, errors: list[str], context: str) -> None:
    record_type = record.get("record_type")
    if record_type == "pasuk_segment":
        require_fields(record, PASUK_SEGMENT_REQUIRED_FIELDS, errors, context)
        for field_name in ("sefer", "perek", "pasuk", "segment_order"):
            if not meaningful_value(record.get(field_name)):
                errors.append(f"{context}: pasuk_segment field '{field_name}' must be populated")
    elif record_type == "word_parse":
        require_fields(record, WORD_PARSE_REQUIRED_FIELDS, errors, context)
        validate_answer_status(
            record,
            (
                "target_shoresh_raw",
                "target_shoresh_normalized",
                "shoresh_meaning",
                "literal_translation",
                "contextual_translation",
                "grammar_features",
            ),
            errors,
            context,
        )
    elif record_type == "word_parse_task":
        require_fields(record, WORD_PARSE_TASK_REQUIRED_FIELDS, errors, context)
        validate_answer_status(
            record,
            (
                "expected_word_in_pasuk",
                "prefixes",
                "suffixes",
            ),
            errors,
            context,
        )
        missing_answer_payload = not any(
            meaningful_value(record.get(field_name))
            for field_name in ("expected_word_in_pasuk", "prefixes", "suffixes")
        )
        if missing_answer_payload and record.get("answer_status") not in {"not_extracted", "not_provided"}:
            errors.append(
                f"{context}: word_parse_task records missing answer content must use not_extracted or not_provided"
            )
    elif record_type == "vocab_entry":
        require_fields(record, VOCAB_ENTRY_REQUIRED_FIELDS, errors, context)
        english_glosses = record.get("english_glosses") or []
        if not english_glosses and record.get("needs_gloss_review") is not True:
            errors.append(f"{context}: vocab entries with empty english_glosses must set needs_gloss_review=true")
    elif record_type == "comprehension_question":
        require_fields(record, COMPREHENSION_REQUIRED_FIELDS, errors, context)
        validate_answer_status(record, ("expected_answer",), errors, context)
    elif record_type == "question_template":
        require_fields(record, QUESTION_TEMPLATE_REQUIRED_FIELDS, errors, context)
    elif record_type == "skill_tag":
        require_fields(record, SKILL_TAG_REQUIRED_FIELDS, errors, context)
    elif record_type == "translation_rule":
        require_fields(record, TRANSLATION_RULE_REQUIRED_FIELDS, errors, context)
    else:
        errors.append(f"{context}: unsupported record_type '{record_type}'")


def validate_registry(registry: dict, errors: list[str]) -> dict[str, dict]:
    packages = registry.get("source_packages")
    if not isinstance(packages, list) or not packages:
        errors.append("source_resource_registry.json: source_packages must be a non-empty list")
        return {}
    registry_lookup: dict[str, dict] = {}
    for package in packages:
        if not isinstance(package, dict):
            errors.append("source_resource_registry.json: each source package must be an object")
            continue
        source_package_id = package.get("source_package_id")
        if not source_package_id:
            errors.append("source_resource_registry.json: source package missing source_package_id")
            continue
        if package.get("runtime_active") is not False:
            errors.append(f"source_resource_registry.json: {source_package_id} must have runtime_active=false")
        registry_lookup[source_package_id] = package
    return registry_lookup


def validate_schema_files(manifest: dict, errors: list[str]) -> list[Path]:
    schema_paths: list[Path] = []
    for relative in manifest.get("schema_files", []):
        schema_path = ROOT / relative
        schema_paths.append(schema_path)
        if not schema_path.exists():
            errors.append(f"manifest schema missing: {relative}")
            continue
        try:
            payload = load_json(schema_path)
        except json.JSONDecodeError as error:
            errors.append(f"{relative}: invalid JSON ({error})")
            continue
        if not isinstance(payload, dict):
            errors.append(f"{relative}: schema must be a JSON object")
    return schema_paths


def collect_records_from_manifest_list(
    manifest: dict,
    key: str,
    errors: list[str],
) -> tuple[dict[str, list[dict]], list[dict]]:
    records_by_file: dict[str, list[dict]] = {}
    all_records: list[dict] = []
    for relative in manifest.get(key, []):
        path = ROOT / relative
        if not path.exists():
            errors.append(f"manifest {key} file missing: {relative}")
            continue
        try:
            records = load_jsonl(path)
        except ValueError as error:
            errors.append(str(error))
            continue
        records_by_file[relative] = records
        all_records.extend(records)
    return records_by_file, all_records


def collect_changed_paths() -> list[str]:
    result = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    paths: list[str] = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        path = path.strip().strip('"').replace("\\", "/")
        if path:
            paths.append(path)
    return paths


def is_allowed_change(path: str) -> bool:
    if path in ALLOWED_CHANGE_EXACT:
        return True
    return any(path.startswith(prefix) for prefix in ALLOWED_CHANGE_PREFIXES)


def forbidden_reason(path: str) -> str:
    for prefix in FORBIDDEN_CHANGE_PREFIXES:
        if path == prefix or path.startswith(prefix):
            return f"forbidden path changed: {path}"
    return f"path outside isolated curriculum extraction allowlist: {path}"


def validate_curriculum_extraction(*, check_git_diff: bool = False) -> dict:
    errors: list[str] = []
    manifest = load_json(MANIFEST_PATH)
    registry = load_json(REGISTRY_PATH)

    if not isinstance(manifest, dict):
        errors.append("curriculum_extraction_manifest.json must be a JSON object")
        manifest = {}
    if not isinstance(registry, dict):
        errors.append("source_resource_registry.json must be a JSON object")
        registry = {}

    if manifest.get("runtime_active") is not False:
        errors.append("curriculum_extraction_manifest.json: runtime_active must be false")
    if manifest.get("integration_status") != "not_runtime_active":
        errors.append("curriculum_extraction_manifest.json: integration_status must be not_runtime_active")

    registry_lookup = validate_registry(registry, errors)
    batch_lookup = validate_resource_batches(manifest, errors)
    schema_paths = validate_schema_files(manifest, errors)
    raw_source_paths = validate_declared_files(manifest, "raw_source_files", errors)
    sample_records_by_file, sample_records = collect_records_from_manifest_list(manifest, "sample_files", errors)
    normalized_records_by_file, normalized_records = collect_records_from_manifest_list(
        manifest,
        "normalized_data_files",
        errors,
    )
    all_records = [*sample_records, *normalized_records]

    seen_ids: set[str] = set()
    valid_skill_refs: set[str] = set()
    for record in sample_records:
        if record.get("record_type") == "skill_tag":
            if record.get("id"):
                valid_skill_refs.add(str(record["id"]))
            if record.get("skill_key"):
                valid_skill_refs.add(str(record["skill_key"]))

    def validate_record_collection(records_by_file: dict[str, list[dict]], record_origin: str) -> None:
        for relative_path, records in records_by_file.items():
            expected_record_type = EXPECTED_RECORD_TYPES.get(relative_path)
            for record in records:
                line_number = record.pop("_meta_line_number", "?")
                source_file = record.pop("_meta_source_file", relative_path)
                context = f"{source_file}:{line_number}"
                expected_review_status = expected_batch_review_status(record, record_origin, batch_lookup)

                require_fields(record, COMMON_REQUIRED_FIELDS, errors, context)
                validate_source_trace(
                    record,
                    errors,
                    context,
                    record_origin=record_origin,
                    expected_review_status=expected_review_status,
                )
                validate_review_flags(record, errors, context, expected_review_status=expected_review_status)

                record_id = record.get("id")
                if record_id in seen_ids:
                    errors.append(f"{context}: duplicate record id '{record_id}'")
                elif record_id:
                    seen_ids.add(str(record_id))

                source_package_id = record.get("source_package_id")
                if source_package_id not in registry_lookup:
                    errors.append(f"{context}: unknown source_package_id '{source_package_id}'")

                record_type = record.get("record_type")
                if expected_record_type and record_type != expected_record_type:
                    errors.append(f"{context}: expected record_type '{expected_record_type}', got '{record_type}'")

                validate_record_type_specific(record, errors, context)
                if record_type != "skill_tag":
                    validate_skill_tags(record, valid_skill_refs, errors, context)

    validate_record_collection(sample_records_by_file, "sample")
    validate_record_collection(normalized_records_by_file, "normalized")

    changed_paths: list[str] = []
    if check_git_diff:
        changed_paths = collect_changed_paths()
        for path in changed_paths:
            if not is_allowed_change(path):
                errors.append(forbidden_reason(path))

    record_counts = Counter(record.get("record_type") for record in all_records if record.get("record_type"))
    review_status_counts = Counter(record.get("review_status") for record in all_records if record.get("review_status"))
    runtime_status_counts = Counter(record.get("runtime_status") for record in all_records if record.get("runtime_status"))
    summary = {
        "valid": not errors,
        "manifest_path": repo_relative(MANIFEST_PATH),
        "registry_path": repo_relative(REGISTRY_PATH),
        "schema_file_count": len(schema_paths),
        "raw_source_file_count": len(raw_source_paths),
        "sample_file_count": len(sample_records_by_file),
        "normalized_file_count": len(normalized_records_by_file),
        "sample_record_count": len(sample_records),
        "normalized_record_count": len(normalized_records),
        "record_count": len(all_records),
        "record_type_counts": dict(sorted(record_counts.items())),
        "review_status_counts": dict(sorted(review_status_counts.items())),
        "runtime_status_counts": dict(sorted(runtime_status_counts.items())),
        "checked_git_diff": check_git_diff,
        "changed_paths": changed_paths,
        "errors": errors,
    }
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the isolated curriculum extraction scaffold.")
    parser.add_argument(
        "--check-git-diff",
        action="store_true",
        help="Fail if changes outside the curriculum extraction allowlist are present.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = validate_curriculum_extraction(check_git_diff=bool(args.check_git_diff))
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
