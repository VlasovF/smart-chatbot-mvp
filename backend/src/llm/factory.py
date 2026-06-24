from src.core.config import settings
from src.llm.base import BaseLLMClient
from src.llm.mock import MockLLMClient


def get_llm_client() -> BaseLLMClient:
    """Фабрика для создания LLM клиента"""
    client_type = settings.LLM_CLIENT_TYPE

    if client_type == "mock":
        return MockLLMClient()
    elif client_type == "ollama":
        # TODO: Добавим позже на Этапе 8
        raise NotImplementedError("Ollama client not implemented yet")
    else:
        raise ValueError(f"Unknown LLM client type: {client_type}")
