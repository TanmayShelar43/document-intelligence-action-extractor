from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from backend.database.models import Reminder, Task, User
from backend.services.notification_service import send_fcm_notification


# =========================================================
# CREATE REMINDER
# =========================================================

def create_reminder(
    db: Session,
    task: Task,
    reminder_time: datetime
) -> Reminder:
    """
    Create a pending reminder for a task.
    """

    reminder = Reminder(
        task_id=task.id,
        reminder_time=reminder_time,
        status="pending"
    )

    db.add(reminder)
    db.commit()
    db.refresh(reminder)

    return reminder


# =========================================================
# GET USER REMINDERS
# =========================================================

def get_user_reminders(
    db: Session,
    user_id: int
):
    """
    Retrieve all reminders belonging to the authenticated user.
    """

    return (
        db.query(Reminder)
        .join(Task, Reminder.task_id == Task.id)
        .filter(Task.user_id == user_id)
        .order_by(Reminder.reminder_time.asc())
        .all()
    )


# =========================================================
# GET SINGLE REMINDER
# =========================================================

def get_user_reminder_by_id(
    db: Session,
    reminder_id: int,
    user_id: int
) -> Optional[Reminder]:
    """
    Retrieve a reminder only if its task belongs
    to the authenticated user.
    """

    return (
        db.query(Reminder)
        .join(Task, Reminder.task_id == Task.id)
        .filter(
            Reminder.id == reminder_id,
            Task.user_id == user_id
        )
        .first()
    )


# =========================================================
# DELETE REMINDER
# =========================================================

def delete_reminder(
    db: Session,
    reminder: Reminder
) -> None:
    """
    Delete a reminder.
    """

    db.delete(reminder)
    db.commit()


# =========================================================
# PROCESS PENDING REMINDERS
# =========================================================

def process_pending_reminders(
    db: Session
) -> None:
    """
    Find pending reminders whose reminder time has arrived,
    send FCM notifications, and mark successfully sent
    reminders as 'sent'.
    """

    now = datetime.utcnow()

    reminders = (
        db.query(Reminder)
        .join(Task, Reminder.task_id == Task.id)
        .filter(
            Reminder.status == "pending",
            Reminder.reminder_time <= now
        )
        .all()
    )

    for reminder in reminders:

        task = (
            db.query(Task)
            .filter(Task.id == reminder.task_id)
            .first()
        )

        if task is None:
            reminder.status = "cancelled"
            continue

        user = (
            db.query(User)
            .filter(User.id == task.user_id)
            .first()
        )

        if user is None:
            reminder.status = "cancelled"
            continue

        # No FCM token registered.
        if not user.fcm_token:
            continue

        try:

            send_fcm_notification(
                fcm_token=user.fcm_token,
                title="Task Reminder",
                body=(
                    f"{task.title} "
                    f"deadline is {task.deadline}."
                )
            )

            reminder.status = "sent"

        except Exception as exc:

            # Do not mark the reminder as sent
            # if Firebase delivery failed.
            print(
                f"FCM notification failed "
                f"for reminder {reminder.id}: {exc}"
            )

    db.commit()