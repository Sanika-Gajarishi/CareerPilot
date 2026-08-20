import streamlit as st

from components.upload import resume_upload_widget
from components.resume_viewer import show_resume_card

from services.resume_service import (
    upload_resume_to_backend,
    fetch_resume_history,
    fetch_resume_details,
    remove_resume,
    get_resume_file,
)


def resume_page():

    st.title("📄 Resume Manager")
    st.write("Upload and manage your resumes.")

    st.divider()

    # ==========================================================
    # Upload Section
    # ==========================================================

    uploaded_file = resume_upload_widget()

    if uploaded_file:

        max_size = 10 * 1024 * 1024

        if uploaded_file.size > max_size:
            st.error("File size must be less than 10 MB.")

        else:

            if st.button(
                "Upload Resume",
                type="primary",
                width="stretch",
            ):

                try:

                    with st.spinner("Uploading and analyzing resume..."):
                        upload_resume_to_backend(uploaded_file)

                    st.toast("Resume uploaded successfully ✅")

                    st.rerun()

                except Exception as e:
                    st.error(str(e))

    st.divider()

    # ==========================================================
    # Resume History
    # ==========================================================

    try:
        resumes = fetch_resume_history()

    except Exception as e:
        st.error(str(e))
        return

    if not resumes:
        st.info("No resumes uploaded yet.")
        return

    # ==========================================================
    # Latest Resume
    # ==========================================================

    st.subheader("⭐ Latest Resume")

    latest_resume = fetch_resume_details(resumes[0]["id"])

    show_resume_card(latest_resume)

    st.divider()

    # ==========================================================
    # Previous Resumes
    # ==========================================================

    st.subheader("📚 Resume History")

    for resume in resumes:

        with st.container(border=True):

            col1, col2, col3, col4 = st.columns([5, 2, 2, 1])

            with col1:
                st.markdown(f"**{resume['original_filename']}**")

            with col2:
                st.caption(resume["created_at"])

            with col3:

                try:

                    file_bytes = get_resume_file(resume["id"])

                    st.download_button(
                        label="Open",
                        data=file_bytes,
                        file_name=resume["original_filename"],
                        mime="application/pdf",
                        key=f"download_{resume['id']}",
                        width="stretch",
                    )

                except Exception:
                    st.error("Unable to load file.")

            with col4:

                if st.button(
                    "Delete",
                    key=f"delete_{resume['id']}",
                    width="stretch",
                ):

                    try:

                        remove_resume(resume["id"])

                        st.toast("Resume deleted successfully 🗑️")

                        st.rerun()

                    except Exception as e:
                        st.error(str(e))