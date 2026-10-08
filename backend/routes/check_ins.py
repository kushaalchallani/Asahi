from collections import Counter
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies.database import get_db
import models

router = APIRouter(prefix='/check-ins', tags=["Check-ins"])

@router.get("")
def get_check_in(db: Session=Depends(get_db)):
    return db.query(models.CheckIn).order_by(
        models.CheckIn.created_at.desc()
    ).all()

@router.get("/insights")
def get_check_in(db:Session=Depends(get_db)):
    week_ago=datetime.now() - timedelta(days=7)

    recent_check_ins=(
        db.query(models.CheckIn).filter(models.CheckIn.created_at>=week_ago).order_by(models.CheckIn.created_at.desc()).all()
    )

    feelings=[check_in.feeling for check_in in recent_check_ins]

    most_common_feeling=None

    if feelings:
        most_common_feeling=Counter(feelings).most_common(1)[0][0]

    return {
        "check_in_count": len(recent_check_ins),
        "most_common_feeling": most_common_feeling
    }

@router.post("")
def create_check_in(feeling: str, note: str | None=None, db: Session=Depends(get_db)):
    check_in = models.CheckIn(feeling=feeling, note=note)

    db.add(check_in)
    db.commit()
    db.refresh(check_in)

    return check_in

