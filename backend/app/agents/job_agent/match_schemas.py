from pydantic import BaseModel


class SkillMatch(BaseModel):
    skill: str
    matched: bool
    source: str


class JobMatchResult(BaseModel):
    matched_skills: list[str]
    missing_skills: list[str]
    match_percentage: float

    resume_skill_count: int
    job_skill_count: int

    skill_details: list[SkillMatch]