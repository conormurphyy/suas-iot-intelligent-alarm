import datetime

from pydantic import BaseModel, ConfigDict, Field, EmailStr

# User schema
class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr = Field(max_length=300)

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    model_config =ConfigDict(from_attributes=True)
    id: int
    image_file: str | None = None
    image_path: str

class UserUpdate(UserBase):
    username: str | None = Field(default = None, min_length=3, max_length=20)
    email: EmailStr | None = Field(default = None,  max_length=300)
    image_file: str | None = None

class PressureMatReadingBase(BaseModel):
    pressure_detected: bool
    event_type: str = Field(max_length=50)

class PressureMatReadingCreate(PressureMatReadingBase):
    pass

class PressureMatReadingResponse(PressureMatReadingBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    date_timestamp: datetime.datetime
    author: UserResponse