import re
from collections import Counter
from copy import deepcopy
from difflib import SequenceMatcher
from functools import lru_cache
from time import perf_counter

import streamlit as st

from adaptive_engine import candidate_weight
from assessment_scope import (
    active_pasuk_texts,
    active_pasuk_record_for_question,
    active_scope_summary,
    bind_question_to_active_scope,
)
from pasuk_flow_generator import (
    analyze_pasuk as validate_analyze_pasuk,
    canonical_tense_code as question_canonical_tense_code,
    entry_type as question_entry_type,
    is_placeholder_translation,
    part_of_speech_target_supported as question_part_of_speech_target_supported,
    runtime_tense_label as question_runtime_tense_label,
    standalone_translation_target as question_standalone_translation_target,
    student_part_of_speech_label as question_student_part_of_speech_label,
    usable_translation as question_usable_translation,
    validate_question_candidate as validate_generated_question_candidate,
)
from progress_store import load_progress_state
from runtime.presentation import SKILL_ORDER
from runtime.runtime_support import (
    analyze_generator_pasuk,
    generate_skill_question,
    get_active_pasuk_ref,
    get_pasukh_text,
    load_progress,
    question_pipeline_source,
)
from torah_parser.word_bank_adapter import normalize_hebrew_key


DEBUG_REJECTION_LABELS = {
    "active_scope_unmapped": "active scope mapping blocked",
    "pasuk_ref_mismatch": "pasuk reference mismatch blocked",
    "displayed_pasuk_mismatch": "displayed pasuk mismatch blocked",
    "target_not_in_bound_pasuk": "target not in bound pasuk blocked",
    "incompatible_skill_target": "incompatible skill target blocked",
    "low_confidence_target_analysis": "low-confidence target analysis blocked",
    "invalid_tense_target": "invalid tense target blocked",
    "invalid_prefix_target": "invalid prefix target blocked",
    "invalid_suffix_target": "invalid suffix target blocked",
    "invalid_shoresh_target": "invalid shoresh target blocked",
    "invalid_part_of_speech_target": "invalid part-of-speech target blocked",
    "duplicate_distractors": "duplicate distractors blocked",
    "ambiguous_answer_key": "ambiguous answer key blocked",
    "explanation_target_conflict": "explanation metadata conflict blocked",
    "followup_generation_error": "follow-up generation error",
    "followup_returned_none": "follow-up returned no question",
    "followup_skipped": "follow-up skipped",
    "repeated_followup_candidate": "repeated follow-up rejected",
    "generation_error": "question generation error",
    "generator_returned_none": "generator returned no question",
    "generator_skipped": "generator skipped candidate",
    "feature_repeat_blocked": "feature repetition blocked",
    "morpheme_family_repeat_blocked": "morpheme-family repetition blocked",
    "opening_mechanical_group_capped": "opening mechanical cap blocked",
    "mechanical_group_cooldown_blocked": "mechanical cooldown blocked",
    "prefix_repeat_blocked": "prefix repetition blocked",
    "recent_exact_repeat": "recent exact repeat blocked",
    "recent_target_repeat": "recent target repeat blocked",
    "recent_prompt_repeat": "recent prompt repeat blocked",
    "tense_followup_continue_blocked": "tense follow-up held for broader variety",
    "tense_family_short_run_capped": "tense-family short-run cap blocked",
    "grammar_taxonomy_short_run_capped": "grammar-taxonomy short-run cap blocked",
    "same_skill_short_run_saturated": "same skill short-run saturation rebalanced",
    "recent_exact_word_repeat": "recent exact-word repeat blocked",
    "recent_same_pasuk_intent_repeat": "same pasuk intent repeat blocked",
    "recent_semantic_sibling_repeat": "semantic sibling repeat blocked",
    "recent_target_family_repeat": "recent target-family repeat blocked",
    "recent_translation_phrase_pattern_repeat": "translation phrase-pattern repeat blocked",
    "recent_meaning_repeat": "recent meaning repeat blocked",
    "recent_tense_lane_overlap": "tense-lane overlap blocked",
    "recent_surface_pattern_repeat": "recent surface-pattern repeat blocked",
    "limited_candidate_reuse": "limited candidate reuse allowed",
    "explicit_reteach_reuse": "explicit reteach reuse allowed",
    "diversity_redirect": "diversity redirect selected a different safe lane",
}
RECENT_QUESTION_HISTORY_LIMIT = 20
EXACT_REPEAT_WINDOW = 8
NEAR_REPEAT_WINDOW = 5
EXACT_WORD_REPEAT_WINDOW = 4
TRANSLATION_EXACT_WORD_REPEAT_WINDOW = 10
TRANSLATION_PHRASE_PATTERN_WINDOW = 5
DUPLICATE_FEEL_WINDOW = 8
TENSE_LANE_OVERLAP_WINDOW = 6
SHORESH_SURFACE_WINDOW = 4
HEBREW_WORD_RE = re.compile(r"[\u0590-\u05ff]+")
MORPHOLOGY_SKILLS = {
    "identify_prefix_meaning",
    "identify_suffix_meaning",
    "identify_pronoun_suffix",
    "identify_tense",
    "identify_prefix_future",
    "identify_suffix_past",
    "identify_present_pattern",
    "segment_word_parts",
    "shoresh",
    "prefix",
    "suffix",
    "verb_tense",
}
TENSE_FAMILY_SKILLS = {
    "identify_tense",
    "verb_tense",
}
GRAMMAR_TAXONOMY_SKILLS = TENSE_FAMILY_SKILLS | {
    "part_of_speech",
}
COMPACT_CONTEXT_QUESTION_TYPES = {
    "word_meaning",
    "translation",
    "shoresh",
    "prefix",
    "suffix",
    "prefix_suffix",
    "verb_tense",
}
FULL_CONTEXT_QUESTION_TYPES = {
    "subject_identification",
    "phrase_meaning",
    "phrase_translation",
    "flow",
    "flow_dependency",
    "role_clarity",
}
OPENING_MECHANICAL_SKILLS = {
    "identify_prefix_meaning",
    "identify_suffix_meaning",
    "identify_pronoun_suffix",
    "identify_verb_marker",
    "segment_word_parts",
}
SEQUENCING_GROUP_SKILLS = {
    "mechanical": [
        "identify_prefix_meaning",
        "identify_suffix_meaning",
        "identify_pronoun_suffix",
        "identify_verb_marker",
        "segment_word_parts",
        "prefix",
        "suffix",
    ],
    "meaning": [
        "translation",
        "shoresh",
        "part_of_speech",
        "preposition_meaning",
    ],
    "verb_building": [
        "verb_tense",
        "identify_tense",
        "identify_prefix_future",
        "identify_suffix_past",
        "identify_present_pattern",
        "match_pronoun_to_verb",
        "convert_future_to_command",
    ],
    "context": [
        "phrase_translation",
        "subject_identification",
        "object_identification",
    ],
}
LEARN_MODE_SEQUENCE_WINDOW = 10
MAX_SEQUENCE_SKILL_ATTEMPTS = 6
MAX_SEQUENCE_SKILLS_PER_GROUP = 2
MAX_FULL_GENERATION_ROWS_PER_PASS = 8
SHORT_RUN_TENSE_WINDOW = 10
SHORT_RUN_TENSE_CAP = 3
SHORT_RUN_SAME_SKILL_CAP = 3
LOW_VARIETY_MECHANICAL_WINDOW = 4
LOW_VARIETY_MECHANICAL_REPEAT_CAP = 2
TOKEN_ANALYSIS_SKILLS = {
    "identify_prefix_meaning",
    "prefix",
    "identify_suffix_meaning",
    "identify_pronoun_suffix",
    "suffix",
    "shoresh",
    "verb_tense",
    "identify_tense",
    "translation",
    "part_of_speech",
}
GENERATOR_VALIDATION_REASON_CODE_MAP = {
    "identify_prefix_meaning": {
        "invalid": {"no_clear_prefix", "multiple_prefixes", "prefix_answer_mismatch", "prefix_meaning_mismatch"},
        "ambiguous": {"prefix_distractor_leak"},
        "low_confidence": {"compound_morphology"},
        "invalid_code": "invalid_prefix_target",
    },
    "identify_suffix_meaning": {
        "invalid": {
            "no_clear_suffix",
            "multiple_suffixes",
            "suffix_answer_mismatch",
            "suffix_meaning_mismatch",
            "context_dependent_suffix",
            "lexical_plural_ending",
        },
        "ambiguous": {"suffix_distractor_leak"},
        "low_confidence": {"compound_morphology"},
        "invalid_code": "invalid_suffix_target",
    },
    "shoresh": {
        "invalid": {"no_clear_shoresh", "shoresh_not_supported", "shoresh_answer_mismatch"},
        "ambiguous": {"shoresh_distractor_leak"},
        "low_confidence": {"compound_morphology"},
        "invalid_code": "invalid_shoresh_target",
    },
    "verb_tense": {
        "invalid": {"no_clear_tense", "tense_not_supported", "tense_answer_mismatch"},
        "ambiguous": {"tense_distractor_leak"},
        "low_confidence": {"compound_morphology"},
        "invalid_code": "invalid_tense_target",
    },
}


def attach_debug_trace(question, **updates):
    if question is None:
        return None

    trace = dict(question.get("_debug_trace") or {})
    for key, value in updates.items():
        if value is None:
            continue
        trace[key] = value
    question["_debug_trace"] = trace
    return question


def timed_question_generation(callback):
    started_at = perf_counter()
    question = callback()
    elapsed_ms = round((perf_counter() - started_at) * 1000, 1)
    return question, elapsed_ms


def answer_to_next_ready_ms():
    started_at = st.session_state.get("last_answer_submitted_at")
    if not started_at:
        return None
    return round((perf_counter() - started_at) * 1000, 1)


@lru_cache(maxsize=256)
def _cached_candidate_source(analyzer, pasuk):
    if analyzer is None:
        return pasuk
    return analyzer(pasuk)


def candidate_source_for_pasuk(pasuk):
    analyzer = analyze_generator_pasuk
    if analyzer is None:
        return pasuk
    return deepcopy(_cached_candidate_source(analyzer, pasuk))


def progress_source_label(progress):
    return "reused" if progress is not None else "reloaded"


def increment_debug_rejection_count(counts, code, amount=1):
    updated = dict(counts or {})
    updated[code] = updated.get(code, 0) + amount
    return updated


def _signature_text(value):
    if not value:
        return ""
    text = normalize_hebrew_key(str(value))
    text = re.sub(r"\s+", " ", text).strip()
    return text.lower()


