from pydantic import BaseModel


class InterviewQuestion(BaseModel):
    question_number: int
    category: str
    difficulty: str
    question: str


class InterviewQuestionSet(BaseModel):
    questions: list[InterviewQuestion]