from __future__ import annotations

import json
import os
import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PATH = (
    REPO_ROOT
    / "data"
    / "standards"
    / "zekelman"
    / "reviewed_bank"
    / "standard_3_mvp_reviewed_bank.json"
)

TEST_MODE_ENV_VAR = "STANDARD_3_MVP_TEST_MODE"
TRUTHY_VALUES = {"1", "true", "yes", "on"}
EXPECTED_RECORD_COUNT = 10

REQUIRED_PROTECTED_FIELDS = {
    "reviewed_bank_record_id",
    "standard",
    "standard_id",
    "source_scope",
    "skill_lane",
    "question_type_family",
    "approved_hebrew_input",
    "approved_input_reference",
    "final_prompt",
    "expected_answer",
    "answer_key_rationale",
    "protected_deferred_content_check",
    "review_status",
    "runtime_status",
    "student_facing_status",
    "promotion_source",
}

ALLOWED_STANDARD_IDS = {"3.01", "3.02", "3.05", "3.06", "3.07"}
ALLOWED_RUNTIME_STATUS = "not_runtime_active"
ALLOWED_STUDENT_FACING_STATUS = "not_student_facing"
ALLOWED_REVIEW_STATUS = "reviewed_for_protected_bank"
ALLOWED_SOURCE_SCOPE = "zekelman_standard_3_mvp"
ALLOWED_PROMOTION_SOURCE = "standard_3_mvp_reviewed_bank_candidate_records"

SKILL_BY_LANE = {
    "Nouns / שמות עצם": "standard_3_noun_recognition",
    "Simple Shorashim / שורשים": "standard_3_simple_shoresh",
    "Pronominal Suffix Decoding": "standard_3_pronominal_suffix_decoding",
    "Visible Prefixes / Articles": "standard_3_visible_prefix_article",
    "Foundational Verb Clues": "standard_3_foundational_verb_clues",
}

QUESTION_TYPE_BY_FAMILY = {
    "Hebrew-to-English noun translation": "standard_3_noun_translation",
    "English-to-Hebrew noun recall": "standard_3_noun_recall",
    "Simple shoresh identification": "standard_3_simple_shoresh_identification",
    "Shoresh-to-basic-meaning match": "standard_3_shoresh_basic_meaning",
    "Simple suffix meaning match": "standard_3_pronominal_suffix_meaning",
    "ה הידיעה recognition": "standard_3_article_heh_recognition",
    "Visible prefix recognition": "standard_3_visible_prefix_recognition",
    "Basic tense/person/form clue recognition": "standard_3_foundational_verb_clue",
}

EXCLUDED_STANDARD_IDS = {"3.04", "3.08", "3.10"}
EXCLUDED_APPROVED_INPUTS = {"את"}
EXCLUDED_LANE_MARKERS = {
    "Pronoun Referent Tracking",
    "Nikud",
    "Grouping and Word Order",
    "סמיכות",
}


class Standard3TestModeLoaderError(ValueError):
    """Raised when protected Standard 3 test-mode data is unsafe or malformed."""


def standard_3_test_mode_enabled(env: Mapping[str, str] | None = None) -> bool:
    values = os.environ if env is None else env
    return str(values.get(TEST_MODE_ENV_VAR, "")).strip().lower() in TRUTHY_VALUES