def question_prompt_family(question):
    family = question.get("question_format") or question.get("question_type")
    if family:
        return str(family)

    prompt = HEBREW_WORD_RE.sub("<hebrew>", question.get("question", "").lower())
    prompt = re.sub(r"[^a-z0-9_<>\s]+", " ", prompt)
    return re.sub(r"\s+", " ", prompt).strip()


def question_target_family(question):
    target = _signature_text(question.get("selected_word") or question.get("word") or "")
    if not target:
        return ""
    if " " in target:
        return target

    family = target
    if len(family) > 3 and family.startswith("ו"):
        family = family[1:]
    if len(family) > 3 and family.startswith(("ה", "ל", "מ", "ב", "כ", "ש")):
        family = family[1:]
    return family or target


def question_repeat_family(question):
    key = question_type_key(question)
    skill = question.get("skill") or ""

    if key in TENSE_FAMILY_SKILLS or skill in TENSE_FAMILY_SKILLS:
        return "tense_family"
    if key in {"translation", "word_meaning"} or skill in {"translation", "word_meaning"}:
        return "translation"
    if key == "shoresh" or skill == "shoresh":
        return "shoresh"
    if key.startswith("prefix_level_") or key in {"identify_prefix_meaning", "prefix"} or skill in {
        "identify_prefix_meaning",
        "prefix",
    }:
        return "prefix_family"
    return skill or key


def question_meaning_key(question):
    if question_repeat_family(question) != "translation":
        return ""

    meaning = _signature_text(question.get("correct_answer") or "")
    if not meaning:
        return ""
    if meaning in {"god", "g-d", "the lord", "the lord god"}:
        return meaning
    return re.sub(r"^(the|a|an)\s+", "", meaning, count=1)


def question_concept_key(question):
    repeat_family = question_repeat_family(question)
    if repeat_family == "translation":
        return question_meaning_key(question) or question_target_family(question)
    if repeat_family == "shoresh":
        return _signature_text(question.get("correct_answer") or "")
    if repeat_family == "tense_family":
        target_family = question_target_family(question)
        answer = _signature_text(question.get("correct_answer") or "")
        if target_family and answer:
            return f"{target_family}|{answer}"
    return ""


def question_surface_pattern(question):
    repeat_family = question_repeat_family(question)
    target = _signature_text(question.get("selected_word") or question.get("word") or "")
    if not target:
        return ""

    if repeat_family == "shoresh":
        if target.startswith("וי"):
            return "vav_yod_surface"
        if target.startswith("ות"):
            return "vav_tav_surface"
        if target.startswith("ו"):
            return "vav_led_surface"
        return "plain_surface"
    return ""


def _answer_text_profile(answer):
    normalized = _signature_text(answer)
    words = normalized.split()
    if normalized.startswith("and the lord god "):
        leading = "and_the_lord_god"
    elif normalized.startswith("and the lord "):
        leading = "and_the_lord"
    elif normalized.startswith("and god "):
        leading = "and_god"
    elif normalized.startswith("and he "):
        leading = "and_he"
    elif normalized.startswith("and she "):
        leading = "and_she"
    elif normalized.startswith("and it "):
        leading = "and_it"
    elif normalized.startswith("and they "):
        leading = "and_they"
    elif normalized.startswith("to "):
        leading = "to_form"
    elif normalized in {"him", "her", "them", "me", "us", "you", "someone else", "something else"}:
        leading = "pronoun"
    elif words[:1] and words[0] in {"the", "a", "an"}:
        leading = "article_noun"
    elif len(words) == 1:
        leading = "single_word"
    else:
        leading = words[0] if words else ""

    relation = ""
    for prefix in ("from", "to", "in", "on", "with"):
        if normalized.startswith(f"{prefix} "):
            relation = prefix
            break

    return {
        "leading": leading,
        "relation": relation,
        "word_count": min(len(words), 4),
    }


def question_answer_pattern(question):
    question = question or {}
    question_type = question_type_key(question)
    profile = _answer_text_profile(question.get("correct_answer") or "")
    parts = [question_type]
    part_of_speech = _signature_text(question.get("part_of_speech") or "")
    role_focus = _signature_text(question.get("role_focus") or question.get("morpheme_type") or "")
    if part_of_speech:
        parts.append(part_of_speech)
    if role_focus:
        parts.append(role_focus)
    if profile["leading"]:
        parts.append(profile["leading"])
    if profile["relation"]:
        parts.append(f"rel:{profile['relation']}")
    parts.append(f"words:{profile['word_count']}")
    return "|".join(parts)


def question_signature(question):
    question = question or {}
    pasuk = question.get("pasuk") or ""
    foundation = dict(question.get("dikduk_foundation") or {})
    foundation_repeat_key = foundation.get("repeat_key") or ""

    return {
        "skill": question.get("skill") or question.get("question_type") or "",
        "repeat_family": question_repeat_family(question),
        "question_type": question_type_key(question),
        "target_word": _signature_text(question.get("selected_word") or question.get("word") or ""),
        "target_family": foundation_repeat_key or question_target_family(question),
        "prompt_family": question_prompt_family(question),
        "correct_answer": _signature_text(question.get("correct_answer") or ""),
        "meaning_key": question_meaning_key(question),
        "concept_key": question_concept_key(question),
        "answer_pattern": question_answer_pattern(question),
        "surface_pattern": question_surface_pattern(question),
        "source_pasuk": _signature_text(get_active_pasuk_ref(pasuk) if pasuk else ""),
        "prefix_letter": _signature_text(question.get("prefix") or ""),
        "foundation_repeat_key": foundation_repeat_key,
    }


def _recent_translation_phrase_question_count(recent_questions, *, window=NEAR_REPEAT_WINDOW):
    recent_questions = list(recent_questions or [])
    return sum(
        1
        for item in recent_questions[-window:]
        if (item or {}).get("skill") == "translation"
        and (item or {}).get("question_type") == "phrase_translation"
    )


def translation_practice_route_bonus(question, recent_questions=None):
    question = question or {}
    if str(question.get("skill") or "").strip() != "translation":
        return 0.0

    question_type = question_type_key(question)
    analysis_source = str(question.get("analysis_source") or "").strip()
    if analysis_source != "active_scope_reviewed_bank":
        return 0.0

    if question_type == "translation":
        return 1.25

    if question_type == "phrase_translation":
        bonus = -0.75
        if _recent_translation_phrase_question_count(recent_questions):
            bonus -= 0.5
        return bonus

    return 0.0


def translation_practice_ready_row_bonus(row, *, requested_skill="", recent_questions=None):
    if str(requested_skill or "").strip() != "translation":
        return 0.0

    row = row or {}
    question_type = str(row.get("question_type") or "").strip()
    analysis_source = str(row.get("analysis_source") or "").strip()
    reviewed = bool(row.get("reviewed")) or analysis_source == "active_scope_reviewed_bank"
    if not reviewed:
        return 0.0

    if question_type == "translation":
        return 1.25

    if question_type == "phrase_translation":
        bonus = -0.75
        if _recent_translation_phrase_question_count(recent_questions):
            bonus -= 0.5
        return bonus

    return 0.0


def reviewed_translation_row_can_rotate(row, *, requested_skill=""):
    row = row or {}
    if str(requested_skill or "").strip() != "translation":
        return False
    if str(row.get("question_type") or "").strip() != "translation":
        return False
    analysis_source = str(row.get("analysis_source") or "").strip()
    reviewed = bool(row.get("reviewed")) or analysis_source == "active_scope_reviewed_bank"
    return reviewed and analysis_source == "active_scope_reviewed_bank"


def recent_question_signature_key(signature):
    signature = signature or {}
    return "|".join(
        [
            signature.get("repeat_family", "") or signature.get("skill", ""),
            signature.get("target_word", ""),
            signature.get("prompt_family", ""),
            signature.get("correct_answer", ""),
            signature.get("source_pasuk", ""),
        ]
    )


def recent_question_repeat_reason(question, recent_questions):
    signature = question_signature(question)
    if not signature["skill"]:
        return ""

    recent_questions = list(recent_questions or [])
    repeat_family = signature.get("repeat_family") or signature["skill"]
    exact_window = recent_questions[-EXACT_REPEAT_WINDOW:]
    exact_key = recent_question_signature_key(signature)
    if any(recent_question_signature_key(item) == exact_key for item in exact_window):
        return "recent_exact_repeat"

    near_window = recent_questions[-NEAR_REPEAT_WINDOW:]
    for previous in near_window:
        previous_family = previous.get("repeat_family") or previous.get("skill")
        if previous_family != repeat_family:
            continue
        if previous.get("target_word") and previous.get("target_word") == signature["target_word"]:
            return "recent_target_repeat"
        if (
            repeat_family == "translation"
            and previous.get("meaning_key")
            and previous.get("meaning_key") == signature.get("meaning_key")
        ):
            return "recent_meaning_repeat"
        if (
            previous.get("prompt_family")
            and previous.get("prompt_family") == signature["prompt_family"]
            and previous.get("correct_answer")
            and previous.get("correct_answer") == signature["correct_answer"]
            and previous.get("source_pasuk")
            and previous.get("source_pasuk") == signature["source_pasuk"]
        ):
            return "recent_prompt_repeat"
        if (
            previous.get("question_type") == signature["question_type"]
            and previous.get("source_pasuk")
            and previous.get("source_pasuk") == signature["source_pasuk"]
            and previous.get("prompt_family") == signature["prompt_family"]
            and previous.get("answer_pattern") == signature["answer_pattern"]
        ):
            return "recent_same_pasuk_intent_repeat"
        if (
            previous.get("concept_key")
            and previous.get("concept_key") == signature.get("concept_key")
            and previous.get("target_word") != signature["target_word"]
        ):
            return "recent_target_family_repeat"
        if (
            previous.get("foundation_repeat_key")
            and previous.get("foundation_repeat_key") == signature.get("foundation_repeat_key")
            and previous.get("target_word") != signature["target_word"]
        ):
            return "recent_target_family_repeat"

    if repeat_family == "tense_family":
        for previous in recent_questions[-TENSE_LANE_OVERLAP_WINDOW:]:
            previous_family = previous.get("repeat_family") or previous.get("skill")
            if previous_family != "tense_family":
                continue
            if previous.get("question_type") == signature["question_type"]:
                continue
            if previous.get("target_family") and previous.get("target_family") == signature["target_family"]:
                return "recent_tense_lane_overlap"

    if repeat_family == "shoresh" and signature.get("surface_pattern") in {
        "vav_yod_surface",
        "vav_tav_surface",
        "vav_led_surface",
    }:
        for previous in recent_questions[-SHORESH_SURFACE_WINDOW:]:
            previous_family = previous.get("repeat_family") or previous.get("skill")
            if previous_family != "shoresh":
                continue
            if previous.get("surface_pattern") == signature["surface_pattern"]:
                return "recent_surface_pattern_repeat"

    previous = recent_questions[-1] if recent_questions else {}
    if previous:
        if (
            (previous.get("repeat_family") or previous.get("skill")) == repeat_family
            and previous.get("target_family")
            and previous.get("target_family") == signature["target_family"]
            and previous.get("target_word") != signature["target_word"]
        ):
            return "recent_semantic_sibling_repeat"

    if (
        signature.get("skill") == "translation"
        and signature.get("question_type") == "phrase_translation"
    ):
        for previous in recent_questions[-TRANSLATION_PHRASE_PATTERN_WINDOW:]:
            if previous.get("skill") != "translation":
                continue
            if previous.get("question_type") != "phrase_translation":
                continue
            if previous.get("answer_pattern") and previous.get("answer_pattern") == signature.get("answer_pattern"):
                return "recent_translation_phrase_pattern_repeat"

    if signature.get("target_word"):
        exact_word_window_size = EXACT_WORD_REPEAT_WINDOW
        if repeat_family == "translation":
            exact_word_window_size = max(
                exact_word_window_size,
                TRANSLATION_EXACT_WORD_REPEAT_WINDOW,
            )
        exact_word_window = recent_questions[-exact_word_window_size:]
        if any(previous.get("target_word") == signature["target_word"] for previous in exact_word_window):
            return "recent_exact_word_repeat"

    return ""


