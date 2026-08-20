import json
import re

import google.generativeai as genai

from app.core.config import settings
from app.agents.interview_agent.schemas import (
    InterviewQuestion,
    InterviewQuestionSet,
)

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


class InterviewGenerator:

    @staticmethod
    def generate(
        target_role: str,
        company: str,
        difficulty: str,
        interview_type: str,
    ) -> InterviewQuestionSet:

        prompt = f"""
You are a Senior Technical Interviewer.

Generate EXACTLY 10 interview questions.

Role:
{target_role}

Company:
{company}

Difficulty:
{difficulty}

Interview Type:
{interview_type}

Rules:

If interview type is Technical:

• ONLY technical questions.

• Around 6 coding questions.

• Around 4 theory questions.

Coding questions should include:

- Python
- DSA
- SQL (if applicable)
- APIs
- OOP
- System Design (for senior roles)

Theory questions should match the role.

------------------------------------

If interview type is HR:

ONLY HR and Behavioral questions.

Examples:

Tell me about yourself.

Why do you want to join {company}?

Strengths

Weaknesses

Leadership

Conflict Resolution

Career Goals

------------------------------------

If interview type is Mixed:

70% Technical

30% HR

------------------------------------

Difficulty:

Easy:
Freshers

Medium:
1-3 Years

Hard:
FAANG Level

------------------------------------

Return ONLY JSON.

Example:

{{
"questions":[
{{
"question_number":1,
"category":"Python",
"difficulty":"Medium",
"question":"Explain list comprehension."
}}
]
}}

Do not include markdown.
"""

        response = model.generate_content(prompt)

        text = response.text.strip()

        text = re.sub(
            r"^```json",
            "",
            text,
            flags=re.IGNORECASE,
        )

        text = re.sub(
            r"```$",
            "",
            text,
        )

        data = json.loads(text)

        questions = []

        for item in data["questions"]:

            questions.append(

                InterviewQuestion(
                    question_number=item["question_number"],
                    category=item["category"],
                    difficulty=item["difficulty"],
                    question=item["question"],
                )

            )

        return InterviewQuestionSet(
            questions=questions
        )