import json
from pathlib import Path

from skill_catalog import resolve_skill_id


PROGRESS_PATH = Path("skill_progress.json")
MASTERY_WINDOW = 12
MASTERY_ACCURACY = 0.85
MASTERY_STREAK = 5
WORD_EXPOSURE_KEY = "word_exposure"
WORD_MASTERY_MIN_SEEN = 5
WORD_MASTERY_ACCURACY = 0.80
WORD_MASTERY_STREAK = 2


def load_skill_progress():
    from progress_store import load_progress_state

    return load_progress_state()


def save_skill_progress(progress):
    from progress_store import save_progress_state

    save_progress_state(progress)


def default_skill_state():
    return {
        "score": 0,
        "correct_count": 0,
        "incorrect_count": 0,
        "current_streak": 0,
        "best_streak": 0,
        "challenge_streak": 0,
        "last_12_results": [],
        "error_counts": {},
        "mastered": False,
    }


def default_word_state():
    return {
        "seen": 0,
        "correct": 0,
        "recent_streak": 0,
        "mastered": False,
    }


def get_point_change(score, is_correct):
    if is_correct:
        if score < 80:
            return 5
        if score <= 90:
            return 3
        return 1

    if score < 80:
        return -5
    if score <= 90:
        return -8
    return -10


def clamp_score(score):
    return max(0, min(100, score))


def _skills_container(progress):
    if progress is None:
        return {}
    return progress.setdefault("skills", {})


def _word_exposure_container(progress):
    if progress is None:
        return {}
    return progress.setdefault(WORD_EXPOSURE_KEY, {})


def update_skill_progress_in_state(progress, skill, is_correct, error_type=None):
    skill = resolve_skill_id(skill) or skill
    skill_progress = _skills_container(progress)
    skill_state = skill_progress.setdefault(skill, default_skill_state())
    skill_state.setdefault("score", 0)
    skill_state.setdefault("best_streak", skill_state.get("current_streak", 0))
    skill_state.setdefault("challenge_streak", 0)
    skill_state.setdefault("error_counts", {})

    old_score = skill_state["score"]
    point_change = get_point_change(old_score, is_correct)

    if is_correct:
        skill_state["correct_count"] += 1
        skill_state["current_streak"] += 1
        skill_state["best_streak"] = max(
            skill_state["best_streak"],
            skill_state["current_streak"],
        )
        skill_state["score"] = clamp_score(old_score + point_change)
        if old_score >= 90:
            skill_state["challenge_streak"] += 1
        elif skill_state["score"] >= 90:
            skill_state["challenge_streak"] = 1
        else:
            skill_state["challenge_streak"] = 0

        if old_score >= 90 and skill_state["challenge_streak"] >= MASTERY_STREAK:
            skill_state["score"] = 100
    else:
        skill_state["incorrect_count"] += 1
        skill_state["current_streak"] = 0
        skill_state["challenge_streak"] = 0
        if error_type:
            skill_state["error_counts"][error_type] = (
                skill_state["error_counts"].get(error_type, 0) + 1
            )
        if old_score >= 90:
            skill_state["score"] = 85
        else:
            skill_state["score"] = clamp_score(old_score + point_change)

    skill_state["last_12_results"].append(bool(is_correct))
    skill_state["last_12_results"] = skill_state["last_12_results"][-MASTERY_WINDOW:]
    skill_state["mastered"] = check_mastery(skill, progress)
    skill_state["last_point_change"] = f"{point_change:+d}"
    recent_window = skill_state["last_12_results"][-5:]
    recent_accuracy = (
        sum(1 for item in recent_window if item) / len(recent_window)
        if recent_window
        else 0.0
    )
    return {
        "score": skill_state["score"],
        "current_streak": skill_state["current_streak"],
        "best_streak": skill_state["best_streak"],
        "mastered": skill_state["mastered"],
        "point_change": skill_state["last_point_change"],
        "error_counts": skill_state["error_counts"],
        "recent_accuracy": recent_accuracy,
        "recent_window_size": len(recent_window),
    }


def update_word_progress_in_state(progress, word, is_correct):
    word_progress = _word_exposure_container(progress)
    word_state = word_progress.setdefault(word, default_word_state())

    word_state.setdefault("seen", 0)
    word_state.setdefault("correct", 0)
    word_state.setdefault("recent_streak", 0)
    word_state.setdefault("mastered", False)

    word_state["seen"] += 1
    if is_correct:
        word_state["correct"] += 1
        word_state["recent_streak"] += 1
    else:
        word_state["recent_streak"] = 0

    word_state["mastered"] = check_word_mastery(word, progress)
    return word_state


def update_skill_progress(skill, is_correct, error_type=None, progress=None):
    if progress is None:
        from progress_store import load_progress_state, save_progress_state

        progress = load_progress_state()
        result = update_skill_progress_in_state(progress, skill, is_correct, error_type)
        save_progress_state(progress)
        return result

    return update_skill_progress_in_state(progress, skill, is_correct, error_type)


def update_word_progress(word, is_correct, progress=None):
    if progress is None:
        from progress_store import load_progress_state, save_progress_state

        progress = load_progress_state()
        result = update_word_progress_in_state(progress, word, is_correct)
        save_progress_state(progress)
        return result

    return update_word_progress_in_state(progress, word, is_correct)


def check_mastery(skill, progress=None):
    skill = resolve_skill_id(skill) or skill
    progress = progress or load_skill_progress()
    skill_state = progress.get("skills", {}).get(skill, progress.get(skill))
    if not skill_state:
        return False

    recent_results = skill_state.get("last_12_results", [])
    if len(recent_results) < MASTERY_WINDOW:
        return False

    accuracy = sum(recent_results) / MASTERY_WINDOW
    return (
        accuracy >= MASTERY_ACCURACY
        and skill_state.get("current_streak", 0) >= MASTERY_STREAK
    )


def check_word_mastery(word, progress=None):
    progress = progress or load_skill_progress()
    word_state = progress.get(WORD_EXPOSURE_KEY, {}).get(word)
    if not word_state:
        return False

    seen = word_state.get("seen", 0)
    if seen < WORD_MASTERY_MIN_SEEN:
        return False

    accuracy = word_state.get("correct", 0) / seen
    return (
        accuracy >= WORD_MASTERY_ACCURACY
        and word_state.get("recent_streak", 0) >= WORD_MASTERY_STREAK
    )


def recent_skill_accuracy(skill_state, window=5):
    recent_results = list((skill_state or {}).get("last_12_results", []))[-window:]
    if not recent_results:
        return 0.0
    return sum(1 for item in recent_results if item) / len(recent_results)


def dominant_error_type(skill_state):
    error_counts = dict((skill_state or {}).get("error_counts", {}))
    if not error_counts:
        return ""
    return max(error_counts, key=error_counts.get)
