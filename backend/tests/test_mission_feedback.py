import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from core.database import Base
from core.security import create_access_token
from dependencies.database import get_db
from main import app
from models.mission import Mission
from models.user import User
from models.user_mission import UserMission

@pytest.fixture
def client():
    test_engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind= test_engine)
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db=TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        with TestingSessionLocal() as db:
            mission = Mission(
                title="Test mission",
                description="A mission for testing",
                category="reflection",
                difficulty="low",
                social_required=False,
                energy_required="low",
            )
            db.add(mission)
            db.flush()

            user = User(
                email="feedback-test@example.com",
                password_hash=None,
                is_active=True,
            )
            db.add(user)
            db.flush()
            assignment = UserMission(
                user_id=user.id,
                mission_id=mission.id,
                status="completed",
                feedback=None,
            )
            db.add(assignment)
            db.commit()
            db.refresh(assignment)

            test_client.assignment_id = assignment.id
            test_client.headers.update({
                "Authorization": f"Bearer {create_access_token(user.id)}"
            })

        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


def test_submit_valid_feedback(client):
    response = client.post(
        f"/missions/assignments/{client.assignment_id}/feedback",
        json={"feedback": "helpful"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "assignment_id": client.assignment_id,
        "feedback": "helpful",
    }


def test_submit_invalid_feedback(client):
    response = client.post(
        f"/missions/assignments/{client.assignment_id}/feedback",
        json={"feedback": "excellent"},
    )

    assert response.status_code == 422


def test_feedback_for_missing_assignment_returns_404(client):
    response = client.post(
        "/missions/assignments/999999/feedback",
        json={"feedback": "helpful"},
    )

    assert response.status_code == 404
