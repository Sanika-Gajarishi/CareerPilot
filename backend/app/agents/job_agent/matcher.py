from app.agents.job_agent.match_schemas import (
    JobMatchResult,
    SkillMatch,
)
from app.agents.job_agent.skill_aliases import SKILL_ALIASES


class JobMatcher:

    @staticmethod
    def normalize_skill(skill: str) -> str:
        normalized = (
            skill
            .strip()
            .lower()
        )
        return SKILL_ALIASES.get(normalized, normalized)

    @classmethod
    def match(
        cls,
        resume_skills: list[str],
        job_skills: list[str],
    ) -> JobMatchResult:

        resume_normalized = {
            cls.normalize_skill(skill)
            for skill in resume_skills
        }

        job_normalized = {
            cls.normalize_skill(skill)
            for skill in job_skills
        }

        matched = sorted(
            resume_normalized.intersection(
                job_normalized
            )
        )

        missing = sorted(
            job_normalized.difference(
                resume_normalized
            )
        )

        skill_details = []

        for skill in sorted(job_normalized):

            if skill in resume_normalized:
                skill_details.append(
                    SkillMatch(
                        skill=skill,
                        matched=True,
                        source="resume",
                    )
                )
            else:
                skill_details.append(
                    SkillMatch(
                        skill=skill,
                        matched=False,
                        source="job_description",
                    )
                )

        if job_normalized:
            match_percentage = round(
                (
                    len(matched)
                    / len(job_normalized)
                ) * 100,
                2,
            )
        else:
            match_percentage = 0.0

        return JobMatchResult(
            matched_skills=matched,
            missing_skills=missing,
            match_percentage=match_percentage,
            resume_skill_count=len(resume_normalized),
            job_skill_count=len(job_normalized),
            skill_details=skill_details,
        )