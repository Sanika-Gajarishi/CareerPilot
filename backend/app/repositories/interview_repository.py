from sqlalchemy.orm import Session

from app.models.interview import InterviewSession


class InterviewRepository:

    @staticmethod
    def create(
        db: Session,
        interview: InterviewSession,
    ) -> InterviewSession:

        db.add(interview)
        db.commit()
        db.refresh(interview)

        return interview

    @staticmethod
    def get_by_id(
        db: Session,
        interview_id: int,
    ):

        return (
            db.query(InterviewSession)
            .filter(
                InterviewSession.id == interview_id
            )
            .first()
        )

    @staticmethod
    def get_user_interviews(
        db: Session,
        user_id: int,
    ):

        return (
            db.query(InterviewSession)
            .filter(
                InterviewSession.user_id == user_id
            )
            .order_by(
                InterviewSession.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        interview: InterviewSession,
    ):

        db.commit()
        db.refresh(interview)

        return interview

    @staticmethod
    def delete(
        db: Session,
        interview: InterviewSession,
    ):

        db.delete(interview)
        db.commit()