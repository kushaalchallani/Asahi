from collections import Counter
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies.database import get_db
from schemas.check_ins import CheckInCreate
from dependencies.auth import get_current_user
from models.user import User
import models

router = APIRouter(prefix='/check-ins', tags=["Check-ins"])

@router.get("")
def get_check_in(db: Session=Depends(get_db), current_user: User = Depends(get_current_user)):
    return (
        db.query(models.CheckIn)
        .filter(models.CheckIn.user_id == current_user.id)
        .order_by(models.CheckIn.created_at.desc())
        .all()
    )

@router.get("/insights")
def get_check_in(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    week_ago = datetime.now() - timedelta(days=7)

    recent_check_ins = (
        db.query(models.CheckIn)
        .filter(
            models.CheckIn.user_id == current_user.id,
            models.CheckIn.created_at >= week_ago,
        )
        .order_by(models.CheckIn.created_at.desc())
        .all()
    )

    feelings = [check_in.feeling for check_in in recent_check_ins]
    most_common_feeling = (
        Counter(feelings).most_common(1)[0][0] if feelings else None
    )

    return {
        "check_in_count": len(recent_check_ins),
        "most_common_feeling": most_common_feeling,
    }

@router.post("")
def create_check_in(check_in: CheckInCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_check_in = models.CheckIn(
        user_id=current_user.id,
        feeling=check_in.feeling,
        note=check_in.note,
    )

    db.add(new_check_in)
    db.commit()
    db.refresh(new_check_in)

    return new_check_in