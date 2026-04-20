import re
from copy import deepcopy
from difflib import SequenceMatcher
from functools import lru_cache
from time import perf_counter

import streamlit as st

from adaptive_engine import candidate_weight
from assessment_scope import (
    active_pasuk_texts,
    active_scope_summary,
    bind_question_to_active_scope,
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
    "trusted_active_scope_unmappable": "trusted active-scope mapping blocked",
    "tense_followup_continue_blocked": "tense follow-up held for broader variety",
    "tense_family_short_run_capped": "tense-family short-run cap blocked",
    "grammar_taxonomy_short_run_capped": "grammar-taxonomy short-run cap blocked",
    "recent_exact_word_repeat": "recent exact-word repeat blocked",
    "recent_same_pasuk_intent_repeat": "same pasuk intent repeat blocked",
    "recent_semantic_sibling_repeat": "semantic sibling repeat blocked",
    "limited_candidate_reuse": "limited candidate reuse allowed",
}
RECENT_QUESTION_HISTORY_LIMIT = 12
EXACT_REPEAT_WINDOW = 8
NEAR_REPEAT_WINDOW = 5
EXACT_WORD_REPEAT_WINDOW = 4
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
def _cached_candidate_source(analyzer_identity, pasuk):
    if analyze_generator_pasuk is None:
        return pasuk
    return analyze_generator_pasuk(pasuk)


def candidate_source_for_pasuk(pasuk):
    if analyze_generator_pasuk is None:
        return pasuk
    return deepcopy(_cached_candidate_source(id(analyze_generator_pasuk), pasuk))


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

    return {
        "skill": question.get("skill") or question.get("question_type") or "",
        "question_type": question_type_key(question),
        "target_word": _signature_text(question.get("selected_word") or question.get("word") or ""),
        "target_family": question_target_family(question),
        "prompt_family": question_prompt_family(question),
        "correct_answer": _signature_text(question.get("correct_answer") or ""),
        "answer_pattern": question_answer_pattern(question),
        "source_pasuk": _signature_text(get_active_pasuk_ref(pasuk) if pasuk else ""),
    }


