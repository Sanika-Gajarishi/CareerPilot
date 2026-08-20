import json
import re

import google.generativeai as genai

from app.agents.interview_agent.evaluator import (
    EvaluationResult,
)
from app.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")


class InterviewFeedbackGenerator:

    @staticmethod
    def generate(
        question: str,
        answer: str,
        evaluation: EvaluationResult,
    ) -> dict:

        score = evaluation.score

        if score >= 90:

            overall = (
                "Excellent answer. Your response is well-structured, technically accurate, and interview-ready."
            )

        elif score >= 75:

            overall = (
                "Good answer. You demonstrated solid understanding with only minor improvements needed."
            )

        elif score >= 60:

            overall = (
                "Average answer. You understand the topic but should provide more depth and examples."
            )

        else:

            overall = (
                "Your answer needs improvement. Focus on explaining concepts clearly and using practical examples."
            )

        fallback = {
            "interviewer_feedback": overall,
            "interviewer_expectations": [
                "Define the main concept clearly.",
                "Explain the reasoning behind your answer.",
                "Include one practical example.",
                "Close with a concise comparison or conclusion.",
            ],
            "missing": evaluation.improvements,
            "ideal_answer": (
                "A strong answer should define the concept, explain its key tradeoffs, "
                "and support the explanation with a practical example."
            ),
            "tips": [
                "Speak confidently and structure your answer.",
                "Keep the answer focused and under two minutes.",
                "Mention one real-world example.",
            ],
        }

        try:
            prompt = f"""
You are an expert technical interviewer. Evaluate the candidate answer below.
Question: {question}
Candidate answer: {answer}

Return only valid JSON with these keys:
interviewer_feedback (string), interviewer_expectations (array of 3-5 strings),
missing (array of strings), ideal_answer (string), tips (array of 2-4 strings).
The ideal answer must teach the candidate without referring to this instruction.
"""
            response = model.generate_content(prompt)
            text = re.sub(r"^```(?:json)?|```$", "", response.text.strip(), flags=re.IGNORECASE).strip()
            generated = json.loads(text)
            if not all(key in generated for key in fallback):
                raise ValueError("Incomplete feedback response")
            return generated
        except Exception:
            return fallback