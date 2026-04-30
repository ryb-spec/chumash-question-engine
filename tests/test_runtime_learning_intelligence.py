from __future__ import annotations

import json
from pathlib import Path

from runtime.attempt_history import load_attempt_history, read_jsonl_records
from runtime.question_identity import build_question_signatures
from runtime.scope_exhaustion import (
    build_exposure_index,
    history_weighting_enabled,
    rank_candidates_by_freshness,
    score_candidate_exposure,
)
from scripts import validate_runtime_learning_intelligence as validator


def test_attempt_history_reader_handles_missing_file(tmp_path):
    missing = tmp_path / "missing.jsonl"

    result = read_jsonl_records(missing)

    assert result["missing"] is True
    assert result["records"] == []
    assert result["malformed_count"] == 0


def test_attempt_history_reader_skips_malformed_jsonl(tmp_path):
    path = tmp_path / "attempts.jsonl"
    path.write_text(
        "\n".join(
            [
                "{bad json",
                json.dumps(
                    {
                        "timestamp_utc": "2026-04-30T00:00:00+00:00",
                        "selected_word": "ברא",
                        "skill": "translation",
                        "question_type": "translation",
                        "is_correct": True,
                    },
                    ensure_ascii=False,
                ),
            ]
        ),
        encoding="utf-8",
    )

    result = read_jsonl_records(path)

    assert result["malformed_count"] == 1
    assert len(result["records"]) == 1
    assert result["records"][0]["hebrew_target"] == "ברא"


def test_load_attempt_history_uses_local_files_without_pii(tmp_path):
    attempt_path = tmp_path / "attempt_log.jsonl"
    pilot_path = tmp_path / "pilot_session_events.jsonl"
    attempt_path.write_text(
        json.dumps({"selected_word": "ברא", "skill": "translation"}, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    pilot_path.write_text(
        json.dumps(
            {
                "event_type": "question_served",
                "question_log_id": "q1",
                "selected_word": "אור",
                "skill": "shoresh",
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    history = load_attempt_history(
        attempt_log_path=attempt_path,
        pilot_events_path=pilot_path,
    )

    assert history["record_count"] == 2
    assert history["source_counts"] == {"attempt_log": 1, "pilot_events": 1}
    assert all("student_name" not in record for record in history["records"])


def test_question_identity_signatures_are_stable():
    question = {
        "id": "q-1",
        "pasuk_ref": {"label": "Bereishis 1:1"},
        "selected_word": "ברא",
        "skill": "translation",
        "question_type": "translation",
        "question": "What does ברא mean?",
    }

    first = build_question_signatures(question)
    second = build_question_signatures(dict(question))

    assert first == second
    assert first["exact_question_signature"] == "q-1"
    assert first["target_signature"] == "ברא"


def test_repeated_exact_target_gets_higher_penalty():
    history = [
        {
            "question_id": "q-1",
            "hebrew_target": "ברא",
            "pasuk_ref": "Bereishis 1:1",
            "skill": "translation",
            "question_type": "translation",
            "prompt": "What does ברא mean?",
        }
    ]
    index = build_exposure_index(history)

    repeated = score_candidate_exposure(
        {
            "question_id": "q-1",
            "hebrew_target": "ברא",
            "pasuk_ref": "Bereishis 1:1",
            "skill": "translation",
            "question_type": "translation",
            "question": "What does ברא mean?",
        },
        index,
    )
    fresh = score_candidate_exposure(
        {
            "question_id": "q-2",
            "hebrew_target": "אור",
            "pasuk_ref": "Bereishis 1:3",
            "skill": "translation",
            "question_type": "translation",
        },
        index,
    )

    assert repeated["penalty"] > fresh["penalty"]
    assert "exact_recent_repeat" in repeated["reasons"]
    assert "repeated_hebrew_target" in repeated["reasons"]


def test_repeated_hebrew_target_is_downweighted():
    index = build_exposure_index(
        [
            {
                "hebrew_target": "ברא",
                "pasuk_ref": "Bereishis 1:1",
                "skill": "shoresh",
                "question_type": "shoresh",
            }
        ]
    )

    repeated = score_candidate_exposure(
        {
            "hebrew_target": "ברא",
            "pasuk_ref": "Bereishis 1:1",
            "skill": "translation",
            "question_type": "translation",
        },
        index,
    )

    assert repeated["penalty"] >= 40
    assert "repeated_hebrew_target" in repeated["reasons"]


def test_fallback_still_returns_candidates_when_all_overexposed():
    candidates = [
        {"hebrew_target": "ברא", "skill": "translation", "question_type": "translation"},
    ]
    index = build_exposure_index(
        [{"hebrew_target": "ברא", "skill": "translation", "question_type": "translation"}]
    )

    ranked = rank_candidates_by_freshness(candidates, index)

    assert [item["candidate"] for item in ranked] == candidates
    assert "fallback_scope_small" in ranked[0]["explanation"]["reasons"]


def test_disable_toggle_turns_weighting_off(monkeypatch):
    monkeypatch.setenv("CHUMASH_DISABLE_HISTORY_WEIGHTING", "1")
    index = build_exposure_index(
        [{"hebrew_target": "ברא", "skill": "translation", "question_type": "translation"}]
    )

    score = score_candidate_exposure(
        {"hebrew_target": "ברא", "skill": "translation", "question_type": "translation"},
        index,
    )

    assert history_weighting_enabled() is False
    assert score["penalty"] == 0
    assert score["reasons"] == ["history_weighting_disabled"]


def test_validator_passes():
    assert validator.validate() == []
