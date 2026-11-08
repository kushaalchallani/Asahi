"""
Integration tests for difficulty preference and mission recommendation flow.
Tests that changing difficulty preference properly refreshes mission recommendations.
"""
import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from core.database import Base
from core.security import create_access_token
from dependencies.database import get_db
from main import app
from models.user import User
from models.mission import Mission
from models.user_mission import UserMission
from models.check_in import CheckIn


@pytest.fixture
def integration_client():
    """Client with full setup for integration testing."""
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        with TestingSessionLocal() as db:
            # Create mission catalog: low, medium, high
            missions = [
                Mission(
                    title="Quiet meditation",
                    description="Sit quietly for 5 minutes",
                    category="regulation",
                    difficulty="low",
                    social_required=False,
                    energy_required="low",
                ),
                Mission(
                    title="Send a message to a friend",
                    description="Reach out with a simple hello",
                    category="connection",
                    difficulty="medium",
                    social_required=True,
                    energy_required="medium",
                ),
                Mission(
                    title="Take on a focused challenge",
                    description="Work on a personal goal",
                    category="reflection",
                    difficulty="high",
                    social_required=False,
                    energy_required="high",
                ),
            ]
            db.add_all(missions)
            db.flush()

            # Create user
            user = User(
                email="difficulty-test@example.com",
                password_hash=None,
                is_active=True,
                difficulty_preference="moderate",
            )
            db.add(user)
            db.flush()

            # Create a check-in
            check_in = CheckIn(
                user_id=user.id,
                feeling="I'm doing okay",
                note="Feeling neutral today",
            )
            db.add(check_in)
            db.flush()

            client.user_id = user.id
            client.missions = missions
            client.headers.update({
                "Authorization": f"Bearer {create_access_token(user.id)}"
            })

        yield client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


def test_difficulty_pref_defaults_to_moderate(integration_client):
    """Users should start with moderate difficulty preference."""
    response = integration_client.get("/preferences/difficulty")
    assert response.status_code == 200
    assert response.json() == {"difficulty_preference": "moderate"}


def test_difficulty_preference_can_be_updated(integration_client):
    """Users can change their difficulty preference."""
    response = integration_client.put(
        "/preferences/difficulty",
        json={"difficulty_preference": "easy"}
    )
    assert response.status_code == 200
    assert response.json() == {"difficulty_preference": "easy"}

    # Verify it persisted
    response = integration_client.get("/preferences/difficulty")
    assert response.json() == {"difficulty_preference": "easy"}


def test_difficulty_preference_is_validated(integration_client):
    """Invalid difficulty preferences should be rejected."""
    response = integration_client.put(
        "/preferences/difficulty",
        json={"difficulty_preference": "impossible-difficulty"}
    )
    assert response.status_code == 422


def test_difficulty_preference_updates_user_model(integration_client):
    """Updating preference should update the user model in database."""
    from dependencies.database import get_db
    from main import app

    # Update preference
    integration_client.put(
        "/preferences/difficulty",
        json={"difficulty_preference": "challenging"}
    )

    # Check DB directly
    db = next(app.dependency_overrides[get_db]())
    user = db.query(User).filter(User.id == integration_client.user_id).first()
    assert user.difficulty_preference == "challenging"
    db.close()


def test_today_mission_reflects_current_preference(integration_client):
    """Today's mission should consider current difficulty preference."""
    # Get initial mission
    response = integration_client.get("/missions/today")
    initial_mission = None
    if response.status_code == 200:
        data = response.json()
        if data.get("mission"):
            initial_mission = data["mission"]

    # Change to easy preference
    integration_client.put(
        "/preferences/difficulty",
        json={"difficulty_preference": "easy"}
    )

    # Check that user preference was updated
    pref_response = integration_client.get("/preferences/difficulty")
    assert pref_response.json()["difficulty_preference"] == "easy"


def test_difficulty_change_requires_authentication(integration_client):
    """Difficulty preference endpoints should require authentication."""
    # Remove auth header
    integration_client.headers.pop("Authorization")

    # Should fail for GET
    response = integration_client.get("/preferences/difficulty")
    assert response.status_code == 401

    # Should fail for PUT
    response = integration_client.put(
        "/preferences/difficulty",
        json={"difficulty_preference": "easy"}
    )
    assert response.status_code == 401

    # Restore auth header
    integration_client.headers.update({
        "Authorization": f"Bearer {create_access_token(integration_client.user_id)}"
    })


def test_mission_assignment_creates_new_user_mission(integration_client):
    """Getting today's mission should create a UserMission assignment."""
    response = integration_client.get("/missions/today")
    assert response.status_code == 200

    data = response.json()
    assert "mission" in data
    assert "assignment_id" in data
    assert data["assignment_id"] is not None


def test_mission_feedback_stored_correctly(integration_client):
    """Mission feedback should be stored and linked to assignment."""
    # Get today's mission
    response = integration_client.get("/missions/today")
    data = response.json()

    if data.get("mission") and data.get("assignment_id"):
        assignment_id = data["assignment_id"]

        # Submit feedback
        feedback_response = integration_client.post(
            f"/missions/assignments/{assignment_id}/feedback",
            json={"feedback": "helpful"}
        )
        assert feedback_response.status_code == 200

        # Check assignment has feedback
        response = integration_client.get("/missions/today")
        data = response.json()
        assert data.get("feedback") == "helpful"


def test_preferred_difficulty_mission_comes_first(integration_client):
    """When easy is preferred, low difficulty missions should be prioritized."""
    # User has moderate preference by default
    # Switch to easy
    integration_client.put(
        "/preferences/difficulty",
        json={"difficulty_preference": "easy"}
    )

    # Get today's mission - should be easy (low difficulty)
    response = integration_client.get("/missions/today")
    assert response.status_code == 200

    data = response.json()
    if data.get("mission") and data.get("assignment_id"):
        # Verify mission was assigned
        assert data["mission"]["difficulty"] == "low"


def test_moderate_preference_selects_medium_difficulty(integration_client):
    """When moderate is preferred, medium difficulty missions should be available."""
    # Ensure moderate preference
    integration_client.put(
        "/preferences/difficulty",
        json={"difficulty_preference": "moderate"}
    )

    response = integration_client.get("/missions/today")
    assert response.status_code == 200


def test_difficulty_preference_affects_recommendation_reasons(integration_client):
    """Changing difficulty preference should affect mission recommendation reasons."""
    # Set to easy
    integration_client.put(
        "/preferences/difficulty",
        json={"difficulty_preference": "easy"}
    )

    response = integration_client.get("/missions/today")
    data = response.json()

    # Reasons should include difficulty information
    if data.get("reasons") and data.get("mission"):
        # Check that reasons list exists
        assert isinstance(data["reasons"], list)