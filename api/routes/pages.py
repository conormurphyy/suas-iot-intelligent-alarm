#https://fastapi.tiangolo.com/reference/apirouter/

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

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

@router.get("/analytics", include_in_schema=False, name="analytics")
async def analytics(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/analytics.html",
        context={"request": request}
    )

@router.get("/schedule", include_in_schema=False, name="schedule")
async def schedule(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/schedule.html",
        context={"request": request}
    )

@router.get("/profile", include_in_schema=False, name="profile")
async def profile(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/profile.html",
        context={"request": request}
    )