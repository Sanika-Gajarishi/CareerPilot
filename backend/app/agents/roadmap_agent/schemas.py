from pydantic import BaseModel, Field
from typing import List, Optional


# -----------------------------------------
# Career Goal Input
# -----------------------------------------

class CareerGoalRequest(BaseModel):
    target_role: str = Field(..., examples=["AI Engineer"])
    target_company: Optional[str] = Field(
        default=None,
        examples=["Google"],
    )
    experience_level: str = Field(
        ...,
        examples=["Fresher"],
    )
    timeline_months: int = Field(
        default=6,
        ge=1,
        le=24,
    )
    weekly_hours: int = Field(
        default=10,
        ge=1,
        le=60,
    )


# -----------------------------------------
# Weekly Task
# -----------------------------------------

class WeeklyTask(BaseModel):
    week: int
    title: str
    description: str
    estimated_hours: int


# -----------------------------------------
# Monthly Milestone
# -----------------------------------------

class MonthlyMilestone(BaseModel):
    month: int
    title: str
    objective: str

    skills: List[str] = []

    projects: List[str] = []

    weekly_tasks: List[WeeklyTask] = []


# -----------------------------------------
# Recommended Project
# -----------------------------------------

class ProjectRecommendation(BaseModel):
    title: str
    difficulty: str
    duration_weeks: int
    description: str
    skills: List[str]


# -----------------------------------------
# Learning Resource
# -----------------------------------------

class LearningResource(BaseModel):
    title: str
    platform: str
    url: str

    resource_type: str

    difficulty: str

    estimated_hours: int


# -----------------------------------------
# Progress
# -----------------------------------------

class RoadmapProgress(BaseModel):
    completed_months: int = 0
    completed_tasks: int = 0
    total_tasks: int = 0

    completion_percentage: float = 0.0


# -----------------------------------------
# Final Response
# -----------------------------------------

class CareerRoadmap(BaseModel):

    target_role: str

    timeline_months: int

    monthly_plan: List[MonthlyMilestone]

    recommended_projects: List[ProjectRecommendation]

    learning_resources: List[LearningResource]

    progress: RoadmapProgress