from pydantic import BaseModel


class SkillGap(BaseModel):

    skill: str

    category: str

    priority: str

    recommendation: str


class SkillGapResult(BaseModel):

    critical: list[SkillGap]

    important: list[SkillGap]

    nice_to_have: list[SkillGap]

    total_gaps: int