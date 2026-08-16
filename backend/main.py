"""
Document Intelligence & Action Extractor
Backend — Milestone 3: Document Upload & Storage
"""

from fastapi import FastAPI
from backend.database.database import engine, Base
from backend.api.auth import router as auth_router
from backend.api.documents import router as documents_router
from backend.api.analysis import router as analysis_router

# Create database tables automatically if they do not exist
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    # Log warning if DB creation fails on startup (e.g. if DB server isn't running yet)
    print(f"Warning: Database creation on startup: {e}")

app = FastAPI(
    title="Document Intelligence & Action Extractor",
    description="Backend API for the Document Intelligence & Action Extractor mobile application.",
    version="0.5.0",
)

# Register routers
app.include_router(auth_router)
app.include_router(documents_router)
app.include_router(analysis_router)



@app.get("/health")
def health_check():
    """
    Health check endpoint.
    Returns {"status": "ok"} when the server is running.
    """
    return {"status": "ok"}
