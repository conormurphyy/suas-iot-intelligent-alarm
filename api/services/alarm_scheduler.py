from datetime import datetime, UTC

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from sqlalchemy.orm import Session

from api.database import SessionLocal
from api.models import Alarm


# Initialise scheduler
scheduler = BackgroundScheduler(timezone="Europe/Dublin")


# Trigger alarm
def trigger_alarm(alarm_id: int, client):

    db: Session = SessionLocal()

    try:
        alarm = db.query(Alarm).filter(
            Alarm.id == alarm_id
        ).first()

        if alarm is None or not alarm.enabled:
            return

        # Disable one-shot alarm
        alarm.enabled = False
        db.commit()

    finally:
        db.close()

    print(f"Alarm {alarm_id} triggered!")

    client.publish("alarm/trigger", "on")


# Schedule alarm
def schedule_alarm(alarm: Alarm, client):

    job_id = str(alarm.id)

    remove_alarm(alarm.id)

    if not alarm.enabled:
        return

    alarm_time = alarm.alarm_time

    # Handle SQLite timezone behaviour
    if alarm_time.tzinfo is None:
        alarm_time = alarm_time.replace(tzinfo=UTC)
    else:
        alarm_time = alarm_time.astimezone(UTC)

    if alarm_time <= datetime.now(UTC):
        return

    scheduler.add_job(
        trigger_alarm,
        trigger=DateTrigger(run_date=alarm_time),
        args=[alarm.id, client],
        id=job_id,
        replace_existing=True
    )

    print(f"Alarm {alarm.id} scheduled for {alarm_time}")


# Remove alarm
def remove_alarm(alarm_id: int):

    job_id = str(alarm_id)

    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)


# Load existing alarms
def load_alarms(client):

    db: Session = SessionLocal()

    try:
        alarms = db.query(Alarm).filter(
            Alarm.enabled == True
        ).all()

        for alarm in alarms:
            schedule_alarm(alarm, client)

    finally:
        db.close()

    print("Existing alarms loaded")
