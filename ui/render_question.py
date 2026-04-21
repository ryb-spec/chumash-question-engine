import hashlib
import json
from html import escape

import streamlit as st
import streamlit.components.v1 as components

from question_ui import build_learning_context
from runtime.pilot_logging import sync_pilot_served_question
from runtime.presentation import (
    QUESTION_TYPE_NAMES,
    get_next_skill,
    get_skill_level,
    skill_path_label,
    student_skill_context,
    thinking_tip,
)
from runtime.question_flow import build_quiz_debug_payload, display_context_policy
from runtime.runtime_support import (
    OPTION_LABELS,
    developer_debug_enabled,
    get_pasukh_text,
    get_source_label,
    handle_answer,
    load_word_bank_metadata,
    menukad_text,
    mixed_text_html,
    rtl_hebrew_html,
)

STUDENT_TENSE_LABELS = {
    "vav_consecutive_past": "past",
    "future_jussive": "future",
    "future": "future",
    "past": "past",
    "present": "present",
    "infinitive": "to do form",
}
COHORT_TAUGHT_TENSE_LABELS = {"past", "future", "present", "to do form"}


def _clean_clue_value(value):
    text = str(value or "").strip()
    if not text:
        return None
    if set(text) == {"?"} or "???" in text:
        return None
    return text


def _clean_shoresh(value):
    text = _clean_clue_value(value)
    if not text or "?" in text:
        return None
    return text


def _student_tense_label(value):
    text = _clean_clue_value(value)
    if not text:
        return None
    label = STUDENT_TENSE_LABELS.get(text, text)
    if label not in COHORT_TAUGHT_TENSE_LABELS:
        return None
    return label


def split_pasuk_phrases(text, words_per_phrase=4):
    words = menukad_text(text).split()
    if len(words) <= words_per_phrase:
        return [" ".join(words)] if words else []

    phrases = []
    for index in range(0, len(words), words_per_phrase):
        phrases.append(" ".join(words[index:index + words_per_phrase]))
    return phrases


def highlight_display_text(text, focus):
    safe_text = escape(menukad_text(text))
    if focus:
        safe_focus = escape(menukad_text(focus))
        safe_text = safe_text.replace(
            safe_focus,
            f"<mark>{safe_focus}</mark>",
            1,
        )
    return safe_text


def question_key(question, prefix):
    raw = "|".join(
        str(part)
        for part in [
            prefix,
            question.get("id", ""),
            question.get("question", ""),
            question.get("selected_word", ""),
            question.get("correct_answer", ""),
        ]
    )
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]


def current_question_arrival_token(question_key_value):
    token = st.session_state.get("current_question_arrival_token", "")
    if token:
        return token
    return f"question-arrival-{question_key_value}"


def question_wrapper_id(arrival_token):
    return f"student-question-wrapper-{arrival_token}"


