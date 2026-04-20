"""Supported Chumash assessment runtime.

This Streamlit app is the supported student-facing runtime for the project.
It uses the active local parsed dataset and shared generator logic.
"""

import json
import os
import re
from datetime import datetime, timezone
from html import escape
from time import perf_counter

import streamlit as st

from adaptive_engine import (
    build_selection_preferences,
    evaluate_skill_progression,
)
from assessment_scope import (
    ACTIVE_ASSESSMENT_SCOPE,
    SUPPORTED_PRACTICE_TYPES,
    active_pesukim_records,
    active_pasuk_texts,
    active_scope_summary,
    data_path,
    repo_path,
)
from progress_store import load_progress_state, record_answer, save_progress_state
from runtime.mode_handlers import (
    render_flow_overview,
    render_mastery_mode,
    render_pasuk_flow,
    render_skill_practice_mode,
)
from runtime.pilot_logging import (
    PILOT_EVENT_LOG_PATH,
    TEACHER_FLAG_LABELS,
    TEACHER_FLAG_NOTE_MAX_LENGTH,
    build_pilot_review_export,
    current_session_review,
    record_pilot_answer,
    record_teacher_flag_label,
    record_teacher_flag_note,
)
from runtime.presentation import (
    MICRO_STANDARD_NAMES,
    MODE_LABELS,
    QUESTION_TYPE_NAMES,
    SKILL_NAMES,
    SKILL_ORDER,
    get_error_type,
    get_next_skill,
    get_next_skill_by_steps,
    get_skill_level,
    get_skill_xp_progress,
    learning_goal,
    next_goal_message,
    plain_skill,
    skill_path_label,
    thinking_tip,
)
from runtime.question_flow import (
    attach_debug_trace,
    build_followup_question,
    build_quiz_debug_payload,
    candidate_quality_breakdown,
    choice_similarity,
    current_routing_mode,
    distractor_separation_score,
    display_context_policy,
    finalize_transition_debug,
    generate_mastery_question,
    generate_practice_question,
    increment_debug_rejection_count,
    is_explicit_reteach_mode,
    progress_source_label,
    question_prompt_family,
    question_signature,
    recent_question_repeat_reason,
    recent_question_signature_key,
    skip_reason_codes,
    summarize_debug_rejection_counts,
    timed_question_generation,
    answer_to_next_ready_ms,
    choose_weighted_pasuk_question,
    select_pasuk_first_question,
)
from runtime.session_state import (
    clear_transient_quiz_messages,
    consume_adaptive_context,
    feature_is_blocked,
    get_generation_history,
    get_question_feature,
    get_question_prefix,
    get_recent_prefixes,
    get_recent_question_formats,
    init_session_state,
    prefix_is_blocked,
    record_question_feature,
    record_question_prefix,
    record_selected_pasuk,
    reset_for_new_question,
    schedule_post_answer_action_visibility,
    set_adaptive_status,
    set_question,
    transition_to_question,
)
from skill_catalog import (
    ADAPTIVE_STANDARD_IDS,
    resolve_skill_id,
)
from torah_parser.word_bank_adapter import (
    adapt_word_bank_data,
    build_word_bank_metadata_index,
    normalize_hebrew_key,
)
from ui.render_feedback import render_feedback
from ui.render_question import (
    answer_choice_label,
    get_word_entry,
    highlight_display_text,
    highlight_focus,
    local_context_snippet,
    question_key,
    question_type_key,
    render_debug,
    render_enter_key_handler,
    render_grammar_clues,
    render_learning_header,
    render_pasukh_panel,
    render_question,
    render_quiz_debug_panel,
    split_pasuk_phrases,
    uses_compact_pasuk_context,
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


BASE_DIR = repo_path()
PROGRESS_PATH = repo_path("progress.json")
SKILL_PROGRESS_PATH = repo_path("skill_progress.json")
WORD_BANK_PATH = data_path("word_bank.json")
ATTEMPT_LOG_PATH = data_path("attempt_log.jsonl")

MODES = ["Adaptive", "WM", "PR", "CF", "PS", "SS", "CM", "Pasuk Flow"]
ADAPTIVE_STANDARDS = list(ADAPTIVE_STANDARD_IDS)
SYSTEM_PESUKIM = [
    "וילך האיש מביתו אל העיר",
    "ויתן האב לחם לבנו",
    "וישב האיש בביתו",
    "בְּרֵאשִׁית בָּרָא אֱלֹקִים אֵת הַשָּׁמַיִם וְאֵת הָאָרֶץ",
    "וְהָאָרֶץ הָיְתָה תֹהוּ וָבֹהוּ וְחֹשֶׁךְ עַל פְּנֵי תְהוֹם",
    "וַיֹּאמֶר אֱלֹקִים יְהִי אוֹר וַיְהִי אוֹר",
    "וַיַּרְא אֱלֹקִים אֶת הָאוֹר כִּי טוֹב",
    "וַיִּקְרָא אֱלֹקִים לָאוֹר יוֹם וְלַחֹשֶׁךְ קָרָא לָיְלָה",
    "וַיֹּאמֶר ה׳ אֶל אַבְרָם לֶךְ לְךָ מֵאַרְצְךָ",
    "וְאֶעֶשְׂךָ לְגוֹי גָּדוֹל וַאֲבָרֶכְךָ",
    "וַיֵּלֶךְ אַבְרָם כַּאֲשֶׁר דִּבֶּר אֵלָיו ה׳",
    "וַיֹּאמֶר אַבְרָם אֶל לוֹט אַל נָא תְהִי מְרִיבָה בֵּינִי וּבֵינֶךָ",
    "וַיֹּאמֶר יַעֲקֹב אֶל בָּנָיו לָמָּה תִּתְרָאוּ",
    "וַיֹּאמֶר יוֹסֵף אֶל אֶחָיו אֲנִי יוֹסֵף",
    "וַיֹּאמֶר פַּרְעֹה אֶל יוֹסֵף רְאֵה נָתַתִּי אֹתְךָ",
    "וַיֹּאמֶר ה׳ אֶל מֹשֶׁה לֶךְ אֶל פַּרְעֹה",
    "וַיֹּאמֶר מֹשֶׁה אֶל ה׳ מִי אָנֹכִי כִּי אֵלֵךְ",
    "וַיֹּאמֶר אֱלֹקִים אֶהְיֶה אֲשֶׁר אֶהְיֶה",
    "אָנֹכִי ה׳ אֱלֹקֶיךָ אֲשֶׁר הוֹצֵאתִיךָ מֵאֶרֶץ מִצְרַיִם",
    "לֹא תִרְצָח לֹא תִנְאָף לֹא תִגְנֹב",
    "כַּבֵּד אֶת אָבִיךָ וְאֶת אִמֶּךָ",
    "וְאָהַבְתָּ אֵת ה׳ אֱלֹקֶיךָ בְּכָל לְבָבְךָ",
    "וְהָיוּ הַדְּבָרִים הָאֵלֶּה עַל לְבָבֶךָ",
    "וְשִׁנַּנְתָּם לְבָנֶיךָ וְדִבַּרְתָּ בָּם",
    "ה׳ רֹעִי לֹא אֶחְסָר",
    "בִּנְאוֹת דֶּשֶׁא יַרְבִּיצֵנִי עַל מֵי מְנֻחוֹת יְנַהֲלֵנִי",
    "גַּם כִּי אֵלֵךְ בְּגֵיא צַלְמָוֶת לֹא אִירָא רָע",
    "שִׁירוּ לַה׳ שִׁיר חָדָשׁ שִׁירוּ לַה׳ כָּל הָאָרֶץ",
    "הוֹדוּ לַה׳ כִּי טוֹב כִּי לְעוֹלָם חַסְדּוֹ",
    "אֶשָּׂא עֵינַי אֶל הֶהָרִים מֵאַיִן יָבֹא עֶזְרִי",
    "עֶזְרִי מֵעִם ה׳ עֹשֵׂה שָׁמַיִם וָאָרֶץ",
    "אֲנִי לְדוֹדִי וְדוֹדִי לִי",
    "קוֹל דּוֹדִי דּוֹפֵק פִּתְחִי לִי אֲחֹתִי",
]
MIN_QUESTIONS_BEFORE_LEVEL5 = 10
MAX_LEVEL5_SESSION_RATIO = 0.2
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


def save_progress(progress):
    return save_progress_state(progress)


def reset_assessment_state():
    for path in [PROGRESS_PATH, SKILL_PROGRESS_PATH]:
        if path.exists():
            path.unlink()

    st.session_state.clear()
    st.session_state.diagnostic_complete = False
    st.session_state.diagnostic_data = {}
    st.session_state.skill_progress = {}
    st.session_state.current_skill = None
    st.session_state.recent_words = []
    st.session_state.recent_pesukim = []
    st.session_state.recent_phrases = []
    st.session_state.recent_questions = []
    st.session_state.developer_debug_mode = diagnostics_enabled()
    st.session_state.last_answer_submitted_at = None
    st.session_state.recent_features = []
    st.session_state.recent_prefixes = []
    st.session_state.adaptive_status_message = ""
    st.session_state.adaptive_status_reason = ""
    st.session_state.adaptive_status_level = "info"
    st.session_state.pending_adaptive_context = {}
    st.rerun()


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


def clue_sentence(question):
    entry = get_word_entry(question)
    if entry:
        clues = []
        if entry.get("prefix"):
            clues.append(f"{entry['prefix']} points to '{entry.get('prefix_meaning', '')}'")
        if entry.get("suffix"):
            clues.append(f"{entry['suffix']} at the end points to '{entry.get('suffix_meaning', '')}'")
        if entry.get("shoresh"):
            clues.append(f"the root is {entry['shoresh']}")
        if clues:
            return "; ".join(clues)

    if question.get("question_type") == "substitution":
        return "the changed word changes the job of the phrase"
    if question.get("question_type") in {"flow", "flow_dependency"}:
        return "the order of the clues shows how the action moves"
    if question.get("question_type") == "role_clarity":
        return "the word's place in the sentence shows its job"
    return "the nearby words support the correct meaning"


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
        # Logging is best-effort only; assessment flow should continue even if
        # the local attempt log is unavailable or unwritable.
        return


def handle_answer(choice, question, progress):
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
    if asked_token:
        if update_word_skill_score is not None:
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


@st.cache_data
def get_skill_ready_pasuks(skill):
    if generate_skill_question is None:
        return []

    ready = []
    for pasuk in active_pasuk_texts():
        try:
            question = generate_skill_question(
                skill,
                (
                    analyze_generator_pasuk(pasuk)
                    if analyze_generator_pasuk is not None
                    else pasuk
                ),
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
            }
        )
    return ready


