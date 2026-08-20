from app.agents.ats_agent.schemas import ATSResult


class ATSSummaryGenerator:

    @staticmethod
    def generate(result: ATSResult) -> str:

        score = result.overall_score

        if score >= 90:
            level = "excellent"
        elif score >= 80:
            level = "very strong"
        elif score >= 70:
            level = "strong"
        elif score >= 60:
            level = "average"
        else:
            level = "needs significant improvement"

        summary = []

        summary.append(
            f"This resume has an overall ATS score of {score}/100 and is {level} for automated screening."
        )

        if result.strengths:
            summary.append(
                "Major strengths include "
                + ", ".join(result.strengths).lower()
                + "."
            )

        if result.weaknesses:
            summary.append(
                "Areas that need improvement include "
                + ", ".join(result.weaknesses).lower()
                + "."
            )

        if result.recommendations:
            summary.append(
                "Recommended next steps: "
                + " ".join(result.recommendations)
            )

        return " ".join(summary)