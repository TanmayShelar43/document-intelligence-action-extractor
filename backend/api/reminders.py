from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.database.models import User
from backend.api.auth import get_current_user
from backend.services import reminder_service


router = APIRouter(
    prefix="/reminders",
    tags=["reminders"]
)


# =========================================================
# REQUEST SCHEMA
# =========================================================

class ReminderCreateRequest(BaseModel):
    task_id: int
    reminder_time: datetime


# =========================================================
# RESPONSE SCHEMA
# =========================================================

class ReminderResponse(BaseModel):
    id: int
    task_id: int
    reminder_time: datetime
    status: str

    model_config = ConfigDict(
        from_attributes=True
    )


class ReminderDeleteResponse(BaseModel):
    message: str
    id: int


# =========================================================
# CREATE REMINDER
# =========================================================

@router.post(
    "",
    response_model=ReminderResponse,
    status_code=status.HTTP_201_CREATED
)
def create_reminder(
    request: ReminderCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a reminder for a task belonging to the authenticated user.

    M8 only persists the reminder.
    Actual FCM notification sending belongs to M9.
    """

    try:
        reminder = reminder_service.create_reminder(
            db=db,
            task_id=request.task_id,
            user_id=current_user.id,
            reminder_time=request.reminder_time
        )

    except ValueError as exc:
        detail = str(exc)

        if "Task not found" in detail:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=detail
            )

        if "blocked" in detail:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=detail
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

    return reminder


# =========================================================
# LIST REMINDERS
# =========================================================

@router.get(
    "",
    response_model=List[ReminderResponse]
)
def list_reminders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve all reminders belonging to the authenticated user.
    """

    return reminder_service.get_user_reminders(
        db=db,
        user_id=current_user.id
    )


# =========================================================
# DELETE REMINDER
# =========================================================

@router.delete(
    "/{reminder_id}",
    response_model=ReminderDeleteResponse
)
def delete_reminder(
    reminder_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a reminder belonging to the authenticated user.
    """

    reminder = reminder_service.get_user_reminder_by_id(
        db=db,
        reminder_id=reminder_id,
        user_id=current_user.id
    )

    if reminder is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found"
        )

    reminder_service.delete_reminder(
        db=db,
        reminder=reminder
    )

    return ReminderDeleteResponse(
        message="Reminder deleted successfully",
        id=reminder_id
    )