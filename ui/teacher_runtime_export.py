from __future__ import annotations

import streamlit as st

from runtime.teacher_runtime_export import (
    build_teacher_runtime_export,
    build_teacher_runtime_export_json,
    render_teacher_runtime_export_markdown,
    write_teacher_runtime_export,
)


def _has_session_context(session_context):
    return bool(session_context) and any(
        (session_context or {}).get(key)
        for key in ("lesson_session_label", "mode_focus", "class_group_label", "teacher_notes")
    )


def render_teacher_runtime_export(session_context, exposure_summary):
    """Render a safe teacher-facing local export control in the sidebar."""

    with st.sidebar.expander("Teacher Runtime Report Export", expanded=False):
        st.markdown("**Save a local teacher runtime report**")
        st.caption(
            "Includes lesson/session setup, Runtime Exposure Center summary, cautious teacher interpretation, and safety/privacy notes."
        )
        st.caption("Local export only: no login, no database, no PII, and no raw JSONL logs.")

        export_data = build_teacher_runtime_export(session_context, exposure_summary)
        markdown_text = render_teacher_runtime_export_markdown(export_data)
        json_text = build_teacher_runtime_export_json(export_data)

        if not _has_session_context(session_context):
            st.warning("Lesson/session setup is empty or incomplete; the report will say that context is missing.")
        if not (exposure_summary or {}).get("summary_available"):
            st.info("No local attempt history is available yet; the report will preserve that missing-evidence note.")

        st.caption(
            "Included: repeated Hebrew targets, pasuk/skill concentration, skill/question-type concentration, fallback status, missing-data warnings, and privacy boundaries."
        )

        if st.button("Save teacher runtime report", type="secondary", use_container_width=True):
            status = write_teacher_runtime_export(export_data)
            if status.get("ok"):
                st.success("Teacher runtime report saved locally.")
                st.caption(f"Markdown: {status.get('markdown_path')}")
                st.caption(f"JSON: {status.get('json_path')}")
            else:
                st.warning("Could not save the teacher runtime report. Student flow can continue.")
                if status.get("error"):
                    st.caption(status["error"])

        st.download_button(
            "Download report Markdown",
            data=markdown_text,
            file_name="teacher_runtime_exposure_report.md",
            mime="text/markdown",
            use_container_width=True,
        )
        st.download_button(
            "Download report JSON",
            data=json_text,
            file_name="teacher_runtime_exposure_report.json",
            mime="application/json",
            use_container_width=True,
        )
