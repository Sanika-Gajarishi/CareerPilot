import streamlit as st

from services.api import download_resume
from services.resume_service import remove_resume


def show_resume_card(resume):
    """
    Shows latest uploaded resume.
    """

    with st.container(border=True):

        st.markdown(f"## 📄 {resume['original_filename']}")
        st.caption(f"Uploaded: {resume['created_at']}")

        st.divider()

        # --------------------------------------------------
        # Buttons
        # --------------------------------------------------

        download_col, delete_col = st.columns(2)

        # ---------------- Download ----------------

        with download_col:

            try:

                token = st.session_state.get("token")

                file_bytes = download_resume(
                    resume["id"],
                    token,
                )

                st.download_button(
                    label="⬇ Download Resume",
                    data=file_bytes,
                    file_name=resume["original_filename"],
                    mime="application/octet-stream",
                    key=f"download_resume_{resume['id']}",
                    width="stretch",
                )

            except Exception as e:

                st.error(f"Download failed: {e}")

        # ---------------- Delete ----------------

        with delete_col:

            if st.button(
                "🗑 Delete Resume",
                key=f"delete_resume_{resume['id']}",
                width="stretch",
            ):

                try:

                    remove_resume(resume["id"])

                    st.toast("Resume deleted successfully ✅")

                    st.rerun()

                except Exception as e:

                    st.error(f"Delete failed: {e}")

