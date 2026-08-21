from sqlalchemy.orm import Session

from app.models.job import Job
from app.agents.job_agent.agent import JobAgent
from app.repositories.job_repository import JobRepository


class JobService:

    @staticmethod
    def create_job(
        db: Session,
        user_id: int,
        description: str,
    ):

        parsed = JobAgent.parse(description)

        job = Job(
            user_id=user_id,
            title=parsed.title or "Untitled Job",
            company=parsed.company,
            location=parsed.location,
            employment_type=parsed.employment_type,
            salary=parsed.salary,
            description=parsed.raw_text,
        )

        return JobRepository.create(
            db=db,
            job=job,
        )

    @staticmethod
    def get_job(
        db: Session,
        job_id: int,
    ):

        return JobRepository.get_by_id(
            db=db,
            job_id=job_id,
        )

    @staticmethod
    def get_user_jobs(
        db: Session,
        user_id: int,
    ):

        return JobRepository.get_all(
            db=db,
            user_id=user_id,
        )

    @staticmethod
    def delete_job(
        db: Session,
        job: Job,
    ):

        JobRepository.delete(
            db=db,
            job=job,
        )