import re

from app.agents.ats_agent.resume_keywords import ResumeKeywords
from app.agents.ats_agent.schemas import KeywordAnalysis
from app.ats_data.technical_skills import TECHNICAL_SKILLS


class KeywordEngine:
    """
    Technical keyword matching engine.

    Responsibilities:
    1. Extract technical keywords from Job Description.
    2. Extract technical keywords from Resume.
    3. Compare both.
    4. Return matched, missing and extra skills.
    """

    @staticmethod
    def normalize(text: str) -> str:
        """
        Normalize text for keyword matching.
        """

        if not text:
            return ""

        text = text.lower()

        text = re.sub(r"[^\w\s+#.-]", " ", text)

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    @classmethod
    def extract_keywords(cls, text: str) -> set[str]:
        """
        Extract only known technical skills from text.
        """

        normalized = cls.normalize(text)

        found = set()

        for skill in TECHNICAL_SKILLS:

            if skill in normalized:
                found.add(skill)

        return found

    @classmethod
    def analyze(
        cls,
        resume,
        job_description: str,
    ) -> KeywordAnalysis:
        """
        Compare resume skills with Job Description.
        """

        resume_keywords = ResumeKeywords.extract(resume)

        jd_keywords = cls.extract_keywords(job_description)

        matched = sorted(
            resume_keywords.intersection(jd_keywords)
        )

        missing = sorted(
            jd_keywords.difference(resume_keywords)
        )

        extra = sorted(
            resume_keywords.difference(jd_keywords)
        )

        if len(jd_keywords) == 0:
            percentage = 0.0
        else:
            percentage = round(
                (len(matched) / len(jd_keywords)) * 100,
                2,
            )

        return KeywordAnalysis(
            matched=matched,
            missing=missing,
            extra=extra,
            match_percentage=percentage,
        )

    @classmethod
    def keyword_summary(
        cls,
        resume,
        job_description: str,
    ) -> dict:
        """
        Helper function for debugging and testing.
        """

        result = cls.analyze(resume, job_description)

        return {
            "matched": len(result.matched),
            "missing": len(result.missing),
            "extra": len(result.extra),
            "match_percentage": result.match_percentage,
        }