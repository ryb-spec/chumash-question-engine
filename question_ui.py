"""Student-facing copy and follow-up helpers for the Streamlit runtime."""

from runtime.presentation import student_skill_context


COHORT_TAUGHT_TENSE_LABELS = {
    "past",
    "future",
    "present",
    "to do form",
}
STUDENT_TENSE_LABEL_ALIASES = {
    "vav_consecutive_past": "past",
    "future_jussive": "future",
    "past narrative": "past",
    "short future form": "future",
    "infinitive": "to do form",
    "to do form": "to do form",
}
STUDENT_WORD_KIND_ALIASES = {
    "noun": "naming word",
    "verb": "action word",
    "particle": "small helper word",
    "prep": "direction word",
    "naming word": "naming word",
    "action word": "action word",
    "small helper word": "small helper word",
    "direction word": "direction word",
}
WORD_KIND_EXPLANATIONS = {
    "naming word": "a person, place, or thing",
    "action word": "something happening or being done",
    "small helper word": "a small clue word, not the main meaning word",
    "direction word": "a word like to, in, or from",
}
TENSE_MEANINGS = {
    "past": "did",
    "future": "will do",
    "present": "doing / is doing",
    "to do form": "to do",
}


def _clean_tense_label(value):
    label = str(value or "").strip().lower()
    label = STUDENT_TENSE_LABEL_ALIASES.get(label, label)
    return label if label in COHORT_TAUGHT_TENSE_LABELS else ""


def tense_contrast_text(correct_answer="", selected_answer=""):
    correct = _clean_tense_label(correct_answer)
    selected = _clean_tense_label(selected_answer)
    pair = {correct, selected}

    if pair == {"present", "to do form"}:
        return "Present = doing / is doing. 'To do' form = to do."
    if pair == {"past", "future"}:
        return "Past = did. Future = will do."
    if correct == "present":
        return "Present = doing / is doing."
    if correct == "to do form":
        return "'To do' form = to do."
    if correct == "past":
        return "Past = did."
    if correct == "future":
        return "Future = will do."
    return ""


def _clean_word_kind_label(value):
    label = STUDENT_WORD_KIND_ALIASES.get(str(value or "").strip().lower(), "")
    return label if label in WORD_KIND_EXPLANATIONS else ""


def _word_kind_article(label):
    if not label:
        return label
    article = "an" if label[0].lower() in {"a", "e", "i", "o", "u"} else "a"
    return f"{article} {label}"


def _grammar_gloss(question):
    gloss = str(question.get("word_gloss") or "").strip()
    token = question.get("selected_word") or question.get("word") or "This word"
    return token, gloss


def _clean_text(value):
    return str(value or "").strip()


def _sentence(text):
    text = _clean_text(text)
    if not text:
        return ""
    if text.endswith((".", "!", "?")):
        return text
    return f"{text}."


def _join_sentences(*parts):
    return " ".join(_sentence(part) for part in parts if _clean_text(part))


def _display_tense_label(label):
    if label == "to do form":
        return "'To do' form"
    return label.capitalize()


def _tense_form_phrase(label):
    custom_phrase = str(label or "").strip()
    if custom_phrase.startswith(("the ", "a ")):
        return custom_phrase
    if label == "to do form":
        return "the to do form"
    return f"the {label} form"


def tense_feedback_text(question, selected_answer=""):
    correct = _clean_tense_label(question.get("correct_answer"))
    selected = _clean_tense_label(selected_answer)
    token, gloss = _grammar_gloss(question)
    if not correct:
        return ""

    display_phrase = question.get("tense_display_phrase") or correct
    parts = []
    if gloss:
        parts.append(f"{token} means '{gloss}', so here it is {_tense_form_phrase(display_phrase)}.")
    if selected and selected != correct:
        parts.append(f"{_display_tense_label(selected)} would mean {TENSE_MEANINGS[selected]}.")
    elif correct in TENSE_MEANINGS:
        parts.append(f"{_display_tense_label(correct)} means {TENSE_MEANINGS[correct]}.")
    return " ".join(part for part in parts if part)


