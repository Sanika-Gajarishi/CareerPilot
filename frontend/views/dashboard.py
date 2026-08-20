import streamlit as st

from components.cards import metric_card
from services.api import get_dashboard
from utils.session import get_token


def dashboard_page():

    token = get_token()

    try:
        dashboard = get_dashboard(token)

    except Exception as e:

        st.error("Unable to load dashboard.")

        with st.expander("Error Details"):
            st.code(str(e))

        return

    # ==========================================================
    # SAFE VALUES
    # ==========================================================

    user_name = dashboard.get("user_name", "User")

    resume_count = dashboard.get("resume_count", 0)
    resume_score = dashboard.get("resume_score", 0)
    ats_score = dashboard.get("ats_score", 0)

    application_count = dashboard.get("application_count", 0)
    roadmap_count = dashboard.get("roadmap_count", 0)
    interview_count = dashboard.get("interview_count", 0)

    interview_ready = dashboard.get("interview_ready", 0)

    career_progress = dashboard.get("career_progress", 0)

    recent_activity = dashboard.get("recent_activity", [])

    recommendations = dashboard.get("recommendations", [])

    # ==========================================================
    # HEADER
    # ==========================================================

    st.title("🏠 Dashboard")

    st.markdown(
        f"""
### 👋 Welcome back, {user_name}

Manage your AI career journey from one place.
"""
    )

    st.write("")

    # ==========================================================
    # METRICS
    # ==========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card(
            "📄 Resumes",
            str(resume_count),
        )

    with col2:
        metric_card(
            "📊 Resume Score",
            f"{resume_score}%",
        )

    with col3:
        metric_card(
            "🎯 ATS Score",
            f"{ats_score}%",
        )

    with col4:
        metric_card(
            "💼 Applications",
            str(application_count),
        )

    col5, col6, col7 = st.columns(3)

    with col5:
        metric_card(
            "🗺 Roadmaps",
            str(roadmap_count),
        )

    with col6:
        metric_card(
            "🎤 Interviews",
            str(interview_count),
        )

    with col7:
        metric_card(
            "📈 Avg. Interview Score",
            f"{interview_ready:g}%",
        )

    st.write("")
    st.write("")

    # ==========================================================
    # CAREER PROGRESS
    # ==========================================================

    left, right = st.columns([2, 1])

    # ==========================================================
    # LEFT PANEL
    # ==========================================================

    with left:

        st.subheader("📈 Career Progress")

        st.progress(min(max(float(career_progress), 0), 100) / 100)

        st.caption(f"Roadmap progress: {career_progress:g}%")

        st.divider()

        st.subheader("📋 Recent Activity")

        if recent_activity:

            for item in recent_activity:
                st.success(item)

        else:
            st.info("No activity recorded yet.")

    # ==========================================================
    # RIGHT PANEL
    # ==========================================================

    with right:

        st.subheader("🤖 AI Recommendations")

        if recommendations:

            for recommendation in recommendations:

                st.info(recommendation)

        else:

            if ats_score == 0:
                st.info("Run your ATS analysis.")

            elif ats_score < 75:
                st.warning("Improve your ATS score.")

            else:
                st.success("Great ATS score!")

            if application_count == 0:
                st.info("Start tracking applications.")

            if interview_ready == 0:
                st.info("Practice interview questions.")

