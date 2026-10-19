from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies.database import get_db
from sqlalchemy import desc
from mission.engine import choose_mission, build_feedback_history, explain_mission_score, format_mission_reasons, detect_mood, detect_repeated_low_mood
from schemas.mission_feedback import MissionFeedbackRequest
import models

router = APIRouter(prefix='/missions', tags=['Missions'])

def get_mission_reasons(mission, current_check_in, recent_check_ins, recent_feedback):
    mood = detect_mood(current_check_in)
    repeated_low_mood = detect_repeated_low_mood(recent_check_ins)

    reason_codes = explain_mission_score(
        mission,
        is_low_mood=mood["is_low_mood"],
        is_stressed=mood["is_stressed"],
        is_lonely=mood["is_lonely"],
        repeated_low_mood=repeated_low_mood,
        feedback_by_mission=recent_feedback,
    )

    return format_mission_reasons(reason_codes)

@router.get("/today")
def get_today_mission(db: Session = Depends(get_db)):
    today = datetime.now().date()

    today_assignment = (
        db.query(models.UserMission)
        .filter(
            models.UserMission.assigned_at
            >= datetime.combine(today, datetime.min.time())
        )
        .order_by(models.UserMission.assigned_at.desc())
        .first()
    )

    if today_assignment:
        mission = (
            db.query(models.Mission)
            .filter(models.Mission.id == today_assignment.mission_id)
            .first()
        )

        current_check_in = (
            db.query(models.CheckIn)
            .order_by(desc(models.CheckIn.created_at))
            .first()
        )

        reasons = []

        if current_check_in and mission:
            week_ago = datetime.now() - timedelta(days=7)

            recent_check_ins = (
                db.query(models.CheckIn)
                .filter(models.CheckIn.created_at >= week_ago)
                .order_by(desc(models.CheckIn.created_at))
                .all()
            )

            feedback_rows = (
                db.query(models.UserMission)
                .filter(models.UserMission.feedback.isnot(None))
                .order_by(desc(models.UserMission.assigned_at))
                .limit(50)
                .all()
            )

            recent_feedback = build_feedback_history(feedback_rows)

            reasons = get_mission_reasons(
                mission,
                current_check_in,
                recent_check_ins,
                recent_feedback,
            )

        return {
            "mission": mission,
            "status": today_assignment.status,
            "assignment_id": today_assignment.id,
            "feedback": today_assignment.feedback,
            "reasons": reasons,
        }

    current_check_in = (
        db.query(models.CheckIn)
        .order_by(desc(models.CheckIn.created_at))
        .first()
    )

    if not current_check_in:
        return {
            "mission": None,
            "status": "assigned",
            "message": "Complete a check-in first.",
        }

    week_ago = datetime.now() - timedelta(days=7)

    recent_check_ins = (
        db.query(models.CheckIn)
        .filter(models.CheckIn.created_at >= week_ago)
        .order_by(desc(models.CheckIn.created_at))
        .all()
    )

    recent_user_missions = (
        db.query(models.UserMission)
        .order_by(desc(models.UserMission.id))
        .limit(5)
        .all()
    )

    feedback_rows = (
        db.query(models.UserMission)
        .filter(models.UserMission.feedback.isnot(None))
        .order_by(desc(models.UserMission.assigned_at))
        .limit(50)
        .all()
    )

    recent_feedback = build_feedback_history(feedback_rows)

    recent_mission_ids = [
        user_mission.mission_id
        for user_mission in recent_user_missions
    ]

    recent_missions = (
        db.query(models.Mission)
        .filter(models.Mission.id.in_(recent_mission_ids))
        .all()
        if recent_mission_ids
        else []
    )

    missions = db.query(models.Mission).all()

    mission = choose_mission(
        current_check_in,
        recent_missions,
        missions,
        recent_feedback=recent_feedback,
        recent_check_ins=recent_check_ins
    )

    if not mission:
        return {
            "mission": None,
            "status": "assigned",
            "message": "No suitable mission found.",
        }

    mood = detect_mood(current_check_in)
    repeated_low_mood = detect_repeated_low_mood(recent_check_ins)

    reason_codes = explain_mission_score(
        mission,
        is_low_mood=mood["is_low_mood"],
        is_stressed=mood["is_stressed"],
        is_lonely=mood["is_lonely"],
        repeated_low_mood=repeated_low_mood,
        feedback_by_mission=recent_feedback,
    )

    reasons = format_mission_reasons(reason_codes)

    user_mission = models.UserMission(
        mission_id=mission.id,
        status="assigned",
    )

    db.add(user_mission)
    db.commit()
    db.refresh(user_mission)

    return {
        "mission": mission,
        "status": user_mission.status,
        "assignment_id": user_mission.id,
        "reasons":reasons
    }


@router.post('/assignments/{assignment_id}/start')
def start_mission(assignment_id: int, db: Session=Depends(get_db)):
    user_mission = (db.query(models.UserMission).filter(models.UserMission.id == assignment_id, models.UserMission.status == "assigned").first())

    if not user_mission:
        raise HTTPException(
        status_code=409,
        detail="Mission assignment not found or already started, completed, or skipped.",
    )

    user_mission.status = 'started'
    user_mission.started_at = datetime.now()

    db.commit()
    db.refresh(user_mission)

    return user_mission

@router.post("/assignments/{assignment_id}/complete")
def complete_mission(assignment_id: int, db: Session = Depends(get_db)):
    user_mission = (
        db.query(models.UserMission)
        .filter(
            models.UserMission.id == assignment_id,
            models.UserMission.status == "started",
        )
        .first()
    )

    if not user_mission:
        raise HTTPException(status_code=404, detail="Mission assignment not found or not started.",)

    user_mission.status = "completed"
    user_mission.completed_at = datetime.now()

    db.commit()
    db.refresh(user_mission)

    return user_mission

@router.post("/assignments/{assignment_id}/skip")
def skip_mission(assignment_id: int, db: Session = Depends(get_db)):
    user_mission = (
        db.query(models.UserMission)
        .filter(
            models.UserMission.id == assignment_id,
            models.UserMission.status == "started",
        )
        .first()
    )

    if not user_mission:
        raise HTTPException(
            status_code=404,
            detail="Mission assignment not found or not started.",
        )

    user_mission.status = "skipped"

    db.commit()
    db.refresh(user_mission)

    return user_mission


@router.post("/assignments/{assignment_id}/feedback")
def submit_mission_feedback(assignment_id: int, payload: MissionFeedbackRequest, db: Session = Depends(get_db)):
    user_mission = (db.query(models.UserMission).filter(models.UserMission.id == assignment_id).first())

    if not user_mission:
        raise HTTPException(
            status_code=404,
            detail="Mission assignment not found."
        )

    if user_mission.status not in ("completed", "skipped"):
        raise HTTPException(
        status_code=409,
        detail="Feedback can only be submitted after completing or skipping a mission.",
    )

    if user_mission.feedback is not None:
        raise HTTPException(
            status_code=409,
            detail="Feedback has already been submitted for this mission.",
        )

    user_mission.feedback = payload.feedback

    db.commit()
    db.refresh(user_mission)

    return {
        "assignment_id": user_mission.id,
        "feedback": user_mission.feedback
    }