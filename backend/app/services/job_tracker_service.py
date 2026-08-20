from app.models.job_tracker import JobTracker
from app.repositories.job_tracker_repository import (
    JobTrackerRepository,
)


class JobTrackerService:

    @staticmethod
    def create_job(
        db,
        user_id: int,
        request,
    ):

        job = JobTracker(

            user_id=user_id,

            company=request.company,

            job_title=request.job_title,

            location=request.location,

            application_url=request.application_url,

            salary=request.salary,

            notes=request.notes,

            applied_date=request.applied_date,

            interview_date=request.interview_date,

            follow_up_date=request.follow_up_date,

            status="Saved",
        )

        return JobTrackerRepository.create(
            db,
            job,
        )

    @staticmethod
    def get_job(
        db,
        job_id,
    ):

        return JobTrackerRepository.get_by_id(
            db,
            job_id,
        )

    @staticmethod
    def get_user_jobs(
        db,
        user_id,
    ):

        return JobTrackerRepository.get_user_jobs(
            db,
            user_id,
        )

    @staticmethod
    def update_job(
        db,
        job,
        request,
    ):

        update_data = request.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        for key, value in update_data.items():
            setattr(job, key, value)

        return JobTrackerRepository.update(
            db,
            job,
        )

    @staticmethod
    def delete_job(
        db,
        job,
    ):

        JobTrackerRepository.delete(
            db,
            job,
        )

    @staticmethod
    def get_jobs_by_status(
        db,
        user_id,
        status,
    ):

        return JobTrackerRepository.get_by_status(
            db,
            user_id,
            status,
        )

    @staticmethod
    def search_jobs(
        db,
        user_id,
        keyword,
    ):

        return JobTrackerRepository.search(
            db,
            user_id,
            keyword,
        )