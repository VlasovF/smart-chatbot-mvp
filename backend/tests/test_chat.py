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


def test_chat_stream_unauthorized():
    """Проверка, что эндпоинт требует авторизации"""
    response = client.post(
        "/chat/stream",
        json={
            "messages": [{"role": "user", "content": "Hello"}],
            "temperature": 0.7,
            "max_tokens": 200,
            "system_prompt": "You are helpful",
        },
    )
    assert response.status_code == 401


def test_chat_stream_success():
    """Проверка успешного стриминга"""
    # Регистрируем и логинимся
    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
        },
    )

    login_response = client.post(
        "/auth/login", json={"username": "testuser", "password": "testpass123"}
    )

    token = login_response.json()["access_token"]

    # Отправляем запрос на стриминг
    response = client.post(
        "/chat/stream",
        json={
            "messages": [{"role": "user", "content": "Hello"}],
            "temperature": 0.7,
            "max_tokens": 200,
            "system_prompt": "You are helpful",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")

    # Читаем стрим
    lines = response.text.split("\n\n")
    has_data = False
    for line in lines:
        if line.startswith("data: "):
            has_data = True
            break

    assert has_data
