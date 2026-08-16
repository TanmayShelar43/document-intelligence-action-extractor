from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.database.models import User, Document
from backend.api.auth import get_current_user
from backend.services import analysis_service

router = APIRouter(prefix="/documents", tags=["analysis"])


class ActionResponse(BaseModel):
    id: int
    document_id: int
    title: str
    description: str
    deadline: Optional[str] = None
    deadline_type: Optional[str] = None
    priority: str
    confidence: float
    source_page: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class FeeResponse(BaseModel):
    id: int
    document_id: int
    amount: float
    currency: str
    purpose: str
    confidence: float
    source_page: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class RiskResponse(BaseModel):
    id: int
    document_id: int
    description: str
    severity: str
    confidence: float
    source_page: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class AnalysisResultResponse(BaseModel):
    document_id: int
    filename: str
    processing_status: str
    summary: Optional[str] = ""
    actions: List[ActionResponse] = []
    fees: List[FeeResponse] = []
    risks: List[RiskResponse] = []
    required_documents: List[str] = []
    people: List[Any] = []

    model_config = ConfigDict(from_attributes=True)


@router.post("/{document_id}/analyze", response_model=AnalysisResultResponse)
def analyze_document_endpoint(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Triggers Gemini AI Document Intelligence analysis on document owned by current_user.
    Strictly verifies document ownership (returns 404 if missing or owned by another user).
    Calls Gemini API, validates output with Pydantic, persists actions/fees/risks/summary,
    and returns complete analysis response.
    """
    doc = db.query(Document).filter(Document.id == document_id, Document.user_id == current_user.id).first()
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    try:
        analysis_service.analyze_document(db, doc)
    except ValueError as val_err:
        err_msg = str(val_err)
        if "GEMINI_API_KEY" in err_msg:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="GEMINI_API_KEY environment variable is missing on server"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Analysis failed: {err_msg}"
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Gemini AI extraction error: {str(exc)}"
        )

    payload = analysis_service.get_document_analysis_payload(db, document_id, current_user.id)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    return payload


@router.get("/{document_id}/analysis", response_model=AnalysisResultResponse)
def get_document_analysis_endpoint(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieves existing AI analysis results for document owned by current_user.
    Strictly verifies document ownership (returns 404 if missing or owned by another user).
    """
    payload = analysis_service.get_document_analysis_payload(db, document_id, current_user.id)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    return payload
