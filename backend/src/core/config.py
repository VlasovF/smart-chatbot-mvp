from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Общие настройки
    ENV: str = "development"

    # JWT настройки
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # База данных
    DATABASE_URL: str = "sqlite:///./app.db"

    # LLM настройки
    LLM_CLIENT_TYPE: str = "mock"  # mock или ollama
    OLLAMA_BASE_URL: str = "http://host.docker.internal:11434"
    OLLAMA_MODEL: str = "phi4-mini:3.8b"

    # CORS настройки
    BACKEND_CORS_ORIGINS_RAW: str = (
        "http://localhost:5173,http://127.0.0.1:5173"
    )

    @computed_field
    @property
    def BACKEND_CORS_ORIGINS(self) -> list[str]:  # noqa: N802
        """Преобразует строку с запятыми в список"""
        return [
            origin.strip()
            for origin in self.BACKEND_CORS_ORIGINS_RAW.split(",")
            if origin.strip()
        ]

    # Опциональные настройки с авто-подстановкой из .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # игнорировать лишние переменные в .env
    )


settings = Settings()
