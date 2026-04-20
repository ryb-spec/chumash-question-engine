from __future__ import annotations

import csv
import json
from functools import lru_cache

from assessment_scope import data_path, resolve_repo_path


FOUNDATIONS_MANIFEST_PATH = data_path("foundations", "manifest.json")
FOUNDATION_LAYER_VALUES = (
    "canonical",
    "benchmark",
    "paradigm",
    "lexicon",
    "teacher_ops",
    "governance",
)
FOUNDATION_STATUS_VALUES = ("validated_seed", "validated_internal")
_MANIFEST_REQUIRED_FIELDS = (
    "resource_name",
    "version",
    "layer",
    "format",
    "path",
    "source",
    "status",
    "intended_use",
)
_CROSSWALK_JSON_REQUIRED_SKILL_FIELDS = (
    "canonical_skill_id",
    "display_name",
    "engine_status",
    "system_layer",
)
_CROSSWALK_CSV_REQUIRED_COLUMNS = (
    "canonical_skill_id",
    "display_name",
    "domain",
    "subdomain",
    "engine_status",
    "system_layer",
)
_CROSSWALK_SYSTEM_LAYER_VALUES = (
    "canonical_truth",
    "benchmark",
    "engine_extension",
    "internal_reviewed_supplement",
)
_ENGINE_EXTENSION_GOVERNANCE_STATUS_VALUES = (
    "proposed",
    "under_review",
    "approved_internal",
    "kept_engine_only",
    "merged",
    "rejected",
)
_ENGINE_EXTENSION_RECOMMENDED_DISPOSITION_VALUES = (
    "keep_engine_extension",
    "promote_reviewed_internal_supplement",
    "merge_into_existing_canonical_skill",
    "rename_for_clarity",
)
_ENGINE_EXTENSION_QUEUE_REQUIRED_FIELDS = (
    "canonical_skill_id",
    "display_name",
    "current_runtime_skills",
    "why_it_exists",
    "nearest_existing_skill_ids",
    "recommended_disposition",
    "governance_status",
    "human_review_needed",
)


