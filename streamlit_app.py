import json
import random
import re
from html import escape
from pathlib import Path

import streamlit as st

from skill_tracker import update_skill_progress

try:
    from pasuk_flow_generator import generate_question as generate_skill_question
except ImportError:
    generate_skill_question = None


BASE_DIR = Path(__file__).parent
QUESTIONS_PATH = BASE_DIR / "questions.json"
PROGRESS_PATH = BASE_DIR / "progress.json"
PASUK_FLOWS_PATH = BASE_DIR / "pasuk_flows.json"
PASUK_FLOW_QUESTIONS_PATH = BASE_DIR / "pasuk_flow_questions.json"
WORD_BANK_PATH = BASE_DIR / "word_bank.json"

MODES = ["Adaptive", "WM", "PR", "CF", "PS", "SS", "CM", "Pasuk Flow"]
ADAPTIVE_STANDARDS = ["WM", "SR", "PR", "CF", "PC", "PS", "SS", "CM"]
SKILL_ORDER = [
    "identify_prefix_meaning",
    "identify_suffix_meaning",
    "identify_pronoun_suffix",
    "identify_verb_marker",
    "segment_word_parts",
    "identify_tense",
    "identify_prefix_future",
    "identify_suffix_past",
    "identify_present_pattern",
    "convert_future_to_command",
    "match_pronoun_to_verb",
    "part_of_speech",
    "shoresh",
    "prefix",
    "suffix",
    "translation",
    "verb_tense",
    "subject_identification",
    "object_identification",
    "preposition_meaning",
    "phrase_translation",
]
SYSTEM_PESUKIM = [
    "וילך האיש מביתו אל העיר",
    "ויתן האב לחם לבנו",
    "וישב האיש בביתו",
]
MIN_QUESTIONS_BEFORE_LEVEL5 = 10
MAX_LEVEL5_SESSION_RATIO = 0.2
HEBREW_WORD_RE = re.compile(r"[\u0590-\u05ff]+")
OPTION_LABELS = ["A", "B", "C", "D"]

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

SKILL_NAMES = {
    "Adaptive": "Recommended Practice",
    "WM": "Understanding words",
    "SR": "Finding the root of a word",
    "PR": "How words are built",
    "PS": "How words are built",
    "SS": "Who is doing what",
    "CM": "Understanding meaning from context",
    "CF": "How the sentence works",
    "PC": "Reading short phrases",
    "FLOW": "What happens in order",
    "Level 5": "Hard explanation questions",
    "Pasuk Flow": "Guided Pasuk Practice",
    "identify_prefix_meaning": "How words are built",
    "identify_suffix_meaning": "How words are built",
    "identify_pronoun_suffix": "How words are built",
    "identify_verb_marker": "How words are built",
    "segment_word_parts": "How words are built",
    "identify_tense": "How verbs are built",
    "identify_prefix_future": "How verbs are built",
    "identify_suffix_past": "How verbs are built",
    "identify_present_pattern": "How verbs are built",
    "convert_future_to_command": "How verbs are built",
    "match_pronoun_to_verb": "How verbs are built",
    "part_of_speech": "Parts of speech",
    "shoresh": "Finding the root",
    "prefix": "Prefixes",
    "suffix": "Suffixes",
    "translation": "Word meaning",
    "verb_tense": "Verb tense",
    "subject_identification": "Who is doing the action",
    "object_identification": "What the action happens to",
    "preposition_meaning": "Small direction words",
    "phrase_translation": "Phrase meaning",
}

QUESTION_TYPE_NAMES = {
    "flow": "What happens in order",
    "flow_dependency": "What happens in order",
    "substitution": "What changes if...",
    "reasoning": "Explain the meaning",
    "phrase_meaning": "How words work together",
    "role_clarity": "Who is doing what",
    "context_meaning": "Understanding meaning from context",
    "prefix_suffix": "How words are built",
    "word_meaning": "Understanding words",
}

