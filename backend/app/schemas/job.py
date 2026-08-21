from datetime import datetime

from pydantic import BaseModel, Field


class JobCreate(BaseModel):
    description: str = Field(
        ...,
        min_length=20,
        description="Full job description",
    )


class JobResponse(BaseModel):
    id: int
    title: str
    company: str | None = None
    location: str | None = None
    employment_type: str | None = None
    salary: str | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True