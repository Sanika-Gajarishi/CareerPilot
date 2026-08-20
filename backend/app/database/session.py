from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.database.base import Base

# Register all models
import app.database

print("=" * 80)
print("DATABASE_URL:", settings.DATABASE_URL)
print("=" * 80)

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)

# Create all database tables
Base.metadata.create_all(bind=engine)

# Temporary Debug
with engine.connect() as conn:
    print(
        "Current Database:",
        conn.execute(
            text("SELECT current_database()")
        ).scalar(),
    )

    print(
        "Search Path:",
        conn.execute(
            text("SHOW search_path")
        ).scalar(),
    )

    rows = conn.execute(
        text(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'resumes'
            ORDER BY ordinal_position
            """
        )
    ).fetchall()

    print("Resume Columns:", rows)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()