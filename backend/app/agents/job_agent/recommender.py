from app.agents.job_agent.recommendation_schemas import (
    Recommendation,
    JobRecommendationResult,
)


class JobRecommendationEngine:

    @classmethod
    def generate(
        cls,
        missing_skills: list[str],
        critical_skills: list[str],
        important_skills: list[str],
        match_score: float,
        ats_score: float,
    ):

        recommendations = []

        # Critical skills
        for skill in critical_skills:

            recommendations.append(
                Recommendation(
                    category="Skill Gap",
                    priority="High",
                    title=f"Learn {skill}",
                    description=(
                        f"{skill} is an important requirement "
                        "for this position and is currently "
                        "missing from your resume."
                    ),
                    action=(
                        f"Learn {skill} and build a practical "
                        "project demonstrating it."
                    ),
                )
            )

        # Important skills
        for skill in important_skills:

            recommendations.append(
                Recommendation(
                    category="Skill Gap",
                    priority="Medium",
                    title=f"Improve {skill}",
                    description=(
                        f"{skill} appears relevant to the "
                        "job but is not currently demonstrated "
                        "in your resume."
                    ),
                    action=(
                        f"Practice {skill} and add evidence "
                        "of it to your portfolio."
                    ),
                )
            )

        # Resume recommendations
        if ats_score < 60:

            recommendations.append(
                Recommendation(
                    category="Resume",
                    priority="High",
                    title="Improve ATS compatibility",
                    description=(
                        "Your resume has a relatively low "
                        "ATS compatibility score."
                    ),
                    action=(
                        "Improve keywords, formatting, "
                        "sections, and measurable achievements."
                    ),
                )
            )

        elif ats_score < 80:

            recommendations.append(
                Recommendation(
                    category="Resume",
                    priority="Medium",
                    title="Optimize your resume",
                    description=(
                        "Your resume is reasonably strong "
                        "but still has opportunities for improvement."
                    ),
                    action=(
                        "Add job-specific keywords and "
                        "strengthen project and experience bullets."
                    ),
                )
            )

        # Match recommendations
        if match_score >= 85:

            application_advice = (
                "Excellent match. Your resume aligns strongly "
                "with this position. Applying is recommended."
            )

        elif match_score >= 70:

            application_advice = (
                "Strong match. You should consider applying "
                "while addressing the identified skill gaps."
            )

        elif match_score >= 55:

            application_advice = (
                "Moderate match. Consider improving the most "
                "important skill gaps before applying."
            )

        elif match_score >= 40:

            application_advice = (
                "Weak match. Significant gaps exist between "
                "your current profile and this position."
            )

        else:

            application_advice = (
                "Low match. This role currently has substantial "
                "requirements that are missing from your profile."
            )

        # Project recommendation
        if critical_skills:

            skills = ", ".join(
                critical_skills[:3]
            )

            recommendations.append(
                Recommendation(
                    category="Project",
                    priority="High",
                    title="Build a targeted project",
                    description=(
                        f"A project demonstrating {skills} "
                        "would strengthen your profile."
                    ),
                    action=(
                        "Build one production-style project "
                        "that combines the missing technologies."
                    ),
                )
            )

        return JobRecommendationResult(
            recommendations=recommendations,
            application_advice=application_advice,
        )