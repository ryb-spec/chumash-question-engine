from __future__ import annotations

import streamlit as st

from runtime.exposure_summary import (
    format_repeated_pasuk_skill_pairs,
    format_repeated_skill_types,
    format_repeated_targets,
    get_runtime_exposure_status_message,
)
from runtime.lesson_session_setup import lesson_session_summary_lines


def _yes_no(value):
    return "yes" if value else "no"


def _render_lines(lines):
    for line in lines:
        st.caption(f"- {line}")


def render_runtime_exposure_center(summary):
    """Render the teacher-facing Runtime Exposure Center in the sidebar."""

    summary = summary or {
        "summary_available": False,
        "warning_messages": ["Runtime exposure summary could not load."],
        "teacher_interpretation_messages": [
            "This visibility tool does not change scores or question selection."
        ],
    }

    with st.sidebar.expander("Runtime Exposure Center", expanded=False):
        st.markdown("**Status**")
        st.caption(
            "Repetition control: "
            + ("Active" if summary.get("repetition_control_active") else "Inactive")
        )
        st.caption(
            "Runtime Learning Intelligence: "
            + ("Enabled" if summary.get("runtime_learning_intelligence_enabled") else "Disabled")
        )
        st.caption("Data source: Local attempt history")
        st.caption("Privacy: No login, no database, no PII")

        st.markdown("**Lesson/session context**")
        for line in lesson_session_summary_lines(summary.get("teacher_lesson_session")):
            st.caption(f"- {line}")

        st.markdown("**Recent history**")
        st.caption(f"Recent attempts counted: {summary.get('recent_attempt_count', 0)}")
        files = {item.get("label"): item for item in summary.get("history_files", [])}
        st.caption(f"Attempt-log file present: {_yes_no((files.get('attempt_log') or {}).get('present'))}")
        st.caption(
            "Pilot-event log present: "
            + _yes_no((files.get("pilot_session_events") or {}).get("present"))
        )
        st.caption(f"Malformed/skipped log lines: {summary.get('skipped_or_malformed_count', 0)}")
        if summary.get("last_observed_attempt_timestamp"):
            st.caption(f"Last observed attempt: {summary['last_observed_attempt_timestamp']}")

        if not summary.get("summary_available"):
            st.info("No local attempt history found yet.")

        st.markdown("**Most repeated Hebrew targets**")
        _render_lines(format_repeated_targets(summary))

        st.markdown("**Most repeated pasuk + skill pairs**")
        _render_lines(format_repeated_pasuk_skill_pairs(summary))

        st.markdown("**Most repeated skills**")
        _render_lines(format_repeated_skill_types(summary))

        question_types = summary.get("repeated_question_types") or []
        if question_types:
            st.markdown("**Most repeated question types**")
            _render_lines(
                f"{item.get('question_type') or 'unknown'}: {item.get('count', 0)}"
                for item in question_types
            )

        st.markdown("**Scope/fallback status**")
        fallback_count = summary.get("fallback_count")
        fallback_status = summary.get("small_pool_fallback_status") or "unknown_not_determined"
        st.caption(f"Small-pool fallback: {fallback_status}")
        st.caption(f"Fallback count: {fallback_count if fallback_count is not None else 'unknown'}")
        if summary.get("fallback_targeted_test_still_needed"):
            st.warning("Small-pool fallback still needs focused confirmation.")

        for message in summary.get("warning_messages", []):
            st.warning(message)

        st.markdown("**Teacher interpretation**")
        st.caption(get_runtime_exposure_status_message(summary))
        for message in summary.get("teacher_interpretation_messages", []):
            st.caption(message)
