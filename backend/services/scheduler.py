from apscheduler.schedulers.background import BackgroundScheduler

from backend.database.database import SessionLocal
from backend.services.reminder_service import process_pending_reminders


scheduler = BackgroundScheduler()


def run_reminder_scheduler():
    """
    Process pending reminders using a fresh database session.
    """

    db = SessionLocal()

    try:
        process_pending_reminders(db)
    finally:
        db.close()


def start_scheduler():
    """
    Start APScheduler.
    """

    if not scheduler.running:

        scheduler.add_job(
            run_reminder_scheduler,
            "interval",
            minutes=1,
            id="reminder_processor",
            replace_existing=True
        )

        scheduler.start()


def stop_scheduler():
    """
    Stop APScheduler.
    """

    if scheduler.running:
        scheduler.shutdown()