import streamlit as st

from utils.session import get_user


def render_navbar():

    user = get_user()

    col1, col2, col3 = st.columns([6, 2, 2])

    with col1:

        st.title("CareerPilot AI")

    with col2:

        st.text_input(
            "Search navigation",
            placeholder="Search...",
            label_visibility="collapsed",
        )

    with col3:

        if user:

            st.write(f"👋 {user['full_name']}")

    st.divider()