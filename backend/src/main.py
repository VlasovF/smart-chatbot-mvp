from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import auth
from src.db.database import Base, engine

# Создание таблиц
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Chatbot MVP", version="0.1.0")

# --- Настройка CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:5173",  # альтернативный адрес
        "http://localhost:3000",  # если используете другой порт
    ],
    allow_credentials=True,  # разрешить отправку cookies и авторизационных заголовков
    allow_methods=[
        "*"
    ],  # разрешить все HTTP методы (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # разрешить все заголовки
)

# Подключаем роуты
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Smart Chatbot API is running"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}