def render_question_arrival_scroll(arrival_token, wrapper_id):
    if st.session_state.get("answered"):
        return

    should_scroll = st.session_state.get("scroll_to_question_on_render", False)
    last_scroll_token = st.session_state.get("last_question_scroll_token", "")
    if not should_scroll and last_scroll_token == arrival_token:
        return

    st.session_state.last_question_scroll_token = arrival_token
    st.session_state.scroll_to_question_on_render = False
    script = """
        <script>
        (function() {{
            const rootWindow = window.parent;
            const rootDocument = rootWindow.document;
            const arrivalToken = {arrival_token};
            const targetId = {wrapper_id};
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
                return Math.max(28, headerHeight + 16);
            }};

            const scrollToTarget = (target) => {{
                const offset = topOffset();
                const scrollContainer = findScrollContainer(target);
                const targetRect = target.getBoundingClientRect();

                if (
                    scrollContainer === rootDocument.body
                    || scrollContainer === rootDocument.documentElement
                    || scrollContainer === rootDocument.scrollingElement
                ) {{
                    const top = Math.max(
                        targetRect.top + rootWindow.pageYOffset - offset,
                        0
                    );
                    rootWindow.scrollTo({{ top, behavior: "auto" }});
                    return;
                }}

                const containerRect = scrollContainer.getBoundingClientRect();
                const top = Math.max(
                    targetRect.top - containerRect.top + scrollContainer.scrollTop - offset,
                    0
                );
                scrollContainer.scrollTo({{ top, behavior: "auto" }});
            }};

            const targetLooksReady = (target) => {{
                const rect = target.getBoundingClientRect();
                const viewportHeight = rootWindow.innerHeight || rootDocument.documentElement.clientHeight || 0;
                const offset = topOffset();
                return rect.top >= offset && rect.top <= Math.max(offset + 140, viewportHeight * 0.35);
            }};

            const activateTarget = (target) => {{
                try {{
                    target.focus({{ preventScroll: true }});
                }} catch (error) {{
                    target.focus();
                }}
                target.classList.add("question-arrival-active");
                rootWindow.setTimeout(() => {{
                    target.classList.remove("question-arrival-active");
                }}, 1200);
            }};

            const retryScroll = () => {{
                if (attempts >= maxAttempts) {{
                    rootWindow.__assessmentArrivalHandledToken = arrivalToken;
                    rootWindow.__assessmentPendingArrivalToken = "";
                    return;
                }}
                rootWindow.requestAnimationFrame(() => rootWindow.setTimeout(findAndScroll, 35));
            }};

            const findAndScroll = () => {{
                if (
                    rootWindow.__assessmentPendingArrivalToken
                    && rootWindow.__assessmentPendingArrivalToken !== arrivalToken
                ) {{
                    return;
                }}

                const target = rootDocument.getElementById(targetId);
                if (!target) {{
                    attempts += 1;
                    retryScroll();
                    return;
                }}

                if (
                    rootWindow.__assessmentArrivalHandledToken === arrivalToken
                    && targetLooksReady(target)
                ) {{
                    return;
                }}

                rootWindow.__assessmentPendingArrivalToken = arrivalToken;
                target.setAttribute("data-arrival-token", arrivalToken);
                scrollToTarget(target);
                rootWindow.requestAnimationFrame(() => {{
                    activateTarget(target);
                    if (targetLooksReady(target)) {{
                        rootWindow.__assessmentArrivalHandledToken = arrivalToken;
                        rootWindow.__assessmentPendingArrivalToken = "";
                        return;
                    }}
                    attempts += 1;
                    retryScroll();
                }});
            }};

            rootWindow.requestAnimationFrame(findAndScroll);
            rootWindow.setTimeout(findAndScroll, 60);
            rootWindow.setTimeout(findAndScroll, 180);
            rootWindow.setTimeout(findAndScroll, 320);
            rootWindow.setTimeout(findAndScroll, 520);
            rootWindow.setTimeout(findAndScroll, 820);
            rootWindow.setTimeout(findAndScroll, 1200);
            if (rootDocument.readyState !== "complete") {{
                rootWindow.addEventListener("load", findAndScroll, {{ once: true }});
            }}
        }})();
        </script>
        """.format(
        arrival_token=json.dumps(arrival_token),
        wrapper_id=json.dumps(wrapper_id),
    )
    components.html(
        script,
        height=0,
    )


def render_enter_key_handler(handler_key, action_labels):
    labels = [label for label in action_labels if label]
    if not labels:
        return

    script = f"""
    <script>
    (function() {{
        const handlerId = {json.dumps(handler_key)};
        const labels = {json.dumps(labels)};
        const root = window.parent.document;
        const registry = window.parent.__assessmentEnterHandlers || (window.parent.__assessmentEnterHandlers = {{}});

        if (registry[handlerId]) {{
            root.removeEventListener('keydown', registry[handlerId], true);
        }}

        const isVisible = (element) => !!(element && element.offsetParent !== null);
        const isAllowedTarget = (element) => {{
            if (!element) return true;
            const tag = (element.tagName || '').toLowerCase();
            if (tag === 'textarea') return false;
            if (tag === 'input') {{
                const inputType = (element.type || '').toLowerCase();
                return !['text', 'search', 'email', 'url', 'password', 'number'].includes(inputType);
            }}
            return true;
        }};

        const handler = (event) => {{
            if (event.key !== 'Enter' || event.shiftKey || event.ctrlKey || event.metaKey || event.altKey) return;
            if (!isAllowedTarget(root.activeElement)) return;

            const buttons = Array.from(root.querySelectorAll('button[kind="primary"], button[data-testid="baseButton-primary"]'));
            const target = buttons.find((button) => {{
                const label = (button.innerText || button.textContent || '').trim();
                return !button.disabled && isVisible(button) && labels.includes(label);
            }});
            if (!target) return;

            event.preventDefault();
            target.click();
        }};

        registry[handlerId] = handler;
        root.addEventListener('keydown', handler, true);
    }})();
    </script>
    """
    components.html(script, height=0, width=0)


