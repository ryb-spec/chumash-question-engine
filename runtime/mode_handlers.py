from html import escape

import streamlit as st

from runtime.presentation import QUESTION_TYPE_NAMES, skill_path_label
from runtime.question_flow import (
    build_followup_question,
    finalize_transition_debug,
    generate_mastery_question,
    generate_practice_question,
)
from runtime.runtime_support import (
    get_active_pasuk_ref,
    last_answer_was_correct,
    load_pasuk_flows,
    mixed_text_html,
    render_assessment_diagnostics,
)
from runtime.session_state import set_question, transition_to_question
from ui.render_question import render_enter_key_handler, render_question


def render_mastery_mode(progress):
    if st.session_state.current_question is None:
        try:
            set_question(
                finalize_transition_debug(
                    generate_mastery_question(progress),
                    "initial_load",
                )
            )
        except Exception as error:
            st.warning(f"No question is ready for this skill and pasuk yet: {error}")
            return

    question = st.session_state.current_question
    if question is None:
        st.warning("No mastery question is ready yet.")
        return

    adaptive_message = st.session_state.get("adaptive_status_message")
    adaptive_reason = st.session_state.get("adaptive_status_reason")
    adaptive_level = st.session_state.get("adaptive_status_level", "info")
    unlocked_message = st.session_state.get("unlocked_skill_message")
    fallback_message = st.session_state.get("feature_fallback_message")

    render_assessment_diagnostics(question, mode="Learn Mode")
    render_question(question, progress, f"mastery_{progress['current_skill']}")

    if not st.session_state.answered:
        if adaptive_message:
            if adaptive_level == "success":
                st.success(adaptive_message)
            elif adaptive_level == "warning":
                st.warning(adaptive_message)
            else:
                st.info(adaptive_message)
            if adaptive_reason:
                st.caption(f"Why this path: {adaptive_reason}.")

        if unlocked_message:
            st.success(unlocked_message)

        if fallback_message:
            st.caption(fallback_message)

    if st.session_state.answered:
        if last_answer_was_correct(question):
            if st.button("Next Question", type="primary", use_container_width=True, key="next_mastery"):
                try:
                    next_question = generate_mastery_question(progress)
                except Exception as error:
                    st.warning(f"No question is ready for this skill and pasuk yet: {error}")
                    return
                transition_to_question(
                    finalize_transition_debug(
                        next_question,
                        "next_question",
                        adaptive_reason,
                    )
                )
            render_enter_key_handler("enter_next_mastery", ["Next Question"])
        else:
            primary, secondary = st.columns([2, 1])
            with primary:
                if st.button("Try One Like This", type="primary", use_container_width=True, key="retry_mastery_like_this"):
                    followup = build_followup_question(progress, question)
                    if followup is None:
                        st.warning("No close follow-up is ready yet. Continuing with the normal path.")
                        followup = generate_mastery_question(progress)
                    transition_to_question(
                        finalize_transition_debug(
                            followup,
                            (followup.get("_debug_trace") or {}).get("transition_path", "follow-up"),
                            (followup.get("_debug_trace") or {}).get("transition_reason", ""),
                        )
                    )
            with secondary:
                if st.button("Continue", use_container_width=True, key="continue_mastery_after_error"):
                    try:
                        next_question = generate_mastery_question(progress)
                    except Exception as error:
                        st.warning(f"No question is ready for this skill and pasuk yet: {error}")
                        return
                    transition_to_question(
                        finalize_transition_debug(
                            next_question,
                            "retry_continue",
                            adaptive_reason,
                        )
                    )
            render_enter_key_handler("enter_retry_mastery", ["Try One Like This", "Continue"])

        if adaptive_message:
            st.caption(adaptive_message)
        if adaptive_reason:
            st.caption(f"Why this path: {adaptive_reason}.")
        if unlocked_message:
            st.caption(unlocked_message)
        if fallback_message:
            st.caption(fallback_message)


