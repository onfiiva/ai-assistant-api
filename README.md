# AI Assistant API

## English

The ai-assistant-api project allows interaction with LLMs (Large Language Models) via API.
Supported models: OpenAI and Gemini.

With this project, you can:
- Send requests to LLMs
- Receive responses
- Experiment with parameters like temperature and top_p
- Control request timeouts
- Save responses in JSON format for analysis and testing
- Switch between multiple LLM providers in the same request
- Filter system/forbidden commands
- Track and log malicious requests

⸻

### 📁 Project Structure
```
ai-assistant-api/
├── app/                  # Core application library
│   ├── __pycache__/      # Python cache files
│   ├── api/              # FastAPI endpoints
│   │   ├── __pycache__/
│   │   ├── auth.py       # Authorization endpoints
│   │   └── chat.py       # Chat endpoint for interacting with LLMs
│   ├── core/             # Core configurations and utilities
│   │   ├── __pycache__/
│   │   ├── config.py     # Application settings, Vault integration, env vars
│   │   ├── logging.py    # Logging configuration
│   │   ├── redis.py      # Redis client for rate limiting
│   │   ├── security.py   # Security checks and logging of malicious requests
│   │   └── vault.py      # Vault client and helper functions
│   ├── dependencies/    # FastAPI dependency injections
│   │   ├── __pycache__/
│   │   ├── auth.py       # Authorization dependency
│   │   ├── rate_limit.py # Rate limiting dependency
│   │   ├── security.py   # Security/logging dependency
│   │   └── validation.py # Input validation dependency for chat requests
│   ├── llm/              # LLM adapters and tools
│   │   ├── __pycache__/
│   │   ├── client.py        # Base client interface for LLM adapters
│   │   ├── config.py        # Default generation configs
│   │   ├── filter.py        # System/forbidden command filtering
│   │   ├── geminiAdapter.py # Adapter for Gemini LLM
│   │   ├── normalizer.py    # Normalizes LLM responses
│   │   ├── openAIAdapter.py # Adapter for OpenAI LLM
│   │   ├── runner.py        # Handles LLM requests with retries, timeout, backoff
│   │   └── schemas.py       # Pydantic schemas for LLM requests/responses
│   ├── main.py           # Entry point for FastAPI application
│   ├── middlewares/      # Custom FastAPI middlewares
│   │   ├── __pycache__/
│   │   └── body.py        # Middleware to read request body for validation/logging
│   ├── models/           # Database and domain models
│   │   ├── __pycache__/
│   │   └── user.py        # User context and models
│   ├── schemas/          # Pydantic schemas for requests/responses
│   │   ├── __pycache__/
│   │   ├── auth.py        # Auth schemas
│   │   └── chat.py        # Chat schemas
│   ├── services/         # Application services/business logic
│   │   ├── __pycache__/
│   │   └── chat_service.py # ChatService: handles switching LLM providers
│   └── validators/       # Input validators
│       ├── __pycache__/
│       ├── generation.py  # Validate generation parameters
│       ├── provider.py    # Validate LLM provider
│       └── timeout.py     # Validate timeout values
├── docker-compose.yaml    # Docker Compose configuration for API, Redis, Vault
├── Dockerfile             # Dockerfile for API container
├── gemini/
│   └── main.py            # Direct testing script for Gemini
├── json_requests/         # Folder for saved JSON responses
├── openai/
│   └── main.py            # Direct testing script for OpenAI
├── README.md              # Project documentation (this file)
├── reflection.md          # Notes and reflections from practice sessions
└── requirements.txt       # Python dependencies
```
⸻

### 🐳 Docker Setup & Running
1.	Build and run containers:
```
docker-compose up --build
```
2.	API will be available on:
```
http://127.0.0.1:8000
```
3.	Swagger UI:
```
http://127.0.0.1:8000/docs
```
4.	Vault KV setup:
```
export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=root
vault kv patch secret/ai-assistant-api \
  OPENAI_API_KEY=sk-xxx \
  GEMINI_API_KEY=AIza-xxx \
  JWT_SECRET_KEY=supersecretkey \
  ALLOWED_PROVIDERS='["openai","gemini"]'
```
⸻

### 🔑 API Key & Vault
- OpenAI / Gemini API keys stored in Vault (preferred) or .env for dev
- DEFAULT_PROVIDER and ALLOWED_PROVIDERS configurable in Vault
- JWT_SECRET_KEY stored in Vault

⸻

### 💡 Endpoint Example
```
curl -X POST "http://127.0.0.1:8000/chat" \
-H "accept: application/json" \
-H "Content-Type: application/json" \
-d '{
  "prompt": "Write a hello world function",
  "provider": "gemini",
  "instruction": "You are a Python Senior Dev",
  "timeout": 60
}'
```
Response saved optionally in json_requests/. Logging tracks retries, forbidden commands, and timeout events.

⸻

