from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator


class BaseLLMClient(ABC):
    """Абстрактный базовый класс для LLM клиентов"""

    @abstractmethod
    async def generate(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 200,
        system_prompt: str = "Ты полезный ассистент.",
    ) -> str:
        """Синхронная генерация ответа (без стриминга)"""
        pass

    @abstractmethod
    async def stream_generate(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 200,
        system_prompt: str = "Ты полезный ассистент.",
    ) -> AsyncGenerator[str, None]:
        """Асинхронная генерация с потоковой выдачей токенов"""
        pass
