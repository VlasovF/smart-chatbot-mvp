# Makefile для Smart Chatbot MVP
# Использование: make <command>

.PHONY: help build up down restart logs shell \
        backend-shell frontend-shell \
        test test-security test-auth test-all \
        lint lint-backend lint-frontend \
        format format-backend format-frontend \
        clean clean-docker clean-all \
		test-integration test-ollama coverage-report

# --- Переменные ---
DOCKER_COMPOSE = docker compose
BACKEND_CONTAINER = backend
FRONTEND_CONTAINER = frontend
PYTEST_ARGS = -v --tb=short

# --- Цвета для вывода ---
GREEN = \033[0;32m
YELLOW = \033[0;33m
RED = \033[0;31m
NC = \033[0m # No Color

# --- Справка ---
help: ## Показать все доступные команды
	@echo "$(GREEN)Доступные команды для Smart Chatbot MVP:$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Примеры:$(NC)"
	@echo "  make build    - Собрать и запустить контейнеры"
	@echo "  make test     - Запустить все тесты"
	@echo "  make shell    - Войти в контейнер бэкенда"

# --- Docker управление ---
build: ## Собрать и запустить контейнеры
	@echo "$(GREEN)🔨 Сборка и запуск контейнеров...$(NC)"
	$(DOCKER_COMPOSE) up --build -d
	@echo "$(GREEN)✅ Контейнеры запущены!$(NC)"
	@echo "  Frontend: http://localhost:5173"
	@echo "  Backend:  http://localhost:8000"
	@echo "  Docs:     http://localhost:8000/docs"

up: ## Запустить контейнеры (без пересборки)
	@echo "$(GREEN)🚀 Запуск контейнеров...$(NC)"
	$(DOCKER_COMPOSE) up -d
	@echo "$(GREEN)✅ Контейнеры запущены!$(NC)"

down: ## Остановить контейнеры
	@echo "$(YELLOW)🛑 Остановка контейнеров...$(NC)"
	$(DOCKER_COMPOSE) down
	@echo "$(GREEN)✅ Контейнеры остановлены$(NC)"

restart: ## Перезапустить контейнеры
	@echo "$(YELLOW)🔄 Перезапуск контейнеров...$(NC)"
	$(DOCKER_COMPOSE) restart
	@echo "$(GREEN)✅ Контейнеры перезапущены$(NC)"

logs: ## Показать логи всех контейнеров
	$(DOCKER_COMPOSE) logs -f

logs-backend: ## Показать логи бэкенда
	$(DOCKER_COMPOSE) logs -f $(BACKEND_CONTAINER)

logs-frontend: ## Показать логи фронтенда
	$(DOCKER_COMPOSE) logs -f $(FRONTEND_CONTAINER)

# --- Shell / Интерактивный доступ ---
shell: backend-shell ## Войти в контейнер бэкенда (по умолчанию)

backend-shell: ## Войти в контейнер бэкенда
	@echo "$(GREEN)🐍 Вход в контейнер бэкенда...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) bash

frontend-shell: ## Войти в контейнер фронтенда
	@echo "$(GREEN)🖥️ Вход в контейнер фронтенда...$(NC)"
	$(DOCKER_COMPOSE) exec $(FRONTEND_CONTAINER) sh

# --- Тесты ---
test: test-all ## Запустить все тесты (по умолчанию)

test-all: ## Запустить все тесты
	@echo "$(GREEN)🧪 Запуск всех тестов...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) pytest $(PYTEST_ARGS)

test-security: ## Запустить тесты безопасности (test_security.py)
	@echo "$(GREEN)🔐 Запуск тестов безопасности...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) pytest tests/test_security.py $(PYTEST_ARGS)

test-auth: ## Запустить тесты аутентификации (test_auth.py)
	@echo "$(GREEN)🔑 Запуск тестов аутентификации...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) pytest tests/test_auth.py $(PYTEST_ARGS)

test-chat: ## Запустить тесты чата (test_chat.py)
	@echo "$(GREEN)💬 Запуск тестов чата...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) pytest tests/test_chat.py $(PYTEST_ARGS)

test-coverage: ## Запустить тесты с покрытием
	@echo "$(GREEN)📊 Запуск тестов с покрытием...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) pytest --cov=src --cov-report=html --cov-report=term $(PYTEST_ARGS)
	@echo "$(GREEN)✅ Отчёт о покрытии создан в backend/htmlcov/index.html$(NC)"

test-integration: ## Запустить интеграционные тесты
	@echo "$(GREEN)🧪 Запуск интеграционных тестов...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) pytest tests/ -m integration

test-ollama: ## Запустить тесты Ollama
	@echo "$(GREEN)🦙 Запуск тестов Ollama...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) pytest tests/test_ollama.py -v

coverage-report: ## Сгенерировать отчёт по покрытию
	@echo "$(GREEN)📊 Генерация отчёта покрытия...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) pytest --cov=src --cov-report=html --cov-report=term
	@echo "$(GREEN)✅ Отчёт: backend/htmlcov/index.html$(NC)"

# --- Линтеры ---
lint: lint-backend lint-frontend ## Запустить все линтеры

lint-backend: ## Запустить ruff (бэкенд)
	@echo "$(GREEN)🔍 Проверка бэкенда ruff...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) ruff check src/ tests/
	@echo "$(GREEN)✅ ruff проверка пройдена$(NC)"

lint-frontend: ## Запустить ESLint (фронтенд)
	@echo "$(GREEN)🔍 Проверка фронтенда ESLint...$(NC)"
	$(DOCKER_COMPOSE) exec $(FRONTEND_CONTAINER) npm run lint
	@echo "$(GREEN)✅ ESLint проверка пройдена$(NC)"

lint-fix: lint-fix-backend lint-fix-frontend ## Исправить ошибки линтеров

lint-fix-backend: ## Исправить ошибки ruff
	@echo "$(GREEN)🔧 Исправление ошибок в бэкенде...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) ruff check --fix src/ tests/
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) ruff format src/ tests/

lint-fix-frontend: ## Исправить ошибки ESLint и Prettier
	@echo "$(GREEN)🔧 Исправление ошибок во фронтенде...$(NC)"
	$(DOCKER_COMPOSE) exec $(FRONTEND_CONTAINER) npm run lint:fix
	$(DOCKER_COMPOSE) exec $(FRONTEND_CONTAINER) npm run format

# --- Форматирование ---
format: format-backend format-frontend ## Отформатировать весь код

format-backend: ## Отформатировать бэкенд (ruff)
	@echo "$(GREEN)🎨 Форматирование бэкенда...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) ruff format src/ tests/

format-frontend: ## Отформатировать фронтенд (Prettier)
	@echo "$(GREEN)🎨 Форматирование фронтенда...$(NC)"
	$(DOCKER_COMPOSE) exec $(FRONTEND_CONTAINER) npm run format

# --- Зависимости ---
install: ## Установить все зависимости
	@echo "$(GREEN)📦 Установка зависимостей...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) poetry install
	$(DOCKER_COMPOSE) exec $(FRONTEND_CONTAINER) npm install

install-backend: ## Установить зависимости бэкенда
	@echo "$(GREEN)📦 Установка зависимостей бэкенда...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) poetry install

install-frontend: ## Установить зависимости фронтенда
	@echo "$(GREEN)📦 Установка зависимостей фронтенда...$(NC)"
	$(DOCKER_COMPOSE) exec $(FRONTEND_CONTAINER) npm install

# --- Очистка ---
clean: ## Очистить кэши и временные файлы
	@echo "$(YELLOW)🧹 Очистка кэшей...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) rm -rf .pytest_cache __pycache__ */__pycache__
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) rm -rf htmlcov .coverage
	$(DOCKER_COMPOSE) exec $(FRONTEND_CONTAINER) rm -rf node_modules/.cache
	@echo "$(GREEN)✅ Очистка завершена$(NC)"

clean-docker: ## Полная очистка Docker (контейнеры, образы, volumes)
	@echo "$(RED)⚠️  ВНИМАНИЕ: Это удалит все контейнеры, образы и volumes!$(NC)"
	@read -p "Вы уверены? [y/N] " -n 1 -r; \
	echo ""; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		$(DOCKER_COMPOSE) down -v; \
		docker system prune -af --volumes; \
		echo "$(GREEN)✅ Очистка Docker завершена$(NC)"; \
	else \
		echo "$(YELLOW)❌ Очистка отменена$(NC)"; \
	fi

clean-all: clean clean-docker ## Полная очистка (кэши + Docker)

# --- Миграции БД ---
migrate: ## Создать таблицы в БД (не используется Alembic)
	@echo "$(GREEN)🗄️ Создание таблиц БД...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) python -c "from src.db.database import engine, Base; Base.metadata.create_all(bind=engine)"
	@echo "$(GREEN)✅ Таблицы созданы$(NC)"

reset-db: ## Сбросить БД (удалить и создать заново)
	@echo "$(RED)⚠️  Удаление базы данных...$(NC)"
	@read -p "Вы уверены? [y/N] " -n 1 -r; \
	echo ""; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) rm -f app.db; \
		$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) python -c "from src.db.database import engine, Base; Base.metadata.create_all(bind=engine)"; \
		echo "$(GREEN)✅ База данных сброшена и создана заново$(NC)"; \
	else \
		echo "$(YELLOW)❌ Операция отменена$(NC)"; \
	fi

# --- Разработка ---
dev: ## Запустить проект в режиме разработки
	@echo "$(GREEN)🚀 Запуск в режиме разработки...$(NC)"
	$(DOCKER_COMPOSE) up --build

status: ## Показать статус контейнеров
	@echo "$(GREEN)📊 Статус контейнеров:$(NC)"
	$(DOCKER_COMPOSE) ps

# --- Default target ---
.DEFAULT_GOAL := help