from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.resume import Resume

from app.schemas.job_match import JobMatchRequest

from app.agents.resume_agent.agent import ResumeAgent
from app.agents.ats_agent.agent import ATSAgent
from app.agents.job_agent.agent import JobAgent


router = APIRouter(
    prefix="/api/v1/job",
    tags=["Job Matching"],
)


@router.post("/match/{resume_id}")
def match_job(
    resume_id: int,
    request: JobMatchRequest,
    db: Session = Depends(get_db),
):

    # Get job description from request body
    job_description = request.job_description

    # Find resume
    resume = (
        db.query(Resume)
        .filter(Resume.id == resume_id)
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found.",
        )

    # Parse Resume
    parsed_resume = ResumeAgent.process(
        resume.raw_text
    )

    # ATS Analysis
    ats_result = ATSAgent.analyze(
        parsed_resume
    )

    ats_score = ats_result.overall_score

    # Job Match Analysis
    result = JobAgent.analyze(
        resume=parsed_resume,
        job_description=job_description,
        ats_score=ats_score,
    )

    return result