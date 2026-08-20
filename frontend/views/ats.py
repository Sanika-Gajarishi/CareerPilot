import json
import streamlit as st

from services.resume_service import get_resume_list
from services.ats_service import analyze_resume
from services.optimizer_service import optimize_resume


def ats_page():

    st.title("📄 ATS Resume Analyzer")

    token = st.session_state.get("token")

    # =====================================================
    # LOAD RESUMES
    # =====================================================

    try:

        resumes = get_resume_list(token)

    except Exception as e:

        st.error(str(e))
        return

    if not resumes:

        st.warning("Please upload a resume first.")
        return

    latest = resumes[0]

    st.subheader("Latest Resume")

    st.write(
        f"**Filename:** {latest['original_filename']}"
    )

    st.write(
        f"**Uploaded:** {latest['created_at']}"
    )

    st.divider()

    # =====================================================
    # ATS ANALYSIS
    # =====================================================

    if st.button(
        "🚀 Analyze Resume",
        width="stretch",
    ):

        with st.spinner(
            "Running ATS Analysis..."
        ):

            try:

                result = analyze_resume(
                    latest["id"],
                    token,
                )

                analysis = result["analysis"]

                # -------------------------------------------------
                # Cache Status
                # -------------------------------------------------

                if result.get("cached"):

                    st.info(
                        "⚡ Loaded cached ATS analysis."
                    )

                else:

                    st.success(
                        "✅ Fresh ATS analysis generated."
                    )

                st.divider()

                # -------------------------------------------------
                # Overall Score
                # -------------------------------------------------

                score = analysis["overall_score"]

                if score >= 90:
                    grade = "A+"

                elif score >= 80:
                    grade = "A"

                elif score >= 70:
                    grade = "B"

                elif score >= 60:
                    grade = "C"

                else:
                    grade = "D"

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Overall ATS Score",
                        f"{score}%",
                    )

                with col2:

                    st.metric(
                        "Grade",
                        grade,
                    )

                st.progress(
                    min(max(score / 100, 0), 1)
                )

                st.divider()

                # -------------------------------------------------
                # Section Scores
                # -------------------------------------------------

                st.subheader(
                    "📊 Section Scores"
                )

                for section in analysis.get(
                    "section_scores",
                    [],
                ):

                    st.write(
                        f"### {section['name']}"
                    )

                    max_score = section.get(
                        "max_score",
                        1,
                    )

                    section_score = section.get(
                        "score",
                        0,
                    )

                    percent = (
                        section_score / max_score
                        if max_score
                        else 0
                    )

                    st.progress(
                        min(max(percent, 0), 1)
                    )

                    st.write(
                        f"{section_score} / "
                        f"{max_score}"
                    )

                    suggestions = section.get(
                        "suggestions",
                        [],
                    )

                    for suggestion in suggestions:

                        st.caption(
                            f"• {suggestion}"
                        )

                st.divider()

                # -------------------------------------------------
                # Strengths
                # -------------------------------------------------

                st.subheader(
                    "✅ Strengths"
                )

                strengths = analysis.get(
                    "strengths",
                    [],
                )

                if strengths:

                    for item in strengths:

                        st.success(item)

                else:

                    st.info(
                        "No major strengths detected."
                    )

                # -------------------------------------------------
                # Weaknesses
                # -------------------------------------------------

                st.subheader(
                    "⚠ Weaknesses"
                )

                weaknesses = analysis.get(
                    "weaknesses",
                    [],
                )

                if weaknesses:

                    for item in weaknesses:

                        st.error(item)

                else:

                    st.success(
                        "No major weaknesses detected."
                    )

                st.divider()

                # -------------------------------------------------
                # Keyword Analysis
                # -------------------------------------------------

                keyword = analysis.get(
                    "keyword_analysis",
                    {},
                )

                st.subheader(
                    "🔑 Keyword Match"
                )

                c1, c2, c3 = st.columns(3)

                with c1:

                    st.metric(
                        "Match %",
                        f"{keyword.get('match_percentage', 0)}%",
                    )

                with c2:

                    st.metric(
                        "Matched",
                        len(
                            keyword.get(
                                "matched",
                                [],
                            )
                        ),
                    )

                with c3:

                    st.metric(
                        "Missing",
                        len(
                            keyword.get(
                                "missing",
                                [],
                            )
                        ),
                    )

                left, right = st.columns(2)

                with left:

                    st.write(
                        "### ✅ Matched Keywords"
                    )

                    matched = keyword.get(
                        "matched",
                        [],
                    )

                    if matched:

                        for k in matched:

                            st.success(k)

                    else:

                        st.info("None")

                with right:

                    st.write(
                        "### ⚠ Missing Keywords"
                    )

                    missing = keyword.get(
                        "missing",
                        [],
                    )

                    if missing:

                        for k in missing:

                            st.warning(k)

                    else:

                        st.success(
                            "No missing keywords"
                        )

                st.divider()

                # -------------------------------------------------
                # Formatting Analysis
                # -------------------------------------------------

                formatting = analysis.get(
                    "formatting_analysis",
                    {},
                )

                st.subheader(
                    "📄 Formatting"
                )

                formatting_score = formatting.get(
                    "score",
                    0,
                )

                formatting_max = formatting.get(
                    "max_score",
                    40,
                )

                st.metric(
                    "Formatting Score",
                    f"{formatting_score} / "
                    f"{formatting_max}",
                )

                if formatting_max:

                    st.progress(
                        min(
                            max(
                                formatting_score
                                / formatting_max,
                                0,
                            ),
                            1,
                        )
                    )

                for check in formatting.get(
                    "checks",
                    [],
                ):

                    icon = (
                        "✅"
                        if check.get("passed")
                        else "❌"
                    )

                    st.write(
                        f"{icon} "
                        f"**{check.get('name', 'Check')}**"
                    )

                    st.caption(
                        check.get(
                            "message",
                            "",
                        )
                    )

                st.divider()

                # -------------------------------------------------
                # Grammar Analysis
                # -------------------------------------------------

                grammar = analysis.get(
                    "grammar_analysis",
                    {},
                )

                st.subheader(
                    "✍ Grammar"
                )

                c1, c2 = st.columns(2)

                with c1:

                    st.metric(
                        "Grammar Score",
                        f"{grammar.get('score', 0)} / "
                        f"{grammar.get('max_score', 20)}",
                    )

                with c2:

                    st.metric(
                        "Grammar Issues",
                        grammar.get(
                            "total_issues",
                            0,
                        ),
                    )

                issues = grammar.get(
                    "issues",
                    [],
                )

                if issues:

                    st.write(
                        "### Grammar Suggestions"
                    )

                    for issue in issues[:10]:

                        with st.expander(
                            issue.get(
                                "message",
                                "Grammar Issue",
                            )
                        ):

                            if issue.get(
                                "sentence"
                            ):

                                st.write(
                                    issue["sentence"]
                                )

                            suggestions = issue.get(
                                "suggestions",
                                [],
                            )

                            if suggestions:

                                st.write(
                                    "Suggestions:"
                                )

                                for suggestion in suggestions:

                                    st.write(
                                        f"• {suggestion}"
                                    )

                else:

                    st.success(
                        "No grammar issues detected."
                    )

                st.divider()

                # -------------------------------------------------
                # Impact Analysis
                # -------------------------------------------------

                impact = analysis.get(
                    "impact_analysis",
                    {},
                )

                st.subheader(
                    "🚀 Project Impact"
                )

                impact_score = impact.get(
                    "score",
                    0,
                )

                impact_max = impact.get(
                    "max_score",
                    40,
                )

                st.metric(
                    "Impact Score",
                    f"{impact_score} / "
                    f"{impact_max}",
                )

                if impact_max:

                    st.progress(
                        min(
                            max(
                                impact_score
                                / impact_max,
                                0,
                            ),
                            1,
                        )
                    )

                for bullet in impact.get(
                    "bullets",
                    [],
                ):

                    bullet_text = bullet.get(
                        "bullet",
                        "",
                    )

                    if len(bullet_text) > 60:

                        title = (
                            bullet_text[:60]
                            + "..."
                        )

                    else:

                        title = bullet_text

                    with st.expander(
                        title
                    ):

                        st.metric(
                            "Bullet Score",
                            bullet.get(
                                "score",
                                0,
                            ),
                        )

                        st.write(
                            bullet_text
                        )

                        suggestions = bullet.get(
                            "suggestions",
                            [],
                        )

                        if suggestions:

                            st.write(
                                "### Suggestions"
                            )

                            for suggestion in suggestions:

                                st.warning(
                                    suggestion
                                )

                        else:

                            st.success(
                                "Excellent bullet point."
                            )

                st.divider()

                # -------------------------------------------------
                # Recommendations
                # -------------------------------------------------

                st.subheader(
                    "💡 Recommendations"
                )

                recommendations = analysis.get(
                    "recommendations",
                    [],
                )

                if recommendations:

                    for recommendation in recommendations:

                        st.info(
                            recommendation
                        )

                else:

                    st.success(
                        "No recommendations. Great job!"
                    )

                st.divider()

                # -------------------------------------------------
                # Download ATS Report
                # -------------------------------------------------

                st.download_button(
                    label="📥 Download ATS Report",
                    data=json.dumps(
                        analysis,
                        indent=4,
                    ),
                    file_name="ats_report.json",
                    mime="application/json",
                    width="stretch",
                )

            except Exception as e:

                st.exception(e)

    # =====================================================
    # AI RESUME OPTIMIZER
    # =====================================================

    st.divider()

    st.header(
        "🤖 AI Resume Optimizer"
    )

    st.write(
        "Improve your resume using "
        "AI-powered recommendations."
    )

    if st.button(
        "🚀 Optimize Resume",
        width="stretch",
    ):

        with st.spinner(
            "Optimizing Resume using AI..."
        ):

            try:

                # ---------------------------------------------
                # THIS WAS YOUR ERROR
                # ---------------------------------------------

                optimized = optimize_resume(
                    latest["id"],
                    token,
                )

                # ---------------------------------------------
                # Success
                # ---------------------------------------------

                st.success(
                    "✅ Resume Optimized Successfully!"
                )

                st.divider()

                # ---------------------------------------------
                # Professional Summary
                # ---------------------------------------------

                st.subheader(
                    "📄 Professional Summary"
                )

                with st.expander(
                    "View Improved Summary",
                    expanded=True,
                ):

                    summary = optimized.get(
                        "summary",
                        "",
                    )

                    st.write(summary)

                    st.code(
                        summary,
                        language="text",
                    )

                st.divider()

                # ---------------------------------------------
                # Skills
                # ---------------------------------------------

                st.subheader(
                    "🛠 Improved Skills"
                )

                skills = optimized.get(
                    "skills",
                    [],
                )

                with st.expander(
                    "View Skills",
                    expanded=True,
                ):

                    if skills:

                        for skill in skills:

                            st.success(skill)

                    else:

                        st.info(
                            "No improved skills returned."
                        )

                st.divider()

                # ---------------------------------------------
                # Experience
                # ---------------------------------------------

                st.subheader(
                    "💼 Improved Experience"
                )

                experience = optimized.get(
                    "experience",
                    [],
                )

                with st.expander(
                    "View Experience",
                    expanded=True,
                ):

                    if experience:

                        for exp in experience:

                            st.write(
                                "• " + exp
                            )

                    else:

                        st.info(
                            "No improved experience returned."
                        )

                st.divider()

                # ---------------------------------------------
                # Projects
                # ---------------------------------------------

                st.subheader(
                    "🚀 Improved Projects"
                )

                projects = optimized.get(
                    "projects",
                    [],
                )

                with st.expander(
                    "View Projects",
                    expanded=True,
                ):

                    if projects:

                        for project in projects:

                            st.write(
                                "• " + project
                            )

                    else:

                        st.info(
                            "No improved projects returned."
                        )

                st.divider()

                # ---------------------------------------------
                # AI Recommendations
                # ---------------------------------------------

                st.subheader(
                    "💡 AI Recommendations"
                )

                recommendations = optimized.get(
                    "recommendations",
                    [],
                )

                with st.expander(
                    "View Recommendations",
                    expanded=True,
                ):

                    if recommendations:

                        for rec in recommendations:

                            st.success(rec)

                    else:

                        st.info(
                            "No additional recommendations."
                        )

                st.divider()

                # ---------------------------------------------
                # Download Optimized Resume
                # ---------------------------------------------

                download_text = f"""
PROFESSIONAL SUMMARY

{summary}

======================================

SKILLS

{chr(10).join(skills)}

======================================

EXPERIENCE

{chr(10).join(experience)}

======================================

PROJECTS

{chr(10).join(projects)}

======================================

RECOMMENDATIONS

{chr(10).join(recommendations)}
"""

                st.download_button(
                    label="📥 Download Optimized Resume",
                    data=download_text,
                    file_name="optimized_resume.txt",
                    mime="text/plain",
                    width="stretch",
                )

            except Exception as e:

                st.exception(e)