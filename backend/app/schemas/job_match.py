from pydantic import BaseModel, Field


class JobMatchRequest(BaseModel):
    job_description: str = Field(
        ...,
        description="Complete job description pasted by the user."
    )