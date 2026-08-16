import logging
from typing import List
from sqlalchemy.orm import Session

from backend.database.models import Document, DocumentPage
from backend.document_parser.validator import validate_document_file
from backend.document_parser.pdf_parser import parse_pdf
from backend.document_parser.docx_parser import parse_docx
from backend.document_parser.image_processor import process_image

logger = logging.getLogger(__name__)


def parse_document(db: Session, document: Document) -> List[DocumentPage]:
    """
    Service function orchestrating document parsing:
    1. Validates document file.
    2. Updates processing_status to 'processing'.
    3. Delegates to appropriate format parser (PDF, DOCX, Image).
    4. Purges old document_pages for document_id (idempotent re-parsing).
    5. Saves parsed DocumentPage records to PostgreSQL.
    6. Updates processing_status to 'complete' (or 'failed' on error).
    """
    try:
        # Step 1: Validate file existence and non-zero size
        validate_document_file(document.file_path)

        # Step 2: Mark status as 'processing'
        document.processing_status = "processing"
        db.commit()

        # Step 3: Route file by type
        file_type = document.file_type.lower()
        if file_type == "pdf":
            parsed_pages = parse_pdf(document.file_path)
        elif file_type in ("docx", "doc"):
            parsed_pages = parse_docx(document.file_path)
        elif file_type in ("jpg", "jpeg", "png", "webp", "heic"):
            parsed_pages = process_image(document.file_path)
        else:
            raise ValueError(f"Unsupported file format '{file_type}' for parsing")

        if not parsed_pages:
            document.processing_status = "failed"
            db.commit()
            return []

        # Step 4: Purge old page records for this document (idempotency)
        db.query(DocumentPage).filter(DocumentPage.document_id == document.id).delete()

        # Step 5: Save new DocumentPage records
        created_pages = []
        for page_info in parsed_pages:
            page_record = DocumentPage(
                document_id=document.id,
                page_number=page_info["page_number"],
                content=page_info["content"],
                is_scanned=page_info["is_scanned"]
            )
            db.add(page_record)
            created_pages.append(page_record)

        # Step 6: Mark status as 'complete'
        document.processing_status = "complete"
        db.commit()
        for p in created_pages:
            db.refresh(p)

        return created_pages

    except Exception as e:
        logger.error(f"Parsing failed for document id={document.id}: {e}")
        db.rollback()
        document.processing_status = "failed"
        db.commit()
        return []
