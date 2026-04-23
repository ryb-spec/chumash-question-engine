from __future__ import annotations

import json
import re
from functools import lru_cache

from assessment_scope import data_path
from torah_parser.word_bank_adapter import normalize_hebrew_key


DIKDUK_FOUNDATIONS_DIR = data_path("foundations", "dikduk")

DIKDUK_SCHEMA_FILENAMES = {
    "skill": "skill.schema.json",
    "rule": "rule.schema.json",
    "morphology_pattern": "morphology_pattern.schema.json",
    "vocabulary_entry": "vocabulary_entry.schema.json",
    "exercise_archetype": "exercise_archetype.schema.json",
    "standards_mapping": "standards_mapping.schema.json",
    "confusion_pattern": "confusion_pattern.schema.json",
}

DIKDUK_COLLECTION_CONFIG = {
    "skills": {
        "filename": "skills.seed.json",
        "schema_name": "skill",
        "id_field": "skill_id",
    },
    "rules": {
        "filename": "rules.seed.json",
        "schema_name": "rule",
        "id_field": "rule_id",
    },
    "morphology_patterns": {
        "filename": "morphology_patterns.seed.json",
        "schema_name": "morphology_pattern",
        "id_field": "pattern_id",
    },
    "vocabulary": {
        "filename": "vocabulary.seed.json",
        "schema_name": "vocabulary_entry",
        "id_field": "vocab_id",
    },
    "exercise_archetypes": {
        "filename": "exercise_archetypes.seed.json",
        "schema_name": "exercise_archetype",
        "id_field": "archetype_id",
    },
    "standards_mappings": {
        "filename": "standards_mappings.seed.json",
        "schema_name": "standards_mapping",
        "id_field": "mapping_id",
    },
    "confusion_patterns": {
        "filename": "confusion_patterns.seed.json",
        "schema_name": "confusion_pattern",
        "id_field": "confusion_pattern_id",
    },
}

UNRESOLVED_CANDIDATES_FILENAME = "unresolved_candidates.json"
DIKDUK_JSON_FILENAMES = tuple(
    list(DIKDUK_SCHEMA_FILENAMES.values())
    + [config["filename"] for config in DIKDUK_COLLECTION_CONFIG.values()]
    + [UNRESOLVED_CANDIDATES_FILENAME]
)
INFERRED_STANDARDS_FRAMEWORK = "inferred_chumash_mastery_framework"
INFERRED_STANDARDS_CONFIDENCE_VALUES = ("inferred_strong", "inferred_tentative")