def highlight_focus(text, focus):
    if not text:
        return ""
    return highlight_display_text(text, focus)


def question_type_key(question):
    return question.get("question_type") or question.get("skill") or ""


def uses_compact_pasuk_context(question, flow=None):
    return display_context_policy(question, flow)["mode"] == "compact"


def local_context_snippet(pasuk, focus, radius=2):
    tokens = menukad_text(pasuk).split()
    focus_text = menukad_text(focus)
    if not tokens or not focus_text:
        return ""

    focus_tokens = focus_text.split()
    if not focus_tokens:
        return ""

    match_index = None
    match_length = len(focus_tokens)
    for index in range(0, len(tokens) - match_length + 1):
        if tokens[index:index + match_length] == focus_tokens:
            match_index = index
            break

    if match_index is None and focus_text in tokens:
        match_index = tokens.index(focus_text)
        match_length = 1

    if match_index is None:
        return ""

    start = max(0, match_index - radius)
    end = min(len(tokens), match_index + match_length + radius)
    snippet = " ".join(tokens[start:end])
    if start > 0:
        snippet = "... " + snippet
    if end < len(tokens):
        snippet += " ..."
    return snippet


def get_word_entry(question):
    word_bank_metadata = load_word_bank_metadata()
    selected_word = question.get("selected_word") or question.get("word", "")
    if selected_word in word_bank_metadata:
        return word_bank_metadata[selected_word]
    from torah_parser.word_bank_adapter import normalize_hebrew_key

    normalized_selected = normalize_hebrew_key(selected_word)
    if normalized_selected in word_bank_metadata:
        return word_bank_metadata[normalized_selected]

    for token in selected_word.split():
        if token in word_bank_metadata:
            return word_bank_metadata[token]
        normalized_token = normalize_hebrew_key(token)
        if normalized_token in word_bank_metadata:
            return word_bank_metadata[normalized_token]

    return None


def render_quiz_debug_panel(question, progress=None, flow=None):
    if not developer_debug_enabled():
        return

    debug = build_quiz_debug_payload(question, progress=progress, flow=flow)
    with st.expander("Developer Debug", expanded=False):
        st.caption(f"Source: {debug['current_question_source']}")
        st.caption(f"Skill: {debug['current_skill']}")
        if debug["target_word"]:
            st.caption(f"Target word: {debug['target_word']}")
        st.caption(f"Routing mode: {debug['routing_mode']}")
        st.caption(f"Path: {debug['next_question_path']}")
        if debug["fallback_path"]:
            st.caption(f"Fallback path: {debug['fallback_path']}")
        st.caption(f"Progress object: {debug['progress_source']}")
        st.caption(f"Candidate filtered: {'yes' if debug['candidate_filtered'] else 'no'}")
        if debug["rejection_total"]:
            st.caption(f"Rejected candidates this cycle: {debug['rejection_total']}")
            for item in debug["rejection_reason_counts"]:
                st.caption(f"Rejected for {item['label']}: {item['count']}")
        if debug["candidate_filter_reasons"]:
            for reason in debug["candidate_filter_reasons"]:
                st.caption(f"Filter reason: {reason}")
        if debug["transition_reason"]:
            st.caption(f"Transition reason: {debug['transition_reason']}")
        if debug["candidate_score_breakdown"]:
            breakdown = debug["candidate_score_breakdown"]
            st.caption(f"Candidate score total: {breakdown.get('total')}")
            for key in (
                "adaptive_weight",
                "clarity",
                "distractor_separation",
                "novelty",
                "context_dependence",
                "display_compactness",
            ):
                if key in breakdown:
                    st.caption(f"{key.replace('_', ' ').title()}: {breakdown[key]}")
            if breakdown.get("display_context_mode"):
                st.caption(
                    f"Display context: {breakdown['display_context_mode']} ({breakdown.get('display_context_reason', '')})"
                )
        if debug["question_generation_ms"] is not None:
            st.caption(f"Question generation: {debug['question_generation_ms']} ms")
        if debug["followup_generation_ms"] is not None:
            st.caption(f"Follow-up generation: {debug['followup_generation_ms']} ms")
        if debug["answer_to_next_ready_ms"] is not None:
            st.caption(f"Answer to next ready: {debug['answer_to_next_ready_ms']} ms")


