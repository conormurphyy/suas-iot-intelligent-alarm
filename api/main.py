from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import Base
import models
from routes.pages import router as pages_router

Base.metadata.create_all(bind=models.engine)

app = FastAPI(title ="Suas IoT Intelligent Alarm API")

app.mount("/media", StaticFiles(directory="../frontend/media"), name="media")
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")

app.include_router(pages_router)
app.include_router(users_router)
