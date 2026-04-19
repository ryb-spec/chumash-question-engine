import streamlit as st

from runtime.presentation import SKILL_ORDER
from runtime.question_flow import remember_recent_question
from runtime.runtime_support import diagnostics_enabled


def reset_for_new_question():
    st.session_state.current_question = None
    st.session_state.answered = False
    st.session_state.selected_answer = None
    st.session_state.last_skill_state = None


def set_question(question):
    st.session_state.current_question = question
    st.session_state.answered = False
    st.session_state.selected_answer = None
    st.session_state.last_skill_state = None
    remember_recent_question(question)


def clear_transient_quiz_messages():
    st.session_state.unlocked_skill_message = ""
    st.session_state.feature_fallback_message = ""
    st.session_state.adaptive_status_message = ""
    st.session_state.adaptive_status_reason = ""
    st.session_state.adaptive_status_level = "info"


def transition_to_question(question):
    clear_transient_quiz_messages()
    set_question(question)
    st.rerun()


def set_adaptive_status(decision):
    decision = decision or {}
    st.session_state.adaptive_status_message = decision.get("message", "")
    st.session_state.adaptive_status_reason = decision.get("reason", "")
    route = decision.get("route", "")
    if route in {"advance", "fast_pass", "double_fast_pass"}:
        level = "success"
    elif route == "reteach_same_skill":
        level = "warning"
    else:
        level = "info"
    st.session_state.adaptive_status_level = level
    st.session_state.pending_adaptive_context = decision


def consume_adaptive_context():
    context = dict(st.session_state.get("pending_adaptive_context") or {})
    st.session_state.pending_adaptive_context = {}
    return context


def record_selected_pasuk(pasuk):
    asked_pasuks = st.session_state.setdefault("asked_pasuks", [])
    asked_pasuks.append(pasuk)
    st.session_state.asked_pasuks = asked_pasuks[-10:]
    recent_pesukim = st.session_state.setdefault("recent_pesukim", [])
    recent_pesukim.append(pasuk)
    st.session_state.recent_pesukim = recent_pesukim[-10:]


def get_generation_history(skill):
    if skill == "phrase_translation":
        return st.session_state.recent_phrases[-5:] + st.session_state.asked_tokens[-5:]
    if skill.startswith(("identify_", "segment_", "convert_", "match_")):
        return st.session_state.asked_question_ids
    return st.session_state.asked_tokens


def get_recent_question_formats():
    return st.session_state.setdefault("recent_question_formats", [])[-3:]


def get_recent_prefixes():
    return st.session_state.setdefault("recent_prefixes", [])[-5:]


def get_question_feature(question):
    skill = question.get("skill", "")
    question_type = question.get("question_type", "")
    standard = question.get("standard", "")

    if "prefix" in skill or "prefix" in question_type:
        return "prefix"
    if "suffix" in skill or "suffix" in question_type:
        return "suffix"
    if skill in {"translation", "phrase_translation"} or "meaning" in question_type:
        return "translation"
    if skill in {"verb_tense", "identify_tense", "identify_verb_marker"}:
        return "verb"
    if skill == "part_of_speech":
        return "part_of_speech"
    if standard == "SR":
        return "verb"
    return skill or standard or "unknown"


def get_question_prefix(question):
    if question.get("prefix"):
        return question["prefix"]
    if get_question_feature(question) != "prefix":
        return ""
    word = question.get("selected_word") or question.get("word") or ""
    if word and word[0] in {"ו", "ב", "ל", "מ", "כ", "ה", "ש"}:
        return word[0]
    return ""


def prefix_is_blocked(prefix):
    if not prefix:
        return False
    return get_recent_prefixes().count(prefix) >= 2


def record_question_prefix(question):
    prefix = get_question_prefix(question)
    if not prefix:
        return
    st.session_state.recent_prefixes.append(prefix)
    st.session_state.recent_prefixes = st.session_state.recent_prefixes[-10:]


def feature_is_blocked(feature):
    recent_features = st.session_state.setdefault("recent_features", [])
    controlled_features = {"prefix", "translation", "verb", "suffix", "part_of_speech"}
    if feature not in controlled_features:
        return False
    return recent_features[-5:].count(feature) >= 2


def record_question_feature(question):
    feature = get_question_feature(question)
    st.session_state.recent_features.append(feature)
    st.session_state.recent_features = st.session_state.recent_features[-10:]


def init_session_state():
    st.session_state.setdefault("mode", "Adaptive")
    st.session_state.setdefault("current_question", None)
    st.session_state.setdefault("answered", False)
    st.session_state.setdefault("selected_answer", None)
    st.session_state.setdefault("flow_step", 0)
    st.session_state.setdefault("flow_label", "")
    st.session_state.setdefault("questions_answered", 0)
    st.session_state.setdefault("level5_answered", 0)
    st.session_state.setdefault("last_skill_state", None)
    st.session_state.setdefault("asked_tokens", [])
    st.session_state.setdefault("asked_question_ids", [])
    st.session_state.setdefault("asked_pasuks", [])
    st.session_state.setdefault("recent_questions", [])
    st.session_state.setdefault("recent_pesukim", [])
    st.session_state.setdefault("recent_phrases", [])
    st.session_state.setdefault("recent_question_formats", [])
    st.session_state.setdefault("recent_features", [])
    st.session_state.setdefault("recent_prefixes", [])
    st.session_state.setdefault("feature_fallback_message", "")
    st.session_state.setdefault("practice_type", "Learn Mode")
    st.session_state.setdefault("practice_skill", SKILL_ORDER[0])
    st.session_state.setdefault("unlocked_skill_message", "")
    st.session_state.setdefault("adaptive_status_message", "")
    st.session_state.setdefault("adaptive_status_reason", "")
    st.session_state.setdefault("adaptive_status_level", "info")
    st.session_state.setdefault("pending_adaptive_context", {})
    st.session_state.setdefault("show_nekudos", True)
    st.session_state.setdefault("pasuk_view_mode", "Full pasuk view")
    st.session_state.setdefault("developer_debug_mode", diagnostics_enabled())
    st.session_state.setdefault("last_answer_submitted_at", None)
