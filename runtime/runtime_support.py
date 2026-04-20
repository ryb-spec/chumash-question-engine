from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from functools import lru_cache
from html import escape
from time import perf_counter

import streamlit as st

from adaptive_engine import build_selection_preferences, evaluate_skill_progression
from assessment_scope import (
    ACTIVE_ASSESSMENT_SCOPE,
    active_pasuk_texts,
    active_pesukim_records,
    active_scope_summary,
    data_path,
    repo_path,
)
from progress_store import load_progress_state, record_answer, save_progress_state
from runtime.pilot_logging import record_pilot_answer
from runtime.presentation import (
    SKILL_ORDER,
    get_error_type,
    get_next_skill,
    skill_path_label,
)
from torah_parser.word_bank_adapter import (
    adapt_word_bank_data,
    build_word_bank_metadata_index,
    normalize_hebrew_key,
)

try:
    from pasuk_flow_generator import analyze_pasuk as analyze_generator_pasuk
    from pasuk_flow_generator import generate_pasuk_flow
    from pasuk_flow_generator import generate_question as generate_skill_question
    from pasuk_flow_generator import update_word_skill_score
except ImportError:
    analyze_generator_pasuk = None
    generate_pasuk_flow = None
    generate_skill_question = None
    update_word_skill_score = None


WORD_BANK_PATH = data_path("word_bank.json")
ATTEMPT_LOG_PATH = data_path("attempt_log.jsonl")
HEBREW_WORD_RE = re.compile(r"[\u0590-\u05ff]+")
HEBREW_MARK_RE = re.compile(r"[\u0591-\u05c7]")
OPTION_LABELS = [chr(ord("A") + index) for index in range(26)]

MENUKAD_FALLBACK = {
    "הלך": "הָלַךְ",
    "בא": "בָּא",
    "יצא": "יָצָא",
    "עלה": "עָלָה",
    "ירד": "יָרַד",
    "ישב": "יָשַׁב",
    "נתן": "נָתַן",
    "לקח": "לָקַח",
    "ראה": "רָאָה",
    "שמע": "שָׁמַע",
    "וילך": "וַיֵּלֶךְ",
    "ויתן": "וַיִּתֵּן",
    "וירא": "וַיַּרְא",
    "וישב": "וַיֵּשֶׁב",
    "ויצא": "וַיֵּצֵא",
    "איש": "אִישׁ",
    "האיש": "הָאִישׁ",
    "אב": "אָב",
    "האב": "הָאָב",
    "בן": "בֵּן",
    "בית": "בַּיִת",
    "ביתו": "בֵּיתוֹ",
    "בביתו": "בְּבֵיתוֹ",
    "מביתו": "מִבֵּיתוֹ",
    "לבנו": "לִבְנוֹ",
    "מבנו": "מִבְּנוֹ",
    "לחם": "לֶחֶם",
    "עיר": "עִיר",
    "העיר": "הָעִיר",
    "ארץ": "אֶרֶץ",
    "הארץ": "הָאָרֶץ",
    "אל": "אֶל",
    "מן": "מִן",
    "על": "עַל",
}


def load_json(path, default):
    if not path.exists():
        return default

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


@st.cache_data
def load_pasuk_flows():
    if generate_pasuk_flow is None:
        return []

    flows = []
    for index, pasuk in enumerate(active_pasuk_texts(), 1):
        try:
            flow = generate_pasuk_flow(pasuk)
        except ValueError:
            continue
        flow["source"] = f"{ACTIVE_ASSESSMENT_SCOPE}:{index}"
        flows.append(flow)
    return flows


@st.cache_data
def load_word_bank_metadata():
    data = load_json(WORD_BANK_PATH, {"words": []})
    return build_word_bank_metadata_index(adapt_word_bank_data(data))


def load_progress():
    return load_progress_state()


def save_progress(progress):
    return save_progress_state(progress)


def menukad_word(word):
    metadata = load_word_bank_metadata()
    if word in metadata and metadata[word].get("menukad"):
        return metadata[word]["menukad"]
    if word in MENUKAD_FALLBACK:
        return MENUKAD_FALLBACK[word]
    return word


def strip_nekudos(text):
    if not isinstance(text, str):
        return text
    return HEBREW_MARK_RE.sub("", text)


def menukad_text(text):
    if not isinstance(text, str):
        return text

    display = HEBREW_WORD_RE.sub(lambda match: menukad_word(match.group(0)), text)
    if not st.session_state.get("show_nekudos", True):
        return strip_nekudos(display)
    return display