def remember_recent_question(question):
    signature = question_signature(question)
    if not any(signature.values()):
        return

    recent_questions = st.session_state.setdefault("recent_questions", [])
    if recent_questions and recent_question_signature_key(recent_questions[-1]) == recent_question_signature_key(signature):
        return

    recent_questions.append(signature)
    st.session_state.recent_questions = recent_questions[-RECENT_QUESTION_HISTORY_LIMIT:]


def is_explicit_reteach_mode(adaptive_context=None):
    return (adaptive_context or {}).get("selection_mode") == "reteach"


def choice_similarity(left, right):
    return SequenceMatcher(None, _signature_text(left), _signature_text(right)).ratio()


def distractor_separation_score(question):
    choices = list(question.get("choices") or [])
    correct = question.get("correct_answer") or ""
    distractors = [choice for choice in choices if choice != correct]
    if not distractors:
        return 0.0

    similarity_penalty = 0.0
    for distractor in distractors:
        similarity_penalty += choice_similarity(correct, distractor)

    average_similarity = similarity_penalty / len(distractors)
    return round(max(0.0, 2.0 - average_similarity * 2.0), 2)


def question_type_key(question):
    return question.get("question_type") or question.get("skill") or ""


def _hebrew_text_signature(value):
    if not value:
        return ""
    return re.sub(r"\s+", " ", normalize_hebrew_key(str(value))).strip()


def _has_hebrew_text(value):
    return bool(HEBREW_WORD_RE.search(str(value or "")))


def _choice_signature(value):
    return _signature_text(value)


def _normalized_choice_counts(choices):
    counts = Counter()
    for choice in choices or []:
        key = _choice_signature(choice)
        if key:
            counts[key] += 1
    return counts


def _question_validation_skill(question):
    key = question_type_key(question)
    skill = question.get("skill") or ""
    if key.startswith("prefix_level_") or skill in {"identify_prefix_meaning", "prefix"}:
        return "identify_prefix_meaning"
    if key in {"identify_suffix_meaning", "identify_pronoun_suffix", "suffix"} or skill in {
        "identify_suffix_meaning",
        "identify_pronoun_suffix",
        "suffix",
    }:
        return "identify_suffix_meaning"
    if key in {"translation", "word_meaning", "phrase_translation"} or skill in {
        "translation",
        "word_meaning",
        "phrase_translation",
    }:
        return "translation"
    if key in {"verb_tense", "identify_tense"} or skill in {"verb_tense", "identify_tense"}:
        return "verb_tense"
    if key == "shoresh" or skill == "shoresh":
        return "shoresh"
    return ""


def _question_requires_target_analysis(question):
    key = question_type_key(question)
    skill = question.get("skill") or ""
    if key == "phrase_translation":
        return False
    return key in TOKEN_ANALYSIS_SKILLS or skill in TOKEN_ANALYSIS_SKILLS or key.startswith("prefix_level_")


def _question_requires_bound_target(question):
    return bool(question.get("selected_word") or question.get("word"))


def _analysis_items_for_pasuk(pasuk_text):
    if not pasuk_text:
        return []
    try:
        regenerated = validate_analyze_pasuk(pasuk_text)
    except Exception:
        return []
    return regenerated if isinstance(regenerated, list) else []


def _analysis_entries_for_item(item):
    entries = []
    if isinstance((item or {}).get("entry"), dict):
        entries.append(item["entry"])
    for analysis in (item or {}).get("analyses") or []:
        if isinstance(analysis, dict):
            entries.append(analysis)
    return entries


def _entry_type_for_validation(entry):
    if not entry:
        return ""
    try:
        return question_entry_type(entry)
    except Exception:
        return str((entry or {}).get("part_of_speech") or (entry or {}).get("type") or "").strip()


def _preferred_analysis_entry(item):
    entries = _analysis_entries_for_item(item)
    if not entries:
        return {}
    for entry in entries:
        if entry.get("confidence") == "generated_alternate":
            continue
        if (
            _entry_type_for_validation(entry) not in {"", "unknown"}
            or entry.get("tense")
            or entry.get("shoresh")
            or entry.get("prefixes")
            or entry.get("suffixes")
        ):
            return dict(entry)
    for entry in entries:
        if entry.get("confidence") != "generated_alternate":
            return dict(entry)
    return dict(entries[0])


def _match_analysis_item(analyzed_items, target_text):
    target_key = _hebrew_text_signature(target_text)
    if not target_key:
        return None

    for item in analyzed_items or []:
        token = item.get("token") or item.get("word") or item.get("surface") or ""
        if _hebrew_text_signature(token) == target_key:
            return {
                "token": token,
                "entry": _preferred_analysis_entry(item),
                "analyses": _analysis_entries_for_item(item),
            }
        for analysis in _analysis_entries_for_item(item):
            surface = analysis.get("surface") or analysis.get("word") or ""
            if _hebrew_text_signature(surface) == target_key:
                return {
                    "token": token or surface,
                    "entry": dict(analysis),
                    "analyses": _analysis_entries_for_item(item),
                }
    return None


def _target_present_in_bound_pasuk(target_text, bound_pasuk_text):
    target_key = _hebrew_text_signature(target_text)
    bound_key = _hebrew_text_signature(bound_pasuk_text)
    return bool(target_key and bound_key and target_key in bound_key)


def _choice_entries_for_question(question, analyzed_items):
    entries = {}
    for choice in question.get("choices") or []:
        match = _match_analysis_item(analyzed_items, choice)
        if match and match.get("entry"):
            entries[choice] = match["entry"]
    return entries or None


def _pasuk_ref_matches_record(original_question, record):
    if not record:
        return True

    expected_ref = record.get("ref") or {}
    expected_pasuk_id = record.get("pasuk_id")
    embedded_ref = original_question.get("pasuk_ref") or {}
    explicit_ids = [
        original_question.get("pasuk_id"),
        original_question.get("override_pasuk_id"),
        embedded_ref.get("pasuk_id"),
    ]
    for explicit_id in explicit_ids:
        if explicit_id and explicit_id != expected_pasuk_id:
            return False

    if embedded_ref.get("sefer") and embedded_ref.get("sefer") != expected_ref.get("sefer"):
        return False
    if embedded_ref.get("perek") and embedded_ref.get("perek") != expected_ref.get("perek"):
        return False
    if embedded_ref.get("pasuk") and embedded_ref.get("pasuk") != expected_ref.get("pasuk"):
        return False

    label = embedded_ref.get("label")
    expected_label = f"{expected_ref.get('sefer')} {expected_ref.get('perek')}:{expected_ref.get('pasuk')}"
    if label and label != expected_label:
        return False
    return True


def _lane_validation_codes(validation_skill, generator_result):
    if not generator_result or generator_result.get("valid", True):
        return []

    reason_codes = set(generator_result.get("reason_codes") or [])
    mapping = GENERATOR_VALIDATION_REASON_CODE_MAP.get(validation_skill) or {}
    mapped = []
    invalid_code = mapping.get("invalid_code")
    if invalid_code and reason_codes.intersection(mapping.get("invalid", set())):
        mapped.append(invalid_code)
    if reason_codes.intersection(mapping.get("low_confidence", set())):
        mapped.append("low_confidence_target_analysis")
    if reason_codes.intersection(mapping.get("ambiguous", set())):
        mapped.append("ambiguous_answer_key")
    if not mapped:
        mapped.append("incompatible_skill_target")
    return mapped


def _validate_part_of_speech_target(question, target_item):
    if not target_item or not target_item.get("entry"):
        return ["invalid_part_of_speech_target"]

    entry = target_item["entry"]
    token = target_item.get("token") or question.get("selected_word") or question.get("word")
    entry_type = _entry_type_for_validation(entry)
    if entry_type not in {"noun", "verb"}:
        return ["invalid_part_of_speech_target"]

    if entry.get("confidence") == "generated_alternate":
        return ["low_confidence_target_analysis", "invalid_part_of_speech_target"]
    if not question_part_of_speech_target_supported(entry, token):
        return ["invalid_part_of_speech_target"]

    expected_label = question_student_part_of_speech_label(entry_type)
    actual_label = question_student_part_of_speech_label(question.get("correct_answer"))
    codes = []
    if _choice_signature(actual_label) != _choice_signature(expected_label):
        codes.append("invalid_part_of_speech_target")

    metadata_label = question.get("part_of_speech")
    if metadata_label and _choice_signature(question_student_part_of_speech_label(metadata_label)) != _choice_signature(expected_label):
        codes.append("explanation_target_conflict")

    return codes


def _structured_affix_forms(entry, key):
    forms = []
    for value in (entry or {}).get(key) or []:
        if not isinstance(value, dict):
            continue
        form = value.get("form")
        if form:
            forms.append(form)
    return forms


