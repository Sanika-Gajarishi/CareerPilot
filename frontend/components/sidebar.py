import streamlit as st


def render_sidebar():

    with st.sidebar:

        st.title("CareerPilot AI")

        pages = [
            "Dashboard",
            "Resume",
            "Job Match",
            "ATS",
            "Roadmap",
            "Applications",
            "Interview",
            "Profile",
        ]

        icons = {
            "Dashboard": "🏠",
            "Resume": "📄",
            "Job Match": "🎯",
            "ATS": "📊",
            "Roadmap": "🛣️",
            "Applications": "💼",
            "Interview": "🎤",
            "Profile": "👤",
        }

        options = [f"{icons[p]}  {p}" for p in pages]

        selected = st.radio(
            "Navigation",
            options,
            label_visibility="collapsed",
        )

        return selected.split("  ", 1)[1]