def rtl_hebrew_html(text, focus=None, class_name="hebrew-text"):
    display = menukad_text(text)
    safe_text = escape(display)
    if focus:
        safe_focus = escape(menukad_text(focus))
        safe_text = safe_text.replace(
            safe_focus,
            f"<mark>{safe_focus}</mark>",
            1,
        )
    return f"<div class='{class_name} hebrew-block' dir='rtl' lang='he'>{safe_text}</div>"


def mixed_text_html(text):
    display = menukad_text(text)
    safe = escape(display)

    def wrap(match):
        return f"<span class='hebrew-inline' dir='rtl' lang='he'>{match.group(0)}</span>"

    return HEBREW_WORD_RE.sub(wrap, safe)


def get_pasukh_text(question, flow=None):
    if flow is not None:
        return flow.get("pasuk", "")
    return question.get("pasuk") or question.get("selected_word") or question.get("word", "")


def get_active_pasuk_ref(pasuk_text):
    for record in active_pesukim_records():
        if record.get("text") != pasuk_text:
            continue
        ref = record.get("ref", {})
        if not ref:
            return record.get("pasuk_id", "unknown")
        return f"{ref.get('sefer')} {ref.get('perek')}:{ref.get('pasuk')}"
    return "not in active parsed dataset"


def get_source_label(question, flow=None):
    if flow is not None:
        return flow.get("source", "generated")
    return question.get("source") or question.get("standard") or "generated"


def diagnostics_enabled():
    if os.environ.get("CHUMASH_ASSESSMENT_DEBUG", "").lower() in {"1", "true", "yes", "on"}:
        return True

    try:
        value = st.query_params.get("assessment_debug", "")
    except Exception:
        value = ""
    if isinstance(value, list):
        value = value[0] if value else ""
    return str(value).lower() in {"1", "true", "yes", "on"}


def developer_debug_enabled():
    if not diagnostics_enabled():
        return False
    return bool(st.session_state.get("developer_debug_mode", True))


def question_pipeline_source(question, flow=None):
    if flow is not None:
        return "generated flow from active parsed dataset"
    return question.get("_assessment_source", "generated from active parsed dataset")


def question_cache_status(question, flow=None):
    if flow is not None:
        return "flow list uses Streamlit cache after first build"
    return question.get(
        "_cache_status",
        "eligible pasuk pool may be cached; question regenerated for current request",
    )


def diagnostic_payload(question=None, flow=None, mode="unknown"):
    pasuk = get_pasukh_text(question or {}, flow)
    scope = active_scope_summary()
    return {
        "active_scope": scope["scope"],
        "active_range": {
            "first": scope["first_ref"],
            "last": scope["last_ref"],
            "pesukim_count": scope["pesukim_count"],
        },
        "mode": mode,
        "current_pasuk_ref": get_active_pasuk_ref(pasuk) if pasuk else "none",
        "current_question_type": (question or {}).get("question_type")
        or (question or {}).get("skill")
        or "none",
        "question_source": question_pipeline_source(question or {}, flow),
        "cache_status": question_cache_status(question or {}, flow),
        "question_in_active_dataset": pasuk in set(active_pasuk_texts()) if pasuk else False,
    }


def render_assessment_diagnostics(question=None, flow=None, mode="unknown"):
    if not diagnostics_enabled():
        return

    with st.sidebar.expander("Assessment Diagnostics", expanded=False):
        st.session_state.developer_debug_mode = st.checkbox(
            "Developer debug panel",
            value=st.session_state.get("developer_debug_mode", True),
            help="Show hidden quiz instrumentation for generation and transition paths.",
        )
        st.json(diagnostic_payload(question, flow, mode))


def append_attempt_log(question, choice, is_correct):
    pasuk_text = question.get("pasuk")
    record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "word": question.get("word"),
        "selected_word": question.get("selected_word"),
        "skill": question.get("skill"),
        "question_type": question.get("question_type"),
        "standard": question.get("standard"),
        "is_correct": is_correct,
        "expected_answer": question.get("correct_answer"),
        "user_answer": choice,
        "pasuk_ref": get_active_pasuk_ref(pasuk_text) if pasuk_text else None,
        "source": question.get("source"),
    }

    try:
        ATTEMPT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with ATTEMPT_LOG_PATH.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:
        return


