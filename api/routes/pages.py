#https://fastapi.tiangolo.com/reference/apirouter/

from typing_extensions import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session
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
    user = _get_or_create_demo_user(db)
    alarms = db.execute(select(models.Alarm)).scalars().all()
    return templates.TemplateResponse(
        request=request,
        name="pages/schedule.html",
        context={"alarms": alarms, "user": user},
    )


def _get_or_create_demo_user(db: Session) -> models.User:
    """Return the first user, creating a demo user if none exists yet.

    There is no authentication yet, so the schedule page needs a concrete
    user_id to attach newly created alarms to.
    """
    user = db.execute(select(models.User)).scalars().first()
    if user is None:
        user = models.User(
            username="demo",
            email="demo@suas.local",
            password="demo1234",
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

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
