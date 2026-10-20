
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from core.database import Base
from dependencies.database import get_db
from main import app
from models.user import User


@pytest.fixture
def client():
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

    with TestClient(app) as test_client:
        test_client.test_db = TestingSessionLocal
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "new-user@example.com",
            "password": "test-password-123",
        },
    )

    assert response.status_code == 201
    assert response.json()["email"] == "new-user@example.com"
    assert "password_hash" not in response.json()

    with client.test_db() as db:
        user = db.query(User).filter_by(
            email="new-user@example.com"
        ).first()
        assert user is not None
        assert user.password_hash != "test-password-123"
        assert user.password_hash is not None


def test_register_duplicate_email(client):
    payload = {
        "email": "duplicate@example.com",
        "password": "test-password-123",
    }

    assert client.post("/auth/register", json=payload).status_code == 201
    response = client.post("/auth/register", json=payload)

    assert response.status_code == 409


def test_login_success(client):
    client.post(
        "/auth/register",
        json={
            "email": "login@example.com",
            "password": "test-password-123",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "login@example.com",
            "password": "test-password-123",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["access_token"]
    assert body["token_type"] == "bearer"
    assert body["user"]["email"] == "login@example.com"
    assert "password_hash" not in body["user"]


def test_login_wrong_password(client):
    client.post(
        "/auth/register",
        json={
            "email": "wrong-password@example.com",
            "password": "test-password-123",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "wrong-password@example.com",
            "password": "incorrect-password",
        },
    )

    assert response.status_code == 401


def test_login_unknown_email(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "unknown@example.com",
            "password": "test-password-123",
        },
    )

    assert response.status_code == 401
