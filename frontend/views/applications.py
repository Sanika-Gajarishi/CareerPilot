from datetime import date, datetime

import streamlit as st

from services.application_service import (
    create_application,
    delete_application,
    get_applications,
    update_application,
)
from utils.session import get_token


STATUSES = ["Saved", "Applied", "Interview", "Offer", "Rejected"]


def _as_date(value):
    if not value:
        return None
    if isinstance(value, date):
        return value
    try:
        return datetime.fromisoformat(value).date()
    except (TypeError, ValueError):
        return None


def _application_form(application=None, form_key="application_form"):
    application = application or {}
    current_status = application.get("status", "Saved")
    if current_status not in STATUSES:
        current_status = "Saved"

    with st.form(form_key):
        col1, col2 = st.columns(2)
        with col1:
            company = st.text_input("Company", value=application.get("company", ""))
            job_title = st.text_input("Job title", value=application.get("job_title", ""))
            location = st.text_input("Location", value=application.get("location", ""))
            salary = st.text_input("Salary", value=application.get("salary", ""))
        with col2:
            status = st.selectbox(
                "Status",
                STATUSES,
                index=STATUSES.index(current_status),
            )
            application_url = st.text_input(
                "Application URL",
                value=application.get("application_url", ""),
            )
            applied_date = st.date_input(
                "Applied date",
                value=_as_date(application.get("applied_date")),
            )
            interview_date = st.date_input(
                "Interview date",
                value=_as_date(application.get("interview_date")),
            )
            follow_up_date = st.date_input(
                "Follow-up date",
                value=_as_date(application.get("follow_up_date")),
            )

        notes = st.text_area("Notes", value=application.get("notes", ""))
        submitted = st.form_submit_button(
            "Save application" if application else "Add application",
            type="primary",
            width="stretch",
        )

    if not submitted:
        return None

    if not company.strip() or not job_title.strip():
        st.error("Company and job title are required.")
        return None

    return {
        "company": company.strip(),
        "job_title": job_title.strip(),
        "location": location.strip() or None,
        "application_url": application_url.strip() or None,
        "salary": salary.strip() or None,
        "status": status,
        "notes": notes.strip() or None,
        "applied_date": applied_date,
        "interview_date": interview_date,
        "follow_up_date": follow_up_date,
    }


def applications_page():
    st.title("Applications")
    st.caption("Track every opportunity from saved job to offer.")

    token = get_token()
    if not token:
        st.error("Please log in to manage applications.")
        return

    try:
        applications = get_applications(token)
    except Exception as error:
        st.error(f"Could not load applications: {error}")
        return

    status_filter = st.selectbox("Filter by status", ["All"] + STATUSES)
    visible_applications = [
        application
        for application in applications
        if status_filter == "All" or application.get("status") == status_filter
    ]

    metric_columns = st.columns(4)
    metrics = [
        ("Total", len(applications)),
        ("Applied", sum(item.get("status") == "Applied" for item in applications)),
        ("Interviews", sum(item.get("status") == "Interview" for item in applications)),
        ("Offers", sum(item.get("status") == "Offer" for item in applications)),
    ]
    for column, (label, value) in zip(metric_columns, metrics):
        with column:
            st.metric(label, value)

    st.divider()
    with st.expander("Add application", expanded=not applications):
        new_application = _application_form()
        if new_application:
            try:
                create_application(new_application, token)
                st.success("Application added.")
                st.rerun()
            except Exception as error:
                st.error(f"Could not add application: {error}")

    st.subheader(f"Your applications ({len(visible_applications)})")
    if not visible_applications:
        st.info("No applications match this filter yet.")
        return

    for application in visible_applications:
        application_id = application["id"]
        title = f"{application.get('job_title', 'Untitled role')} · {application.get('company', 'Unknown company')}"
        action_col, details_col = st.columns([1, 7])
        with action_col:
            delete_confirmed = st.checkbox(
                "Confirm",
                key=f"confirm_delete_application_{application_id}",
                label_visibility="collapsed",
            )
            if st.button(
                "Delete",
                key=f"delete_application_{application_id}",
                type="secondary",
                disabled=not delete_confirmed,
                use_container_width=True,
            ):
                try:
                    delete_application(application_id, token)
                    st.success("Application deleted.")
                    st.rerun()
                except Exception as error:
                    st.error(f"Could not delete application: {error}")

        with details_col:
            st.markdown(f"**{title}**")
        with st.expander(title):
            edited_application = _application_form(
                application,
                form_key=f"edit_application_{application_id}",
            )
            if edited_application:
                try:
                    update_application(application_id, edited_application, token)
                    st.success("Application updated.")
                    st.rerun()
                except Exception as error:
                    st.error(f"Could not update application: {error}")

            if application.get("application_url"):
                st.link_button("Open application", application["application_url"])
