from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

import api.models
from api.database import Base, engine
from api.routes.alarm import router as alarm_router
from api.routes.pages import router as pages_router
from api.routes.readings import router as readings_router
from api.routes.users import router as users_router
from api.services.alarm_scheduler import load_alarms, scheduler
from api.services.mqtt_client import start_mqtt, stop_mqtt


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_mqtt()
    load_alarms()
    scheduler.start()

    print("Scheduler started")

    yield

    scheduler.shutdown(wait=False)
    stop_mqtt()


templates = Jinja2Templates(directory="../frontend/templates")

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Suas IoT Intelligent Alarm API", lifespan=lifespan)

app.mount("/media", StaticFiles(directory="../frontend/media"), name="media")
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")
app.mount("/templates", StaticFiles(directory="../frontend/templates"), name="templates")

app.include_router(pages_router)
app.include_router(users_router)
app.include_router(readings_router)
app.include_router(alarm_router)


@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again"
    )
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
    return templates.TemplateResponse(
        request,
        "pages/error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": exception.detail,
        },
        status_code=exception.status_code,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exception: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=jsonable_encoder({"detail": exception.errors()}),
    )