def _read_json(path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def dikduk_path(*parts):
    return data_path("foundations", "dikduk", *parts)


def dikduk_json_paths():
    return {filename: dikduk_path(filename) for filename in DIKDUK_JSON_FILENAMES}


def dikduk_schema_paths():
    return {
        schema_name: dikduk_path(filename)
        for schema_name, filename in DIKDUK_SCHEMA_FILENAMES.items()
    }


def dikduk_seed_collection_names():
    return tuple(DIKDUK_COLLECTION_CONFIG.keys())


def dikduk_seed_paths():
    return {
        collection_name: dikduk_path(config["filename"])
        for collection_name, config in DIKDUK_COLLECTION_CONFIG.items()
    }


def unresolved_candidates_path():
    return dikduk_path(UNRESOLVED_CANDIDATES_FILENAME)


@lru_cache(maxsize=1)
def load_dikduk_schema_map():
    return {
        schema_name: _read_json(path)
        for schema_name, path in dikduk_schema_paths().items()
    }


@lru_cache(maxsize=1)
def load_dikduk_seed_map():
    return {
        collection_name: _read_json(path)
        for collection_name, path in dikduk_seed_paths().items()
    }


@lru_cache(maxsize=1)
def load_unresolved_candidates():
    return _read_json(unresolved_candidates_path())


@lru_cache(maxsize=1)
def load_validated_dikduk_seed_map():
    errors = validate_dikduk_foundations()
    if errors:
        raise ValueError("\n".join(errors))
    return load_dikduk_seed_map()


@lru_cache(maxsize=1)
def load_dikduk_runtime_bundle():
    seeds = load_validated_dikduk_seed_map()
    skill_map = {
        record["skill_id"]: record
        for record in seeds["skills"]
    }
    rule_map = {
        record["rule_id"]: record
        for record in seeds["rules"]
    }
    pattern_map = {
        record["pattern_id"]: record
        for record in seeds["morphology_patterns"]
    }
    confusion_map = {
        record["confusion_pattern_id"]: record
        for record in seeds["confusion_patterns"]
    }
    vocab_by_normalized = {}
    for record in seeds["vocabulary"]:
        vocab_by_normalized.setdefault(record["normalized_hebrew"], []).append(record)
    return {
        "skills": skill_map,
        "rules": rule_map,
        "patterns": pattern_map,
        "confusions": confusion_map,
        "vocab_by_normalized": vocab_by_normalized,
    }


def _json_type_matches(value, expected_type):
    if expected_type == "object":
        return isinstance(value, dict)
    if expected_type == "array":
        return isinstance(value, list)
    if expected_type == "string":
        return isinstance(value, str)
    if expected_type == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected_type == "boolean":
        return isinstance(value, bool)
    if expected_type == "null":
        return value is None
    raise ValueError(f"Unsupported schema type: {expected_type}")


def _validate_type(value, expected_type, label, errors):
    if isinstance(expected_type, list):
        if not any(_json_type_matches(value, option) for option in expected_type):
            errors.append(f"{label} must match one of {expected_type}.")
            return False
        return True
    if not _json_type_matches(value, expected_type):
        errors.append(f"{label} must be of type '{expected_type}'.")
        return False
    return True


def _validate_schema_node(value, schema, label, errors):
    if not isinstance(schema, dict):
        errors.append(f"{label} schema must be an object.")
        return

    expected_type = schema.get("type")
    if expected_type is not None and not _validate_type(value, expected_type, label, errors):
        return

    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{label} must be one of {schema['enum']}.")

    if value is None:
        return

    if isinstance(value, str) and "pattern" in schema:
        if re.search(schema["pattern"], value) is None:
            errors.append(f"{label} does not match pattern {schema['pattern']!r}.")

    if isinstance(value, int) and not isinstance(value, bool) and "minimum" in schema:
        if value < schema["minimum"]:
            errors.append(f"{label} must be >= {schema['minimum']}.")

    if isinstance(value, list):
        min_items = schema.get("minItems")
        if min_items is not None and len(value) < min_items:
            errors.append(f"{label} must contain at least {min_items} item(s).")
        if schema.get("uniqueItems"):
            seen = set()
            for item in value:
                marker = json.dumps(item, ensure_ascii=False, sort_keys=True)
                if marker in seen:
                    errors.append(f"{label} must not contain duplicate items.")
                    break
                seen.add(marker)
        item_schema = schema.get("items")
        if item_schema is not None:
            for index, item in enumerate(value):
                _validate_schema_node(item, item_schema, f"{label}[{index}]", errors)
        return

    if isinstance(value, dict):
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        for field_name in required:
            if field_name not in value:
                errors.append(f"{label} missing required field '{field_name}'.")
        for field_name, field_value in value.items():
            if field_name not in properties:
                if schema.get("additionalProperties", True) is False:
                    errors.append(f"{label} has unsupported field '{field_name}'.")
                continue
            _validate_schema_node(
                field_value,
                properties[field_name],
                f"{label}.{field_name}",
                errors,
            )


def _validate_top_level_schema(schema_name, schema, errors):
    label = f"{schema_name}.schema"
    if not isinstance(schema, dict):
        errors.append(f"{label} must be a JSON object.")
        return
    if schema.get("type") != "object":
        errors.append(f"{label} must declare top-level type 'object'.")
    if not isinstance(schema.get("properties"), dict):
        errors.append(f"{label} must declare a properties object.")
    if not isinstance(schema.get("required"), list):
        errors.append(f"{label} must declare a required field list.")


def _validate_seed_collection_shape(collection_name, records, errors):
    if not isinstance(records, list):
        errors.append(f"{collection_name} must load as a JSON array.")
        return
    config = DIKDUK_COLLECTION_CONFIG[collection_name]
    id_field = config["id_field"]
    seen_ids = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"{collection_name}[{index}] must be a JSON object.")
            continue
        record_id = record.get(id_field)
        if not record_id:
            errors.append(f"{collection_name}[{index}] missing id field '{id_field}'.")
            continue
        if record_id in seen_ids:
            errors.append(f"{collection_name} contains duplicate id '{record_id}'.")
        else:
            seen_ids.add(record_id)


