from __future__ import annotations

import streamlit as st

from runtime.lesson_session_setup import (
    DEFAULT_MODE_FOCUS,
    DEFAULT_PLANNED_LESSON_FOCUS,
    get_lesson_session_metadata,
    lesson_session_summary_lines,
    reset_lesson_session_metadata,
    update_lesson_session_metadata,
)

PLANNED_LESSON_FOCUS_OPTIONS = [
    "Current app mode",
    "General review",
    "Full Passuk view",
    "Skill practice",
    "Pasuk Flow",
    "Pilot observation",
]
MODE_FOCUS_OPTIONS = PLANNED_LESSON_FOCUS_OPTIONS


def render_teacher_lesson_session_setup():
    """Render a local teacher lesson/session setup panel.

    The panel stores metadata in Streamlit session state only and does not
    change runtime scope, question selection, scoring, mastery, or content.
    """

    metadata = get_lesson_session_metadata(st.session_state)
    with st.sidebar.expander("Teacher Lesson / Session Setup", expanded=False):
        st.caption("Local teacher context only. No login, no database, no PII.")
        lesson_label = st.text_input(
            "Lesson/session label",
            value=metadata.get("lesson_label", ""),
            max_chars=80,
            help="Example: Perek 3 review, shoresh warmup, or Thursday pilot run.",
        )
        current_focus = (
            metadata.get("planned_lesson_focus")
            or metadata.get("mode_focus")
            or DEFAULT_PLANNED_LESSON_FOCUS
        )
        focus_index = (
            PLANNED_LESSON_FOCUS_OPTIONS.index(current_focus)
            if current_focus in PLANNED_LESSON_FOCUS_OPTIONS
            else 0
        )
        planned_lesson_focus = st.selectbox(
            "Planned lesson focus",
            PLANNED_LESSON_FOCUS_OPTIONS,
            index=focus_index,
            help="This is a teacher/report label only. It does not change the student question mode.",
        )
        st.caption("Planned lesson focus is for teacher reports only; it does not change the student question mode.")
        class_group_label = st.text_input(
            "Class period / group label (optional)",
            value=metadata.get("class_group_label") or metadata.get("class_period_label", ""),
            max_chars=60,
        )
        teacher_notes = st.text_area(
            "Teacher notes (local, optional)",
            value=metadata.get("teacher_notes", ""),
            max_chars=240,
            height=80,
        )
        left, right = st.columns(2)
        with left:
            if st.button("Save session setup", use_container_width=True):
                metadata = update_lesson_session_metadata(
                    st.session_state,
                    lesson_label=lesson_label,
                    mode_focus=planned_lesson_focus,
                    planned_lesson_focus=planned_lesson_focus,
                    class_period_label=class_group_label,
                    class_group_label=class_group_label,
                    teacher_notes=teacher_notes,
                )
                st.success("Session setup saved locally.")
        with right:
            if st.button("Clear setup", use_container_width=True):
                metadata = reset_lesson_session_metadata(st.session_state)
                st.info("Session setup cleared.")

        st.markdown("**Current session context**")
        for line in lesson_session_summary_lines(metadata):
            st.caption(f"- {line}")
        st.caption(
            "This context does not change scores, mastery, active scope, student question mode, or question selection."
        )
    return metadata
