import streamlit as st

from services.resume_service import get_resume_list
from services.job_service import analyze_job_match


def _bounded_score(value):
    return min(max(float(value or 0), 0), 100)


def _score_tone(value):
    value = _bounded_score(value)
    if value >= 80:
        return "good"
    if value >= 55:
        return "steady"
    return "needs-work"


def _skill_chips(skills, class_name="skill-chip"):
    if not skills:
        return '<span class="muted-copy">None detected</span>'
    return "".join(
        f'<span class="{class_name}">{skill}</span>'
        for skill in skills
    )


def _render_score_card(label, value, weight):
    value = _bounded_score(value)
    contribution = value * weight
    st.markdown(
        f"""
        <div class="score-card">
            <div class="score-card__top">
                <span>{label}</span>
                <strong>{value:g}%</strong>
            </div>
            <div class="score-track"><span class="score-fill { _score_tone(value) }" style="width:{value}%"></span></div>
            <small>Weight {weight:.0%} <b>·</b> contributes {contribution:.1f} points</small>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_gap_group(title, subtitle, gaps, tone):
    st.markdown(
        f'<div class="gap-group gap-group--{tone}"><div class="gap-group__heading"><div><h4>{title}</h4><p>{subtitle}</p></div><span class="count-badge">{len(gaps)}</span></div>',
        unsafe_allow_html=True,
    )
    if gaps:
        for gap in gaps:
            st.markdown(
                f'<div class="gap-row"><span>{gap.get("skill", "")}</span><small>{gap.get("category", "Other")}</small></div>',
                unsafe_allow_html=True,
            )
    else:
        st.markdown('<p class="muted-copy">No gaps in this tier.</p>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def show_results(result):
    score = _bounded_score(result.get("overall_score"))
    breakdown = result.get("breakdown") or {}
    matched = result.get("matched_skills") or []
    missing = result.get("missing_skills") or []

    st.divider()
    st.subheader("Match summary")
    score_col, level_col = st.columns([1, 2])
    with score_col:
        st.metric("Overall match", f"{score:g}%")
    with level_col:
        st.markdown(f"### {result.get('match_level', 'Match analysis')}")
        explanations = result.get("explanation") or []
        st.write(explanations[0] if explanations else "Your resume was compared with the job description.")
    st.progress(score / 100)

    st.subheader("All sections")
    sections = [
        ("Skills", breakdown.get("skill_match")),
        ("ATS readiness", breakdown.get("ats_score")),
        ("Experience", breakdown.get("experience_match")),
        ("Education", breakdown.get("education_match")),
        ("Keywords", breakdown.get("keyword_coverage")),
    ]
    for label, value in sections:
        section_score = _bounded_score(value)
        left, right = st.columns([2, 5])
        with left:
            st.write(f"**{label}**")
        with right:
            st.progress(section_score / 100, text=f"{section_score:g}%")

    st.subheader("Skills comparison")
    matched_col, missing_col = st.columns(2)
    with matched_col:
        st.markdown(f"**Matched ({len(matched)})**")
        if matched:
            for skill in matched:
                st.success(skill)
        else:
            st.caption("No matching skills detected.")
    with missing_col:
        st.markdown(f"**Missing ({len(missing)})**")
        if missing:
            for skill in missing:
                st.warning(skill)
        else:
            st.caption("No missing skills detected.")

    recommendations_data = result.get("recommendations") or {}
    recommendations = recommendations_data.get("recommendations") or []
    if recommendations:
        st.subheader("What to improve")
        for recommendation in recommendations:
            title = recommendation.get("title", "Recommendation")
            action = recommendation.get("action") or recommendation.get("description", "")
            st.write(f"**{title}:** {action}")

    advice = recommendations_data.get("application_advice")
    if advice:
        st.info(advice)


def job_match_page():

    st.title("🎯 Job Match Analyzer")

    token = st.session_state.get("token")

    try:
        resumes = get_resume_list(token)
    except Exception as error:
        st.error(f"Could not load your resumes: {error}")
        return

    if not resumes:
        st.warning("Upload a resume first.")
        return

    latest = resumes[0]

    st.success(
        f"Using Resume: {latest['original_filename']}"
    )

    job_description = st.text_area(
        "Paste Job Description",
        height=300,
    )

    if st.button(
        "Analyze Job Match",
        width="stretch",
    ):

        if not job_description.strip():

            st.error(
                "Paste a Job Description."
            )

            return

        with st.spinner("Analyzing Resume..."):

            try:
                result = analyze_job_match(
                    latest["id"],
                    job_description,
                    token,
                )
            except Exception as error:
                st.error(f"Could not analyze this job: {error}")
                return

            st.session_state["job_match_result"] = result

            st.rerun()

    if "job_match_result" in st.session_state:

        show_results(
            st.session_state["job_match_result"]
        )