def _validate_cross_links(seeds, errors):
    skill_ids = {record["skill_id"] for record in seeds["skills"]}
    rule_ids = {record["rule_id"] for record in seeds["rules"]}
    confusion_ids = {
        record["confusion_pattern_id"] for record in seeds["confusion_patterns"]
    }

    for record in seeds["skills"]:
        for prerequisite_id in record["prerequisite_skill_ids"]:
            if prerequisite_id not in skill_ids:
                errors.append(
                    f"skills:{record['skill_id']} references missing prerequisite skill '{prerequisite_id}'."
                )

    for record in seeds["rules"]:
        for confusion_id in record["confusion_pattern_ids"]:
            if confusion_id not in confusion_ids:
                errors.append(
                    f"rules:{record['rule_id']} references missing confusion pattern '{confusion_id}'."
                )

    for record in seeds["morphology_patterns"]:
        for rule_id in record["linked_rule_ids"]:
            if rule_id not in rule_ids:
                errors.append(
                    f"morphology_patterns:{record['pattern_id']} references missing rule '{rule_id}'."
                )

    for record in seeds["vocabulary"]:
        for skill_id in record["linked_skill_ids"]:
            if skill_id not in skill_ids:
                errors.append(
                    f"vocabulary:{record['vocab_id']} references missing skill '{skill_id}'."
                )

    for record in seeds["exercise_archetypes"]:
        for skill_id in record["primary_skill_ids"] + record["secondary_skill_ids"]:
            if skill_id not in skill_ids:
                errors.append(
                    f"exercise_archetypes:{record['archetype_id']} references missing skill '{skill_id}'."
                )

    for record in seeds["standards_mappings"]:
        for skill_id in record["linked_skill_ids"]:
            if skill_id not in skill_ids:
                errors.append(
                    f"standards_mappings:{record['mapping_id']} references missing skill '{skill_id}'."
                )
        for rule_id in record["linked_rule_ids"]:
            if rule_id not in rule_ids:
                errors.append(
                    f"standards_mappings:{record['mapping_id']} references missing rule '{rule_id}'."
                )
        if record["standard_framework"] != INFERRED_STANDARDS_FRAMEWORK:
            errors.append(
                "standards_mappings:"
                f"{record['mapping_id']} must use inferred framework '{INFERRED_STANDARDS_FRAMEWORK}'."
            )
        if record["confidence"] not in INFERRED_STANDARDS_CONFIDENCE_VALUES:
            errors.append(
                "standards_mappings:"
                f"{record['mapping_id']} must keep inferred confidence, found '{record['confidence']}'."
            )

    for record in seeds["confusion_patterns"]:
        for skill_id in record["affected_skill_ids"]:
            if skill_id not in skill_ids:
                errors.append(
                    f"confusion_patterns:{record['confusion_pattern_id']} references missing skill '{skill_id}'."
                )
        for rule_id in record["affected_rule_ids"]:
            if rule_id not in rule_ids:
                errors.append(
                    f"confusion_patterns:{record['confusion_pattern_id']} references missing rule '{rule_id}'."
                )


def _validate_unresolved_candidates(unresolved, errors):
    if not isinstance(unresolved, dict):
        errors.append("unresolved_candidates must be a JSON object.")
        return
    expected_sections = ("rules", "morphology_patterns", "vocabulary", "examples", "standards")
    for section in expected_sections:
        if section not in unresolved:
            errors.append(f"unresolved_candidates missing required section '{section}'.")
        elif not isinstance(unresolved[section], list):
            errors.append(f"unresolved_candidates.{section} must be a list.")


def validate_dikduk_foundations():
    errors = []

    for filename, path in dikduk_json_paths().items():
        if not path.exists():
            errors.append(f"Missing dikduk foundations file: {filename}")

    if errors:
        return errors

    schemas = load_dikduk_schema_map()
    for schema_name, schema in schemas.items():
        _validate_top_level_schema(schema_name, schema, errors)

    seeds = load_dikduk_seed_map()
    for collection_name, records in seeds.items():
        _validate_seed_collection_shape(collection_name, records, errors)
        schema_name = DIKDUK_COLLECTION_CONFIG[collection_name]["schema_name"]
        schema = schemas[schema_name]
        for index, record in enumerate(records):
            _validate_schema_node(record, schema, f"{collection_name}[{index}]", errors)

    unresolved = load_unresolved_candidates()
    _validate_unresolved_candidates(unresolved, errors)

    if not errors:
        _validate_cross_links(seeds, errors)

    return errors


def _entry_part_of_speech(entry):
    raw = str((entry or {}).get("type") or (entry or {}).get("part_of_speech") or "").strip()
    if raw in {"prep", "preposition"}:
        return "preposition"
    if raw in {"particle", "conjunction", "pronoun", "prefix_morpheme", "noun", "verb"}:
        return raw
    return raw


def _entry_prefix_forms(entry):
    forms = []
    for prefix_data in (entry or {}).get("prefixes") or []:
        if not isinstance(prefix_data, dict):
            continue
        form = prefix_data.get("form")
        if form:
            forms.append(form)
    legacy = (entry or {}).get("prefix")
    if legacy:
        forms.append(legacy)
    return [normalize_hebrew_key(form) for form in forms if form]


