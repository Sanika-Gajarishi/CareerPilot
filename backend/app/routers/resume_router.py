from pathlib import Path
import shutil
import uuid
from app.services.ats_service import ATSService
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.ats_analysis import ATSAnalysis
from app.database.session import get_db
from app.api.dependencies.auth import get_current_user
from app.models.resume import Resume
from app.schemas.resume import ResumeResponse
from app.services.resume_parser import ResumeParser

router = APIRouter(
    prefix="/api/v1/resume",
    tags=["Resume"],
)

UPLOAD_DIR = Path("uploads/resumes")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload", response_model=ResumeResponse)
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing."
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    filename = f"{uuid.uuid4()}.pdf"

    file_path = UPLOAD_DIR / filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = ResumeParser.extract_text(str(file_path))

    resume = Resume(
        user_id=current_user.id,
        original_filename=file.filename,
        file_path=str(file_path),
        raw_text=extracted_text,
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    analysis = ATSService.analyze_resume(extracted_text)

    ats_analysis = ATSAnalysis(
    resume_id=resume.id,
    overall_score=analysis["ats_score"],
    result=analysis,
    resume_updated_at=resume.updated_at,
   )

    db.add(ats_analysis)
    db.commit()

    return resume

    

   