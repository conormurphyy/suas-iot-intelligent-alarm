# Alarm Routes

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

router = APIRouter(prefix="/api/alarms", tags=["Alarms"])
templates = Jinja2Templates(directory="../frontend/templates")

#Create Alarm

#Get All Alarms

#Get Alarm by ID

#Update Alarm Full

#Update Alarm Partial

#Delete Alarm
