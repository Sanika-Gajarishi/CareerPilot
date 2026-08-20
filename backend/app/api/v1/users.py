from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.auth import get_db
from app.models.user import User
from app.models.interview import InterviewSession
from app.models.job_tracker import JobTracker
from app.models.resume import Resume
from app.models.roadmap import CareerRoadmapModel
from app.models.ats_analysis import ATSAnalysis
from app.schemas.user import UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me")
def get_current_user_profile(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "phone": current_user.phone,
        "github_url": current_user.github_url,
        "linkedin_url": current_user.linkedin_url,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at,
    }


@router.put("/me")
def update_current_user_profile(
    request: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not request.full_name.strip():
        raise HTTPException(status_code=400, detail="Full name is required.")

    current_user.full_name = request.full_name.strip()
    current_user.phone = request.phone.strip() if request.phone else None
    current_user.github_url = request.github_url.strip() if request.github_url else None
    current_user.linkedin_url = request.linkedin_url.strip() if request.linkedin_url else None

    db.commit()
    db.refresh(current_user)

    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "phone": current_user.phone,
        "github_url": current_user.github_url,
        "linkedin_url": current_user.linkedin_url,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at,
    }


@router.delete("/me")
def delete_current_user_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resume_ids = [
        resume.id
        for resume in db.query(Resume).filter(Resume.user_id == current_user.id).all()
    ]
    if resume_ids:
        db.query(ATSAnalysis).filter(ATSAnalysis.resume_id.in_(resume_ids)).delete(
            synchronize_session=False,
        )
    db.query(Resume).filter(Resume.user_id == current_user.id).delete(
        synchronize_session=False,
    )
    db.query(JobTracker).filter(JobTracker.user_id == current_user.id).delete(
        synchronize_session=False,
    )
    db.query(InterviewSession).filter(InterviewSession.user_id == current_user.id).delete(
        synchronize_session=False,
    )
    db.query(CareerRoadmapModel).filter(CareerRoadmapModel.user_id == current_user.id).delete(
        synchronize_session=False,
    )
    db.delete(current_user)
    db.commit()

    return {"message": "Account deleted successfully."}