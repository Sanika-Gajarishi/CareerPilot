import re

from app.ats_data.action_verbs import ACTION_VERBS
from app.ats_data.technical_skills import TECHNICAL_SKILLS
from app.agents.ats_agent.schemas import (
    ImpactAnalysis,
    ImpactFeedback,
)


class ImpactAnalyzer:

    @classmethod
    def analyze(cls, resume):

        feedback = []
        total_score = 0
        bullet_points = []

        # ----------------------------------
        # Experience Bullet Points
        # description is list[str]
        # ----------------------------------
        for exp in resume.experience:
            if exp.description:
                bullet_points.extend(exp.description)

        # ----------------------------------
        # Project Description
        # description is str
        # ----------------------------------
        for project in resume.projects:
            if project.description:
                bullet_points.append(project.description)

        # ----------------------------------
        # Analyze each bullet
        # ----------------------------------
        for bullet in bullet_points:

            score = 0
            suggestions = []

            bullet = bullet.strip()

            if not bullet:
                continue

            lower = bullet.lower()

            # ----------------------------
            # Action Verb
            # ----------------------------
            if any(lower.startswith(v.lower()) for v in ACTION_VERBS):
                score += 10
            else:
                suggestions.append(
                    "Start the sentence with a strong action verb."
                )

            # ----------------------------
            # Numbers / Metrics
            # ----------------------------
            if re.search(r"\d+[%+]?", bullet):
                score += 10
            else:
                suggestions.append(
                    "Include measurable achievements or numbers."
                )

            # ----------------------------
            # Technical Skills
            # ----------------------------
            if any(skill.lower() in lower for skill in TECHNICAL_SKILLS):
                score += 10
            else:
                suggestions.append(
                    "Mention relevant technologies or tools."
                )

            # ----------------------------
            # Length
            # ----------------------------
            words = len(bullet.split())

            if 12 <= words <= 35:
                score += 5
            else:
                suggestions.append(
                    "Keep the sentence between 12 and 35 words."
                )

            # ----------------------------
            # Bonus
            # ----------------------------
            if score >= 25:
                score += 5

            total_score += score

            feedback.append(
                ImpactFeedback(
                    bullet=bullet,
                    score=score,
                    suggestions=suggestions,
                )
            )

        # ----------------------------------
        # Final Score
        # ----------------------------------
        if feedback:
            average_score = round(total_score / len(feedback))
        else:
            average_score = 0

        return ImpactAnalysis(
            score=average_score,
            bullets=feedback,
        )