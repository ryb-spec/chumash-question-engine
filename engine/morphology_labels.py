from __future__ import annotations

from torah_parser.word_bank_adapter import normalize_hebrew_key


STUDENT_TENSE_LABELS = {
    "vav_consecutive_past": "past",
    "future_jussive": "future",
    "future": "future",
    "past": "past",
    "present": "present",
    "infinitive": "to do form",
}
COHORT_TAUGHT_TENSE_LABELS = (
    "past",
    "future",
    "present",
    "to do form",
)
LEGACY_TENSE_LABELS = {
    "vav_consecutive_past": "past narrative",
    "future_jussive": "short future form",
    "infinitive": "infinitive",
}
CANONICAL_TENSE_ALIASES = {
    "vav_consecutive_past": "vav_consecutive_past",
    "past narrative": "vav_consecutive_past",
    "future_jussive": "future_jussive",
    "short future form": "future_jussive",
    "future": "future",
    "past": "past",
    "present": "present",
    "infinitive": "infinitive",
    "to do form": "infinitive",
    "command": "command",
}
BASE_CONJUGATION_BY_CODE = {
    "vav_consecutive_past": "converted_imperfect",
    "future_jussive": "imperfect",
    "future": "imperfect",
    "past": "perfect",
    "present": "participle",
    "infinitive": "infinitive",
    "command": "imperative",
}


def clean_tense_value(value):
    text = str(value or "").strip()
    return text or None


def canonical_tense_code(value):
    text = clean_tense_value(value)
    if text is None:
        return None
    return CANONICAL_TENSE_ALIASES.get(text, text)


def student_tense_label(value):
    code = canonical_tense_code(value)
    if code is None:
        return None
    return STUDENT_TENSE_LABELS.get(code, code)


def _has_leading_vav(token):
    normalized = normalize_hebrew_key(token or "")
    return normalized.startswith("ו")


def classify_tense_form(value, *, token=""):
    raw_code = canonical_tense_code(value)
    if raw_code is None:
        return {
            "raw_code": None,
            "base_conjugation": "",
            "vav_prefix_type": "",
            "displayed_label": None,
            "display_phrase": "",
            "accepted_answer_aliases": [],
        }

    displayed_label = student_tense_label(raw_code)
    if raw_code == "future_jussive":
        display_phrase = "a future-style form"
    elif raw_code == "vav_consecutive_past":
        display_phrase = "a past-style form"
    elif displayed_label == "to do form":
        display_phrase = "the 'to do' form"
    else:
        display_phrase = f"the {displayed_label} form"

    if raw_code == "vav_consecutive_past":
        vav_prefix_type = "consecutive"
    elif _has_leading_vav(token) and raw_code in {"future_jussive", "future"}:
        vav_prefix_type = "conjunction"
    else:
        vav_prefix_type = ""

    aliases = []
    for item in (
        displayed_label,
        raw_code,
        LEGACY_TENSE_LABELS.get(raw_code),
    ):
        if item and item not in aliases:
            aliases.append(item)

    return {
        "raw_code": raw_code,
        "base_conjugation": BASE_CONJUGATION_BY_CODE.get(raw_code, ""),
        "vav_prefix_type": vav_prefix_type,
        "displayed_label": displayed_label,
        "display_phrase": display_phrase,
        "accepted_answer_aliases": aliases,
    }

