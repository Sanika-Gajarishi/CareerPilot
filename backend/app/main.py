from fastapi import FastAPI
from app.api.router import api_router
from app.core.config import settings
from app.core.logging import logger
from app.database.init_db import create_tables
from app.api.ats import router as ats_router
import app.database
from app.api.jobs import router as job_router
from app.api.roadmap import router as roadmap_router
import app.models
from app.api.v1.users import router as users_router
from app.routers.resume_router import router as resume_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.optimizer import router as optimizer_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)
from app.api.v1.job_tracker import (
    router as job_tracker_router,
)
api_router.include_router(job_tracker_router,)



@app.on_event("startup")
def startup():

    create_tables()

    logger.info("Database Initialized")

    logger.info("CareerPilot Backend Started")



app.include_router(api_router)
app.include_router(ats_router)
app.include_router(job_router)
app.include_router(roadmap_router)
app.include_router(resume_router)
app.include_router(
    users_router,
    prefix="/api/v1",
)
app.include_router(
    dashboard_router,
    prefix="/api/v1",
)
app.include_router(optimizer_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to CareerPilot AI 🚀",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health():

    return {"status": "healthy"}