def select_system_pasuk(skill):
    if generate_skill_question is None:
        return None

    recent_pesukim = st.session_state.setdefault("recent_pesukim", [])
    candidates = [row["pasuk"] for row in get_skill_ready_pasuks(skill)]

    if not candidates:
        return None

    recent_window = recent_pesukim[-5:]
    unused = [
        pasuk
        for pasuk in candidates
        if pasuk not in st.session_state.asked_pasuks
        and pasuk not in recent_window
    ]
    attempts = 0
    while not unused and attempts < 10:
        attempts += 1
        st.session_state.asked_pasuks = []
        unused = [
            pasuk
            for pasuk in candidates
            if pasuk not in recent_window
        ]

    if not unused:
        st.session_state.asked_pasuks = []
        unused = candidates

    return unused[0]


def get_strengths(progress):
    standards = progress.get("standards", {})
    return sorted(standards.items(), key=lambda item: item[1], reverse=True)[:3]


def get_weak_areas(progress):
    standards = progress.get("standards", {})
    return sorted(standards.items(), key=lambda item: item[1])[:3]


def get_next_focus(progress):
    weak_areas = get_weak_areas(progress)
    if not weak_areas:
        return plain_skill("WM")
    return plain_skill(weak_areas[0][0])


def render_unlocks(progress):
    standards = progress.get("standards", {})
    level5_ready = st.session_state.questions_answered >= MIN_QUESTIONS_BEFORE_LEVEL5
    level5_ratio_ok = (
        st.session_state.questions_answered == 0
        or (st.session_state.level5_answered + 1)
        / (st.session_state.questions_answered + 1)
        <= MAX_LEVEL5_SESSION_RATIO
    )

    unlocks = {
        "SS": standards.get("WM", 0) >= 60 or standards.get("PS", 0) >= 60,
        "CM": standards.get("SS", 0) >= 50 or standards.get("CF", 0) >= 60,
        "Level 5": level5_ready and level5_ratio_ok,
    }

    st.sidebar.markdown("### New challenges")
    for name, unlocked in unlocks.items():
        st.sidebar.write(f"{plain_skill(name)}: {'Ready' if unlocked else 'Keep practicing'}")


