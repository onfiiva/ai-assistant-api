# AI Assistant API

[English](#english) | [Русский](#русский)

- [🐳 Installation](#-docker-setup--running)
- [🐳 Установка](#-настройка-и-запуск-docker)

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
- Swagger UI with JWT authorization support

⸻

### 📁 Project Structure
```
ai-assistant-api/
├── alembic/                # Database migrations (PostgreSQL)
│   ├── env.py             # Alembic environment configuration
│   ├── README             # Alembic notes and description
│   ├── script.py.mako     # Alembic migration script template
│   └── versions/          # Migration files
├── alembic.ini             # Alembic configuration
├── app/                    # Core application library
│   ├── api/                # FastAPI endpoints
│   │   ├── auth.py         # Endpoints for login/register users
│   │   ├── chat.py         # Chat endpoints: /chat/ (LLM) and /chat/rag (RAG)
│   │   ├── embeddings.py   # Endpoints for embeddings search
│   │   ├── ingestion.py    # Endpoint to ingest documents into vector DB
│   │   └── search.py       # GET endpoint for searching stored embeddings
│   ├── container.py        # Application container setup (DI)
│   ├── core/               # Core configuration and utilities
│   │   ├── config.py       # App settings and environment variables
│   │   ├── logging.py      # Logging setup
│   │   ├── redis.py        # Redis client for rate limiting
│   │   ├── security.py     # Security helpers
│   │   ├── timing.py       # Request timing metrics
│   │   ├── tokens.py       # JWT token utils
│   │   └── vault.py        # Vault client helpers
│   ├── dependencies/       # FastAPI dependencies
│   │   ├── auth.py         # Auth dependency
│   │   ├── rate_limit.py   # Rate limiting dependency
│   │   ├── security.py     # Security/logging dependency
│   │   ├── user.py         # Current user context dependency
│   │   └── validation.py   # Validation for chat requests
│   ├── embeddings/         # Embeddings clients and services
│   │   ├── clients/        # Provider clients
│   │   │   ├── client.py        # Base embedding client interface
│   │   │   ├── gemini_client.py # Gemini embedding client
│   │   │   └── openai_client.py # OpenAI embedding client
│   │   ├── factory.py            # Embedding provider factory
│   │   ├── schemas.py            # Pydantic schemas for embeddings
│   │   ├── service.py            # Service for similarity and top-k
│   │   ├── similarity.py         # Cosine similarity calculations
│   │   └── vector_store.py       # Qdrant interaction logic
│   ├── infra/              # Infrastructure utilities
│   │   ├── chunker.py       # Document chunking logic
│   │   ├── pdf_loader.py    # PDF loader and parser
│   │   └── db/              # Database interaction
│   │       ├── base.py       # Base DB connection
│   │       ├── models/       # SQLAlchemy models
│   │       ├── pg.py         # PostgreSQL client
│   │       └── qdrant.py     # Qdrant client
│   ├── llm/               # LLM adapters and utilities
│   │   ├── adapters/
│   │   │   ├── geminiAdapter.py # Gemini LLM adapter
│   │   │   └── openAIAdapter.py # OpenAI LLM adapter
│   │   ├── config.py        # Default generation configs
│   │   ├── factory.py       # LLM client factory
│   │   ├── filter.py        # System/forbidden command filter
│   │   ├── normalizer.py    # Normalize LLM responses
│   │   ├── runner.py        # Handles LLM calls with retry/backoff
│   │   └── schemas.py       # Pydantic schemas for LLM requests/responses
│   ├── main.py             # FastAPI entrypoint
│   ├── middlewares/        # Custom middlewares
│   │   ├── body.py          # Read request body
│   │   ├── observability.py # Metrics collection
│   │   ├── prometheus.py    # Prometheus integration
│   │   ├── timings.py       # Request timing
│   │   └── tokens.py        # Token tracking
│   ├── models/             # Data models
│   │   └── user.py         # User model and context
│   ├── schemas/            # Pydantic schemas for API
│   │   ├── auth.py
│   │   └── chat.py
│   ├── services/           # Application services
│   │   ├── auth_service.py
│   │   ├── chat_service.py # LLM interactions and provider switching
│   │   ├── ingestion.py    # Document ingestion service
│   │   └── rag_service.py  # RAG (retrieval-augmented generation) service
│   └── validators/         # Input validators
│       ├── generation.py
│       ├── provider.py
│       └── timeout.py
├── docker-compose.yaml     # Docker Compose configuration for API, Redis, Vault, Postgres, Qdrant
├── Dockerfile              # Dockerfile for API container
├── gemini/                 # Scripts for testing Gemini API
│   └── main.py
├── json_requests/          # Saved JSON responses from LLM
├── openai/                 # Scripts for testing OpenAI API
│   └── main.py
├── prometheus.yaml         # Prometheus config
├── README.md               # Project documentation
├── reflection.md           # Notes and reflections after practice
└── requirements.txt        # Python dependencies
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
RATE_LIMIT_ADMIN_REQUESTS=10
RATE_LIMIT_WINDOW=60
JWT_SECRET_KEY=root
VAULT_ADDR=http://localhost:8200
VAULT_TOKEN=root
DEBUG_MODE=True
MAX_EMBED_CHUNKS=60
MAX_EMBED_TOKENS=40_000
MAX_CHUNK_TOKENS=512
```

⸻

### 🗃 Alembic (Database Migrations)
- Alembic manages PostgreSQL migrations
- Commands:

1.	Create new migration
```
alembic revision --autogenerate -m "migration message"
```
2.	Apply migrations
```
alembic upgrade head
```
3.	Rollback migration
```
alembic downgrade -1
```
- Models located in app/infra/db/models/

⸻

### 💡 Endpoints

#### /auth
- POST /auth/login — login user and return JWT token
- POST /auth/register — register a new user (admin only) and return JWT token

#### /chat
- POST /chat/ — send prompt to LLM, supports system command filtering, provider selection, and timeout
- POST /chat/rag — RAG-based question answering using embeddings + LLM

#### /embeddings
- POST /embeddings/search — search documents semantically using embeddings, top-k results

#### /ingestion
- POST /ingestion/ingest — ingest PDF documents into vector DB with embedding, tracks ingestion limits

#### /search
- GET /search/ — search pre-ingested embeddings, returns top-k matches

⸻

### 📚 Resources
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference/introduction)
- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs?hl=en)


## Русский

Проект ai-assistant-api позволяет взаимодействовать с LLM (Large Language Models — большие языковые модели) через API.
Поддерживаемые модели: OpenAI и Gemini.

С этим проектом вы можете:
- Отправлять запросы к LLM
- Получать ответы
- Экспериментировать с параметрами, такими как temperature и top_p
- Контролировать таймауты запросов
- Сохранять ответы в формате JSON для анализа и тестирования
- Переключаться между несколькими провайдерами LLM в одном запросе
- Фильтровать системные и запрещённые команды
- Отслеживать и логировать вредоносные запросы
- Применять лимиты запросов для пользователей и администраторов
- Встраивать документы, хранить их в векторной БД (Qdrant) и выполнять семантический поиск
- Работать с мультиязычным контентом и большими документами через разбиение на части (chunking)
- Использовать Swagger UI с поддержкой JWT авторизации

⸻

### 📁 Структура проекта
```
ai-assistant-api/
├── alembic/                # Миграции базы данных (PostgreSQL)
│   ├── env.py             # Конфигурация окружения Alembic
│   ├── README             # Заметки и описание Alembic
│   ├── script.py.mako     # Шаблон скрипта миграции
│   └── versions/          # Файлы миграций
├── alembic.ini             # Конфигурация Alembic
├── app/                    # Основная библиотека приложения
│   ├── api/                # FastAPI эндпоинты
│   │   ├── auth.py         # Эндпоинты для логина/регистрации
│   │   ├── chat.py         # Эндпоинты чата: /chat/ (LLM) и /chat/rag (RAG)
│   │   ├── embeddings.py   # Эндпоинты поиска по эмбеддингам
│   │   ├── ingestion.py    # Эндпоинт для загрузки документов в векторную БД
│   │   └── search.py       # GET эндпоинт для поиска по сохранённым эмбеддингам
│   ├── container.py        # Настройка приложения (DI)
│   ├── core/               # Основные настройки и утилиты
│   │   ├── config.py       # Настройки приложения и переменные окружения
│   │   ├── logging.py      # Настройка логирования
│   │   ├── redis.py        # Клиент Redis для лимитов запросов
│   │   ├── security.py     # Помощники по безопасности
│   │   ├── timing.py       # Метрики времени запросов
│   │   ├── tokens.py       # Утилиты JWT токенов
│   │   └── vault.py        # Клиент Vault
│   ├── dependencies/       # Зависимости FastAPI
│   │   ├── auth.py         # Auth зависимость
│   │   ├── rate_limit.py   # Зависимость лимитов запросов
│   │   ├── security.py     # Зависимость безопасности/логирования
│   │   ├── user.py         # Контекст текущего пользователя
│   │   └── validation.py   # Валидация запросов чата
│   ├── embeddings/         # Клиенты и сервисы эмбеддингов
│   │   ├── clients/        # Клиенты провайдеров
│   │   │   ├── client.py        # Базовый интерфейс клиента эмбеддингов
│   │   │   ├── gemini_client.py # Клиент Gemini
│   │   │   └── openai_client.py # Клиент OpenAI
│   │   ├── factory.py            # Фабрика провайдера эмбеддингов
│   │   ├── schemas.py            # Pydantic схемы для эмбеддингов
│   │   ├── service.py            # Сервис для similarity/top-k
│   │   ├── similarity.py         # Вычисление косинусной близости
│   │   └── vector_store.py       # Логика работы с Qdrant
│   ├── infra/              # Инфраструктурные утилиты
│   │   ├── chunker.py       # Логика разбиения документов
│   │   ├── pdf_loader.py    # Парсер PDF
│   │   └── db/              # Работа с базой данных
│   │       ├── base.py       # Базовое подключение к БД
│   │       ├── models/       # SQLAlchemy модели
│   │       ├── pg.py         # Клиент PostgreSQL
│   │       └── qdrant.py     # Клиент Qdrant
│   ├── llm/               # Адаптеры и утилиты LLM
│   │   ├── adapters/
│   │   │   ├── geminiAdapter.py # Адаптер Gemini
│   │   │   └── openAIAdapter.py # Адаптер OpenAI
│   │   ├── config.py        # Настройки генерации по умолчанию
│   │   ├── factory.py       # Фабрика LLM клиентов
│   │   ├── filter.py        # Фильтр системных/запрещённых команд
│   │   ├── normalizer.py    # Нормализация ответов LLM
│   │   ├── runner.py        # Вызовы LLM с retry/backoff
│   │   └── schemas.py       # Pydantic схемы для запросов/ответов LLM
│   ├── main.py             # Точка входа FastAPI
│   ├── middlewares/        # Пользовательские middlewares
│   │   ├── body.py          # Чтение тела запроса
│   │   ├── observability.py # Сбор метрик
│   │   ├── prometheus.py    # Интеграция с Prometheus
│   │   ├── timings.py       # Время обработки запросов
│   │   └── tokens.py        # Трекинг токенов
│   ├── models/             # Модели данных
│   │   └── user.py         # Модель пользователя
│   ├── schemas/            # Pydantic схемы для API
│   │   ├── auth.py
│   │   └── chat.py
│   ├── services/           # Сервисы приложения
│   │   ├── auth_service.py
│   │   ├── chat_service.py # Взаимодействие с LLM и переключение провайдеров
│   │   ├── ingestion.py    # Сервис загрузки документов
│   │   └── rag_service.py  # RAG (retrieval-augmented generation) сервис
│   └── validators/         # Валидаторы входных данных
│       ├── generation.py
│       ├── provider.py
│       └── timeout.py
├── docker-compose.yaml     # Docker Compose для API, Redis, Vault, Postgres, Qdrant
├── Dockerfile              # Dockerfile для контейнера API
├── gemini/                 # Скрипты для тестирования Gemini API
│   └── main.py
├── json_requests/          # Сохранённые JSON ответы LLM
├── openai/                 # Скрипты для тестирования OpenAI API
│   └── main.py
├── prometheus.yaml         # Конфиг Prometheus
├── README.md               # Документация проекта
├── reflection.md           # Заметки и рефлексии после практики
└── requirements.txt        # Python зависимости
```
⸻

### 🐳 Настройка и запуск Docker
1.	Собрать и запустить контейнеры:
```
docker-compose up --build
```
2.	API доступно по адресу:
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
RATE_LIMIT_ADMIN_REQUESTS=10
RATE_LIMIT_WINDOW=60
JWT_SECRET_KEY=root
VAULT_ADDR=http://localhost:8200
VAULT_TOKEN=root
DEBUG_MODE=True
MAX_EMBED_CHUNKS=60
MAX_EMBED_TOKENS=40_000
MAX_CHUNK_TOKENS=512
```
⸻

### 🗃 Alembic (миграции базы данных)
- Alembic управляет миграциями PostgreSQL
- Команды:

1.	Создать новую миграцию
```
alembic revision --autogenerate -m "migration message"
```
2.	Применить миграции
```
alembic upgrade head
```
3.	Откатить миграцию
```
alembic downgrade -1
```
- Модели находятся в app/infra/db/models/

⸻

### 💡 Эндпоинты

#### /auth
- POST /auth/login — логин пользователя и получение JWT
- POST /auth/register — регистрация нового пользователя (только админ) и получение JWT

#### /chat
- POST /chat/ — отправка запроса к LLM, поддержка фильтрации системных команд, выбор провайдера и таймаут
- POST /chat/rag — RAG-based ответы с использованием эмбеддингов + LLM

#### /embeddings
- POST /embeddings/search — семантический поиск документов, топ-k результатов

#### /ingestion
- POST /ingestion/ingest — загрузка PDF документов в векторную БД с эмбеддингами, контроль лимитов загрузки

#### /search
- GET /search/ — поиск по загруженным эмбеддингам, возвращает топ-k совпадений

⸻

### 📚 Ресурсы
- [Документация OpenAI API](https://platform.openai.com/docs/api-reference/introduction)
- [Документация Gemini API](https://ai.google.dev/gemini-api/docs?hl=ru)