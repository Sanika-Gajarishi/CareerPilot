import streamlit as st

from components.roadmap.roadmap_form import roadmap_form
from services.learning_service import (
    delete_roadmap,
    generate_roadmap,
    get_roadmaps,
)


def roadmap_list():
    token = st.session_state.get("token")
    st.title("Roadmaps")

    if not token:
        st.error("Please log in to view your roadmaps.")
        return

    try:
        roadmaps = get_roadmaps(token)
    except Exception as error:
        st.error(str(error))
        return

    if not roadmaps:
        st.info("No roadmaps yet. Create one to get started.")
        st.session_state["show_roadmap_form"] = True
    elif st.button("Create Roadmap", use_container_width=True):
        st.session_state["show_roadmap_form"] = True

    if st.session_state.get("show_roadmap_form", False):
        data = roadmap_form()
        if data is not None:
            try:
                roadmap = generate_roadmap(data, token)
            except Exception as error:
                st.error(f"Could not generate roadmap: {error}")
            else:
                st.session_state["show_roadmap_form"] = False
                st.session_state["page"] = "roadmap_detail"
                st.session_state["selected_roadmap"] = roadmap.get("id")
                st.rerun()

    if not roadmaps:
        return

    for roadmap in roadmaps:
        with st.container():
            st.subheader(f"🎯 {roadmap['target_role']}")
            st.write(f"Timeline: {roadmap['timeline_months']} months")
            st.progress(roadmap.get("completion_percentage", 0) / 100)
            st.caption(roadmap.get("status", "In Progress"))
            if st.button(
                "Open",
                key=f"open_{roadmap['id']}",
                use_container_width=True,
            ):
                st.session_state["page"] = "roadmap_detail"
                st.session_state["selected_roadmap"] = roadmap["id"]
                st.rerun()
            if st.button(
                "Delete",
                key=f"delete_{roadmap['id']}",
                use_container_width=True,
            ):
                try:
                    delete_roadmap(roadmap["id"], token)
                except Exception as error:
                    st.error(f"Could not delete roadmap: {error}")
                else:
                    st.rerun()