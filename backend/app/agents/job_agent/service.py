from app.agents.job_agent.parser import JobParser
from app.agents.job_agent.matcher import JobMatcher
from app.agents.job_agent.gap_analyzer import SkillGapAnalyzer
from app.agents.job_agent.experience_matcher import ExperienceMatcher
from app.agents.job_agent.education_matcher import EducationMatcher
from app.agents.job_agent.scorer import JobMatchScorer
from app.agents.job_agent.recommender import JobRecommendationEngine

from app.agents.resume_agent.schemas import ResumeData


class JobAnalyzer:

    @classmethod
    def analyze(
        cls,
        resume: ResumeData,
        job_description: str,
        ats_score: float = 0,
    ):

        # -----------------------------
        # Parse Job Description
        # -----------------------------
        job = JobParser.parse(job_description)

        # -----------------------------
        # Skill Matching
        # -----------------------------
        skill_result = JobMatcher.match(
            resume_skills=resume.skills,
            job_skills=job.skills,
        )

        # -----------------------------
        # Skill Gap Analysis
        # -----------------------------
        gap_result = SkillGapAnalyzer.analyze(
            skill_result.missing_skills
        )

        # -----------------------------
        # Experience Match
        # -----------------------------
        experience_years = len(resume.experience)

        experience_score = ExperienceMatcher.calculate(
            resume_experience_years=experience_years,
            required_experience=job.experience,
        )

        # -----------------------------
        # Education Match
        # -----------------------------
        education_score = EducationMatcher.calculate(
            resume_education=resume.education,
            required_education=job.education,
        )

        # -----------------------------
        # Overall Match Score
        # -----------------------------
        match_result = JobMatchScorer.calculate(
            skill_match=skill_result.match_percentage,
            ats_score=ats_score,
            experience_match=experience_score,
            education_match=education_score,
            keyword_coverage=skill_result.match_percentage,
        )

        # -----------------------------
        # Recommendations
        # -----------------------------
        recommendation_result = JobRecommendationEngine.generate(
            missing_skills=skill_result.missing_skills,
            critical_skills=[
                gap.skill for gap in gap_result.critical
            ],
            important_skills=[
                gap.skill for gap in gap_result.important
            ],
            match_score=match_result["overall_score"],
            ats_score=ats_score,
        )

        # -----------------------------
        # Final Response
        # -----------------------------
        return {
            "job": job,
            "skill_match": skill_result,
            "skill_gap": gap_result,
            "experience_match": experience_score,
            "education_match": education_score,
            "match_score": match_result,
            "recommendations": recommendation_result,
        }