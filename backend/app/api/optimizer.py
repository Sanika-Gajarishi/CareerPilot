from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.resume import Resume

from app.agents.resume_optimizer.agent import (
    ResumeOptimizerAgent,
)


router = APIRouter(
    prefix="/api/v1/optimizer",
    tags=["Resume Optimizer"],
)


@router.post("/{resume_id}")
def optimize_resume(
    resume_id: int,
    db: Session = Depends(get_db),
):

    # -------------------------------------------------
    # Find Resume
    # -------------------------------------------------

    resume = (
        db.query(Resume)
        .filter(
            Resume.id == resume_id
        )
        .first()
    )

    if not resume:

        raise HTTPException(
            status_code=404,
            detail="Resume not found.",
        )

    # -------------------------------------------------
    # Validate Resume Text
    # -------------------------------------------------

    if not resume.raw_text:

        raise HTTPException(
            status_code=400,
            detail="Resume text is empty.",
        )

    # -------------------------------------------------
    # Optimize
    # -------------------------------------------------

    try:

        result = ResumeOptimizerAgent.optimize(
            resume.raw_text
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Resume optimization failed: {str(e)}",
        )

    # -------------------------------------------------
    # Return
    # -------------------------------------------------

    return {
        "success": True,
        "resume_id": resume.id,
        "summary": result.get(
            "summary",
            "",
        ),
        "skills": result.get(
            "skills",
            [],
        ),
        "experience": result.get(
            "experience",
            [],
        ),
        "projects": result.get(
            "projects",
            [],
        ),
        "recommendations": result.get(
            "recommendations",
            [],
        ),
    }