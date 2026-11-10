# Alarm Routes

from select import select
from unittest import result
from unittest import result
from typing_extensions import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from requests import Session
from sqlalchemy.ext.asyncio import AsyncSession
from api import models
from api.database import get_db
from api.schemas import AlarmResponse, AlarmCreate, AlarmUpdate

router = APIRouter(prefix="/api/alarms", tags=["Alarms"])
templates = Jinja2Templates(directory="../frontend/templates")

#Create Alarm
@router.post("/", response_model=AlarmResponse, status_code=status.HTTP_201_CREATED)
async def create_alarm(alarm: AlarmResponse, db: Annotated[Session, Depends(get_db)]):
    new_alarm = models.Alarm(
        user_id=alarm.user_id,
        alarm_time=alarm.alarm_time,
        enabled=alarm.enabled,
        sound_file=alarm.sound_file,
        sound_path=alarm.sound_path
    )
    db.add(new_alarm)
    await db.commit()
    await db.refresh(new_alarm)
    return new_alarm

#Get All Alarms
@router.get("/", response_model=list[AlarmResponse])
async def get_all_alarms(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.Alarm))
    alarms = result.scalars().all()
    
    return alarms

#Get Alarm by ID
@router.get("/api/alarm/{alarm_id}", response_model=AlarmResponse)
async def get_alarm(alarm_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.Alarm).where(models.Alarm.id == alarm_id))
    alarm = result.scalars().first()
    if alarm:
        return alarm
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alarm with id {alarm_id} not found")

#Get Alarm by User ID
@router.get("/api/user/{user_id}/alarms", response_model=list[AlarmResponse])
async def get_user_alarms(user_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.Alarm).where(models.Alarm.user_id == user_id))
    alarms = result.scalars().all()
    if not alarms:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No alarms found for user with id {user_id}")
    return alarms

#Update Alarm Full
@router.put("/api/alarm/{alarm_id}", response_model=AlarmResponse)
async def update_alarm(alarm_id: int, alarm: AlarmUpdate, db: Annotated
[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.Alarm).where(models.Alarm.id == alarm_id))
    existing_alarm = result.scalars().first()
    if existing_alarm:
        existing_alarm.user_id = alarm.user_id
        existing_alarm.status = alarm.status
        existing_alarm.timestamp = alarm.timestamp
        await db.commit()
        return existing_alarm
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alarm with id {alarm_id} not found")

#Update Alarm Partial
@router.patch("/api/alarm/{alarm_id}", response_model=AlarmResponse)
async def update_alarm_partial(alarm_id: int, alarm: AlarmUpdate, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.Alarm).where(models.Alarm.id == alarm_id))
    existing_alarm = result.scalars().first()
    if existing_alarm:
        if alarm.user_id is not None:
            existing_alarm.user_id = alarm.user_id
        if alarm.status is not None:
            existing_alarm.status = alarm.status
        if alarm.timestamp is not None:
            existing_alarm.timestamp = alarm.timestamp
        await db.commit()
        return existing_alarm
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alarm with id {alarm_id} not found")

#Delete Alarm
@router.delete("/api/alarm/{alarm_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_alarm(alarm_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.Alarm).where(models.Alarm.id == alarm_id))
    existing_alarm = result.scalars().first()
    if existing_alarm:
        await db.delete(existing_alarm)
        await db.commit()
        return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alarm with id {alarm_id} not found")
