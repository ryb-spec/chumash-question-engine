import hashlib
import json

import streamlit as st
import streamlit.components.v1 as components

from question_ui import build_learning_context
from runtime.question_flow import build_quiz_debug_payload, display_context_policy


def split_pasuk_phrases(text, words_per_phrase=4):
    import streamlit_app as app

    words = app.menukad_text(text).split()
    if len(words) <= words_per_phrase:
        return [" ".join(words)] if words else []

    phrases = []
    for index in range(0, len(words), words_per_phrase):
        phrases.append(" ".join(words[index:index + words_per_phrase]))
    return phrases


def highlight_display_text(text, focus):
    import streamlit_app as app

    safe_text = app.escape(app.menukad_text(text))
    if focus:
        safe_focus = app.escape(app.menukad_text(focus))
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
    import streamlit_app as app

    tokens = app.menukad_text(pasuk).split()
    focus_text = app.menukad_text(focus)
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
    import streamlit_app as app

    word_bank_metadata = app.load_word_bank_metadata()
    selected_word = question.get("selected_word") or question.get("word", "")
    if selected_word in word_bank_metadata:
        return word_bank_metadata[selected_word]
    normalized_selected = app.normalize_hebrew_key(selected_word)
    if normalized_selected in word_bank_metadata:
        return word_bank_metadata[normalized_selected]

    for token in selected_word.split():
        if token in word_bank_metadata:
            return word_bank_metadata[token]
        normalized_token = app.normalize_hebrew_key(token)
        if normalized_token in word_bank_metadata:
            return word_bank_metadata[normalized_token]

    return None


def render_quiz_debug_panel(question, progress=None, flow=None):
    import streamlit_app as app

    if not app.developer_debug_enabled():
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


def render_debug(question):
    import streamlit_app as app

    word_bank_metadata = app.load_word_bank_metadata()
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
    st.markdown(
        f"""
        <div class="learning-chips">
            <span>{app.escape(app.learning_goal(question))}</span>
            <span>Level {app.escape(str(difficulty))}</span>
            <span dir="rtl" lang="he">{app.mixed_text_html(selected_word)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_learning_header(question, progress, flow=None):
    import streamlit_app as app

    standard = question.get("standard", "unknown")
    score = progress["standards"].get(standard, 0)
    xp = progress["xp"].get(standard, 0)
    level = app.get_skill_level(xp)
    skill_state = st.session_state.get("last_skill_state")
    mastery_score = skill_state["score"] if skill_state else score

    if flow is not None:
        steps = flow.get("questions") or flow.get("steps", [])
        step_index = st.session_state.flow_step + 1
        progress_value = step_index / max(1, len(steps))
        progress_text = f"You're {int(progress_value * 100)}% through this pasuk."
        step_text = f"Step {step_index} of {len(steps)}"
    else:
        progress_value = mastery_score / 100
        progress_text = f"You're building {app.plain_skill(question).lower()}."
        step_text = f"Practice level {level}"

    source = app.get_source_label(question, flow)
    practice_type = "Pasuk Flow" if flow is not None else st.session_state.get("practice_type", "Learn Mode")
    current_skill = progress.get("current_skill", question.get("skill", standard))
    next_skill_label = app.skill_path_label(app.get_next_skill(current_skill))
    header_context = build_learning_context(
        practice_type=practice_type,
        skill_label=app.plain_skill(question),
        current_skill_label=app.skill_path_label(current_skill),
        next_skill_label=next_skill_label,
        source_label=source,
        focus_tip=app.thinking_tip(question),
    )
    st.markdown(
        f"""
        <section class="learning-header">
            <div class="meta-row quiz-meta-row">
                <span>{app.escape(source)}</span>
                <span>{app.escape(step_text)}</span>
                <span>{app.escape(app.plain_skill(question))}</span>
                <span class="mastery-chip">Mastery {app.escape(str(mastery_score))}/100</span>
            </div>
            <p class="focus-line">{app.escape(header_context['what_to_focus_on'])}</p>
            <small class="progress-note">{app.escape(progress_text)}</small>
        </section>
        """,
        unsafe_allow_html=True,
    )
    st.progress(progress_value)


def render_pasukh_panel(question, flow=None):
    import streamlit_app as app

    if question.get("hide_pasuk"):
        return

    pasuk = app.get_pasukh_text(question, flow)
    focus = "" if question.get("hide_focus_word") else question.get("selected_word") or question.get("word", "")
    if not pasuk:
        return

    source = app.get_source_label(question, flow)
    compact_context = uses_compact_pasuk_context(question, flow)
    st.markdown(
        f"""
        <div class="section-heading">
            <span>{'Focus Word' if compact_context else 'Read The Pasuk'}</span>
            <small>{app.escape(source)}</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if compact_context and focus:
        snippet = local_context_snippet(pasuk, focus)
        st.markdown(
            f"""
            <section class="compact-context">
                <div class="target-word" dir="rtl" lang="he">{app.mixed_text_html(focus)}</div>
                <div class="context-snippet" dir="rtl" lang="he">
                    {highlight_display_text(snippet, focus) if snippet else ''}
                </div>
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
                    app.rtl_hebrew_html(pasuk, focus, "pasuk-box compact-full-pasuk"),
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
        st.markdown(app.rtl_hebrew_html(pasuk, focus, "pasuk-box"), unsafe_allow_html=True)


def render_grammar_clues(question):
    import streamlit_app as app

    entry = get_word_entry(question)
    clues = []
    if entry:
        if entry.get("prefix"):
            clues.append(f"{entry['prefix']} = {entry.get('prefix_meaning', '')}")
        if entry.get("shoresh"):
            clues.append(f"root clue: {entry['shoresh']}")
        if entry.get("suffix"):
            clues.append(f"{entry['suffix']} = {entry.get('suffix_meaning', '')}")
        if entry.get("tense"):
            clues.append(f"time clue: {entry['tense']}")

    if clues:
        st.markdown("**Key clues:**")
        st.markdown(app.mixed_text_html(" | ".join(clues)), unsafe_allow_html=True)


def answer_choice_label(choice, index):
    import streamlit_app as app

    return f"{app.OPTION_LABELS[index]}. {app.menukad_text(choice)}"


def render_question(question, progress, button_prefix, flow=None):
    import streamlit_app as app

    render_learning_header(question, progress, flow)
    with st.container():
        render_pasukh_panel(question, flow)
        render_debug(question)
        st.markdown(
            f"""
            <section class="question-card">
                <div class="section-label">Question</div>
                <div class="question-text">{app.mixed_text_html(question['question'])}</div>
            </section>
            """,
            unsafe_allow_html=True,
        )
        render_quiz_debug_panel(question, progress=progress, flow=flow)

    key = question_key(question, button_prefix)
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
        format_func=lambda choice: label_by_choice.get(choice, app.menukad_text(choice)),
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
            app.handle_answer(selected_choice, question, progress)
            st.rerun()
        render_enter_key_handler(f"{button_prefix}_enter_check_{key}", ["Check Answer"])

    if st.session_state.answered:
        app.render_feedback(question, progress)
