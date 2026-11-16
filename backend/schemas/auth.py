from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Literal


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    name: str | None = Field(default=None, max_length=100)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    is_active: bool
    difficulty_preference: str
    name: str | None = None

    #user prefs
    theme: Literal["light", "dark", "system"] = "system"
    reminders_enabled: bool = True
    reminder_time: str = "20:00"
    email_digest: bool = True
    text_size: Literal["normal", "large", "xlarge"] = "normal"
    reduced_motion: bool = False
    high_contrast: bool = False


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic
