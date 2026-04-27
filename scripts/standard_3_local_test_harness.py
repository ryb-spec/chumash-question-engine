from __future__ import annotations

import argparse
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from runtime.standard_3_test_mode_loader import (  # noqa: E402
    EXPECTED_RECORD_COUNT,
    TEST_MODE_ENV_VAR,
    load_standard_3_test_mode_records,
    standard_3_test_mode_enabled,
)


REQUIRED_OUTPUT_FIELDS = (
    "reviewed_id",
    "source_record_id",
    "question",
    "correct_answer",
    "skill",
    "question_type",
    "mode",
    "runtime_status",
    "student_facing_status",
    "test_mode_only",
)

BOUNDARY_LINES = (
    "Teacher/admin review only.",
    "Runtime activation: blocked.",
    "Student-facing use: blocked.",
    "Active scope: untouched.",
    "Staged reviewed questions: untouched.",
)


class Standard3LocalHarnessError(RuntimeError):
    """Raised when the local Standard 3 harness cannot safely run."""


def _configure_console_encoding() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")


def _require_enabled(env: Mapping[str, str] | None = None) -> None:
    if not standard_3_test_mode_enabled(env):
        raise Standard3LocalHarnessError(
            f"{TEST_MODE_ENV_VAR} must be explicitly enabled before running this local review harness."
        )


def load_harness_records(env: Mapping[str, str] | None = None) -> list[dict]:
    _require_enabled(env)
    records = load_standard_3_test_mode_records(env=env)
    if len(records) != EXPECTED_RECORD_COUNT:
        raise Standard3LocalHarnessError(
            f"Expected {EXPECTED_RECORD_COUNT} Standard 3 test-mode records, found {len(records)}."
        )
    return records


def _format_field(name: str, value: object) -> str:
    return f"{name}: {value}"


def render_summary(records: Sequence[dict]) -> str:
    lines = [
        "Zekelman Standard 3 MVP Local Test Harness Summary",
        *BOUNDARY_LINES,
        f"Record count: {len(records)}",
        "",
    ]
    for index, record in enumerate(records, start=1):
        lines.append(f"Record {index}/{len(records)}")
        for field in REQUIRED_OUTPUT_FIELDS:
            lines.append(_format_field(field, record.get(field)))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_markdown_report(records: Sequence[dict]) -> str:
    lines = [
        "# Zekelman Standard 3 MVP Local Test Harness Review Report",
        "",
        "Teacher/admin review only.",
        "",
        "- Runtime activation: blocked",
        "- Student-facing use: blocked",
        "- Active scope: untouched",
        "- Staged reviewed questions: untouched",
        "- Current artifact: local review-only harness output",
        "",
        f"Record count: {len(records)}",
        "",
    ]
    for index, record in enumerate(records, start=1):
        lines.extend(
            [
                f"## Record {index}: `{record.get('reviewed_id')}`",
                "",
                f"- Source record ID: `{record.get('source_record_id')}`",
                f"- Question: {record.get('question')}",
                f"- Correct answer: {record.get('correct_answer')}",
                f"- Skill: `{record.get('skill')}`",
                f"- Question type: `{record.get('question_type')}`",
                f"- Mode: `{record.get('mode')}`",
                f"- Runtime status: `{record.get('runtime_status')}`",
                f"- Student-facing status: `{record.get('student_facing_status')}`",
                f"- Test-mode only: `{record.get('test_mode_only')}`",
                "",
                "Teacher/admin notes:",
                "",
                "",
            ]
        )
    lines.extend(
        [
            "## Final Status",
            "",
            "- Runtime activation: blocked",
            "- Student-facing use: blocked",
            "- Active scope: untouched",
            "- Staged reviewed questions: untouched",
            "- Question-ready status: not granted",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def write_markdown_report(records: Sequence[dict], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown_report(records), encoding="utf-8")
    return path


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Local teacher/admin-only review harness for Standard 3 MVP test-mode records."
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print the teacher/admin review-only summary to stdout.",
    )
    parser.add_argument(
        "--write-report",
        metavar="PATH",
        help="Write a teacher/admin review-only markdown report to PATH.",
    )
    return parser


def main(argv: Sequence[str] | None = None, env: Mapping[str, str] | None = None) -> int:
    _configure_console_encoding()
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    should_print_summary = args.summary or not args.write_report

    try:
        records = load_harness_records(env=env)
    except Standard3LocalHarnessError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if should_print_summary:
        print(render_summary(records), end="")
    if args.write_report:
        path = write_markdown_report(records, args.write_report)
        print(f"Wrote teacher/admin review-only report: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