def _read_json(path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def _read_csv_rows(path):
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _load_resource_payload(record):
    path = resolve_repo_path(record["path"])
    if record["format"] == "json":
        return _read_json(path)
    if record["format"] == "csv":
        return _read_csv_rows(path)
    raise ValueError(f"Unsupported foundation resource format: {record['format']}")


def _validate_mapping(data, label, errors):
    if not isinstance(data, dict):
        errors.append(f"{label} must be a JSON object.")
        return False
    return True


def _validate_list(value, label, errors):
    if not isinstance(value, list):
        errors.append(f"{label} must be a list.")
        return False
    return True


def _validate_crosswalk_json(data):
    errors = []
    if not _validate_mapping(data, "canonical_skill_crosswalk_json", errors):
        return errors
    if not _validate_mapping(data.get("meta"), "canonical_skill_crosswalk_json.meta", errors):
        return errors
    skills = data.get("skills")
    if not _validate_list(skills, "canonical_skill_crosswalk_json.skills", errors):
        return errors
    seen_ids = set()
    for index, skill in enumerate(skills):
        if not isinstance(skill, dict):
            errors.append(f"canonical_skill_crosswalk_json.skills[{index}] must be an object.")
            continue
        for field in _CROSSWALK_JSON_REQUIRED_SKILL_FIELDS:
            if not skill.get(field):
                errors.append(
                    f"canonical_skill_crosswalk_json.skills[{index}] missing required field '{field}'."
                )
        system_layer = skill.get("system_layer")
        if system_layer and system_layer not in _CROSSWALK_SYSTEM_LAYER_VALUES:
            errors.append(
                "canonical_skill_crosswalk_json.skills"
                f"[{index}] has unsupported system_layer '{system_layer}'."
            )
        canonical_skill_id = skill.get("canonical_skill_id")
        if canonical_skill_id in seen_ids:
            errors.append(f"Duplicate canonical_skill_id in crosswalk JSON: {canonical_skill_id}")
        elif canonical_skill_id:
            seen_ids.add(canonical_skill_id)
    return errors


def _validate_crosswalk_csv(rows):
    errors = []
    if not isinstance(rows, list):
        return ["canonical_skill_crosswalk_csv must load as a row list."]
    if not rows:
        return ["canonical_skill_crosswalk_csv must contain at least one row."]
    columns = set(rows[0].keys())
    for column in _CROSSWALK_CSV_REQUIRED_COLUMNS:
        if column not in columns:
            errors.append(f"canonical_skill_crosswalk_csv missing required column '{column}'.")
    seen_ids = set()
    for index, row in enumerate(rows):
        canonical_skill_id = row.get("canonical_skill_id")
        if not canonical_skill_id:
            errors.append(f"canonical_skill_crosswalk_csv row {index + 1} missing canonical_skill_id.")
            continue
        system_layer = row.get("system_layer")
        if system_layer and system_layer not in _CROSSWALK_SYSTEM_LAYER_VALUES:
            errors.append(
                f"canonical_skill_crosswalk_csv row {index + 1} has unsupported system_layer '{system_layer}'."
            )
        if canonical_skill_id in seen_ids:
            errors.append(f"Duplicate canonical_skill_id in crosswalk CSV: {canonical_skill_id}")
        else:
            seen_ids.add(canonical_skill_id)
    return errors


def _validate_assessment_blueprint(data):
    errors = []
    if not _validate_mapping(data, "assessment_blueprint", errors):
        return errors
    _validate_mapping(data.get("meta"), "assessment_blueprint.meta", errors)
    if not _validate_mapping(
        data.get("external_benchmark"), "assessment_blueprint.external_benchmark", errors
    ):
        return errors
    if not _validate_mapping(
        data.get("recommended_local_blueprint"),
        "assessment_blueprint.recommended_local_blueprint",
        errors,
    ):
        return errors
    _validate_list(
        data["external_benchmark"].get("jsat_section_weights"),
        "assessment_blueprint.external_benchmark.jsat_section_weights",
        errors,
    )
    _validate_list(
        data["recommended_local_blueprint"].get("mvp_focus"),
        "assessment_blueprint.recommended_local_blueprint.mvp_focus",
        errors,
    )
    _validate_list(
        data["recommended_local_blueprint"].get("question_archetypes"),
        "assessment_blueprint.recommended_local_blueprint.question_archetypes",
        errors,
    )
    _validate_list(
        data["recommended_local_blueprint"].get("difficulty_bands"),
        "assessment_blueprint.recommended_local_blueprint.difficulty_bands",
        errors,
    )
    return errors


def _validate_grammar_paradigms(data):
    errors = []
    if not _validate_mapping(data, "grammar_paradigms", errors):
        return errors
    _validate_mapping(data.get("meta"), "grammar_paradigms.meta", errors)
    for field in (
        "subject_pronouns",
        "object_pronouns",
        "possessive_pronouns",
        "verb_paradigm_example",
    ):
        _validate_mapping(data.get(field), f"grammar_paradigms.{field}", errors)
    _validate_list(data.get("instructional_uses"), "grammar_paradigms.instructional_uses", errors)
    return errors


def _validate_high_frequency_lexicon(data):
    errors = []
    if not _validate_mapping(data, "high_frequency_lexicon", errors):
        return errors
    _validate_mapping(data.get("meta"), "high_frequency_lexicon.meta", errors)
    _validate_list(data.get("priority_tiers"), "high_frequency_lexicon.priority_tiers", errors)
    _validate_list(data.get("seed_entries"), "high_frequency_lexicon.seed_entries", errors)
    _validate_list(
        data.get("recommended_engine_fields"),
        "high_frequency_lexicon.recommended_engine_fields",
        errors,
    )
    return errors


def _validate_teacher_ops_workflow(data):
    errors = []
    if not _validate_mapping(data, "teacher_ops_workflow", errors):
        return errors
    _validate_mapping(data.get("meta"), "teacher_ops_workflow.meta", errors)
    _validate_list(data.get("readiness_criteria"), "teacher_ops_workflow.readiness_criteria", errors)
    _validate_list(data.get("deployment_cycle"), "teacher_ops_workflow.deployment_cycle", errors)
    _validate_mapping(
        data.get("system_outputs_to_support_teachers"),
        "teacher_ops_workflow.system_outputs_to_support_teachers",
        errors,
    )
    return errors


def _validate_engine_extension_review_queue(data):
    errors = []
    if not _validate_mapping(data, "engine_extension_review_queue", errors):
        return errors
    metadata = data.get("metadata")
    records = data.get("records")
    if not _validate_mapping(metadata, "engine_extension_review_queue.metadata", errors):
        return errors
    if not _validate_list(records, "engine_extension_review_queue.records", errors):
        return errors

    status_values = tuple(metadata.get("governance_status_values") or ())
    disposition_values = tuple(metadata.get("recommended_disposition_values") or ())
    if status_values != _ENGINE_EXTENSION_GOVERNANCE_STATUS_VALUES:
        errors.append(
            "engine_extension_review_queue.metadata.governance_status_values must match the supported governance status model."
        )
    if disposition_values != _ENGINE_EXTENSION_RECOMMENDED_DISPOSITION_VALUES:
        errors.append(
            "engine_extension_review_queue.metadata.recommended_disposition_values must match the supported disposition model."
        )

    seen_ids = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"engine_extension_review_queue.records[{index}] must be an object.")
            continue
        for field in _ENGINE_EXTENSION_QUEUE_REQUIRED_FIELDS:
            if field not in record:
                errors.append(
                    f"engine_extension_review_queue.records[{index}] missing required field '{field}'."
                )
        canonical_skill_id = record.get("canonical_skill_id")
        if canonical_skill_id in seen_ids:
            errors.append(
                f"Duplicate canonical_skill_id in engine_extension_review_queue: {canonical_skill_id}"
            )
        elif canonical_skill_id:
            seen_ids.add(canonical_skill_id)
        if not isinstance(record.get("current_runtime_skills"), list):
            errors.append(
                f"engine_extension_review_queue.records[{index}].current_runtime_skills must be a list."
            )
        if not isinstance(record.get("nearest_existing_skill_ids"), list):
            errors.append(
                f"engine_extension_review_queue.records[{index}].nearest_existing_skill_ids must be a list."
            )
        if not isinstance(record.get("human_review_needed"), bool):
            errors.append(
                f"engine_extension_review_queue.records[{index}].human_review_needed must be a boolean."
            )
        governance_status = record.get("governance_status")
        if governance_status and governance_status not in _ENGINE_EXTENSION_GOVERNANCE_STATUS_VALUES:
            errors.append(
                "engine_extension_review_queue.records"
                f"[{index}] has unsupported governance_status '{governance_status}'."
            )
        recommended_disposition = record.get("recommended_disposition")
        if (
            recommended_disposition
            and recommended_disposition not in _ENGINE_EXTENSION_RECOMMENDED_DISPOSITION_VALUES
        ):
            errors.append(
                "engine_extension_review_queue.records"
                f"[{index}] has unsupported recommended_disposition '{recommended_disposition}'."
            )
    return errors


