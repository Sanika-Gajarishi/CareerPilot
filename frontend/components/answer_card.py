import streamlit as st


def answer_card(answer):

    with st.container():

        st.write("### Your Answer")

        st.write(answer["answer"])

        st.write("### Interviewer Feedback")

        feedback = answer["feedback"]

        if isinstance(feedback, dict):

            st.write(
                feedback.get(
                    "interviewer_feedback",
                    feedback.get("overall_feedback", ""),
                )
            )

            expectations = feedback.get(
                "interviewer_expectations",
                [],
            )
            if expectations:
                st.write("**As an interviewer, I would expect:**")
                for item in expectations:
                    st.write(f"- {item}")

            if "strengths" in feedback:

                for s in feedback["strengths"]:
                    st.success(s)

            missing = feedback.get(
                "missing",
                feedback.get("improvements", []),
            )
            if missing:
                st.write("**Missing**")
                for item in missing:
                    st.warning(item)

            if "ideal_answer" in feedback:
                st.write("### Ideal Interview Answer")
                st.info(feedback["ideal_answer"])

            if "tips" in feedback:
                st.write("### Tips")
                for item in feedback["tips"]:
                    st.success(item)

        else:

            st.write(feedback)