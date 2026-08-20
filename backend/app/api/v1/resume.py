from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.core.security import get_current_user
from app.models.user import User

from app.agents.resume_agent.agent import ResumeAgent
from app.agents.resume_agent.extractor import ResumeExtractor
from app.agents.resume_agent.file_handler import FileHandler
from app.agents.resume_agent.parser import ResumeParser

from app.repositories.resume_repository import ResumeRepository
from app.resume.pipeline import ResumePipeline

from app.schemas.resume import (
    ResumeUploadResponse,
    ResumeListResponse,
    ResumeDetailResponse,
)

from app.services.resume_service import ResumeService


router = APIRouter(
    prefix="/resume",
    tags=["Resume"],
)


# ============================================================
# Get All User Resumes
# ============================================================

@router.get(
    "/",
    response_model=list[ResumeListResponse],
)
def get_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = ResumeRepository(db)

    return repository.get_all_by_user_id(current_user.id)


# ============================================================
# Resume History
# ============================================================

@router.get(
    "/list",
    response_model=list[ResumeListResponse],
)
def list_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ResumeService.list_resumes(
        db=db,
        user_id=current_user.id,
    )


# ============================================================
# Get Resume Details
# ============================================================

@router.get(
    "/{resume_id}",
    response_model=ResumeDetailResponse,
)
def get_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resume = ResumeService.get_resume(
        db=db,
        resume_id=resume_id,
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found",
        )

    if resume.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied",
        )

    return resume


# ============================================================
# View Resume in Browser
# ============================================================

@router.get("/{resume_id}/view")
def view_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resume = ResumeService.get_resume_file(
        db=db,
        resume_id=resume_id,
    )

    if resume.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied",
        )

    media_type = (
        "application/pdf"
        if resume.original_filename.lower().endswith(".pdf")
        else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    return FileResponse(
        path=resume.file_path,
        filename=resume.original_filename,
        media_type=media_type,
        headers={
            "Content-Disposition": f'inline; filename="{resume.original_filename}"'
        },
    )


# ============================================================
# Download Resume
# ============================================================

@router.get("/{resume_id}/download")
def download_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resume = ResumeService.get_resume_file(
        db=db,
        resume_id=resume_id,
    )

    if resume.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied",
        )

    return FileResponse(
        path=resume.file_path,
        filename=resume.original_filename,
        media_type="application/octet-stream",
    )


# ============================================================
# Delete Resume
# ============================================================

@router.delete("/{resume_id}")
def delete_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resume = ResumeService.get_resume(
        db=db,
        resume_id=resume_id,
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found",
        )

    if resume.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied",
        )

    return ResumeService.delete_resume(
        db=db,
        resume_id=resume_id,
    )


# ============================================================
# Upload Resume
# ============================================================

@router.post(
    "/upload",
    response_model=ResumeUploadResponse,
)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if file.content_type not in (
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported.",
        )

    file_bytes = await file.read()

    if file.content_type == "application/pdf":
        raw_text = ResumeParser.parse_pdf(file_bytes)
    else:
        raw_text = ResumeParser.parse_docx(file_bytes)

    raw_text = ResumeExtractor.clean_text(raw_text)

    pipeline = ResumePipeline()
    pipeline.process(raw_text)

    resume_agent = ResumeAgent()
    parsed_resume = resume_agent.process(raw_text)

    file_path, _ = FileHandler.save(
        file_bytes=file_bytes,
        original_filename=file.filename,
    )

    repository = ResumeRepository(db)
    service = ResumeService(repository)

    return service.save_resume(
        user_id=current_user.id,
        filename=file.filename,
        file_path=file_path,
        raw_text=raw_text,
        parsed_data=parsed_resume.model_dump(),
    )