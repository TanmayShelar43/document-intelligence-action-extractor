import logging
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session

from backend.database.models import Document, Action, Fee, Risk
from backend.services import parsing_service
from backend.ai import extraction

logger = logging.getLogger(__name__)


def analyze_document(
    db: Session,
    document: Document,
    client_mock: Optional[Any] = None
) -> Document:
    """
    Executes AI Document Intelligence extraction workflow for document:
    1. Verifies/runs M4 document parsing if pages do not exist.
    2. Updates processing_status to 'processing'.
    3. Calls Gemini AI extraction module with M4 document pages.
    4. Validates output with Pydantic.
    5. Persists actions, fees, risks, summary, required_documents, and people to PostgreSQL.
    6. Updates processing_status to 'complete' (or 'failed' on error).
    """
    # Ensure document pages from M4 exist
    if not document.pages:
        parsing_service.parse_document(db, document)
        db.refresh(document)

    if not document.pages:
        document.processing_status = "failed"
        db.commit()
        raise ValueError("Document contains no parsed pages for AI analysis")

    try:
        # Mark status as 'processing'
        document.processing_status = "processing"
        db.commit()

        # Call Gemini extraction with M4 page content
        extracted_data = extraction.extract_information_from_pages(
            pages=document.pages,
            file_path=document.file_path,
            client_mock=client_mock
        )

        # Clear previous AI extraction results (idempotent re-analysis)
        db.query(Action).filter(Action.document_id == document.id).delete()
        db.query(Fee).filter(Fee.document_id == document.id).delete()
        db.query(Risk).filter(Risk.document_id == document.id).delete()

        # Save summary, required_documents, and people on document record
        document.summary = extracted_data.summary
        document.required_documents = extracted_data.required_documents
        document.people = [p.model_dump() for p in extracted_data.people]

        # Save Actions
        for act in extracted_data.actions:
            action_record = Action(
                document_id=document.id,
                title=act.title,
                description=act.description,
                deadline=act.deadline,
                deadline_type=act.deadline_type,
                priority=act.priority,
                confidence=act.confidence,
                source_page=act.source_page
            )
            db.add(action_record)

        # Save Fees
        for fee_item in extracted_data.fees:
            fee_record = Fee(
                document_id=document.id,
                amount=fee_item.amount,
                currency=fee_item.currency,
                purpose=fee_item.purpose,
                confidence=fee_item.confidence,
                source_page=fee_item.source_page
            )
            db.add(fee_record)

        # Save Risks
        for risk_item in extracted_data.risks:
            risk_record = Risk(
                document_id=document.id,
                description=risk_item.description,
                severity=risk_item.severity,
                confidence=risk_item.confidence,
                source_page=risk_item.source_page
            )
            db.add(risk_record)

        # Mark status as 'complete'
        document.processing_status = "complete"
        db.commit()
        db.refresh(document)
        return document

    except Exception as e:
        logger.error(f"Analysis failed for document id={document.id}: {e}")
        db.rollback()
        document.processing_status = "failed"
        db.commit()
        raise e


def get_document_analysis_payload(db: Session, document_id: int, user_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieves complete M5 AI analysis payload for document owned strictly by user_id.
    Returns None if document is not found or belongs to another user.
    """
    doc = db.query(Document).filter(Document.id == document_id, Document.user_id == user_id).first()
    if not doc:
        return None

    actions = db.query(Action).filter(Action.document_id == doc.id).all()
    fees = db.query(Fee).filter(Fee.document_id == doc.id).all()
    risks = db.query(Risk).filter(Risk.document_id == doc.id).all()

    return {
        "document_id": doc.id,
        "filename": doc.filename,
        "processing_status": doc.processing_status,
        "summary": doc.summary or "",
        "actions": actions,
        "fees": fees,
        "risks": risks,
        "required_documents": doc.required_documents or [],
        "people": doc.people or []
    }
