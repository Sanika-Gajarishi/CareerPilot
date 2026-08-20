import streamlit as st


def show_summary(interview):

    st.divider()

    st.header("Interview Summary")

    feedback = interview.get("feedback") or {}
    readiness = min(100, max(0, round(interview.get("overall_score", 0))))

    st.subheader(
        f"Overall Performance: {feedback.get('grade', 'Complete')}"
    )
    st.progress(readiness / 100)
    st.write(f"Estimated Interview Readiness: **{readiness}%**")

    questions = interview.get("questions", {}).get("questions", [])
    answers = interview.get("answers", [])
    answered_numbers = {
        int(item.get("question_number", -1))
        for item in answers
    }
    answered_topics = [
        item.get("category", "General")
        for item in questions
        if int(item.get("question_number", -1)) in answered_numbers
    ]
    missing_topics = [
        item.get("category", "General")
        for item in questions
        if int(item.get("question_number", -1)) not in answered_numbers
    ]

    if answered_topics:
        st.write("**Topics Covered**")
        st.write(" • ".join(dict.fromkeys(answered_topics)))
    if missing_topics:
        st.write("**Needs Improvement**")
        for topic in dict.fromkeys(missing_topics):
            st.warning(topic)

    stars = max(1, min(5, round(readiness / 20)))
    st.write(f"Communication {'★' * stars}{'☆' * (5 - stars)}")
    st.write(f"Technical Depth {'★' * stars}{'☆' * (5 - stars)}")

    st.write("### Status")

    if interview["status"] == "Completed":
        st.success("Completed")
    else:
        st.info(interview["status"])

    if feedback.get("recommendation"):
        st.write(f"**Recommendation:** {feedback['recommendation']}")