def word_kind_feedback_text(question, selected_answer=""):
    correct = _clean_word_kind_label(question.get("correct_answer"))
    selected = _clean_word_kind_label(selected_answer)
    token, gloss = _grammar_gloss(question)
    if not correct:
        return ""

    parts = []
    if gloss:
        parts.append(f"{token} means '{gloss}', so here it is {_word_kind_article(correct)}.")
    if selected and selected != correct:
        parts.append(
            f"{selected.capitalize()} would mean {WORD_KIND_EXPLANATIONS[selected]}."
        )
    elif correct in WORD_KIND_EXPLANATIONS:
        parts.append(f"{correct.capitalize()} means {WORD_KIND_EXPLANATIONS[correct]}.")
    return " ".join(part for part in parts if part)


def build_learning_context(
    *,
    practice_type,
    skill_label,
    current_skill_label=None,
    next_skill_label=None,
    source_label=None,
    focus_tip="",
):
    source_text = source_label or "the active parsed dataset"
    if practice_type == "Pasuk Flow":
        return {
            "why_this_question": "This step was chosen because it unlocks the next clue in this pasuk.",
            "what_to_focus_on": focus_tip or "Stay with the current clue before moving to the next step.",
            "what_happens_next": "After this answer, you will continue to the next step in the same pasuk.",
        }

    if practice_type == "Practice Mode":
        return {
            "why_this_question": f"You are practicing {skill_label} on a pasuk that supports it.",
            "what_to_focus_on": focus_tip or "Focus on the clue that separates the best answer from the close distractors.",
            "what_happens_next": f"Next you will see another {skill_label} question from {source_text}.",
        }

    current_text = current_skill_label or skill_label
    next_text = next_skill_label or current_text
    return {
        "why_this_question": (
            f"You are currently working on {current_text}. "
            f"This question was picked because it gives you a clean example from {source_text}."
        ),
        "what_to_focus_on": focus_tip or "Focus on the strongest clue before you translate or guess.",
        "what_happens_next": (
            f"If this skill feels steady, you will keep building toward {next_text}."
            if next_text != current_text
            else f"If this skill feels steady, you will keep strengthening {current_text}."
        ),
    }


def likely_confusion_text(question, selected_answer=""):
    question_type = question.get("question_type") or ""
    skill = question.get("skill") or ""
    standard = question.get("standard") or ""

    if question_type in {"prefix_suffix", "prefix", "suffix"} or "prefix" in skill or "suffix" in skill:
        return "A small letter clue can look like part of the base word if you read too quickly."
    if question_type == "verb_tense" or skill in {"verb_tense", "identify_tense", "identify_verb_marker"}:
        contrast = tense_contrast_text(question.get("correct_answer"), selected_answer)
        if contrast:
            return contrast
        return "Watch the verb form closely: the tense clue changes the whole meaning."
    if question_type == "part_of_speech" or skill == "part_of_speech":
        contrast = word_kind_feedback_text(question, selected_answer)
        if contrast:
            return contrast
        return ""
    if question_type in {"subject_identification", "role_clarity"} or skill in {"subject_identification", "object_identification"}:
        return "A strong noun can look important even when another clue is marking the real role."
    if question_type in {"phrase_meaning", "flow", "flow_dependency"} or skill == "phrase_translation":
        return "One part may have made sense on its own, but the phrase works only when the clues are read together."
    if question_type == "word_meaning" or skill == "translation" or standard == "WM":
        return "A close meaning may have sounded right, even though the best answer fits the pasuk more precisely."
    if skill == "shoresh":
        return "A surface form can hide the root if you focus on the whole word instead of the core letters."
    return ""


