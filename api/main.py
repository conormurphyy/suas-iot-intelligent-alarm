from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session
import models
from routes.pages import router as pages_router


app = FastAPI()

app.mount("/media", StaticFiles(directory="../frontend/media"), name="media")
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")

app.include_router(pages_router)