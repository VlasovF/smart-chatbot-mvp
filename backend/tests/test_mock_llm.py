import pytest

from src.llm.mock import MockLLMClient


@pytest.mark.asyncio
async def test_mock_generate():
    client = MockLLMClient()

    messages = [{"role": "user", "content": "Привет, как дела?"}]

    response = await client.generate(
        messages=messages, temperature=0.7, max_tokens=100
    )

    assert isinstance(response, str)
    assert len(response) > 0
    assert "Привет" in response or "дела" in response


@pytest.mark.asyncio
async def test_mock_stream():
    client = MockLLMClient()

    messages = [{"role": "user", "content": "Расскажи шутку"}]

    tokens = []
    async for token in client.stream_generate(
        messages=messages, temperature=0.7, max_tokens=50
    ):
        tokens.append(token)

    assert len(tokens) > 0

    full_response = "".join(tokens)
    assert isinstance(full_response, str)
    assert len(full_response) > 0