def _skill_specific_feedback(question, selected_answer="", is_correct=True):
    skill = question.get("skill") or ""
    question_type = question.get("question_type") or ""
    token = question.get("selected_word") or question.get("word") or "this word"
    prefix = question.get("prefix") or ""
    prefix_meaning = question.get("prefix_meaning") or ""
    suffix = question.get("suffix") or ""
    suffix_meaning = question.get("suffix_meaning") or ""
    shoresh = question.get("shoresh") or question.get("correct_answer") or ""

    if "prefix" in skill or "prefix" in question_type:
        if prefix and prefix_meaning:
            return f"Prefix: {prefix}. Here it means '{prefix_meaning}'."
        if prefix:
            return f"Prefix: {prefix}."

    if "suffix" in skill or "suffix" in question_type:
        if suffix and suffix_meaning:
            return f"Ending: {suffix}. Here it signals '{suffix_meaning}'."
        if suffix:
            return f"Ending: {suffix}."

    if skill == "shoresh" or question_type == "shoresh":
        if shoresh and token and shoresh != token:
            return f"Shoresh: {shoresh}. Read past the added letters in {token}."
        if shoresh:
            return f"Shoresh: {shoresh}."

    if question_type == "verb_tense" or skill in {"verb_tense", "identify_tense", "identify_verb_marker"}:
        if not is_correct:
            feedback = tense_feedback_text(question, selected_answer)
            if feedback:
                return feedback
        clue = question.get("explanation") or ""
        return clue or "Watch the verb form; the marker shows the tense."

    if question_type == "part_of_speech" or skill == "part_of_speech":
        if not is_correct:
            feedback = word_kind_feedback_text(question, selected_answer)
            if feedback:
                return feedback
        clue = question.get("explanation") or ""
        return clue or "Check what the full word means before you choose its kind."

    return question.get("explanation") or ""


def _prefix_feedback_fields(question, selected_answer=""):
    prefix = _clean_text(question.get("prefix"))
    prefix_meaning = _clean_text(question.get("prefix_meaning"))
    selected = _clean_text(selected_answer)
    token = _clean_text(question.get("selected_word") or question.get("word") or "This word")

    if not prefix:
        return {}

    return {
        "rule_text": f"Look for the prefix before the rest of the word",
        "core_text": f"Prefix {prefix} = '{prefix_meaning}'" if prefix_meaning else f"Prefix {prefix}",
        "here_text": (
            f"Here {token} uses {prefix} as '{prefix_meaning}'"
            if prefix_meaning
            else f"Here {token} keeps the clue from {prefix}"
        ),
        "tempting_wrong_text": (
            f"'{selected}' would need a different prefix clue"
            if selected and selected != _clean_text(question.get('correct_answer'))
            else ""
        ),
    }


def _suffix_feedback_fields(question, selected_answer=""):
    suffix = _clean_text(question.get("suffix"))
    suffix_meaning = _clean_text(question.get("suffix_meaning"))
    selected = _clean_text(selected_answer)
    token = _clean_text(question.get("selected_word") or question.get("word") or "This word")

    if not suffix:
        return {}

    return {
        "rule_text": "Look at the ending before you choose the meaning",
        "core_text": f"Ending {suffix} = '{suffix_meaning}'" if suffix_meaning else f"Ending {suffix}",
        "here_text": (
            f"Here {token} uses that ending as '{suffix_meaning}'"
            if suffix_meaning
            else f"Here {token} keeps the clue from {suffix}"
        ),
        "tempting_wrong_text": (
            f"'{selected}' would need a different ending clue"
            if selected and selected != _clean_text(question.get('correct_answer'))
            else ""
        ),
    }


def _shoresh_feedback_fields(question, selected_answer=""):
    token = _clean_text(question.get("selected_word") or question.get("word") or "This word")
    shoresh = _clean_text(question.get("shoresh") or question.get("correct_answer"))
    selected = _clean_text(selected_answer)
    if not shoresh:
        return {}

    return {
        "rule_text": "Read past the added letters to find the root",
        "core_text": f"Root: {shoresh}",
        "here_text": f"Here {token} is built on that root" if token and token != shoresh else "",
        "tempting_wrong_text": (
            f"'{selected}' matches the surface form more than the root"
            if selected and selected != shoresh
            else ""
        ),
    }


