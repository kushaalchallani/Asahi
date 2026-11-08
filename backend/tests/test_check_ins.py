import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from core.database import Base
from core.security import create_access_token
from dependencies.database import get_db
from main import app
from models.check_in import CheckIn
from models.user import User


@pytest.fixture
def checkin_client():
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
            user_a = User(
                email="checkin-a@example.com",
                password_hash=None,
                is_active=True,
            )
            user_b = User(
                email="checkin-b@example.com",
                password_hash=None,
                is_active=True,
            )
            db.add_all([user_a, user_b])
            db.flush()

            checkin_a = CheckIn(
                user_id=user_a.id,
                feeling="Stressed",
                note="User A note",
            )
            checkin_b = CheckIn(
                user_id=user_b.id,
                feeling="Lonely",
                note="User B note",
            )
            db.add_all([checkin_a, checkin_b])
            db.commit()

            client.user_a_id = user_a.id
            client.user_b_id = user_b.id
            client.checkin_a_id = checkin_a.id
            client.checkin_b_id = checkin_b.id

        yield client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


def test_check_ins_require_authentication(checkin_client):
    response = checkin_client.get("/check-ins")
    assert response.status_code == 401


def test_user_only_sees_own_check_ins(checkin_client):
    checkin_client.headers.update({
        "Authorization": (
            f"Bearer {create_access_token(checkin_client.user_a_id)}"
        )
    })

    response = checkin_client.get("/check-ins")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == checkin_client.checkin_a_id
    assert data[0]["feeling"] == "Stressed"


def test_insights_only_count_own_check_ins(checkin_client):
    checkin_client.headers.update({
        "Authorization": (
            f"Bearer {create_access_token(checkin_client.user_a_id)}"
        )
    })

    response = checkin_client.get("/check-ins/insights")

    assert response.status_code == 200
    data = response.json()
    assert data["check_in_count"] == 1
    assert data["most_common_feeling"] == "Stressed"


def test_create_check_in_assigns_current_user(checkin_client):
    checkin_client.headers.update({
        "Authorization": (
            f"Bearer {create_access_token(checkin_client.user_a_id)}"
        )
    })

    response = checkin_client.post(
        "/check-ins",
        json={"feeling": "A little low", "note": "Test note"},
    )

    assert response.status_code == 200
    assert response.json()["user_id"] == checkin_client.user_a_id


def test_create_check_in_without_note(checkin_client):
    """Check-in can be created without optional note."""
    checkin_client.headers.update({
        "Authorization": (
            f"Bearer {create_access_token(checkin_client.user_a_id)}"
        )
    })

    response = checkin_client.post(
        "/check-ins",
        json={"feeling": "Okay"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == checkin_client.user_a_id
    assert data["feeling"] == "Okay"


def test_check_in_creation_requires_authentication(checkin_client):
    """Creating a check-in requires authentication."""
    response = checkin_client.post(
        "/check-ins",
        json={"feeling": "Okay"},
    )
    assert response.status_code == 401
