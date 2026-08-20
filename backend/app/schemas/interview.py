from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class InterviewCreate(BaseModel):
    target_role: str
    company: Optional[str] = None
    difficulty: str
    interview_type: str


class AnswerRequest(BaseModel):
    question_number: int
    answer: str


class InterviewResponse(BaseModel):
    id: int
    target_role: str
    company: Optional[str] = None
    difficulty: str
    interview_type: str

    questions: dict[str, Any]
    answers: list[dict[str, Any]]
    feedback: dict[str, Any]

    overall_score: float
    status: str

    model_config = ConfigDict(from_attributes=True)


class InterviewSummary(BaseModel):
    id: int
    target_role: str
    company: Optional[str] = None
    overall_score: float
    status: str

    model_config = ConfigDict(from_attributes=True)