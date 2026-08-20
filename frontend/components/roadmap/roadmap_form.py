import streamlit as st


def roadmap_form():

    with st.form("roadmap_form"):

        role = st.text_input(
            "Target Role",
            placeholder="AI Engineer"
        )

        company = st.text_input(
            "Dream Company",
            placeholder="Google"
        )

        level = st.selectbox(
            "Experience",
            [
                "Fresher",
                "0-1 Years",
                "2-3 Years",
                "5+ Years"
            ]
        )

        months = st.slider(
            "Timeline (Months)",
            1,
            24,
            6,
        )

        hours = st.slider(
            "Study Hours / Week",
            1,
            60,
            10,
        )

        submit = st.form_submit_button(
            "Generate Roadmap",
            use_container_width=True,
        )

    if submit:

        if not role.strip():
            st.error("Target role is required.")
            return None

        return {
            "target_role": role,
            "target_company": company.strip() or None,
            "experience_level": level,
            "timeline_months": months,
            "weekly_hours": hours,
        }

    return None

