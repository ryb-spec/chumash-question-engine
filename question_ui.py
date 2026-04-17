"""Student-facing copy and follow-up helpers for the Streamlit runtime."""


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


def likely_confusion_text(question):
    question_type = question.get("question_type") or ""
    skill = question.get("skill") or ""
    standard = question.get("standard") or ""

    if question_type in {"prefix_suffix", "prefix", "suffix"} or "prefix" in skill or "suffix" in skill:
        return "A small letter clue can look like part of the base word if you read too quickly."
    if question_type == "verb_tense" or skill in {"verb_tense", "identify_tense", "identify_verb_marker"}:
        return "The verb form can look familiar even when the tense clue points in a different direction."
    if question_type in {"subject_identification", "role_clarity"} or skill in {"subject_identification", "object_identification"}:
        return "A strong noun can look important even when another clue is marking the real role."
    if question_type in {"phrase_meaning", "flow", "flow_dependency"} or skill == "phrase_translation":
        return "One part may have made sense on its own, but the phrase works only when the clues are read together."
    if question_type == "word_meaning" or skill == "translation" or standard == "WM":
        return "A close meaning may have sounded right, even though the best answer fits the pasuk more precisely."
    if skill == "shoresh":
        return "A surface form can hide the root if you focus on the whole word instead of the core letters."
    return "A nearby clue likely mattered more than the first answer that felt familiar."


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
    followup = build_followup_plan(
        practice_type=practice_type,
        is_correct=is_correct,
        skill_label=skill_label,
        next_skill_label=next_skill_label,
    )
    context = {
        "title": "Correct" if is_correct else "Incorrect",
        "clue_that_mattered": clue_text or "The strongest clue in the question mattered most here.",
        "likely_confusion": "" if is_correct else likely_confusion_text(question),
        "what_comes_next": followup["summary"],
        "followup": followup,
        "selected_answer": selected_answer or "",
        "correct_answer": question.get("correct_answer", ""),
        "explanation": question.get("explanation", ""),
    }
    return context
