from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.database.models import User
from backend.api.auth import get_current_user
from backend.services import document_service

router = APIRouter(prefix="/documents", tags=["documents"])


class DocumentResponse(BaseModel):
    id: int
    user_id: int
    filename: str
    file_type: str
    file_size: int
    file_path: str
    processing_status: str
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DocumentDeleteResponse(BaseModel):
    message: str
    id: int


@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload a document.
    Validates supported file extension, saves file to local backend storage,
    creates metadata record in PostgreSQL, and returns document response.
    Requires valid JWT token.
    """
    file_ext = document_service.validate_file_extension(file.filename)
    file_path, file_size = document_service.save_file_to_disk(file, current_user.id, file_ext)

    doc = document_service.create_document(
        db=db,
        user_id=current_user.id,
        filename=file.filename,
        file_type=file_ext,
        file_size=file_size,
        file_path=file_path
    )
    return doc


@router.get("", response_model=List[DocumentResponse])
def list_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve list of uploaded documents belonging to authenticated user.
    Requires valid JWT token. Enforces strict user isolation.
    """
    return document_service.get_user_documents(db, current_user.id)


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve document details by ID for authenticated user.
    Returns 404 Not Found if document does not exist or belongs to another user.
    """
    doc = document_service.get_user_document_by_id(db, document_id, current_user.id)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    return doc


@router.delete("/{document_id}", response_model=DocumentDeleteResponse)
def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete document metadata and physical file for authenticated user.
    Returns 404 Not Found if document does not exist or belongs to another user.
    """
    success = document_service.delete_user_document(db, document_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    return DocumentDeleteResponse(
        message="Document deleted successfully",
        id=document_id
    )