def _records_from_payload(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        records = payload
    elif isinstance(payload, dict) and isinstance(payload.get("records"), list):
        records = payload["records"]
    else:
        raise Standard3TestModeLoaderError(
            "Standard 3 protected bank must be a list or an object with a records list."
        )
    if not all(isinstance(record, dict) for record in records):
        raise Standard3TestModeLoaderError("Every Standard 3 protected bank record must be an object.")
    return list(records)


def load_standard_3_protected_bank(path: str | Path = DEFAULT_PATH) -> list[dict[str, Any]]:
    source_path = Path(path)
    with source_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    records = _records_from_payload(payload)
    if len(records) != EXPECTED_RECORD_COUNT:
        raise Standard3TestModeLoaderError(
            f"Standard 3 protected bank must contain exactly {EXPECTED_RECORD_COUNT} records."
        )
    for record in records:
        validate_standard_3_protected_record(record)
    return records


def validate_standard_3_protected_record(record: dict[str, Any]) -> None:
    missing = sorted(REQUIRED_PROTECTED_FIELDS - set(record))
    if missing:
        raise Standard3TestModeLoaderError(f"Standard 3 protected record is missing fields: {missing}")

    record_id = str(record.get("reviewed_bank_record_id") or "").strip()
    if not record_id:
        raise Standard3TestModeLoaderError("Standard 3 protected record must include reviewed_bank_record_id.")
    if record.get("runtime_status") != ALLOWED_RUNTIME_STATUS:
        raise Standard3TestModeLoaderError(f"{record_id}: runtime_status must be {ALLOWED_RUNTIME_STATUS}.")
    if record.get("student_facing_status") != ALLOWED_STUDENT_FACING_STATUS:
        raise Standard3TestModeLoaderError(
            f"{record_id}: student_facing_status must be {ALLOWED_STUDENT_FACING_STATUS}."
        )
    if record.get("review_status") != ALLOWED_REVIEW_STATUS:
        raise Standard3TestModeLoaderError(f"{record_id}: review_status must be {ALLOWED_REVIEW_STATUS}.")
    if record.get("standard") != "3":
        raise Standard3TestModeLoaderError(f"{record_id}: standard must be 3.")
    if record.get("source_scope") != ALLOWED_SOURCE_SCOPE:
        raise Standard3TestModeLoaderError(f"{record_id}: source_scope must be {ALLOWED_SOURCE_SCOPE}.")
    if record.get("promotion_source") != ALLOWED_PROMOTION_SOURCE:
        raise Standard3TestModeLoaderError(
            f"{record_id}: promotion_source must be {ALLOWED_PROMOTION_SOURCE}."
        )

    standard_id = str(record.get("standard_id") or "").strip()
    if standard_id not in ALLOWED_STANDARD_IDS or standard_id in EXCLUDED_STANDARD_IDS:
        raise Standard3TestModeLoaderError(f"{record_id}: standard_id is not allowed for Standard 3 MVP test mode.")

    lane = str(record.get("skill_lane") or "").strip()
    family = str(record.get("question_type_family") or "").strip()
    if lane not in SKILL_BY_LANE:
        raise Standard3TestModeLoaderError(f"{record_id}: skill_lane is not an approved MVP lane.")
    if family not in QUESTION_TYPE_BY_FAMILY:
        raise Standard3TestModeLoaderError(f"{record_id}: question_type_family is not approved.")
    if any(marker in lane or marker in family for marker in EXCLUDED_LANE_MARKERS):
        raise Standard3TestModeLoaderError(f"{record_id}: excluded lane marker is present.")

    approved_input = str(record.get("approved_hebrew_input") or "").strip()
    if not approved_input or approved_input in EXCLUDED_APPROVED_INPUTS:
        raise Standard3TestModeLoaderError(f"{record_id}: approved_hebrew_input is not allowed.")


def _slug(value: str) -> str:
    rendered = re.sub(r"[^0-9A-Za-z]+", "_", value).strip("_").lower()
    return rendered or "standard_3_mvp"


def _pasuk_ref_payload(record: dict[str, Any]) -> dict[str, str]:
    return {
        "label": "Standard 3 MVP test item",
        "pasuk_id": "standard_3_mvp_test",
        "standard_id": str(record.get("standard_id") or ""),
        "source_scope": ALLOWED_SOURCE_SCOPE,
    }


def transform_standard_3_record_for_test_mode(record: dict[str, Any]) -> dict[str, Any]:
    validate_standard_3_protected_record(record)

    record_id = str(record["reviewed_bank_record_id"])
    skill_lane = str(record["skill_lane"])
    question_type_family = str(record["question_type_family"])
    expected_answer = str(record["expected_answer"])
    approved_input = str(record["approved_hebrew_input"])

    return {
        "reviewed_id": record_id,
        "question": str(record["final_prompt"]),
        "question_text": str(record["final_prompt"]),
        "correct_answer": expected_answer,
        "choices": [],
        "skill": SKILL_BY_LANE[skill_lane],
        "question_type": QUESTION_TYPE_BY_FAMILY[question_type_family],
        "mode": "standard_3_mvp_test_mode",
        "standard": str(record["standard"]),
        "micro_standard": str(record["standard_id"]),
        "difficulty": "mvp_foundational",
        "word": approved_input,
        "selected_word": approved_input,
        "pasuk_id": "standard_3_mvp_test",
        "pasuk_ref": _pasuk_ref_payload(record),
        "review_family": "zekelman_standard_3_mvp",
        "runtime_status": ALLOWED_RUNTIME_STATUS,
        "student_facing_status": ALLOWED_STUDENT_FACING_STATUS,
        "source_record_id": record_id,
        "source_candidate_record_id": record.get("source_candidate_record_id"),
        "source_preview_item_id": record.get("source_preview_item_id"),
        "approved_input_reference": record.get("approved_input_reference"),
        "test_mode_only": True,
        "open_response": True,
        "source": "zekelman_standard_3_mvp_protected_bank",
        "analysis_source": "standard_3_mvp_test_mode_adapter",
        "explanation": str(record.get("answer_key_rationale") or ""),
        "_standard_3_source_scope": ALLOWED_SOURCE_SCOPE,
        "_standard_3_review_status": record.get("review_status"),
        "_standard_3_runtime_status": record.get("runtime_status"),
        "_standard_3_student_facing_status": record.get("student_facing_status"),
        "_protected_deferred_content_check": record.get("protected_deferred_content_check"),
        "_reviewer_notes": record.get("reviewer_notes"),
        "_choice_policy": "open_response_no_distractors",
        "_record_slug": _slug(record_id),
    }


def load_standard_3_test_mode_records(
    env: Mapping[str, str] | None = None,
    path: str | Path = DEFAULT_PATH,
) -> list[dict[str, Any]]:
    if not standard_3_test_mode_enabled(env):
        return []
    records = load_standard_3_protected_bank(path)
    return [transform_standard_3_record_for_test_mode(record) for record in records]
