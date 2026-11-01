import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from core.database import Base
from core.security import create_access_token
from dependencies.database import get_db
from main import app
from models.user import User


@pytest.fixture
def preferences_client():
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
            user = User(
                email="preferences@example.com",
                password_hash=None,
                is_active=True,
            )
            db.add(user)
            db.commit()
            db.refresh(user)

            client.user_id = user.id

        client.headers.update({
            "Authorization": (
                f"Bearer {create_access_token(client.user_id)}"
            )
        })

        yield client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


def test_get_difficulty_preference(preferences_client):
    response = preferences_client.get("/preferences/difficulty")

    assert response.status_code == 200
    assert response.json() == {
        "difficulty_preference": "moderate"
    }


def test_update_difficulty_preference(preferences_client):
    response = preferences_client.put(
        "/preferences/difficulty",
        json={"difficulty_preference": "easy"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "difficulty_preference": "easy"
    }


def test_difficulty_preference_persists(preferences_client):
    preferences_client.put(
        "/preferences/difficulty",
        json={"difficulty_preference": "challenging"},
    )

    response = preferences_client.get("/preferences/difficulty")

    assert response.status_code == 200
    assert response.json() == {
        "difficulty_preference": "challenging"
    }


def test_invalid_difficulty_preference_is_rejected(preferences_client):
    response = preferences_client.put(
        "/preferences/difficulty",
        json={"difficulty_preference": "impossible"},
    )

    assert response.status_code == 422


def test_difficulty_preference_requires_authentication(
    preferences_client,
):
    preferences_client.headers.pop("Authorization")

    response = preferences_client.get("/preferences/difficulty")

    assert response.status_code == 401
