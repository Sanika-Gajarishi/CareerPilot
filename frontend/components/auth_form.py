import streamlit as st


def login_form():

    st.markdown(
        """
        <h1 style='text-align:center;'>
            CareerPilot AI
        </h1>

        <p style='text-align:center;color:gray'>
            AI Powered Career Mentor
        </p>
        """,
        unsafe_allow_html=True,
    )

    with st.form("login_form"):

        email = st.text_input(
            "Email",
            placeholder="Enter Email",
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter Password",
        )

        submitted = st.form_submit_button(
            "Login",
            width="stretch",
        )

    return submitted, email, password