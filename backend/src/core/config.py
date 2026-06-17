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

    # Опциональные настройки с авто-подстановкой из .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # игнорировать лишние переменные в .env
    )


settings = Settings()
