from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies.database import get_db
from sqlalchemy import desc
from mission.engine import choose_mission
import models

router = APIRouter(prefix='/missions', tags=['Missions'])

@router.get("/today")
def get_today_mission(db: Session=Depends(get_db)):
    today = datetime.now().date()

    today_assignment = (
        db.query(models.UserMission).filter(models.UserMission.assigned_at >= datetime.combine(today, datetime.min.time())).order_by(models.UserMission.assigned_at.desc()).first()
    )


    if today_assignment:
        if today_assignment.status == "skipped":
            return {
                "mission": None,
                "status": "skipped"
            }

        mission = (
            db.query(models.Mission)
            .filter(
                models.Mission.id == today_assignment.mission_id
            )
            .first()
        )

        return {
            "mission": mission,
            "status": today_assignment.status
        }

    current_check_in=(
            db.query(models.CheckIn).order_by(desc(models.CheckIn.created_at)).first()
        )

    if not current_check_in:
        return {
            "mission": None,
            "message": "Complete a check-in first."
        }

    week_ago = datetime.now() - timedelta(days=7)

    recent_check_ins = (
        db.query(models.CheckIn).filter(models.CheckIn.created_at >= week_ago).order_by(desc(models.CheckIn.created_at)).all()
    )

    recent_user_missions = (
        db.query(models.UserMission).order_by(desc(models.UserMission.id)).limit(5).all()
    )

    recent_mission_ids=[
        user_mission.mission_id
        for user_mission in recent_user_missions
    ]

    recent_missions = (
        db.query(models.Mission).filter(models.Mission.id.in_(recent_mission_ids)).all()
        if recent_mission_ids
        else []
    )

    

    missions=db.query(models.Mission).all()

    mission=choose_mission(
        current_check_in,
        recent_missions,
        missions
    )

    if not mission:
        return {
            "mission": None,
            "message": "No suitable mission found."
        }


    user_mission = models.UserMission(
        mission_id = mission.id,
        status = "assigned"
    )

    db.add(user_mission)
    db.commit()
    db.refresh(user_mission)


    return {
        "mission": mission
    }

@router.post('/{mission_id}/start')
def start_mission(mission_id: int, db: Session=Depends(get_db)):
    user_mission = (
        db.query(models.UserMission).filter(models.UserMission.mission_id == mission_id).order_by(models.UserMission.assigned_at.desc()).first()
    )

    if not user_mission:
        return {
            "message": "Mission assignment not found."
        }

    user_mission.status = 'started'
    user_mission.started_at = datetime.now()

    db.commit()
    db.refresh(user_mission)

    return user_mission

@router.post("/{mission_id}/complete")
def complete_mission(mission_id: int, db: Session=Depends(get_db)):
    user_mission= (
        db.query(models.UserMission).filter(models.UserMission.mission_id == mission_id, models.UserMission.status == 'started').order_by(models.UserMission.assigned_at.desc()).first()
    )

    if not user_mission:
        return {
            "message": "Started mission not found."
        }

    user_mission.status = "completed"
    user_mission.completed_at = datetime.now()

    db.commit()
    db.refresh(user_mission)

    return user_mission

@router.post("/{mission_id}/skip")
def skip_mission(mission_id: int, db: Session = Depends(get_db)):
    user_mission = (
        db.query(models.UserMission).filter(models.UserMission.mission_id == mission_id, models.UserMission.status == 'started').order_by(models.UserMission.assigned_at.desc()).first()
    )

    if not user_mission:
        return {
            "message": "Started mission not found."
        }

    user_mission.status = "skipped"

    db.commit()
    db.refresh(user_mission)

    return user_mission


