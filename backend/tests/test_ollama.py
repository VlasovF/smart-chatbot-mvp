import pytest

from src.core.config import settings
from src.llm.ollama import OllamaLLMClient


@pytest.mark.asyncio
async def test_ollama_generate():
    """Тест синхронной генерации Ollama"""
    client = OllamaLLMClient(
        model="phi4-mini:3.8b", base_url=settings.OLLAMA_BASE_URL
    )

    messages = [{"role": "user", "content": "Привет! Как дела?"}]

    response = await client.generate(messages=messages)

    assert isinstance(response, str)
    assert len(response) > 0


@pytest.mark.asyncio
async def test_ollama_stream():
    """Тест стриминга Ollama"""
    client = OllamaLLMClient(
        model="phi4-mini:3.8b", base_url=settings.OLLAMA_BASE_URL
    )

    messages = [{"role": "user", "content": "Расскажи шутку"}]

    tokens = []
    async for token in client.stream_generate(messages=messages):
        tokens.append(token)

    assert len(tokens) > 0
    full_response = "".join(tokens)
    assert len(full_response) > 10
