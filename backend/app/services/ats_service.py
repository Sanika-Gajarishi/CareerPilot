import json
import google.generativeai as genai

from app.core.config import settings


genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


class ATSService:

    @staticmethod
    def analyze_resume(resume_text: str):

        prompt = f"""
You are an ATS Resume Expert.

Analyze the resume below.

Return ONLY valid JSON.

Schema:

{{
    "ats_score": 0,
    "summary": "",
    "strengths": [],
    "weaknesses": [],
    "missing_keywords": [],
    "recommendations": []
}}

Resume:

{resume_text}
"""

        response = model.generate_content(prompt)

        return json.loads(response.text)