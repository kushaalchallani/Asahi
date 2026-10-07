from database import SessionLocal
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
]

def seed_missions():
    db=SessionLocal()

    try:
        existing_count = db.query(Mission).count()

        if existing_count > 0:
            print("Mission already exist. Nothing to seed.")
            return

        db.add_all(missions)
        db.commit()

        print(f"Seeded {len(missions)} mission(s).")
    finally:
        db.close()

if __name__ == "__main__":
    seed_missions()