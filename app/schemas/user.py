from pydantic import BaseModel,EmailStr,Field,ConfigDict
from uuid import UUID

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    full_name: str = Field(min_length=1, max_length=100)


class UserRegister(UserBase):
    password: str = Field(min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: UUID
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str
    
class UserUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str | None = Field(
        default=None,
        min_length=3,
        max_length=50,
    )

    full_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )