import json
from pathlib import Path

from assessment_scope import repo_path
from skill_catalog import adaptive_standard_ids, resolve_skill_id, skill_ids_in_runtime_order
from skill_tracker import (
    update_skill_progress_in_state,
    update_word_progress_in_state,
)


UNIFIED_PROGRESS_PATH = repo_path("progress.json")
LEGACY_SKILL_PROGRESS_PATH = repo_path("skill_progress.json")
SCHEMA_VERSION = 2
DEFAULT_STANDARDS = tuple(adaptive_standard_ids())
DEFAULT_CURRENT_SKILL = skill_ids_in_runtime_order()[0]


def load_json(path):
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def default_progress_state():
    return {
        "schema_version": SCHEMA_VERSION,
        "words": {},
        "standards": {standard: 0 for standard in DEFAULT_STANDARDS},
        "micro_standards": {},
        "xp": {standard: 0 for standard in DEFAULT_STANDARDS},
        "current_skill": DEFAULT_CURRENT_SKILL,
        "prefix_level": 1,
        "recent_pesukim": [],
        "adaptive_state": {"last_decision": {}, "history": []},
        "skills": {},
        "word_exposure": {},
    }


def _normalized_skill_state(skill_state):
    normalized = {
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
    normalized.update(skill_state or {})
    normalized.setdefault("last_point_change", "+0")
    normalized["last_12_results"] = list(normalized.get("last_12_results", []))
    normalized["error_counts"] = dict(normalized.get("error_counts", {}))
    return normalized


def _normalized_word_state(word_state):
    normalized = {
        "seen": 0,
        "correct": 0,
        "recent_streak": 0,
        "mastered": False,
    }
    normalized.update(word_state or {})
    return normalized


def ensure_progress_state(progress):
    state = default_progress_state()
    if isinstance(progress, dict):
        for key, value in progress.items():
            state[key] = value

    state["schema_version"] = SCHEMA_VERSION
    state["words"] = dict(state.get("words", {}))
    state["micro_standards"] = dict(state.get("micro_standards", {}))
    state["recent_pesukim"] = list(state.get("recent_pesukim", []))
    adaptive_state = dict(state.get("adaptive_state", {}))
    adaptive_state.setdefault("last_decision", {})
    adaptive_state["history"] = list(adaptive_state.get("history", []))[-20:]
    state["adaptive_state"] = adaptive_state

    standards = dict(state.get("standards", {}))
    xp = dict(state.get("xp", {}))
    for standard in DEFAULT_STANDARDS:
        standards.setdefault(standard, 0)
        xp.setdefault(standard, 0)
    state["standards"] = standards
    state["xp"] = xp

    state["current_skill"] = resolve_skill_id(state.get("current_skill")) or state.get("current_skill") or DEFAULT_CURRENT_SKILL
    state["prefix_level"] = state.get("prefix_level", 1) or 1

    normalized_skills = {}
    for skill, skill_state in dict(state.get("skills", {})).items():
        canonical_skill = resolve_skill_id(skill) or skill
        merged_state = dict(normalized_skills.get(canonical_skill, {}))
        merged_state.update(skill_state or {})
        normalized_skills[canonical_skill] = _normalized_skill_state(merged_state)
    state["skills"] = normalized_skills
    state["word_exposure"] = {
        word: _normalized_word_state(word_state)
        for word, word_state in dict(state.get("word_exposure", {})).items()
    }
    return state


def migrate_legacy_progress(progress_data=None, skill_progress_data=None):
    state = ensure_progress_state(progress_data or {})

    legacy_skill_progress = dict(skill_progress_data or {})
    legacy_word_exposure = legacy_skill_progress.pop("word_exposure", {})

    for word, word_state in legacy_word_exposure.items():
        merged = dict(state["word_exposure"].get(word, {}))
        merged.update(word_state or {})
        state["word_exposure"][word] = _normalized_word_state(merged)

    for skill, skill_state in legacy_skill_progress.items():
        merged = dict(state["skills"].get(skill, {}))
        merged.update(skill_state or {})
        state["skills"][skill] = _normalized_skill_state(merged)

    return ensure_progress_state(state)


def load_progress_state(progress_path=UNIFIED_PROGRESS_PATH, legacy_skill_path=LEGACY_SKILL_PROGRESS_PATH):
    progress_data = load_json(progress_path)
    skill_progress_data = load_json(legacy_skill_path)

    already_unified = (
        isinstance(progress_data, dict)
        and progress_data.get("schema_version") == SCHEMA_VERSION
        and "skills" in progress_data
        and "word_exposure" in progress_data
    )

    if already_unified and skill_progress_data is None:
        return ensure_progress_state(progress_data)

    state = migrate_legacy_progress(progress_data, skill_progress_data)
    save_progress_state(state, progress_path=progress_path)
    return state


def save_progress_state(progress, progress_path=UNIFIED_PROGRESS_PATH):
    state = ensure_progress_state(progress)
    with progress_path.open("w", encoding="utf-8") as file:
        json.dump(state, file, indent=2, ensure_ascii=False)
    return state


def record_answer(progress, question, is_correct, error_type=None):
    state = ensure_progress_state(progress)
    amount = 10 if is_correct else -10
    xp_gain = 15 if is_correct else 3
    word = question["word"]
    standard = question["standard"]
    micro_standard = question["micro_standard"]

    state["words"].setdefault(word, 0)
    state["standards"].setdefault(standard, 0)
    state["micro_standards"].setdefault(micro_standard, 0)
    state["xp"].setdefault(standard, 0)

    state["words"][word] = max(0, min(100, state["words"].get(word, 0) + amount))
    state["standards"][standard] = max(0, min(100, state["standards"].get(standard, 0) + amount))
    state["micro_standards"][micro_standard] = max(
        0,
        min(100, state["micro_standards"].get(micro_standard, 0) + amount),
    )
    state["xp"][standard] = state["xp"].get(standard, 0) + xp_gain

    skill = question.get("skill", question.get("standard", "unknown"))
    skill_state = update_skill_progress_in_state(state, skill, is_correct, error_type)

    asked_token = question.get("selected_word") or question.get("word")
    word_state = None
    if asked_token:
        word_state = update_word_progress_in_state(state, asked_token, is_correct)

    if isinstance(progress, dict):
        progress.clear()
        progress.update(state)

    return {
        "progress": state,
        "skill": skill,
        "skill_state": skill_state,
        "asked_token": asked_token,
        "word_state": word_state,
    }
