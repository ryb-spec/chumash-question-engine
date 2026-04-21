import json
from html import escape

import streamlit as st
import streamlit.components.v1 as components

from runtime.presentation import QUESTION_TYPE_NAMES, skill_path_label
from runtime.question_flow import (
    build_followup_question,
    finalize_transition_debug,
    generate_mastery_question,
    generate_practice_question,
    validate_question_for_serve,
)
from runtime.runtime_support import (
    get_active_pasuk_ref,
    last_answer_was_correct,
    load_pasuk_flows,
    mixed_text_html,
    render_assessment_diagnostics,
)
from runtime.session_state import (
    is_tense_family_skill,
    schedule_question_arrival,
    set_question,
    transition_to_question,
)
from ui.render_question import render_enter_key_handler, render_question


def queue_post_answer_action(action_name):
    if st.session_state.get("post_answer_action_pending"):
        return
    st.session_state.post_answer_action_pending = action_name
    st.rerun()


def render_post_answer_action_bar(note_text="Ready for the next question?"):
    token = st.session_state.get("current_post_answer_visibility_token", "") or "static"
    wrapper_id = f"post-answer-action-{token}"
    st.markdown(
        f"""
        <div class="post-answer-action-sentinel"></div>
        <section
            id="{wrapper_id}"
            class="post-answer-action-shell post-answer-action-target"
            data-post-answer-token="{escape(token)}"
            tabindex="-1"
        >
            <div class="section-label">Continue</div>
            <div class="post-answer-action-note">{escape(note_text)}</div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    return wrapper_id


def render_post_answer_action_visibility(wrapper_id, button_labels):
    token = st.session_state.get("current_post_answer_visibility_token", "")
    if not token or not st.session_state.get("answered"):
        return

    should_scroll = st.session_state.get("scroll_to_post_answer_action_on_render", False)
    last_token = st.session_state.get("last_post_answer_scroll_token", "")
    if not should_scroll and last_token == token:
        return

    st.session_state.last_post_answer_scroll_token = token
    st.session_state.scroll_to_post_answer_action_on_render = False
    labels_json = json.dumps(list(button_labels or []))
    script = """
        <script>
        (function() {{
            const rootWindow = window.parent;
            const rootDocument = rootWindow.document;
            const token = {token};
            const wrapperId = {wrapper_id};
            const buttonLabels = {button_labels};
            const maxAttempts = 90;
            let attempts = 0;

            const isScrollable = (node) => {{
                if (!node || !node.tagName) return false;
                const style = rootWindow.getComputedStyle(node);
                return ['auto', 'scroll', 'overlay'].includes(style.overflowY)
                    && node.scrollHeight > node.clientHeight + 4;
            }};

            const preferredMainContainer = () => {{
                const main = rootDocument.querySelector('[data-testid="stMain"]');
                if (main && main.scrollHeight > main.clientHeight + 4) {{
                    return main;
                }}
                return null;
            }};

            const findScrollContainer = (node) => {{
                const main = preferredMainContainer();
                if (main) {{
                    return main;
                }}
                let current = node ? node.parentElement : null;
                while (current && current !== rootDocument.body) {{
                    if (isScrollable(current)) {{
                        return current;
                    }}
                    current = current.parentElement;
                }}
                return rootDocument.scrollingElement || rootDocument.documentElement || rootDocument.body;
            }};

            const topOffset = () => {{
                const header = rootDocument.querySelector('header[data-testid="stHeader"]');
                const headerHeight = header ? header.getBoundingClientRect().height : 0;
                return Math.max(20, headerHeight + 12);
            }};

            const bottomPad = () => 24;

            const firstMatchingButton = (wrapper) => {{
                const scope = wrapper.closest('[data-testid="stVerticalBlock"]') || wrapper.parentElement || rootDocument.body;
                const buttons = Array.from(scope.querySelectorAll('button')).filter((button) => {{
                    if (!button || button.offsetParent === null) return false;
                    const relation = wrapper.compareDocumentPosition(button);
                    return Boolean(relation & Node.DOCUMENT_POSITION_FOLLOWING);
                }});
                for (const label of buttonLabels) {{
                    const exact = buttons.find((button) => button.innerText.trim() === label);
                    if (exact) return exact;
                }}
                for (const label of buttonLabels) {{
                    const loose = buttons.find((button) => button.innerText.trim().startsWith(label));
                    if (loose) return loose;
                }}
                return buttons[0] || null;
            }};

            const scrollContainerTo = (scrollContainer, top) => {{
                if (
                    scrollContainer === rootDocument.body
                    || scrollContainer === rootDocument.documentElement
                    || scrollContainer === rootDocument.scrollingElement
                ) {{
                    rootWindow.scrollTo({{ top, behavior: 'auto' }});
                    return;
                }}
                scrollContainer.scrollTo({{ top, behavior: 'auto' }});
            }};

            const currentScrollTop = (scrollContainer) => {{
                if (
                    scrollContainer === rootDocument.body
                    || scrollContainer === rootDocument.documentElement
                    || scrollContainer === rootDocument.scrollingElement
                ) {{
                    return rootWindow.pageYOffset || rootDocument.documentElement.scrollTop || 0;
                }}
                return scrollContainer.scrollTop || 0;
            }};

            const makeVisible = (wrapper, button) => {{
                const scrollContainer = findScrollContainer(wrapper);
                const offset = topOffset();
                const wrapperRect = wrapper.getBoundingClientRect();
                const scrollTop = currentScrollTop(scrollContainer);
                const initialTop = Math.max(wrapperRect.top + scrollTop - offset, 0);
                scrollContainerTo(scrollContainer, initialTop);

                rootWindow.requestAnimationFrame(() => {{
                    const buttonRect = (button || wrapper).getBoundingClientRect();
                    const viewportHeight = rootWindow.innerHeight || rootDocument.documentElement.clientHeight || 0;
                    const maxBottom = viewportHeight - bottomPad();
                    const minTop = offset;
                    let adjustment = 0;
                    if (buttonRect.bottom > maxBottom) {{
                        adjustment += buttonRect.bottom - maxBottom;
                    }}
                    if (buttonRect.top < minTop) {{
                        adjustment -= (minTop - buttonRect.top);
                    }}
                    if (adjustment) {{
                        scrollContainerTo(scrollContainer, Math.max(currentScrollTop(scrollContainer) + adjustment, 0));
                    }}
                }});
            }};

            const focusTarget = (target) => {{
                if (!target) return;
                try {{
                    target.focus({{ preventScroll: true }});
                }} catch (error) {{
                    target.focus();
                }}
            }};

            const isReady = (button) => {{
                if (!button) return false;
                const rect = button.getBoundingClientRect();
                const viewportHeight = rootWindow.innerHeight || rootDocument.documentElement.clientHeight || 0;
                return rect.top >= topOffset() - 8 && rect.bottom <= viewportHeight - bottomPad() + 8;
            }};

            const retry = () => {{
                if (attempts >= maxAttempts) {{
                    rootWindow.__assessmentHandledPostAnswerToken = token;
                    rootWindow.__assessmentPendingPostAnswerToken = '';
                    return;
                }}
                rootWindow.requestAnimationFrame(() => rootWindow.setTimeout(findAndScroll, 35));
            }};

            const findAndScroll = () => {{
                if (
                    rootWindow.__assessmentPendingPostAnswerToken
                    && rootWindow.__assessmentPendingPostAnswerToken !== token
                ) {{
                    return;
                }}
                const wrapper = rootDocument.getElementById(wrapperId);
                if (!wrapper) {{
                    attempts += 1;
                    retry();
                    return;
                }}
                const button = firstMatchingButton(wrapper);
                if (!button) {{
                    attempts += 1;
                    retry();
                    return;
                }}
                if (rootWindow.__assessmentHandledPostAnswerToken === token && isReady(button)) {{
                    return;
                }}

                rootWindow.__assessmentPendingPostAnswerToken = token;
                makeVisible(wrapper, button);
                rootWindow.requestAnimationFrame(() => {{
                    focusTarget(button);
                    if (isReady(button)) {{
                        rootWindow.__assessmentHandledPostAnswerToken = token;
                        rootWindow.__assessmentPendingPostAnswerToken = '';
                        return;
                    }}
                    attempts += 1;
                    retry();
                }});
            }};

            findAndScroll();
        }})();
        </script>
    """.format(
        token=json.dumps(token),
        wrapper_id=json.dumps(wrapper_id),
        button_labels=labels_json,
    )
    components.html(script, height=0, width=0)


def run_pending_post_answer_action(action_name, action_callable, loading_key):
    if st.session_state.get("post_answer_action_pending") != action_name:
        return False

    render_post_answer_action_bar("Loading the next question now.")
    st.button(
        "Loading next question...",
        key=loading_key,
        type="primary",
        disabled=True,
        use_container_width=True,
    )
    with st.spinner("Loading next question..."):
        st.session_state.post_answer_action_pending = ""
        try:
            action_callable()
        except Exception as error:
            st.warning(f"No question is ready for this skill and pasuk yet: {error}")
    return True


def render_answered_status_captions(adaptive_message="", adaptive_reason="", unlocked_message="", fallback_message=""):
    if adaptive_message:
        st.caption(adaptive_message)
    if adaptive_reason:
        st.caption(f"Why this path: {adaptive_reason}.")
    if unlocked_message:
        st.caption(unlocked_message)
    if fallback_message:
        st.caption(fallback_message)


def transition_to_mastery_followup(progress, question):
    followup = build_followup_question(progress, question)
    if followup is None:
        st.warning("No close follow-up is ready yet. Continuing with the normal path.")
        followup = generate_mastery_question(progress)
    if is_tense_family_skill(question):
        st.session_state.pending_tense_contrast_followup = False
    transition_to_question(
        finalize_transition_debug(
            followup,
            (followup.get("_debug_trace") or {}).get("transition_path", "follow-up"),
            (followup.get("_debug_trace") or {}).get("transition_reason", ""),
        )
    )


def transition_to_practice_followup(progress, question, skill):
    followup = build_followup_question(progress, question)
    if followup is None:
        followup = generate_practice_question(skill, progress)
    if is_tense_family_skill(question):
        st.session_state.pending_tense_contrast_followup = False
    transition_to_question(
        finalize_transition_debug(
            followup,
            (followup.get("_debug_trace") or {}).get("transition_path", "follow-up"),
            (followup.get("_debug_trace") or {}).get("transition_reason", ""),
        )
    )


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
            if run_pending_post_answer_action(
                "next_mastery",
                lambda: transition_to_question(
                    finalize_transition_debug(
                        generate_mastery_question(progress),
                        "next_question",
                        adaptive_reason,
                    )
                ),
                "next_mastery_loading",
            ):
                return
            render_answered_status_captions(adaptive_message, adaptive_reason, unlocked_message, fallback_message)
            with st.container():
                action_wrapper_id = render_post_answer_action_bar()
                if st.button("Next Question", type="primary", use_container_width=True, key="next_mastery"):
                    queue_post_answer_action("next_mastery")
                    return
                render_enter_key_handler("enter_next_mastery", ["Next Question"])
                render_post_answer_action_visibility(action_wrapper_id, ["Next Question"])
        else:
            if run_pending_post_answer_action(
                "retry_mastery_like_this",
                lambda: transition_to_mastery_followup(progress, question),
                "retry_mastery_like_this_loading",
            ):
                return
            if run_pending_post_answer_action(
                "continue_mastery_after_error",
                lambda: transition_to_question(
                    finalize_transition_debug(
                        generate_mastery_question(progress),
                        "retry_continue",
                        adaptive_reason,
                    )
                ),
                "continue_mastery_after_error_loading",
            ):
                return
            render_answered_status_captions(adaptive_message, adaptive_reason, unlocked_message, fallback_message)
            with st.container():
                action_wrapper_id = render_post_answer_action_bar("Keep going when you're ready.")
                if st.button("Try One Like This", type="primary", use_container_width=True, key="retry_mastery_like_this"):
                    queue_post_answer_action("retry_mastery_like_this")
                    return
                if st.button("Continue", use_container_width=True, key="continue_mastery_after_error"):
                    queue_post_answer_action("continue_mastery_after_error")
                    return
                render_enter_key_handler("enter_retry_mastery", ["Try One Like This", "Continue"])
                render_post_answer_action_visibility(action_wrapper_id, ["Continue", "Try One Like This"])


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
            if run_pending_post_answer_action(
                f"next_practice_{skill}",
                lambda: transition_to_question(
                    finalize_transition_debug(
                        generate_practice_question(skill, progress),
                        "next_question",
                    )
                ),
                f"next_practice_{skill}_loading",
            ):
                return
            render_answered_status_captions(fallback_message=fallback_message)
            with st.container():
                action_wrapper_id = render_post_answer_action_bar()
                if st.button("Next Question", type="primary", use_container_width=True, key=f"next_practice_{skill}"):
                    queue_post_answer_action(f"next_practice_{skill}")
                    return
                render_enter_key_handler(f"enter_next_practice_{skill}", ["Next Question"])
                render_post_answer_action_visibility(action_wrapper_id, ["Next Question"])
        else:
            if run_pending_post_answer_action(
                f"retry_practice_like_this_{skill}",
                lambda: transition_to_practice_followup(progress, question, skill),
                f"retry_practice_like_this_{skill}_loading",
            ):
                return
            if run_pending_post_answer_action(
                f"continue_practice_after_error_{skill}",
                lambda: transition_to_question(
                    finalize_transition_debug(
                        generate_practice_question(skill, progress),
                        "retry_continue",
                    )
                ),
                f"continue_practice_after_error_{skill}_loading",
            ):
                return
            render_answered_status_captions(fallback_message=fallback_message)
            with st.container():
                action_wrapper_id = render_post_answer_action_bar("Keep going when you're ready.")
                if st.button("Try One Like This", type="primary", use_container_width=True, key=f"retry_practice_like_this_{skill}"):
                    queue_post_answer_action(f"retry_practice_like_this_{skill}")
                    return
                if st.button("Continue", use_container_width=True, key=f"continue_practice_after_error_{skill}"):
                    queue_post_answer_action(f"continue_practice_after_error_{skill}")
                    return
                render_enter_key_handler(f"enter_retry_practice_{skill}", ["Try One Like This", "Continue"])
                render_post_answer_action_visibility(action_wrapper_id, ["Continue", "Try One Like This"])


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
    validation = validate_question_for_serve(
        question,
        fallback_text=flow.get("pasuk", ""),
        validation_path="pasuk_flow_step",
        trusted_active_scope=True,
    )
    if not validation["valid"]:
        st.warning(
            "This pasuk-flow question was blocked before serve because it no longer passed runtime validation."
        )
        return
    question = validation["question"]
    steps[step_index] = question

    render_assessment_diagnostics(question, flow, "Pasuk Flow")
    render_question(question, progress, f"flow_{step_index}", flow)
    with st.expander("Pasuk Flow Steps", expanded=False):
        render_flow_overview(flow, step_index)

    if st.session_state.answered:
        if step_index + 1 < len(steps):
            if run_pending_post_answer_action(
                f"next_flow_step_{step_index}",
                lambda: _advance_flow_step(),
                f"next_flow_step_{step_index}_loading",
            ):
                return
            with st.container():
                action_wrapper_id = render_post_answer_action_bar("Ready for the next step?")
                if st.button("Next Step", type="primary", use_container_width=True, key=f"next_flow_step_{step_index}"):
                    queue_post_answer_action(f"next_flow_step_{step_index}")
                    return
                render_enter_key_handler(f"enter_next_flow_{step_index}", ["Next Step"])
                render_post_answer_action_visibility(action_wrapper_id, ["Next Step"])
        else:
            st.success("Pasuk flow complete.")
            if run_pending_post_answer_action(
                "restart_flow",
                lambda: _restart_flow(),
                "restart_flow_loading",
            ):
                return
            with st.container():
                action_wrapper_id = render_post_answer_action_bar("Ready to run this pasuk flow again?")
                if st.button("Restart Flow", type="primary", use_container_width=True, key="restart_flow"):
                    queue_post_answer_action("restart_flow")
                    return
                render_enter_key_handler("enter_restart_flow", ["Restart Flow"])
                render_post_answer_action_visibility(action_wrapper_id, ["Restart Flow"])


def _advance_flow_step():
    st.session_state.flow_step += 1
    st.session_state.answered = False
    st.session_state.selected_answer = None
    st.session_state.post_answer_action_pending = ""
    schedule_question_arrival()
    st.rerun()


def _restart_flow():
    st.session_state.flow_step = 0
    st.session_state.answered = False
    st.session_state.selected_answer = None
    st.session_state.post_answer_action_pending = ""
    schedule_question_arrival()
    st.rerun()
