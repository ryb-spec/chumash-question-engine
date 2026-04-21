from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
ATTEMPT_LOG_PATH = BASE_DIR / "data" / "attempt_log.jsonl"
PILOT_EVENT_LOG_PATH = BASE_DIR / "data" / "pilot" / "pilot_session_events.jsonl"
OUTPUT_PATH = BASE_DIR / "data" / "validation" / "nightly_insights.md"


def load_attempts(path: Path) -> list[dict]:
    attempts = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                attempts.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return attempts


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def top_lines(counter: Counter, label: str, limit: int = 10) -> list[str]:
    if not counter:
        return [f"- No {label.lower()} recorded."]
    return [f"- `{item}`: {count}" for item, count in counter.most_common(limit)]


def threshold_lines(counter: Counter, label: str, minimum: int) -> list[str]:
    rows = [(item, count) for item, count in counter.most_common() if count >= minimum]
    if not rows:
        return [f"- No {label.lower()} met the threshold."]
    return [f"- `{item}`: {count}" for item, count in rows]


def suggestion_lines(
    missed_words: Counter,
    missed_skills: Counter,
    missed_question_types: Counter,
    missed_standards: Counter,
) -> list[str]:
    suggestions = []

    top_skill, top_skill_count = missed_skills.most_common(1)[0] if missed_skills else (None, 0)
    if top_skill == "identify_prefix_meaning":
        suggestions.append("- Review prefix meaning questions.")
    elif top_skill == "identify_suffix_meaning":
        suggestions.append("- Review suffix meaning questions.")
    elif top_skill:
        suggestions.append(f"- Review {top_skill} questions.")

    frequent_words = [word for word, count in missed_words.most_common() if count >= 3]
    if frequent_words:
        word_text = ", ".join(frequent_words[:3])
        if len(frequent_words) == 1:
            suggestions.append(f"- Add more gold cases for {word_text} and closely related forms.")
        else:
            suggestions.append(f"- Add more gold cases for {word_text}, and related forms.")

    top_question_type, _ = (
        missed_question_types.most_common(1)[0] if missed_question_types else (None, 0)
    )
    if top_question_type == "prefix":
        suggestions.append("- Add more prefix-focused review items in the next practice cycle.")
    elif top_question_type == "suffix":
        suggestions.append("- Add more suffix-focused review items in the next practice cycle.")
    elif top_question_type:
        suggestions.append(f"- Review the {top_question_type} question type with a few extra examples.")

    top_standard, _ = missed_standards.most_common(1)[0] if missed_standards else (None, 0)
    if top_standard:
        suggestions.append(f"- Revisit standard {top_standard} with a short targeted review set.")

    if not suggestions:
        return ["- No clear review targets yet."]

    deduped = []
    seen = set()
    for suggestion in suggestions:
        if suggestion in seen:
            continue
        seen.add(suggestion)
        deduped.append(suggestion)
    return deduped


def next_action_lines(
    missed_words: Counter,
    missed_skills: Counter,
    missed_question_types: Counter,
    missed_standards: Counter,
) -> list[str]:
    actions = []

    if missed_question_types.get("suffix", 0) >= 5:
        actions.append("- Prioritize noun suffix fallback fixes.")
    if missed_question_types.get("prefix", 0) >= 5:
        actions.append("- Tighten prefix handling and add more prefix review coverage.")
    if missed_standards.get("PR", 0) >= 5:
        actions.append("- Add reteach practice for PR-standard items.")

    repeated_words = [word for word, count in missed_words.most_common() if count >= 3]
    if repeated_words:
        actions.append("- Expand gold cases for repeated trouble words.")

    suffix_heavy_words = [word for word in repeated_words if word.endswith(("ו", "הו"))]
    if suffix_heavy_words:
        actions.append("- Review suffix-bearing noun forms that are still being over-literalized.")

    top_skill, _ = missed_skills.most_common(1)[0] if missed_skills else (None, 0)
    if top_skill == "identify_prefix_meaning":
        actions.append("- Review prefix meaning distractors and reteach sequencing.")
    elif top_skill == "identify_suffix_meaning":
        actions.append("- Review suffix meaning distractors and reteach sequencing.")

    if not actions:
        return ["- No urgent next actions yet."]

    deduped = []
    seen = set()
    for action in actions:
        if action in seen:
            continue
        seen.add(action)
        deduped.append(action)
    return deduped


