import json
import hashlib
import random
import re
from html import escape
from pathlib import Path

import streamlit as st

from skill_tracker import update_skill_progress, update_word_progress

try:
    from pasuk_flow_generator import analyze_pasuk as analyze_generator_pasuk
    from pasuk_flow_generator import generate_question as generate_skill_question
    from pasuk_flow_generator import update_word_skill_score
except ImportError:
    analyze_generator_pasuk = None
    generate_skill_question = None
    update_word_skill_score = None


BASE_DIR = Path(__file__).parent
QUESTIONS_PATH = BASE_DIR / "questions.json"
PROGRESS_PATH = BASE_DIR / "progress.json"
SKILL_PROGRESS_PATH = BASE_DIR / "skill_progress.json"
PASUK_FLOWS_PATH = BASE_DIR / "pasuk_flows.json"
PASUK_FLOW_QUESTIONS_PATH = BASE_DIR / "pasuk_flow_questions.json"
WORD_BANK_PATH = BASE_DIR / "data" / "word_bank.json"
LEGACY_WORD_BANK_PATH = BASE_DIR / "word_bank.json"

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
    st.session_state.recent_features = []
    st.session_state.recent_prefixes = []
    st.rerun()


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
    metadata = {}
    for path in [LEGACY_WORD_BANK_PATH, WORD_BANK_PATH]:
        data = load_json(path, {"words": []})
        for entry in adapt_word_bank_metadata(data):
            add_word_metadata(metadata, entry)
    return metadata


def normalize_hebrew_key(text):
    if not isinstance(text, str):
        return text
    return HEBREW_MARK_RE.sub("", text)


def old_word_type(part_of_speech):
    return {
        "proper_noun": "noun",
        "preposition": "prep",
    }.get(part_of_speech, part_of_speech or "unknown")


def first_morpheme_value(items, key, default=""):
    if not items:
        return default
    first = items[0] or {}
    return first.get(key, default)


def adapt_word_analysis(surface, analysis, analysis_index=0):
    prefixes = analysis.get("prefixes") or []
    suffixes = analysis.get("suffixes") or []
    word = analysis.get("surface") or surface
    translation_literal = analysis.get("translation_literal") or analysis.get("translation")
    translation_context = analysis.get("translation_context") or analysis.get("context_translation")
    adapted = {
        "word": word,
        "Word": word,
        "surface": word,
        "menukad": word,
        "normalized": analysis.get("normalized") or normalize_hebrew_key(word),
        "lemma": analysis.get("lemma"),
        "shoresh": analysis.get("shoresh"),
        "Shoresh": analysis.get("shoresh"),
        "type": old_word_type(analysis.get("part_of_speech")),
        "part_of_speech": analysis.get("part_of_speech"),
        "translation": translation_context or translation_literal or word,
        "translation_literal": translation_literal,
        "translation_context": translation_context,
        "context_translation": translation_context,
        "base_translation": translation_literal,
        "prefixes": prefixes,
        "suffixes": suffixes,
        "prefix": first_morpheme_value(prefixes, "form"),
        "prefix_meaning": first_morpheme_value(prefixes, "translation"),
        "suffix": first_morpheme_value(suffixes, "form"),
        "suffix_meaning": first_morpheme_value(suffixes, "translation"),
        "binyan": analysis.get("binyan"),
        "tense": analysis.get("tense"),
        "person": analysis.get("person"),
        "number": analysis.get("number"),
        "gender": analysis.get("gender"),
        "source_refs": analysis.get("source_refs", []),
        "analysis_index": analysis_index,
    }
    adapted["analyses"] = [dict(adapted)]
    return adapted


