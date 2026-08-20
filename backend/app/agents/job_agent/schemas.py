from pydantic import BaseModel


class ParsedJobDescription(BaseModel):

    title: str | None = None
    company: str | None = None
    location: str | None = None
    employment_type: str | None = None
    salary: str | None = None

    skills: list[str] = []

    required_skills: list[str] = []
    preferred_skills: list[str] = []

    responsibilities: list[str] = []
    qualifications: list[str] = []

    education: str | None = None
    experience: str | None = None

    raw_text: str