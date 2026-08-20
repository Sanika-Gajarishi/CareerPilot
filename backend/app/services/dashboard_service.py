from sqlalchemy.orm import Session

from app.models.user import User


class DashboardService:

    def __init__(self, db: Session):
        self.db = db

    def get_dashboard(self, current_user: User):

        return {

            "user_name": current_user.full_name,

            "resume_uploaded": False,

            "resume_count": 0,

            "ats_score": 0,

            "applications": 0,

            "job_matches": 0,

            "interview_sessions": 0,

            "roadmap_generated": False,
        }