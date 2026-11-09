# Reading Routes

from select import select
from unittest import result
from unittest import result
from typing_extensions import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from requests import Session

from api import models
from api.database import get_db
from api.schemas import UserResponse

router = APIRouter(prefix="/api/readings", tags=["Readings"])
templates = Jinja2Templates(directory="../frontend/templates")

@router.get("/api/readings", response_model=list[UserResponse])
async def get_all_readings(db: Annotated[Session, Depends(get_db)]):
    result = await db.execute(select(models.Reading))
    readings = result.scalars().all()
    if readings.count() == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No readings found")
    return readings

@router.get("/api/reading/{reading_id}", response_model=UserResponse)
async def get_reading(reading_id: int, db: Annotated[Session, Depends(get_db)]):
    result = await db.execute(select(models.Reading).where(models.Reading.id == reading_id))
    reading = result.scalars().first()
    if reading:
        return reading
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reading with id {reading_id} not found")
