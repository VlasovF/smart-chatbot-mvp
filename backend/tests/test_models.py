import pytest
from fastapi.testclient import TestClient

from src.db.database import Base, engine
from src.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_get_models_unauthorized():
    """Проверка, что эндпоинт моделей требует авторизации"""
    response = client.get("/models/")
    assert response.status_code == 401


def test_get_models_authorized():
    """Проверка получения списка моделей"""
    # Регистрация и логин
    client.post(
        "/auth/register",
        json={
            "username": "modeluser",
            "email": "model@example.com",
            "password": "testpass123",
        },
    )

    login_response = client.post(
        "/auth/login", json={"username": "modeluser", "password": "testpass123"}
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/models/", headers={"Authorization": f"Bearer {token}"}
    )

    # Может вернуть 503, если Ollama не запущен, но это нормально
    assert response.status_code in [200, 503]

    if response.status_code == 200:
        data = response.json()
        assert "models" in data
        assert isinstance(data["models"], list)
