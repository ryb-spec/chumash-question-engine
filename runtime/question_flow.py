import re
from difflib import SequenceMatcher
from time import perf_counter

import streamlit as st

from adaptive_engine import candidate_weight
from assessment_scope import active_scope_summary


DEBUG_REJECTION_LABELS = {
    "followup_generation_error": "follow-up generation error",
    "followup_returned_none": "follow-up returned no question",
    "followup_skipped": "follow-up skipped",
    "repeated_followup_candidate": "repeated follow-up rejected",
    "generation_error": "question generation error",
    "generator_returned_none": "generator returned no question",
    "generator_skipped": "generator skipped candidate",
    "feature_repeat_blocked": "feature repetition blocked",
    "prefix_repeat_blocked": "prefix repetition blocked",
    "recent_exact_repeat": "recent exact repeat blocked",
    "recent_target_repeat": "recent target repeat blocked",
    "recent_prompt_repeat": "recent prompt repeat blocked",
    "limited_candidate_reuse": "limited candidate reuse allowed",
}
RECENT_QUESTION_HISTORY_LIMIT = 12
EXACT_REPEAT_WINDOW = 8
NEAR_REPEAT_WINDOW = 5
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


def progress_source_label(progress):
    return "reused" if progress is not None else "reloaded"


def increment_debug_rejection_count(counts, code, amount=1):
    updated = dict(counts or {})
    updated[code] = updated.get(code, 0) + amount
    return updated


def _signature_text(value):
    if not value:
        return ""
    import streamlit_app as app

    text = app.normalize_hebrew_key(str(value))
    text = re.sub(r"\s+", " ", text).strip()
    return text.lower()


def question_prompt_family(question):
    family = question.get("question_format") or question.get("question_type")
    if family:
        return str(family)

    prompt = HEBREW_WORD_RE.sub("<hebrew>", question.get("question", "").lower())
    prompt = re.sub(r"[^a-z0-9_<>\s]+", " ", prompt)
    return re.sub(r"\s+", " ", prompt).strip()


