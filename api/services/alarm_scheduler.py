from hardware.alarm_controller import run_alarm
from api.database import SessionLocal
from models import Alarm
from sqlalchemy.orm import Session
def trigger_alarm(alarm_id: int):

    db: Session = SessionLocal()

    try:
        alarm = db.query(Alarm).filter(
            Alarm.id == alarm_id
        ).first()

        if alarm is None or not alarm.enabled:
            return

        alarm.enabled = False
        db.commit()

    finally:
        db.close()

    run_alarm()