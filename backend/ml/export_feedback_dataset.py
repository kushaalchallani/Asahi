from sqlalchemy.orm import Session
import models


def export_feedback_dataset(db: Session) -> list[dict]:
    records = []

    assignments = (
        db.query(models.UserMission)
        .order_by(models.UserMission.assigned_at.asc())
        .all()
    )

    for assignment in assignments:
        if assignment.feedback not in {"helpful", "not_for_me"}:
            continue

        mission = (
            db.query(models.Mission)
            .filter(models.Mission.id == assignment.mission_id)
            .first()
        )

        if mission is None:
            continue

        latest_check_in = (
            db.query(models.CheckIn)
            .filter(
                models.CheckIn.created_at <= assignment.assigned_at
            )
            .order_by(models.CheckIn.created_at.desc())
            .first()
        )

        if latest_check_in is None:
            continue

        feeling = (latest_check_in.feeling or "").lower()
        note = (latest_check_in.note or "").lower()
        text = f"{feeling} {note}"

        if any(word in text for word in [
            "low",
            "tired",
            "sad",
            "broken",
            "exhausted",
            "drained",
        ]):
            energy_preference = "low"
        elif any(word in text for word in [
            "energetic",
            "active",
            "motivated",
        ]):
            energy_preference = "high"
        else:
            energy_preference = "medium"

        records.append({
            "category": mission.category,
            "difficulty": mission.difficulty,
            "energy_required": mission.energy_required,
            "social_required": mission.social_required,
            "energy_preference": energy_preference,
            "recently_seen": False,
            "preference_match": int(
                assignment.feedback == "helpful"
            ),
        })

    return records