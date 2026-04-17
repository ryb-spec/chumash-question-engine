from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
VALIDATION_DIR = BASE_DIR / "data" / "validation"
TEST_SUMMARY_PATH = VALIDATION_DIR / "test_summary.json"
NIGHTLY_INSIGHTS_PATH = VALIDATION_DIR / "nightly_insights.md"
OUTPUT_PATH = VALIDATION_DIR / "daily_review.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_test_summary() -> dict | None:
    if not TEST_SUMMARY_PATH.exists():
        return None
    try:
        return json.loads(TEST_SUMMARY_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def load_nightly_insights() -> str | None:
    if not NIGHTLY_INSIGHTS_PATH.exists():
        return None
    try:
        text = NIGHTLY_INSIGHTS_PATH.read_text(encoding="utf-8")
    except OSError:
        return None
    return text.strip() or None


def strip_top_heading(markdown_text: str) -> str:
    lines = markdown_text.splitlines()
    if lines and lines[0].strip() == "# Nightly Insights":
        lines = lines[1:]
        while lines and not lines[0].strip():
            lines = lines[1:]
    return "\n".join(lines).strip()


def remove_sections(markdown_text: str, headings_to_remove: set[str]) -> str:
    kept_lines = []
    skip_section = False

    for line in markdown_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            skip_section = stripped in headings_to_remove
            if skip_section:
                continue
        if not skip_section:
            kept_lines.append(line)

    return "\n".join(kept_lines).strip()


def extract_bullets_from_section(markdown_text: str, heading: str) -> list[str]:
    bullets = []
    in_section = False
    for line in markdown_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            in_section = stripped == heading
            continue
        if in_section and stripped.startswith("- "):
            bullets.append(stripped)
        elif in_section and stripped:
            continue
    return bullets


def build_test_status_lines(summary: dict | None) -> list[str]:
    if not summary:
        return ["No test summary available yet."]
    return [
        f"- Total tests: {summary.get('total', 0)}",
        f"- Passed: {summary.get('passed', 0)}",
        f"- Failed: {summary.get('failed', 0)}",
        f"- Errors: {summary.get('errors', 0)}",
    ]


def build_gold_status_lines(summary: dict | None) -> list[str]:
    if not summary:
        return ["No gold-suite summary available yet."]

    shoresh = summary.get("gold_shoresh_status")
    affix = summary.get("gold_affix_status")
    if shoresh is None and affix is None:
        return ["No gold-suite summary available yet."]

    return [
        f"- Gold shoresh suite: {shoresh or 'unknown'}",
        f"- Gold affix suite: {affix or 'unknown'}",
    ]


def build_recommended_actions(summary: dict | None, nightly_insights: str | None) -> list[str]:
    actions = []

    if summary:
        if summary.get("failed", 0) or summary.get("errors", 0):
            actions.append("- Investigate any failing gold suites.")
        if summary.get("gold_shoresh_status") not in {"passed", "unknown", None}:
            actions.append("- Investigate gold shoresh coverage gaps.")
        if summary.get("gold_affix_status") not in {"passed", "unknown", None}:
            actions.append("- Investigate gold affix handling gaps.")

    if nightly_insights:
        for bullet in extract_bullets_from_section(nightly_insights, "## Suggested Review Targets"):
            actions.append(bullet)
        for bullet in extract_bullets_from_section(nightly_insights, "## Recommended Next Actions"):
            actions.append(bullet)

    if not actions:
        actions.append("- No clear next actions yet.")

    deduped = []
    seen = set()
    for action in actions:
        if action in seen:
            continue
        seen.add(action)
        deduped.append(action)
    return deduped


def build_review_prompts() -> list[str]:
    return [
        '- "Review this daily report and suggest the next 5 highest-impact parser improvements."',
        '- "Which skills need reteach based on this report?"',
        '- "Suggest 10 new gold-standard Hebrew cases based on the repeated trouble words."',
    ]


def build_document() -> str:
    summary = load_test_summary()
    nightly_insights = load_nightly_insights()

    lines = [
        "# Chumash Engine Daily Review",
        "",
        f"- Generated at (UTC): {utc_now()}",
        "",
        "## Test Status",
        "",
        *build_test_status_lines(summary),
        "",
        "## Gold Accuracy Status",
        "",
        *build_gold_status_lines(summary),
        "",
        "## Nightly Insights",
        "",
    ]

    if nightly_insights:
        nightly_body = strip_top_heading(nightly_insights)
        nightly_body = remove_sections(
            nightly_body,
            {"## Suggested Review Targets", "## Recommended Next Actions"},
        )
        lines.extend([nightly_body, ""])
    else:
        lines.extend(["No nightly insights available yet.", ""])

    lines.extend(
        [
            "## Recommended Next Actions",
            "",
            *build_recommended_actions(summary, nightly_insights),
            "",
            "## Review With ChatGPT",
            "",
            *build_review_prompts(),
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(build_document(), encoding="utf-8")


if __name__ == "__main__":
    main()