def render_dashboard(progress):
    st.sidebar.markdown("### Your learning map")

    st.sidebar.markdown("**Strengths**")
    for standard, score in get_strengths(progress):
        st.sidebar.write(f"{plain_skill(standard)}: {score}")

    st.sidebar.markdown("**Needs More Practice**")
    for standard, score in get_weak_areas(progress):
        st.sidebar.write(f"{plain_skill(standard)}: {score}")

    st.sidebar.markdown("**Next Step**")
    st.sidebar.info(get_next_focus(progress))

    st.sidebar.markdown("### Practice growth")
    for standard in ADAPTIVE_STANDARDS:
        xp = progress.get("xp", {}).get(standard, 0)
        score = progress.get("standards", {}).get(standard, 0)
        st.sidebar.write(
            f"{plain_skill(standard)}: Practice level {get_skill_level(xp)}"
        )
        st.sidebar.caption(next_goal_message(score))


def render_teacher_pilot_monitor(progress):
    review_export = build_pilot_review_export(max_sessions=8)
    session_review = current_session_review()

    with st.sidebar.expander("Pilot Monitor", expanded=False):
        st.caption(f"Session: {st.session_state.get('pilot_session_id', 'unknown')}")
        if session_review:
            st.write(f"Served: {session_review.get('served_questions', 0)}")
            st.write(
                "Answered: "
                f"{session_review.get('answered_questions', 0)} "
                f"({session_review.get('correct_answers', 0)} correct / "
                f"{session_review.get('incorrect_answers', 0)} incorrect)"
            )
            st.write(f"Flagged unclear: {session_review.get('flagged_unclear', 0)}")
            scope_status = session_review.get("session_scope_status", "open_pilot_scope")
            if scope_status == "trusted_active_scope":
                st.write("Pilot scope: trusted active parsed scope")
            elif scope_status == "outside_active_scope_detected":
                st.write("Pilot scope: not trusted; outside active parsed scope was served")
            else:
                st.write("Pilot scope: open pilot scope")
            served_question_types = session_review.get("served_question_types", {})
            if served_question_types:
                st.write(
                    "Current session families: "
                    + ", ".join(
                        f"{question_type}: {count}"
                        for question_type, count in served_question_types.items()
                    )
                )
            if session_review.get("average_response_time_ms") is not None:
                st.write(f"Average response time: {session_review['average_response_time_ms']} ms")

        st.markdown("#### Recent Sessions")
        for session in review_export.get("sessions", [])[:5]:
            practice_mix = session.get("practice_types", {})
            scope_status = session.get("session_scope_status", "open_pilot_scope")
            if scope_status == "trusted_active_scope":
                scope_label = "trusted active parsed scope"
            elif scope_status == "outside_active_scope_detected":
                scope_label = "outside active scope detected"
            else:
                scope_label = "open pilot scope"

            st.markdown(
                f"**{session.get('session_id', 'unknown')}**"
                f" | served {session.get('served_questions', 0)}"
                f" | answered {session.get('answered_questions', 0)}"
                f" | unclear {session.get('flagged_unclear', 0)}"
            )
            if practice_mix:
                st.caption(
                    "Practice: "
                    + ", ".join(f"{name}: {count}" for name, count in practice_mix.items())
                )
            served_mix = session.get("served_question_types", {})
            if served_mix:
                st.caption(
                    "Families: "
                    + ", ".join(f"{name}: {count}" for name, count in served_mix.items())
                )
            st.caption(f"Scope: {scope_label}")

        st.markdown("#### Flagged Review Queue")
        flagged_queue = review_export.get("flagged_review_queue", [])
        if not flagged_queue:
            st.caption("No flagged unclear items yet.")
        for item in flagged_queue[:8]:
            st.markdown(
                f"**{item.get('pasuk_ref') or 'Unknown ref'}**"
                f" | {item.get('question_type') or 'unknown'}"
                f" | session {item.get('session_id') or 'unknown'}"
            )
            st.caption(item.get("question_text") or "")
            if item.get("selected_word"):
                st.caption(f"Word: {item['selected_word']}")
            if item.get("student_note"):
                st.caption(f"Student note: {item['student_note']}")
            if item.get("repeat_count", 0) > 1:
                st.caption(f"Repeated flag count: {item['repeat_count']}")
            current_label = item.get("teacher_label")
            current_teacher_note = item.get("teacher_note") or ""
            label_options = [""] + list(TEACHER_FLAG_LABELS)
            default_index = label_options.index(current_label) if current_label in label_options else 0
            select_key = f"teacher_flag_label_{item.get('question_log_id')}"
            note_key = f"teacher_flag_note_{item.get('question_log_id')}"
            selected_label = st.selectbox(
                "Teacher label",
                label_options,
                index=default_index,
                key=select_key,
                label_visibility="collapsed",
            )
            teacher_note = st.text_area(
                "Teacher note",
                value=current_teacher_note,
                key=note_key,
                height=80,
                max_chars=TEACHER_FLAG_NOTE_MAX_LENGTH,
                placeholder="Optional: explain why this was unclear or how to improve it",
                label_visibility="collapsed",
            )
            if st.button(
                "Save review",
                key=f"save_teacher_flag_{item.get('question_log_id')}",
                use_container_width=True,
            ):
                saved = False
                if selected_label:
                    saved = record_teacher_flag_label(
                        item.get("question_log_id"),
                        selected_label,
                        session_id=item.get("session_id"),
                    ) or saved
                if teacher_note.strip():
                    saved = record_teacher_flag_note(
                        item.get("question_log_id"),
                        teacher_note,
                        session_id=item.get("session_id"),
                    ) or saved
                if saved:
                    st.rerun()
            if current_label:
                st.caption(f"Current label: {current_label}")
            if current_teacher_note:
                st.caption(f"Teacher note: {current_teacher_note}")

        st.markdown("#### Quick Pilot Summary")
        summary = review_export.get("summary", {})
        dominant_families = summary.get("dominant_served_question_families", {})
        if dominant_families:
            st.caption(
                "Dominant families: "
                + ", ".join(f"{name}: {count}" for name, count in dominant_families.items())
            )
        top_flagged = summary.get("top_repeated_flagged_items", [])
        if top_flagged:
            st.caption("Top repeated flagged items:")
            for item in top_flagged[:3]:
                st.write(
                    f"- {item.get('question_type')}: {item.get('repeat_count')} "
                    f"({item.get('pasuk_ref') or 'unknown ref'})"
                )
        high_unclear = summary.get("highest_unclear_rate_sessions", [])
        if high_unclear:
            st.caption("Highest unclear-rate sessions:")
            for item in high_unclear[:3]:
                st.write(
                    f"- {item.get('session_id')}: "
                    f"{item.get('flagged_unclear', 0)}/{item.get('served_questions', 0)} flagged"
                )
        violations = summary.get("trusted_scope_violations", [])
        if violations:
            st.caption("Trusted-scope violations:")
            for item in violations[:3]:
                st.write(
                    f"- {item.get('session_id')}: "
                    f"{item.get('served_outside_active_scope_questions', 0)} outside active scope"
                )

        st.download_button(
            "Export Recent Pilot Sessions",
            data=json.dumps(review_export, ensure_ascii=False, indent=2),
            file_name="pilot_review_export.json",
            mime="application/json",
            use_container_width=True,
        )
        st.caption(f"Log path: {PILOT_EVENT_LOG_PATH}")

    render_unlocks(progress)


