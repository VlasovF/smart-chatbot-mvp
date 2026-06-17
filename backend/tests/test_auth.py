import pytest
from fastapi.testclient import TestClient

from src.db.database import Base, engine
from src.main import app

client = TestClient(app)


@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_register_success():
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"


def test_register_duplicate():
    # Первая регистрация
    client.post(
        "/auth/register",
        json={
            "username": "testuser2",
            "email": "test2@example.com",
            "password": "testpass123",
        },
    )
    # Вторая с тем же username
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser2",
            "email": "unique@example.com",
            "password": "testpass123",
        },
    )
    assert response.status_code == 400


def test_login_success():
    # Сначала регистрируем
    client.post(
        "/auth/register",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "testpass123",
        },
    )
    # Пытаемся войти
    response = client.post(
        "/auth/login", json={"username": "loginuser", "password": "testpass123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password():
    client.post(
        "/auth/register",
        json={
            "username": "wrongpass",
            "email": "wrong@example.com",
            "password": "correctpass",
        },
    )
    response = client.post(
        "/auth/login", json={"username": "wrongpass", "password": "wrongpass"}
    )
    assert response.status_code == 401
