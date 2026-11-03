from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session
import models



app = FastAPI()

app.mount("/media", StaticFiles(directory="../frontend/media"), name="media")

app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")
templates = Jinja2Templates(directory="../frontend/templates")

# Get reqs for pages
@app.get("/", include_in_schema=False, name="home")
@app.get("/overview", include_in_schema=False, name="overview")
async def overview(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/index.html",
        context={"request": request}
    )

@app.get("/analytics", include_in_schema=False, name="analytics")
async def analytics(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/analytics.html",
        context={"request": request}
    )

@app.get("/schedule", include_in_schema=False, name="schedule")
async def schedule(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/schedule.html",
        context={"request": request}
    )

@app.get("/profile", include_in_schema=False, name="profile")
async def profile(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/profile.html",
        context={"request": request}
    )

