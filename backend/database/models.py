from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from backend.database.database import Base


class User(Base):
    """
    User model representing registered users in the database.
    Required for authentication and user isolation across all resources.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, server_default=func.now())

    documents = relationship("Document", back_populates="owner", cascade="all, delete-orphan")


class Document(Base):
    """
    Document model representing uploaded user documents in PostgreSQL.
    """
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    file_path = Column(String, nullable=False)
    processing_status = Column(String, nullable=False, default="pending")
    uploaded_at = Column(DateTime, nullable=False, default=datetime.utcnow, server_default=func.now())

    owner = relationship("User", back_populates="documents")
    pages = relationship("DocumentPage", back_populates="document", cascade="all, delete-orphan")


class DocumentPage(Base):
    """
    DocumentPage model storing page-level text extraction and scanned status.
    """
    __tablename__ = "document_pages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    page_number = Column(Integer, nullable=False)
    content = Column(Text, nullable=True)
    is_scanned = Column(Boolean, nullable=False, default=False)

    document = relationship("Document", back_populates="pages")