def handle_answer(choice, question, progress):
    from runtime.session_state import (
        is_tense_family_skill,
        schedule_post_answer_action_visibility,
        set_adaptive_status,
    )

    if st.session_state.answered:
        return

    pipeline_started_at = perf_counter()
    st.session_state.last_answer_submitted_at = pipeline_started_at
    st.session_state.answered = True
    st.session_state.selected_answer = choice
    schedule_post_answer_action_visibility()
    st.session_state.questions_answered += 1
    if question.get("difficulty") == 5:
        st.session_state.level5_answered += 1
    is_correct = choice == question["correct_answer"]
    attempt_log_started_at = perf_counter()
    append_attempt_log(question, choice, is_correct)
    attempt_log_ms = round((perf_counter() - attempt_log_started_at) * 1000, 1)
    pilot_log_started_at = perf_counter()
    record_pilot_answer(question, choice, is_correct)
    pilot_log_ms = round((perf_counter() - pilot_log_started_at) * 1000, 1)
    scoring_started_at = perf_counter()
    progress_result = record_answer(
        progress,
        question,
        is_correct,
        None if is_correct else get_error_type(question.get("skill")),
    )
    scoring_ms = round((perf_counter() - scoring_started_at) * 1000, 1)
    answered_skill = question.get("skill", question.get("standard", "unknown"))
    full_skill_state = dict(progress.get("skills", {}).get(answered_skill, {}))
    if progress_result.get("skill_state", {}).get("point_change"):
        full_skill_state["point_change"] = progress_result["skill_state"]["point_change"]
    st.session_state.last_skill_state = full_skill_state
    asked_token = question.get("selected_word") or question.get("word")
    word_score_ms = 0.0
    if asked_token and update_word_skill_score is not None:
        word_score_started_at = perf_counter()
        update_word_skill_score(
            asked_token,
            question.get("skill", question.get("standard", "unknown")),
            is_correct,
            progress,
        )
        word_score_ms = round((perf_counter() - word_score_started_at) * 1000, 1)
    if asked_token:
        st.session_state.asked_tokens.append(asked_token)
        if (
            question.get("skill") in {"phrase", "phrase_translation"}
            or question.get("question_type") == "phrase_meaning"
        ):
            st.session_state.recent_phrases.append(asked_token)
            st.session_state.recent_phrases = st.session_state.recent_phrases[-10:]
    if question.get("id"):
        st.session_state.asked_question_ids.append(question["id"])
    if question.get("question_format"):
        st.session_state.recent_question_formats.append(question["question_format"])
        st.session_state.recent_question_formats = st.session_state.recent_question_formats[-10:]

    answered_skill = question.get("skill")
    if st.session_state.get("practice_type") == "Learn Mode" and is_tense_family_skill(answered_skill):
        st.session_state.pending_tense_contrast_followup = not is_correct
    elif answered_skill and not is_tense_family_skill(answered_skill):
        st.session_state.pending_tense_contrast_followup = False

    if (
        st.session_state.get("practice_type") == "Learn Mode"
        and answered_skill == progress.get("current_skill")
    ):
        adaptive_started_at = perf_counter()
        current_skill = progress.get("current_skill")
        next_skill_label = skill_path_label(get_next_skill(current_skill))
        decision = evaluate_skill_progression(
            current_skill=current_skill,
            answered_skill=answered_skill,
            skill_state=st.session_state.last_skill_state,
            is_correct=is_correct,
            skill_order=SKILL_ORDER,
            skill_label=skill_path_label(current_skill),
            next_skill_label=next_skill_label,
        )
        decision.update(build_selection_preferences(decision, question))
        set_adaptive_status(decision)
        progress.setdefault("adaptive_state", {}).setdefault("history", []).append(decision)
        progress["adaptive_state"]["history"] = progress["adaptive_state"]["history"][-20:]
        progress["adaptive_state"]["last_decision"] = decision

        target_skill = decision.get("target_skill", current_skill)
        if target_skill != current_skill:
            progress["current_skill"] = target_skill
            st.session_state.asked_tokens = []
            st.session_state.asked_question_ids = []
            st.session_state.asked_pasuks = []
        st.session_state.unlocked_skill_message = ""
        adaptive_ms = round((perf_counter() - adaptive_started_at) * 1000, 1)
    else:
        adaptive_ms = 0.0

    save_started_at = perf_counter()
    save_progress(progress)
    save_progress_ms = round((perf_counter() - save_started_at) * 1000, 1)
    st.session_state.last_answer_pipeline_timing = {
        "attempt_log_ms": attempt_log_ms,
        "pilot_log_ms": pilot_log_ms,
        "scoring_ms": scoring_ms,
        "word_score_ms": word_score_ms,
        "adaptive_ms": adaptive_ms,
        "save_progress_ms": save_progress_ms,
        "total_ms": round((perf_counter() - pipeline_started_at) * 1000, 1),
    }


def last_answer_was_correct(question):
    return st.session_state.selected_answer == question["correct_answer"]


def get_system_pasuks():
    return list(active_pasuk_texts())
