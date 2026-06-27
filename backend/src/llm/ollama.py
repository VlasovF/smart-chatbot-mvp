import json
from collections.abc import AsyncGenerator

import httpx

from src.core.config import settings
from src.llm.base import BaseLLMClient


class OllamaLLMClient(BaseLLMClient):
    """Клиент для работы с Ollama API"""

    def __init__(
        self, model: str = "phi4-mini:3.8b", base_url: str | None = None
    ):
        """
        Инициализация клиента Ollama

        Args:
            model: Название модели (по умолчанию phi4-mini:3.8b)
            base_url: URL Ollama API (по умолчанию из настроек)
        """
        self.model = model
        self.base_url = base_url or settings.OLLAMA_BASE_URL

    async def generate(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 200,
        system_prompt: str = "Ты полезный ассистент. Отвечай кратко и по делу.",
    ) -> str:
        """
        Синхронная генерация ответа (без стриминга)
        """
        # Формируем запрос для Ollama
        ollama_messages = []

        # Добавляем системный промпт
        if system_prompt:
            ollama_messages.append({"role": "system", "content": system_prompt})

        # Добавляем историю сообщений
        ollama_messages.extend(messages)

        payload = {
            "model": self.model,
            "messages": ollama_messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/api/chat", json=payload
            )
            response.raise_for_status()

            data = response.json()
            return data.get("message", {}).get("content", "")

    async def stream_generate(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 200,
        system_prompt: str = "Ты полезный ассистент. Отвечай кратко и по делу.",
    ) -> AsyncGenerator[str, None]:
        """
        Асинхронная генерация с потоковой выдачей токенов
        """
        # Формируем запрос для Ollama
        ollama_messages = []

        if system_prompt:
            ollama_messages.append({"role": "system", "content": system_prompt})

        ollama_messages.extend(messages)

        payload = {
            "model": self.model,
            "messages": ollama_messages,
            "stream": True,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }

        async with (
            httpx.AsyncClient(timeout=60.0) as client,
            client.stream(
                "POST", f"{self.base_url}/api/chat", json=payload
            ) as response,
        ):
            response.raise_for_status()

            async for line in response.aiter_lines():
                if not line.strip():
                    continue

                try:
                    data = json.loads(line)

                    # Проверяем, есть ли сообщение
                    if "message" in data:
                        content = data["message"].get("content", "")
                        if content:
                            yield content

                    # Проверяем, завершён ли ответ
                    if data.get("done", False):
                        break

                except json.JSONDecodeError:
                    continue
