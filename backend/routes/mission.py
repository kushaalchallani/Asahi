from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies.database import get_db
from sqlalchemy import desc
from mission.engine import choose_mission, build_feedback_history, explain_mission_score, format_mission_reasons, detect_mood, detect_repeated_low_mood, score_difficulty_preference
from schemas.mission_feedback import MissionFeedbackRequest
from dependencies.auth import get_current_user
from models.user import User
import models

router = APIRouter(prefix='/missions', tags=['Missions'])

def get_mission_reasons(mission, current_check_in, recent_check_ins, recent_feedback, difficulty_preference="moderate"):
    mood = detect_mood(current_check_in)
    repeated_low_mood = detect_repeated_low_mood(recent_check_ins)

    reason_codes = explain_mission_score(
        mission,
        is_low_mood=mood["is_low_mood"],
        is_stressed=mood["is_stressed"],
        is_lonely=mood["is_lonely"],
        repeated_low_mood=repeated_low_mood,
        feedback_by_mission=recent_feedback,
        difficulty_preference=difficulty_preference,
    )

    return format_mission_reasons(reason_codes)

@router.get("/today")
def get_today_mission(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    today = datetime.now().date()
    user_id = current_user.id
    today_assignment = (
        db.query(models.UserMission)
        .filter(
            models.UserMission.user_id == user_id,
            models.UserMission.assigned_at
            >= datetime.combine(today, datetime.min.time()),
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
            .filter(models.CheckIn.user_id == user_id)
            .order_by(desc(models.CheckIn.created_at))
            .first()
        )

        reasons = []

        if current_check_in and mission:
            week_ago = datetime.now() - timedelta(days=7)

            recent_check_ins = (
                db.query(models.CheckIn)
                .filter(
                    models.CheckIn.user_id == user_id,
                    models.CheckIn.created_at >= week_ago,
                )
                .order_by(desc(models.CheckIn.created_at))
                .all()
            )

            feedback_rows = (
                db.query(models.UserMission)
                .filter(
                    models.UserMission.user_id == user_id,
                    models.UserMission.feedback.isnot(None),
                )
                .order_by(
                    desc(models.UserMission.feedback_at).nullslast(),
                    desc(models.UserMission.assigned_at),
                )
                .limit(50)
                .all()
            )

            recent_feedback = build_feedback_history(feedback_rows)
            
            if (
                today_assignment.status == "assigned"
                and mission
                and current_check_in
                and score_difficulty_preference(
                    mission,
                    current_user.difficulty_preference,
                ) == 0
            ):
                recent_user_missions = (
                    db.query(models.UserMission)
                    .filter(models.UserMission.user_id == user_id)
                    .order_by(desc(models.UserMission.id))
                    .limit(5)
                    .all()
                )

                recent_mission_ids = [
                    item.mission_id for item in recent_user_missions
                ]

                recent_missions = (
                    db.query(models.Mission)
                    .filter(models.Mission.id.in_(recent_mission_ids))
                    .all()
                    if recent_mission_ids else []
                )

                all_missions = db.query(models.Mission).all()

                new_mission = choose_mission(
                    current_check_in,
                    recent_missions,
                    all_missions,
                    recent_feedback=recent_feedback,
                    recent_check_ins=recent_check_ins,
                    difficulty_preference=current_user.difficulty_preference,
                )

                if (
                    new_mission
                    and new_mission.id != mission.id
                    and score_difficulty_preference(
                        new_mission,
                        current_user.difficulty_preference,
                    ) > 0
                ):
                    today_assignment.status = "superseded"

                    new_assignment = models.UserMission(
                        user_id=user_id,
                        mission_id=new_mission.id,
                        status="assigned",
                    )

                    db.add(new_assignment)
                    db.commit()
                    db.refresh(new_assignment)

                    reasons = get_mission_reasons(
                        new_mission,
                        current_check_in,
                        recent_check_ins,
                        recent_feedback,
                        current_user.difficulty_preference,
                    )

                    return {
                        "mission": new_mission,
                        "status": new_assignment.status,
                        "assignment_id": new_assignment.id,
                        "feedback": None,
                        "reasons": reasons,
                    }

            reasons = get_mission_reasons(
                mission,
                current_check_in,
                recent_check_ins,
                recent_feedback,
                current_user.difficulty_preference,
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
        .filter(models.CheckIn.user_id == user_id)
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
        .filter(
            models.CheckIn.user_id == user_id,
            models.CheckIn.created_at >= week_ago,
        )
        .order_by(desc(models.CheckIn.created_at))
        .all()
    )

    recent_user_missions = (
        db.query(models.UserMission)
        .filter(models.UserMission.user_id == user_id)
        .order_by(desc(models.UserMission.id))
        .limit(5)
        .all()
    )

    feedback_rows = (
        db.query(models.UserMission)
        .filter(
            models.UserMission.user_id == user_id,
            models.UserMission.feedback.isnot(None),
        )
        .order_by(
            desc(models.UserMission.feedback_at).nullslast(),
            desc(models.UserMission.assigned_at),
        )
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
        recent_check_ins=recent_check_ins,
        difficulty_preference=current_user.difficulty_preference,
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
        difficulty_preference=current_user.difficulty_preference
    )

    reasons = format_mission_reasons(reason_codes)

    user_mission = models.UserMission(
        user_id=user_id,
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
        "reasons": reasons,
    }

@router.post('/assignments/{assignment_id}/start')
def start_mission(assignment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_mission = (
        db.query(models.UserMission)
        .filter(
            models.UserMission.id == assignment_id,
            models.UserMission.user_id == current_user.id,
            models.UserMission.status == "assigned",
        )
        .first()
    )

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
def complete_mission(assignment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_mission = (
        db.query(models.UserMission)
        .filter(
            models.UserMission.id == assignment_id,
            models.UserMission.user_id == current_user.id,
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
def skip_mission(assignment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_mission = (
        db.query(models.UserMission)
        .filter(
            models.UserMission.id == assignment_id,
            models.UserMission.user_id == current_user.id,
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
def submit_mission_feedback(assignment_id: int, payload: MissionFeedbackRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_mission = (
        db.query(models.UserMission)
        .filter(
            models.UserMission.id == assignment_id,
            models.UserMission.user_id == current_user.id,
        )
        .first()
    )

    if not user_mission:
        raise HTTPException(
            status_code=404,
            detail="Mission assignment not found."
        )

    if user_mission.status not in ("completed", "skipped"):
        raise HTTPException(
            status_code=409,
            detail="Feedback can only be submitted after completing or skipping a mission."
        )

    if user_mission.feedback is not None:
        raise HTTPException(
            status_code=409,
            detail="Feedback has already been submitted for this mission.",
        )

    user_mission.feedback = payload.feedback
    user_mission.feedback_at = datetime.now()

    db.commit()
    db.refresh(user_mission)

    return {
        "assignment_id": user_mission.id,
        "feedback": user_mission.feedback,
    }