_RESOURCE_VALIDATORS = {
    "canonical_skill_crosswalk_json": _validate_crosswalk_json,
    "canonical_skill_crosswalk_csv": _validate_crosswalk_csv,
    "assessment_blueprint": _validate_assessment_blueprint,
    "grammar_paradigms": _validate_grammar_paradigms,
    "high_frequency_lexicon": _validate_high_frequency_lexicon,
    "teacher_ops_workflow": _validate_teacher_ops_workflow,
    "engine_extension_review_queue": _validate_engine_extension_review_queue,
}


def validate_foundation_manifest(manifest=None):
    manifest = manifest or _read_json(FOUNDATIONS_MANIFEST_PATH)
    errors = []
    if not _validate_mapping(manifest, "foundation manifest", errors):
        return errors
    metadata = manifest.get("metadata")
    resources = manifest.get("resources")
    if not _validate_mapping(metadata, "foundation manifest.metadata", errors):
        return errors
    if not _validate_list(resources, "foundation manifest.resources", errors):
        return errors

    seen_names = set()
    loaded_payloads = {}
    for index, record in enumerate(resources):
        if not isinstance(record, dict):
            errors.append(f"foundation manifest.resources[{index}] must be an object.")
            continue
        for field in _MANIFEST_REQUIRED_FIELDS:
            if not record.get(field):
                errors.append(f"foundation manifest.resources[{index}] missing '{field}'.")
        resource_name = record.get("resource_name")
        if resource_name in seen_names:
            errors.append(f"Duplicate foundation resource_name: {resource_name}")
        elif resource_name:
            seen_names.add(resource_name)

        if record.get("layer") not in FOUNDATION_LAYER_VALUES:
            errors.append(
                f"{resource_name or f'foundation manifest.resources[{index}]'} has unsupported layer '{record.get('layer')}'."
            )
        if record.get("status") not in FOUNDATION_STATUS_VALUES:
            errors.append(
                f"{resource_name or f'foundation manifest.resources[{index}]'} has unsupported status '{record.get('status')}'."
            )
        if record.get("format") not in {"json", "csv"}:
            errors.append(
                f"{resource_name or f'foundation manifest.resources[{index}]'} has unsupported format '{record.get('format')}'."
            )

        for path_field in ("path", "source"):
            path_value = record.get(path_field)
            if path_value and not resolve_repo_path(path_value).exists():
                errors.append(
                    f"{resource_name or f'foundation manifest.resources[{index}]'} missing {path_field} file: {path_value}"
                )

        if resource_name in _RESOURCE_VALIDATORS and not errors:
            payload = _load_resource_payload(record)
            loaded_payloads[resource_name] = payload
            errors.extend(
                f"{resource_name}: {message}"
                for message in _RESOURCE_VALIDATORS[resource_name](payload)
            )

    crosswalk_json = loaded_payloads.get("canonical_skill_crosswalk_json")
    crosswalk_csv = loaded_payloads.get("canonical_skill_crosswalk_csv")
    engine_extension_queue = loaded_payloads.get("engine_extension_review_queue")
    if crosswalk_json is not None and crosswalk_csv is not None:
        json_ids = {
            skill.get("canonical_skill_id")
            for skill in crosswalk_json.get("skills", [])
            if isinstance(skill, dict)
        }
        csv_ids = {
            row.get("canonical_skill_id")
            for row in crosswalk_csv
            if isinstance(row, dict)
        }
        if json_ids != csv_ids:
            errors.append("canonical_skill_crosswalk_json and canonical_skill_crosswalk_csv disagree on canonical_skill_id membership.")

    if crosswalk_json is not None and engine_extension_queue is not None:
        crosswalk_engine_extension_ids = {
            skill.get("canonical_skill_id")
            for skill in crosswalk_json.get("skills", [])
            if isinstance(skill, dict) and skill.get("system_layer") == "engine_extension"
        }
        governed_ids = {
            record.get("canonical_skill_id")
            for record in engine_extension_queue.get("records", [])
            if isinstance(record, dict)
        }
        if crosswalk_engine_extension_ids != governed_ids:
            errors.append(
                "canonical_skill_crosswalk_json engine_extension ids and engine_extension_review_queue ids disagree."
            )

    return errors


