"""
Document Intelligence & Action Extractor
Backend — Milestone 9: Push Notifications
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.database.database import engine, Base

from backend.api.auth import router as auth_router
from backend.api.documents import router as documents_router
from backend.api.analysis import router as analysis_router
from backend.api.tasks import router as tasks_router
from backend.api.reminders import router as reminders_router

from backend.services.scheduler import (
    start_scheduler,
    stop_scheduler
)


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(
        f"Warning: Database creation on startup: {e}"
    )


# =========================================================
# APPLICATION LIFESPAN
# =========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown lifecycle.

    Starts the reminder scheduler when the application starts
    and stops it when the application shuts down.
    """

    # Start reminder scheduler
    start_scheduler()

    yield

    # Stop reminder scheduler
    stop_scheduler()


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="Document Intelligence & Action Extractor",
    description=(
        "Backend API for the Document Intelligence "
        "& Action Extractor mobile application."
    ),
    version="0.9.0",
    lifespan=lifespan,
)


# =========================================================
# ROUTERS
# =========================================================

app.include_router(auth_router)
app.include_router(documents_router)
app.include_router(analysis_router)
app.include_router(tasks_router)
app.include_router(reminders_router)


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health_check():
    """
    Health check endpoint.

    Returns:
        {"status": "ok"}
    """

    return {
        "status": "ok"
    }