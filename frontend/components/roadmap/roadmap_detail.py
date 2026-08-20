import streamlit as st

from services.learning_service import get_roadmap, update_roadmap_progress


def _persist_progress(roadmap_id, task_keys, token):
    completed = sum(
        bool(st.session_state.get(key, False)) for key in task_keys
    )
    progress = round((completed / len(task_keys)) * 100, 2) if task_keys else 0
    try:
        update_roadmap_progress(roadmap_id, progress, token)
    except Exception as error:
        st.session_state["roadmap_progress_error"] = str(error)


def roadmap_detail_page(roadmap_id):

    token = st.session_state.get("token")

    if not token or roadmap_id is None:
        st.error("Select a roadmap to view its details.")
        if st.button("Back to Roadmaps"):
            st.session_state["page"] = "Roadmap"
            st.rerun()
        return

    try:
        roadmap = get_roadmap(roadmap_id, token)
    except Exception as error:
        st.error(f"Could not load roadmap: {error}")
        if st.button("Back to Roadmaps"):
            st.session_state["page"] = "Roadmap"
            st.rerun()
        return

    st.title("🗺 Career Roadmap")

    if st.button("⬅ Back to Roadmaps"):
        st.session_state["page"] = "Roadmap"
        st.rerun()

    st.subheader(roadmap.get("target_role", "Career Roadmap"))

    col1, col2, col3 = st.columns(3)

    try:
        progress = float(roadmap.get("completion_percentage") or 0)
    except (TypeError, ValueError):
        progress = 0

    with col1:
        st.metric(
            "Timeline",
            f'{roadmap.get("timeline_months", "-")} Months',
        )

    with col2:
        st.metric(
            "Progress",
            f"{progress:.0f}%",
        )

    with col3:
        st.metric(
            "Status",
            roadmap.get(
                "status",
                "In Progress",
            ),
        )

    # --------------------------------------------------
    # Overall Progress
    # --------------------------------------------------

    total_tasks = 0
    completed_tasks = 0

    roadmap_data = roadmap.get("roadmap") or {}
    monthly_plan = roadmap_data.get("monthly_plan") or []
    task_keys = []

    for month in monthly_plan:

        for task in month.get("weekly_tasks") or []:

            total_tasks += 1

            key = (
                f'roadmap_{roadmap_id}_'
                f'{month.get("month", 0)}_'
                f'{task.get("week", 0)}'
            )
            task_keys.append(key)

            if st.session_state.get(key, False):
                completed_tasks += 1

    if total_tasks:

        overall_progress = (
            completed_tasks / total_tasks
        )

        st.progress(min(max(overall_progress, 0), 1))

        st.success(
            f"{completed_tasks}/{total_tasks} Tasks Completed"
        )

    if st.session_state.pop("roadmap_progress_error", None):
        st.error("Progress could not be saved. Please try again.")

    st.divider()

    # --------------------------------------------------
    # Monthly Plan
    # --------------------------------------------------

    st.header("📅 Monthly Plan")

    for month in monthly_plan:

        weekly_tasks = month.get("weekly_tasks") or []
        total = len(weekly_tasks)

        done = 0

        for task in weekly_tasks:

            key = (
                f'roadmap_{roadmap_id}_'
                f'{month.get("month", 0)}_'
                f'{task.get("week", 0)}'
            )

            if st.session_state.get(key, False):
                done += 1

        icon = "✅" if total > 0 and done == total else "📘"

        with st.expander(
            f"{icon} Month {month.get('month', '?')} • {month.get('title', 'Untitled')}",
            expanded=False,
        ):

            st.markdown(
                f"### 🎯 Objective\n{month.get('objective', 'No objective provided.')}"
            )

            # ---------------- Skills ----------------

            st.markdown("### 🛠 Skills")

            cols = st.columns(3)

            for i, skill in enumerate(month.get("skills") or []):

                cols[i % 3].success(skill)

            st.divider()

            # ---------------- Weekly Tasks ----------------

            st.markdown("### ✅ Weekly Tasks")

            completed = 0

            for task in weekly_tasks:

                key = (
                    f'roadmap_{roadmap_id}_'
                    f'{month.get("month", 0)}_'
                    f'{task.get("week", 0)}'
                )

                checked = st.checkbox(
                    f'Week {task.get("week", "?")} • {task.get("title", "Untitled")}',
                    key=key,
                    on_change=_persist_progress,
                    args=(roadmap_id, task_keys, token),
                )

                if checked:
                    completed += 1

                st.caption(task.get("description", ""))

                st.caption(
                    f'⏱ Estimated Hours: {task.get("estimated_hours", 0)}'
                )

                st.divider()

            if total:

                percentage = completed / total

                st.progress(percentage)

                st.info(
                    f"{completed}/{total} Weekly Tasks Completed"
                )

            # ---------------- Projects ----------------

            st.markdown("### 🚀 Project")

            for project in month.get("projects") or []:

                st.info(project)

    # --------------------------------------------------
    # Recommended Projects
    # --------------------------------------------------

    st.divider()

    st.header("🚀 Recommended Projects")

    for project in roadmap_data.get("recommended_projects") or []:

        with st.container():

            st.subheader(project.get("title", "Untitled project"))

            c1, c2 = st.columns(2)

            with c1:

                st.write(
                    f"**Difficulty:** {project.get('difficulty', 'Not specified')}"
                )

            with c2:

                st.write(
                    f"**Duration:** {project.get('duration_weeks', '?')} weeks"
                )

            st.write(project.get("description", "No description provided."))

            st.write("### Skills")

            cols = st.columns(3)

            for i, skill in enumerate(project.get("skills") or []):

                cols[i % 3].success(skill)

            st.divider()

    # --------------------------------------------------
    # Learning Resources
    # --------------------------------------------------

    st.header("📚 Learning Resources")

    for resource in roadmap_data.get("learning_resources") or []:

        with st.container():

            st.subheader(resource.get("title", "Untitled resource"))

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    f"**Platform:** {resource.get('platform', 'Not specified')}"
                )

                st.write(
                    f"**Difficulty:** {resource.get('difficulty', 'Not specified')}"
                )

            with col2:

                st.write(
                    f"**Type:** {resource.get('resource_type', 'Not specified')}"
                )

                st.write(
                    f"**Estimated Hours:** {resource.get('estimated_hours', 0)}"
                )

            resource_url = resource.get("url")
            if resource_url:
                st.link_button("Open Resource", resource_url)

            st.divider()