def _fallback_question_translation_gloss(question, entry, token):
    question = question or {}
    gloss = str(question.get("word_gloss") or question.get("correct_answer") or "").strip()
    if not gloss or _has_hebrew_text(gloss):
        return None

    if _choice_signature(question.get("correct_answer")) != _choice_signature(gloss):
        return None

    part_of_speech = str(question.get("part_of_speech") or _entry_type_for_validation(entry) or "").strip()
    if part_of_speech == "verb" or question.get("tense") or question.get("tense_code"):
        return None

    if (entry or {}).get("entity_type") == "grammatical_particle":
        return None

    prefix_forms = _structured_affix_forms(entry, "prefixes")
    suffix_forms = _structured_affix_forms(entry, "suffixes")
    legacy_prefix = question.get("prefix") or (entry or {}).get("prefix")
    legacy_suffix = question.get("suffix") or (entry or {}).get("suffix")
    if not prefix_forms and legacy_prefix:
        prefix_forms = [legacy_prefix]
    if not suffix_forms and legacy_suffix:
        suffix_forms = [legacy_suffix]

    prefix_forms = [form for form in prefix_forms if form]
    suffix_forms = [form for form in suffix_forms if form]

    if len(prefix_forms) > 1 or suffix_forms:
        return None

    if prefix_forms and _hebrew_text_signature(prefix_forms[0]) == _hebrew_text_signature("ו"):
        return None

    if normalize_hebrew_key((entry or {}).get("shoresh") or "") == normalize_hebrew_key("היה") and token:
        return None

    return gloss


def _validate_translation_target(question, target_item):
    if not target_item or not target_item.get("entry"):
        return ["incompatible_skill_target"]

    entry = target_item["entry"]
    token = target_item["token"]
    codes = []
    if entry.get("confidence") == "generated_alternate":
        codes.append("low_confidence_target_analysis")

    expected_translation = question_usable_translation(entry, token)
    if not expected_translation:
        expected_translation = _fallback_question_translation_gloss(question, entry, token)
        if not expected_translation:
            codes.append("incompatible_skill_target")
            return list(dict.fromkeys(codes))
    elif not question_standalone_translation_target(entry, token):
        codes.append("incompatible_skill_target")
        return list(dict.fromkeys(codes))

    if _choice_signature(question.get("correct_answer")) != _choice_signature(expected_translation):
        codes.append("incompatible_skill_target")

    metadata_gloss = question.get("word_gloss")
    if metadata_gloss and _choice_signature(metadata_gloss) != _choice_signature(expected_translation):
        codes.append("explanation_target_conflict")

    return list(dict.fromkeys(codes))


def _validate_phrase_translation_question(question):
    target_text = question.get("selected_word") or question.get("word") or ""
    correct_answer = question.get("correct_answer") or ""
    if not target_text or not correct_answer:
        return ["incompatible_skill_target"]

    codes = []
    if is_placeholder_translation(correct_answer, target_text):
        codes.append("incompatible_skill_target")

    metadata_gloss = question.get("word_gloss")
    if metadata_gloss:
        answer_signature = _choice_signature(correct_answer)
        gloss_signature = _choice_signature(metadata_gloss)
        bare_answer_signature = _choice_signature(re.sub(r"^and\s+", "", str(correct_answer), flags=re.IGNORECASE))
        if gloss_signature not in {answer_signature, bare_answer_signature}:
            codes.append("explanation_target_conflict")

    return list(dict.fromkeys(codes))


def _validate_lane_target(question, target_item, analyzed_items):
    validation_skill = _question_validation_skill(question)
    if validation_skill:
        if validation_skill == "translation" and question_type_key(question) == "phrase_translation":
            return _validate_phrase_translation_question(question)
        if validation_skill == "translation":
            return _validate_translation_target(question, target_item)
        if not target_item or not target_item.get("entry"):
            invalid_code = GENERATOR_VALIDATION_REASON_CODE_MAP.get(validation_skill, {}).get("invalid_code")
            return [invalid_code or "incompatible_skill_target"]
        correct_answer = question.get("correct_answer")
        choices = list(question.get("choices") or [])
        if validation_skill == "verb_tense":
            correct_answer = question_canonical_tense_code(question.get("tense_code") or correct_answer)
            choices = [
                code
                for code in (
                    question_canonical_tense_code(choice)
                    for choice in choices
                )
                if code
            ]
        generator_result = validate_generated_question_candidate(
            validation_skill,
            target_item["token"],
            target_item["entry"],
            correct_answer=correct_answer,
            choices=choices,
            choice_entries=_choice_entries_for_question(question, analyzed_items),
        )
        codes = _lane_validation_codes(validation_skill, generator_result)
        entry = target_item["entry"]
        if entry.get("confidence") == "generated_alternate" and "low_confidence_target_analysis" not in codes:
            codes.append("low_confidence_target_analysis")
        if validation_skill == "identify_prefix_meaning":
            expected_prefix = ((entry.get("prefixes") or [{}])[0] or {}).get("form") or entry.get("prefix")
            expected_meaning = ((entry.get("prefixes") or [{}])[0] or {}).get("translation") or entry.get("prefix_meaning")
            if question.get("prefix") and _hebrew_text_signature(question.get("prefix")) != _hebrew_text_signature(expected_prefix):
                codes.extend(["invalid_prefix_target", "explanation_target_conflict"])
            if question.get("prefix_meaning") and _choice_signature(question.get("prefix_meaning")) != _choice_signature(expected_meaning):
                codes.extend(["invalid_prefix_target", "explanation_target_conflict"])
        elif validation_skill == "identify_suffix_meaning":
            expected_suffix = ((entry.get("suffixes") or [{}])[0] or {}).get("form") or entry.get("suffix")
            expected_meaning = ((entry.get("suffixes") or [{}])[0] or {}).get("translation") or entry.get("suffix_meaning")
            if question.get("suffix") and _hebrew_text_signature(question.get("suffix")) != _hebrew_text_signature(expected_suffix):
                codes.extend(["invalid_suffix_target", "explanation_target_conflict"])
            if question.get("suffix_meaning") and _choice_signature(question.get("suffix_meaning")) != _choice_signature(expected_meaning):
                codes.extend(["invalid_suffix_target", "explanation_target_conflict"])
        elif validation_skill == "shoresh":
            if question.get("shoresh") and _hebrew_text_signature(question.get("shoresh")) != _hebrew_text_signature(target_item["entry"].get("shoresh")):
                codes.extend(["invalid_shoresh_target", "explanation_target_conflict"])
        elif validation_skill == "verb_tense":
            expected_code = question_runtime_tense_label(target_item["entry"], target_item["token"])
            if question.get("tense_code") and question_canonical_tense_code(question.get("tense_code")) != expected_code:
                codes.extend(["invalid_tense_target", "explanation_target_conflict"])
            if question.get("tense") and question_canonical_tense_code(question.get("tense")) != expected_code:
                codes.extend(["invalid_tense_target", "explanation_target_conflict"])
        return list(dict.fromkeys(codes))

    key = question_type_key(question)
    skill = question.get("skill") or ""
    if key == "part_of_speech" or skill == "part_of_speech":
        return _validate_part_of_speech_target(question, target_item)
    if key == "translation" or skill == "translation":
        return _validate_translation_target(question, target_item)
    return []


def validation_failure_message(validation):
    codes = list(validation.get("rejection_codes") or [])
    if not codes:
        return "A candidate was blocked by pre-serve validation."
    labels = [DEBUG_REJECTION_LABELS.get(code, code.replace("_", " ")) for code in codes]
    return f"Blocked pre-serve: {'; '.join(labels)}."


def validate_question_for_serve(
    question,
    *,
    fallback_text="",
    validation_path="runtime",
    trusted_active_scope=None,
    expected_bound_record=None,
):
    candidate = deepcopy(question or {})
    original = deepcopy(question or {})
    rejection_codes = []
    trusted_scope = (
        trusted_active_scope_selection_enabled()
        if trusted_active_scope is None
        else bool(trusted_active_scope)
    )

    bound_record = active_pasuk_record_for_question(candidate, fallback_text=fallback_text)
    if trusted_scope and not bound_record:
        rejection_codes.append("active_scope_unmapped")
    if (
        bound_record
        and expected_bound_record
        and bound_record.get("pasuk_id") != expected_bound_record.get("pasuk_id")
    ):
        rejection_codes.append("pasuk_ref_mismatch")
    if bound_record and not _pasuk_ref_matches_record(original, bound_record):
        rejection_codes.append("pasuk_ref_mismatch")

    if bound_record:
        bind_question_to_active_scope(candidate, fallback_text=fallback_text)
        if _hebrew_text_signature(candidate.get("pasuk")) != _hebrew_text_signature(bound_record.get("text")):
            rejection_codes.append("displayed_pasuk_mismatch")

    bound_pasuk_text = (bound_record or {}).get("text") or candidate.get("pasuk") or fallback_text or ""
    choices = list(candidate.get("choices") or [])
    correct_answer = candidate.get("correct_answer")
    choice_counts = _normalized_choice_counts(choices)
    correct_key = _choice_signature(correct_answer)

    question_type = question_type_key(candidate)
    requires_four_choices = bool(candidate.get("skill") or question_type or choices)
    if requires_four_choices:
        min_choices = 4 if question_type.startswith("prefix_level_") else 4
        if len(choices) < min_choices:
            rejection_codes.append("ambiguous_answer_key")
        if not correct_key or correct_key not in choice_counts:
            rejection_codes.append("ambiguous_answer_key")

    if any(count > 1 for count in choice_counts.values()):
        rejection_codes.append("duplicate_distractors")
    if correct_key and choice_counts.get(correct_key, 0) > 1:
        rejection_codes.append("ambiguous_answer_key")

    analyzed_items = _analysis_items_for_pasuk(bound_pasuk_text)
    target_text = candidate.get("selected_word") or candidate.get("word") or ""
    has_bound_hebrew = _has_hebrew_text(bound_pasuk_text)
    has_target_hebrew = _has_hebrew_text(target_text)
    if (
        _question_requires_bound_target(candidate)
        and has_target_hebrew
        and has_bound_hebrew
        and not _target_present_in_bound_pasuk(target_text, bound_pasuk_text)
    ):
        rejection_codes.append("target_not_in_bound_pasuk")

    target_item = _match_analysis_item(analyzed_items, target_text)
    if (
        _question_requires_target_analysis(candidate)
        and has_target_hebrew
        and has_bound_hebrew
        and not target_item
    ):
        rejection_codes.append("target_not_in_bound_pasuk")

    if has_target_hebrew and has_bound_hebrew:
        rejection_codes.extend(_validate_lane_target(candidate, target_item, analyzed_items))
    rejection_codes = list(dict.fromkeys(code for code in rejection_codes if code))

    if not rejection_codes:
        attach_debug_trace(
            candidate,
            pre_serve_validation_passed=True,
            pre_serve_validation_path=validation_path,
            pre_serve_validation_codes=[],
        )
    return {
        "valid": not rejection_codes,
        "question": candidate,
        "bound_record": bound_record,
        "target_item": target_item,
        "rejection_codes": rejection_codes,
        "validation_path": validation_path,
    }


