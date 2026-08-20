from sqlalchemy.orm import Session

from app.models.job_tracker import JobTracker


class JobTrackerRepository:

    @staticmethod
    def create(
        db: Session,
        job: JobTracker,
    ) -> JobTracker:

        db.add(job)
        db.commit()
        db.refresh(job)

        return job

    @staticmethod
    def get_by_id(
        db: Session,
        job_id: int,
    ) -> JobTracker | None:

        return (
            db.query(JobTracker)
            .filter(
                JobTracker.id == job_id
            )
            .first()
        )

    @staticmethod
    def get_user_jobs(
        db: Session,
        user_id: int,
    ) -> list[JobTracker]:

        return (
            db.query(JobTracker)
            .filter(
                JobTracker.user_id == user_id
            )
            .order_by(
                JobTracker.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        job: JobTracker,
    ) -> JobTracker:

        db.commit()
        db.refresh(job)

        return job

    @staticmethod
    def delete(
        db: Session,
        job: JobTracker,
    ) -> None:

        db.delete(job)
        db.commit()

    @staticmethod
    def get_by_status(
        db: Session,
        user_id: int,
        status: str,
    ) -> list[JobTracker]:

        return (
            db.query(JobTracker)
            .filter(
                JobTracker.user_id == user_id,
                JobTracker.status == status,
            )
            .order_by(
                JobTracker.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def search(
        db: Session,
        user_id: int,
        keyword: str,
    ) -> list[JobTracker]:

        return (
            db.query(JobTracker)
            .filter(
                JobTracker.user_id == user_id,
                (
                    JobTracker.company.ilike(f"%{keyword}%")
                )
                | (
                    JobTracker.job_title.ilike(f"%{keyword}%")
                ),
            )
            .order_by(
                JobTracker.created_at.desc()
            )
            .all()
        )