MICRO_STANDARD_NAMES = {
    "WM1": "Match a Hebrew word to its meaning",
    "WM2": "Recognize the Hebrew word from English",
    "WM3": "Group related meanings",
    "WM4": "Tell close meanings apart",
    "WM5": "Understand abstract words",
    "PR1": "Recognize a prefix",
    "PR2": "Recognize an ending",
    "PR3": "Combine prefix and word",
    "PR4": "Combine word and ending",
    "PR5": "Read the whole word form",
    "PS1": "Find the subject in a phrase",
    "PS2": "Find the action in a phrase",
    "PS3": "Read a prefix inside a phrase",
    "PS4": "Understand a phrase unit",
    "PS5": "Put phrase clues together",
    "SS1": "Find who is doing the action",
    "SS2": "Find the main action",
    "SS3": "Identify each word's role",
    "SS4": "Follow the order of events",
    "SS5": "Explain how the sentence works",
    "CM1": "Use context to choose the meaning",
    "CF1": "Connect root and meaning",
    "CF2": "Connect prefix and meaning",
    "CF3": "Put root, prefix, and meaning together",
    "CF4": "Decode several clues at once",
    "CF5": "Explain a complex form",
}


def load_json(path, default):
    if not path.exists():
        return default

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_progress(progress):
    with PROGRESS_PATH.open("w", encoding="utf-8") as file:
        json.dump(progress, file, indent=2, ensure_ascii=False)


@st.cache_data
def load_questions():
    data = load_json(QUESTIONS_PATH, {"questions": []})
    return data.get("questions", [])


@st.cache_data
def load_pasuk_flows():
    flows = []
    for path in [PASUK_FLOW_QUESTIONS_PATH, PASUK_FLOWS_PATH]:
        data = load_json(path, {"flows": []})
        flows.extend(data.get("flows", []))
    return flows


@st.cache_data
def load_word_bank_metadata():
    data = load_json(WORD_BANK_PATH, {"words": []})
    metadata = {}
    for entry in data.get("words", []):
        metadata.setdefault(entry["word"], entry)
    return metadata


def load_progress():
    return load_json(
        PROGRESS_PATH,
        {"words": {}, "standards": {}, "micro_standards": {}, "xp": {}},
    )


def ensure_progress_keys(progress, questions):
    progress.setdefault("words", {})
    progress.setdefault("standards", {})
    progress.setdefault("micro_standards", {})
    progress.setdefault("xp", {})
    progress.setdefault("current_skill", SKILL_ORDER[0])

    for standard in ADAPTIVE_STANDARDS:
        progress["standards"].setdefault(standard, 0)
        progress["xp"].setdefault(standard, 0)

    for question in questions:
        progress["words"].setdefault(question["word"], 0)
        progress["standards"].setdefault(question["standard"], 0)
        progress["micro_standards"].setdefault(question["micro_standard"], 0)
        progress["xp"].setdefault(question["standard"], 0)


