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


def test_chat_with_ollama():
    """Тест чата с реальной моделью"""
    # Регистрация и логин
    client.post(
        "/auth/register",
        json={
            "username": "ollamauser",
            "email": "ollama@example.com",
            "password": "testpass123",
        },
    )

    login_response = client.post(
        "/auth/login",
        json={"username": "ollamauser", "password": "testpass123"},
    )

    token = login_response.json()["access_token"]

    # Запрос к чату с указанием модели
    response = client.post(
        "/chat/stream",
        json={
            "messages": [{"role": "user", "content": "Привет"}],
            "temperature": 0.7,
            "max_tokens": 100,
            "system_prompt": "Отвечай кратко",
            "model": "phi4-mini:3.8b",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert "text/event-stream" in response.headers.get("content-type", "")

    # Проверяем, что есть данные
    lines = response.text.split("\n\n")
    has_data = False
    for line in lines:
        if line.startswith("data: "):
            has_data = True
            break
    assert has_data
