import streamlit as st

from question_ui import build_feedback_context
from runtime.pilot_logging import (
    STUDENT_FLAG_NOTE_MAX_LENGTH,
    mark_current_question_unclear,
    question_is_flagged_unclear,
)
from runtime.presentation import get_next_skill, skill_path_label
from runtime.runtime_support import last_answer_was_correct, mixed_text_html
from ui.question_support import clue_sentence, render_grammar_clues


def render_feedback(question, progress):
    skill_state = st.session_state.get("last_skill_state") or {}
    point_change = skill_state.get("point_change", "")
    is_correct = last_answer_was_correct(question)
    status_class = "correct" if is_correct else "incorrect"
    selected = st.session_state.selected_answer or ""
    practice_type = st.session_state.get("practice_type", "Learn Mode")
    current_skill = progress.get("current_skill", question.get("skill", ""))
    feedback = build_feedback_context(
        question=question,
        selected_answer=selected,
        is_correct=is_correct,
        clue_text=clue_sentence(question),
        practice_type=practice_type,
        skill_label=skill_path_label(current_skill or question.get("skill", "")),
        current_skill=current_skill,
        next_skill_label=skill_path_label(get_next_skill(current_skill or question.get("skill", ""))),
    )
    main_lines = [
        ("Rule", feedback.get("rule_text", "")),
        ("Core", feedback.get("core_text", "")),
        ("Here", feedback.get("here_text", "")),
        ("Why Not", feedback.get("tempting_wrong_text", "")),
    ]
    main_lines = [(label, value) for label, value in main_lines if value]
    primary_detail_html = "".join(
        f"""
        <div class="feedback-line">
            <span>{label}</span>
            <div>{mixed_text_html(value)}</div>
        </div>
        """
        for label, value in main_lines
    )

    st.markdown(
        f"""
        <section class="feedback-panel {status_class}">
            <div class="feedback-status">
                <strong>{feedback['title']}</strong>
                <span>{point_change}</span>
            </div>
            <div class="section-label feedback-heading">{feedback['student_skill_label']}</div>
            <div class="feedback-line">
                <span>Your answer</span>
                <b>{mixed_text_html(feedback['selected_answer'])}</b>
            </div>
            <div class="feedback-line">
                <span>Correct answer</span>
                <b>{mixed_text_html(feedback['correct_answer'])}</b>
            </div>
            {primary_detail_html}
        </section>
        """,
        unsafe_allow_html=True,
    )
    extra_detail = bool(
        feedback["clue_that_mattered"]
        or feedback["explanation"]
        or feedback["likely_confusion"]
        or feedback.get("secondary_detail")
    )
    if extra_detail:
        with st.expander("More detail", expanded=False):
            if feedback["clue_that_mattered"]:
                st.markdown(
                    f"""
                    <section class="feedback-detail-grid">
                        <div class="feedback-detail">
                            <span>Clue That Mattered</span>
                            <div>{mixed_text_html(feedback['clue_that_mattered'])}</div>
                        </div>
                    </section>
                    """,
                    unsafe_allow_html=True,
                )
            if feedback.get("secondary_detail"):
                st.markdown(
                    f"""
                    <section class="feedback-detail-grid">
                        <div class="feedback-detail">
                            <span>More To Know</span>
                            <div>{mixed_text_html(feedback['secondary_detail'])}</div>
                        </div>
                    </section>
                    """,
                    unsafe_allow_html=True,
                )
            if feedback["explanation"] and feedback["explanation"] not in {
                feedback.get("rule_text", ""),
                feedback.get("core_text", ""),
                feedback.get("here_text", ""),
                feedback.get("tempting_wrong_text", ""),
                feedback.get("secondary_detail", ""),
            }:
                st.markdown(
                    f"""
                    <section class="feedback-detail-grid">
                        <div class="feedback-detail">
                            <span>More Detail</span>
                            <div>{mixed_text_html(feedback['explanation'])}</div>
                        </div>
                    </section>
                    """,
                    unsafe_allow_html=True,
                )
            if feedback["likely_confusion"]:
                st.markdown(
                    f"""
                    <section class="reteach-panel">
                        <span>Likely Confusion</span>
                        <div>{mixed_text_html(feedback['likely_confusion'])}</div>
                    </section>
                    """,
                    unsafe_allow_html=True,
                )
            st.markdown(
                f"""
                <section class="feedback-detail-grid">
                    <div class="feedback-detail">
                        <span>Word</span>
                        <div>{mixed_text_html(question.get('selected_word') or question.get('word') or '')}</div>
                    </div>
                </section>
                """,
                unsafe_allow_html=True,
            )
            render_grammar_clues(question)

    if skill_state:
        st.caption(f"Mastery {skill_state['score']}/100 | Streak {skill_state['current_streak']}")

    note_key = f"mark_unclear_note_{question.get('id') or question.get('question') or question.get('selected_word') or 'question'}"
    button_key = f"mark_unclear_{question.get('id') or question.get('question') or question.get('selected_word') or 'question'}"
    student_note = st.text_input(
        "Optional note for teacher",
        key=note_key,
        max_chars=STUDENT_FLAG_NOTE_MAX_LENGTH,
        placeholder="Optional: say what felt unclear",
        disabled=question_is_flagged_unclear(),
    )
    if st.button("Mark Question Unclear", key=button_key, use_container_width=True, disabled=question_is_flagged_unclear()):
        mark_current_question_unclear(question, note_text=student_note)
    if question_is_flagged_unclear():
        question_log_id = st.session_state.get("pilot_current_question_log_id")
        flagged_notes = st.session_state.setdefault("pilot_flagged_question_notes", {})
        st.caption("Marked for teacher review.")
        if question_log_id and flagged_notes.get(question_log_id):
            st.caption(f"Your note: {flagged_notes[question_log_id]}")
