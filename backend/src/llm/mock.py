import asyncio
import random
from collections.abc import AsyncGenerator

from src.llm.base import BaseLLMClient


class MockLLMClient(BaseLLMClient):
    """Мок-клиент для имитации работы LLM"""

    async def generate(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 200,
        system_prompt: str = "Ты полезный ассистент.",
    ) -> str:
        """Имитация генерации (без стриминга)"""
        # Берём последнее сообщение пользователя
        last_user_message = ""
        for msg in reversed(messages):
            if msg["role"] == "user":
                last_user_message = msg["content"]
                break

        # Создаём имитацию ответа
        responses = [
            f"Интересный вопрос! Давайте подумаем: {last_user_message[:50]}...",
            f"Я понимаю, что вы имеете в виду. Мой ответ: {last_user_message} — отличная мысль!",
            f"Хм, дайте подумать... {last_user_message}. Это действительно важный момент.",
            f"Спасибо за ваш вопрос! {last_user_message} — это то, что я могу прокомментировать.",
            f"О, это интересно! {last_user_message} — давайте разберёмся подробнее.",
        ]

        # Добавляем немного вариативности на основе temperature
        if temperature > 0.8:
            responses.append("Вау! Это очень креативный вопрос! 🤔")
        elif temperature < 0.4:
            responses.append("Коротко и ясно: да, вы правы.")

        return random.choice(responses)

    async def stream_generate(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 200,
        system_prompt: str = "Ты полезный ассистент.",
    ) -> AsyncGenerator[str, None]:
        """Имитация потоковой генерации"""

        # Получаем полный ответ
        full_response = await self.generate(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            system_prompt=system_prompt,
        )

        # Разбиваем на слова и выдаём по одному
        words = full_response.split()

        # Регулируем скорость на основе температуры
        # Чем выше температура, тем более "креативная" задержка
        base_delay = 0.05
        if temperature > 0.8:
            delay_variation = 0.15  # более неравномерная выдача
        elif temperature < 0.4:
            delay_variation = 0.02  # более равномерная выдача
        else:
            delay_variation = 0.08

        # Выдаём слова с добавлением пробелов
        for i, word in enumerate(words):
            # Добавляем случайную задержку для имитации "мышления"
            delay = base_delay + random.uniform(0, delay_variation)
            await asyncio.sleep(delay)

            yield word + (" " if i < len(words) - 1 else "")
