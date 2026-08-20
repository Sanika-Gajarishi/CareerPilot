import streamlit as st


def resume_upload_widget():
    """
    Resume Upload Component

    Returns:
        uploaded_file or None
    """

    st.subheader("📄 Upload Resume")

    st.caption(
        "Supported formats: PDF, DOCX (Max 10 MB)"
    )

    uploaded_file = st.file_uploader(
        label="Choose Resume",
        type=["pdf", "docx"],
        accept_multiple_files=False,
        label_visibility="collapsed",
    )

    return uploaded_file