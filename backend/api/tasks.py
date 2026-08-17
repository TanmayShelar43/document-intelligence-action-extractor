from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.database.models import User
from backend.api.auth import get_current_user
from backend.services import task_service


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


# =========================================================
# REQUEST SCHEMAS
# =========================================================

class TaskCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: Optional[str] = None
    priority: str = "MEDIUM"
    action_id: Optional[int] = None
    confirmed: bool = False


class TaskUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None


# =========================================================
# RESPONSE SCHEMA
# =========================================================

class TaskResponse(BaseModel):
    id: int
    user_id: int
    action_id: Optional[int]
    title: str
    description: Optional[str]
    deadline: Optional[str]
    priority: str
    status: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class TaskDeleteResponse(BaseModel):
    message: str
    id: int


# =========================================================
# CREATE TASK
# =========================================================

@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    request: TaskCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a task for the authenticated user.

    Manual task:
        action_id = null

    Extracted task:
        action_id contains an existing Action ID.

    Low-confidence extracted actions require:
        confirmed = true
    """

    title = request.title.strip()

    if not title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title must not be empty"
        )

    try:
        task = task_service.create_task(
            db=db,
            user_id=current_user.id,
            title=title,
            description=request.description,
            deadline=request.deadline,
            priority=request.priority,
            action_id=request.action_id,
            confirmed=request.confirmed
        )

    except ValueError as exc:
        detail = str(exc)

        if detail == "Action not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=detail
            )

        if "requires explicit confirmation" in detail:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=detail
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

    return task


# =========================================================
# LIST TASKS
# =========================================================

@router.get(
    "",
    response_model=List[TaskResponse]
)
def list_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve all tasks belonging to the authenticated user.
    """

    return task_service.get_user_tasks(
        db=db,
        user_id=current_user.id
    )


# =========================================================
# UPDATE TASK
# =========================================================

@router.patch(
    "/{task_id}",
    response_model=TaskResponse
)
def update_task(
    task_id: int,
    request: TaskUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a task belonging to the authenticated user.
    """

    task = task_service.get_user_task_by_id(
        db=db,
        task_id=task_id,
        user_id=current_user.id
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    try:
        return task_service.update_task(
            db=db,
            task=task,
            title=request.title,
            description=request.description,
            deadline=request.deadline,
            priority=request.priority,
            status=request.status
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )


# =========================================================
# DELETE TASK
# =========================================================

@router.delete(
    "/{task_id}",
    response_model=TaskDeleteResponse
)
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a task belonging to the authenticated user.
    """

    task = task_service.get_user_task_by_id(
        db=db,
        task_id=task_id,
        user_id=current_user.id
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    task_service.delete_task(
        db=db,
        task=task
    )

    return TaskDeleteResponse(
        message="Task deleted successfully",
        id=task_id
    )