from sqlalchemy.orm import Session
from datetime import datetime
from app.models.roadmap import CareerRoadmapModel


class RoadmapRepository:

    @staticmethod
    def create(
        db: Session,
        roadmap: CareerRoadmapModel,
    ) -> CareerRoadmapModel:

        db.add(roadmap)
        db.commit()
        db.refresh(roadmap)

        return roadmap

    @staticmethod
    def get_by_id(
        db: Session,
        roadmap_id: int,
    ):

        return (
            db.query(CareerRoadmapModel)
            .filter(
                CareerRoadmapModel.id == roadmap_id
            )
            .first()
        )

    @staticmethod
    def get_user_roadmaps(
        db: Session,
        user_id: int,
    ):

        return (
            db.query(CareerRoadmapModel)
            .filter(
                CareerRoadmapModel.user_id == user_id
            )
            .order_by(
                CareerRoadmapModel.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        roadmap: CareerRoadmapModel,
    ):

        db.commit()
        db.refresh(roadmap)

        return roadmap

    @staticmethod
    def delete(
        db: Session,
        roadmap: CareerRoadmapModel,
    ):

        db.delete(roadmap)
        db.commit()

    @staticmethod
    def update_progress(db, roadmap, progress):
         roadmap.completion_percentage = progress
         db.commit()
         db.refresh(roadmap)
         return roadmap


    @staticmethod
    def update_last_opened(db, roadmap):
         roadmap.last_opened = datetime.utcnow()
         db.commit()
         db.refresh(roadmap)
         return roadmap