def apply_global_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Hebrew:wght@400;500;700;800&display=swap');
        :root {
            --ink: #19211f;
            --muted: #65716d;
            --line: #d9e1de;
            --surface: #ffffff;
            --wash: #f4f7f6;
            --info: #2563a9;
            --info-soft: #eaf3ff;
            --accent: #21745a;
            --accent-soft: #e8f5ef;
            --danger: #b42318;
            --danger-soft: #fff0ed;
            --success: #16784d;
            --success-soft: #e8f7ee;
            --highlight: #fff4a3;
        }
        .stApp {
            background: linear-gradient(180deg, #f8faf9 0%, #eef4f2 100%);
            color: var(--ink);
        }
        .block-container {
            max-width: 980px;
            padding-top: 1.1rem;
            padding-bottom: 7rem;
        }
        h1 {
            letter-spacing: 0 !important;
        }
        .app-title {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            margin: 0 0 4px 0;
        }
        .app-title h1 {
            margin: 0 !important;
            font-size: 1.65rem !important;
            text-align: left;
        }
        .learning-header,
        .question-card,
        .pasuk-box,
        .compact-context,
        .flow-overview,
        .feedback-panel {
            border: 1px solid var(--line);
            border-radius: 8px;
            background: var(--surface);
            box-shadow: 0 4px 16px rgba(28, 45, 40, 0.05);
        }
        .learning-header {
            display: grid;
            gap: 4px;
            padding: 8px 12px;
            margin-bottom: 4px;
        }
        .focus-line {
            color: var(--muted);
            font-size: 0.86rem;
            line-height: 1.28;
            margin: 0;
        }
        .progress-note {
            color: var(--muted);
            font-size: 0.74rem;
            line-height: 1.2;
            margin: 0;
        }
        .meta-row,
        .learning-chips,
        .feedback-status {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            align-items: center;
        }
        .meta-row span,
        .learning-chips span {
            border: 1px solid var(--line);
            background: var(--wash);
            border-radius: 999px;
            color: var(--muted);
            font-size: 0.74rem;
            font-weight: 700;
            padding: 3px 8px;
        }
        .quiz-meta-row {
            margin-bottom: 0;
        }
        .mastery-chip {
            border-color: rgba(33, 116, 90, 0.18) !important;
            background: var(--accent-soft) !important;
            color: var(--accent);
            font-weight: 800;
        }
        .section-heading small {
            color: var(--muted);
            line-height: 1.35;
        }
        .feedback-detail,
        .reteach-panel {
            border: 1px solid var(--line);
            border-radius: 8px;
            background: #ffffff;
            padding: 10px 12px;
        }
        .feedback-detail span,
        .reteach-panel span {
            display: block;
            color: var(--muted);
            font-size: 0.8rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 4px;
        }
        .feedback-detail div,
        .reteach-panel div {
            margin: 0;
            line-height: 1.35;
            font-size: 0.92rem;
            font-weight: 650;
        }
        .section-label,
        .section-heading span {
            color: var(--muted);
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0;
            text-transform: uppercase;
        }
        .section-heading {
            display: flex;
            justify-content: space-between;
            gap: 10px;
            align-items: center;
            margin: 6px 0 3px 0;
        }
        .pasuk-box {
            padding: 18px 20px;
            margin: 0 0 6px 0;
            background: #fbfdfc;
            direction: rtl;
            text-align: center;
            font-family: "Noto Sans Hebrew", "SBL Hebrew", "Ezra SIL", "Taamey David CLM", "Times New Roman", serif;
            font-size: 2.15rem;
            font-weight: 700;
            line-height: 1.72;
            overflow-wrap: anywhere;
            unicode-bidi: plaintext;
        }
        .compact-context {
            margin: 0 0 4px 0;
            padding: 8px 10px;
            background: #fbfdfc;
            text-align: center;
        }
        .target-word {
            direction: rtl;
            font-family: "Noto Sans Hebrew", "SBL Hebrew", "Ezra SIL", "Taamey David CLM", "Times New Roman", serif;
            font-size: 1.95rem;
            font-weight: 800;
            line-height: 1.18;
            letter-spacing: 0;
            unicode-bidi: plaintext;
        }
        .context-snippet {
            margin-top: 2px;
            color: var(--muted);
            font-family: "Noto Sans Hebrew", "SBL Hebrew", "Ezra SIL", "Taamey David CLM", "Times New Roman", serif;
            font-size: 0.98rem;
            font-weight: 600;
            line-height: 1.28;
            letter-spacing: 0;
            unicode-bidi: plaintext;
        }
        .compact-full-pasuk {
            margin-bottom: 4px;
            font-size: 1.35rem;
            padding: 12px 14px;
        }
        .hebrew-block,
        .hebrew-text,
        .hebrew-inline,
        .phrase-text {
            direction: rtl;
            font-family: "Noto Sans Hebrew", "SBL Hebrew", "Ezra SIL", "Taamey David CLM", "Times New Roman", serif;
            line-height: 1.9;
            unicode-bidi: plaintext;
            letter-spacing: 0;
        }
        .hebrew-inline {
            display: inline;
            white-space: normal;
        }
        .phrase-box {
            display: grid;
            gap: 6px;
            text-align: right;
            font-size: 1.7rem;
        }
        .phrase-line {
            display: grid;
            grid-template-columns: 42px minmax(0, 1fr);
            gap: 10px;
            align-items: center;
            direction: ltr;
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 8px 10px;
            background: #ffffff;
        }
        .phrase-number,
        .flow-index {
            width: 32px;
            height: 32px;
            display: inline-grid;
            place-items: center;
            border-radius: 8px;
            background: var(--info-soft);
            color: var(--info);
            font-size: 0.9rem;
            font-weight: 800;
        }
        .question-card {
            padding: 12px 14px;
            margin: 4px 0 6px 0;
        }
        .question-arrival-target {
            scroll-margin-top: 56px;
            outline: none;
        }
        .question-arrival-target.question-arrival-active {
            box-shadow: 0 0 0 3px rgba(37, 99, 169, 0.18), 0 4px 16px rgba(28, 45, 40, 0.05);
        }
        .question-text {
            margin-top: 2px;
            font-size: 1.54rem;
            font-weight: 850;
            line-height: 1.28;
        }
        .answer-label {
            margin-top: 4px;
            margin-bottom: 4px;
        }
        div[data-testid="stRadio"] [role="radiogroup"] {
            display: grid;
            gap: 6px;
        }
        div[data-testid="stRadio"] label {
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 8px 10px;
            background: #ffffff;
            min-height: 44px;
            align-items: center;
            transition: border-color 120ms ease, background-color 120ms ease, transform 120ms ease;
        }
        div[data-testid="stRadio"] label:hover {
            border-color: var(--accent);
            background: var(--accent-soft);
            transform: translateY(-1px);
        }
        div[data-testid="stRadio"] label p {
            font-size: 0.96rem;
            font-weight: 650;
            line-height: 1.28;
            unicode-bidi: plaintext;
        }
        div[data-testid="stRadio"] {
            margin-bottom: 2px;
        }
        div.stButton > button {
            min-height: 44px;
            border-radius: 8px;
            font-weight: 800;
            font-size: 0.98rem;
            letter-spacing: 0;
        }
        div.stButton {
            margin-top: 2px;
        }
        div.stButton > button[kind="primary"] {
            background: var(--accent);
            border-color: var(--accent);
        }
        .feedback-panel {
            margin-top: 6px;
            padding: 10px 12px;
            border-left-width: 5px;
        }
        .feedback-panel.correct {
            border-left-color: var(--success);
            background: var(--success-soft);
        }
        .feedback-panel.incorrect {
            border-left-color: var(--danger);
            background: var(--danger-soft);
        }
        .post-answer-action-shell {
            margin-top: 8px;
            padding: 8px 12px 6px 12px;
            border: 1px solid var(--line);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.94);
            box-shadow: 0 4px 16px rgba(28, 45, 40, 0.06);
            backdrop-filter: blur(8px);
        }
        .post-answer-action-target {
            scroll-margin-top: 56px;
            outline: none;
        }
        .post-answer-action-note {
            margin-top: 4px;
            color: var(--muted);
            font-size: 0.92rem;
            font-weight: 650;
            line-height: 1.3;
        }
        [data-testid="stVerticalBlock"] > div:has(.post-answer-action-sentinel) ~ div div.stButton > button {
            position: sticky;
            bottom: max(0.8rem, env(safe-area-inset-bottom));
            z-index: 30;
            box-shadow: 0 10px 24px rgba(25, 33, 31, 0.14);
        }
        [data-testid="stVerticalBlock"] > div:has(.post-answer-action-sentinel) ~ div [data-testid="stSpinner"] {
            position: sticky;
            bottom: max(4.1rem, calc(env(safe-area-inset-bottom) + 3.3rem));
            z-index: 29;
            margin-top: 8px;
            padding: 8px 10px;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.96);
            border: 1px solid var(--line);
        }
        .feedback-status {
            justify-content: space-between;
            margin-bottom: 4px;
        }
        .feedback-status strong {
            font-size: 1.08rem;
        }
        .feedback-line {
            display: grid;
            grid-template-columns: 88px minmax(0, 1fr);
            gap: 8px;
            padding: 4px 0;
            border-top: 1px solid rgba(25, 33, 31, 0.08);
        }
        .feedback-line span {
            color: var(--muted);
            font-weight: 700;
            font-size: 0.82rem;
        }
        .feedback-line b,
        .feedback-line div {
            font-size: 0.94rem;
            line-height: 1.28;
        }
        .feedback-heading {
            margin-top: 4px;
            margin-bottom: 2px;
        }
        .feedback-clue div,
        .feedback-note div {
            font-weight: 700;
        }
        .feedback-detail-grid {
            display: grid;
            grid-template-columns: minmax(0, 1fr);
            gap: 8px;
            padding-top: 0;
            margin-top: 6px;
        }
        .reteach-panel {
            margin-top: 8px;
            background: #fff9ed;
            border-color: rgba(180, 35, 24, 0.18);
        }
        .flow-overview {
            padding: 12px;
            margin: 6px 0 12px 0;
        }
        .flow-grid {
            display: grid;
            gap: 8px;
        }
        .flow-row {
            display: grid;
            grid-template-columns: 42px minmax(0, 1fr);
            gap: 12px;
            align-items: center;
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 10px 12px;
            background: #ffffff;
        }
        .flow-row.active {
            border-color: var(--info);
            background: var(--info-soft);
        }
        .flow-row.complete {
            border-color: rgba(22, 120, 77, 0.35);
            background: var(--success-soft);
        }
        .flow-row strong {
            display: block;
            margin-bottom: 2px;
        }
        mark {
            background: var(--highlight);
            color: #111111;
            padding: 3px 8px;
            border-radius: 6px;
            box-decoration-break: clone;
            -webkit-box-decoration-break: clone;
        }
        [data-testid="stSidebar"] {
            background: #f7faf9;
            border-right: 1px solid var(--line);
        }
        [data-testid="stProgress"] > div {
            height: 12px;
            border-radius: 8px;
            background: #e4ebe8;
        }
        [data-testid="stProgress"] div[role="progressbar"] {
            background: var(--accent);
        }
        @media (max-width: 820px) {
            .block-container {
                padding-left: 0.8rem;
                padding-right: 0.8rem;
            }
            .pasuk-box {
                font-size: 1.75rem;
                padding: 14px 16px;
                line-height: 1.65;
            }
            .target-word {
                font-size: 1.75rem;
            }
            .context-snippet {
                font-size: 0.96rem;
            }
            .compact-full-pasuk {
                font-size: 1.18rem;
                padding: 10px 12px;
            }
            .phrase-box {
                font-size: 1.35rem;
            }
            .question-text {
                font-size: 1.28rem;
            }
            .feedback-line {
                grid-template-columns: 1fr;
                gap: 2px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    st.set_page_config(page_title="Chumash Quiz", layout="wide")
    init_session_state()
    apply_global_styles()

    progress = load_progress()

    st.markdown(
        """
        <header class="app-title">
            <div>
                <h1>Chumash Practice</h1>
            </div>
        </header>
        """,
        unsafe_allow_html=True,
    )
    focus_mode = st.sidebar.toggle("Focus Mode", value=True)
    st.sidebar.toggle("Show Nekudos", value=True, key="show_nekudos")
    st.sidebar.radio(
        "Pasuk display",
        ["Full pasuk view", "Break into phrases"],
        key="pasuk_view_mode",
    )
    if st.sidebar.button("Restart Assessment", type="secondary"):
        reset_assessment_state()

    practice_options = list(SUPPORTED_PRACTICE_TYPES)
    current_practice_type = (
        st.session_state.practice_type
        if st.session_state.practice_type in practice_options
        else "Learn Mode"
    )
    practice_type = st.sidebar.radio(
        "Practice type",
        practice_options,
        index=practice_options.index(current_practice_type),
    )
    if practice_type != st.session_state.practice_type:
        st.session_state.practice_type = practice_type
        st.session_state.asked_tokens = []
        st.session_state.asked_question_ids = []
        st.session_state.asked_pasuks = []
        reset_for_new_question()
        st.rerun()

    current_skill = progress["current_skill"]
    next_skill = get_next_skill(current_skill)
    st.sidebar.markdown("### Skill path")
    st.sidebar.write(f"Current skill: **{skill_path_label(current_skill)}**")
    st.sidebar.write(f"Next skill: **{skill_path_label(next_skill)}**")
    render_teacher_pilot_monitor(progress)

    if not focus_mode:
        st.sidebar.caption(
            "Hard explanation questions used: "
            f"{st.session_state.level5_answered}/{st.session_state.questions_answered} "
            f"(practice a bit first; these stay occasional)"
        )
        render_dashboard(progress)

    if practice_type == "Learn Mode":
        render_mastery_mode(progress)
    elif practice_type == "Pasuk Flow":
        render_pasuk_flow(progress)
    else:
        current_practice_skill = resolve_skill_id(st.session_state.practice_skill) or st.session_state.practice_skill
        practice_index = SKILL_ORDER.index(current_practice_skill) if current_practice_skill in SKILL_ORDER else 0
        practice_skill = st.sidebar.selectbox(
            "Choose a skill to practice",
            SKILL_ORDER,
            index=practice_index,
            format_func=skill_path_label,
        )
        if practice_skill != st.session_state.practice_skill:
            st.session_state.practice_skill = practice_skill
            st.session_state.asked_tokens = []
            st.session_state.asked_question_ids = []
            st.session_state.asked_pasuks = []
            reset_for_new_question()
            st.rerun()
        render_skill_practice_mode(progress, practice_skill)


if __name__ == "__main__":
    main()