def display_context_policy(question, flow=None):
    if flow is not None:
        return {"mode": "full", "reason": "pasuk_flow"}

    key = question_type_key(question)
    skill = question.get("skill") or ""

    if key in FULL_CONTEXT_QUESTION_TYPES or skill in {
        "subject_identification",
        "object_identification",
        "phrase_translation",
    }:
        return {"mode": "full", "reason": "surrounding_context_required"}

    if key in COMPACT_CONTEXT_QUESTION_TYPES or key.startswith("prefix_level_") or skill in MORPHOLOGY_SKILLS:
        return {"mode": "compact", "reason": "word_level_question"}

    return {"mode": "full", "reason": "default_full_context"}


def candidate_quality_breakdown(
    row,
    recent_pesukim,
    recent_words,
    recent_questions,
    *,
    progress=None,
    adaptive_context=None,
):
    question = row.get("question") or {}
    word = row.get("word") or question.get("selected_word") or question.get("word") or ""
    pasuk = row.get("pasuk") or question.get("pasuk") or ""
    signature = question_signature(question)
    adaptive_weight = candidate_weight(
        row,
        progress or {},
        recent_pesukim,
        recent_words,
        adaptive_context=adaptive_context,
    )
    context_policy = display_context_policy(question)
    translation_route = translation_practice_route_bonus(question, recent_questions)

    clarity = 0.0
    if question.get("selected_word") or question.get("word"):
        clarity += 1.0
    if question.get("prefix") or question.get("suffix") or question.get("shoresh"):
        clarity += 1.0
    if len((question.get("question") or "").split()) <= 10:
        clarity += 0.5

    context_dependence = 0.5 if context_policy["mode"] == "compact" else 0.0
    display_compactness = 0.5 if context_policy["mode"] == "compact" else 0.0

    novelty = 0.0
    if word and word not in recent_words[-5:]:
        novelty += 1.0
    if pasuk and pasuk not in recent_pesukim[-5:]:
        novelty += 0.5
    if not recent_question_repeat_reason(question, recent_questions):
        novelty += 0.5
    if (
        signature.get("repeat_family") == "translation"
        and signature.get("meaning_key")
        and any(
            previous.get("meaning_key") == signature["meaning_key"]
            for previous in recent_questions[-DUPLICATE_FEEL_WINDOW:]
        )
    ):
        novelty = max(0.0, novelty - 0.5)
    if (
        signature.get("repeat_family") == "shoresh"
        and signature.get("surface_pattern") in {"vav_yod_surface", "vav_tav_surface", "vav_led_surface"}
        and any(
            previous.get("surface_pattern") == signature["surface_pattern"]
            for previous in recent_questions[-SHORESH_SURFACE_WINDOW:]
        )
    ):
        novelty = max(0.0, novelty - 0.25)

    distractor_separation = distractor_separation_score(question)
    total = round(
        adaptive_weight
        + clarity
        + distractor_separation
        + novelty
        + context_dependence
        + display_compactness,
        2,
    )
    total = round(
        total + translation_route,
        2,
    )

    return {
        "total": total,
        "adaptive_weight": adaptive_weight,
        "clarity": round(clarity, 2),
        "distractor_separation": distractor_separation,
        "novelty": round(novelty, 2),
        "context_dependence": round(context_dependence, 2),
        "display_compactness": round(display_compactness, 2),
        "translation_route": round(translation_route, 2),
        "display_context_mode": context_policy["mode"],
        "display_context_reason": context_policy["reason"],
    }


def skip_reason_codes(question, fallback_code):
    details = (question or {}).get("details") or {}
    reason_codes = list(details.get("reason_codes") or [])
    return reason_codes or [fallback_code]


def summarize_debug_rejection_counts(rejection_counts):
    rows = []
    for code, count in sorted((rejection_counts or {}).items(), key=lambda item: (-item[1], item[0])):
        rows.append(
            {
                "code": code,
                "label": DEBUG_REJECTION_LABELS.get(code, code.replace("_", " ")),
                "count": count,
            }
        )
    return rows


def rejection_reason_messages(rejection_counts, *, limit=4):
    rows = summarize_debug_rejection_counts(rejection_counts)
    messages = []
    for row in rows[:limit]:
        label = row["label"].capitalize()
        if row["count"] > 1:
            label = f"{label} ({row['count']})."
        else:
            label = f"{label}."
        messages.append(label)
    return messages


def opening_variety_guard_skills(current_skill):
    return [
        skill
        for skill in SKILL_ORDER
        if skill != current_skill and skill not in OPENING_MECHANICAL_SKILLS
    ]


def recent_tense_family_count(recent_questions, window=SHORT_RUN_TENSE_WINDOW):
    recent_questions = list(recent_questions or [])
    return sum(
        1
        for item in recent_questions[-window:]
        if (item or {}).get("skill") in TENSE_FAMILY_SKILLS
    )


def tense_family_selection_block_reason(skill, recent_questions):
    if current_routing_mode() != "Learn Mode" or skill not in TENSE_FAMILY_SKILLS:
        return ""
    if st.session_state.get("pending_tense_contrast_followup"):
        return "tense_followup_continue_blocked"
    if recent_tense_family_count(recent_questions) >= SHORT_RUN_TENSE_CAP:
        return "tense_family_short_run_capped"
    return ""


def recent_grammar_taxonomy_count(recent_questions, window=SHORT_RUN_TENSE_WINDOW):
    recent_questions = list(recent_questions or [])
    return sum(
        1
        for item in recent_questions[-window:]
        if (item or {}).get("skill") in GRAMMAR_TAXONOMY_SKILLS
    )


def grammar_taxonomy_selection_block_reason(skill, recent_questions):
    if current_routing_mode() != "Learn Mode" or skill not in GRAMMAR_TAXONOMY_SKILLS:
        return ""
    if recent_grammar_taxonomy_count(recent_questions) >= SHORT_RUN_TENSE_CAP:
        return "grammar_taxonomy_short_run_capped"
    return ""


def recent_skill_count(skill, recent_questions, window=LEARN_MODE_SEQUENCE_WINDOW):
    if not skill:
        return 0
    recent_questions = list(recent_questions or [])
    normalized_skill = (skill or "").lower()
    return sum(
        1
        for item in recent_questions[-window:]
        if (item or {}).get("skill", "").lower() == normalized_skill
    )


def low_variety_mechanical_skill_is_saturated(skill, recent_questions, *, question_number=None):
    from runtime.session_state import get_instructional_group

    if current_routing_mode() != "Learn Mode" or not skill:
        return False
    if (question_number or short_run_question_number()) > LEARN_MODE_SEQUENCE_WINDOW:
        return False
    if get_instructional_group(skill) != "mechanical":
        return False

    normalized_skill = (skill or "").lower()
    recent_skill_entries = [
        item
        for item in list(recent_questions or [])[-LOW_VARIETY_MECHANICAL_WINDOW:]
        if (item or {}).get("skill", "").lower() == normalized_skill
    ]
    if len(recent_skill_entries) < LOW_VARIETY_MECHANICAL_REPEAT_CAP:
        return False

    pattern_counts = {}
    for item in recent_skill_entries:
        pattern_key = (
            item.get("prompt_family") or "",
            item.get("answer_pattern") or "",
        )
        if not any(pattern_key):
            continue
        pattern_counts[pattern_key] = pattern_counts.get(pattern_key, 0) + 1
    if pattern_counts and max(pattern_counts.values()) >= LOW_VARIETY_MECHANICAL_REPEAT_CAP:
        return True

    if normalized_skill in {"identify_prefix_meaning", "prefix"}:
        recent_prefix_letters = [
            item.get("prefix_letter")
            for item in recent_skill_entries
            if item.get("prefix_letter")
        ]
        if len(recent_prefix_letters) >= 2 and recent_prefix_letters[-1] == recent_prefix_letters[-2]:
            return True

    return False


def same_skill_is_saturated(skill, recent_questions, *, question_number=None):
    if current_routing_mode() != "Learn Mode" or not skill:
        return False
    if (question_number or short_run_question_number()) > LEARN_MODE_SEQUENCE_WINDOW:
        return False
    return recent_skill_count(skill, recent_questions) >= SHORT_RUN_SAME_SKILL_CAP


def trusted_active_scope_selection_enabled():
    return st.session_state.get("pilot_scope_mode", "trusted_active_scope") == "trusted_active_scope"


def short_run_question_number():
    return int(st.session_state.get("questions_answered", 0)) + 1


def sequencing_stage_for_question_number(question_number):
    if question_number <= 2:
        return "warmup"
    if question_number <= 6:
        return "meaning_build"
    if question_number <= LEARN_MODE_SEQUENCE_WINDOW:
        return "context_ramp"
    return "open"


def rebalance_group_preferences(preferences, recent_instructional_groups):
    preferences = list(preferences)
    recent_instructional_groups = list(recent_instructional_groups or [])
    if len(preferences) <= 1 or not recent_instructional_groups:
        return preferences

    last_group = recent_instructional_groups[-1]
    if recent_instructional_groups[-2:].count(last_group) >= 2 and last_group in preferences:
        preferences = [group for group in preferences if group != last_group] + [last_group]
    elif last_group == "mechanical" and last_group in preferences[:-1]:
        preferences = [group for group in preferences if group != last_group] + [last_group]

    return preferences


def sequencing_group_preferences(question_number, recent_instructional_groups):
    stage = sequencing_stage_for_question_number(question_number)
    if stage == "warmup":
        preferences = ["mechanical", "meaning", "verb_building", "context"]
    elif stage == "meaning_build":
        preferences = ["meaning", "verb_building", "context", "mechanical"]
    elif stage == "context_ramp":
        preferences = ["context", "meaning", "verb_building", "mechanical"]
    else:
        preferences = ["meaning", "context", "verb_building", "mechanical"]
    return stage, rebalance_group_preferences(preferences, recent_instructional_groups)


