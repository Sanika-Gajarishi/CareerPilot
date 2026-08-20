from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class JobTrackerCreate(BaseModel):

    company: str

    job_title: str

    location: Optional[str] = None

    application_url: Optional[str] = None

    salary: Optional[str] = None

    notes: Optional[str] = None

    applied_date: Optional[date] = None

    interview_date: Optional[date] = None

    follow_up_date: Optional[date] = None


class JobTrackerUpdate(BaseModel):

    company: Optional[str] = None

    job_title: Optional[str] = None

    location: Optional[str] = None

    application_url: Optional[str] = None

    salary: Optional[str] = None

    status: Optional[str] = None

    notes: Optional[str] = None

    applied_date: Optional[date] = None

    interview_date: Optional[date] = None

    follow_up_date: Optional[date] = None


class JobTrackerResponse(BaseModel):

    id: int

    company: str

    job_title: str

    location: Optional[str]

    application_url: Optional[str]

    salary: Optional[str]

    status: str

    notes: Optional[str]

    applied_date: Optional[date]

    interview_date: Optional[date]

    follow_up_date: Optional[date]

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True