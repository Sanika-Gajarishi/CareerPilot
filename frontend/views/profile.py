import streamlit as st

from services.user_service import (
    delete_current_user,
    get_current_user,
    update_current_user,
)
from utils.session import logout


def profile_page():
    token = st.session_state.get("token")
    cached_user = st.session_state.get("current_user") or {}

    st.title("Profile")

    if not token:
        st.error("Please log in to view your profile.")
        return

    try:
        user = get_current_user(token)
        st.session_state["current_user"] = user
    except Exception as error:
        user = cached_user
        if not user:
            st.error(f"Could not load your profile: {error}")
            return
        st.warning("Showing your last loaded profile details.")

    st.caption("Manage your CareerPilot account")

    if st.button("Edit profile", type="primary"):
        st.session_state["editing_profile"] = True

    if st.session_state.get("editing_profile"):
        with st.form("profile_form"):
            full_name = st.text_input("Full name", value=user.get("full_name", ""))
            st.text_input("Email", value=user.get("email", ""), disabled=True)
            phone = st.text_input("Phone", value=user.get("phone", ""))
            github_url = st.text_input("GitHub", value=user.get("github_url", ""))
            linkedin_url = st.text_input("LinkedIn", value=user.get("linkedin_url", ""))
            save = st.form_submit_button("Save profile", type="primary")

        if save:
            if not full_name.strip():
                st.error("Full name is required.")
            else:
                try:
                    updated_user = update_current_user(
                        token,
                        {
                            "full_name": full_name,
                            "phone": phone,
                            "github_url": github_url,
                            "linkedin_url": linkedin_url,
                        },
                    )
                    st.session_state["current_user"] = updated_user
                    st.session_state["editing_profile"] = False
                    st.success("Profile saved.")
                    st.rerun()
                except Exception as error:
                    st.error(f"Could not save profile: {error}")
    else:
        with st.container(border=True):
            st.subheader(user.get("full_name", "CareerPilot user"))
            st.write(user.get("email", "Email unavailable"))
            st.write(f"Phone: {user.get('phone') or 'Not added'}")
            st.write(f"GitHub: {user.get('github_url') or 'Not added'}")
            st.write(f"LinkedIn: {user.get('linkedin_url') or 'Not added'}")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Account status", "Active" if user.get("is_active") else "Inactive")
            with col2:
                created_at = user.get("created_at")
                st.metric("Member since", str(created_at)[:10] if created_at else "Unavailable")

    st.divider()
    st.subheader("Delete account")
    st.caption("This permanently deletes your profile, resumes, roadmaps, interviews, and tracked jobs.")
    confirm_delete = st.checkbox("I understand this cannot be undone.")
    if st.button("Delete my account", type="secondary", disabled=not confirm_delete):
        try:
            delete_current_user(token)
            logout()
            st.rerun()
        except Exception as error:
            st.error(f"Could not delete account: {error}")