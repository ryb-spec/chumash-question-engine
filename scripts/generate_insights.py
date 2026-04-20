from __future__ import annotations

from collections import Counter
from pathlib import Path

from runtime.pilot_logging import build_pilot_export, load_attempts

BASE_DIR = Path(__file__).resolve().parents[1]
ATTEMPT_LOG_PATH = BASE_DIR / "data" / "attempt_log.jsonl"
OUTPUT_PATH = BASE_DIR / "data" / "validation" / "nightly_insights.md"


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


def build_report() -> str:
    if not ATTEMPT_LOG_PATH.exists():
        return (
            "# Nightly Insights\n\n"
            "No attempt data is available yet.\n"
        )

    attempts = load_attempts(ATTEMPT_LOG_PATH)
    pilot_export = build_pilot_export(attempts)
    pilot_summary = pilot_export["summary"]
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

    lines = [
        "# Nightly Insights",
        "",
        "## Summary",
        "",
        f"- Served questions: {pilot_summary['served']}",
        f"- Answered questions: {pilot_summary['answered']}",
        f"- Total attempts: {len(attempts)}",
        f"- Total incorrect: {len(incorrect_attempts)}",
        f"- In active parsed dataset: {pilot_summary['in_active_scope_served']}",
        f"- Out of active parsed dataset: {pilot_summary['out_of_scope_served']}",
        "",
        "## Pilot Consistency Checks",
        "",
        f"- Served equals question-type totals: {pilot_export['consistency']['served_equals_question_type_total']}",
        f"- Served equals question-family totals: {pilot_export['consistency']['served_equals_question_family_total']}",
        f"- Answered ≤ served: {pilot_export['consistency']['answered_lte_served']}",
        f"- Correct ≤ answered: {pilot_export['consistency']['correct_lte_answered']}",
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
    ]
    return "\n".join(lines)


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(build_report(), encoding="utf-8")


if __name__ == "__main__":
    main()
