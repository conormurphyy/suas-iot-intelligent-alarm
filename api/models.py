from __future__ import annotations

from datetime import UTC, datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    date_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                     default=lambda: datetime.now(UTC))
    image_file: Mapped[str | None] = mapped_column(String(200), nullable=True, default=None,)
    password: Mapped[str] = mapped_column(String(200), nullable=False)

    alarm:Mapped[list[Alarm]] = relationship(back_populates="author", cascade="all, delete-orphan")
    
    reading:Mapped[list[Reading]] = relationship(back_populates="author", cascade="all, delete-orphan")


class Alarm(Base):
    __tablename__ = "alarm"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    alarm_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    enabled: Mapped[bool] = mapped_column(nullable=False, default=True)
    sound_file: Mapped[str] = mapped_column(String(200), nullable=False, default="default_alarm.mp3")
    date_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                     default=lambda: datetime.now(UTC))
    author: Mapped[User] = relationship(back_populates="alarm")
    
class Reading(Base):
    __tablename__ = "reading"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    pressure_detected: Mapped[bool] = mapped_column(nullable=False, default=False)
    date_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                     default=lambda: datetime.now(UTC))
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    author: Mapped[User] = relationship(back_populates="reading")
