# Exception Routes

from typing import Annotated

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException as StarletteHTTPException

import models
from database import get_db
from schemas import PressureMatReadingResponse, UserResponse

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