def sequence_skill_attempt_order(current_skill, recent_instructional_groups):
    from runtime.session_state import get_instructional_group

    current_skill = current_skill or ""
    current_group = get_instructional_group(current_skill)
    question_number = short_run_question_number()
    recent_questions = list(st.session_state.setdefault("recent_questions", []))
    stage, group_preferences = sequencing_group_preferences(question_number, recent_instructional_groups)

    attempted = []
    should_prepend_current = (
        (stage == "warmup" and current_group in {"meaning", "verb_building", "context"})
        or (stage == "meaning_build" and current_group in {"meaning", "verb_building"})
        or (stage == "context_ramp" and current_group == "context")
    )
    if current_skill and should_prepend_current:
        attempted.append(current_skill)

    for group in group_preferences:
        added_for_group = 0
        if current_skill and current_group == group and current_skill not in attempted:
            attempted.append(current_skill)
            added_for_group += 1
        for skill in SEQUENCING_GROUP_SKILLS.get(group, []):
            if (
                skill not in SKILL_ORDER
                or skill in attempted
                or added_for_group >= MAX_SEQUENCE_SKILLS_PER_GROUP
            ):
                continue
            attempted.append(skill)
            added_for_group += 1
            if len(attempted) >= MAX_SEQUENCE_SKILL_ATTEMPTS:
                break
        if len(attempted) >= MAX_SEQUENCE_SKILL_ATTEMPTS:
            break

    if current_skill and current_skill not in attempted:
        attempted.append(current_skill)

    saturated_skills = [
        skill for skill in attempted
        if same_skill_is_saturated(skill, recent_questions, question_number=question_number)
        or low_variety_mechanical_skill_is_saturated(
            skill,
            recent_questions,
            question_number=question_number,
        )
    ]
    if current_skill in saturated_skills:
        for sibling_skill in SEQUENCING_GROUP_SKILLS.get(current_group, []):
            if (
                sibling_skill != current_skill
                and sibling_skill in SKILL_ORDER
                and sibling_skill not in attempted
            ):
                attempted = [sibling_skill] + attempted
                break
    if saturated_skills:
        attempted = [skill for skill in attempted if skill not in saturated_skills] + saturated_skills

    return {
        "question_number": question_number,
        "stage": stage,
        "group_preferences": group_preferences,
        "attempted_skills": attempted[:MAX_SEQUENCE_SKILL_ATTEMPTS],
        "current_group": current_group,
        "saturated_skills": saturated_skills,
        "low_variety_skills": [
            skill for skill in attempted
            if low_variety_mechanical_skill_is_saturated(
                skill,
                recent_questions,
                question_number=question_number,
            )
        ],
    }


def current_routing_mode(flow=None):
    if flow is not None:
        return "Pasuk Flow"
    return st.session_state.get("practice_type", "Learn Mode")


def finalize_transition_debug(question, transition_path, transition_reason=""):
    return attach_debug_trace(
        question,
        transition_path=transition_path,
        transition_reason=transition_reason,
        answer_to_next_ready_ms=answer_to_next_ready_ms(),
    )


def build_quiz_debug_payload(question, progress=None, flow=None):
    question = question or {}
    trace = question.get("_debug_trace") or {}
    transition_reason = (
        trace.get("transition_reason")
        or st.session_state.get("adaptive_status_reason", "")
        or st.session_state.get("feature_fallback_message", "")
    )
    filter_reasons = list(trace.get("candidate_filter_reasons") or [])
    if not filter_reasons and trace.get("candidate_filtered"):
        filter_reasons = ["A candidate question was filtered before selection."]
    rejection_counts = summarize_debug_rejection_counts(trace.get("rejection_counts") or {})
    pasuk = get_pasukh_text(question or {}, flow)
    scope = active_scope_summary()

    return {
        "active_scope": scope["scope"],
        "active_range": {
            "first": scope["first_ref"],
            "last": scope["last_ref"],
            "pesukim_count": scope["pesukim_count"],
        },
        "mode": current_routing_mode(flow),
        "current_pasuk_ref": get_active_pasuk_ref(pasuk) if pasuk else "none",
        "current_question_type": question.get("question_type") or question.get("skill") or "none",
        "current_question_source": question_pipeline_source(question, flow),
        "current_skill": question.get("skill") or (progress or {}).get("current_skill") or "unknown",
        "target_word": question.get("selected_word") or question.get("word") or "",
        "routing_mode": current_routing_mode(flow),
        "next_question_path": trace.get("transition_path", "current_question"),
        "fallback_path": trace.get("fallback_path", ""),
        "reuse_mode": trace.get("reuse_mode", ""),
        "selection_mode": trace.get("selection_mode", ""),
        "pre_serve_validation_passed": bool(trace.get("pre_serve_validation_passed")),
        "pre_serve_validation_path": trace.get("pre_serve_validation_path", ""),
        "progress_source": trace.get("progress_source", "unknown"),
        "candidate_filtered": bool(trace.get("candidate_filtered")),
        "candidate_filter_reasons": filter_reasons,
        "rejection_reason_counts": rejection_counts,
        "rejection_total": sum(item["count"] for item in rejection_counts),
        "variety_guard_applied": bool(trace.get("variety_guard_applied")),
        "variety_guard_source": trace.get("variety_guard_source", ""),
        "transition_reason": transition_reason,
        "question_generation_ms": trace.get("question_generation_ms"),
        "followup_generation_ms": trace.get("followup_generation_ms"),
        "answer_to_next_ready_ms": trace.get("answer_to_next_ready_ms"),
        "selection_timing": dict(trace.get("selection_timing") or {}),
        "answer_pipeline_timing": dict(st.session_state.get("last_answer_pipeline_timing") or {}),
        "candidate_score_breakdown": dict(trace.get("candidate_score_breakdown") or {}),
    }


def build_followup_question(progress, question):
    from runtime.session_state import (
        get_generation_history,
        get_recent_prefixes,
        get_recent_question_formats,
        record_question_feature,
        record_question_prefix,
        record_selected_pasuk,
    )

    if generate_skill_question is None:
        return None

    started_at = perf_counter()
    skill = question.get("skill") or progress.get("current_skill")
    pasuk = question.get("pasuk") or get_pasukh_text(question)
    expected_bound_record = active_pasuk_record_for_question(question, fallback_text=pasuk)
    current_word = question.get("selected_word") or question.get("word")
    asked_tokens = list(get_generation_history(skill))
    if current_word:
        asked_tokens.append(current_word)

    prefix_level = progress.get("prefix_level", 1)
    recent_question_formats = get_recent_question_formats()
    recent_prefixes = get_recent_prefixes()
    recent_questions = list(st.session_state.setdefault("recent_questions", []))
    allow_recent_reuse = is_explicit_reteach_mode(st.session_state.get("pending_adaptive_context"))
    selection_mode = (st.session_state.get("pending_adaptive_context") or {}).get("selection_mode") or ""

    candidate_sources = []
    if pasuk and analyze_generator_pasuk is not None:
        try:
            candidate_sources.append((pasuk, candidate_source_for_pasuk(pasuk)))
        except Exception:
            pass
    if pasuk:
        candidate_sources.append((pasuk, pasuk))

    candidate_filter_reasons = []
    candidate_filtered = False
    rejection_counts = {}
    for pasuk_text, candidate_source in candidate_sources:
        try:
            followup = generate_skill_question(
                skill,
                candidate_source,
                asked_tokens=asked_tokens,
                prefix_level=prefix_level,
                recent_question_formats=recent_question_formats,
                recent_prefixes=recent_prefixes,
                recent_questions=recent_questions,
            )
        except Exception:
            candidate_filtered = True
            candidate_filter_reasons.append("A targeted follow-up candidate raised an error and was skipped.")
            rejection_counts = increment_debug_rejection_count(rejection_counts, "followup_generation_error")
            continue
        if followup is None:
            candidate_filtered = True
            candidate_filter_reasons.append("A targeted follow-up candidate returned no question.")
            rejection_counts = increment_debug_rejection_count(rejection_counts, "followup_returned_none")
            continue
        if followup.get("status") == "skipped":
            candidate_filtered = True
            candidate_filter_reasons.append(
                followup.get("reason") or "A targeted follow-up candidate was skipped before selection."
            )
            for code in skip_reason_codes(followup, "followup_skipped"):
                rejection_counts = increment_debug_rejection_count(rejection_counts, code)
            continue
        validation = validate_question_for_serve(
            followup,
            fallback_text=pasuk_text,
            validation_path="followup_candidate",
            expected_bound_record=expected_bound_record,
        )
        if not validation["valid"]:
            candidate_filtered = True
            candidate_filter_reasons.append(validation_failure_message(validation))
            for code in validation["rejection_codes"]:
                rejection_counts = increment_debug_rejection_count(rejection_counts, code)
            continue
        followup = validation["question"]
        repeat_reason = recent_question_repeat_reason(followup, recent_questions)
        if repeat_reason and not allow_recent_reuse:
            candidate_filtered = True
            candidate_filter_reasons.append("A repeated follow-up candidate was rejected before selection.")
            rejection_counts = increment_debug_rejection_count(rejection_counts, repeat_reason)
            continue
        next_word = followup.get("selected_word") or followup.get("word")
        if (
            not allow_recent_reuse
            and next_word == current_word
            and followup.get("question") == question.get("question")
        ):
            candidate_filtered = True
            candidate_filter_reasons.append("A repeated follow-up candidate was rejected before selection.")
            rejection_counts = increment_debug_rejection_count(rejection_counts, "repeated_followup_candidate")
            continue
        followup.setdefault("pasuk", pasuk_text)
        followup["_assessment_source"] = "targeted follow-up from active parsed dataset"
        followup["_cache_status"] = "targeted follow-up regenerated after the current error"
        record_selected_pasuk(followup["pasuk"])
        record_question_feature(followup)
        record_question_prefix(followup)
        followup_rejection_counts = dict(rejection_counts)
        followup_filter_reasons = list(candidate_filter_reasons)
        reuse_mode = ""
        transition_reason = ""
        if allow_recent_reuse and repeat_reason:
            reuse_mode = "explicit_reteach_reuse"
            transition_reason = "Explicit reteach reused a recent safe follow-up candidate."
            followup_rejection_counts = increment_debug_rejection_count(
                followup_rejection_counts,
                "explicit_reteach_reuse",
            )
            followup_filter_reasons.append("Explicit reteach reused a recent safe follow-up candidate.")
        return attach_debug_trace(
            followup,
            transition_path="follow-up",
            progress_source="reused",
            candidate_filtered=candidate_filtered,
            candidate_filter_reasons=followup_filter_reasons,
            rejection_counts=followup_rejection_counts,
            followup_generation_ms=round((perf_counter() - started_at) * 1000, 1),
            reuse_mode=reuse_mode,
            transition_reason=transition_reason,
            selection_mode=selection_mode,
        )

    fallback = generate_practice_question(skill, progress)
    if fallback:
        fallback_validation = validate_question_for_serve(
            fallback,
            fallback_text=pasuk,
            validation_path="followup_fallback",
        )
        if not fallback_validation["valid"]:
            candidate_filter_reasons.append(validation_failure_message(fallback_validation))
            for code in fallback_validation["rejection_codes"]:
                rejection_counts = increment_debug_rejection_count(rejection_counts, code)
            return None
        fallback = fallback_validation["question"]
        fallback["_assessment_source"] = "fallback follow-up from active parsed dataset"
        fallback["_cache_status"] = "fallback follow-up regenerated after the current error"
        candidate_filter_reasons.append("Targeted follow-up unavailable; used practice fallback.")
        return attach_debug_trace(
            fallback,
            transition_path="practice_fallback",
            progress_source="reused",
            candidate_filtered=True,
            candidate_filter_reasons=candidate_filter_reasons,
            rejection_counts=rejection_counts,
            fallback_path="practice_fallback",
            transition_reason="Targeted follow-up unavailable; used practice fallback.",
            followup_generation_ms=round((perf_counter() - started_at) * 1000, 1),
            selection_mode=selection_mode,
        )
    return fallback


