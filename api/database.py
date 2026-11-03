from __future__ import annotations
from datatime import UTC, datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class User(Base):
    __tablename__ = "user"

    user_id = Mapped[int] = mapped_column(primary_key=True, index = True)
    username = Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email = Mapped[str] = mapped_column(String(300), unique=True, nullable=False)
    image_file = Mapped[str | None] = mapped_column(String(200), nullable=True, default="default.jpg")

    readings = Mapped[list[Reading]] = relationship(back_populates="author", cascade="all, delete-orphan")
    