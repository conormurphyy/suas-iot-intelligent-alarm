
from pathlib import Path
import os

import paho.mqtt.client as mqtt

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

from starlette.exceptions import HTTPException as StarletteHTTPException

import api.models

from api.database import Base, engine
from api.routes.alarm import router as alarm_router
from api.routes.pages import router as pages_router
from api.routes.readings import router as readings_router
from api.routes.users import router as users_router

from api.services.alarm_scheduler import scheduler, load_alarms


# Frontend directories
FRONTEND_DIR = Path("/frontend")

# MQTT configuration
MQTT_BROKER = "mosquitto"
MQTT_PORT = 1883


# MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.username_pw_set(
    os.getenv("MQTT_USERNAME"),
    os.getenv("MQTT_PASSWORD")
)


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to EC2 MQTT Broker with result code {reason_code}")


client.on_connect = on_connect


# Templates
templates = Jinja2Templates(
    directory=str(FRONTEND_DIR / "templates")
)


# Application lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

    app.state.mqtt_client = client

    load_alarms(client)
    scheduler.start()

    print("Scheduler started")

    yield

    scheduler.shutdown(wait=False)

    client.loop_stop()
    client.disconnect()

    print("MQTT client stopped")


# Database
Base.metadata.create_all(bind=engine)


# FastAPI application
app = FastAPI(
    title="Suas IoT Intelligent Alarm API",
    lifespan=lifespan
)


# Static files
app.mount(
    "/media",
    StaticFiles(directory=str(FRONTEND_DIR / "media")),
    name="media"
)

app.mount(
    "/static",
    StaticFiles(directory=str(FRONTEND_DIR / "static")),
    name="static"
)

app.mount(
    "/templates",
    StaticFiles(directory=str(FRONTEND_DIR / "templates")),
    name="templates"
)


# Routers
app.include_router(pages_router)
app.include_router(users_router)
app.include_router(readings_router)
app.include_router(alarm_router)


# Exception handler
@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(
    request: Request,
    exception: StarletteHTTPException
):

    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again"
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message}
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
