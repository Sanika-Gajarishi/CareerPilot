from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.api.dependencies.auth import get_current_user
from app.services.job_tracker_service import JobTrackerService
from app.schemas.job_tracker import (
    JobTrackerCreate,
    JobTrackerUpdate,
    JobTrackerResponse,
)

router = APIRouter(
    prefix="/job-tracker",
    tags=["Job Tracker"],
)


@router.post(
    "",
    response_model=JobTrackerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_job(
    request: JobTrackerCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return JobTrackerService.create_job(
        db=db,
        user_id=current_user.id,
        request=request,
    )


@router.get(
    "",
    response_model=list[JobTrackerResponse],
)
def get_jobs(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return JobTrackerService.get_user_jobs(
        db,
        current_user.id,
    )


# -----------------------------
# SEARCH
# -----------------------------
@router.get(
    "/search",
    response_model=list[JobTrackerResponse],
)
def search_jobs(
    keyword: str = Query(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return JobTrackerService.search_jobs(
        db,
        current_user.id,
        keyword,
    )


# -----------------------------
# FILTER BY STATUS
# -----------------------------
@router.get(
    "/status/{status}",
    response_model=list[JobTrackerResponse],
)
def get_jobs_by_status(
    status: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return JobTrackerService.get_jobs_by_status(
        db,
        current_user.id,
        status,
    )


# -----------------------------
# GET SINGLE JOB
# -----------------------------
@router.get(
    "/{job_id}",
    response_model=JobTrackerResponse,
)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    job = JobTrackerService.get_job(
        db,
        job_id,
    )

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found.",
        )

    if job.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied.",
        )

    return job


# -----------------------------
# UPDATE JOB
# -----------------------------
@router.put(
    "/{job_id}",
    response_model=JobTrackerResponse,
)
def update_job(
    job_id: int,
    request: JobTrackerUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    job = JobTrackerService.get_job(
        db,
        job_id,
    )

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found.",
        )

    if job.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied.",
        )

    return JobTrackerService.update_job(
        db,
        job,
        request,
    )


# -----------------------------
# DELETE JOB
# -----------------------------
@router.delete(
    "/{job_id}",
)
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    job = JobTrackerService.get_job(
        db,
        job_id,
    )

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found.",
        )

    if job.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied.",
        )

    JobTrackerService.delete_job(
        db,
        job,
    )

    return {
        "message": "Job deleted successfully."
    }