def gold_failure_lines() -> list[str]:
    # We do not yet maintain a dedicated gold-failure summary artifact, so the
    # nightly report surfaces a placeholder until one exists.
    return ["- No gold-failure summary is available yet."]


def pilot_repeat_lines(events: list[dict], *, group_key: str, label: str, limit: int = 5) -> list[str]:
    served = [
        event for event in events
        if event.get("event_type") == "question_served" and event.get("served_status") == "served"
    ]
    counts = Counter()
    for event in served:
        question_type = event.get("question_type") or "unknown"
        group_value = event.get(group_key) or ""
        if not group_value:
            continue
        counts[(question_type, group_value)] += 1
    repeated = [(item, count) for item, count in counts.most_common(limit) if count > 1]
    if not repeated:
        return [f"- No repeated {label.lower()} recorded."]
    return [f"- `{question_type}` -> `{value}`: {count}" for (question_type, value), count in repeated]


def normalized_translation_meaning(value: str | None) -> str:
    text = " ".join(str(value or "").split()).lower()
    if not text:
        return ""
    if text not in {"god", "g-d", "lord", "the lord", "the lord god"}:
        for prefix in ("the ", "a ", "an "):
            if text.startswith(prefix):
                text = text[len(prefix):]
                break
    return text


def shoresh_surface_pattern(value: str | None) -> str:
    text = str(value or "").strip()
    if text.startswith("וַי"):
        return "vav_yod_surface"
    if text.startswith("וְת"):
        return "vav_tav_surface"
    if text.startswith("ו"):
        return "vav_led_surface"
    return "plain_surface"


def pilot_translation_meaning_repeat_lines(events: list[dict], *, limit: int = 5) -> list[str]:
    served = [
        event for event in events
        if event.get("event_type") == "question_served"
        and event.get("served_status") == "served"
        and event.get("question_type") in {"translation", "word_meaning"}
    ]
    counts = Counter()
    for event in served:
        meaning = normalized_translation_meaning(event.get("correct_answer"))
        if not meaning:
            continue
        counts[meaning] += 1
    repeated = [(meaning, count) for meaning, count in counts.most_common(limit) if count > 1]
    if not repeated:
        return ["- No repeated translation meanings recorded."]
    return [f"- `{meaning}`: {count}" for meaning, count in repeated]


def pilot_tense_lane_overlap_lines(events: list[dict], *, limit: int = 5) -> list[str]:
    served = [
        event for event in events
        if event.get("event_type") == "question_served"
        and event.get("served_status") == "served"
        and event.get("question_type") in {"identify_tense", "verb_tense"}
    ]
    by_target: dict[str, set[str]] = {}
    for event in served:
        target = event.get("selected_word") or ""
        lane = event.get("question_type") or ""
        if not target or not lane:
            continue
        by_target.setdefault(target, set()).add(lane)
    overlap = sorted(
        [
            (target, sorted(lanes))
            for target, lanes in by_target.items()
            if len(lanes) > 1
        ],
        key=lambda item: (-len(item[1]), item[0]),
    )
    if not overlap:
        return ["- No tense targets were served through both tense lanes."]
    return [f"- `{target}`: {', '.join(lanes)}" for target, lanes in overlap[:limit]]


def pilot_shoresh_surface_lines(events: list[dict]) -> list[str]:
    served = [
        event for event in events
        if event.get("event_type") == "question_served"
        and event.get("served_status") == "served"
        and event.get("question_type") == "shoresh"
    ]
    counts = Counter(
        shoresh_surface_pattern(event.get("selected_word"))
        for event in served
        if event.get("selected_word")
    )
    if not counts:
        return ["- No shoresh questions were served yet."]
    return [f"- `{pattern}`: {count}" for pattern, count in counts.most_common()]


