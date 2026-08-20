from pydantic import BaseModel


class MatchScoreBreakdown(BaseModel):

    skill_match: float
    ats_score: float
    experience_match: float
    education_match: float
    keyword_coverage: float


class JobMatchScore(BaseModel):

    overall_score: float

    match_level: str

    breakdown: MatchScoreBreakdown

    explanation: list[str]