def get_skill_level(xp):
    return (xp // 100) + 1


def get_skill_xp_progress(xp):
    return (xp % 100) / 100


def get_next_skill(current_skill):
    try:
        index = SKILL_ORDER.index(current_skill)
    except ValueError:
        return SKILL_ORDER[0]

    if index + 1 >= len(SKILL_ORDER):
        return current_skill

    return SKILL_ORDER[index + 1]


def skill_path_label(skill):
    return SKILL_NAMES.get(skill, skill.replace("_", " ").title())


def get_error_type(skill):
    return {
        "identify_prefix_meaning": "prefix_error",
        "identify_suffix_meaning": "suffix_error",
        "identify_verb_marker": "verb_marker_error",
    }.get(skill)


def menukad_word(word):
    metadata = load_word_bank_metadata()
    if word in metadata and metadata[word].get("menukad"):
        return metadata[word]["menukad"]
    if word in MENUKAD_FALLBACK:
        return MENUKAD_FALLBACK[word]
    return word


def menukad_text(text):
    if not isinstance(text, str):
        return text
    return HEBREW_WORD_RE.sub(lambda match: menukad_word(match.group(0)), text)


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
    return f"<div class='{class_name}' dir='rtl'>{safe_text}</div>"


def mixed_text_html(text):
    display = menukad_text(text)
    safe = escape(display)

    def wrap(match):
        return f"<span class='hebrew-inline' dir='rtl'>{match.group(0)}</span>"

    return HEBREW_WORD_RE.sub(wrap, safe)


def next_goal_message(score):
    if score < 40:
        return "Next goal: build a steady foundation."
    if score < 70:
        return "Next goal: answer close choices with more confidence."
    if score < 90:
        return "Next goal: explain the clue, not just the answer."
    return "Next goal: keep sharp with harder examples."


def plain_skill(question_or_mode):
    if isinstance(question_or_mode, str):
        return SKILL_NAMES.get(question_or_mode, question_or_mode)

    question_type = question_or_mode.get("question_type")
    if question_type in QUESTION_TYPE_NAMES:
        return QUESTION_TYPE_NAMES[question_type]
    return SKILL_NAMES.get(question_or_mode.get("standard"), "Chumash Reading")


def learning_goal(question):
    if question.get("skill"):
        return skill_path_label(question["skill"])
    return MICRO_STANDARD_NAMES.get(
        question.get("micro_standard"),
        plain_skill(question),
    )


def thinking_tip(question):
    question_type = question.get("question_type", "")
    standard = question.get("standard", "")

    if question_type == "substitution":
        return "Ask what changed, then ask what meaning no longer fits."
    if question_type in {"flow", "flow_dependency"}:
        return "Follow the action from the first clue to the next clue."
    if question_type == "phrase_meaning":
        return "Read the words as one unit, not as separate guesses."
    if question_type == "role_clarity":
        return "Decide what job the word has in the sentence."
    if question_type == "reasoning":
        return "Choose the answer that explains all the clues, not just one."
    if standard in {"PR", "PS"}:
        return "Look at the beginning and ending of the word before translating."
    if standard == "SS":
        return "Find the action, then find who is doing it."
    if standard == "CM":
        return "Use the nearby words to choose the best meaning."
    return "Start with the word you know, then check the nearby clues."


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


def highlight_focus(text, focus):
    if not text:
        return ""
    safe_text = escape(menukad_text(text))
    if focus:
        safe_focus = escape(menukad_text(focus))
        safe_text = safe_text.replace(
            safe_focus,
            f"<mark>{safe_focus}</mark>",
            1,
        )
    return safe_text


def get_word_entry(question):
    word_bank_metadata = load_word_bank_metadata()
    selected_word = question.get("selected_word") or question.get("word", "")
    if selected_word in word_bank_metadata:
        return word_bank_metadata[selected_word]

    for token in selected_word.split():
        if token in word_bank_metadata:
            return word_bank_metadata[token]

    return None


def render_learning_header(question, progress, flow=None):
    standard = question.get("standard", "unknown")
    score = progress["standards"].get(standard, 0)
    xp = progress["xp"].get(standard, 0)
    level = get_skill_level(xp)
    skill_state = st.session_state.get("last_skill_state")
    mastery_score = skill_state["score"] if skill_state else score
    if flow is not None:
        steps = flow.get("questions") or flow.get("steps", [])
        step_index = st.session_state.flow_step + 1
        progress_value = step_index / max(1, len(steps))
        progress_text = f"You're {int(progress_value * 100)}% through this pasuk."
    else:
        progress_value = mastery_score / 100
        progress_text = f"You're building {plain_skill(question).lower()}."

    with st.container():
        st.markdown("<div class='top-card'>", unsafe_allow_html=True)
        col1, col2 = st.columns([1.1, 1.7])
        with col1:
            st.markdown(f"<div class='eyebrow'>Focus</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='focus-title'>{plain_skill(question)}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='eyebrow'>Think about</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='think-text'>{thinking_tip(question)}</div>", unsafe_allow_html=True)
        st.progress(progress_value)
        st.markdown(
            f"<div class='progress-text'>{progress_text} Mastery: {mastery_score}/100. "
            f"Practice level {level}. {next_goal_message(mastery_score)}</div>",
            unsafe_allow_html=True,
        )
        if skill_state:
            st.caption(f"🔥 Streak: {skill_state['current_streak']}")
            if mastery_score >= 90:
                st.info("You're in the mastery zone. Stay sharp.")
            elif mastery_score >= 80:
                st.info("You're close to mastery.")
        st.markdown("</div>", unsafe_allow_html=True)


def render_pasukh_panel(question, flow=None):
    if question.get("hide_pasuk"):
        return

    pasuk = get_pasukh_text(question, flow)
    focus = "" if question.get("hide_focus_word") else question.get("selected_word") or question.get("word", "")
    if not pasuk:
        return

    st.markdown("<div class='section-label'>Read the pasuk</div>", unsafe_allow_html=True)
    st.markdown(rtl_hebrew_html(pasuk, focus, "pasuk-box"), unsafe_allow_html=True)


def render_grammar_clues(question):
    entry = get_word_entry(question)
    clues = []
    if entry:
        if entry.get("prefix"):
            clues.append(f"{entry['prefix']} = {entry.get('prefix_meaning', '')}")
        if entry.get("shoresh"):
            clues.append(f"root clue: {entry['shoresh']}")
        if entry.get("suffix"):
            clues.append(f"{entry['suffix']} = {entry.get('suffix_meaning', '')}")
        if entry.get("tense"):
            clues.append(f"time clue: {entry['tense']}")

    if clues:
        st.markdown("**Key clues:**")
        st.markdown(mixed_text_html(" | ".join(clues)), unsafe_allow_html=True)


def get_question_pool(mode, questions, progress):
    if mode == "Adaptive":
        available = [
            question
            for question in questions
            if question.get("standard") in ADAPTIVE_STANDARDS
        ]
        if not available:
            return []

        available_standards = {question["standard"] for question in available}
        weakest_standard = min(
            available_standards,
            key=lambda standard: progress["standards"].get(standard, 0),
        )
        return [
            question
            for question in available
            if question["standard"] == weakest_standard
        ]

    return [
        question
        for question in questions
        if question.get("standard") == mode
    ]


def filter_questions_by_session_limits(questions):
    questions_answered = st.session_state.questions_answered
    level5_answered = st.session_state.level5_answered
    allow_level5_by_count = questions_answered >= MIN_QUESTIONS_BEFORE_LEVEL5
    allow_level5_by_ratio = (
        (level5_answered + 1) / (questions_answered + 1)
        <= MAX_LEVEL5_SESSION_RATIO
    )

    if allow_level5_by_count and allow_level5_by_ratio:
        return questions

    return [question for question in questions if question.get("difficulty") != 5]


def choose_question(mode, questions, progress):
    pool = get_question_pool(mode, questions, progress)
    pool = filter_questions_by_session_limits(pool)
    if not pool:
        return None
    return random.choice(pool)


def update_progress(progress, question, is_correct):
    amount = 10 if is_correct else -10
    xp_gain = 15 if is_correct else 3
    word = question["word"]
    standard = question["standard"]
    micro_standard = question["micro_standard"]

    progress["words"].setdefault(word, 0)
    progress["standards"].setdefault(standard, 0)
    progress["micro_standards"].setdefault(micro_standard, 0)

    progress["words"][word] = max(0, min(100, progress["words"].get(word, 0) + amount))
    progress["standards"][standard] = max(
        0,
        min(100, progress["standards"].get(standard, 0) + amount),
    )
    progress["micro_standards"][micro_standard] = max(
        0,
        min(100, progress["micro_standards"].get(micro_standard, 0) + amount),
    )
    progress.setdefault("xp", {})
    progress["xp"][standard] = progress["xp"].get(standard, 0) + xp_gain
    save_progress(progress)


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


def handle_answer(choice, question, progress):
    if st.session_state.answered:
        return

    st.session_state.answered = True
    st.session_state.selected_answer = choice
    st.session_state.questions_answered += 1
    if question.get("difficulty") == 5:
        st.session_state.level5_answered += 1
    is_correct = choice == question["correct_answer"]
    update_progress(progress, question, is_correct)
    st.session_state.last_skill_state = update_skill_progress(
        question.get("skill", question.get("standard", "unknown")),
        is_correct,
        None if is_correct else get_error_type(question.get("skill")),
    )
    asked_token = question.get("selected_word") or question.get("word")
    if asked_token:
        st.session_state.asked_tokens.append(asked_token)
    if question.get("id"):
        st.session_state.asked_question_ids.append(question["id"])

    answered_skill = question.get("skill")
    if (
        st.session_state.get("practice_type") == "Learn Mode"
        and answered_skill == progress.get("current_skill")
        and st.session_state.last_skill_state["mastered"]
    ):
        next_skill = get_next_skill(answered_skill)
        progress["current_skill"] = next_skill
        save_progress(progress)
        st.session_state.asked_tokens = []
        st.session_state.asked_question_ids = []
        st.session_state.asked_pasuks = []
        st.session_state.unlocked_skill_message = (
            f"{skill_path_label(answered_skill)} mastered. "
            f"Next skill: {skill_path_label(next_skill)}."
        )


def render_debug(question):
    word_bank_metadata = load_word_bank_metadata()
    selected_word = question.get("selected_word") or question.get("word", "")
    word_entry = word_bank_metadata.get(selected_word)

    if word_entry is None:
        for token in selected_word.split():
            if token in word_bank_metadata:
                word_entry = word_bank_metadata[token]
                break

    group = question.get("generation_group")
    if group is None and word_entry is not None:
        group = word_entry.get("group")

    difficulty = question.get("difficulty")
    if difficulty is None and word_entry is not None:
        difficulty = word_entry.get("difficulty")

    st.caption(f"What you are learning: {learning_goal(question)}")
    distractor_group = question.get("generation_group")
    st.caption(
        f"Focus word: {menukad_text(selected_word)} | "
        f"Challenge level: {question['difficulty']}"
    )


def render_question(question, progress, button_prefix, flow=None):
    render_learning_header(question, progress, flow)
    with st.container():
        render_pasukh_panel(question, flow)
        render_debug(question)
        st.markdown(
            f"<div class='question-card'><div class='section-label'>Question</div>"
            f"<div class='question-text'>{mixed_text_html(question['question'])}</div></div>",
            unsafe_allow_html=True,
        )

    st.markdown("<div class='section-label answer-label'>Choose an answer</div>", unsafe_allow_html=True)
    for index, choice in enumerate(question["choices"]):
        label = OPTION_LABELS[index]
        button_type = "primary" if st.session_state.selected_answer == choice else "secondary"
        st.button(
            f"{label}. {menukad_text(choice)}",
            key=f"{button_prefix}_{index}_{choice}",
            use_container_width=True,
            disabled=st.session_state.answered,
            type=button_type,
            on_click=handle_answer,
            args=(choice, question, progress),
        )

    if st.session_state.answered:
        skill_state = st.session_state.get("last_skill_state") or {}
        point_change = skill_state.get("point_change", "")
        st.markdown("<div class='feedback-card'>", unsafe_allow_html=True)
        if st.session_state.selected_answer == question["correct_answer"]:
            st.success(f"Correct! {point_change}")
            st.caption(menukad_text(question["explanation"]))
        else:
            st.error(f"Incorrect. {point_change}")
            st.caption(f"Answer: {menukad_text(question['correct_answer'])}")
            st.caption(menukad_text(question["explanation"]))

        if skill_state:
            st.progress(skill_state["score"] / 100)
            st.write(f"Mastery: {skill_state['score']}/100")
            st.write(f"🔥 Streak: {skill_state['current_streak']}")
            if skill_state["score"] >= 90:
                st.info("You're in the mastery zone. Stay sharp.")
            elif skill_state["score"] >= 80:
                st.info("You're close to mastery.")

        render_grammar_clues(question)
        st.markdown("</div>", unsafe_allow_html=True)


def render_standard_mode(mode, questions, progress):
    if st.session_state.current_question is None:
        set_question(choose_question(mode, questions, progress))

    question = st.session_state.current_question
    if question is None:
        st.warning(
            "No practice questions are ready for this choice yet. Try Recommended Practice, "
            "Guided Pasuk Practice, or choose another learning area."
        )
        return

    render_question(question, progress, f"question_{mode}")

    if st.session_state.answered:
        if st.button("Next Question", type="primary"):
            set_question(choose_question(mode, questions, progress))
            st.rerun()


def get_system_pasuks():
    flow_pasuks = [flow["pasuk"] for flow in load_pasuk_flows() if flow.get("pasuk")]
    return list(dict.fromkeys(flow_pasuks + SYSTEM_PESUKIM))


def select_system_pasuk(skill):
    if generate_skill_question is None:
        return None

    candidates = []
    for pasuk in get_system_pasuks():
        try:
            generate_skill_question(skill, pasuk)
        except Exception:
            continue
        candidates.append(pasuk)

    if not candidates:
        return None

    unused = [
        pasuk
        for pasuk in candidates
        if pasuk not in st.session_state.asked_pasuks
    ]
    if not unused:
        st.session_state.asked_pasuks = []
        unused = candidates

    return unused[0]


def generate_mastery_question(progress):
    if generate_skill_question is None:
        return None
    pasuk = select_system_pasuk(progress["current_skill"])
    if pasuk is None:
        return None
    question = generate_skill_question(
        progress["current_skill"],
        pasuk,
        asked_tokens=st.session_state.asked_question_ids
        if progress["current_skill"].startswith(("identify_", "segment_", "convert_", "match_"))
        else st.session_state.asked_tokens,
    )
    question["pasuk"] = pasuk
    selected_token = question.get("selected_word") or question.get("word")
    if selected_token in st.session_state.asked_tokens:
        st.session_state.asked_tokens = []
        question = generate_skill_question(progress["current_skill"], pasuk)
        question["pasuk"] = pasuk
    st.session_state.asked_pasuks.append(pasuk)
    return question


def generate_practice_question(skill):
    if generate_skill_question is None:
        return None
    pasuk = select_system_pasuk(skill)
    if pasuk is None:
        return None
    question = generate_skill_question(
        skill,
        pasuk,
        asked_tokens=st.session_state.asked_question_ids
        if skill.startswith(("identify_", "segment_", "convert_", "match_"))
        else st.session_state.asked_tokens,
    )
    question["pasuk"] = pasuk
    st.session_state.asked_pasuks.append(pasuk)
    return question


def render_mastery_mode(progress):
    if st.session_state.current_question is None:
        try:
            set_question(generate_mastery_question(progress))
        except Exception as error:
            st.warning(f"No question is ready for this skill and pasuk yet: {error}")
            return

    question = st.session_state.current_question
    if question is None:
        st.warning("No mastery question is ready yet.")
        return

    render_question(question, progress, f"mastery_{progress['current_skill']}")

    if st.session_state.get("unlocked_skill_message"):
        st.success(st.session_state.unlocked_skill_message)

    if st.session_state.answered:
        if st.button("Next Question", type="primary"):
            st.session_state.unlocked_skill_message = ""
            try:
                set_question(generate_mastery_question(progress))
            except Exception as error:
                st.warning(f"No question is ready for this skill and pasuk yet: {error}")
                return
            st.rerun()


def render_skill_practice_mode(progress, skill):
    if st.session_state.current_question is None:
        try:
            set_question(generate_practice_question(skill))
        except Exception as error:
            st.warning(f"No question is ready for this skill and pasuk yet: {error}")
            return

    question = st.session_state.current_question
    if question is None:
        st.warning("No practice question is ready yet.")
        return

    render_question(question, progress, f"practice_{skill}")

    if st.session_state.answered:
        if st.button("Next Question", type="primary"):
            set_question(generate_practice_question(skill))
            st.rerun()


def render_pasuk_flow(progress):
    flows = load_pasuk_flows()
    if not flows:
        st.warning(
            "No guided Pasuk practice is ready yet. Add a flow, then come back here to walk through it step by step."
        )
        return

    flow_labels = [
        f"{flow.get('source', 'unknown')} - {flow['pasuk']}"
        for flow in flows
    ]
    selected_label = st.sidebar.selectbox("Pasuk", flow_labels)
    flow = flows[flow_labels.index(selected_label)]

    st.caption(f"Source: {flow.get('source', 'unknown')}")

    if st.session_state.flow_label != selected_label:
        st.session_state.flow_label = selected_label
        st.session_state.flow_step = 0
        st.session_state.answered = False
        st.session_state.selected_answer = None

    steps = flow.get("questions") or flow.get("steps", [])
    step_index = st.session_state.flow_step
    question = steps[step_index]

    st.caption(f"Step {step_index + 1} of {len(steps)}")
    render_question(question, progress, f"flow_{step_index}", flow)

    if st.session_state.answered:
        if step_index + 1 < len(steps):
            if st.button("Next Step", type="primary"):
                st.session_state.flow_step += 1
                st.session_state.answered = False
                st.session_state.selected_answer = None
                st.rerun()
        else:
            st.success("Pasuk flow complete.")
            if st.button("Restart Flow"):
                st.session_state.flow_step = 0
                st.session_state.answered = False
                st.session_state.selected_answer = None
                st.rerun()


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
    st.session_state.setdefault("practice_type", "Learn Mode")
    st.session_state.setdefault("practice_skill", SKILL_ORDER[0])
    st.session_state.setdefault("unlocked_skill_message", "")


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

    render_unlocks(progress)


def main():
    st.set_page_config(page_title="Chumash Quiz", layout="centered")
    init_session_state()
    st.markdown(
        """
        <style>
        :root {
            --ink: #202124;
            --muted: #5f6368;
            --line: #dfe4ea;
            --soft: #f7f9fb;
            --panel: #ffffff;
            --accent: #496b5b;
            --accent-soft: #edf5f0;
            --gold: #fff2a8;
        }
        .stApp {
            background: #fbfcfd;
            color: var(--ink);
        }
        .block-container {
            max-width: 900px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }
        h1 {
            text-align: center;
            font-size: 2.4rem !important;
            letter-spacing: 0;
            margin-bottom: 1rem !important;
        }
        .top-card,
        .question-card,
        .pasuk-box {
            border: 1px solid var(--line);
            border-radius: 8px;
            background: var(--panel);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        }
        .top-card {
            padding: 18px 20px 16px 20px;
            margin: 8px 0 26px 0;
        }
        .eyebrow,
        .section-label {
            color: var(--muted);
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0;
            margin-bottom: 6px;
        }
        .focus-title {
            color: var(--ink);
            font-size: 1.12rem;
            font-weight: 750;
            line-height: 1.35;
        }
        .think-text {
            color: var(--ink);
            font-size: 1rem;
            line-height: 1.45;
        }
        .progress-text {
            color: var(--muted);
            font-size: 0.94rem;
            margin-top: 10px;
            line-height: 1.45;
        }
        div[data-testid="stProgress"] > div {
            height: 12px;
            border-radius: 8px;
            background: #e9edf1;
        }
        div[data-testid="stProgress"] div[role="progressbar"] {
            background: var(--accent);
        }
        .pasuk-box {
            padding: 24px 28px;
            margin: 8px 0 24px 0;
            font-size: 2.55rem;
            line-height: 2.05;
            background: var(--soft);
            direction: rtl;
            text-align: right;
            font-family: "SBL Hebrew", "Ezra SIL", "Taamey David CLM", "Times New Roman", serif;
            unicode-bidi: isolate;
        }
        .hebrew-text,
        .hebrew-inline {
            direction: rtl;
            text-align: right;
            font-family: "SBL Hebrew", "Ezra SIL", "Taamey David CLM", "Times New Roman", serif;
            unicode-bidi: isolate;
        }
        .question-card {
            padding: 22px 24px;
            margin: 14px 0 22px 0;
        }
        .question-text {
            font-size: 1.55rem;
            font-weight: 750;
            margin: 4px 0 0 0;
            line-height: 1.55;
        }
        .answer-label {
            margin-top: 10px;
            margin-bottom: 10px;
        }
        div.stButton > button {
            min-height: 58px;
            border-radius: 8px;
            border: 1px solid var(--line);
            background: #ffffff;
            color: var(--ink);
            font-size: 1.06rem;
            font-weight: 650;
            line-height: 1.35;
            margin: 2px 0 8px 0;
            text-align: left;
            justify-content: flex-start;
            unicode-bidi: plaintext;
            transition: border-color 120ms ease, background-color 120ms ease, transform 120ms ease;
        }
        div.stButton > button:hover {
            border-color: var(--accent);
            background: var(--accent-soft);
            transform: translateY(-1px);
        }
        div.stButton > button:disabled {
            opacity: 0.82;
            transform: none;
        }
        div.stButton > button[kind="primary"] {
            background: var(--accent);
            border-color: var(--accent);
            color: #ffffff;
        }
        .feedback-card {
            border: 1px solid var(--line);
            border-radius: 8px;
            background: #ffffff;
            padding: 16px 18px;
            margin-top: 18px;
        }
        mark {
            background: var(--gold);
            color: #111111;
            padding: 3px 8px;
            border-radius: 6px;
            box-decoration-break: clone;
            -webkit-box-decoration-break: clone;
        }
        [data-testid="stSidebar"] {
            background: #f7f9fb;
            border-right: 1px solid var(--line);
        }
        [data-testid="stSidebar"] h3 {
            font-size: 1rem;
        }
        [data-testid="stSidebar"] .stMarkdown,
        [data-testid="stSidebar"] p {
            color: var(--muted);
        }
        @media (max-width: 760px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }
            .pasuk-box {
                font-size: 2rem;
                padding: 20px;
            }
            .question-text {
                font-size: 1.3rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    questions = load_questions()
    progress = load_progress()
    ensure_progress_keys(progress, questions)

    st.title("Chumash Quiz")
    focus_mode = st.sidebar.toggle("Focus Mode", value=True)
    practice_type = st.sidebar.radio(
        "Practice type",
        ["Learn Mode", "Practice Mode"],
        index=0 if st.session_state.practice_type == "Learn Mode" else 1,
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

    if not focus_mode:
        st.sidebar.caption(
            "Hard explanation questions used: "
            f"{st.session_state.level5_answered}/{st.session_state.questions_answered} "
            f"(practice a bit first; these stay occasional)"
        )
        render_dashboard(progress)

    if practice_type == "Learn Mode":
        render_mastery_mode(progress)
    else:
        practice_skill = st.sidebar.selectbox(
            "Choose a skill to practice",
            SKILL_ORDER,
            index=SKILL_ORDER.index(st.session_state.practice_skill),
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
