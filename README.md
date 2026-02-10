# AI Assistant API

[English](#english) | [Русский](#русский)

- [🐳 Installation](#-docker-setup--running)
- [🐳 Установка](#-docker-установка-и-запуск)

⸻

## English

The ai-assistant-api project allows interaction with LLMs (Large Language Models) via API.
Supported models: OpenAI and Gemini.

With this project, you can:
- Send requests to LLMs (sync, async and via agent)
- Use RAG (retrieval-augmented generation)
- Experiment with generation parameters (temperature, top_p, max_tokens, etc.)
- Track job status via async inference API
- Control request timeouts
- Save responses in JSON format for analysis and testing
- Switch between multiple LLM providers in the same request
- Filter system/forbidden commands and sanitize user input
- Track and log malicious requests
- Apply rate limiting per user/admin
- Embed documents, store them in a vector database (Qdrant), and perform semantic search
- Work with multi-language content and large documents by chunking
- Swagger UI with JWT authorization support
- Use async inference workers with job queue and heartbeat monitoring

⸻

### 📁 Project Structure
```
ai-assistant-api/
├── alembic/                    # Database migrations for PostgreSQL
│   ├── env.py                  # Alembic environment configuration
│   ├── README                  # Notes and description for migrations
│   ├── script.py.mako          # Template for migration scripts
│   └── versions/               # Folder containing migration files
│       └── <migration_files>   # Python migration scripts
├── alembic.ini                  # Alembic configuration
├── app/                        # Main application package
│   ├── api/                    # FastAPI endpoint definitions
│   │   ├── agents.py           # Endpoints for agent actions, status, and tools
│   │   ├── auth.py             # Endpoints for login/register users
│   │   ├── chat.py             # Synchronous chat endpoints (/chat/, /chat/rag)
│   │   ├── chat_async.py       # Async chat endpoints (/chat/async, /chat/rag/async)
│   │   ├── embeddings.py       # Endpoints for embedding searches
│   │   ├── ingestion.py        # Endpoint to ingest PDFs into vector DB
│   │   ├── search.py           # GET endpoint to search stored embeddings
│   │   └── inference.py        # Endpoints to manage async inference jobs
│   ├── agents/                 # Agent logic and memory management
│   │   ├── actions.py          # Agent action implementations
│   │   ├── schemas.py          # Pydantic schemas for agent input/output
│   │   ├── memory/             # Agent memory backends
│   │   │   ├── base.py         # Base memory class
│   │   │   ├── in_memory.py    # Memory implementation in RAM
│   │   │   ├── redis.py        # Redis synchronous memory
│   │   │   └── redis_async.py  # Redis async memory
│   │   └── tools/              # Agent tool implementations
│   │       ├── actions/        # Tool actions
│   │       │   └── execute.py  # Universal tool executor
│   │       ├── base.py         # Base tool class
│   │       ├── registry.py     # Tool registry
│   │       ├── external_api.py # External API call tool
│   │       ├── summary.py      # Summary tool
│   │       ├── validation.py   # Tool validation schema
│   │       ├── vector_search.py        # Vector search tool
│   │       ├── vector_search_async.py  # Vector search async tool
│   │       └── search.py       # Search tool
│   ├── container.py            # Dependency injection container setup
│   ├── core/                   # Core application configurations and utilities
│   │   ├── config.py           # Application settings and environment variables
│   │   ├── logging.py          # Logging configuration
│   │   ├── redis.py            # Redis client configuration (rate limits, jobs)
│   │   ├── security.py         # Security helpers (password hashing, token checks)
│   │   ├── timing.py           # Request timing utilities
│   │   ├── tokens.py           # JWT token utilities
│   │   └── vault.py            # Vault client helper
│   ├── dependencies/           # FastAPI dependencies for endpoints
│   │   ├── agent_params.py     # Validates agent parameters
│   │   ├── auth.py             # Current user retrieval
│   │   ├── inference.py        # Provides InferenceService instance
│   │   ├── rate_limit.py       # Rate limiting per user/admin
│   │   ├── security.py         # Security middleware dependency
│   │   ├── user.py             # Current user context
│   │   └── validation.py       # Input validation for chat requests
│   ├── embeddings/             # Embeddings management
│   │   ├── clients/            # Provider-specific clients (OpenAI/Gemini)
│   │   │   ├── client.py
│   │   │   ├── openai_client.py
│   │   │   └── gemini_client.py
│   │   ├── factory.py          # Embeddings service factory
│   │   ├── service.py          # Main embeddings service
│   │   ├── similarity.py       # Vector similarity calculation
│   │   ├── vector_store.py     # Vector DB client (Qdrant)
│   │   └── schemas.py          # Pydantic schemas for embeddings
│   ├── inference/              # Async inference logic
│   │   ├── inference_service.py    # Job creation and status management
│   │   ├── inference_repository.py # Redis storage for jobs
│   │   └── workers/            # Background worker scripts
│   │       ├── async_inference_worker.py
│   │       ├── inference_worker.py
│   │       └── worker_main.py  # Entrypoint to run workers
│   ├── infra/                  # Infrastructure utilities
│   │   ├── chunker.py          # Document chunking logic
│   │   ├── pdf_loader.py       # PDF parsing
│   │   └── db/                 # Database interactions
│   │       ├── models/         # SQLAlchemy models
│   │       │   ├── base.py
│   │       │   ├── models.py
│   │       │   └── user_model.py
│   │       ├── pg.py           # PostgreSQL client
│   │       └── qdrant.py       # Qdrant client
│   ├── llm/                     # LLM adapters and utilities
│   │   ├── adapters/           # LLM provider adapters
│   │   │   ├── client.py
│   │   │   ├── openAIAdapter.py
│   │   │   └── geminiAdapter.py
│   │   ├── config.py
│   │   ├── factory.py
│   │   ├── filter.py           # Filters for forbidden commands
│   │   ├── normalizer.py       # Normalize model outputs
│   │   ├── runner.py           # Run LLM requests
│   │   ├── sanitizer.py        # User input sanitization
│   │   └── schemas.py          # Request/response schemas
│   ├── main.py                 # FastAPI entrypoint
│   ├── middlewares/            # Custom middlewares
│   │   ├── body.py
│   │   ├── observability.py
│   │   ├── prometheus.py
│   │   ├── timings.py
│   │   └── tokens.py
│   ├── models/                 # Core data models
│   │   └── user.py
│   ├── schemas/                # Pydantic schemas for API input/output
│   │   ├── agent.py
│   │   ├── auth.py
│   │   ├── chat.py
│   │   └── inference.py
│   ├── services/               # Application services
│   │   ├── auth_service.py
│   │   ├── chat_service.py
│   │   ├── ingestion.py
│   │   ├── rag_service.py
│   │   └── worker_main.py
│   └── validators/             # Input validators
│       ├── agent.py
│       ├── generation.py
│       ├── provider.py
│       └── timeout.py
├── docker-compose.yaml          # Docker Compose configuration
├── Dockerfile                   # Dockerfile for building the service
├── gemini/                      # Scripts to test Gemini API
│   └── main.py
├── openai/                      # Scripts to test OpenAI API
│   └── main.py
├── json_requests/               # Stored JSON requests/responses for testing
├── prometheus.yaml              # Prometheus configuration
├── README.md                    # Project README
├── reflection.md                # Notes and reflections
└── requirements.txt             # Python dependencies
```

⸻

### 🐳 Docker Setup & Running
1.	Build and run containers:
```bash
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
```bash
export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=root
vault kv put secret/ai-assistant-api \
  JWT_SECRET_KEY="somesecret" \
  OPENAI_API_KEY="somekey" \
  GEMINI_API_KEY="somekey" \
  ALLOWED_PROVIDERS='["openai","gemini"]' \
  FORBIDDEN_COMMANDS='["rm -rf", "shutdown", "docker stop"]' \
  ROOT_USR_PASS="somepass" \
  INSTRUCTION_PATTERNS='["ignore previous","follow these steps","you must","act as","pretend you are","roleplay","system prompt","developer message","internal instructions"]' \
  EXFILTRATION_PATTERNS='["what are your instructions","show system prompt","reveal context","print everything you know","dump input","debug output"]' \
  FORBIDDEN_LLM_OUTPUT='["as a system","internal instructions","developer message"]' \
  INSTRUCTION_REGEX='["\\byou must\\b","\\byou should\\b","\\byou are\\b","\\bact as\\b","\\bpretend you are\\b","\\bfollow these\\b","\\bignore\\b.+\\b(instruction|rule|above|previous)\\b"]' \
  ROLE_OVERRIDE_REGEX='["\\bas a system\\b","\\bas an ai\\b","\\bas chatgpt\\b","\\bas gemini\\b","\\byour role is\\b","\\byou are no longer\\b","\\bdeveloper mode\\b","\\bdan\\b"]' \
  META_SYSTEM_REGEX='["\\bsystem prompt\\b","\\binternal instructions\\b","\\bdeveloper message\\b","\\bhidden rules\\b","\\bwhat are your instructions\\b","\\bshow.*prompt\\b"]' \
  MAX_PROMPT_LENGTH=2048 \
  MAX_RESPONSE_LENGTH=2048
```

⸻

### 🔑 Environment Variables (.env)
```env
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
MAX_EMBED_TOKENS=40000
MAX_CHUNK_TOKENS=512
```

⸻

### 💡 Endpoints

/auth
- POST /auth/login — login user and return JWT token
- POST /auth/register — register a new user (admin only) and return JWT token

/chat
- POST /chat/ — sync LLM call
- POST /chat/rag — sync RAG call
- POST /chat/async — async LLM call, returns job_id
- POST /chat/rag/async — async RAG call, returns job_id

/agents
- POST /agents/run — run an agent with a goal, returns job_id
- GET /agents/{job_id} — get agent job status and step history
- GET /agents/tools — list available tools for the agent

/embeddings
- POST /embeddings/search — semantic search, returns top-k results

/ingestion
- POST /ingestion/ingest — ingest PDF documents into vector DB with embeddings

/search
- GET /search/ — search pre-ingested embeddings, returns top-k matches

/inference
- POST /inference/ — create async inference job
- GET /inference/{job_id} — get status and result/error of async job

⸻

### ⚙️ Async Inference Worker

#### Purpose
Handles asynchronous execution of LLM requests. Users do not need to wait for LLM to finish in real-time — they can fetch results later using a job_id.

#### Workflow
1.	Job creation: user sends a request to /chat/async or /chat/rag/async
2.	Job queue: jobs enter a Redis-backed queue respecting rate limits and LLM load
3.	Workers: run as separate processes/containers and process jobs:
- Send request to LLM (OpenAI/Gemini)
- Normalize, filter, and log responses
- Save result/error back to Redis
4.	Heartbeat: workers send periodic heartbeat signals
5.	Fetching results: GET /inference/{job_id} returns:
- status: pending, completed, error
- result (if ready)
- error message (if any)

#### Usage
- Run a worker:
```bash
python -m app.inference.workers.worker_main
```
- Multiple workers can run simultaneously
- Load is balanced via job queue
- Works with rate-limiting to prevent overloading LLM

#### Related Endpoints
- POST /chat/async — create async LLM job
- POST /chat/rag/async — create async RAG job
- GET /inference/{job_id} — fetch job result/status

⸻

### 📚 Resources
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference/introduction)
- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs?hl=en)


## Русский

Проект ai-assistant-api позволяет взаимодействовать с LLM (Large Language Models — большие языковые модели) через API.
Поддерживаемые модели: OpenAI и Gemini.

С помощью этого проекта вы можете:
- Отправлять запросы к LLM (синхронно, асинхронно и через агента)
- Использовать RAG (retrieval-augmented generation — генерацию с использованием поиска)
- Экспериментировать с параметрами генерации (temperature, top_p, max_tokens и др.)
- Отслеживать статус заданий через асинхронный API инференса
- Управлять таймаутами запросов
- Сохранять ответы в формате JSON для анализа и тестирования
- Использовать несколько LLM-провайдеров в одном запросе
- Фильтровать системные/запрещённые команды и очищать пользовательский ввод
- Отслеживать и логировать вредоносные запросы
- Применять лимиты запросов на пользователя/администратора
- Встраивать документы, хранить их в векторной БД (Qdrant) и выполнять семантический поиск
- Работать с многоязычным контентом и большими документами, разбивая их на чанки
- Использовать Swagger UI с поддержкой авторизации через JWT
- Применять асинхронные воркеры инференса с очередью заданий и мониторингом heartbeat

⸻

### 📁 Структура проекта
```
ai-assistant-api/
├── alembic/                    # Миграции базы данных PostgreSQL
│   ├── env.py                  # Конфигурация окружения Alembic
│   ├── README                  # Заметки и описание миграций
│   ├── script.py.mako          # Шаблон скрипта миграции
│   └── versions/               # Папка с файлами миграций
│       └── <migration_files>   # Python-скрипты миграций
├── alembic.ini                  # Конфигурация Alembic
├── app/                        # Основной пакет приложения
│   ├── api/                    # Определения FastAPI эндпоинтов
│   │   ├── agents.py           # Эндпоинты для действий агента, статуса и инструментов
│   │   ├── auth.py             # Эндпоинты для логина/регистрации пользователей
│   │   ├── chat.py             # Синхронные чат-эндпоинты (/chat/, /chat/rag)
│   │   ├── chat_async.py       # Асинхронные чат-эндпоинты (/chat/async, /chat/rag/async)
│   │   ├── embeddings.py       # Эндпоинты для поиска по эмбеддингам
│   │   ├── ingestion.py        # Эндпоинт для загрузки PDF в векторную БД
│   │   ├── search.py           # GET-эндпоинт для поиска по загруженным эмбеддингам
│   │   └── inference.py        # Эндпоинты управления асинхронными заданиями инференса
│   ├── agents/                 # Логика агента и управление памятью
│   │   ├── actions.py          # Реализация действий агента
│   │   ├── schemas.py          # Pydantic схемы ввода/вывода агента
│   │   ├── memory/             # Бэкенды памяти агента
│   │   │   ├── base.py         # Базовый класс памяти
│   │   │   ├── in_memory.py    # Память в RAM
│   │   │   ├── redis.py        # Синхронная память Redis
│   │   │   └── redis_async.py  # Асинхронная память Redis
│   │   └── tools/              # Реализация инструментов агента
│   │       ├── actions/        # Выполнение инструментов
│   │       │   └── execute.py  # Универсальный вызов инструментов
│   │       ├── base.py         # Базовый класс инструмента
│   │       ├── registry.py     # Реестр инструментов
│   │       ├── external_api.py # Инструмент вызова внешней API
│   │       ├── summary.py      # Инструмент summary
│   │       ├── validation.py   # Схема валидации инструментов
│   │       ├── vector_search.py        # Инструмент векторного поиска
│   │       ├── vector_search_async.py  # Асинхронный инструмент векторного поиска
│   │       └── search.py       # Инструмент поиска
│   ├── container.py            # Настройка DI-контейнера
│   ├── core/                   # Основные настройки и утилиты приложения
│   │   ├── config.py           # Настройки приложения и переменные окружения
│   │   ├── logging.py          # Настройка логирования
│   │   ├── redis.py            # Конфигурация Redis (лимиты, задания)
│   │   ├── security.py         # Секьюрити-хелперы (хеширование паролей, проверка токенов)
│   │   ├── timing.py           # Утилиты для замера времени запросов
│   │   ├── tokens.py           # Работа с JWT токенами
│   │   └── vault.py            # Хелпер для Vault
│   ├── dependencies/           # FastAPI зависимости для эндпоинтов
│   │   ├── agent_params.py     # Валидация параметров агента
│   │   ├── auth.py             # Получение текущего пользователя
│   │   ├── inference.py        # Предоставляет экземпляр InferenceService
│   │   ├── rate_limit.py       # Лимиты запросов на пользователя/администратора
│   │   ├── security.py         # Зависимость для секьюрити middleware
│   │   ├── user.py             # Контекст текущего пользователя
│   │   └── validation.py       # Валидация входных данных чата
│   ├── embeddings/             # Управление эмбеддингами
│   │   ├── clients/            # Клиенты для провайдеров (OpenAI/Gemini)
│   │   │   ├── client.py
│   │   │   ├── openai_client.py
│   │   │   └── gemini_client.py
│   │   ├── factory.py          # Фабрика сервиса эмбеддингов
│   │   ├── service.py          # Основной сервис эмбеддингов
│   │   ├── similarity.py       # Вычисление векторной схожести
│   │   ├── vector_store.py     # Клиент векторной БД (Qdrant)
│   │   └── schemas.py          # Pydantic схемы для эмбеддингов
│   ├── inference/              # Асинхронная логика инференса
│   │   ├── inference_service.py    # Создание заданий и управление статусом
│   │   ├── inference_repository.py # Хранение заданий в Redis
│   │   └── workers/            # Скрипты фоновых воркеров
│   │       ├── async_inference_worker.py
│   │       ├── inference_worker.py
│   │       └── worker_main.py  # Точка запуска воркеров
│   ├── infra/                  # Инфраструктурные утилиты
│   │   ├── chunker.py          # Разбиение документов на чанки
│   │   ├── pdf_loader.py       # Парсинг PDF
│   │   └── db/                 # Работа с базой данных
│   │       ├── models/         # SQLAlchemy модели
│   │       │   ├── base.py
│   │       │   ├── models.py
│   │       │   └── user_model.py
│   │       ├── pg.py           # PostgreSQL клиент
│   │       └── qdrant.py       # Qdrant клиент
│   ├── llm/                     # Адаптеры LLM и утилиты
│   │   ├── adapters/           # Адаптеры провайдеров LLM
│   │   │   ├── client.py
│   │   │   ├── openAIAdapter.py
│   │   │   └── geminiAdapter.py
│   │   ├── config.py
│   │   ├── factory.py
│   │   ├── filter.py           # Фильтры запрещённых команд
│   │   ├── normalizer.py       # Нормализация ответов модели
│   │   ├── runner.py           # Выполнение запросов к LLM
│   │   ├── sanitizer.py        # Очистка пользовательского ввода
│   │   └── schemas.py          # Схемы запросов/ответов
│   ├── main.py                 # Точка входа FastAPI
│   ├── middlewares/            # Пользовательские middleware
│   │   ├── body.py
│   │   ├── observability.py
│   │   ├── prometheus.py
│   │   ├── timings.py
│   │   └── tokens.py
│   ├── models/                 # Основные модели данных
│   │   └── user.py
│   ├── schemas/                # Pydantic схемы API
│   │   ├── agent.py
│   │   ├── auth.py
│   │   ├── chat.py
│   │   └── inference.py
│   ├── services/               # Сервисы приложения
│   │   ├── auth_service.py
│   │   ├── chat_service.py
│   │   ├── ingestion.py
│   │   ├── rag_service.py
│   │   └── worker_main.py
│   └── validators/             # Валидаторы входных данных
│       ├── agent.py
│       ├── generation.py
│       ├── provider.py
│       └── timeout.py
├── docker-compose.yaml          # Конфигурация Docker Compose
├── Dockerfile                   # Dockerfile для сборки сервиса
├── gemini/                      # Скрипты для тестирования Gemini API
│   └── main.py
├── openai/                      # Скрипты для тестирования OpenAI API
│   └── main.py
├── json_requests/               # Сохранённые JSON-запросы/ответы для тестирования
├── prometheus.yaml              # Конфигурация Prometheus
├── README.md                    # README проекта
├── reflection.md                # Заметки и размышления
└── requirements.txt             # Python-зависимости
```
⸻

### 🐳 Docker: установка и запуск
1.	Сборка и запуск контейнеров:
```bash
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
```bash
export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=root
vault kv put secret/ai-assistant-api \
  JWT_SECRET_KEY="somesecret" \
  OPENAI_API_KEY="somekey" \
  GEMINI_API_KEY="somekey" \
  ALLOWED_PROVIDERS='["openai","gemini"]' \
  FORBIDDEN_COMMANDS='["rm -rf", "shutdown", "docker stop"]' \
  ROOT_USR_PASS="somepass" \
  INSTRUCTION_PATTERNS='["ignore previous","follow these steps","you must","act as","pretend you are","roleplay","system prompt","developer message","internal instructions"]' \
  EXFILTRATION_PATTERNS='["what are your instructions","show system prompt","reveal context","print everything you know","dump input","debug output"]' \
  FORBIDDEN_LLM_OUTPUT='["as a system","internal instructions","developer message"]' \
  INSTRUCTION_REGEX='["\\byou must\\b","\\byou should\\b","\\byou are\\b","\\bact as\\b","\\bpretend you are\\b","\\bfollow these\\b","\\bignore\\b.+\\b(instruction|rule|above|previous)\\b"]' \
  ROLE_OVERRIDE_REGEX='["\\bas a system\\b","\\bas an ai\\b","\\bas chatgpt\\b","\\bas gemini\\b","\\byour role is\\b","\\byou are no longer\\b","\\bdeveloper mode\\b","\\bdan\\b"]' \
  META_SYSTEM_REGEX='["\\bsystem prompt\\b","\\binternal instructions\\b","\\bdeveloper message\\b","\\bhidden rules\\b","\\bwhat are your instructions\\b","\\bshow.*prompt\\b"]' \
  MAX_PROMPT_LENGTH=2048 \
  MAX_RESPONSE_LENGTH=2048
```
⸻

### 🔑 Переменные окружения (.env)
```env
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
MAX_EMBED_TOKENS=40000
MAX_CHUNK_TOKENS=512
```
⸻

### 💡 Эндпоинты

#### /auth
- POST /auth/login — логин пользователя и выдача JWT
- POST /auth/register — регистрация нового пользователя (только для админа) и выдача JWT

#### /chat
- POST /chat/ — синхронный вызов LLM
- POST /chat/rag — синхронный вызов RAG
- POST /chat/async — асинхронный вызов LLM, возвращает job_id
- POST /chat/rag/async — асинхронный вызов RAG, возвращает job_id

#### /agents
- POST /agents/run — запуск агента с целью, возвращает job_id
- GET /agents/{job_id} — получение статуса задания агента и истории шагов
- GET /agents/tools — список доступных инструментов для агента

#### /embeddings
- POST /embeddings/search — семантический поиск, возвращает top-k результатов

#### /ingestion
- POST /ingestion/ingest — загрузка PDF-документов в векторную БД с эмбеддингами

#### /search
- GET /search/ — поиск по загруженным эмбеддингам, возвращает top-k совпадений

#### /inference
- POST /inference/ — создание асинхронного задания инференса
- GET /inference/{job_id} — получение статуса и результата/ошибки асинхронного задания

⸻

### ⚙️ Асинхронный воркер инференса

#### Назначение:
Обработка асинхронных запросов к LLM. Пользователю не нужно ждать завершения LLM в реальном времени — результат можно получить позже по job_id.

#### Workflow
1.	Создание задания: пользователь отправляет запрос в /chat/async или /chat/rag/async
2.	Очередь заданий: задания поступают в очередь на Redis с учётом лимитов и нагрузки на LLM
3.	Воркеры: запускаются как отдельные процессы/контейнеры и обрабатывают задания:

- Отправляют запрос к LLM (OpenAI/Gemini)
- Нормализуют, фильтруют и логируют ответы
- Сохраняют результат/ошибку обратно в Redis

4.	Heartbeat: воркеры отправляют периодические сигналы heartbeat
5.	Получение результатов: GET /inference/{job_id} возвращает:

- status: pending, completed, error
- result (если готово)
- error message (если есть)

#### Использование
- Запуск воркера:
```bash
python -m app.inference.workers.worker_main
```
- Можно запускать несколько воркеров одновременно
- Балансировка нагрузки через очередь заданий
- Поддержка rate-limiting для предотвращения перегрузки LLM

#### Связанные эндпоинты
- POST /chat/async — создание асинхронного задания LLM
- POST /chat/rag/async — создание асинхронного задания RAG
- GET /inference/{job_id} — получение результата/статуса задания

⸻

#### 📚 Ресурсы
- [Документация OpenAI API](https://platform.openai.com/docs/api-reference/introduction)
- [Документация Gemini API](https://ai.google.dev/gemini-api/docs?hl=ru)