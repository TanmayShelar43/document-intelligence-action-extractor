from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from backend.database.models import Task, Action


def create_task(
    db: Session,
    user_id: int,
    title: str,
    description: Optional[str],
    deadline: Optional[str],
    priority: str,
    action_id: Optional[int] = None,
    confirmed: bool = False
) -> Task:
    """
    Create a task belonging to the authenticated user.

    Manual task:
        action_id = None

    Extracted task:
        action_id = Action.id

    If an extracted action has confidence below 0.60,
    explicit user confirmation is required.
    """

    # ---------------------------------------------------------
    # VALIDATE EXTRACTED ACTION
    # ---------------------------------------------------------
    action = None

    if action_id is not None:
        action = (
            db.query(Action)
            .filter(Action.id == action_id)
            .first()
        )

        if action is None:
            raise ValueError("Action not found")

        # NEEDS VERIFICATION gate
        if action.confidence < 0.60 and not confirmed:
            raise ValueError(
                "Task creation blocked: action requires "
                "explicit confirmation because confidence "
                "is below 0.60"
            )

        # Make sure the action belongs to a document
        # that belongs to this user.
        document = action.document

        if document is None or document.user_id != user_id:
            raise ValueError("Action not found")

    # ---------------------------------------------------------
    # CREATE TASK
    # ---------------------------------------------------------
    task = Task(
        user_id=user_id,
        action_id=action_id,
        title=title.strip(),
        description=description.strip() if description else None,
        deadline=deadline,
        priority=priority,
        status="pending"
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_user_tasks(
    db: Session,
    user_id: int
):
    """
    Retrieve all tasks belonging to the authenticated user.
    """

    return (
        db.query(Task)
        .filter(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
        .all()
    )


def get_user_task_by_id(
    db: Session,
    task_id: int,
    user_id: int
) -> Optional[Task]:
    """
    Retrieve a single task only if it belongs to
    the authenticated user.
    """

    return (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.user_id == user_id
        )
        .first()
    )


def update_task(
    db: Session,
    task: Task,
    title: Optional[str] = None,
    description: Optional[str] = None,
    deadline: Optional[str] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None
) -> Task:
    """
    Update editable task fields.
    """

    if title is not None:
        cleaned_title = title.strip()

        if not cleaned_title:
            raise ValueError("Task title must not be empty")

        task.title = cleaned_title

    if description is not None:
        task.description = description.strip()

    if deadline is not None:
        task.deadline = deadline

    if priority is not None:
        task.priority = priority

    if status is not None:
        task.status = status

    db.commit()
    db.refresh(task)

    return task


def delete_task(
    db: Session,
    task: Task
) -> None:
    """
    Delete a task.
    """

    db.delete(task)
    db.commit()