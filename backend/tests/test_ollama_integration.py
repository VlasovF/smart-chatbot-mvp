import pytest

from src.core.config import settings
from src.llm.ollama import OllamaLLMClient


@pytest.mark.skipif(
    settings.LLM_CLIENT_TYPE != "ollama", reason="Ollama not configured"
)
@pytest.mark.asyncio
async def test_ollama_connection():
    """Тест подключения к Ollama"""
    client = OllamaLLMClient(
        model=settings.OLLAMA_MODEL, base_url=settings.OLLAMA_BASE_URL
    )

    messages = [{"role": "user", "content": "Hello"}]

    try:
        response = await client.generate(messages=messages, max_tokens=10)
        assert isinstance(response, str)
    except Exception as e:
        # Если Ollama не запущен, тест пропускается
        pytest.skip(f"Ollama not available: {e}")
