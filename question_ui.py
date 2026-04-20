"""Student-facing copy and follow-up helpers for the Streamlit runtime."""


COHORT_TAUGHT_TENSE_LABELS = {
    "past",
    "future",
    "present",
    "infinitive",
}


def _clean_tense_label(value):
    label = str(value or "").strip().lower()
    return label if label in COHORT_TAUGHT_TENSE_LABELS else ""


def tense_contrast_text(correct_answer="", selected_answer=""):
    correct = _clean_tense_label(correct_answer)
    selected = _clean_tense_label(selected_answer)
    pair = {correct, selected}

    if pair == {"present", "infinitive"}:
        return "Present = doing / is doing. Infinitive = to do."
    if pair == {"past", "future"}:
        return "Past = did. Future = will do."
    if correct == "present":
        return "Present = doing / is doing."
    if correct == "infinitive":
        return "Infinitive = to do."
    if correct == "past":
        return "Past = did."
    if correct == "future":
        return "Future = will do."
    return ""


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
            "why_this_question": f"You are practicing {skill_label.lower()} on a pasuk that supports it.",
            "what_to_focus_on": focus_tip or "Focus on the clue that separates the best answer from the close distractors.",
            "what_happens_next": f"Next you will see another {skill_label.lower()} question from {source_text}.",
        }

    current_text = current_skill_label or skill_label
    next_text = next_skill_label or current_text
    return {
        "why_this_question": (
            f"You are currently working on {current_text.lower()}. "
            f"This question was picked because it gives you a clean example from {source_text}."
        ),
        "what_to_focus_on": focus_tip or "Focus on the strongest clue before you translate or guess.",
        "what_happens_next": (
            f"If this skill feels steady, you will keep building toward {next_text.lower()}."
            if next_text != current_text
            else f"If this skill feels steady, you will keep strengthening {current_text.lower()}."
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
    if question_type in {"subject_identification", "role_clarity"} or skill in {"subject_identification", "object_identification"}:
        return "A strong noun can look important even when another clue is marking the real role."
    if question_type in {"phrase_meaning", "flow", "flow_dependency"} or skill == "phrase_translation":
        return "One part may have made sense on its own, but the phrase works only when the clues are read together."
    if question_type == "word_meaning" or skill == "translation" or standard == "WM":
        return "A close meaning may have sounded right, even though the best answer fits the pasuk more precisely."
    if skill == "shoresh":
        return "A surface form can hide the root if you focus on the whole word instead of the core letters."
    return "A nearby clue likely mattered more than the first answer that felt familiar."


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
            contrast = tense_contrast_text(question.get("correct_answer"), selected_answer)
            if contrast:
                return contrast
        clue = question.get("explanation") or ""
        return clue or "Watch the verb form; the marker shows the tense."

    return question.get("explanation") or ""


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
            summary = f"You may be close to moving from {skill_label.lower()} to {next_skill_label.lower()}."
        elif practice_type == "Practice Mode":
            summary = f"Next you will get another {skill_label.lower()} example."
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
        "summary": f"Next you can try one more {skill_label.lower()} item that stays close to this mistake.",
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
    next_skill_label=None,
):
    context = {
        "title": "Correct" if is_correct else "Incorrect",
        "grammar_feedback": _skill_specific_feedback(
            question,
            selected_answer=selected_answer,
            is_correct=is_correct,
        ),
        "selected_answer": selected_answer or "",
        "correct_answer": question.get("correct_answer", ""),
        "explanation": question.get("explanation", ""),
        "clue_that_mattered": clue_text or "",
        "likely_confusion": "" if is_correct else likely_confusion_text(question, selected_answer),
    }
    return context
