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
    image_file: str | None
    image_path: str

class UserUpdate(UserBase):
    username: str | None = Field(min_length=3, max_length=20)
    email: EmailStr | None = Field(default = None,  max_length=300)
    image_file: str | None
