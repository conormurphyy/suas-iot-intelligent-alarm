# Users Routes

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/api/users", tags=["Users"])


# Create User
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    new_user = models.User(
        username=user.username,
        email=user.email,
        password=user.password,
        image_file=user.image_file,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Get User by ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")


# Get All Users
@router.get("/", response_model=list[UserResponse])
def get_all_users(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User))
    users = result.scalars().all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
    return users


# Update User Full
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == user_id))
    existing_user = result.scalars().first()
    if existing_user:
        existing_user.username = user.username
        existing_user.email = user.email
        existing_user.password = user.password
        existing_user.image_file = user.image_file
        db.commit()
        db.refresh(existing_user)
        return existing_user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")


# Update User Partial
@router.patch("/{user_id}", response_model=UserResponse)
def update_user_partial(user_id: int, user: UserUpdate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == user_id))
    existing_user = result.scalars().first()
    if existing_user:
        if user.username is not None:
            existing_user.username = user.username
        if user.email is not None:
            existing_user.email = user.email
        if user.password is not None:
            existing_user.password = user.password
        if user.image_file is not None:
            existing_user.image_file = user.image_file
        db.commit()
        db.refresh(existing_user)
        return existing_user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")


# Delete User
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == user_id))
    existing_user = result.scalars().first()
    if existing_user:
        db.delete(existing_user)
        db.commit()
        return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")