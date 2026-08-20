from dataclasses import dataclass


@dataclass
class EvaluationResult:
    score: float
    strengths: list[str]
    improvements: list[str]


class InterviewEvaluator:

    @staticmethod
    def evaluate(
        question: str,
        answer: str,
    ) -> EvaluationResult:

        answer = answer.strip()

        if not answer:

            return EvaluationResult(
                score=0,
                strengths=[],
                improvements=[
                    "No answer provided."
                ],
            )

        score = 50

        strengths = []

        improvements = []

        word_count = len(answer.split())

        if word_count >= 20:
            score += 15
            strengths.append(
                "Provided a detailed response."
            )
        else:
            improvements.append(
                "Expand your answer with more detail."
            )

        if "." in answer:
            score += 10
            strengths.append(
                "Answer is well structured."
            )

        keywords = [
            "example",
            "because",
            "therefore",
            "experience",
        ]

        matches = sum(
            keyword.lower() in answer.lower()
            for keyword in keywords
        )

        score += matches * 5

        if matches:
            strengths.append(
                "Used reasoning/examples."
            )
        else:
            improvements.append(
                "Support your explanation with examples."
            )

        score = min(score, 100)

        return EvaluationResult(
            score=score,
            strengths=strengths,
            improvements=improvements,
        )