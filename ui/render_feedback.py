import streamlit as st

from question_ui import build_feedback_context


def render_feedback(question, progress):
    import streamlit_app as app

    skill_state = st.session_state.get("last_skill_state") or {}
    point_change = skill_state.get("point_change", "")
    is_correct = app.last_answer_was_correct(question)
    status_class = "correct" if is_correct else "incorrect"
    selected = st.session_state.selected_answer or ""
    practice_type = st.session_state.get("practice_type", "Learn Mode")
    skill_label = app.plain_skill(question)
    feedback = build_feedback_context(
        question=question,
        selected_answer=selected,
        is_correct=is_correct,
        clue_text=app.clue_sentence(question),
        practice_type=practice_type,
        skill_label=skill_label,
        next_skill_label=app.skill_path_label(app.get_next_skill(progress.get("current_skill", question.get("skill", "")))),
    )
    short_clue = feedback["grammar_feedback"] or feedback["clue_that_mattered"]
    short_explanation = feedback["explanation"]
    if short_explanation == short_clue:
        short_explanation = feedback["clue_that_mattered"]
    if short_explanation == short_clue:
        short_explanation = ""

    st.markdown(
        f"""
        <section class="feedback-panel {status_class}">
            <div class="feedback-status">
                <strong>{feedback['title']}</strong>
                <span>{app.escape(str(point_change))}</span>
            </div>
            <div class="feedback-line">
                <span>Your answer</span>
                <b>{app.mixed_text_html(feedback['selected_answer'])}</b>
            </div>
            <div class="feedback-line">
                <span>Correct answer</span>
                <b>{app.mixed_text_html(feedback['correct_answer'])}</b>
            </div>
            <div class="section-label feedback-heading">Grammar</div>
            <div class="feedback-line feedback-clue">
                <span>Clue</span>
                <div>{app.mixed_text_html(short_clue)}</div>
            </div>
            <div class="feedback-line feedback-note">
                <span>Why</span>
                <div>{app.mixed_text_html(short_explanation)}</div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    extra_detail = bool(feedback["clue_that_mattered"] or feedback["explanation"] or feedback["likely_confusion"])
    if extra_detail:
        with st.expander("More grammar detail", expanded=False):
            if feedback["clue_that_mattered"]:
                st.markdown(
                    f"""
                    <section class="feedback-detail-grid">
                        <div class="feedback-detail">
                            <span>Clue That Mattered</span>
                            <div>{app.mixed_text_html(feedback['clue_that_mattered'])}</div>
                        </div>
                    </section>
                    """,
                    unsafe_allow_html=True,
                )
            if feedback["explanation"] and feedback["explanation"] not in {short_clue, short_explanation}:
                st.markdown(
                    f"""
                    <section class="feedback-detail-grid">
                        <div class="feedback-detail">
                            <span>More Detail</span>
                            <div>{app.mixed_text_html(feedback['explanation'])}</div>
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
                        <div>{app.mixed_text_html(feedback['likely_confusion'])}</div>
                    </section>
                    """,
                    unsafe_allow_html=True,
                )
            st.markdown(
                f"""
                <section class="feedback-detail-grid">
                    <div class="feedback-detail">
                        <span>Word</span>
                        <div>{app.mixed_text_html(question.get('selected_word') or question.get('word') or '')}</div>
                    </div>
                </section>
                """,
                unsafe_allow_html=True,
            )
            app.render_grammar_clues(question)

    if skill_state:
        st.caption(f"Mastery {skill_state['score']}/100 | Streak {skill_state['current_streak']}")
