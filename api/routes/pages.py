# https://fastapi.tiangolo.com/reference/apirouter/

from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from api import models
from api.auth import create_access_token, hash_password, verify_access_token, verify_password
from api.database import get_db

router = APIRouter()

FRONTEND_DIR = Path("frontend") if Path("frontend").exists() else Path("../frontend")
templates = Jinja2Templates(directory=str(FRONTEND_DIR / "templates"))


def _get_logged_in_user(request: Request, db: Session) -> models.User | None:
    token = request.cookies.get("access_token")
    if not token:
        return None
    user_id = verify_access_token(token)
    if user_id is None:
        return None
    try:
        return db.execute(select(models.User).where(models.User.id == int(user_id))).scalars().first()
    except ValueError:
        return None


def _alarm_sort_key(alarm: models.Alarm) -> datetime:
    dt = alarm.alarm_time
    if dt is None:
        return datetime.max.replace(tzinfo=UTC)
    return dt.replace(tzinfo=UTC) if dt.tzinfo is None else dt.astimezone(UTC)


@router.get("/", include_in_schema=False, name="home")
@router.get("/overview", include_in_schema=False, name="overview")
def overview(request: Request, db: Annotated[Session, Depends(get_db)]):
    user = _get_logged_in_user(request, db)
    if user is None:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    alarms = sorted(
        db.execute(select(models.Alarm).where(models.Alarm.user_id == user.id)).scalars().all(),
        key=_alarm_sort_key,
    )
    readings = (
        db.execute(
            select(models.PressureMatReading).where(models.PressureMatReading.user_id == user.id)
        )
        .scalars()
        .all()
    )

    now = datetime.now(UTC)
    next_alarm = None
    upcoming = [alarm for alarm in alarms if alarm.enabled and alarm.alarm_time is not None]
    for alarm in sorted(upcoming, key=lambda a: a.alarm_time):
        alarm_at = alarm.alarm_time
        if alarm_at.tzinfo is None:
            alarm_at = alarm_at.replace(tzinfo=UTC)
        if alarm_at >= now:
            next_alarm = alarm
            break

    return templates.TemplateResponse(
        request=request,
        name="pages/index.html",
        context={
            "request": request,
            "user": user,
            "alarms": alarms,
            "readings": readings,
            "next_alarm": next_alarm,
        },
    )


@router.get("/schedule", include_in_schema=False, name="schedule")
def schedule(request: Request, db: Annotated[Session, Depends(get_db)]):
    user = _get_logged_in_user(request, db)
    if user is None:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    alarms = sorted(
        db.execute(select(models.Alarm).where(models.Alarm.user_id == user.id)).scalars().all(),
        key=_alarm_sort_key,
    )
    return templates.TemplateResponse(
        request=request,
        name="pages/schedule.html",
        context={"alarms": alarms, "user": user},
    )


@router.get("/profile", include_in_schema=False, name="profile")
def profile(request: Request, db: Annotated[Session, Depends(get_db)]):
    user = _get_logged_in_user(request, db)
    if user is None:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(
        request=request,
        name="pages/profile.html",
        context={"request": request, "user": user},
    )


