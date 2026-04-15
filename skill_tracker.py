import json
from pathlib import Path


PROGRESS_PATH = Path("skill_progress.json")
MASTERY_WINDOW = 12
MASTERY_ACCURACY = 0.85
MASTERY_STREAK = 5


def load_skill_progress():
    if not PROGRESS_PATH.exists():
        return {}

    with PROGRESS_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_skill_progress(progress):
    with PROGRESS_PATH.open("w", encoding="utf-8") as file:
        json.dump(progress, file, indent=2, ensure_ascii=False)


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


def update_skill_progress(skill, is_correct, error_type=None):
    progress = load_skill_progress()
    skill_state = progress.setdefault(skill, default_skill_state())
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

    save_skill_progress(progress)
    return {
        "score": skill_state["score"],
        "current_streak": skill_state["current_streak"],
        "best_streak": skill_state["best_streak"],
        "mastered": skill_state["mastered"],
        "point_change": skill_state["last_point_change"],
        "error_counts": skill_state["error_counts"],
    }


def check_mastery(skill, progress=None):
    progress = progress or load_skill_progress()
    skill_state = progress.get(skill)
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