def render_skill_practice_mode(progress, skill):
    if st.session_state.current_question is None:
        try:
            set_question(
                finalize_transition_debug(
                    generate_practice_question(skill),
                    "initial_load",
                )
            )
        except Exception as error:
            st.warning(f"No question is ready for this skill and pasuk yet: {error}")
            return

    question = st.session_state.current_question
    if question is None:
        st.warning("No practice question is ready yet.")
        return

    fallback_message = st.session_state.get("feature_fallback_message")
    render_assessment_diagnostics(question, mode="Practice Mode")
    render_question(question, progress, f"practice_{skill}")
    if not st.session_state.answered and fallback_message:
        st.caption(fallback_message)

    if st.session_state.answered:
        if last_answer_was_correct(question):
            if st.button("Next Question", type="primary", use_container_width=True, key=f"next_practice_{skill}"):
                transition_to_question(
                    finalize_transition_debug(
                        generate_practice_question(skill, progress),
                        "next_question",
                    )
                )
            render_enter_key_handler(f"enter_next_practice_{skill}", ["Next Question"])
        else:
            primary, secondary = st.columns([2, 1])
            with primary:
                if st.button("Try One Like This", type="primary", use_container_width=True, key=f"retry_practice_like_this_{skill}"):
                    followup = build_followup_question(progress, question)
                    if followup is None:
                        followup = generate_practice_question(skill, progress)
                    transition_to_question(
                        finalize_transition_debug(
                            followup,
                            (followup.get("_debug_trace") or {}).get("transition_path", "follow-up"),
                            (followup.get("_debug_trace") or {}).get("transition_reason", ""),
                        )
                    )
            with secondary:
                if st.button("Continue", use_container_width=True, key=f"continue_practice_after_error_{skill}"):
                    transition_to_question(
                        finalize_transition_debug(
                            generate_practice_question(skill, progress),
                            "retry_continue",
                        )
                    )
            render_enter_key_handler(f"enter_retry_practice_{skill}", ["Try One Like This", "Continue"])

        if fallback_message:
            st.caption(fallback_message)


def render_flow_overview(flow, active_step):
    steps = flow.get("questions") or flow.get("steps", [])
    if not steps:
        return

    rows = []
    for index, step in enumerate(steps):
        status = "complete" if index < active_step else "active" if index == active_step else "upcoming"
        title = QUESTION_TYPE_NAMES.get(
            step.get("question_type"),
            skill_path_label(step.get("skill", f"Step {index + 1}")),
        )
        focus = step.get("selected_word") or step.get("word") or ""
        rows.append(
            f"""
            <div class="flow-row {status}">
                <div class="flow-index">{index + 1}</div>
                <div>
                    <strong>{escape(title)}</strong>
                    <span dir="rtl" lang="he">{mixed_text_html(focus)}</span>
                </div>
            </div>
            """
        )

    st.markdown(
        f"""
        <section class="flow-overview">
            <div class="section-heading">
                <span>Pasuk Flow</span>
                <small>{active_step + 1}/{len(steps)}</small>
            </div>
            <div class="flow-grid">{''.join(rows)}</div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_pasuk_flow(progress):
    flows = load_pasuk_flows()
    if not flows:
        st.warning(
            "No guided Pasuk practice is ready yet. Add a flow, then come back here to walk through it step by step."
        )
        return

    flow_labels = []
    for flow in flows:
        pasuk_ref = get_active_pasuk_ref(flow.get("pasuk", ""))
        flow_labels.append(f"{pasuk_ref} - Guided pasuk")
    selected_label = st.sidebar.selectbox("Pasuk", flow_labels)
    flow = flows[flow_labels.index(selected_label)]

    st.caption(f"Source: {flow.get('source', 'unknown')}")

    if st.session_state.flow_label != selected_label:
        st.session_state.flow_label = selected_label
        st.session_state.flow_step = 0
        st.session_state.answered = False
        st.session_state.selected_answer = None

    steps = flow.get("questions") or flow.get("steps", [])
    step_index = st.session_state.flow_step
    question = steps[step_index]

    render_assessment_diagnostics(question, flow, "Pasuk Flow")
    render_question(question, progress, f"flow_{step_index}", flow)
    with st.expander("Pasuk Flow Steps", expanded=False):
        render_flow_overview(flow, step_index)

    if st.session_state.answered:
        if step_index + 1 < len(steps):
            if st.button("Next Step", type="primary", use_container_width=True, key=f"next_flow_step_{step_index}"):
                st.session_state.flow_step += 1
                st.session_state.answered = False
                st.session_state.selected_answer = None
                st.rerun()
            render_enter_key_handler(f"enter_next_flow_{step_index}", ["Next Step"])
        else:
            st.success("Pasuk flow complete.")
            if st.button("Restart Flow", type="primary", use_container_width=True, key="restart_flow"):
                st.session_state.flow_step = 0
                st.session_state.answered = False
                st.session_state.selected_answer = None
                st.rerun()
            render_enter_key_handler("enter_restart_flow", ["Restart Flow"])
