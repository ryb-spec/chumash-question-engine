from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def isolate_runtime_logs(tmp_path, monkeypatch):
    """Keep tests from mutating tracked runtime log files in data/."""

    attempt_log_path = tmp_path / "attempt_log.jsonl"
    pilot_log_path = tmp_path / "pilot_session_events.jsonl"

    monkeypatch.setenv("CHUMASH_PILOT_EVENT_LOG_PATH", str(pilot_log_path))

    import runtime.pilot_logging as pilot_logging
    import runtime.runtime_support as runtime_support
    import streamlit_app

    monkeypatch.setattr(streamlit_app, "ATTEMPT_LOG_PATH", attempt_log_path, raising=False)
    monkeypatch.setattr(runtime_support, "ATTEMPT_LOG_PATH", attempt_log_path, raising=False)
    monkeypatch.setattr(
        pilot_logging,
        "DEFAULT_PILOT_EVENT_LOG_PATH",
        pilot_log_path,
        raising=False,
    )
    monkeypatch.setattr(
        pilot_logging,
        "PILOT_EVENT_LOG_PATH",
        pilot_log_path,
        raising=False,
    )
