# Exception Routes

from select import select
from unittest import result
from unittest import result
from fastapi.exceptions import RequestValidationError
from typing_extensions import Annotated
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from requests import Session
from starlette.exceptions import HTTPException as StarletteHTTPException
from api import models
from api.database import get_db
from api.schemas import PressureMatReadingResponse, UserResponse

router = APIRouter(prefix="/api/exceptions", tags=["Exceptions"])
templates = Jinja2Templates(directory="../frontend/templates")

@router.exception_handler(StarletteHTTPException)
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
        "error.html",
        {
        "status_code": exception.status_code,
         "title": exception.status_code,
         "message":exception.detail,
         },
        status_code = exception.status_code,
    )
    
@router.exception_handler(RequestValidationError)
def validation_exception_handler(request:Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
            return JSONResponse(
                status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
                content = {"detail": exception.errors()}
            )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
        "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message":"Invalid request. Please check your input and try again",
            },
        status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
    )