### 📚 Resources
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference/introduction)
- [Gemini API Documentatio](https://ai.google.dev/gemini-api/docs?hl=en)

# AI Assistant API

## Русский

Проект ai-assistant-api позволяет взаимодействовать с LLM (Large Language Models) через API.
Поддерживаемые модели: OpenAI и Gemini.

С помощью проекта можно:
- Отправлять запросы к LLM
- Получать ответы
- Экспериментировать с параметрами, такими как temperature и top_p
- Контролировать таймауты запросов
- Сохранять ответы в формате JSON для анализа и тестирования
- Переключаться между несколькими провайдерами LLM в одном запросе
- Фильтровать системные и запрещённые команды
- Логировать попытки злоумышленников и нарушения правил

⸻

### 📁 Структура проекта
```
ai-assistant-api/
├── app/                  # Основная библиотека приложения
│   ├── __pycache__/      # Кэш Python
│   ├── api/              # FastAPI эндпоинты
│   │   ├── __pycache__/
│   │   ├── auth.py       # Эндпоинты авторизации
│   │   └── chat.py       # Эндпоинт для чата с LLM
│   ├── core/             # Основные настройки и утилиты
│   │   ├── __pycache__/
│   │   ├── config.py     # Настройки приложения, интеграция с Vault, переменные окружения
│   │   ├── logging.py    # Конфигурация логирования
│   │   ├── redis.py      # Клиент Redis для ограничения частоты запросов
│   │   ├── security.py   # Безопасность, логирование нарушений
│   │   └── vault.py      # Клиент Vault и вспомогательные функции
│   ├── dependencies/    # FastAPI зависимости
│   │   ├── __pycache__/
│   │   ├── auth.py       # Зависимость авторизации
│   │   ├── rate_limit.py # Зависимость ограничения частоты запросов
│   │   ├── security.py   # Безопасность и логирование
│   │   └── validation.py # Валидация входных данных для чата
│   ├── llm/              # Адаптеры и утилиты LLM
│   │   ├── __pycache__/
│   │   ├── client.py        # Базовый интерфейс клиента LLM
│   │   ├── config.py        # Конфигурации генерации по умолчанию
│   │   ├── filter.py        # Фильтрация системных команд
│   │   ├── geminiAdapter.py # Адаптер для Gemini LLM
│   │   ├── normalizer.py    # Нормализация ответов LLM
│   │   ├── openAIAdapter.py # Адаптер для OpenAI LLM
│   │   ├── runner.py        # Обработка запросов с ретраями и таймаутами
│   │   └── schemas.py       # Pydantic схемы для запросов и ответов
│   ├── main.py           # Точка входа FastAPI
│   ├── middlewares/      # Пользовательские middlewares
│   │   ├── __pycache__/
│   │   └── body.py        # Middleware для чтения тела запроса
│   ├── models/           # Модели данных и пользователей
│   │   ├── __pycache__/
│   │   └── user.py        # Модель и контекст пользователя
│   ├── schemas/          # Pydantic схемы запросов и ответов
│   │   ├── __pycache__/
│   │   ├── auth.py        # Схемы авторизации
│   │   └── chat.py        # Схемы для чата
│   ├── services/         # Сервисы приложения
│   │   ├── __pycache__/
│   │   └── chat_service.py # ChatService для работы с несколькими LLM
│   └── validators/       # Валидации входных данных
│       ├── __pycache__/
│       ├── generation.py  # Валидация параметров генерации
│       ├── provider.py    # Валидация провайдера LLM
│       └── timeout.py     # Валидация таймаута
├── docker-compose.yaml    # Docker Compose для API, Redis, Vault
├── Dockerfile             # Dockerfile для контейнера API
├── gemini/
│   └── main.py            # Скрипт тестирования Gemini
├── json_requests/         # Сохранённые JSON ответы
├── openai/
│   └── main.py            # Скрипт тестирования OpenAI
├── README.md              # Документация проекта
├── reflection.md          # Заметки после практики
└── requirements.txt       # Python зависимости
```
⸻

### 🐳 Docker и запуск
1.	Сборка и запуск контейнеров:
```
docker-compose up --build
```
2.	API доступно на:
```
http://127.0.0.1:8000
```
3.	Swagger UI:
```
http://127.0.0.1:8000/docs
```
4.	Настройка Vault KV:
```
export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=root
vault kv patch secret/ai-assistant-api \
  OPENAI_API_KEY=sk-xxx \
  GEMINI_API_KEY=AIza-xxx \
  JWT_SECRET_KEY=supersecretkey \
  ALLOWED_PROVIDERS='["openai","gemini"]'
```
⸻

### 🔑 Настройка ключей и Vault
- OpenAI / Gemini ключи можно хранить в Vault (рекомендуется) или в .env для dev
- DEFAULT_PROVIDER и ALLOWED_PROVIDERS конфигурируются через Vault
- JWT_SECRET_KEY хранится в Vault

⸻

### 💡 Пример запроса к эндпоинту
```
curl -X POST "http://127.0.0.1:8000/chat" \
-H "accept: application/json" \
-H "Content-Type: application/json" \
-d '{
  "prompt": "Напишите функцию hello world",
  "provider": "gemini",
  "instruction": "Вы опытный Python разработчик",
  "timeout": 60
}'
```
Ответ возвращается в нормализованном формате JSON и при необходимости сохраняется в json_requests/. Логирование отслеживает ретраи, запрещённые команды и таймауты.

⸻

### 📚 Ресурсы
- [Документация OpenAI API](https://platform.openai.com/docs/api-reference/introduction)
- [Документация Gemini API](https://ai.google.dev/gemini-api/docs?hl=ru)