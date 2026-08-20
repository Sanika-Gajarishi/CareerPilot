from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.interview import (
    InterviewCreate,
    InterviewResponse,
    InterviewSummary,
    AnswerRequest,
)
from app.services.interview_service import InterviewService

from app.api.dependencies.auth import get_current_user

router = APIRouter(
    prefix="/interview",
    tags=["Interview"],
)

@router.post(
    "/start",
    response_model=InterviewResponse,
    status_code=status.HTTP_201_CREATED,
)
def start_interview(
    request: InterviewCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    interview = InterviewService.start_interview(
        db=db,
        user_id=current_user.id,
        request=request,
    )

    return interview

@router.post(
    "/{interview_id}/answer",
    response_model=InterviewResponse,
)
def submit_answer(
    interview_id: int,
    request: AnswerRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    interview = InterviewService.get_interview(
        db,
        interview_id,
    )

    if interview is None:

        raise HTTPException(
            status_code=404,
            detail="Interview not found.",
        )

    if interview.user_id != current_user.id:

        raise HTTPException(
            status_code=403,
            detail="Not authorized.",
        )

    return InterviewService.submit_answer(
        db,
        interview,
        request,
    )

@router.get(
    "/{interview_id}",
    response_model=InterviewResponse,
)
def get_interview(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    interview = InterviewService.get_interview(
        db,
        interview_id,
    )

    if interview is None:

        raise HTTPException(
            status_code=404,
            detail="Interview not found.",
        )

    if interview.user_id != current_user.id:

        raise HTTPException(
            status_code=403,
            detail="Not authorized.",
        )

    return interview

@router.get(
    "",
    response_model=list[InterviewSummary],
)
def get_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return InterviewService.get_user_interviews(
        db,
        current_user.id,
    )

@router.delete(
    "/{interview_id}",
)
def delete_interview(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    interview = InterviewService.get_interview(
        db,
        interview_id,
    )

    if interview is None:

        raise HTTPException(
            status_code=404,
            detail="Interview not found.",
        )

    if interview.user_id != current_user.id:

        raise HTTPException(
            status_code=403,
            detail="Not authorized.",
        )

    InterviewService.delete_interview(
        db,
        interview,
    )

    return {
        "message": "Interview deleted successfully."
    }