@router.post("/profile", include_in_schema=False, name="profile_update")
def update_profile(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    username: Annotated[str, Form()] = "",
    email: Annotated[str, Form()] = "",
):
    user = _get_logged_in_user(request, db)
    if user is None:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    username = username.strip()
    email = email.strip().lower()

    if username.lower() != user.username.lower():
        existing = db.execute(
            select(models.User).where(func.lower(models.User.username) == username.lower())
        ).scalars().first()
        if existing:
            return templates.TemplateResponse(
                request=request,
                name="pages/profile.html",
                context={"user": user, "error": "Username already exists."},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    if email != user.email.lower():
        existing = db.execute(
            select(models.User).where(func.lower(models.User.email) == email)
        ).scalars().first()
        if existing:
            return templates.TemplateResponse(
                request=request,
                name="pages/profile.html",
                context={"user": user, "error": "Email already exists."},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    user.username = username
    user.email = email
    db.commit()
    db.refresh(user)

    return templates.TemplateResponse(
        request=request,
        name="pages/profile.html",
        context={"user": user, "success": "Profile updated successfully."},
    )


@router.post("/profile/password", include_in_schema=False, name="profile_password")
def update_profile_password(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    current_password: Annotated[str, Form()] = "",
    new_password: Annotated[str, Form()] = "",
    confirm_password: Annotated[str, Form()] = "",
):
    user = _get_logged_in_user(request, db)
    if user is None:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    if not verify_password(current_password, user.password):
        return templates.TemplateResponse(
            request=request,
            name="pages/profile.html",
            context={"user": user, "error": "Current password is incorrect."},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if new_password != confirm_password:
        return templates.TemplateResponse(
            request=request,
            name="pages/profile.html",
            context={"user": user, "error": "New passwords do not match."},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    user.password = hash_password(new_password)
    db.commit()

    return templates.TemplateResponse(
        request=request,
        name="pages/profile.html",
        context={"user": user, "success": "Password updated successfully."},
    )


@router.get("/time", include_in_schema=False, name="time")
async def time(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/time.html",
        context={"request": request},
    )


@router.get("/login", include_in_schema=False, name="login")
def login(request: Request, db: Annotated[Session, Depends(get_db)]):
    if _get_logged_in_user(request, db) is not None:
        return RedirectResponse(url="/overview", status_code=status.HTTP_303_SEE_OTHER)

    success = "Account created. Please sign in." if request.query_params.get("registered") == "1" else None
    return templates.TemplateResponse(
        request=request,
        name="pages/login.html",
        context={"request": request, "success": success},
    )


@router.post("/login", include_in_schema=False, name="login_submit")
def login_submit(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    email: Annotated[str, Form()] = "",
    password: Annotated[str, Form()] = "",
    remember_me: Annotated[str | None, Form()] = None,
):
    user = (
        db.execute(select(models.User).where(func.lower(models.User.email) == email.strip().lower()))
        .scalars()
        .first()
    )
    if not user or not verify_password(password, user.password):
        return templates.TemplateResponse(
            request=request,
            name="pages/login.html",
            context={
                "error": "Incorrect email or password.",
                "form_data": {"email": email.strip()},
            },
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    expires = timedelta(days=7) if remember_me else None
    token = create_access_token(data={"sub": str(user.id)}, expires_delta=expires)

    response = RedirectResponse(url="/overview", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=token, httponly=True, samesite="lax")
    return response


@router.get("/register", include_in_schema=False, name="register")
def register(request: Request, db: Annotated[Session, Depends(get_db)]):
    if _get_logged_in_user(request, db) is not None:
        return RedirectResponse(url="/overview", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(
        request=request,
        name="pages/register.html",
        context={"request": request},
    )


@router.post("/register", include_in_schema=False, name="register_submit")
def register_submit(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    username: Annotated[str, Form()] = "",
    email: Annotated[str, Form()] = "",
    password: Annotated[str, Form()] = "",
    confirm_password: Annotated[str, Form()] = "",
):
    username = username.strip()
    email = email.strip().lower()

    if password != confirm_password:
        return templates.TemplateResponse(
            request=request,
            name="pages/register.html",
            context={
                "error": "Passwords do not match.",
                "form_data": {"username": username, "email": email},
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    existing_user = (
        db.execute(select(models.User).where(func.lower(models.User.username) == username.lower()))
        .scalars()
        .first()
    )
    if existing_user:
        return templates.TemplateResponse(
            request=request,
            name="pages/register.html",
            context={
                "error": "Username already exists.",
                "form_data": {"username": username, "email": email},
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    existing_email = (
        db.execute(select(models.User).where(func.lower(models.User.email) == email))
        .scalars()
        .first()
    )
    if existing_email:
        return templates.TemplateResponse(
            request=request,
            name="pages/register.html",
            context={
                "error": "Email already exists.",
                "form_data": {"username": username, "email": email},
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    new_user = models.User(
        username=username,
        email=email,
        password=hash_password(password),
    )
    db.add(new_user)
    db.commit()

    return RedirectResponse(url="/login?registered=1", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/logout", include_in_schema=False, name="logout")
def logout():
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("access_token")
    return response
