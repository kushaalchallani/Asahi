from typing import Literal
from pydantic import BaseModel, Field


DifficultyLevel = Literal["easy", "moderate", "challenging"]
ThemeLevel = Literal["light", "dark", "system"]
TextSizeLevel = Literal["normal", "large", "xlarge"]


class DifficultyPreferenceUpdate(BaseModel):
    difficulty_preference: DifficultyLevel


class DifficultyPreferenceResponse(BaseModel):
    difficulty_preference: DifficultyLevel


class UserPreferences(BaseModel):
    theme: ThemeLevel = "system"
    reminders_enabled: bool = True
    reminder_time: str = Field(default="20:00", pattern=r"^\d{2}:\d{2}$")
    email_digest: bool = True
    text_size: TextSizeLevel = "normal"
    reduced_motion: bool = False
    high_contrast: bool = False


class UserPreferencesUpdate(BaseModel):
    theme: ThemeLevel | None = None
    reminders_enabled: bool | None = None
    reminder_time: str | None = Field(default="20:00", pattern=r"^\d{2}:\d{2}$")
    email_digest: bool | None = None
    text_size: TextSizeLevel | None = None
    reduced_motion: bool | None = None
    high_contrast: bool | None = None


class UserPreferencesResponse(BaseModel):
    theme: ThemeLevel
    reminders_enabled: bool
    reminder_time: str
    email_digest: bool
    text_size: TextSizeLevel
    reduced_motion: bool
    high_contrast: bool