"""Stable question and target identity helpers for runtime exposure checks."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping


QUESTION_ID_KEYS = ("question_id", "id", "reviewed_id")
SOURCE_ID_KEYS = ("source_candidate_id",)
PASUK_REF_KEYS = ("pasuk_ref", "ref")
HEBREW_TARGET_KEYS = ("hebrew_target", "selected_word", "target", "word")
SKILL_KEYS = ("skill", "skill_id", "canonical_skill_id", "standard")
QUESTION_TYPE_KEYS = ("question_type", "prompt_family", "mode")
PROMPT_KEYS = ("question", "question_text", "prompt")
MODE_KEYS = ("mode", "practice_type")


def _value_from(candidate, key):
    if isinstance(candidate, Mapping):
        return candidate.get(key)
    return getattr(candidate, key, None)


def _first_present(candidate, keys):
    for key in keys:
        value = _value_from(candidate, key)
        if value not in (None, ""):
            return value
    return None


def normalize_text(value):
    if value is None:
        return ""
    if isinstance(value, Mapping):
        if value.get("label"):
            return normalize_text(value.get("label"))
        if {"sefer", "perek", "pasuk"} & set(value):
            return " ".join(
                normalize_text(value.get(key))
                for key in ("sefer", "perek", "pasuk")
                if value.get(key) not in (None, "")
            )
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    if isinstance(value, (list, tuple)):
        return "|".join(normalize_text(item) for item in value if item not in (None, ""))
    return " ".join(str(value).strip().split())


def stable_hash(*parts, length=16):
    clean_parts = [normalize_text(part) for part in parts if normalize_text(part)]
    if not clean_parts:
        return ""
    payload = "|".join(clean_parts)
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()[:length]


def build_question_identity(candidate):
    candidate = candidate or {}
    question_id = normalize_text(_first_present(candidate, QUESTION_ID_KEYS))
    source_candidate_id = normalize_text(_first_present(candidate, SOURCE_ID_KEYS))
    pasuk_ref = normalize_text(_first_present(candidate, PASUK_REF_KEYS))
    hebrew_target = normalize_text(_first_present(candidate, HEBREW_TARGET_KEYS))
    skill = normalize_text(_first_present(candidate, SKILL_KEYS))
    question_type = normalize_text(_first_present(candidate, QUESTION_TYPE_KEYS))
    prompt = normalize_text(_first_present(candidate, PROMPT_KEYS))
    mode = normalize_text(_first_present(candidate, MODE_KEYS))

    return {
        "question_id": question_id,
        "source_candidate_id": source_candidate_id,
        "pasuk_ref": pasuk_ref,
        "hebrew_target": hebrew_target,
        "skill": skill,
        "question_type": question_type,
        "prompt": prompt,
        "mode": mode,
    }


def build_question_signatures(candidate):
    identity = build_question_identity(candidate)
    exact_basis = (
        identity["question_id"]
        or stable_hash(
            identity["source_candidate_id"],
            identity["pasuk_ref"],
            identity["hebrew_target"],
            identity["skill"],
            identity["question_type"],
            identity["prompt"],
        )
    )
    target_basis = identity["source_candidate_id"] or identity["hebrew_target"]
    pasuk_skill_basis = stable_hash(identity["pasuk_ref"], identity["skill"])
    skill_type_basis = stable_hash(identity["skill"], identity["question_type"])

    return {
        **identity,
        "exact_question_signature": exact_basis,
        "target_signature": target_basis,
        "pasuk_skill_signature": pasuk_skill_basis,
        "skill_type_signature": skill_type_basis,
    }
