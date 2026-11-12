
from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session
from api.database import Base, engine, get_db
import api.models
from api.routes.pages import router as pages_router
from api.routes.users import router as users_router
from api.routes.readings import router as readings_router
from api.routes.alarm import router as alarm_router
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from contextlib import asynccontextmanager
from api.services.alarm_scheduler import scheduler, load_alarms
import paho.mqtt.client as mqtt

MQTT_BROKER = "mosquitto"
MQTT_PORT = 1883

    
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to EC2 MQTT Broker with result code {reason_code}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
    
@asynccontextmanager
async def lifespan(app: FastAPI):

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

    load_alarms(client)
    scheduler.start()

    print("Scheduler started")

    yield

    client.loop_stop()
    client.disconnect()

    scheduler.shutdown(wait=False)

templates = Jinja2Templates(directory="../frontend/templates")

Base.metadata.create_all(bind=engine)

app = FastAPI(title ="Suas IoT Intelligent Alarm API", lifespan=lifespan)

app.mount("/media", StaticFiles(directory="../frontend/media"), name="media")
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")
app.mount("/templates", StaticFiles(directory="../frontend/templates"), name="templates")

app.include_router(pages_router)
app.include_router(users_router)
app.include_router(readings_router)
app.include_router(alarm_router)

@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request:Request, exception:StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again"
    )
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code = exception.status_code,
            content = {"detail": message}
        )
    return templates.TemplateResponse(
        request,
        "pages/error.html",
        {
        "status_code": exception.status_code,
         "title": exception.status_code,
         "message":exception.detail,
         },
        status_code = exception.status_code,
    )
    
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exception: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=jsonable_encoder({"detail": exception.errors()}),
    )
