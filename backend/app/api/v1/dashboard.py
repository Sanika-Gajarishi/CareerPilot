from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.api.dependencies.auth import get_current_user

from app.models.user import User
from app.models.resume import Resume
from app.models.ats_analysis import ATSAnalysis
from app.models.job_tracker import JobTracker
from app.models.interview import InterviewSession
from app.models.roadmap import CareerRoadmapModel

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("")
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    resumes = (
        db.query(Resume)
        .filter(Resume.user_id == current_user.id)
        .all()
    )

    resume_count = len(resumes)

    applications = (
        db.query(JobTracker)
        .filter(JobTracker.user_id == current_user.id)
        .all()
    )

    interviews = (
        db.query(InterviewSession)
        .filter(InterviewSession.user_id == current_user.id)
        .all()
    )

    roadmaps = (
        db.query(CareerRoadmapModel)
        .filter(CareerRoadmapModel.user_id == current_user.id)
        .all()
    )

    latest_resume = None

    if resumes:
        latest_resume = max(
            resumes,
            key=lambda r: r.created_at,
        )

    resume_score = 0
    ats_score = 0

    if latest_resume:
        parsed_data = latest_resume.parsed_data or {}
        resume_score = parsed_data.get("resume_score", 0)
        ats_score = parsed_data.get("ats_score", 0)

        latest_analysis = (
            db.query(ATSAnalysis)
            .filter(ATSAnalysis.resume_id == latest_resume.id)
            .order_by(ATSAnalysis.created_at.desc())
            .first()
        )

        if latest_analysis:
            ats_score = latest_analysis.overall_score or ats_score
            resume_score = resume_score or ats_score

    interview_scores = [
        float(interview.overall_score or 0)
        for interview in interviews
        if interview.overall_score is not None
    ]
    roadmap_progress = [
        float(roadmap.completion_percentage or 0)
        for roadmap in roadmaps
    ]

    recent_activity = []
    if resume_count:
        recent_activity.append(f"{resume_count} resume(s) uploaded")
    if applications:
        recent_activity.append(f"{len(applications)} job application(s) tracked")
    if interviews:
        recent_activity.append(f"{len(interviews)} interview session(s) completed")
    if roadmaps:
        recent_activity.append(f"{len(roadmaps)} career roadmap(s) created")
    if not recent_activity:
        recent_activity.append("No career activity yet")

    recommendations = []
    if not resume_count:
        recommendations.append("Upload your first resume")
    elif ats_score < 75:
        recommendations.append("Improve your resume ATS score")
    if not roadmaps:
        recommendations.append("Create a career roadmap")
    if not applications:
        recommendations.append("Track your first job application")

    return {

        "user_name": current_user.full_name,

        "resume_count": resume_count,

        "resume_score": resume_score,

        "ats_score": ats_score,

        "application_count": len(applications),

        "interview_ready": round(sum(interview_scores) / len(interview_scores), 2) if interview_scores else 0,

        "career_progress": round(sum(roadmap_progress) / len(roadmap_progress), 2) if roadmap_progress else 0,

        "resume_uploaded": bool(resume_count),

        "roadmap_count": len(roadmaps),
        "interview_count": len(interviews),
        "recent_activity": recent_activity,
        "recommendations": recommendations,

    }