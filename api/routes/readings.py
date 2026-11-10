# Reading Routes

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas import PressureMatReadingResponse, UserResponse

router = APIRouter(prefix="/api/readings", tags=["Readings"])
templates = Jinja2Templates(directory="../frontend/templates")
 
#Get All Readings
@router.get("/", response_model=list[PressureMatReadingResponse])
def get_all_readings(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Reading))
    readings = result.scalars().all()
    if readings.count() == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No readings found")
    return readings

#Get Reading by ID
@router.get("/{reading_id}", response_model=PressureMatReadingResponse)
def get_reading(reading_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Reading).where(models.Reading.id == reading_id))
    reading = result.scalars().first()
    if reading:
        return reading
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reading with id {reading_id} not found")

#Get Readings by User ID
@router.get("/{user_id}/readings", response_model = list[PressureMatReadingResponse])
def get_user_readings(user_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Reading).where(models.Reading.user_id == user_id))
    readings = result.scalars().all()
    if not readings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No readings found for user with id {user_id}")
    return readings