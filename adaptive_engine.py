"""Focused adaptive mastery helpers for the supported Streamlit runtime."""

from skill_catalog import next_skill_id, resolve_skill_id
from runtime.presentation import dominant_error_type

RECENT_DECISION_WINDOW = 5
RETEACH_WINDOW = 4
FAST_PASS_WINDOW = 5
DOUBLE_FAST_PASS_WINDOW = 6


def recent_results(skill_state, window=RECENT_DECISION_WINDOW):
    return list((skill_state or {}).get("last_12_results", []))[-window:]


def recent_accuracy(skill_state, window=RECENT_DECISION_WINDOW):
    results = recent_results(skill_state, window)
    if not results:
        return 0.0
    return sum(1 for item in results if item) / len(results)
def next_skill_in_order(current_skill, skill_order, steps=1):
    if not skill_order:
        return next_skill_id(current_skill, steps)
    current_skill = resolve_skill_id(current_skill) or current_skill
    skill_order = [resolve_skill_id(skill) or skill for skill in skill_order]
    try:
        index = skill_order.index(current_skill)
    except ValueError:
        return skill_order[0]
    target_index = min(len(skill_order) - 1, index + max(0, steps))
    return skill_order[target_index]


def clustered_errors(skill_state):
    results = recent_results(skill_state, RETEACH_WINDOW)
    if len(results) < 2:
        return False
    recent_false = len([item for item in results if not item])
    if len(results) >= 4 and recent_false >= 2:
        return True
    if len(results) >= 2 and results[-2:] == [False, False]:
        return True
    return False


def reteach_needed(skill_state, is_correct):
    if is_correct:
        return False
    if clustered_errors(skill_state):
        return True
    error_counts = dict((skill_state or {}).get("error_counts", {}))
    return bool(error_counts and max(error_counts.values()) >= 2)


def fast_pass_ready(skill_state, is_correct):
    if not is_correct:
        return False
    results = recent_results(skill_state, FAST_PASS_WINDOW)
    if len(results) < 4:
        return False
    return (
        recent_accuracy(skill_state, FAST_PASS_WINDOW) >= 0.8
        and (skill_state or {}).get("current_streak", 0) >= 4
        and (skill_state or {}).get("score", 0) >= 70
    )


def double_fast_pass_ready(skill_state, is_correct):
    if not is_correct:
        return False
    results = recent_results(skill_state, DOUBLE_FAST_PASS_WINDOW)
    if len(results) < DOUBLE_FAST_PASS_WINDOW:
        return False
    return (
        all(results)
        and (skill_state or {}).get("current_streak", 0) >= 6
        and (skill_state or {}).get("score", 0) >= 90
        and (skill_state or {}).get("challenge_streak", 0) >= 2
    )


def challenge_ready(skill_state, is_correct):
    if not is_correct:
        return False
    results = recent_results(skill_state, FAST_PASS_WINDOW)
    if len(results) < 3:
        return False
    return (
        recent_accuracy(skill_state, FAST_PASS_WINDOW) >= 0.75
        and (skill_state or {}).get("current_streak", 0) >= 2
    )


def decision_message(route, current_skill_label, target_skill_label, dominant_error):
    if route == "reteach_same_skill":
        if dominant_error:
            return (
                f"We are staying with {current_skill_label.lower()} for one more round "
                f"because recent mistakes clustered around {dominant_error.replace('_', ' ')}."
            )
        return f"We are staying with {current_skill_label.lower()} for one more round to reinforce the recent misses."
    if route == "advance":
        return f"You locked in {current_skill_label.lower()}, so we are moving to {target_skill_label.lower()}."
    if route == "fast_pass":
        return (
            f"Your recent run on {current_skill_label.lower()} was strong enough to move early into "
            f"{target_skill_label.lower()}."
        )
    if route == "double_fast_pass":
        return (
            f"Your recent answers were exceptionally strong, so we are jumping ahead to "
            f"{target_skill_label.lower()}."
        )
    if route == "challenge_same_skill":
        return f"You are doing well, so the next {current_skill_label.lower()} question will stretch you a bit."
    return f"We are keeping the focus on {current_skill_label.lower()} for the next question."


def selection_mode_for(route):
    if route == "reteach_same_skill":
        return "reteach"
    if route == "challenge_same_skill":
        return "challenge"
    if route in {"fast_pass", "double_fast_pass", "advance"}:
        return "fresh_skill"
    return "steady"