def choose_weighted_pasuk_question(
    candidates,
    recent_pesukim,
    recent_words,
    progress=None,
    adaptive_context=None,
    recent_questions=None,
):
    scored = []
    for item in candidates:
        breakdown = candidate_quality_breakdown(
            item,
            recent_pesukim,
            recent_words,
            recent_questions or [],
            progress=progress,
            adaptive_context=adaptive_context,
        )
        scored.append(
            (
                breakdown["total"],
                item.get("word") or "",
                item.get("pasuk") or "",
                item,
                breakdown,
            )
        )

    scored.sort(key=lambda row: (-row[0], row[1], row[2]))
    if not scored:
        return candidates[0]

    selected = scored[0][3]
    selected["candidate_score_breakdown"] = scored[0][4]
    return selected


def rank_ready_rows(
    ready_rows,
    recent_pesukim,
    recent_words,
    *,
    skill=None,
    recent_questions=None,
    progress=None,
    adaptive_context=None,
):
    scored = []
    for row in ready_rows:
        route_bonus = translation_practice_ready_row_bonus(
            row,
            requested_skill=skill,
            recent_questions=recent_questions,
        )
        scored.append(
            {
                "weight": candidate_weight(
                    row,
                    progress or {},
                    recent_pesukim,
                    recent_words,
                    adaptive_context=adaptive_context,
                ) + route_bonus,
                "reviewed": bool(row.get("reviewed")),
                "word": row.get("word") or "",
                "pasuk": row.get("pasuk") or "",
                "route_bonus": route_bonus,
                "row": row,
            }
        )
    scored.sort(key=lambda item: (-item["weight"], -int(item["reviewed"]), item["word"], item["pasuk"]))
    return [item["row"] for item in scored]


def chunk_rows(rows, size):
    if size <= 0:
        return [list(rows)]
    return [rows[index:index + size] for index in range(0, len(rows), size)]


@st.cache_data
def get_skill_ready_pasuks(skill):
    from runtime.session_state import (
        get_morpheme_family,
        get_question_feature,
        get_question_prefix,
    )

    if generate_skill_question is None:
        return []

    ready = []
    for pasuk in active_pasuk_texts():
        try:
            question = generate_skill_question(
                skill,
                candidate_source_for_pasuk(pasuk),
            )
        except Exception:
            continue
        if question is None or question.get("status") == "skipped":
            continue
        ready.append(
            {
                "pasuk": pasuk,
                "word": question.get("selected_word") or question.get("word"),
                "feature": get_question_feature(question),
                "prefix": get_question_prefix(question),
                "morpheme_family": get_morpheme_family(question),
                "reviewed": question.get("analysis_source") == "active_scope_reviewed_bank",
                "question_type": question_type_key(question),
                "analysis_source": question.get("analysis_source") or "",
            }
        )
    return ready


def select_pasuk_first_question(skill, progress=None, adaptive_context=None):
    from runtime.session_state import (
        get_morpheme_family,
        feature_is_blocked,
        get_generation_history,
        get_question_feature,
        get_question_prefix,
        get_recent_prefixes,
        get_recent_question_formats,
        mechanical_group_cooldown_is_blocked,
        mechanical_group_is_capped,
        morpheme_family_is_blocked,
        prefix_is_blocked,
        record_question_feature,
        record_question_prefix,
        record_selected_pasuk,
    )

    if generate_skill_question is None:
        return None

    ready_lookup_started_at = perf_counter()
    recent_pesukim = st.session_state.setdefault("recent_pesukim", [])
    recent_words = st.session_state.setdefault("asked_tokens", [])
    ready_rows = get_skill_ready_pasuks(skill)
    ready_lookup_ms = round((perf_counter() - ready_lookup_started_at) * 1000, 1)
    if not ready_rows:
        return None
    pasuk_pool = [row["pasuk"] for row in ready_rows]
    recent_pasuk_window = recent_pesukim[-5:]
    preferred_pasuks = [pasuk for pasuk in pasuk_pool if pasuk not in recent_pasuk_window]
    progress = progress or load_progress()
    adaptive_context = adaptive_context or {}
    generation_history = get_generation_history(skill)
    recent_questions = list(st.session_state.setdefault("recent_questions", []))
    prefix_level = progress.get("prefix_level", 1)
    recent_question_formats = get_recent_question_formats()
    recent_prefixes = get_recent_prefixes()
    preferred_pasuk = adaptive_context.get("preferred_pasuk")
    allow_recent_reuse = is_explicit_reteach_mode(adaptive_context)
    selection_block_reason = (
        tense_family_selection_block_reason(skill, recent_questions)
        or grammar_taxonomy_selection_block_reason(skill, recent_questions)
    )
    if selection_block_reason:
        st.session_state.feature_fallback_message = ""
        return None
    candidate_rows = []
    repeat_blocked_rows = []
    fallback_reason = ""
    rejection_counts = {}
    if adaptive_context.get("selection_mode") == "reteach" and preferred_pasuk:
        search_pool = [pasuk for pasuk in pasuk_pool if pasuk == preferred_pasuk] or (preferred_pasuks or pasuk_pool)
    else:
        search_pool = preferred_pasuks or pasuk_pool
    metadata_filter_started_at = perf_counter()

    def prefilter_ready_rows(candidate_pasuks):
        candidate_pasuk_set = set(candidate_pasuks)
        filtered_ready_rows = [
            row for row in ready_rows if row["pasuk"] in candidate_pasuk_set
        ]
        eligible_rows = []
        fallback_ready_rows = []
        recent_target_words = {
            item.get("target_word")
            for item in recent_questions[-EXACT_WORD_REPEAT_WINDOW:]
            if (item or {}).get("target_word")
        }
        for ready_row in filtered_ready_rows:
            feature = ready_row.get("feature", "")
            prefix = ready_row.get("prefix", "")
            morpheme_family = ready_row.get("morpheme_family", "")
            row_word = _signature_text(ready_row.get("word") or "")
            if (
                row_word
                and row_word in recent_target_words
                and not reviewed_translation_row_can_rotate(ready_row, requested_skill=skill)
            ):
                nonlocal_rejection_counts[0] = increment_debug_rejection_count(
                    nonlocal_rejection_counts[0],
                    "recent_exact_word_repeat",
                )
                continue
            if not morpheme_family:
                if skill == "identify_verb_marker":
                    morpheme_family = "verb_marker"
                elif skill == "identify_pronoun_suffix":
                    morpheme_family = "pronoun_suffix"
                elif skill == "identify_suffix_meaning":
                    morpheme_family = "suffix_meaning"
                elif skill == "segment_word_parts":
                    morpheme_family = "segment_word_parts"
            if mechanical_group_is_capped(morpheme_family):
                rejection_counts_local = "opening_mechanical_group_capped"
                nonlocal_rejection_counts[0] = increment_debug_rejection_count(
                    nonlocal_rejection_counts[0],
                    rejection_counts_local,
                )
                continue
            if morpheme_family_is_blocked(morpheme_family):
                nonlocal_rejection_counts[0] = increment_debug_rejection_count(
                    nonlocal_rejection_counts[0],
                    "morpheme_family_repeat_blocked",
                )
                continue
            if mechanical_group_cooldown_is_blocked(morpheme_family):
                nonlocal_rejection_counts[0] = increment_debug_rejection_count(
                    nonlocal_rejection_counts[0],
                    "mechanical_group_cooldown_blocked",
                )
                continue
            if feature == "prefix" and prefix_is_blocked(prefix):
                fallback_ready_rows.append(ready_row)
                nonlocal_rejection_counts[0] = increment_debug_rejection_count(
                    nonlocal_rejection_counts[0],
                    "prefix_repeat_blocked",
                )
                continue
            if feature_is_blocked(feature):
                fallback_ready_rows.append(ready_row)
                nonlocal_rejection_counts[0] = increment_debug_rejection_count(
                    nonlocal_rejection_counts[0],
                    "feature_repeat_blocked",
                )
                continue
            eligible_rows.append(ready_row)
        return filtered_ready_rows, eligible_rows, fallback_ready_rows

    nonlocal_rejection_counts = [rejection_counts]
    filtered_ready_rows, eligible_ready_rows, fallback_ready_rows = prefilter_ready_rows(search_pool)
    if not eligible_ready_rows and not fallback_ready_rows and search_pool is not pasuk_pool:
        filtered_ready_rows, eligible_ready_rows, fallback_ready_rows = prefilter_ready_rows(pasuk_pool)

    rejection_counts = nonlocal_rejection_counts[0]
    metadata_filter_ms = round((perf_counter() - metadata_filter_started_at) * 1000, 1)

    ranking_started_at = perf_counter()
    ranked_ready_rows = rank_ready_rows(
        eligible_ready_rows,
        recent_pesukim,
        recent_words,
        skill=skill,
        recent_questions=recent_questions,
        progress=progress,
        adaptive_context=adaptive_context,
    )
    ranked_fallback_ready_rows = rank_ready_rows(
        fallback_ready_rows,
        recent_pesukim,
        recent_words,
        skill=skill,
        recent_questions=recent_questions,
        progress=progress,
        adaptive_context=adaptive_context,
    )
    ranking_ms = round((perf_counter() - ranking_started_at) * 1000, 1)

    full_generation_started_at = perf_counter()
    full_generation_rows = 0

    def materialize_candidate_rows(ranked_rows):
        nonlocal full_generation_rows, rejection_counts
        generated_candidates = []
        for ready_batch in chunk_rows(ranked_rows, MAX_FULL_GENERATION_ROWS_PER_PASS):
            batch_candidates = []
            for ready_row in ready_batch:
                pasuk = ready_row["pasuk"]
                try:
                    question = generate_skill_question(
                        skill,
                        candidate_source_for_pasuk(pasuk),
                        asked_tokens=generation_history,
                        prefix_level=prefix_level,
                        recent_question_formats=recent_question_formats,
                        recent_prefixes=recent_prefixes,
                        recent_questions=recent_questions,
                    )
                    full_generation_rows += 1
                except Exception:
                    rejection_counts = increment_debug_rejection_count(rejection_counts, "generation_error")
                    continue
                if question is None:
                    rejection_counts = increment_debug_rejection_count(rejection_counts, "generator_returned_none")
                    continue
                if question.get("status") == "skipped":
                    for code in skip_reason_codes(question, "generator_skipped"):
                        rejection_counts = increment_debug_rejection_count(rejection_counts, code)
                    continue
                validation = validate_question_for_serve(
                    question,
                    fallback_text=pasuk,
                    validation_path="first_question_candidate",
                )
                if not validation["valid"]:
                    for code in validation["rejection_codes"]:
                        rejection_counts = increment_debug_rejection_count(rejection_counts, code)
                    continue
                question = validation["question"]

                row = {
                    "pasuk": question.get("pasuk", pasuk),
                    "question": question,
                    "word": question.get("selected_word") or question.get("word"),
                    "feature": get_question_feature(question),
                    "prefix": get_question_prefix(question),
                    "reuse_mode": "",
                }
                repeat_reason = recent_question_repeat_reason(question, recent_questions)
                if repeat_reason and not allow_recent_reuse:
                    repeat_blocked_rows.append(row)
                    rejection_counts = increment_debug_rejection_count(rejection_counts, repeat_reason)
                    continue
                if repeat_reason and allow_recent_reuse:
                    row["reuse_mode"] = "explicit_reteach_reuse"
                batch_candidates.append(row)

            if batch_candidates:
                generated_candidates.extend(batch_candidates)
                break
        return generated_candidates

    candidate_rows = materialize_candidate_rows(ranked_ready_rows)

    if not candidate_rows and ranked_fallback_ready_rows:
        fallback_reason = "Feature repetition fallback used after 10 attempts."
        st.session_state.feature_fallback_message = fallback_reason
        candidate_rows = materialize_candidate_rows(ranked_fallback_ready_rows)

    full_generation_ms = round((perf_counter() - full_generation_started_at) * 1000, 1)

    if not candidate_rows:
        if repeat_blocked_rows:
            rejection_counts = increment_debug_rejection_count(rejection_counts, "limited_candidate_reuse")
            fallback_reason = fallback_reason or "Freshness fallback used because the safe candidate pool was too small."
            for row in repeat_blocked_rows:
                row["reuse_mode"] = "limited_candidate_reuse"
            candidate_rows = repeat_blocked_rows
        else:
            return None

    selected = choose_weighted_pasuk_question(
        candidate_rows,
        recent_pesukim,
        recent_words,
        progress=progress,
        adaptive_context=adaptive_context,
        recent_questions=recent_questions,
    )
    question = selected["question"]
    question.setdefault("pasuk", selected["pasuk"])
    question["_assessment_source"] = "generated skill question from active parsed dataset"
    question["_cache_status"] = "eligible pasuk pool cached; question regenerated"
    trace_rejection_counts = dict(rejection_counts)
    trace_fallback_path = (
        "feature_repetition_fallback"
        if ranked_fallback_ready_rows and fallback_reason
        else ("limited_candidate_reuse" if repeat_blocked_rows and fallback_reason else "")
    )
    trace_transition_reason = fallback_reason
    if selected.get("reuse_mode") == "explicit_reteach_reuse":
        trace_rejection_counts = increment_debug_rejection_count(
            trace_rejection_counts,
            "explicit_reteach_reuse",
        )
        trace_transition_reason = "Explicit reteach reused a recent safe candidate."
    trace_filter_reasons = (
        [fallback_reason]
        if fallback_reason
        else rejection_reason_messages(trace_rejection_counts)
    )
    if not trace_filter_reasons and (ranked_fallback_ready_rows or repeat_blocked_rows):
        trace_filter_reasons = ["One or more candidate questions were filtered before selection."]
    attach_debug_trace(
        question,
        candidate_filtered=bool(ranked_fallback_ready_rows or repeat_blocked_rows),
        candidate_filter_reasons=trace_filter_reasons,
        rejection_counts=trace_rejection_counts,
        fallback_path=trace_fallback_path,
        candidate_score_breakdown=selected.get("candidate_score_breakdown", {}),
        transition_reason=trace_transition_reason,
        reuse_mode=selected.get("reuse_mode") or "",
        selection_mode=adaptive_context.get("selection_mode") or "",
        selection_timing={
            "ready_rows_lookup_ms": ready_lookup_ms,
            "metadata_filter_ms": metadata_filter_ms,
            "ranking_ms": ranking_ms,
            "full_generation_ms": full_generation_ms,
            "ready_rows_total": len(ready_rows),
            "search_rows_total": len(filtered_ready_rows),
            "eligible_ready_rows": len(ranked_ready_rows),
            "fallback_ready_rows": len(ranked_fallback_ready_rows),
            "full_generation_rows": full_generation_rows,
        },
    )
    record_selected_pasuk(selected["pasuk"])
    record_question_feature(question)
    record_question_prefix(question)
    return question