def pilot_lane_concentration_lines(events: list[dict], *, limit: int = 6) -> list[str]:
    served = [
        event for event in events
        if event.get("event_type") == "question_served" and event.get("served_status") == "served"
    ]
    by_lane: dict[str, Counter] = {}
    for event in served:
        lane = event.get("question_type") or "unknown"
        answer = event.get("correct_answer") or ""
        if not answer:
            continue
        by_lane.setdefault(lane, Counter())[answer] += 1
    rows = []
    for lane, counter in by_lane.items():
        total = sum(counter.values())
        answer, count = counter.most_common(1)[0]
        share = round((count / total) * 100) if total else 0
        rows.append((share, count, lane, answer, total))
    rows.sort(reverse=True)
    if not rows:
        return ["- No served question lanes recorded."]
    return [
        f"- `{lane}` -> `{answer}`: {count}/{total} ({share}%)"
        for share, count, lane, answer, total in rows[:limit]
    ]


def pilot_reuse_lines(events: list[dict]) -> list[str]:
    served = [
        event for event in events
        if event.get("event_type") == "question_served" and event.get("served_status") == "served"
    ]
    reuse_counts = Counter(
        event.get("debug_reuse_mode")
        for event in served
        if event.get("debug_reuse_mode")
    )
    if not reuse_counts:
        return ["- No reuse events recorded yet."]
    return [f"- `{mode}`: {count}" for mode, count in reuse_counts.most_common()]


def pilot_diversity_redirect_lines(events: list[dict]) -> list[str]:
    served = [
        event for event in events
        if event.get("event_type") == "question_served" and event.get("served_status") == "served"
    ]
    redirects = Counter(
        event.get("debug_variety_guard_source")
        for event in served
        if event.get("debug_variety_guard_applied") and event.get("debug_variety_guard_source")
    )
    if not redirects:
        return ["- No diversity redirects recorded yet."]
    return [f"- `{skill}`: {count}" for skill, count in redirects.most_common()]


def pilot_validation_rejection_lines(events: list[dict], *, limit: int = 10) -> list[str]:
    served = [
        event for event in events
        if event.get("event_type") == "question_served"
    ]
    counts = Counter()
    for event in served:
        for code, count in (event.get("debug_rejection_counts") or {}).items():
            counts[code] += count
    if not counts:
        return ["- No pre-serve rejection counts recorded yet."]
    return [f"- `{code}`: {count}" for code, count in counts.most_common(limit)]


def pilot_validation_rejections_by_lane_lines(events: list[dict], *, limit: int = 10) -> list[str]:
    served = [
        event for event in events
        if event.get("event_type") == "question_served"
    ]
    counts = Counter()
    for event in served:
        lane = event.get("question_type") or event.get("skill") or "unknown"
        for code, count in (event.get("debug_rejection_counts") or {}).items():
            counts[(lane, code)] += count
    rows = [(item, count) for item, count in counts.most_common(limit) if count > 0]
    if not rows:
        return ["- No lane-specific rejection counts recorded yet."]
    return [f"- `{lane}` -> `{code}`: {count}" for (lane, code), count in rows]


def pilot_validation_bypass_lines(events: list[dict]) -> list[str]:
    served = [
        event for event in events
        if event.get("event_type") == "question_served" and event.get("served_status") == "served"
    ]
    validated = sum(1 for event in served if event.get("debug_pre_serve_validation_passed"))
    bypassed = len(served) - validated
    if not served:
        return ["- No served questions recorded yet."]
    return [
        f"- Served with validation flag: {validated}",
        f"- Served missing validation flag: {bypassed}",
    ]


def pilot_scope_safety_lines(events: list[dict]) -> list[str]:
    served = [
        event for event in events
        if event.get("event_type") == "question_served" and event.get("served_status") == "served"
    ]
    unmapped = [
        event for event in served
        if event.get("scope_membership") != "active_parsed"
    ]
    if not served:
        return ["- No served questions recorded yet."]
    if not unmapped:
        return ["- No served questions were outside the active parsed dataset."]
    counts = Counter(event.get("question_type") or "unknown" for event in unmapped)
    return [f"- `{lane}`: {count}" for lane, count in counts.most_common()]