def recent_question_signature_key(signature):
    signature = signature or {}
    return "|".join(
        [
            signature.get("skill", ""),
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
    exact_window = recent_questions[-EXACT_REPEAT_WINDOW:]
    exact_key = recent_question_signature_key(signature)
    if any(recent_question_signature_key(item) == exact_key for item in exact_window):
        return "recent_exact_repeat"

    near_window = recent_questions[-NEAR_REPEAT_WINDOW:]
    for previous in near_window:
        if previous.get("skill") != signature["skill"]:
            continue
        if previous.get("target_word") and previous.get("target_word") == signature["target_word"]:
            return "recent_target_repeat"
        if (
            previous.get("prompt_family")
            and previous.get("prompt_family") == signature["prompt_family"]
            and previous.get("correct_answer")
            and previous.get("correct_answer") == signature["correct_answer"]
            and previous.get("source_pasuk")
            and previous.get("source_pasuk") == signature["source_pasuk"]
        ):
            return "recent_prompt_repeat"

    previous = recent_questions[-1] if recent_questions else {}
    if previous:
        if (
            previous.get("question_type") == signature["question_type"]
            and previous.get("source_pasuk")
            and previous.get("source_pasuk") == signature["source_pasuk"]
            and previous.get("prompt_family") == signature["prompt_family"]
            and previous.get("answer_pattern") == signature["answer_pattern"]
        ):
            return "recent_same_pasuk_intent_repeat"
        if (
            previous.get("question_type") == signature["question_type"]
            and previous.get("target_family")
            and previous.get("target_family") == signature["target_family"]
            and previous.get("target_word") != signature["target_word"]
        ):
            return "recent_semantic_sibling_repeat"

    if signature.get("target_word"):
        exact_word_window = recent_questions[-EXACT_WORD_REPEAT_WINDOW:]
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
    adaptive_weight = candidate_weight(
        row,
        progress or {},
        recent_pesukim,
        recent_words,
        adaptive_context=adaptive_context,
    )
    context_policy = display_context_policy(question)

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

    return {
        "total": total,
        "adaptive_weight": adaptive_weight,
        "clarity": round(clarity, 2),
        "distractor_separation": distractor_separation,
        "novelty": round(novelty, 2),
        "context_dependence": round(context_dependence, 2),
        "display_compactness": round(display_compactness, 2),
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

    return {
        "question_number": question_number,
        "stage": stage,
        "group_preferences": group_preferences,
        "attempted_skills": attempted[:MAX_SEQUENCE_SKILL_ATTEMPTS],
        "current_group": current_group,
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
        "progress_source": trace.get("progress_source", "unknown"),
        "candidate_filtered": bool(trace.get("candidate_filtered")),
        "candidate_filter_reasons": filter_reasons,
        "rejection_reason_counts": rejection_counts,
        "rejection_total": sum(item["count"] for item in rejection_counts),
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
    current_word = question.get("selected_word") or question.get("word")
    asked_tokens = list(get_generation_history(skill))
    if current_word:
        asked_tokens.append(current_word)

    prefix_level = progress.get("prefix_level", 1)
    recent_question_formats = get_recent_question_formats()
    recent_prefixes = get_recent_prefixes()
    recent_questions = list(st.session_state.setdefault("recent_questions", []))
    allow_recent_reuse = is_explicit_reteach_mode(st.session_state.get("pending_adaptive_context"))

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
        scope_record = bind_question_to_active_scope(followup, fallback_text=pasuk_text)
        if trusted_active_scope_selection_enabled() and not scope_record:
            candidate_filtered = True
            candidate_filter_reasons.append(
                "A follow-up candidate could not be mapped to the active parsed dataset in trusted mode."
            )
            rejection_counts = increment_debug_rejection_count(
                rejection_counts,
                "trusted_active_scope_unmappable",
            )
            continue
        repeat_reason = ""
        if not allow_recent_reuse:
            repeat_reason = recent_question_repeat_reason(followup, recent_questions)
        if repeat_reason:
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
        return attach_debug_trace(
            followup,
            transition_path="follow-up",
            progress_source="reused",
            candidate_filtered=candidate_filtered,
            candidate_filter_reasons=candidate_filter_reasons,
            rejection_counts=rejection_counts,
            followup_generation_ms=round((perf_counter() - started_at) * 1000, 1),
        )

    fallback = generate_practice_question(skill, progress)
    if fallback:
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
    progress=None,
    adaptive_context=None,
):
    scored = []
    for row in ready_rows:
        scored.append(
            (
                candidate_weight(
                    row,
                    progress or {},
                    recent_pesukim,
                    recent_words,
                    adaptive_context=adaptive_context,
                ),
                row.get("word") or "",
                row.get("pasuk") or "",
                row,
            )
        )
    scored.sort(key=lambda item: (-item[0], item[1], item[2]))
    return [item[3] for item in scored]


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
            if row_word and row_word in recent_target_words:
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
        progress=progress,
        adaptive_context=adaptive_context,
    )
    ranked_fallback_ready_rows = rank_ready_rows(
        fallback_ready_rows,
        recent_pesukim,
        recent_words,
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
                scope_record = bind_question_to_active_scope(question, fallback_text=pasuk)
                if trusted_active_scope_selection_enabled() and not scope_record:
                    rejection_counts = increment_debug_rejection_count(
                        rejection_counts,
                        "trusted_active_scope_unmappable",
                    )
                    continue

                row = {
                    "pasuk": question.get("pasuk", pasuk),
                    "question": question,
                    "word": question.get("selected_word") or question.get("word"),
                    "feature": get_question_feature(question),
                    "prefix": get_question_prefix(question),
                }
                if not allow_recent_reuse:
                    repeat_reason = recent_question_repeat_reason(question, recent_questions)
                    if repeat_reason:
                        repeat_blocked_rows.append(row)
                        rejection_counts = increment_debug_rejection_count(rejection_counts, repeat_reason)
                        continue
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
    attach_debug_trace(
        question,
        candidate_filtered=bool(ranked_fallback_ready_rows or repeat_blocked_rows),
        candidate_filter_reasons=(
            [fallback_reason]
            if fallback_reason
            else (
                ["One or more candidate questions were filtered before selection."]
                if ranked_fallback_ready_rows or repeat_blocked_rows
                else []
            )
        ),
        rejection_counts=rejection_counts,
        fallback_path=(
            "feature_repetition_fallback"
            if ranked_fallback_ready_rows and fallback_reason
            else ("limited_candidate_reuse" if repeat_blocked_rows and fallback_reason else "")
        ),
        candidate_score_breakdown=selected.get("candidate_score_breakdown", {}),
        transition_reason=fallback_reason,
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

            question = attach_debug_trace(
                question,
                sequencing_applied=True,
                sequencing_stage=stage,
                sequencing_question_number=question_number,
                sequencing_group_preferences=group_preferences,
                sequencing_attempted_skills=attempted_skills,
                sequencing_selected_group=selected_group,
                sequencing_source_skill=current_skill,
                transition_reason=transition_reason,
            )
            if skill_to_try != current_skill and current_skill in OPENING_MECHANICAL_SKILLS:
                question = attach_debug_trace(
                    question,
                    variety_guard_applied=True,
                    variety_guard_source=current_skill,
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
