from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
VALIDATION_DIR = BASE_DIR / "data" / "validation"
INPUT_PATH = VALIDATION_DIR / "test_summary_input.json"
PYTEST_REPORT_PATH = VALIDATION_DIR / "pytest_report.json"
OUTPUT_PATH = VALIDATION_DIR / "test_summary.json"

GOLD_SHORESH_FILE = "tests/test_gold_shoresh_accuracy.py"
GOLD_AFFIX_FILE = "tests/test_gold_affix_handling.py"


def default_summary() -> dict:
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": "placeholder",
        "total": 0,
        "passed": 0,
        "failed": 0,
        "errors": 0,
        "gold_shoresh_status": "unknown",
        "gold_affix_status": "unknown",
    }


def load_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def load_manual_summary(path: Path) -> dict | None:
    data = load_json(path)
    if not data:
        return None

    summary = default_summary()
    summary["source"] = "manual_input"
    for key in (
        "total",
        "passed",
        "failed",
        "errors",
        "gold_shoresh_status",
        "gold_affix_status",
    ):
        if key in data:
            summary[key] = data[key]
    return summary


def suite_status_from_tests(tests: list[dict], filename: str) -> str:
    matching = [test for test in tests if str(test.get("nodeid", "")).startswith(filename)]
    if not matching:
        return "unknown"

    outcomes = {test.get("outcome", "unknown") for test in matching}
    if "failed" in outcomes:
        return "failed"
    if "error" in outcomes:
        return "error"
    if outcomes.issubset({"passed", "skipped"}):
        return "passed"
    return "unknown"


def load_pytest_summary(path: Path) -> dict | None:
    report = load_json(path)
    if not report:
        return None

    summary = default_summary()
    summary["source"] = "pytest_json_report"

    report_summary = report.get("summary", {}) if isinstance(report, dict) else {}
    tests = report.get("tests", []) if isinstance(report, dict) else []
    if not isinstance(tests, list):
        tests = []

    summary["total"] = report_summary.get("total", report_summary.get("collected", 0))
    summary["passed"] = report_summary.get("passed", 0)
    summary["failed"] = report_summary.get("failed", 0)
    summary["errors"] = report_summary.get("error", report_summary.get("errors", 0))
    summary["gold_shoresh_status"] = suite_status_from_tests(tests, GOLD_SHORESH_FILE)
    summary["gold_affix_status"] = suite_status_from_tests(tests, GOLD_AFFIX_FILE)
    return summary


def main() -> None:
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else INPUT_PATH
    summary = (
        load_pytest_summary(PYTEST_REPORT_PATH)
        or load_manual_summary(input_path)
        or default_summary()
    )
    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
