import json
import re

import google.generativeai as genai

from app.core.config import settings


# ---------------------------------------------------------
# Gemini Configuration
# ---------------------------------------------------------

genai.configure(
    api_key=settings.GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


class ResumeOptimizerService:

    @staticmethod
    def optimize(resume_text: str):

        if not resume_text or not resume_text.strip():
            raise ValueError(
                "Resume text is empty."
            )

        # -------------------------------------------------
        # Prompt
        # -------------------------------------------------

        prompt = """
You are an expert ATS resume optimizer and professional resume writer.

Your task is to improve the provided resume while preserving the
candidate's REAL information.

IMPORTANT RULES:

1. Do not invent companies.
2. Do not invent job titles.
3. Do not invent education.
4. Do not invent certifications.
5. Do not invent technologies that are not supported by the resume.
6. Do not invent achievements.
7. Do not invent numbers.
8. Improve grammar and professional wording.
9. Use strong action verbs.
10. Make project and experience bullets ATS friendly.
11. Preserve the original meaning.
12. Add measurable language only when the resume already provides
    enough information to support it.
13. Return ONLY valid JSON.
14. Do NOT use Markdown.
15. Do NOT use ```json.
16. Do NOT add explanations outside the JSON.

Return exactly this JSON structure:

{
    "summary": "Improved professional summary",
    "skills": [
        "skill 1",
        "skill 2"
    ],
    "experience": [
        "Improved experience bullet 1",
        "Improved experience bullet 2"
    ],
    "projects": [
        "Improved project bullet 1",
        "Improved project bullet 2"
    ],
    "recommendations": [
        "Recommendation 1",
        "Recommendation 2"
    ]
}

Resume:

""" + resume_text

        # -------------------------------------------------
        # Gemini Request
        # -------------------------------------------------

        response = model.generate_content(prompt)

        if not response or not response.text:
            raise ValueError(
                "Gemini returned an empty response."
            )

        raw_response = response.text.strip()

        # -------------------------------------------------
        # Remove Markdown Code Fence
        # -------------------------------------------------

        raw_response = re.sub(
            r"^```json\s*",
            "",
            raw_response,
            flags=re.IGNORECASE,
        )

        raw_response = re.sub(
            r"^```\s*",
            "",
            raw_response,
        )

        raw_response = re.sub(
            r"\s*```$",
            "",
            raw_response,
        )

        raw_response = raw_response.strip()

        # -------------------------------------------------
        # Parse JSON
        # -------------------------------------------------

        try:

            result = json.loads(
                raw_response
            )

        except json.JSONDecodeError as e:

            raise ValueError(
                "AI returned invalid JSON. "
                f"Parser error: {str(e)}"
            )

        # -------------------------------------------------
        # Validate Structure
        # -------------------------------------------------

        if not isinstance(result, dict):
            raise ValueError(
                "Optimizer response must be a JSON object."
            )

        result.setdefault(
            "summary",
            "",
        )

        result.setdefault(
            "skills",
            [],
        )

        result.setdefault(
            "experience",
            [],
        )

        result.setdefault(
            "projects",
            [],
        )

        result.setdefault(
            "recommendations",
            [],
        )

        # Ensure correct types

        if not isinstance(
            result["summary"],
            str,
        ):
            result["summary"] = str(
                result["summary"]
            )

        for field in [
            "skills",
            "experience",
            "projects",
            "recommendations",
        ]:

            if not isinstance(
                result[field],
                list,
            ):
                result[field] = []

        return result