from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, ForeignKey, JSON, func
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

    # M5 AI Analysis summary & extractions
    summary = Column(Text, nullable=True)
    required_documents = Column(JSON, nullable=True)
    people = Column(JSON, nullable=True)

    owner = relationship("User", back_populates="documents")
    pages = relationship("DocumentPage", back_populates="document", cascade="all, delete-orphan")
    actions = relationship("Action", back_populates="document", cascade="all, delete-orphan")
    fees = relationship("Fee", back_populates="document", cascade="all, delete-orphan")
    risks = relationship("Risk", back_populates="document", cascade="all, delete-orphan")


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


class Action(Base):
    """
    Action model representing extracted action items from AI analysis.
    """
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    deadline = Column(String, nullable=True)
    deadline_type = Column(String, nullable=True)
    priority = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    source_page = Column(Integer, nullable=True)

    document = relationship("Document", back_populates="actions")


class Fee(Base):
    """
    Fee model representing extracted fee requirements from AI analysis.
    """
    __tablename__ = "fees"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    purpose = Column(Text, nullable=False)
    confidence = Column(Float, nullable=False)
    source_page = Column(Integer, nullable=True)

    document = relationship("Document", back_populates="fees")


class Risk(Base):
    """
    Risk model representing extracted risks and penalties from AI analysis.
    """
    __tablename__ = "risks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    description = Column(Text, nullable=False)
    severity = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    source_page = Column(Integer, nullable=True)

    document = relationship("Document", back_populates="risks")


