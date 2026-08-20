import os

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.agents.roadmap_agent.generator import RoadmapGenerator
from app.models.roadmap import CareerRoadmapModel
from app.models.resume import Resume
from app.models.ats_analysis import ATSAnalysis
from app.repositories.resume_repository import ResumeRepository
from app.repositories.roadmap_repository import RoadmapRepository



class ResumeService:
    def __init__(self, repository: ResumeRepository):
        self.repository = repository

    # =====================================
    # Instance Methods
    # =====================================

    def save_resume(
        self,
        user_id: int,
        filename: str,
        file_path: str,
        raw_text: str,
        parsed_data: dict,
    ):
        resume = Resume(
            user_id=user_id,
            original_filename=filename,
            file_path=file_path,
            raw_text=raw_text,
            parsed_data=parsed_data,
        )

        return self.repository.create(resume)

    # =====================================
    # Static Methods
    # =====================================

    @staticmethod
    def list_resumes(
        db: Session,
        user_id: int,
    ):
        repository = ResumeRepository(db)
        return repository.get_all_by_user_id(user_id)

    @staticmethod
    def get_resume(
        db: Session,
        resume_id: int,
    ):
        repository = ResumeRepository(db)
        return repository.get_by_id(resume_id)

    @staticmethod
    def get_resume_file(
        db: Session,
        resume_id: int,
    ):
        repository = ResumeRepository(db)

        resume = repository.get_by_id(resume_id)

        if not resume:
            raise HTTPException(
                status_code=404,
                detail="Resume not found",
            )

        if not os.path.exists(resume.file_path):
            raise HTTPException(
                status_code=404,
                detail="Resume file not found",
            )

        return resume

    @staticmethod
    def delete_resume(
        db: Session,
        resume_id: int,
    ):
        repository = ResumeRepository(db)

        resume = repository.get_by_id(resume_id)

        if not resume:
            raise HTTPException(
                status_code=404,
                detail="Resume not found",
            )

        if resume.file_path and os.path.exists(resume.file_path):
            os.remove(resume.file_path)

        db.query(ATSAnalysis).filter(
            ATSAnalysis.resume_id == resume_id
        ).delete(synchronize_session=False)

        repository.delete(resume)

        return {
            "message": "Resume deleted successfully"
        }


    @staticmethod
    def generate_and_save(
        db,
        user_id: int,
        request,
    ):
        roadmap = RoadmapGenerator.generate(request)

        model = CareerRoadmapModel(
            user_id=user_id,
            target_role=request.target_role,
            target_company=request.target_company,
            experience_level=request.experience_level,
            timeline_months=request.timeline_months,
            roadmap=roadmap.model_dump(),
            completion_percentage=0,
        )

        return RoadmapRepository.create(
            db,
            model,
        )

    @staticmethod
    def get_user_roadmaps(
        db,
        user_id: int,
    ):
        return RoadmapRepository.get_user_roadmaps(
            db,
            user_id,
        )

    @staticmethod
    def get_by_id(
        db,
        roadmap_id: int,
    ):
        return RoadmapRepository.get_by_id(
            db,
            roadmap_id,
        )

    @staticmethod
    def delete(
        db,
        roadmap,
    ):
        RoadmapRepository.delete(
            db,
            roadmap,
        )

    @staticmethod
    def update_progress(
        db,
        roadmap,
        progress,
    ):
        return RoadmapRepository.update_progress(
            db,
            roadmap,
            progress,
        )

    @staticmethod
    def update_last_opened(
        db,
        roadmap,
    ):
        return RoadmapRepository.update_last_opened(
            db,
            roadmap,
        )