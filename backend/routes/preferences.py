from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from dependencies.auth import get_current_user
from dependencies.database import get_db
from models.user import User
from schemas.auth import UserPublic
from schemas.preferences import (
    DifficultyPreferenceUpdate,
    DifficultyPreferenceResponse,
    UserPreferences,
    UserPreferencesUpdate,
    UserPreferencesResponse,
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

@router.get("/settings", response_model=UserPreferencesResponse)
def get_user_preferences(
    current_user: User = Depends(get_current_user),
):
    return {
        "theme": current_user.theme,
        "reminders_enabled": current_user.reminders_enabled,
        "reminder_time": current_user.reminder_time,
        "email_digest": current_user.email_digest,
        "text_size": current_user.text_size,
        "reduced_motion": current_user.reduced_motion,
        "high_contrast": current_user.high_contrast,
    }


@router.put("/settings", response_model=UserPreferencesResponse)
def update_user_preferences(
    preferences: UserPreferencesUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if preferences.theme is not None:
        current_user.theme = preferences.theme
    if preferences.reminders_enabled is not None:
        current_user.reminders_enabled = preferences.reminders_enabled
    if preferences.reminder_time is not None:
        current_user.reminder_time = preferences.reminder_time
    if preferences.email_digest is not None:
        current_user.email_digest = preferences.email_digest
    if preferences.text_size is not None:
        current_user.text_size = preferences.text_size
    if preferences.reduced_motion is not None:
        current_user.reduced_motion = preferences.reduced_motion
    if preferences.high_contrast is not None:
        current_user.high_contrast = preferences.high_contrast

    db.commit()
    db.refresh(current_user)

    return {
        "theme": current_user.theme,
        "reminders_enabled": current_user.reminders_enabled,
        "reminder_time": current_user.reminder_time,
        "email_digest": current_user.email_digest,
        "text_size": current_user.text_size,
        "reduced_motion": current_user.reduced_motion,
        "high_contrast": current_user.high_contrast,
    }


class EmailUpdateRequest(BaseModel):
    email: str


@router.patch("/email", response_model=UserPublic)
def update_email(
    data: EmailUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    from fastapi import HTTPException, status
    from core.security import hash_password

    email = data.email

    #if new email is different from current
    if email.lower() == current_user.email.lower():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New email must be different from current email."
        )

    #if email is already in use
    existing_user = db.query(User).filter(User.email == email.lower()).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists."
        )

    current_user.email = email.lower()
    db.commit()
    db.refresh(current_user)

    return current_user


class PasswordUpdateRequest(BaseModel):
    current_password: str
    new_password: str


@router.patch("/password", response_model=UserPublic)
def update_password(
    data: PasswordUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from fastapi import HTTPException, status
    from core.security import verify_password, hash_password

    #current password
    if not current_user.password_hash or not verify_password(data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect."
        )

    #new password
    if len(data.new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be at least 8 characters."
        )

    current_user.password_hash = hash_password(data.new_password)
    db.commit()
    db.refresh(current_user)

    return current_user