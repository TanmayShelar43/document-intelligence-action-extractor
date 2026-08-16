"""
Document Intelligence & Action Extractor
Backend — Milestone 1: FastAPI Skeleton

Scope: GET /health only.
No database, no authentication, no Gemini, no document handling.
"""

from fastapi import FastAPI

app = FastAPI(
    title="Document Intelligence & Action Extractor",
    description="Backend API for the Document Intelligence & Action Extractor mobile application.",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    Returns {"status": "ok"} when the server is running.
    """
    return {"status": "ok"}
