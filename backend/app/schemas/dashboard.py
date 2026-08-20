from pydantic import BaseModel


class DashboardResponse(BaseModel):
    user_name: str

    resume_uploaded: bool
    resume_count: int

    ats_score: int

    applications: int

    job_matches: int

    interview_sessions: int

    roadmap_generated: bool