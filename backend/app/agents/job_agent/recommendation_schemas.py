from pydantic import BaseModel


class Recommendation(BaseModel):
    category: str
    priority: str
    title: str
    description: str
    action: str


class JobRecommendationResult(BaseModel):
    recommendations: list[Recommendation]
    application_advice: str