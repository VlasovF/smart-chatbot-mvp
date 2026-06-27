from src.core.config import settings
from src.llm.base import BaseLLMClient
from src.llm.mock import MockLLMClient
from src.llm.ollama import OllamaLLMClient


def get_llm_client() -> BaseLLMClient:
    """
    Фабрика для создания LLM клиента

    Returns:
        BaseLLMClient: Экземпляр клиента (Mock или Ollama)
    """
    client_type = settings.LLM_CLIENT_TYPE

    if client_type == "mock":
        return MockLLMClient()
    elif client_type == "ollama":
        return OllamaLLMClient(
            model=settings.OLLAMA_MODEL, base_url=settings.OLLAMA_BASE_URL
        )
    else:
        raise ValueError(f"Unknown LLM client type: {client_type}")
