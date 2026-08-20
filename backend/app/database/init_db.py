from app.database.base import Base
from app.database.session import engine
from sqlalchemy import text

# Import models here
from app.models.user import User


def create_tables():
    Base.metadata.create_all(bind=engine)

    # Add columns introduced after the original roadmap table was created.
    with engine.begin() as connection:
        connection.execute(
            text(
                "ALTER TABLE users "
                "ADD COLUMN IF NOT EXISTS phone VARCHAR(30)"
            )
        )
        connection.execute(
            text(
                "ALTER TABLE users "
                "ADD COLUMN IF NOT EXISTS github_url VARCHAR(500)"
            )
        )
        connection.execute(
            text(
                "ALTER TABLE users "
                "ADD COLUMN IF NOT EXISTS linkedin_url VARCHAR(500)"
            )
        )
        connection.execute(
            text(
                "ALTER TABLE career_roadmaps "
                "ADD COLUMN IF NOT EXISTS status VARCHAR "
                "DEFAULT 'In Progress'"
            )
        )
        connection.execute(
            text(
                "ALTER TABLE career_roadmaps "
                "ADD COLUMN IF NOT EXISTS last_opened TIMESTAMP"
            )
        )