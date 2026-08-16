"""
Document Intelligence & Action Extractor
Backend — Milestone 2: Database & Authentication
"""

from fastapi import FastAPI
from backend.database.database import engine, Base
from backend.api.auth import router as auth_router

# Create database tables automatically if they do not exist
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    # Log warning if DB creation fails on startup (e.g. if DB server isn't running yet)
    print(f"Warning: Database creation on startup: {e}")

app = FastAPI(
    title="Document Intelligence & Action Extractor",
    description="Backend API for the Document Intelligence & Action Extractor mobile application.",
    version="0.2.0",
)

# Register routers
app.include_router(auth_router)


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    Returns {"status": "ok"} when the server is running.
    """
    return {"status": "ok"}