def _translation_feedback_fields(question, selected_answer=""):
    token = _clean_text(question.get("selected_word") or question.get("word") or "This word")
    correct = _clean_text(question.get("correct_answer"))
    selected = _clean_text(selected_answer)
    gloss = _clean_text(question.get("word_gloss"))
    prefix = _clean_text(question.get("prefix"))
    prefix_meaning = _clean_text(question.get("prefix_meaning"))
    suffix = _clean_text(question.get("suffix"))
    suffix_meaning = _clean_text(question.get("suffix_meaning"))

    rule_text = "Choose the meaning that fits the whole word here"
    core_parts = []
    if gloss and gloss != correct:
        core_parts.append(f"Core meaning: '{gloss}'")
    if prefix and prefix_meaning:
        rule_text = "Read the added letter with the base word"
        core_parts.append(f"Prefix {prefix} = '{prefix_meaning}'")
    if suffix and suffix_meaning:
        rule_text = "Read the ending with the base word"
        core_parts.append(f"Ending {suffix} = '{suffix_meaning}'")

    tempting = ""
    if selected and selected != correct:
        if prefix and prefix_meaning:
            tempting = f"'{selected}' misses the extra clue from {prefix}"
        elif suffix and suffix_meaning:
            tempting = f"'{selected}' misses the extra clue from the ending {suffix}"
        else:
            tempting = f"'{selected}' is close, but this pasuk points to '{correct}'"

    return {
        "rule_text": rule_text,
        "core_text": ". ".join(core_parts),
        "here_text": f"Here {token} means '{correct}'" if correct else "",
        "tempting_wrong_text": tempting,
    }


def _tense_feedback_fields(question, selected_answer=""):
    token, gloss = _grammar_gloss(question)
    correct = _clean_tense_label(question.get("correct_answer"))
    selected = _clean_tense_label(selected_answer)
    if not correct:
        return {}

    display_phrase = _clean_text(question.get("tense_display_phrase")) or _tense_form_phrase(correct)
    correct_display = _display_tense_label(correct)
    tempting = ""
    if selected and selected != correct:
        tempting = f"{_display_tense_label(selected)} would point to {TENSE_MEANINGS.get(selected, selected)}"

    return {
        "rule_text": "Look at the verb form, not just the first letter",
        "core_text": f"Core meaning: '{gloss}'" if gloss else "",
        "here_text": f"Here {token} uses {display_phrase}",
        "tempting_wrong_text": tempting,
        "secondary_detail": f"{correct_display} means {TENSE_MEANINGS[correct]}" if correct in TENSE_MEANINGS else "",
    }


def _part_of_speech_feedback_fields(question, selected_answer=""):
    token, gloss = _grammar_gloss(question)
    correct = _clean_word_kind_label(question.get("correct_answer"))
    selected = _clean_word_kind_label(selected_answer)
    if not correct:
        return {}

    tempting = ""
    if selected and selected != correct:
        tempting = f"{selected.capitalize()} would mean {WORD_KIND_EXPLANATIONS.get(selected, selected)}"

    return {
        "rule_text": "Decide what job the whole word does here",
        "core_text": f"Core meaning: '{gloss}'" if gloss else "",
        "here_text": f"Here {token} is {_word_kind_article(correct)}",
        "tempting_wrong_text": tempting,
        "secondary_detail": (
            f"{correct.capitalize()} means {WORD_KIND_EXPLANATIONS[correct]}"
            if correct in WORD_KIND_EXPLANATIONS
            else ""
        ),
    }


def _role_feedback_fields(question, selected_answer=""):
    explanation = _clean_text(question.get("explanation"))
    if not explanation:
        return {}
    return {
        "rule_text": explanation,
        "core_text": "",
        "here_text": "",
        "tempting_wrong_text": "",
    }


