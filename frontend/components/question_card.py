import streamlit as st


def question_card(question):

    st.markdown("---")

    st.subheader(
        f"Question {question['question_number']}"
    )

    st.write(question["question"])