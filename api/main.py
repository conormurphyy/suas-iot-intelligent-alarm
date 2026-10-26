from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session
import models



app = FastAPI()

app.mount("/media", StaticFiles(directory="media"), name="media")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", include_in_schema=False, name="home")
@app.get("/overview", include_in_schema=False, name="overview")
async def overview(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/index.html",
        context={"request": request}
    )