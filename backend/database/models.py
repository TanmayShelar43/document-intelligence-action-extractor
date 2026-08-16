from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, func
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
