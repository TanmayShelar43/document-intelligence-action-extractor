import os
import uuid
from typing import List, Optional
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.models import Document

ALLOWED_EXTENSIONS = {"pdf", "doc", "docx", "jpg", "jpeg", "png", "webp", "heic"}

# Storage directory under backend/uploads
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.getenv("UPLOAD_DIR", os.path.join(BASE_DIR, "uploads"))


def validate_file_extension(filename: str) -> str:
    """
    Validates file extension against allowed document types.
    Returns normalized lower-case extension string.
    Raises HTTPException 400 if unsupported or filename is empty.
    """
    if not filename or "." not in filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file name or missing file extension."
        )
    ext = filename.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type '{ext}'. Allowed types: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )
    return ext


def save_file_to_disk(file: UploadFile, user_id: int, file_ext: str) -> tuple[str, int]:
    """
    Saves UploadFile to local backend filesystem isolated in uploads/{user_id}/ directory.
    Returns tuple of (stored_file_path, file_size_in_bytes).
    """
    user_upload_dir = os.path.join(UPLOAD_DIR, str(user_id))
    os.makedirs(user_upload_dir, exist_ok=True)

    # Generate a unique stored filename to prevent collisions while preserving original extension
    unique_filename = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(user_upload_dir, unique_filename)

    # Save content to disk and measure file size
    bytes_written = 0
    try:
        with open(file_path, "wb") as buffer:
            while chunk := file.file.read(8192):
                buffer.write(chunk)
                bytes_written += len(chunk)
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file on disk: {str(e)}"
        )

    if bytes_written == 0:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty (0 bytes)."
        )

    return file_path, bytes_written


def create_document(
    db: Session,
    user_id: int,
    filename: str,
    file_type: str,
    file_size: int,
    file_path: str
) -> Document:
    """
    Creates and persists document record in PostgreSQL.
    """
    doc = Document(
        user_id=user_id,
        filename=filename,
        file_type=file_type,
        file_size=file_size,
        file_path=file_path,
        processing_status="pending"
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def get_user_documents(db: Session, user_id: int) -> List[Document]:
    """
    Retrieves all documents belonging exclusively to user_id.
    """
    return db.query(Document).filter(Document.user_id == user_id).order_by(Document.uploaded_at.desc()).all()


def get_user_document_by_id(db: Session, document_id: int, user_id: int) -> Optional[Document]:
    """
    Retrieves document by ID strictly verifying user_id ownership.
    Returns None if document does not exist or belongs to another user.
    """
    return db.query(Document).filter(Document.id == document_id, Document.user_id == user_id).first()


def delete_user_document(db: Session, document_id: int, user_id: int) -> bool:
    """
    Deletes document record from database and removes underlying file from disk.
    Strictly scoped to user_id ownership.
    Returns True if deleted, False if document not found / forbidden.
    """
    doc = get_user_document_by_id(db, document_id=document_id, user_id=user_id)
    if not doc:
        return False

    # Delete physical file from disk if present
    if doc.file_path and os.path.exists(doc.file_path):
        try:
            os.remove(doc.file_path)
        except OSError as e:
            print(f"Warning: Failed to delete physical file {doc.file_path}: {e}")

    # Delete record from database
    db.delete(doc)
    db.commit()
    return True