@lru_cache(maxsize=1)
def load_foundation_manifest():
    manifest = _read_json(FOUNDATIONS_MANIFEST_PATH)
    errors = validate_foundation_manifest(manifest)
    if errors:
        raise ValueError("\n".join(errors))
    return manifest


def foundation_resource_records():
    return tuple(load_foundation_manifest().get("resources", []))


@lru_cache(maxsize=1)
def foundation_resource_map():
    return {
        record["resource_name"]: dict(record)
        for record in foundation_resource_records()
    }


def foundation_resource_names():
    return tuple(foundation_resource_map().keys())


def get_foundation_resource_metadata(resource_name):
    return dict(foundation_resource_map()[resource_name])


def foundation_resource_path(resource_name):
    return resolve_repo_path(get_foundation_resource_metadata(resource_name)["path"])


def load_foundation_resource(resource_name):
    record = get_foundation_resource_metadata(resource_name)
    payload = _load_resource_payload(record)
    validator = _RESOURCE_VALIDATORS.get(resource_name)
    if validator:
        errors = validator(payload)
        if errors:
            raise ValueError(
                "\n".join(f"{resource_name}: {message}" for message in errors)
            )
    return payload


def validate_all_foundation_resources():
    validation = {}
    manifest = load_foundation_manifest()
    for record in manifest.get("resources", []):
        resource_name = record["resource_name"]
        payload = _load_resource_payload(record)
        validator = _RESOURCE_VALIDATORS.get(resource_name)
        validation[resource_name] = [] if validator is None else validator(payload)
    return validation
