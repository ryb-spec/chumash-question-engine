from __future__ import annotations

import streamlit as st

from runtime.teacher_runtime_export import (
    build_session_bounded_exposure_summary,
    build_teacher_runtime_export,
    build_teacher_runtime_export_json,
    render_teacher_runtime_export_markdown,
    write_teacher_runtime_export,
)

SCOPE_OPTIONS = [
    ("Current session only (recommended)", "current_pilot_session"),
    ("Since teacher setup was saved", "teacher_setup_window"),
    ("Recent local history", "recent_local_history"),
]


def _has_session_context(session_context):
    return bool(session_context) and any(
        (session_context or {}).get(key)
        for key in (
            "lesson_session_label",
            "lesson_label",
            "planned_lesson_focus",
            "mode_focus",
            "class_group_label",
            "class_period_label",
            "teacher_notes",
        )
    )


def _default_scope_index(session_context, pilot_session_id):
    if pilot_session_id:
        return 0
    if (session_context or {}).get("saved_at") or (session_context or {}).get("updated_at_utc"):
        return 1
    return 2


def _build_export_snapshot(session_context, requested_scope, pilot_session_id, fallback_count):
    scoped_summary, export_scope = build_session_bounded_exposure_summary(
        session_context,
        requested_scope=requested_scope,
        pilot_session_id=pilot_session_id,
        fallback_count=fallback_count,
    )
    return build_teacher_runtime_export(
        session_context,
        scoped_summary,
        export_scope=export_scope,
        requested_scope=requested_scope,
        pilot_session_id=pilot_session_id,
    )


def render_teacher_runtime_export(
    session_context,
    exposure_summary=None,
    *,
    pilot_session_id=None,
    fallback_count=None,
):
    """Render a safe teacher-facing local export control in the sidebar."""

    with st.sidebar.expander("Teacher Runtime Report Export", expanded=False):
        st.markdown("**Save a local teacher runtime report**")
        st.caption(
            "Includes lesson/session setup, Runtime Exposure Center summary, cautious teacher interpretation, and safety/privacy notes."
        )
        st.caption("Local export only: no login, no database, no PII, and no raw JSONL logs.")

        scope_labels = [label for label, _value in SCOPE_OPTIONS]
        default_index = _default_scope_index(session_context, pilot_session_id)
        selected_scope_label = st.selectbox(
            "Report scope",
            scope_labels,
            index=default_index,
            help=(
                "Current session only is best for teacher review. Recent local history may include prior testing "
                "sessions and should be treated as diagnostic only."
            ),
        )
        requested_scope = dict(SCOPE_OPTIONS)[selected_scope_label]
        st.caption(
            "Report scope controls only this teacher export. It does not change student question mode, scoring, "
            "active scope, or question selection."
        )

        snapshot_key = "teacher_runtime_export_snapshot"
        scope_key = "teacher_runtime_export_snapshot_scope"
        if st.button("Build/refresh report snapshot", type="secondary", use_container_width=True):
            st.session_state[snapshot_key] = _build_export_snapshot(
                session_context,
                requested_scope,
                pilot_session_id,
                fallback_count,
            )
            st.session_state[scope_key] = requested_scope
            st.success("Teacher runtime report snapshot prepared.")

        export_data = st.session_state.get(snapshot_key)
        if not export_data or st.session_state.get(scope_key) != requested_scope:
            export_data = _build_export_snapshot(session_context, requested_scope, pilot_session_id, fallback_count)
            st.session_state[snapshot_key] = export_data
            st.session_state[scope_key] = requested_scope

        export_scope = export_data.get("export_scope") or {}
        scoped_exposure = export_data.get("exposure_summary") or {}
        markdown_text = render_teacher_runtime_export_markdown(export_data)
        json_text = build_teacher_runtime_export_json(export_data)

        if not _has_session_context(session_context):
            st.warning("Lesson/session setup is empty or incomplete; the report will say that context is missing.")
        if not scoped_exposure.get("summary_available"):
            st.info("No local attempt history is available yet; the report will preserve that missing-evidence note.")

        st.caption(
            "Included: repeated Hebrew targets, pasuk/skill concentration, skill/question-type concentration, fallback status, missing-data warnings, and privacy boundaries."
        )
        st.markdown("**Scope preview**")
        st.caption(f"Scope: {export_scope.get('scope_label') or 'unknown'}")
        st.caption(f"Records in scope: {export_scope.get('records_in_scope', 0)} of {export_scope.get('records_considered', 0)} considered")
        st.caption(f"Current-session bounded: {str(bool(export_scope.get('current_session_bounded'))).lower()}")
        st.caption(f"Fallback/scope-small status: {scoped_exposure.get('small_pool_fallback_status') or 'unknown_not_determined'}")
        st.caption(f"Malformed/skipped log lines: {scoped_exposure.get('malformed_count', scoped_exposure.get('skipped_or_malformed_count', 0))}")
        if export_scope.get("scope_warning"):
            st.warning(export_scope["scope_warning"])

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
