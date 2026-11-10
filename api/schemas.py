import datetime

from pydantic import BaseModel, ConfigDict, Field, EmailStr

# User schema
class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr = Field(max_length=300)

class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=100)
    image_file: str | None = None

class UserResponse(UserBase):
    model_config =ConfigDict(from_attributes=True)

    id: int
    date_timestamp: datetime.datetime
    image_file: str | None = None
    image_path: str

class UserUpdate(UserBase):
    username: str | None = Field(default = None, min_length=3, max_length=20)
    email: EmailStr | None = Field(default = None,  max_length=300)
    password: str | None = Field(default = None, min_length=6, max_length=100)
    image_file: str | None = None

# Alarm Schema

# Pressure Mat Reading schema
class PressureMatReadingBase(BaseModel):
    pressure_detected: bool
    event_type: str = Field(max_length=50)

class PressureMatReadingCreate(PressureMatReadingBase):
    pass

class PressureMatReadingUpdate(PressureMatReadingBase):
    pressure_detected: bool | None = None
    event_type: str | None = Field(default=None, max_length=50)

class PressureMatReadingResponse(PressureMatReadingBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    date_timestamp: datetime.datetime
    author: UserResponse