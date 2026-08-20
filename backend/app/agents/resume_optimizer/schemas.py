from pydantic import BaseModel


class ResumeOptimization(BaseModel):

    summary: str

    skills: list[str]

    experience: list[str]

    projects: list[str]

    recommendations: list[str]