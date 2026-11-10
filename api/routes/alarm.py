# Alarm Routes

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from api import models
from api.database import get_db
from api.schemas import AlarmBase, AlarmCreate, AlarmResponse, AlarmUpdate

router = APIRouter(prefix="/api/alarms", tags=["Alarms"])


# Create Alarm
@router.post("/", response_model=AlarmResponse, status_code=status.HTTP_201_CREATED)
def create_alarm(alarm: AlarmCreate, db: Annotated[Session, Depends(get_db)]):
    new_alarm = models.Alarm(
        user_id=alarm.user_id,
        alarm_time=alarm.alarm_time,
        enabled=alarm.enabled,
        sound_file=alarm.sound_file,
    )
    db.add(new_alarm)
    db.commit()
    db.refresh(new_alarm)
    return new_alarm


# Get All Alarms
@router.get("/", response_model=list[AlarmResponse])
def get_all_alarms(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Alarm))
    alarms = result.scalars().all()
    return alarms


# Get Alarm by ID
@router.get("/{alarm_id}", response_model=AlarmResponse)
def get_alarm(alarm_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Alarm).where(models.Alarm.id == alarm_id))
    alarm = result.scalars().first()
    if alarm:
        return alarm
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alarm with id {alarm_id} not found")


# Get Alarms by User ID
@router.get("/{user_id}/alarms", response_model=list[AlarmResponse])
def get_user_alarms(user_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Alarm).where(models.Alarm.user_id == user_id))
    alarms = result.scalars().all()
    if not alarms:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No alarms found for user with id {user_id}")
    return alarms


# Update Alarm Full (PUT)
@router.put("/{alarm_id}", response_model=AlarmResponse)
def update_alarm(alarm_id: int, alarm: AlarmBase, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Alarm).where(models.Alarm.id == alarm_id))
    existing_alarm = result.scalars().first()
    if existing_alarm:
        existing_alarm.alarm_time = alarm.alarm_time
        existing_alarm.enabled = alarm.enabled
        existing_alarm.sound_file = alarm.sound_file
        db.commit()
        db.refresh(existing_alarm)
        return existing_alarm
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alarm with id {alarm_id} not found")


# Update Alarm Partial (PATCH)
@router.patch("/{alarm_id}", response_model=AlarmResponse)
def update_alarm_partial(alarm_id: int, alarm: AlarmUpdate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Alarm).where(models.Alarm.id == alarm_id))
    existing_alarm = result.scalars().first()
    if existing_alarm:
        if alarm.alarm_time is not None:
            existing_alarm.alarm_time = alarm.alarm_time
        if alarm.enabled is not None:
            existing_alarm.enabled = alarm.enabled
        if alarm.sound_file is not None:
            existing_alarm.sound_file = alarm.sound_file
        db.commit()
        db.refresh(existing_alarm)
        return existing_alarm
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alarm with id {alarm_id} not found")


# Delete Alarm
@router.delete("/{alarm_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alarm(alarm_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Alarm).where(models.Alarm.id == alarm_id))
    existing_alarm = result.scalars().first()
    if existing_alarm:
        db.delete(existing_alarm)
        db.commit()
        return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alarm with id {alarm_id} not found")