def _entry_suffix_forms(entry):
    forms = []
    for suffix_data in (entry or {}).get("suffixes") or []:
        if not isinstance(suffix_data, dict):
            continue
        form = suffix_data.get("form")
        if form:
            forms.append(form)
    legacy = (entry or {}).get("suffix")
    if legacy:
        forms.append(legacy)
    return [normalize_hebrew_key(form) for form in forms if form]


def _pattern_matches(pattern_id, token, entry):
    normalized_token = normalize_hebrew_key(token or "")
    part_of_speech = _entry_part_of_speech(entry)
    tense = str((entry or {}).get("tense") or "").strip()
    number = str((entry or {}).get("number") or "").strip()
    prefix_forms = set(_entry_prefix_forms(entry))
    suffix_forms = set(_entry_suffix_forms(entry))

    if pattern_id == "pat_verb_future_tav_ambiguous":
        return (
            part_of_speech == "verb"
            and tense == "future"
            and number in {"", "singular"}
            and normalized_token.startswith(normalize_hebrew_key("ת"))
        )
    if pattern_id == "pat_verb_past_3mp_or_imperative_mp":
        return (
            part_of_speech == "verb"
            and normalized_token.endswith(normalize_hebrew_key("ו"))
            and not prefix_forms
            and not suffix_forms
        )
    if pattern_id == "pat_verb_object_suffix_family":
        return part_of_speech == "verb" and bool(suffix_forms)
    if pattern_id == "pat_noun_poss_2ms_sg":
        return part_of_speech == "noun" and normalize_hebrew_key("ך") in suffix_forms
    if pattern_id == "pat_noun_poss_1cp":
        return part_of_speech == "noun" and normalize_hebrew_key("נו") in suffix_forms
    return False


def dikduk_foundation_metadata(token, entry=None, *, skill=None, question_type=None):
    bundle = load_dikduk_runtime_bundle()
    normalized_token = normalize_hebrew_key(token or "")
    matched_vocab = list(bundle["vocab_by_normalized"].get(normalized_token, []))

    pattern_ids = [
        pattern_id
        for pattern_id in bundle["patterns"]
        if entry and _pattern_matches(pattern_id, token, entry)
    ]
    rule_ids = []
    confusion_ids = []
    for pattern_id in pattern_ids:
        pattern = bundle["patterns"][pattern_id]
        for rule_id in pattern.get("linked_rule_ids") or []:
            if rule_id not in rule_ids:
                rule_ids.append(rule_id)
            for confusion_id in (bundle["rules"].get(rule_id) or {}).get("confusion_pattern_ids") or []:
                if confusion_id not in confusion_ids:
                    confusion_ids.append(confusion_id)

    skill_ids = []
    for vocab in matched_vocab:
        for skill_id in vocab.get("linked_skill_ids") or []:
            if skill_id not in skill_ids:
                skill_ids.append(skill_id)

    part_of_speech = _entry_part_of_speech(entry)
    weak_standalone_translation = any(
        vocab.get("function_vs_content") == "function"
        or vocab.get("part_of_speech") in {
            "particle",
            "pronoun",
            "conjunction",
            "preposition",
            "prefix_morpheme",
        }
        for vocab in matched_vocab
    )
    ambiguous_without_context = any(
        pattern_id in {"pat_verb_future_tav_ambiguous", "pat_verb_past_3mp_or_imperative_mp"}
        for pattern_id in pattern_ids
    )
    if part_of_speech in {"particle", "preposition", "conjunction", "pronoun"}:
        weak_standalone_translation = True

    repeat_key = ""
    shoresh = normalize_hebrew_key((entry or {}).get("shoresh") or "")
    if shoresh:
        repeat_key = f"shoresh:{shoresh}"
    elif matched_vocab:
        repeat_key = f"vocab:{matched_vocab[0]['vocab_id']}"
    elif pattern_ids:
        repeat_key = f"pattern:{pattern_ids[0]}"

    requested_skill = str(skill or question_type or "").strip()
    return {
        "used": bool(matched_vocab or pattern_ids or skill_ids),
        "safe_seed_only": True,
        "requested_skill": requested_skill,
        "vocab_ids": [record["vocab_id"] for record in matched_vocab],
        "skill_ids": skill_ids,
        "pattern_ids": pattern_ids,
        "rule_ids": rule_ids,
        "confusion_pattern_ids": confusion_ids,
        "weak_standalone_translation": bool(weak_standalone_translation),
        "ambiguous_without_context": bool(ambiguous_without_context),
        "repeat_key": repeat_key,
    }
