from __future__ import annotations

import hashlib
from html import escape

import streamlit as st

from runtime.runtime_support import OPTION_LABELS, load_word_bank_metadata, menukad_text, mixed_text_html
from torah_parser.word_bank_adapter import normalize_hebrew_key

STUDENT_TENSE_LABELS = {
    "vav_consecutive_past": "past narrative",
    "future_jussive": "short future form",
    "future": "future",
    "past": "past",
    "present": "present",
    "infinitive": "infinitive",
    "command": "command",
}


def _clean_clue_value(value):
    text = str(value or "").strip()
    if not text:
        return None
    if set(text) == {"?"} or "???" in text:
        return None
    return text


def _clean_shoresh(value):
    text = _clean_clue_value(value)
    if not text or "?" in text:
        return None
    return text


def _student_tense_label(value):
    text = _clean_clue_value(value)
    if not text:
        return None
    return STUDENT_TENSE_LABELS.get(text, text)


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


def local_context_snippet(pasuk, focus, radius=2):
    tokens = menukad_text(pasuk).split()
    focus_text = menukad_text(focus)
    if not tokens or not focus_text:
        return ""

    focus_tokens = focus_text.split()
    if not focus_tokens:
        return ""

    match_index = None
    match_length = len(focus_tokens)
    for index in range(0, len(tokens) - match_length + 1):
        if tokens[index:index + match_length] == focus_tokens:
            match_index = index
            break

    if match_index is None and focus_text in tokens:
        match_index = tokens.index(focus_text)
        match_length = 1

    if match_index is None:
        return ""

    start = max(0, match_index - radius)
    end = min(len(tokens), match_index + match_length + radius)
    snippet = " ".join(tokens[start:end])
    if start > 0:
        snippet = "... " + snippet
    if end < len(tokens):
        snippet += " ..."
    return snippet


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


def clue_sentence(question):
    entry = get_word_entry(question)
    if entry:
        clues = []
        prefix = _clean_clue_value(entry.get("prefix"))
        prefix_meaning = _clean_clue_value(entry.get("prefix_meaning"))
        suffix = _clean_clue_value(entry.get("suffix"))
        suffix_meaning = _clean_clue_value(entry.get("suffix_meaning"))
        shoresh = _clean_shoresh(entry.get("shoresh"))
        tense = _student_tense_label(entry.get("tense"))
        if prefix and prefix_meaning:
            clues.append(f"{prefix} points to '{prefix_meaning}'")
        if suffix and suffix_meaning:
            clues.append(f"{suffix} at the end points to '{suffix_meaning}'")
        if shoresh:
            clues.append(f"the root is {shoresh}")
        if tense:
            clues.append(f"the verb form points to {tense}")
        if clues:
            return "; ".join(clues)

    if question.get("question_type") == "substitution":
        return "the changed word changes the job of the phrase"
    if question.get("question_type") in {"flow", "flow_dependency"}:
        return "the order of the clues shows how the action moves"
    if question.get("question_type") == "role_clarity":
        return "the word's place in the sentence shows its job"
    return "the nearby words support the correct meaning"


def render_grammar_clues(question):
    entry = get_word_entry(question)
    clues = []
    if entry:
        prefix = _clean_clue_value(entry.get("prefix"))
        prefix_meaning = _clean_clue_value(entry.get("prefix_meaning"))
        shoresh = _clean_shoresh(entry.get("shoresh"))
        suffix = _clean_clue_value(entry.get("suffix"))
        suffix_meaning = _clean_clue_value(entry.get("suffix_meaning"))
        tense = _student_tense_label(entry.get("tense"))
        if prefix and prefix_meaning:
            clues.append(f"{prefix} = {prefix_meaning}")
        if shoresh:
            clues.append(f"root clue: {shoresh}")
        if suffix and suffix_meaning:
            clues.append(f"{suffix} = {suffix_meaning}")
        if tense:
            clues.append(f"time clue: {tense}")

    if clues:
        st.markdown("**Key clues:**")
        st.markdown(mixed_text_html(" | ".join(clues)), unsafe_allow_html=True)


def answer_choice_label(choice, index):
    return f"{OPTION_LABELS[index]}. {menukad_text(choice)}"
