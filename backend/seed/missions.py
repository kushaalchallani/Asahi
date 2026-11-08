from core.database import SessionLocal
from models import Mission

missions = [
    Mission(
        title="Take a quiet pause",
        description="Find a comfortable place and give yourself a few quiet minutes without needing to accomplish anything.",
        category="regulation",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Step outside for a moment",
        description="Spend a few minutes outside and simply notice what's around you.",
        category="environment",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Write down what's on your mind",
        description="Take a few minutes to write whatever has been sitting in your thoughts. It doesn't need to be organized.",
        category="reflection",
        difficulty="low",
        social_required=False,
        energy_required="low",
    ),
    Mission(
        title="Do one small thing you've been putting off",
        description="Choose one small task you've been avoiding and spend a few minutes making progress on it.",
        category="self-care",
        difficulty="medium",
        social_required=False,
        energy_required="medium",
    ),
    Mission(
        title="Send a simple message",
        description="Reach out to someone you trust with a simple message. It doesn't have to become a long conversation.",
        category="connection",
        difficulty="medium",
        social_required=True,
        energy_required="medium",
    ),
    Mission(
        title="Spend a little time with someone",
        description="If you feel up to it, spend some time around someone you feel comfortable with.",
        category="connection",
        difficulty="medium",
        social_required=True,
        energy_required="medium",
    ),
    Mission(
        title="Plan and work towards a personal goal",
        description="Choose something meaningful you would like to accomplish. Break it into smaller steps and spend some focused time working on the first one.",
        category="reflection",
        difficulty="high",
        social_required=False,
        energy_required="high",
    ),
    Mission(
        title="Take on a focused learning challenge",
        description="Choose something you have been curious about learning. Set aside some focused time to explore it and put what you learn into practice.",
        category="reflection",
        difficulty="high",
        social_required=False,
        energy_required="medium",
    ),
]

def seed_missions():
    db = SessionLocal()
    added_count = 0

    try:
        for mission in missions:
            existing = (
                db.query(Mission)
                .filter(Mission.title == mission.title)
                .first()
            )

            if not existing:
                db.add(mission)
                added_count += 1

        db.commit()

        print(f"Added {added_count} new mission(s).")

    finally:
        db.close()
if __name__ == "__main__":
    seed_missions()