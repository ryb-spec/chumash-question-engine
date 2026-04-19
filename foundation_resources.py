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
)
FOUNDATION_STATUS_VALUES = ("validated_seed",)
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


_RESOURCE_VALIDATORS = {
    "canonical_skill_crosswalk_json": _validate_crosswalk_json,
    "canonical_skill_crosswalk_csv": _validate_crosswalk_csv,
    "assessment_blueprint": _validate_assessment_blueprint,
    "grammar_paradigms": _validate_grammar_paradigms,
    "high_frequency_lexicon": _validate_high_frequency_lexicon,
    "teacher_ops_workflow": _validate_teacher_ops_workflow,
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
