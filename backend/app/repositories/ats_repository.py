from datetime import datetime

from sqlalchemy.orm import Session

from app.models.ats_analysis import ATSAnalysis


class ATSRepository:

    @staticmethod
    def save(
        db: Session,
        resume_id: int,
        score: float,
        result: dict,
        resume_updated_at: datetime,
    ):
        analysis = ATSAnalysis(
            resume_id=resume_id,
            overall_score=score,
            result=result,
            resume_updated_at=resume_updated_at,
        )

        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        return analysis

    @staticmethod
    def get_history(
        db: Session,
    ):
        return (
            db.query(ATSAnalysis)
            .order_by(ATSAnalysis.created_at.desc())
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        analysis_id: int,
    ):
        return (
            db.query(ATSAnalysis)
            .filter(
                ATSAnalysis.id == analysis_id
            )
            .first()
        )

    @staticmethod
    def get_latest_by_resume(
        db: Session,
        resume_id: int,
    ):
        return (
            db.query(ATSAnalysis)
            .filter(
                ATSAnalysis.resume_id == resume_id
            )
            .order_by(
                ATSAnalysis.created_at.desc()
            )
            .first()
        )

    @staticmethod
    def delete(
        db: Session,
        analysis: ATSAnalysis,
    ):
        db.delete(analysis)
        db.commit()