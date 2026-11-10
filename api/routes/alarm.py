# Alarm Routes

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas import AlarmResponse, AlarmCreate, AlarmUpdate

router = APIRouter(prefix="/api/alarms", tags=["Alarms"])
templates = Jinja2Templates(directory="../frontend/templates")

#Create Alarm
@router.post("/", response_model=AlarmResponse, status_code=status.HTTP_201_CREATED)
def create_alarm(alarm: AlarmResponse, db: Annotated[Session, Depends(get_db)]):
    new_alarm = models.Alarm(
        user_id=alarm.user_id,
        alarm_time=alarm.alarm_time,
        enabled=alarm.enabled,
        sound_file=alarm.sound_file,
        sound_path=alarm.sound_path
    )
    db.add(new_alarm)
    db.commit()
    db.refresh(new_alarm)
    return new_alarm

#Get All Alarms
@router.get("/", response_model=list[AlarmResponse])
def get_all_alarms(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Alarm))
    alarms = result.scalars().all()
    
    return alarms

#Get Alarm by ID
@router.get("/{alarm_id}", response_model=AlarmResponse)
def get_alarm(alarm_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Alarm).where(models.Alarm.id == alarm_id))
    alarm = result.scalars().first()
    if alarm:
        return alarm
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alarm with id {alarm_id} not found")

#Get Alarm by User ID
@router.get("/{user_id}/alarms", response_model=list[AlarmResponse])
def get_user_alarms(user_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Alarm).where(models.Alarm.user_id == user_id))
    alarms = result.scalars().all()
    if not alarms:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No alarms found for user with id {user_id}")
    return alarms

#Update Alarm Full
@router.put("/{alarm_id}", response_model=AlarmResponse)
def update_alarm(alarm_id: int, alarm: AlarmUpdate, db: Annotated
[Session, Depends(get_db)]):
    result = db.execute(select(models.Alarm).where(models.Alarm.id == alarm_id))
    existing_alarm = result.scalars().first()
    if existing_alarm:
        existing_alarm.user_id = alarm.user_id
        existing_alarm.status = alarm.status
        existing_alarm.timestamp = alarm.timestamp
        db.commit()
        return existing_alarm
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alarm with id {alarm_id} not found")

#Update Alarm Partial
@router.patch("/{alarm_id}", response_model=AlarmResponse)
def update_alarm_partial(alarm_id: int, alarm: AlarmUpdate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Alarm).where(models.Alarm.id == alarm_id))
    existing_alarm = result.scalars().first()
    if existing_alarm:
        if alarm.user_id is not None:
            existing_alarm.user_id = alarm.user_id
        if alarm.status is not None:
            existing_alarm.status = alarm.status
        if alarm.timestamp is not None:
            existing_alarm.timestamp = alarm.timestamp
        db.commit()
        return existing_alarm
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alarm with id {alarm_id} not found")

#Delete Alarm
@router.delete("/{alarm_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alarm(alarm_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Alarm).where(models.Alarm.id == alarm_id))
    existing_alarm = result.scalars().first()
    if existing_alarm:
        db.delete(existing_alarm)
        db.commit()
        return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alarm with id {alarm_id} not found")