def render_debug(question, progress=None):
    word_bank_metadata = load_word_bank_metadata()
    selected_word = question.get("selected_word") or question.get("word", "")
    word_entry = word_bank_metadata.get(selected_word)

    if word_entry is None:
        for token in selected_word.split():
            if token in word_bank_metadata:
                word_entry = word_bank_metadata[token]
                break

    group = question.get("generation_group")
    if group is None and word_entry is not None:
        group = word_entry.get("group")

    difficulty = question.get("difficulty")
    if difficulty is None and word_entry is not None:
        difficulty = word_entry.get("difficulty")

    difficulty = difficulty or question.get("difficulty", 1)
    current_skill = (progress or {}).get("current_skill", question.get("skill", ""))
    skill_context = student_skill_context(question=question, current_skill=current_skill)
    st.markdown(
        f"""
        <div class="learning-chips">
            <span>{escape(skill_context['student_label'])}</span>
            <span>Level {escape(str(difficulty))}</span>
            <span dir="rtl" lang="he">{mixed_text_html(selected_word)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_learning_header(question, progress, flow=None):
    standard = question.get("standard", "unknown")
    score = progress["standards"].get(standard, 0)
    xp = progress["xp"].get(standard, 0)
    level = get_skill_level(xp)
    skill_state = st.session_state.get("last_skill_state")
    mastery_score = skill_state["score"] if skill_state else score
    source = get_source_label(question, flow)
    practice_type = "Pasuk Flow" if flow is not None else st.session_state.get("practice_type", "Learn Mode")
    current_skill = progress.get("current_skill", question.get("skill", standard))
    skill_context = student_skill_context(question=question, current_skill=current_skill)

    if flow is not None:
        steps = flow.get("questions") or flow.get("steps", [])
        step_index = st.session_state.flow_step + 1
        progress_value = step_index / max(1, len(steps))
        progress_text = f"You're {int(progress_value * 100)}% through this pasuk."
        step_text = f"Step {step_index} of {len(steps)}"
    else:
        progress_value = mastery_score / 100
        progress_text = f"You're building {skill_context['current_label']}."
        step_text = f"Practice level {level}"

    next_skill_label = skill_path_label(get_next_skill(current_skill))
    header_context = build_learning_context(
        practice_type=practice_type,
        skill_label=skill_context["focus_label"],
        current_skill_label=skill_context["current_label"],
        next_skill_label=next_skill_label,
        source_label=source,
        focus_tip=thinking_tip(question),
    )
    st.markdown(
        f"""
        <section class="learning-header">
            <div class="meta-row quiz-meta-row">
                <span>{escape(source)}</span>
                <span>{escape(step_text)}</span>
                <span>{escape(skill_context['student_label'])}</span>
                <span class="mastery-chip">Mastery {escape(str(mastery_score))}/100</span>
            </div>
            <p class="focus-line">{escape(header_context['what_to_focus_on'])}</p>
            <small class="progress-note">{escape(progress_text)}</small>
        </section>
        """,
        unsafe_allow_html=True,
    )
    st.progress(progress_value)


def render_pasukh_panel(question, flow=None):
    if question.get("hide_pasuk"):
        return

    pasuk = get_pasukh_text(question, flow)
    focus = "" if question.get("hide_focus_word") else question.get("selected_word") or question.get("word", "")
    if not pasuk:
        return

    source = get_source_label(question, flow)
    compact_context = uses_compact_pasuk_context(question, flow)
    focus_label = "Focus Phrase" if focus and " " in focus.strip() else "Focus Word"
    st.markdown(
        f"""
        <div class="section-heading">
            <span>{focus_label if compact_context else 'Read The Pasuk'}</span>
            <small>{escape(source)}</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if compact_context and focus:
        st.markdown(
            f"""
            <section class="compact-context">
                <div class="target-word" dir="rtl" lang="he">{mixed_text_html(focus)}</div>
            </section>
            """,
            unsafe_allow_html=True,
        )
        with st.expander("Show full pasuk"):
            if st.session_state.get("pasuk_view_mode") == "Break into phrases":
                lines = []
                for index, phrase in enumerate(split_pasuk_phrases(pasuk), start=1):
                    lines.append(
                        f"""
                        <div class="phrase-line">
                            <span class="phrase-number">{index}</span>
                            <span class="phrase-text" dir="rtl" lang="he">{highlight_display_text(phrase, focus)}</span>
                        </div>
                        """
                    )
                st.markdown(
                    f"<section class='pasuk-box phrase-box compact-full-pasuk' dir='rtl' lang='he'>{''.join(lines)}</section>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    rtl_hebrew_html(pasuk, focus, "pasuk-box compact-full-pasuk"),
                    unsafe_allow_html=True,
                )
        return

    if st.session_state.get("pasuk_view_mode") == "Break into phrases":
        lines = []
        for index, phrase in enumerate(split_pasuk_phrases(pasuk), start=1):
            lines.append(
                f"""
                <div class="phrase-line">
                    <span class="phrase-number">{index}</span>
                    <span class="phrase-text" dir="rtl" lang="he">{highlight_display_text(phrase, focus)}</span>
                </div>
                """
            )
        st.markdown(
            f"<section class='pasuk-box phrase-box' dir='rtl' lang='he'>{''.join(lines)}</section>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(rtl_hebrew_html(pasuk, focus, "pasuk-box"), unsafe_allow_html=True)


def render_grammar_clues(question):
    entry = get_word_entry(question)
    clues = []
    if entry:
        prefix = _clean_clue_value(entry.get("prefix"))
        prefix_meaning = _clean_clue_value(entry.get("prefix_meaning"))
        shoresh = _clean_shoresh(entry.get("shoresh"))
        suffix = _clean_clue_value(entry.get("suffix"))
        suffix_meaning = _clean_clue_value(entry.get("suffix_meaning"))
        tense = _student_tense_label(entry.get("tense"))
        if prefix and prefix_meaning:
            clues.append(f"{prefix} = {prefix_meaning}")
        if shoresh:
            clues.append(f"root clue: {shoresh}")
        if suffix and suffix_meaning:
            clues.append(f"{suffix} = {suffix_meaning}")
        if tense:
            clues.append(f"time clue: {tense}")

    if clues:
        st.markdown("**Key clues:**")
        st.markdown(mixed_text_html(" | ".join(clues)), unsafe_allow_html=True)


def answer_choice_label(choice, index):
    return f"{OPTION_LABELS[index]}. {menukad_text(choice)}"


def render_question(question, progress, button_prefix, flow=None):
    practice_type = "Pasuk Flow" if flow is not None else st.session_state.get("practice_type", "Learn Mode")
    sync_pilot_served_question(
        question,
        practice_type=practice_type,
        flow_label=st.session_state.get("flow_label", "") if flow is not None else "",
        flow_step=(st.session_state.get("flow_step", 0) + 1) if flow is not None else None,
    )
    from ui.render_feedback import render_feedback

    key = question_key(question, button_prefix)
    arrival_token = current_question_arrival_token(key)
    wrapper_id = question_wrapper_id(arrival_token)
    render_question_arrival_scroll(arrival_token, wrapper_id)
    render_learning_header(question, progress, flow)
    with st.container():
        render_pasukh_panel(question, flow)
        render_debug(question, progress=progress)
        st.markdown(
            f"""
            <section
                id="{wrapper_id}"
                class="question-card question-arrival-target"
                data-arrival-token="{arrival_token}"
                tabindex="-1"
            >
                <div class="section-label">Question</div>
                <div class="question-text">{mixed_text_html(question['question'])}</div>
            </section>
            """,
            unsafe_allow_html=True,
        )
        render_quiz_debug_panel(question, progress=progress, flow=flow)

    choices = question["choices"]
    label_by_choice = {
        choice: answer_choice_label(choice, index)
        for index, choice in enumerate(choices)
    }

    st.markdown("<div class='section-label answer-label'>Choose An Answer</div>", unsafe_allow_html=True)
    selected_choice = st.radio(
        "Choose an answer",
        choices,
        key=f"{button_prefix}_choice_{key}",
        index=None,
        format_func=lambda choice: label_by_choice.get(choice, menukad_text(choice)),
        disabled=st.session_state.answered,
        label_visibility="collapsed",
    )

    if not st.session_state.answered:
        if st.button(
            "Check Answer",
            key=f"{button_prefix}_check_{key}",
            type="primary",
            disabled=selected_choice is None,
            use_container_width=True,
        ):
            handle_answer(selected_choice, question, progress)
            st.rerun()
        render_enter_key_handler(f"{button_prefix}_enter_check_{key}", ["Check Answer"])

    if st.session_state.answered:
        render_feedback(question, progress)
