import streamlit as st


def initialize_session():
    """
    Initialize Streamlit session variables.
    """

    defaults = {
        "logged_in": False,
        "token": None,
        "current_user": None,
        "current_page": "Dashboard",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def login(token: str, user: dict):
    """
    Save login state.
    """

    st.session_state.logged_in = True
    st.session_state.token = token
    st.session_state.current_user = user


def logout():
    """
    Logout current user.
    """

    st.session_state.logged_in = False
    st.session_state.token = None
    st.session_state.current_user = None
    st.session_state.current_page = "Dashboard"


def is_logged_in():
    """
    Returns True if user is logged in.
    """

    return st.session_state.get("logged_in", False)


def get_token():
    return st.session_state.get("token")


def get_user():
    return st.session_state.get("current_user")