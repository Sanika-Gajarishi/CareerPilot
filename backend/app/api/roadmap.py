from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.api.dependencies.auth import get_current_user

from app.agents.roadmap_agent.schemas import CareerGoalRequest

from app.services.roadmap_service import RoadmapService


router = APIRouter(
    prefix="/roadmap",
    tags=["Career Roadmap"],
)


# ---------------------------------------------------------
# Generate Roadmap
# ---------------------------------------------------------

@router.post(
    "/generate",
    status_code=status.HTTP_201_CREATED,
)
def generate_roadmap(
    request: CareerGoalRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Generate a new roadmap for the logged-in user.
    """

    roadmap = RoadmapService.generate_and_save(
        db=db,
        user_id=current_user.id,
        request=request,
    )

    return roadmap


# ---------------------------------------------------------
# Get All Roadmaps
# ---------------------------------------------------------

@router.get("")
def get_my_roadmaps(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Return all roadmaps of the current user.
    """

    return RoadmapService.get_user_roadmaps(
        db=db,
        user_id=current_user.id,
    )


# ---------------------------------------------------------
# Get Single Roadmap
# ---------------------------------------------------------

@router.get("/{roadmap_id}")
def get_roadmap(
    roadmap_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Get one roadmap.
    """

    roadmap = RoadmapService.get_by_id(
        db=db,
        roadmap_id=roadmap_id,
    )

    if roadmap is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Roadmap not found.",
        )

    if roadmap.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized.",
        )

    return roadmap


# ---------------------------------------------------------
# Delete Roadmap
# ---------------------------------------------------------

@router.delete("/{roadmap_id}")
def delete_roadmap(
    roadmap_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Delete roadmap.
    """

    roadmap = RoadmapService.get_by_id(
        db=db,
        roadmap_id=roadmap_id,
    )

    if roadmap is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Roadmap not found.",
        )

    if roadmap.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized.",
        )

    RoadmapService.delete(
        db=db,
        roadmap=roadmap,
    )

    return {
        "message": "Roadmap deleted successfully."
    }


# ---------------------------------------------------------
# Update Progress
# ---------------------------------------------------------

@router.patch("/{roadmap_id}/progress/{progress}")
def update_progress(
    roadmap_id: int,
    progress: float,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Update roadmap completion percentage.
    """

    roadmap = RoadmapService.get_by_id(
        db=db,
        roadmap_id=roadmap_id,
    )

    if roadmap is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Roadmap not found.",
        )

    if roadmap.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized.",
        )

    return RoadmapService.update_progress(
        db=db,
        roadmap=roadmap,
        progress=progress,
    )


# ---------------------------------------------------------
# Mark Last Opened
# ---------------------------------------------------------

@router.patch("/{roadmap_id}/open")
def mark_opened(
    roadmap_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Update last opened timestamp.
    """

    roadmap = RoadmapService.get_by_id(
        db=db,
        roadmap_id=roadmap_id,
    )

    if roadmap is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Roadmap not found.",
        )

    if roadmap.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized.",
        )

    return RoadmapService.update_last_opened(
        db=db,
        roadmap=roadmap,
    )