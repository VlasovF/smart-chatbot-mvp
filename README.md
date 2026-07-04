# Smart Chatbot MVP

Асинхронное веб-приложение на **FastAPI + React + TypeScript** с авторизацией (JWT), стримингом ответов и поддержкой малых языковых моделей через **Ollama**.

## Используемые технологии

    Бэкенд: FastAPI, SQLAlchemy, Pydantic, PyJWT, bcrypt
    Фронтенд: Reac, TypeScript, Vite, React Router
    LLM: Ollama
    Тестирование: pytest, Vitest, React Testing Library
    Линтеры: ruff, ESLint, Prettier
    Контейнеризация: Docker, Docker Compose

## Быстрый старт

### Требования
- Docker & Docker Compose
- Make (опционально)
- Node.js 18+ (для локальной разработки)
- Python 3.11+ (для локальной разработки)

### Запуск

```bash
git clone https://github.com/VlasovF/smart-chatbot-mvp.git
cd smart-chatbot-mvp
docker-compose up --build
```

Frontend: http://localhost:5173
Backend API: http://localhost:8000/docs

## Структура

```text
smart-chatbot-mvp/
├── backend/              # FastAPI бэкенд
│   ├── src/
│   │   ├── api/          # Эндпоинты (auth, chat, models)
│   │   ├── core/         # Конфигурация, безопасность
│   │   ├── db/           # SQLAlchemy модели
│   │   ├── llm/          # LLM клиенты (mock, ollama)
│   │   └── services/     # Бизнес-логика
│   ├── tests/            # Тесты (pytest)
│   └── pyproject.toml    # Poetry зависимости
├── frontend/             # React + TypeScript фронтенд
│   ├── src/
│   │   ├── components/   # React компоненты
│   │   ├── hooks/        # Хуки (useAuth)
│   │   └── services/     # API клиенты
│   └── package.json      # npm зависимости
├── docker-compose.yml
├── Makefile
└── .env.example
```

## Архитектура

```text
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   React     │      │   FastAPI   │      │   Ollama    │
│   + Vite    │◄────►│   + SQLite  │◄────►│   + SLM     │
│  (TypeScript)│      │   (Python)  │      │   (модель)  │
└─────────────┘      └─────────────┘      └─────────────┘
     │                      │                      │
     └───── JWT Auth ───────┘                      │
     └─────── SSE Streaming ───────────────────────┘
```