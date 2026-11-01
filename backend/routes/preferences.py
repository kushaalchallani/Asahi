from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.auth import get_current_user
from dependencies.database import get_db
from models.user import User
from schemas.preferences import (
    DifficultyPreferenceUpdate,
    DifficultyPreferenceResponse,
)

router = APIRouter(prefix="/preferences", tags=["Preferences"])


@router.get("/difficulty", response_model=DifficultyPreferenceResponse)
def get_difficulty_preference(
    current_user: User = Depends(get_current_user),
):
    return {
        "difficulty_preference": current_user.difficulty_preference
    }


@router.put("/difficulty", response_model=DifficultyPreferenceResponse)
def update_difficulty_preference(
    preference: DifficultyPreferenceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user.difficulty_preference = preference.difficulty_preference

    db.commit()
    db.refresh(current_user)

    return {
        "difficulty_preference": current_user.difficulty_preference
    }