def adapt_word_bank_metadata(data):
    words = data.get("words", [])
    if isinstance(words, list):
        entries = []
        for entry in words:
            adapted = dict(entry)
            adapted.setdefault("word", adapted.get("Word"))
            adapted.setdefault("Word", adapted.get("word"))
            adapted.setdefault("surface", adapted.get("word"))
            adapted.setdefault("menukad", adapted.get("surface") or adapted.get("word"))
            adapted.setdefault("normalized", normalize_hebrew_key(adapted.get("word", "")))
            adapted.setdefault("Shoresh", adapted.get("shoresh"))
            adapted.setdefault("type", old_word_type(adapted.get("part_of_speech")))
            adapted.setdefault("translation_literal", adapted.get("translation"))
            adapted.setdefault("translation_context", adapted.get("context_translation"))
            adapted.setdefault(
                "translation",
                adapted.get("translation_context") or adapted.get("translation_literal") or adapted.get("word"),
            )
            adapted.setdefault("context_translation", adapted.get("translation_context"))
            adapted.setdefault("base_translation", adapted.get("translation_literal"))
            adapted.setdefault("prefixes", [])
            adapted.setdefault("suffixes", [])
            adapted.setdefault("analyses", [dict(adapted)])
            entries.append(adapted)
        return entries

    entries = []
    for surface, analyses in words.items():
        for index, analysis in enumerate(analyses):
            entries.append(adapt_word_analysis(surface, analysis, index))
    return entries


def add_word_metadata(metadata, entry):
    word = entry.get("word")
    if not word:
        return
    if word in metadata:
        existing = metadata[word]
        existing.setdefault("analyses", [existing])
        existing["analyses"].extend(entry.get("analyses", [entry]))
        existing.update(entry)
    else:
        metadata[word] = entry

    normalized = entry.get("normalized")
    if normalized:
        metadata.setdefault(normalized, entry)


def load_legacy_word_bank_metadata():
    data = load_json(LEGACY_WORD_BANK_PATH, {"words": []})
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
    progress.setdefault("prefix_level", 1)

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


def get_source_label(question, flow=None):
    if flow is not None:
        return flow.get("source", "generated")
    return question.get("source") or question.get("standard") or "generated"


def split_pasuk_phrases(text, words_per_phrase=4):
    words = menukad_text(text).split()
    if len(words) <= words_per_phrase:
        return [" ".join(words)] if words else []

    phrases = []
    for index in range(0, len(words), words_per_phrase):
        phrases.append(" ".join(words[index:index + words_per_phrase]))
    return phrases


def highlight_display_text(text, focus):
    safe_text = escape(menukad_text(text))
    if focus:
        safe_focus = escape(menukad_text(focus))
        safe_text = safe_text.replace(
            safe_focus,
            f"<mark>{safe_focus}</mark>",
            1,
        )
    return safe_text


def question_key(question, prefix):
    raw = "|".join(
        str(part)
        for part in [
            prefix,
            question.get("id", ""),
            question.get("question", ""),
            question.get("selected_word", ""),
            question.get("correct_answer", ""),
        ]
    )
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]


def highlight_focus(text, focus):
    if not text:
        return ""
    return highlight_display_text(text, focus)


def get_word_entry(question):
    word_bank_metadata = load_word_bank_metadata()
    selected_word = question.get("selected_word") or question.get("word", "")
    if selected_word in word_bank_metadata:
        return word_bank_metadata[selected_word]
    normalized_selected = normalize_hebrew_key(selected_word)
    if normalized_selected in word_bank_metadata:
        return word_bank_metadata[normalized_selected]

    for token in selected_word.split():
        if token in word_bank_metadata:
            return word_bank_metadata[token]
        normalized_token = normalize_hebrew_key(token)
        if normalized_token in word_bank_metadata:
            return word_bank_metadata[normalized_token]

    return None


