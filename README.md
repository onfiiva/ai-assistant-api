# AI Assistant API

[English](#english) | [Русский](#русский)

- [🐳 Installation](#-docker-setup--running)
- [🐳 Установка](#-docker-и-запуск)

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
- Apply rate limiting per user/admin
- Embed documents, store them in a vector database (Qdrant), and perform semantic search
- Work with multi-language content and large documents by chunking

⸻

### 📁 Project Structure
```
ai-assistant-api/
├── alembic/                # Database migrations (PostgreSQL)
│   ├── env.py             # Alembic environment config
│   ├── README             # Alembic notes / description
│   ├── script.py.mako      # Alembic script template
│   └── versions/           # Migration files
├── alembic.ini             # Alembic config
├── app/                    # Core application library
│   ├── api/                # FastAPI endpoints
│   │   ├── auth.py         # Authorization endpoints
│   │   ├── chat.py         # Chat endpoints
│   │   ├── embeddings.py   # Endpoints for embeddings and semantic search
│   │   ├── ingestion.py    # Endpoint to ingest documents into vector DB
│   │   └── search.py       # Endpoint to perform search queries
│   ├── core/               # Core configurations and utilities
│   │   ├── config.py       # App settings, Vault integration, env vars
│   │   ├── logging.py      # Logging setup
│   │   ├── redis.py        # Redis client for rate limiting
│   │   ├── security.py     # Security utils, logging forbidden requests
│   │   └── vault.py        # Vault client helpers
│   ├── dependencies/       # FastAPI dependency injections
│   │   ├── auth.py         # Authorization dependency
│   │   ├── rate_limit.py   # Rate limiting dependency
│   │   ├── security.py     # Security/logging dependency
│   │   ├── user.py         # User context / current user dependency
│   │   └── validation.py   # Input validation dependency for chat requests
│   ├── embeddings/         # Embedding clients, services, similarity logic
│   │   ├── clients/
│   │   │   ├── client.py        # Base embedding client interface
│   │   │   ├── gemini_client.py # Gemini embedding client
│   │   │   └── openai_client.py # OpenAI embedding client
│   │   ├── factory.py            # Factory to choose embedding provider
│   │   ├── schemas.py            # Pydantic schemas for embedding requests/responses
│   │   ├── service.py            # Service to compute similarity / top-k results
│   │   ├── similarity.py         # Cosine similarity calculations
│   │   └── vector_store.py       # Logic to interact with Qdrant / vector DB
│   ├── infra/              # Infrastructure helpers
│   │   ├── chunker.py       # Document splitting/chunking logic
│   │   ├── pdf_loader.py    # PDF loader and parser
│   │   └── db/              # Database interaction
│   │       ├── base.py       # Base DB connection
│   │       ├── models.py     # SQLAlchemy models
│   │       ├── pg.py         # PostgreSQL client
│   │       └── qdrant.py     # Qdrant client and queries
│   ├── llm/               # LLM adapters and tools
│   │   ├── config.py        # Default generation configs
│   │   ├── factory.py       # LLM client factory
│   │   ├── filter.py        # System/forbidden command filtering
│   │   ├── geminiAdapter.py # Adapter for Gemini LLM
│   │   ├── normalizer.py    # Normalizes LLM responses
│   │   ├── openAIAdapter.py # Adapter for OpenAI LLM
│   │   ├── runner.py        # Handles LLM requests with retries, timeout, backoff
│   │   └── schemas.py       # Pydantic schemas for LLM requests/responses
│   ├── main.py             # FastAPI entry point
│   ├── middlewares/        # Custom middlewares
│   │   ├── body.py          # Middleware for reading request body
│   │   └── prometheus.py    # Middleware for Prometheus metrics
│   ├── models/             # Data models
│   │   └── user.py         # User context and DB model
│   ├── schemas/            # Pydantic schemas for requests/responses
│   │   ├── auth.py
│   │   └── chat.py
│   ├── services/           # Application services
│   │   ├── auth_service.py
│   │   ├── chat_service.py # Handles LLM interactions and switching providers
│   │   ├── ingestion.py    # Document ingestion service
│   │   └── rag_service.py  # RAG (retrieval-augmented generation) service
│   └── validators/         # Input validators
│       ├── generation.py   # Validate generation parameters
│       ├── provider.py     # Validate LLM provider
│       └── timeout.py      # Validate timeout values
├── docker-compose.yaml     # Docker Compose config for API, Redis, Vault
├── Dockerfile              # Dockerfile for API container
├── prometheus.yaml         # Prometheus config
├── gemini/                 # Gemini testing scripts
│   └── main.py
├── json_requests/          # Saved JSON responses from LLM
├── openai/                 # OpenAI testing scripts
│   └── main.py
├── README.md               # Project documentation
├── reflection.md           # Notes and reflections from practice
├── requirements.txt        # Python dependencies
└── venv/                   # Virtual environment
```
⸻

### 🐳 Docker Setup & Running
1.	Build and run containers:
```
docker-compose up --build
```
2.	API available at:
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
vault kv put secret/ai-assistant-api \
  JWT_SECRET_KEY="somesecret" \
  OPENAI_API_KEY="somekey" \
  GEMINI_API_KEY="somekey" \
  ALLOWED_PROVIDERS='["openai","gemini"]' \
  FORBIDDEN_COMMANDS='["rm -rf", "shutdown", "docker stop"]' \
  ROOT_USR_PASS="somepass"
```
⸻

### 🔑 Environment Variables (.env)
```
DEFAULT_PROVIDER=gemini
EMBEDDING_PROVIDER=gemini
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
DATABASE_URL=postgresql+asyncpg://rag:rag@rag-postgres:5432/rag
DB_HOST=localhost
DB_USER=rag
DB_PASS=rag
DB_NAME=rag
QDRANT_URL=http://db-qdrant:6333
RATE_LIMIT_USER_REQUESTS=5
RATE_LIMIT_ADMIN_REQUESTS=5
RATE_LIMIT_WINDOW=60
VAULT_ADDR=http://localhost:8200
VAULT_TOKEN=root
DEBUG_MODE=True
```
⸻

### 🗃 Alembic (Database Migrations)
- Alembic manages database migrations (PostgreSQL)
- Migration commands:

1. Create new migration
```
alembic revision --autogenerate -m "migration message"
```
2. Apply migrations
```
alembic upgrade head
```
3. downgrade
```
alembic downgrade -1
```
- Models located in app/infra/db/models.py

⸻

### 💡 Swagger & JWT Authorization
- All endpoints requiring authorization use Security(auth_dependency) → Swagger UI shows Authorize button.
- Rate limiting and forbidden command checks are applied via Depends(rate_limit_dependency) and Depends(security_dependency).

⸻

### 💡 Endpoint Example
```
curl -X POST "http://127.0.0.1:8000/chat" \
-H "accept: application/json" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <JWT_TOKEN>" \
-d '{
  "prompt": "Напишите функцию hello world",
  "provider": "gemini",
  "instruction": "Вы опытный Python разработчик",
  "timeout": 60
}'
```
- Responses returned in normalized JSON format
- Logging tracks retries, forbidden commands, and timeout events

⸻

### 📚 Resources
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference/introduction)
- [Gemini API Documentatio](https://ai.google.dev/gemini-api/docs?hl=en)

⸻

## Русский

Проект ai-assistant-api позволяет взаимодействовать с LLM через API.
Поддерживаемые модели: OpenAI и Gemini.

Возможности проекта:
- Отправка запросов к LLM
- Получение ответов
- Эксперименты с параметрами temperature и top_p
- Контроль таймаутов запросов
- Сохранение ответов в формате JSON для анализа и тестирования
- Переключение между несколькими провайдерами LLM в одном запросе
- Фильтрация системных и запрещённых команд
- Логирование попыток злоумышленников
- Ограничение частоты запросов (rate limit) для пользователей и админов
- Использование embedding для документов, хранение их в Qdrant и поиск по похожести
- Работа с многоязычными текстами и крупными документами через разбиение на чанки
- Поддержка Swagger UI с кнопкой Authorize для токена JWT

⸻

### 📁 Структура проекта
```
ai-assistant-api/
├── alembic/                # Миграции базы данных (PostgreSQL)
│   ├── env.py             # Конфигурация окружения Alembic
│   ├── README             # Заметки / описание Alembic
│   ├── script.py.mako      # Шаблон скрипта Alembic
│   └── versions/           # Файлы миграций
├── alembic.ini             # Конфигурация Alembic
├── app/                    # Основная библиотека приложения
│   ├── api/                # FastAPI эндпоинты
│   │   ├── auth.py         # Эндпоинты авторизации
│   │   ├── chat.py         # Эндпоинты чата
│   │   ├── embeddings.py   # Эндпоинты для embeddings и семантического поиска
│   │   ├── ingestion.py    # Эндпоинт для загрузки документов в векторную БД
│   │   └── search.py       # Эндпоинт для выполнения поисковых запросов
│   ├── core/               # Основные настройки и утилиты
│   │   ├── config.py       # Настройки приложения, интеграция с Vault, переменные окружения
│   │   ├── logging.py      # Настройка логирования
│   │   ├── redis.py        # Клиент Redis для ограничения частоты запросов
│   │   ├── security.py     # Утилиты безопасности, логирование запрещённых запросов
│   │   └── vault.py        # Вспомогательные функции для работы с Vault
│   ├── dependencies/       # Зависимости FastAPI
│   │   ├── auth.py         # Зависимость авторизации
│   │   ├── rate_limit.py   # Зависимость ограничения частоты запросов
│   │   ├── security.py     # Зависимость безопасности/логирования
│   │   ├── user.py         # Контекст пользователя / зависимость текущего пользователя
│   │   └── validation.py   # Валидация входных данных для запросов чата
│   ├── embeddings/         # Клиенты embeddings, сервисы, логика similarity
│   │   ├── clients/
│   │   │   ├── client.py        # Базовый интерфейс клиента embeddings
│   │   │   ├── gemini_client.py # Клиент Gemini
│   │   │   └── openai_client.py # Клиент OpenAI
│   │   ├── factory.py            # Фабрика для выбора провайдера embeddings
│   │   ├── schemas.py            # Pydantic схемы для запросов/ответов embeddings
│   │   ├── service.py            # Сервис для вычисления похожести / top-k результатов
│   │   ├── similarity.py         # Вычисление косинусной похожести
│   │   └── vector_store.py       # Логика взаимодействия с Qdrant / векторной БД
│   ├── infra/              # Вспомогательные инструменты инфраструктуры
│   │   ├── chunker.py       # Разбиение документов на чанки
│   │   ├── pdf_loader.py    # Загрузка и парсинг PDF
│   │   └── db/              # Взаимодействие с базой данных
│   │       ├── base.py       # Базовое подключение к БД
│   │       ├── models.py     # SQLAlchemy модели
│   │       ├── pg.py         # Клиент PostgreSQL
│   │       └── qdrant.py     # Клиент Qdrant и запросы
│   ├── llm/               # Адаптеры и утилиты для LLM
│   │   ├── config.py        # Настройки генерации по умолчанию
│   │   ├── factory.py       # Фабрика клиентов LLM
│   │   ├── filter.py        # Фильтрация системных / запрещённых команд
│   │   ├── geminiAdapter.py # Адаптер для Gemini LLM
│   │   ├── normalizer.py    # Нормализация ответов LLM
│   │   ├── openAIAdapter.py # Адаптер для OpenAI LLM
│   │   ├── runner.py        # Обработка запросов с ретраями, таймаутами и бэкоффом
│   │   └── schemas.py       # Pydantic схемы для запросов/ответов LLM
│   ├── main.py             # Точка входа FastAPI
│   ├── middlewares/        # Пользовательские middleware
│   │   ├── body.py          # Middleware для чтения тела запроса
│   │   └── prometheus.py    # Middleware для метрик Prometheus
│   ├── models/             # Модели данных
│   │   └── user.py         # Модель пользователя и контекст
│   ├── schemas/            # Pydantic схемы для запросов/ответов
│   │   ├── auth.py
│   │   └── chat.py
│   ├── services/           # Сервисы приложения
│   │   ├── auth_service.py
│   │   ├── chat_service.py # Обработка взаимодействия с LLM и переключения провайдеров
│   │   ├── ingestion.py    # Сервис загрузки документов
│   │   └── rag_service.py  # Сервис RAG (retrieval-augmented generation)
│   └── validators/         # Валидаторы входных данных
│       ├── generation.py   # Проверка параметров генерации
│       ├── provider.py     # Проверка провайдера LLM
│       └── timeout.py      # Проверка таймаутов
├── docker-compose.yaml     # Конфигурация Docker Compose для API, Redis, Vault
├── Dockerfile              # Dockerfile для контейнера API
├── prometheus.yaml         # Конфигурация Prometheus
├── gemini/                 # Скрипты для тестирования Gemini
│   └── main.py
├── json_requests/          # Сохранённые JSON-ответы от LLM
├── openai/                 # Скрипты для тестирования OpenAI
│   └── main.py
├── README.md               # Документация проекта
├── reflection.md           # Заметки и выводы после практик
├── requirements.txt        # Зависимости Python
└── venv/                   # Виртуальное окружение
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
vault kv put secret/ai-assistant-api \
  JWT_SECRET_KEY="somesecret" \
  OPENAI_API_KEY="somekey" \
  GEMINI_API_KEY="somekey" \
  ALLOWED_PROVIDERS='["openai","gemini"]' \
  FORBIDDEN_COMMANDS='["rm -rf", "shutdown", "docker stop"]' \
  ROOT_USR_PASS="somepass"
```
⸻

### 🔑 Переменные окружения (.env)
```
DEFAULT_PROVIDER=gemini
EMBEDDING_PROVIDER=gemini
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
DATABASE_URL=postgresql+asyncpg://rag:rag@rag-postgres:5432/rag
DB_HOST=localhost
DB_USER=rag
DB_PASS=rag
DB_NAME=rag
QDRANT_URL=http://db-qdrant:6333
RATE_LIMIT_USER_REQUESTS=5
RATE_LIMIT_ADMIN_REQUESTS=5
RATE_LIMIT_WINDOW=60
VAULT_ADDR=http://localhost:8200
VAULT_TOKEN=root
DEBUG_MODE=True
```
⸻

### 🗃 Alembic (Миграции базы данных)
- Alembic управляет миграциями PostgreSQL
- Команды:

1. Создание новой миграции
```
alembic revision --autogenerate -m "migration message"
```
2. применить миграции
```
alembic upgrade head
```
3. Откат миграции
```
alembic downgrade -1
```

- Модели находятся в app/infra/db/models.py

⸻

### 💡 Пример запроса к эндпоинту
```
curl -X POST "http://127.0.0.1:8000/chat" \
-H "accept: application/json" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <JWT_TOKEN>" \
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