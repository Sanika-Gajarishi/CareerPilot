import streamlit as st


def roadmap_card(roadmap):

    st.subheader(
        f"🎯 {roadmap['target_role']}"
    )

    st.write(
        f"Timeline : {roadmap['timeline_months']} Months"
    )

    st.progress(
        roadmap["completion_percentage"] / 100
    )

    st.caption(
        roadmap["status"]
    )