def generate_mastery_question(progress):
    from runtime.session_state import (
        consume_adaptive_context,
        is_grammar_taxonomy_skill,
        get_instructional_group,
        get_recent_instructional_groups,
        is_tense_family_skill,
    )

    adaptive_context = consume_adaptive_context()

    def build_mastery_question():
        current_skill = progress["current_skill"]
        if current_routing_mode() != "Learn Mode" or short_run_question_number() > LEARN_MODE_SEQUENCE_WINDOW:
            question = select_pasuk_first_question(
                current_skill,
                progress=progress,
                adaptive_context=adaptive_context,
            )
            if question is not None or current_routing_mode() != "Learn Mode":
                return question

            if current_skill in OPENING_MECHANICAL_SKILLS:
                fallback_skills = opening_variety_guard_skills(current_skill)
            elif current_skill in GRAMMAR_TAXONOMY_SKILLS:
                fallback_skills = [
                    skill for skill in SKILL_ORDER
                    if skill != current_skill and skill not in GRAMMAR_TAXONOMY_SKILLS
                ]
            else:
                return None

            for fallback_skill in fallback_skills:
                fallback_question = select_pasuk_first_question(
                    fallback_skill,
                    progress=progress,
                    adaptive_context=adaptive_context,
                )
                if fallback_question is None:
                    continue
                if (
                    st.session_state.get("pending_tense_contrast_followup")
                    and current_skill in TENSE_FAMILY_SKILLS
                ):
                    st.session_state.pending_tense_contrast_followup = False
                return attach_debug_trace(
                    fallback_question,
                    variety_guard_applied=True,
                    variety_guard_source=current_skill,
                    transition_reason=(
                        "Learn Mode selected a broader non-mechanical question."
                    ),
                )
            return None

        recent_instructional_groups = get_recent_instructional_groups()
        sequence_plan = sequence_skill_attempt_order(current_skill, recent_instructional_groups)
        attempted_skills = sequence_plan["attempted_skills"]
        stage = sequence_plan["stage"]
        question_number = sequence_plan["question_number"]
        group_preferences = sequence_plan["group_preferences"]
        saturated_skills = sequence_plan.get("saturated_skills") or []
        low_variety_skills = sequence_plan.get("low_variety_skills") or []

        for skill_to_try in attempted_skills:
            question = select_pasuk_first_question(
                skill_to_try,
                progress=progress,
                adaptive_context=adaptive_context,
            )
            if question is None:
                continue

            selected_group = get_instructional_group(question)
            transition_reason = ""
            if stage == "meaning_build" and selected_group in {"meaning", "verb_building"}:
                transition_reason = "Short-run sequencing moved the session toward meaning work."
            elif stage == "context_ramp" and selected_group == "context":
                transition_reason = "Short-run sequencing moved the session toward context."
            elif skill_to_try != current_skill:
                transition_reason = "Short-run sequencing selected a different instructional family."
            if (
                st.session_state.get("pending_tense_contrast_followup")
                and is_tense_family_skill(current_skill)
                and not is_tense_family_skill(question)
            ):
                st.session_state.pending_tense_contrast_followup = False
                transition_reason = (
                    "A short tense contrast was shown, so the run moved back into broader variety."
                )
            elif skill_to_try != current_skill and is_grammar_taxonomy_skill(current_skill):
                transition_reason = "Learn Mode moved back to clearer word work before more grammar labels."
            elif skill_to_try != current_skill and current_skill in saturated_skills:
                transition_reason = "Short-run sequencing widened the run after one skill had already appeared several times."
            if skill_to_try != current_skill and current_skill in low_variety_skills:
                transition_reason = "Short-run diversity moved the session off a repetitive mechanical lane."

            question_rejection_counts = dict(question.get("_debug_trace", {}).get("rejection_counts") or {})
            question = attach_debug_trace(
                question,
                sequencing_applied=True,
                sequencing_stage=stage,
                sequencing_question_number=question_number,
                sequencing_group_preferences=group_preferences,
                sequencing_attempted_skills=attempted_skills,
                sequencing_selected_group=selected_group,
                sequencing_source_skill=current_skill,
                sequencing_saturated_skills=saturated_skills,
                sequencing_low_variety_skills=low_variety_skills,
                transition_reason=transition_reason,
            )
            if skill_to_try != current_skill and current_skill in OPENING_MECHANICAL_SKILLS:
                question_rejection_counts = increment_debug_rejection_count(
                    question_rejection_counts,
                    "diversity_redirect",
                )
                question = attach_debug_trace(
                    question,
                    variety_guard_applied=True,
                    variety_guard_source=current_skill,
                    rejection_counts=question_rejection_counts,
                )
            elif skill_to_try != current_skill and current_skill in saturated_skills:
                question_rejection_counts = increment_debug_rejection_count(
                    question_rejection_counts,
                    "diversity_redirect",
                )
                question = attach_debug_trace(
                    question,
                    variety_guard_applied=True,
                    variety_guard_source=current_skill,
                    rejection_counts=increment_debug_rejection_count(
                        question_rejection_counts,
                        "same_skill_short_run_saturated",
                    ),
                )
            elif skill_to_try != current_skill and current_skill in low_variety_skills:
                question_rejection_counts = increment_debug_rejection_count(
                    question_rejection_counts,
                    "diversity_redirect",
                )
                question = attach_debug_trace(
                    question,
                    variety_guard_applied=True,
                    variety_guard_source=current_skill,
                    rejection_counts=question_rejection_counts,
                )
            return question
        return None

    question, elapsed_ms = timed_question_generation(
        build_mastery_question
    )
    return attach_debug_trace(
        question,
        question_generation_ms=elapsed_ms,
        progress_source="reused",
    )


def generate_practice_question(skill, progress=None):
    question, elapsed_ms = timed_question_generation(
        lambda: select_pasuk_first_question(skill, progress=progress or load_progress_state())
    )
    return attach_debug_trace(
        question,
        question_generation_ms=elapsed_ms,
        progress_source=progress_source_label(progress),
    )
