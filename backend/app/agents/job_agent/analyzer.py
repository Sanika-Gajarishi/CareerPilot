from app.agents.job_agent.parser import JobParser
from app.agents.job_agent.matcher import JobMatcher
from app.agents.job_agent.gap_analyzer import SkillGapAnalyzer
from app.agents.job_agent.scorer import JobMatchScorer
from app.agents.job_agent.experience_matcher import ExperienceMatcher
from app.agents.job_agent.education_matcher import EducationMatcher
from app.agents.job_agent.recommender import JobRecommendationEngine
from app.agents.resume_agent.schemas import ResumeData


class JobAnalyzer:

    @classmethod
    def analyze(
        cls,
        resume: ResumeData,
        ats_score: float,
        job_description: str,
    ):

        # Parse Job Description
        parsed_job = JobParser.parse(job_description)

        # Match Skills
        match = JobMatcher.match(
            resume_skills=resume.skills,
            job_skills=parsed_job.skills,
        )

        # Skill Gap Analysis
        gaps = SkillGapAnalyzer.analyze(
            match.missing_skills
        )

        # Experience Match
        experience_match = ExperienceMatcher.calculate(
            resume_experience_years=len(resume.experience),
            required_experience=parsed_job.experience,
        )

        # Education Match
        education_match = EducationMatcher.calculate(
            resume_education=resume.education,
            required_education=parsed_job.education,
        )

        # Overall Score
        score = JobMatchScorer.calculate(
            skill_match=match.match_percentage,
            ats_score=ats_score,
            experience_match=experience_match,
            education_match=education_match,
            keyword_coverage=match.match_percentage,
        )

        # Recommendations
        recommendations = JobRecommendationEngine.generate(
            missing_skills=match.missing_skills,
            critical_skills=[
                gap.skill for gap in gaps.critical
            ],
            important_skills=[
                gap.skill for gap in gaps.important
            ],
            match_score=score["overall_score"],
            ats_score=ats_score,
        )

        return {
            **score,
            "matched_skills": match.matched_skills,
            "missing_skills": match.missing_skills,
            "skill_details": [
                detail.model_dump()
                for detail in match.skill_details
            ],
            "skill_groups": {
                "critical": [
                    gap.model_dump()
                    for gap in gaps.critical
                ],
                "important": [
                    gap.model_dump()
                    for gap in gaps.important
                ],
                "nice_to_have": [
                    gap.model_dump()
                    for gap in gaps.nice_to_have
                ],
            },
            "top_missing_keywords": [
                gap.skill
                for gap in (
                    gaps.critical
                    + gaps.important
                    + gaps.nice_to_have
                )[:8]
            ],
            "recommendations": recommendations.model_dump(),
        }