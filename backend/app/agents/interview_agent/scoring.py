from statistics import mean


class InterviewScoreCalculator:

    @staticmethod
    def calculate(
        question_scores: list[float],
    ) -> dict:

        if not question_scores:

            return {
                "overall_score": 0,
                "grade": "Not Attempted",
                "recommendation": "Complete the interview to receive feedback.",
            }

        overall_score = round(
            mean(question_scores),
            2,
        )

        if overall_score >= 90:
            grade = "Excellent"
            recommendation = (
                "Interview Ready"
            )

        elif overall_score >= 75:
            grade = "Good"
            recommendation = (
                "Ready with Minor Improvements"
            )

        elif overall_score >= 60:
            grade = "Average"
            recommendation = (
                "Needs More Practice"
            )

        else:
            grade = "Needs Improvement"
            recommendation = (
                "Focus on fundamentals and practice more interviews."
            )

        return {
            "overall_score": overall_score,
            "grade": grade,
            "recommendation": recommendation,
        }