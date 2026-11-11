#https://fastapi.tiangolo.com/reference/apirouter/

from typing_extensions import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from select import select
from api import models
from api.database import get_db

router = APIRouter()

templates = Jinja2Templates(directory="../frontend/templates")

@router.get("/", include_in_schema=False, name="home")
@router.get("/overview", include_in_schema=False, name="overview")
async def overview(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/index.html",
        context={"request": request}
    )

@router.get("/schedule", name="schedule")
def schedule(request: Request, db: Annotated[Session, Depends(get_db)]):
    alarms = db.execute(select(models.Alarm)).scalars().all()
    return templates.TemplateResponse(
        request=request,
        name="pages/schedule.html",
        context={"alarms": alarms},
    )

@router.get("/profile", include_in_schema=False, name="profile")
async def profile(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/profile.html",
        context={"request": request}
    )

@router.get("/time", include_in_schema=False, name="time")
async def time(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/time.html",
        context={"request": request}
    )

@router.get("/login", include_in_schema=False, name="login")
async def login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/login.html",
        context={"request": request}
    )

@router.get("/register", include_in_schema=False, name="register")
async def register(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/register.html",
        context={"request": request}
    )
