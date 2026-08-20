import streamlit as st
from pathlib import Path

from utils.session import (
    initialize_session,
    is_logged_in,
)

from views.login import show_login

from components.sidebar import render_sidebar
from components.navbar import render_navbar
from components.roadmap.roadmap_detail import roadmap_detail_page
from views.dashboard import dashboard_page
from views.resume import resume_page
from views.job_match import job_match_page
from views.ats import ats_page
from views.roadmap import roadmap_page
from views.applications import applications_page
from views.interview import interview_page
from views.profile import profile_page


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------
# INITIALIZE SESSION
# ---------------------------------------------------

initialize_session()

# ---------------------------------------------------
# LOAD CSS
# ---------------------------------------------------

css = Path(__file__).parent / "assets" / "style.css"

if css.exists():
    with open(css, encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )

# ---------------------------------------------------
# LOGIN GATE
# ---------------------------------------------------

if not is_logged_in():
    show_login()
    st.stop()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

page = render_sidebar()

# ---------------------------------------------------
# NAVBAR
# ---------------------------------------------------

render_navbar()

st.markdown(
    "<div style='margin-top:20px'></div>",
    unsafe_allow_html=True,
)


# ---------------------------------------------------
# PAGE ROUTER
# ---------------------------------------------------

# ---------------------------------------------------
# PAGE ROUTER
# ---------------------------------------------------

PAGE_ROUTES = {
    "Dashboard": dashboard_page,
    "Resume": resume_page,
    "Job Match": job_match_page,
    "ATS": ats_page,
    "Roadmap": roadmap_page,
    "Applications": applications_page,
    "Interview": interview_page,
    "Profile": profile_page,
}

# Special page for roadmap details
if st.session_state.get("page") == "roadmap_detail":

    roadmap_detail_page(
        st.session_state.get("selected_roadmap")
    )

else:

    if page in PAGE_ROUTES:
        PAGE_ROUTES[page]()
    else:
        st.error(f"Unknown page: {page}")