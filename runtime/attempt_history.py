"""Local attempt-history reader for Runtime Learning Intelligence V1."""

from __future__ import annotations

import json
import os
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ATTEMPT_LOG_PATH = REPO_ROOT / "data" / "attempt_log.jsonl"
DEFAULT_PILOT_EVENTS_PATH = REPO_ROOT / "data" / "pilot" / "pilot_session_events.jsonl"
SERVE_OR_ANSWER_EVENTS = {"question_served", "question_answered"}


def _pasuk_ref_label(value):
    if isinstance(value, dict):
        return value.get("label") or " ".join(
            str(value.get(key))
            for key in ("sefer", "perek", "pasuk")
            if value.get(key) not in (None, "")
        )
    return value


def normalize_attempt_record(record, *, source_file=""):
    record = record or {}
    return {
        "timestamp": record.get("timestamp_utc") or record.get("timestamp") or record.get("time"),
        "session_id": record.get("session_id"),
        "mode": record.get("mode") or record.get("practice_type"),
        "question_id": record.get("question_id") or record.get("question_log_id") or record.get("id"),
        "pasuk_ref": _pasuk_ref_label(record.get("pasuk_ref") or record.get("ref")),
        "hebrew_target": (
            record.get("hebrew_target")
            or record.get("selected_word")
            or record.get("target")
            or record.get("word")
        ),
        "skill": record.get("skill") or record.get("canonical_skill_id") or record.get("standard"),
        "question_type": record.get("question_type"),
        "answer_correct": (
            record.get("answer_correct")
            if "answer_correct" in record
            else record.get("is_correct")
        ),
        "prompt": record.get("question") or record.get("question_text") or record.get("prompt"),
        "source_file": source_file,
    }


def read_jsonl_records(path, *, max_records=None, event_types=None):
    path = Path(path)
    result = {
        "records": [],
        "malformed_count": 0,
        "missing": False,
        "path": str(path),
    }
    if not path.exists():
        result["missing"] = True
        return result

    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            text = line.strip()
            if not text:
                continue
            try:
                record = json.loads(text)
            except json.JSONDecodeError:
                result["malformed_count"] += 1
                continue
            if event_types and record.get("event_type") not in event_types:
                continue
            result["records"].append(normalize_attempt_record(record, source_file=str(path)))

    if max_records is not None and max_records >= 0:
        result["records"] = result["records"][-max_records:]
    return result


def load_attempt_history(
    *,
    attempt_log_path=None,
    pilot_events_path=None,
    max_records=500,
):
    attempt_path = Path(
        attempt_log_path or os.environ.get("CHUMASH_ATTEMPT_LOG_PATH") or DEFAULT_ATTEMPT_LOG_PATH
    )
    pilot_path = Path(
        pilot_events_path or os.environ.get("CHUMASH_PILOT_EVENT_LOG_PATH") or DEFAULT_PILOT_EVENTS_PATH
    )
    attempt_result = read_jsonl_records(attempt_path, max_records=max_records)
    pilot_result = read_jsonl_records(
        pilot_path,
        max_records=max_records,
        event_types=SERVE_OR_ANSWER_EVENTS,
    )
    records = [*attempt_result["records"], *pilot_result["records"]]
    records = records[-max_records:] if max_records is not None and max_records >= 0 else records
    used = []
    missing = []
    for result in (attempt_result, pilot_result):
        if result["missing"]:
            missing.append(result["path"])
        elif result["records"]:
            used.append(result["path"])

    return {
        "records": records,
        "record_count": len(records),
        "malformed_count": attempt_result["malformed_count"] + pilot_result["malformed_count"],
        "missing_files": missing,
        "history_files_used": used,
        "source_counts": {
            "attempt_log": len(attempt_result["records"]),
            "pilot_events": len(pilot_result["records"]),
        },
    }
