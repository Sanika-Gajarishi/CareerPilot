import streamlit as st

from components.answer_card import answer_card
from components.interview_summary import show_summary
from components.question_card import question_card
from services.interview_service import (
    interview_history,
    start_interview,
    submit_answer,
)


def _answer_for(answers, question_number):
    return next(
        (
            item
            for item in answers
            if int(item.get("question_number", -1)) == question_number
        ),
        None,
    )


def _show_question_status(questions, answers):
    st.caption("Questions")
    columns = st.columns(len(questions))
    for index, item in enumerate(questions):
        number = int(item["question_number"])
        answered = _answer_for(answers, number) is not None
        label = f"{'✓' if answered else '○'} {number}"
        if columns[index].button(label, key=f"question_{number}"):
            st.session_state.current_question = index
            st.session_state.hint_question = None
            st.rerun()


def interview_page():
    st.title("AI Mock Interview")
    token = st.session_state.get("token")
    if not token:
        st.error("Please login first.")
        return

    if "interview" not in st.session_state:
        st.session_state.interview = None
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "hint_question" not in st.session_state:
        st.session_state.hint_question = None

    if st.session_state.interview is None:
        st.subheader("Start New Interview")
        target_role = st.text_input("Target Role", placeholder="AI Engineer")
        company = st.text_input("Company", placeholder="Google")
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
        interview_type = st.selectbox("Interview Type", ["Technical", "HR", "Mixed"])
        if st.button("Start Interview", use_container_width=True):
            with st.spinner("Generating interview..."):
                try:
                    st.session_state.interview = start_interview(
                        token, target_role, company, difficulty, interview_type
                    )
                    st.session_state.current_question = 0
                    st.rerun()
                except Exception as error:
                    st.error(str(error))
        return

    interview = st.session_state.interview
    questions = interview.get("questions", {}).get("questions", [])
    answers = interview.get("answers", [])
    if not questions:
        st.error("This interview has no questions.")
        return

    current = min(st.session_state.current_question, len(questions) - 1)
    st.session_state.current_question = current
    question = questions[current]
    question_number = int(question["question_number"])
    saved_answer = _answer_for(answers, question_number)

    st.write(f"**Role:** {interview['target_role']}")
    st.write(f"**Company:** {interview.get('company') or 'Open role'}")
    st.progress((current + 1) / len(questions))
    st.write(f"Question {current + 1} of {len(questions)}")
    question_card(question)

    if st.button("Hint", key=f"hint_{question_number}"):
        st.session_state.hint_question = question_number
    if st.session_state.hint_question == question_number:
        st.info(
            "Think about: the definition, the key parts involved, one practical "
            "example, and the tradeoffs or use cases."
        )

    answer = st.text_area(
        "Your Answer",
        value=saved_answer.get("answer", "") if saved_answer else "",
        height=220,
        key=f"answer_{question_number}",
    )
    if st.button("Save Answer", use_container_width=True):
        try:
            st.session_state.interview = submit_answer(
                interview["id"], question_number, answer, token
            )
            st.session_state.hint_question = None
            st.rerun()
        except Exception as error:
            st.error(str(error))

    previous_column, next_column = st.columns(2)
    with previous_column:
        if st.button("← Previous", disabled=current == 0, use_container_width=True):
            st.session_state.current_question = current - 1
            st.session_state.hint_question = None
            st.rerun()
    with next_column:
        if st.button(
            "Next →",
            disabled=current == len(questions) - 1,
            use_container_width=True,
        ):
            st.session_state.current_question = current + 1
            st.session_state.hint_question = None
            st.rerun()

    _show_question_status(questions, answers)

    if saved_answer:
        st.divider()
        answer_card(saved_answer)

    if interview.get("status") == "Completed":
        show_summary(interview)

    st.divider()
    st.subheader("Previous Interviews")
    try:
        history = interview_history(token)
        if not history:
            st.info("No previous interviews.")
        for item in history:
            with st.expander(f"{item['target_role']} • {item['status']}"):
                st.write(f"Company: {item.get('company') or 'Open role'}")
                st.write(f"Difficulty: {item['difficulty']}")
    except Exception:
        pass