import streamlit as st

from runtime.pilot_logging import ensure_pilot_session_id
from runtime.presentation import SKILL_ORDER
from runtime.question_flow import remember_recent_question
from runtime.runtime_support import diagnostics_enabled


MECHANICAL_MORPHEME_FAMILIES = {
    "prefix_letter",
    "suffix_meaning",
    "pronoun_suffix",
    "verb_marker",
    "segment_word_parts",
}
MECHANICAL_SKILLS = {
    "identify_prefix_meaning",
    "identify_suffix_meaning",
    "identify_pronoun_suffix",
    "identify_verb_marker",
    "segment_word_parts",
    "prefix",
    "suffix",
}
MEANING_SKILLS = {
    "translation",
    "shoresh",
    "part_of_speech",
    "preposition_meaning",
}
VERB_BUILDING_SKILLS = {
    "identify_tense",
    "identify_prefix_future",
    "identify_suffix_past",
    "identify_present_pattern",
    "convert_future_to_command",
    "match_pronoun_to_verb",
    "verb_tense",
}
CONTEXT_SKILLS = {
    "subject_identification",
    "object_identification",
    "phrase_translation",
}
OPENING_MECHANICAL_GROUP_WINDOW = 6
OPENING_MECHANICAL_GROUP_CAP = 2
MORPHEME_FAMILY_REPEAT_WINDOW = 6
MORPHEME_FAMILY_REPEAT_CAP = 2
POST_MECHANICAL_COOLDOWN_NON_MECHANICAL = 4


def reset_for_new_question():
    st.session_state.current_question = None
    st.session_state.answered = False
    st.session_state.selected_answer = None
    st.session_state.last_skill_state = None
    st.session_state.pilot_current_question_signature = ""
    st.session_state.pilot_current_question_log_id = None
    st.session_state.pilot_current_question_started_at = None


def set_question(question):
    st.session_state.current_question = question
    st.session_state.answered = False
    st.session_state.selected_answer = None
    st.session_state.last_skill_state = None
    st.session_state.pilot_current_question_signature = ""
    st.session_state.pilot_current_question_log_id = None
    st.session_state.pilot_current_question_started_at = None
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


def get_recent_morpheme_families():
    return st.session_state.setdefault("recent_morpheme_families", [])[-10:]


def get_recent_question_groups():
    return st.session_state.setdefault("recent_question_groups", [])[-12:]


def get_recent_instructional_groups():
    return st.session_state.setdefault("recent_instructional_groups", [])[-12:]


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


def get_morpheme_family(question):
    skill = (question.get("skill", "") or "").lower()
    question_type = (question.get("question_type", "") or "").lower()

    if "identify_prefix_letter" in question_type:
        return "prefix_letter"
    if skill == "identify_suffix_meaning" or "identify_suffix_meaning" in question_type:
        return "suffix_meaning"
    if skill == "identify_pronoun_suffix" or "identify_pronoun_suffix" in question_type:
        return "pronoun_suffix"
    if skill == "identify_verb_marker" or "identify_verb_marker" in question_type:
        return "verb_marker"
    if skill == "segment_word_parts":
        return "segment_word_parts"
    return ""


def get_instructional_group(question_or_skill):
    if isinstance(question_or_skill, str):
        skill = question_or_skill
        question_type = ""
    else:
        question = question_or_skill or {}
        skill = question.get("skill", "") or question.get("question_type", "")
        question_type = question.get("question_type", "") or ""

    skill = (skill or "").lower()
    question_type = (question_type or "").lower()

    if skill in MECHANICAL_SKILLS or "prefix" in question_type or "suffix" in question_type:
        return "mechanical"
    if skill in CONTEXT_SKILLS or question_type in {"phrase_translation", "subject_identification", "object_identification"}:
        return "context"
    if skill in VERB_BUILDING_SKILLS:
        return "verb_building"
    if skill in MEANING_SKILLS or "meaning" in question_type or question_type == "translation":
        return "meaning"
    return "other"


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


def morpheme_family_is_blocked(family):
    if (
        st.session_state.get("practice_type", "Learn Mode") != "Learn Mode"
        or family not in MECHANICAL_MORPHEME_FAMILIES
    ):
        return False

    recent_families = get_recent_morpheme_families()
    if recent_families and recent_families[-1] == family:
        return True
    return recent_families[-MORPHEME_FAMILY_REPEAT_WINDOW:].count(family) >= MORPHEME_FAMILY_REPEAT_CAP


def mechanical_group_cooldown_is_blocked(family):
    if (
        st.session_state.get("practice_type", "Learn Mode") != "Learn Mode"
        or family not in MECHANICAL_MORPHEME_FAMILIES
    ):
        return False

    recent_groups = get_recent_question_groups()
    mechanical_positions = [
        index for index, group in enumerate(recent_groups) if group == "mechanical"
    ]
    if len(mechanical_positions) < 2:
        return False

    latest_mechanical = mechanical_positions[-1]
    since_latest = recent_groups[latest_mechanical + 1:]
    non_mechanical_since_latest = since_latest.count("other")
    return non_mechanical_since_latest < POST_MECHANICAL_COOLDOWN_NON_MECHANICAL


def mechanical_group_is_capped(family):
    if (
        st.session_state.get("practice_type", "Learn Mode") != "Learn Mode"
        or family not in MECHANICAL_MORPHEME_FAMILIES
    ):
        return False

    recent_groups = get_recent_question_groups()
    if len(recent_groups) >= OPENING_MECHANICAL_GROUP_WINDOW:
        return False
    return recent_groups.count("mechanical") >= OPENING_MECHANICAL_GROUP_CAP


def record_question_prefix(question):
    prefix = get_question_prefix(question)
    if not prefix:
        return
    st.session_state.recent_prefixes.append(prefix)
    st.session_state.recent_prefixes = st.session_state.recent_prefixes[-10:]


def record_question_morpheme_family(question):
    family = get_morpheme_family(question)
    if not family:
        return
    st.session_state.recent_morpheme_families.append(family)
    st.session_state.recent_morpheme_families = st.session_state.recent_morpheme_families[-10:]


def record_question_group(question):
    family = get_morpheme_family(question)
    group = "mechanical" if family in MECHANICAL_MORPHEME_FAMILIES else "other"
    st.session_state.recent_question_groups.append(group)
    st.session_state.recent_question_groups = st.session_state.recent_question_groups[-12:]
    instructional_group = get_instructional_group(question)
    st.session_state.recent_instructional_groups.append(instructional_group)
    st.session_state.recent_instructional_groups = st.session_state.recent_instructional_groups[-12:]


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
    record_question_morpheme_family(question)
    record_question_group(question)


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
    st.session_state.setdefault("recent_morpheme_families", [])
    st.session_state.setdefault("recent_question_groups", [])
    st.session_state.setdefault("recent_instructional_groups", [])
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
    st.session_state.setdefault("last_answer_pipeline_timing", {})
    st.session_state.setdefault("pilot_session_id", None)
    st.session_state.setdefault("pilot_scope_mode", "trusted_active_scope")
    st.session_state.setdefault("pilot_trusted_active_scope_session", True)
    st.session_state.setdefault("pilot_current_question_signature", "")
    st.session_state.setdefault("pilot_current_question_log_id", None)
    st.session_state.setdefault("pilot_current_question_started_at", None)
    st.session_state.setdefault("pilot_flagged_question_log_ids", [])
    ensure_pilot_session_id()
