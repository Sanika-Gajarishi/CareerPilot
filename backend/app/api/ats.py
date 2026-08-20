from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.agents.resume_agent.schemas import ResumeData
from app.database.session import get_db

from app.models.resume import Resume

from app.agents.resume_agent.agent import ResumeAgent
from app.agents.ats_agent.agent import ATSAgent

from app.repositories.ats_repository import ATSRepository

router = APIRouter(
    prefix="/api/v1/ats",
    tags=["ATS"],
)


@router.post("/analyze/{resume_id}")
def analyze_resume(
    resume_id: int,
    db: Session = Depends(get_db),
):
    """
    Analyze a resume.

    If a cached analysis exists for the current
    resume version, return it instead of
    running the ATS engine again.
    """

    # Fetch Resume
    resume_record = (
        db.query(Resume)
        .filter(Resume.id == resume_id)
        .first()
    )

    if not resume_record:
        raise HTTPException(
            status_code=404,
            detail="Resume not found."
        )

    # ----------------------------
    # Check Cached Analysis
    # ----------------------------

    latest_analysis = ATSRepository.get_latest_by_resume(
        db=db,
        resume_id=resume_id,
    )

    if (
        latest_analysis
        and latest_analysis.resume_updated_at
        == resume_record.updated_at
    ):
        return {
            "cached": True,
            "analysis": latest_analysis.result,
        }

    # ----------------------------
    # Parse Resume
    # ----------------------------

    parsed_resume = ResumeData.model_validate(
        resume_record.parsed_data
    )
    parsed_resume.raw_text = resume_record.raw_text

    # ----------------------------
    # Run ATS Engine
    # ----------------------------

    result = ATSAgent.analyze(parsed_resume)

    result_dict = result.model_dump()

    # ----------------------------
    # Save Analysis
    # ----------------------------

    ATSRepository.save(
        db=db,
        resume_id=resume_id,
        score=result.overall_score,
        result=result_dict,
        resume_updated_at=resume_record.updated_at,
    )

    return {
        "cached": False,
        "analysis": result_dict,
    }


@router.get("/history")
def get_analysis_history(
    db: Session = Depends(get_db),
):
    """
    Return ATS analysis history.
    """

    analyses = ATSRepository.get_history(db)

    return [
        {
            "id": analysis.id,
            "resume_id": analysis.resume_id,
            "overall_score": analysis.overall_score,
            "created_at": analysis.created_at,
        }
        for analysis in analyses
    ]


@router.get("/{analysis_id}")
def get_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
):
    """
    Return one ATS analysis.
    """

    analysis = ATSRepository.get_by_id(
        db=db,
        analysis_id=analysis_id,
    )

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found."
        )

    return analysis.result


@router.delete("/{analysis_id}")
def delete_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete an ATS analysis.
    """

    analysis = ATSRepository.get_by_id(
        db=db,
        analysis_id=analysis_id,
    )

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found."
        )

    ATSRepository.delete(
        db=db,
        analysis=analysis,
    )

    return {
        "message": "Analysis deleted successfully."
    }