def question_signature(question):
    question = question or {}
    pasuk = question.get("pasuk") or ""
    import streamlit_app as app

    return {
        "skill": question.get("skill") or question.get("question_type") or "",
        "target_word": _signature_text(question.get("selected_word") or question.get("word") or ""),
        "prompt_family": question_prompt_family(question),
        "correct_answer": _signature_text(question.get("correct_answer") or ""),
        "source_pasuk": _signature_text(app.get_active_pasuk_ref(pasuk) if pasuk else ""),
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
    import streamlit_app as app

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
    pasuk = app.get_pasukh_text(question or {}, flow)
    scope = active_scope_summary()

    return {
        "active_scope": scope["scope"],
        "active_range": {
            "first": scope["first_ref"],
            "last": scope["last_ref"],
            "pesukim_count": scope["pesukim_count"],
        },
        "mode": current_routing_mode(flow),
        "current_pasuk_ref": app.get_active_pasuk_ref(pasuk) if pasuk else "none",
        "current_question_type": question.get("question_type") or question.get("skill") or "none",
        "current_question_source": app.question_pipeline_source(question, flow),
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
        "candidate_score_breakdown": dict(trace.get("candidate_score_breakdown") or {}),
    }


def build_followup_question(progress, question):
    import streamlit_app as app
    from runtime.session_state import (
        get_generation_history,
        get_recent_prefixes,
        get_recent_question_formats,
        record_question_feature,
        record_question_prefix,
        record_selected_pasuk,
    )

    if app.generate_skill_question is None:
        return None

    started_at = perf_counter()
    skill = question.get("skill") or progress.get("current_skill")
    pasuk = question.get("pasuk") or app.get_pasukh_text(question)
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
    if pasuk and app.analyze_generator_pasuk is not None:
        try:
            candidate_sources.append((pasuk, app.analyze_generator_pasuk(pasuk)))
        except Exception:
            pass
    if pasuk:
        candidate_sources.append((pasuk, pasuk))

    candidate_filter_reasons = []
    candidate_filtered = False
    rejection_counts = {}
    for pasuk_text, candidate_source in candidate_sources:
        try:
            followup = app.generate_skill_question(
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

    fallback = app.generate_practice_question(skill, progress)
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


def select_pasuk_first_question(skill, progress=None, adaptive_context=None):
    import streamlit_app as app
    from runtime.session_state import (
        feature_is_blocked,
        get_generation_history,
        get_question_feature,
        get_question_prefix,
        get_recent_prefixes,
        get_recent_question_formats,
        prefix_is_blocked,
        record_question_feature,
        record_question_prefix,
        record_selected_pasuk,
    )

    if app.generate_skill_question is None:
        return None

    recent_pesukim = st.session_state.setdefault("recent_pesukim", [])
    recent_words = st.session_state.setdefault("asked_tokens", [])
    ready_rows = app.get_skill_ready_pasuks(skill)
    if not ready_rows:
        return None
    pasuk_pool = [row["pasuk"] for row in ready_rows]
    recent_pasuk_window = recent_pesukim[-5:]
    preferred_pasuks = [pasuk for pasuk in pasuk_pool if pasuk not in recent_pasuk_window]
    progress = progress or app.load_progress()
    adaptive_context = adaptive_context or {}
    generation_history = get_generation_history(skill)
    recent_questions = list(st.session_state.setdefault("recent_questions", []))
    prefix_level = progress.get("prefix_level", 1)
    recent_question_formats = get_recent_question_formats()
    recent_prefixes = get_recent_prefixes()
    preferred_pasuk = adaptive_context.get("preferred_pasuk")
    allow_recent_reuse = is_explicit_reteach_mode(adaptive_context)

    attempts = 0
    candidate_rows = []
    fallback_rows = []
    repeat_blocked_rows = []
    fallback_reason = ""
    rejection_counts = {}
    if adaptive_context.get("selection_mode") == "reteach" and preferred_pasuk:
        search_pool = [pasuk for pasuk in pasuk_pool if pasuk == preferred_pasuk] or (preferred_pasuks or pasuk_pool)
    else:
        search_pool = preferred_pasuks or pasuk_pool

    while attempts < 10 and not candidate_rows:
        attempts += 1
        for pasuk in search_pool:
            try:
                question = app.generate_skill_question(
                    skill,
                    (
                        app.analyze_generator_pasuk(pasuk)
                        if app.analyze_generator_pasuk is not None
                        else pasuk
                    ),
                    asked_tokens=generation_history,
                    prefix_level=prefix_level,
                    recent_question_formats=recent_question_formats,
                    recent_prefixes=recent_prefixes,
                )
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

            word = question.get("selected_word") or question.get("word")
            feature = get_question_feature(question)
            prefix = get_question_prefix(question)
            row = {
                "pasuk": question.get("pasuk", pasuk),
                "question": question,
                "word": word,
                "feature": feature,
                "prefix": prefix,
            }
            if feature == "prefix" and prefix_is_blocked(prefix):
                fallback_rows.append(row)
                rejection_counts = increment_debug_rejection_count(rejection_counts, "prefix_repeat_blocked")
                continue
            if feature_is_blocked(feature):
                fallback_rows.append(row)
                rejection_counts = increment_debug_rejection_count(rejection_counts, "feature_repeat_blocked")
                continue
            if not allow_recent_reuse:
                repeat_reason = recent_question_repeat_reason(question, recent_questions)
                if repeat_reason:
                    repeat_blocked_rows.append(row)
                    rejection_counts = increment_debug_rejection_count(rejection_counts, repeat_reason)
                    continue
            candidate_rows.append(row)

        if not candidate_rows and search_pool is not pasuk_pool:
            search_pool = pasuk_pool

    if not candidate_rows:
        reuse_rows = list(repeat_blocked_rows) + list(fallback_rows)
        if not reuse_rows:
            return None
        if repeat_blocked_rows:
            rejection_counts = increment_debug_rejection_count(rejection_counts, "limited_candidate_reuse")
        if fallback_rows:
            fallback_reason = "Feature repetition fallback used after 10 attempts."
            st.session_state.feature_fallback_message = fallback_reason
        else:
            fallback_reason = "Freshness fallback used because the safe candidate pool was too small."
        candidate_rows = reuse_rows

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
        candidate_filtered=bool(fallback_rows),
        candidate_filter_reasons=(
            [fallback_reason]
            if fallback_reason
            else (
                ["One or more candidate questions were filtered before selection."]
                if fallback_rows or repeat_blocked_rows
                else []
            )
        ),
        rejection_counts=rejection_counts,
        fallback_path=(
            "feature_repetition_fallback"
            if fallback_rows and fallback_reason
            else ("limited_candidate_reuse" if repeat_blocked_rows and fallback_reason else "")
        ),
        candidate_score_breakdown=selected.get("candidate_score_breakdown", {}),
        transition_reason=fallback_reason,
    )
    record_selected_pasuk(selected["pasuk"])
    record_question_feature(question)
    record_question_prefix(question)
    return question


def generate_mastery_question(progress):
    from runtime.session_state import consume_adaptive_context

    adaptive_context = consume_adaptive_context()
    question, elapsed_ms = timed_question_generation(
        lambda: select_pasuk_first_question(
            progress["current_skill"],
            progress=progress,
            adaptive_context=adaptive_context,
        )
    )
    return attach_debug_trace(
        question,
        question_generation_ms=elapsed_ms,
        progress_source="reused",
    )


def generate_practice_question(skill, progress=None):
    import streamlit_app as app

    question, elapsed_ms = timed_question_generation(
        lambda: select_pasuk_first_question(skill, progress=progress or app.load_progress())
    )
    return attach_debug_trace(
        question,
        question_generation_ms=elapsed_ms,
        progress_source=progress_source_label(progress),
    )