def _legacy_render_learning_header(question, progress, flow=None):
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
        step_text = f"Step {step_index} of {len(steps)}"
    else:
        progress_value = mastery_score / 100
        progress_text = f"You're building {plain_skill(question).lower()}."
        step_text = f"Practice level {level}"

    source = get_source_label(question, flow)
    st.markdown(
        f"""
        <section class="learning-header">
            <div>
                <div class="meta-row">
                    <span>{escape(source)}</span>
                    <span>{escape(step_text)}</span>
                </div>
                <h1>{escape(plain_skill(question))}</h1>
                <p>{escape(thinking_tip(question))}</p>
            </div>
            <div class="mastery-panel">
                <span class="section-label">Mastery</span>
                <strong>{mastery_score}/100</strong>
                <small>{escape(progress_text)} {escape(next_goal_message(mastery_score))}</small>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    st.progress(progress_value)

    if skill_state:
        if mastery_score >= 90:
            st.info("You're in the mastery zone. Stay sharp.")
        elif mastery_score >= 80:
            st.info("You're close to mastery.")


def render_pasukh_panel(question, flow=None):
    if question.get("hide_pasuk"):
        return

    pasuk = get_pasukh_text(question, flow)
    focus = "" if question.get("hide_focus_word") else question.get("selected_word") or question.get("word", "")
    if not pasuk:
        return

    source = get_source_label(question, flow)
    st.markdown(
        f"""
        <div class="section-heading">
            <span>Read The Pasuk</span>
            <small>{escape(source)}</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.get("pasuk_view_mode") == "Break into phrases":
        lines = []
        for index, phrase in enumerate(split_pasuk_phrases(pasuk), start=1):
            lines.append(
                f"""
                <div class="phrase-line">
                    <span class="phrase-number">{index}</span>
                    <span class="phrase-text" dir="rtl" lang="he">{highlight_display_text(phrase, focus)}</span>
                </div>
                """
            )
        st.markdown(
            f"<section class='pasuk-box phrase-box' dir='rtl' lang='he'>{''.join(lines)}</section>",
            unsafe_allow_html=True,
        )
    else:
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
        update_word_progress(asked_token, is_correct)
        if update_word_skill_score is not None:
            update_word_skill_score(
                asked_token,
                question.get("skill", question.get("standard", "unknown")),
                is_correct,
                progress,
            )
            save_progress(progress)
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

    difficulty = difficulty or question.get("difficulty", 1)
    st.markdown(
        f"""
        <div class="learning-chips">
            <span>{escape(learning_goal(question))}</span>
            <span>Level {escape(str(difficulty))}</span>
            <span dir="rtl" lang="he">{mixed_text_html(selected_word)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _legacy_render_question(question, progress, button_prefix, flow=None):
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


def answer_choice_label(choice, index):
    return f"{OPTION_LABELS[index]}. {menukad_text(choice)}"


def render_feedback(question):
    skill_state = st.session_state.get("last_skill_state") or {}
    point_change = skill_state.get("point_change", "")
    is_correct = st.session_state.selected_answer == question["correct_answer"]
    status_class = "correct" if is_correct else "incorrect"
    title = "Correct" if is_correct else "Not Quite"
    selected = st.session_state.selected_answer or ""
    correct = question["correct_answer"]

    st.markdown(
        f"""
        <section class="feedback-panel {status_class}">
            <div class="feedback-status">
                <strong>{title}</strong>
                <span>{escape(str(point_change))}</span>
            </div>
            <div class="feedback-line">
                <span>Your answer</span>
                <b>{mixed_text_html(selected)}</b>
            </div>
            <div class="feedback-line">
                <span>Correct answer</span>
                <b>{mixed_text_html(correct)}</b>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Why this answer works", expanded=True):
        st.markdown(mixed_text_html(question.get("explanation", "")), unsafe_allow_html=True)
        render_grammar_clues(question)

    if skill_state:
        st.progress(skill_state["score"] / 100)
        st.markdown(
            f"""
            <div class="learning-chips">
                <span>Mastery {skill_state['score']}/100</span>
                <span>Streak {skill_state['current_streak']}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_question(question, progress, button_prefix, flow=None):
    render_learning_header(question, progress, flow)
    with st.container():
        render_pasukh_panel(question, flow)
        render_debug(question)
        st.markdown(
            f"""
            <section class="question-card">
                <div class="section-label">Question</div>
                <div class="question-text">{mixed_text_html(question['question'])}</div>
            </section>
            """,
            unsafe_allow_html=True,
        )

    key = question_key(question, button_prefix)
    choices = question["choices"]
    label_by_choice = {
        choice: answer_choice_label(choice, index)
        for index, choice in enumerate(choices)
    }

    st.markdown("<div class='section-label answer-label'>Choose An Answer</div>", unsafe_allow_html=True)
    selected_choice = st.radio(
        "Choose an answer",
        choices,
        key=f"{button_prefix}_choice_{key}",
        index=None,
        format_func=lambda choice: label_by_choice.get(choice, menukad_text(choice)),
        disabled=st.session_state.answered,
        label_visibility="collapsed",
    )

    if not st.session_state.answered:
        if st.button(
            "Check Answer",
            key=f"{button_prefix}_check_{key}",
            type="primary",
            disabled=selected_choice is None,
            use_container_width=True,
        ):
            handle_answer(selected_choice, question, progress)
            st.rerun()

    if st.session_state.answered:
        render_feedback(question)


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

    recent_pesukim = st.session_state.setdefault("recent_pesukim", [])
    candidates = []
    for pasuk in get_system_pasuks():
        try:
            analyzed_pasuk = (
                analyze_generator_pasuk(pasuk)
                if analyze_generator_pasuk is not None
                else pasuk
            )
            generate_skill_question(skill, analyzed_pasuk)
        except Exception:
            continue
        candidates.append(pasuk)

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


def choose_weighted_pasuk_question(candidates, recent_pesukim, recent_words):
    new_pasuks = [
        item
        for item in candidates
        if item["pasuk"] not in recent_pesukim[-5:]
    ]
    new_words = [
        item
        for item in candidates
        if (item["word"] or "") not in recent_words[-5:]
    ]

    roll = random.random()
    if roll < 0.5 and new_pasuks:
        return random.choice(new_pasuks)
    if roll < 0.8 and new_words:
        return random.choice(new_words)

    seen = [
        item
        for item in candidates
        if item not in new_pasuks and item not in new_words
    ]
    return random.choice(seen or new_words or new_pasuks or candidates)


def select_pasuk_first_question(skill):
    if generate_skill_question is None:
        return None

    recent_pesukim = st.session_state.setdefault("recent_pesukim", [])
    recent_words = st.session_state.setdefault("asked_tokens", [])
    pasuk_pool = get_system_pasuks()
    recent_pasuk_window = recent_pesukim[-5:]
    preferred_pasuks = [
        pasuk for pasuk in pasuk_pool if pasuk not in recent_pasuk_window
    ]

    attempts = 0
    candidate_rows = []
    fallback_rows = []
    search_pool = preferred_pasuks or pasuk_pool

    while attempts < 10 and not candidate_rows:
        attempts += 1
        for pasuk in search_pool:
            try:
                question = generate_skill_question(
                    skill,
                    (
                        analyze_generator_pasuk(pasuk)
                        if analyze_generator_pasuk is not None
                        else pasuk
                    ),
                    asked_tokens=get_generation_history(skill),
                    prefix_level=load_progress().get("prefix_level", 1),
                    recent_question_formats=get_recent_question_formats(),
                    recent_prefixes=get_recent_prefixes(),
                )
            except Exception:
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
                continue
            if feature_is_blocked(feature):
                fallback_rows.append(row)
                continue
            candidate_rows.append(row)

        if not candidate_rows and search_pool is not pasuk_pool:
            search_pool = pasuk_pool

    if not candidate_rows:
        if not fallback_rows:
            return None
        st.session_state.feature_fallback_message = (
            "Feature repetition fallback used after 10 attempts."
        )
        candidate_rows = fallback_rows

    selected = choose_weighted_pasuk_question(
        candidate_rows,
        recent_pesukim,
        recent_words,
    )
    question = selected["question"]
    question.setdefault("pasuk", selected["pasuk"])
    record_selected_pasuk(selected["pasuk"])
    record_question_feature(question)
    record_question_prefix(question)
    return question


def record_selected_pasuk(pasuk):
    st.session_state.asked_pasuks.append(pasuk)
    st.session_state.asked_pasuks = st.session_state.asked_pasuks[-10:]
    st.session_state.recent_pesukim.append(pasuk)
    st.session_state.recent_pesukim = st.session_state.recent_pesukim[-10:]


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


def generate_mastery_question(progress):
    return select_pasuk_first_question(progress["current_skill"])


def generate_practice_question(skill):
    return select_pasuk_first_question(skill)


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
    if st.session_state.get("feature_fallback_message"):
        st.caption(st.session_state.feature_fallback_message)

    if st.session_state.answered:
        if st.button("Next Question", type="primary"):
            st.session_state.unlocked_skill_message = ""
            st.session_state.feature_fallback_message = ""
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
    if st.session_state.get("feature_fallback_message"):
        st.caption(st.session_state.feature_fallback_message)

    if st.session_state.answered:
        if st.button("Next Question", type="primary"):
            st.session_state.feature_fallback_message = ""
            set_question(generate_practice_question(skill))
            st.rerun()


def render_flow_overview(flow, active_step):
    steps = flow.get("questions") or flow.get("steps", [])
    if not steps:
        return

    rows = []
    for index, step in enumerate(steps):
        status = "complete" if index < active_step else "active" if index == active_step else "upcoming"
        title = QUESTION_TYPE_NAMES.get(
            step.get("question_type"),
            skill_path_label(step.get("skill", f"Step {index + 1}")),
        )
        focus = step.get("selected_word") or step.get("word") or ""
        rows.append(
            f"""
            <div class="flow-row {status}">
                <div class="flow-index">{index + 1}</div>
                <div>
                    <strong>{escape(title)}</strong>
                    <span dir="rtl" lang="he">{mixed_text_html(focus)}</span>
                </div>
            </div>
            """
        )

    st.markdown(
        f"""
        <section class="flow-overview">
            <div class="section-heading">
                <span>Pasuk Flow</span>
                <small>{active_step + 1}/{len(steps)}</small>
            </div>
            <div class="flow-grid">{''.join(rows)}</div>
        </section>
        """,
        unsafe_allow_html=True,
    )


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

    render_flow_overview(flow, step_index)
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
    st.session_state.setdefault("recent_pesukim", [])
    st.session_state.setdefault("recent_phrases", [])
    st.session_state.setdefault("recent_question_formats", [])
    st.session_state.setdefault("recent_features", [])
    st.session_state.setdefault("recent_prefixes", [])
    st.session_state.setdefault("feature_fallback_message", "")
    st.session_state.setdefault("practice_type", "Learn Mode")
    st.session_state.setdefault("practice_skill", SKILL_ORDER[0])
    st.session_state.setdefault("unlocked_skill_message", "")
    st.session_state.setdefault("show_nekudos", True)
    st.session_state.setdefault("pasuk_view_mode", "Full pasuk view")


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
            max-width: 1120px;
            padding-top: 1.25rem;
            padding-bottom: 3rem;
        }
        h1 {
            letter-spacing: 0 !important;
        }
        .app-title {
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            gap: 18px;
            margin: 4px 0 22px 0;
        }
        .app-title h1 {
            margin: 0 !important;
            font-size: 2.2rem !important;
            text-align: left;
        }
        .app-title p {
            color: var(--muted);
            margin: 4px 0 0 0;
            font-size: 1rem;
        }
        .learning-header,
        .question-card,
        .pasuk-box,
        .flow-overview,
        .feedback-panel {
            border: 1px solid var(--line);
            border-radius: 8px;
            background: var(--surface);
            box-shadow: 0 14px 40px rgba(28, 45, 40, 0.07);
        }
        .learning-header {
            display: grid;
            grid-template-columns: minmax(0, 1fr) 220px;
            gap: 22px;
            align-items: stretch;
            padding: 24px;
            margin-bottom: 14px;
        }
        .learning-header h1 {
            text-align: left;
            font-size: 1.95rem !important;
            margin: 8px 0 8px 0 !important;
        }
        .learning-header p {
            color: var(--muted);
            font-size: 1.03rem;
            line-height: 1.55;
            margin: 0;
        }
        .meta-row,
        .learning-chips,
        .feedback-status {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            align-items: center;
        }
        .meta-row span,
        .learning-chips span {
            border: 1px solid var(--line);
            background: var(--wash);
            border-radius: 999px;
            color: var(--muted);
            font-size: 0.82rem;
            font-weight: 700;
            padding: 5px 10px;
        }
        .mastery-panel {
            border-left: 4px solid var(--accent);
            background: var(--accent-soft);
            border-radius: 8px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            gap: 4px;
        }
        .mastery-panel strong {
            color: var(--accent);
            font-size: 2rem;
            line-height: 1;
        }
        .mastery-panel small,
        .section-heading small {
            color: var(--muted);
            line-height: 1.35;
        }
        .section-label,
        .section-heading span {
            color: var(--muted);
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0;
            text-transform: uppercase;
        }
        .section-heading {
            display: flex;
            justify-content: space-between;
            gap: 16px;
            align-items: center;
            margin: 22px 0 8px 0;
        }
        .pasuk-box {
            padding: 28px 32px;
            margin: 0 0 22px 0;
            background: #fbfdfc;
            direction: rtl;
            text-align: center;
            font-family: "Noto Sans Hebrew", "SBL Hebrew", "Ezra SIL", "Taamey David CLM", "Times New Roman", serif;
            font-size: 2.6rem;
            font-weight: 700;
            line-height: 2.05;
            overflow-wrap: anywhere;
            unicode-bidi: plaintext;
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
            gap: 10px;
            text-align: right;
            font-size: 2.1rem;
        }
        .phrase-line {
            display: grid;
            grid-template-columns: 42px minmax(0, 1fr);
            gap: 14px;
            align-items: center;
            direction: ltr;
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 10px 14px;
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
            padding: 22px 24px;
            margin: 14px 0 20px 0;
        }
        .question-text {
            margin-top: 8px;
            font-size: 1.48rem;
            font-weight: 800;
            line-height: 1.6;
        }
        .answer-label {
            margin-top: 18px;
            margin-bottom: 8px;
        }
        div[data-testid="stRadio"] [role="radiogroup"] {
            display: grid;
            gap: 10px;
        }
        div[data-testid="stRadio"] label {
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 14px 16px;
            background: #ffffff;
            min-height: 58px;
            align-items: center;
            transition: border-color 120ms ease, background-color 120ms ease, transform 120ms ease;
        }
        div[data-testid="stRadio"] label:hover {
            border-color: var(--accent);
            background: var(--accent-soft);
            transform: translateY(-1px);
        }
        div[data-testid="stRadio"] label p {
            font-size: 1.06rem;
            font-weight: 650;
            line-height: 1.55;
            unicode-bidi: plaintext;
        }
        div.stButton > button {
            min-height: 52px;
            border-radius: 8px;
            font-weight: 800;
            letter-spacing: 0;
        }
        div.stButton > button[kind="primary"] {
            background: var(--accent);
            border-color: var(--accent);
        }
        .feedback-panel {
            margin-top: 18px;
            padding: 18px;
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
        .feedback-status {
            justify-content: space-between;
            margin-bottom: 12px;
        }
        .feedback-status strong {
            font-size: 1.35rem;
        }
        .feedback-line {
            display: grid;
            grid-template-columns: 140px minmax(0, 1fr);
            gap: 12px;
            padding: 8px 0;
            border-top: 1px solid rgba(25, 33, 31, 0.08);
        }
        .feedback-line span {
            color: var(--muted);
            font-weight: 700;
        }
        .flow-overview {
            padding: 18px;
            margin: 10px 0 20px 0;
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
                padding-left: 1rem;
                padding-right: 1rem;
            }
            .app-title,
            .learning-header {
                grid-template-columns: 1fr;
                display: grid;
            }
            .pasuk-box {
                font-size: 2rem;
                padding: 20px;
                line-height: 2.15;
            }
            .phrase-box {
                font-size: 1.65rem;
            }
            .question-text {
                font-size: 1.24rem;
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
    apply_global_styles()

    questions = load_questions()
    progress = load_progress()
    ensure_progress_keys(progress, questions)

    st.markdown(
        """
        <header class="app-title">
            <div>
                <h1>Chumash Practice</h1>
                <p>Read the pasuk, notice the clue, then choose carefully.</p>
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

    practice_options = ["Learn Mode", "Practice Mode", "Pasuk Flow"]
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
