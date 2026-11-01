from typing import Literal
from pydantic import BaseModel


DifficultyLevel = Literal["easy", "moderate", "challenging"]


class DifficultyPreferenceUpdate(BaseModel):
    difficulty_preference: DifficultyLevel


class DifficultyPreferenceResponse(BaseModel):
    difficulty_preference: DifficultyLevel