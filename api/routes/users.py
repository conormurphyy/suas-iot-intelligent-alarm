# Users Routes

from select import select
from typing_extensions import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from requests import Session

from api import models
from api.database import get_db
from api.schemas import UserResponse

router = APIRouter(prefix="/api/users", tags=["Users"])
templates = Jinja2Templates(directory="../frontend/templates")

#User Create
@router.post("/api/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserResponse, db: Annotated[Session, Depends(get_db)]):
    new_user = models.User(
        username=user.username,
        email=user.email,
        image_file=user.image_file,
        image_path=user.image_path
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#Get User by ID
@router.get("/api/user/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")

#Get All Users
@router.get("/api/users", response_model=list[UserResponse])
async def get_all_users(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User))
    users = result.scalars().all()
    if users.count() == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
    return users