from datetime import datetime
from typing import Any

from pydantic import BaseModel


class RoadmapCreate(BaseModel):
    target_role: str
    target_company: str | None = None
    experience_level: str
    timeline_months: int
    weekly_hours: int


class RoadmapResponse(BaseModel):
    id: int
    user_id: int

    target_role: str
    target_company: str | None = None
    experience_level: str

    timeline_months: int

    roadmap: dict[str, Any]

    completion_percentage: float

    status: str

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True


class RoadmapSummary(BaseModel):
    id: int

    target_role: str

    experience_level: str

    completion_percentage: float

    status: str

    created_at: datetime

    class Config:
        from_attributes = True