def build_report() -> str:
    attempts = load_attempts(ATTEMPT_LOG_PATH) if ATTEMPT_LOG_PATH.exists() else []
    incorrect_attempts = [row for row in attempts if not row.get("is_correct")]

    missed_words = Counter()
    missed_skills = Counter()
    missed_question_types = Counter()
    missed_standards = Counter()

    for row in incorrect_attempts:
        word = row.get("selected_word") or row.get("word")
        skill = row.get("skill") or row.get("question_type") or row.get("standard")
        question_type = row.get("question_type")
        standard = row.get("standard")
        if word:
            missed_words[word] += 1
        if skill:
            missed_skills[skill] += 1
        if question_type:
            missed_question_types[question_type] += 1
        if standard:
            missed_standards[standard] += 1

    suggestions = suggestion_lines(
        missed_words,
        missed_skills,
        missed_question_types,
        missed_standards,
    )
    next_actions = next_action_lines(
        missed_words,
        missed_skills,
        missed_question_types,
        missed_standards,
    )
    gold_failures = gold_failure_lines()
    pilot_events = load_jsonl(PILOT_EVENT_LOG_PATH)
    pilot_prompt_lines = pilot_repeat_lines(pilot_events, group_key="question_text", label="Prompts")
    pilot_target_lines = pilot_repeat_lines(pilot_events, group_key="selected_word", label="Target Words")
    pilot_meaning_lines = pilot_translation_meaning_repeat_lines(pilot_events)
    pilot_tense_overlap_lineset = pilot_tense_lane_overlap_lines(pilot_events)
    pilot_shoresh_surfaces = pilot_shoresh_surface_lines(pilot_events)
    pilot_concentration = pilot_lane_concentration_lines(pilot_events)
    pilot_reuse = pilot_reuse_lines(pilot_events)
    pilot_redirects = pilot_diversity_redirect_lines(pilot_events)
    pilot_validation_rejections = pilot_validation_rejection_lines(pilot_events)
    pilot_validation_by_lane = pilot_validation_rejections_by_lane_lines(pilot_events)
    pilot_validation_bypass = pilot_validation_bypass_lines(pilot_events)
    pilot_scope_safety = pilot_scope_safety_lines(pilot_events)

    lines = [
        "# Nightly Insights",
        "",
        "## Summary",
        "",
        f"- Total attempts: {len(attempts)}",
        f"- Total incorrect: {len(incorrect_attempts)}",
        "",
        "## Most Missed Words",
        "",
        *top_lines(missed_words, "Words"),
        "",
        "## Most Missed Skills",
        "",
        *top_lines(missed_skills, "Skills"),
        "",
        "## Most Missed Question Types",
        "",
        *top_lines(missed_question_types, "Question Types"),
        "",
        "## Most Missed Standards",
        "",
        *top_lines(missed_standards, "Standards"),
        "",
        "## Words Missed 3+ Times",
        "",
        *threshold_lines(missed_words, "Words", 3),
        "",
        "## Suggested Review Targets",
        "",
        *suggestions,
        "",
        "## Recommended Next Actions",
        "",
        *next_actions,
        "",
        "## Gold Failures to Review",
        "",
        *gold_failures,
        "",
        "## Pilot Repetition Signals",
        "",
        "### Top Repeated Prompts",
        "",
        *pilot_prompt_lines,
        "",
        "### Top Repeated Target Words",
        "",
        *pilot_target_lines,
        "",
        "### Top Repeated Translation Meanings",
        "",
        *pilot_meaning_lines,
        "",
        "### Tense-Lane Overlap Targets",
        "",
        *pilot_tense_overlap_lineset,
        "",
        "### Shoresh Surface Pattern Concentration",
        "",
        *pilot_shoresh_surfaces,
        "",
        "### Dominant Correct Answer Concentration by Lane",
        "",
        *pilot_concentration,
        "",
        "### Reuse Triggered by Reteach vs Exhaustion",
        "",
        *pilot_reuse,
        "",
        "### Diversity Redirects",
        "",
        *pilot_redirects,
        "",
        "## Pre-Serve Validation Signals",
        "",
        "### Top Rejection Codes",
        "",
        *pilot_validation_rejections,
        "",
        "### Rejection Counts by Lane",
        "",
        *pilot_validation_by_lane,
        "",
        "### Served Questions Missing Validation Flag",
        "",
        *pilot_validation_bypass,
        "",
        "### Served Questions Outside Active Scope",
        "",
        *pilot_scope_safety,
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(build_report(), encoding="utf-8")


if __name__ == "__main__":
    main()