def evaluate_skill_progression(
    *,
    current_skill,
    answered_skill,
    skill_state,
    is_correct,
    skill_order,
    skill_label,
    next_skill_label,
):
    if answered_skill != current_skill:
        return {
            "route": "steady_same_skill",
            "target_skill": current_skill,
            "selection_mode": "steady",
            "message": "",
            "reason": "",
            "advanced": False,
        }

    dominant_error = dominant_error_type(skill_state)
    if reteach_needed(skill_state, is_correct):
        return {
            "route": "reteach_same_skill",
            "target_skill": current_skill,
            "selection_mode": selection_mode_for("reteach_same_skill"),
            "message": decision_message("reteach_same_skill", skill_label, next_skill_label, dominant_error),
            "reason": "recent mistakes clustered, so the skill is repeating with a tighter follow-up",
            "advanced": False,
        }

    if skill_state.get("mastered"):
        target_skill = next_skill_in_order(current_skill, skill_order, 1)
        route = "advance" if target_skill != current_skill else "steady_same_skill"
        return {
            "route": route,
            "target_skill": target_skill,
            "selection_mode": selection_mode_for(route),
            "message": decision_message(route, skill_label, next_skill_label, dominant_error),
            "reason": "mastery threshold reached in the current skill",
            "advanced": target_skill != current_skill,
        }

    if double_fast_pass_ready(skill_state, is_correct):
        target_skill = next_skill_in_order(current_skill, skill_order, 2)
        route = "double_fast_pass" if target_skill != current_skill else "steady_same_skill"
        return {
            "route": route,
            "target_skill": target_skill,
            "selection_mode": selection_mode_for(route),
            "message": decision_message(route, skill_label, next_skill_label, dominant_error),
            "reason": "recent perfect run plus strong challenge streak",
            "advanced": target_skill != current_skill,
        }

    if fast_pass_ready(skill_state, is_correct):
        target_skill = next_skill_in_order(current_skill, skill_order, 1)
        route = "fast_pass" if target_skill != current_skill else "steady_same_skill"
        return {
            "route": route,
            "target_skill": target_skill,
            "selection_mode": selection_mode_for(route),
            "message": decision_message(route, skill_label, next_skill_label, dominant_error),
            "reason": "recent accuracy and streak show strong confidence",
            "advanced": target_skill != current_skill,
        }

    if challenge_ready(skill_state, is_correct):
        return {
            "route": "challenge_same_skill",
            "target_skill": current_skill,
            "selection_mode": selection_mode_for("challenge_same_skill"),
            "message": decision_message("challenge_same_skill", skill_label, next_skill_label, dominant_error),
            "reason": "recent answers are strong but not ready to move on yet",
            "advanced": False,
        }

    return {
        "route": "steady_same_skill",
        "target_skill": current_skill,
        "selection_mode": selection_mode_for("steady_same_skill"),
        "message": decision_message("steady_same_skill", skill_label, next_skill_label, dominant_error),
        "reason": "the current skill still needs a steady sample of correct work",
        "advanced": False,
    }


def build_selection_preferences(decision, question=None):
    question = question or {}
    return {
        "route": decision.get("route", "steady_same_skill"),
        "selection_mode": decision.get("selection_mode", "steady"),
        "preferred_pasuk": question.get("pasuk"),
        "avoid_word": question.get("selected_word") or question.get("word"),
        "reason": decision.get("reason", ""),
    }


def candidate_weight(row, progress, recent_pesukim, recent_words, adaptive_context=None):
    adaptive_context = adaptive_context or {}
    route = adaptive_context.get("selection_mode", "steady")
    word = row.get("word") or ""
    pasuk = row.get("pasuk") or ""
    word_state = dict((progress or {}).get("word_exposure", {}).get(word, {}))
    seen = word_state.get("seen", 0)
    mastered = bool(word_state.get("mastered"))
    accuracy = (
        word_state.get("correct", 0) / seen
        if seen
        else 0.0
    )

    score = 1
    if pasuk not in recent_pesukim[-5:]:
        score += 3
    if word and word not in recent_words[-5:]:
        score += 2
    if not mastered:
        score += 1

    if route == "reteach":
        if pasuk and pasuk == adaptive_context.get("preferred_pasuk"):
            score += 5
        if word and word == adaptive_context.get("avoid_word"):
            score -= 3
        if seen and accuracy < 0.7:
            score += 3
        if mastered:
            score -= 2
    elif route == "challenge":
        if seen == 0:
            score += 4
        elif seen <= 2:
            score += 2
        if mastered:
            score -= 3
        if pasuk not in recent_pesukim[-5:]:
            score += 2
    elif route == "fresh_skill":
        if seen == 0:
            score += 3
        if pasuk not in recent_pesukim[-5:]:
            score += 2
    else:
        if seen == 0:
            score += 1

    return score
