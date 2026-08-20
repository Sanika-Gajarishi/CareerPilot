from sqlalchemy.orm import Session

from app.models.roadmap import CareerRoadmapModel
from app.repositories.roadmap_repository import RoadmapRepository

from app.agents.roadmap_agent.generator import RoadmapGenerator


class RoadmapService:

    @staticmethod
    def generate_and_save(
        db: Session,
        user_id: int,
        request,
    ):
        """
        Generate a career roadmap using the AI roadmap generator
        and save it to the database.
        """

        roadmap = RoadmapGenerator.generate(request)

        roadmap_model = CareerRoadmapModel(
            user_id=user_id,
            target_role=request.target_role,
            target_company=request.target_company,
            experience_level=request.experience_level,
            timeline_months=request.timeline_months,
            roadmap=roadmap.model_dump(),
            completion_percentage=0,
            status="In Progress",
        )

        return RoadmapRepository.create(
            db=db,
            roadmap=roadmap_model,
        )

    @staticmethod
    def get_user_roadmaps(
        db: Session,
        user_id: int,
    ):
        return RoadmapRepository.get_user_roadmaps(
            db=db,
            user_id=user_id,
        )

    @staticmethod
    def get_by_id(
        db: Session,
        roadmap_id: int,
    ):
        roadmap = RoadmapRepository.get_by_id(
            db=db,
            roadmap_id=roadmap_id,
        )

        if roadmap:
            RoadmapRepository.update_last_opened(
                db=db,
                roadmap=roadmap,
            )

        return roadmap

    @staticmethod
    def delete(
        db: Session,
        roadmap,
    ):
        RoadmapRepository.delete(
            db=db,
            roadmap=roadmap,
        )

    @staticmethod
    def update_progress(
        db: Session,
        roadmap,
        progress: float,
    ):
        return RoadmapRepository.update_progress(
            db=db,
            roadmap=roadmap,
            progress=progress,
        )