def instructional_feedback_fields(question, selected_answer="", is_correct=True):
    skill = question.get("skill") or ""
    question_type = question.get("question_type") or ""

    if "prefix" in skill or "prefix" in question_type:
        return _prefix_feedback_fields(question, selected_answer)
    if "suffix" in skill or "suffix" in question_type:
        return _suffix_feedback_fields(question, selected_answer)
    if skill == "shoresh" or question_type == "shoresh":
        return _shoresh_feedback_fields(question, selected_answer)
    if question_type == "verb_tense" or skill in {"verb_tense", "identify_tense", "identify_verb_marker"}:
        return _tense_feedback_fields(question, selected_answer)
    if question_type == "part_of_speech" or skill == "part_of_speech":
        return _part_of_speech_feedback_fields(question, selected_answer)
    if question_type in {"subject_identification", "object_identification", "role_clarity"} or skill in {"subject_identification", "object_identification"}:
        return _role_feedback_fields(question, selected_answer)
    if question_type == "word_meaning" or skill == "translation" or question.get("standard") == "WM":
        return _translation_feedback_fields(question, selected_answer)

    explanation = _clean_text(question.get("explanation"))
    clue = _clean_text(question.get("clue_text"))
    return {
        "rule_text": clue or explanation,
        "core_text": "",
        "here_text": "",
        "tempting_wrong_text": "",
    }


def build_followup_plan(*, practice_type, is_correct, skill_label, next_skill_label=None):
    if practice_type == "Pasuk Flow":
        return {
            "route": "flow_continue",
            "headline": "Keep the pasuk moving.",
            "summary": "The next step will stay in the same pasuk and build on this one.",
            "primary_label": "Next Step",
            "secondary_label": "",
        }

    if is_correct:
        if practice_type == "Learn Mode" and next_skill_label and next_skill_label != skill_label:
            summary = f"You may be close to moving from {skill_label} to {next_skill_label}."
        elif practice_type == "Practice Mode":
            summary = f"Next you will get another {skill_label} example."
        else:
            summary = "Next you will get another question in this guided path."
        return {
            "route": "normal_next",
            "headline": "Good. Keep going.",
            "summary": summary,
            "primary_label": "Next Question",
            "secondary_label": "",
        }

    return {
        "route": "retry_similar",
        "headline": "Let's reinforce that clue.",
        "summary": f"Next you can try one more {skill_label} item that stays close to this mistake.",
        "primary_label": "Try One Like This",
        "secondary_label": "Continue",
    }


def build_feedback_context(
    *,
    question,
    selected_answer,
    is_correct,
    clue_text,
    practice_type,
    skill_label,
    current_skill=None,
    next_skill_label=None,
):
    skill_context = student_skill_context(
        question=question,
        current_skill=current_skill or question.get("skill"),
    )
    fields = instructional_feedback_fields(
        question,
        selected_answer=selected_answer,
        is_correct=is_correct,
    )
    legacy_feedback = _join_sentences(
        fields.get("rule_text"),
        fields.get("core_text"),
        fields.get("here_text"),
        fields.get("tempting_wrong_text"),
    )
    secondary_detail = _clean_text(fields.get("secondary_detail"))
    explanation = _clean_text(question.get("explanation"))
    context = {
        "title": "Correct" if is_correct else "Incorrect",
        "student_skill_label": skill_context["student_label"],
        "current_skill_label": skill_context["current_label"],
        "focus_skill_label": skill_context["focus_label"],
        "rule_text": _clean_text(fields.get("rule_text")),
        "core_text": _clean_text(fields.get("core_text")),
        "here_text": _clean_text(fields.get("here_text")),
        "tempting_wrong_text": "" if is_correct else _clean_text(fields.get("tempting_wrong_text")),
        "secondary_detail": secondary_detail,
        "grammar_feedback": legacy_feedback or _skill_specific_feedback(
            question,
            selected_answer=selected_answer,
            is_correct=is_correct,
        ),
        "selected_answer": selected_answer or "",
        "correct_answer": question.get("correct_answer", ""),
        "explanation": explanation,
        "clue_that_mattered": clue_text or "",
        "likely_confusion": "" if is_correct else likely_confusion_text(question, selected_answer),
    }
    return context
