from __future__ import annotations

from skill_catalog import (
    MICRO_STANDARD_LABELS,
    STANDARD_LABELS,
    micro_standard_display_label,
    next_skill_id,
    resolve_skill_id,
    skill_display_label,
    skill_ids_in_runtime_order,
    standard_display_label,
)


MODE_LABELS = {
    "Adaptive": "Recommended Practice",
    "FLOW": "What happens in order",
    "Level 5": "Hard explanation questions",
    "Pasuk Flow": "Guided Pasuk Practice",
}

ERROR_TYPE_BY_SKILL = {
    "identify_prefix_meaning": "prefix_error",
    "identify_suffix_meaning": "suffix_error",
    "identify_verb_marker": "verb_marker_error",
}

SKILL_ORDER = skill_ids_in_runtime_order()

SKILL_NAMES = {
    **MODE_LABELS,
    **STANDARD_LABELS,
    **{skill_id: skill_display_label(skill_id) for skill_id in SKILL_ORDER},
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

MICRO_STANDARD_NAMES = dict(MICRO_STANDARD_LABELS)


def get_skill_level(xp):
    return (xp // 100) + 1


def get_skill_xp_progress(xp):
    return (xp % 100) / 100


def get_next_skill(current_skill):
    return next_skill_id(current_skill, 1)


def get_next_skill_by_steps(current_skill, steps=1):
    return next_skill_id(current_skill, steps)


def skill_path_label(skill):
    canonical_skill = resolve_skill_id(skill) or skill
    return SKILL_NAMES.get(canonical_skill, canonical_skill.replace("_", " ").title())


def question_focus_label(question):
    if not isinstance(question, dict):
        return plain_skill(question)

    skill = resolve_skill_id(question.get("skill"))
    if skill:
        return skill_path_label(skill)

    question_type = question.get("question_type")
    if question_type in QUESTION_TYPE_NAMES:
        return QUESTION_TYPE_NAMES[question_type]

    return standard_display_label(question.get("standard"), "Chumash Reading")


def student_skill_context(*, question=None, current_skill=None):
    current_label = skill_path_label(current_skill) if current_skill else ""
    focus_label = question_focus_label(question) if isinstance(question, dict) else ""

    if not current_label:
        current_label = focus_label or "Chumash Reading"
    if not focus_label:
        focus_label = current_label

    student_label = current_label
    if focus_label and focus_label != current_label:
        student_label = f"{current_label} · {focus_label}"

    return {
        "current_label": current_label,
        "focus_label": focus_label,
        "student_label": student_label,
    }


def get_error_type(skill):
    skill = resolve_skill_id(skill) or skill
    return ERROR_TYPE_BY_SKILL.get(skill)


def dominant_error_type(skill_state):
    error_counts = dict((skill_state or {}).get("error_counts", {}))
    if not error_counts:
        return ""
    return max(error_counts, key=error_counts.get)


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
        canonical = resolve_skill_id(question_or_mode)
        if canonical:
            return skill_path_label(canonical)
        return SKILL_NAMES.get(question_or_mode, question_or_mode)

    return question_focus_label(question_or_mode)


def learning_goal(question):
    if question.get("skill"):
        return question_focus_label(question)
    return micro_standard_display_label(question.get("micro_standard"), plain_skill(question))


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
