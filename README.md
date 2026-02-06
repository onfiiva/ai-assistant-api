# AI Assistant API

[English](#english) | [Русский](#русский)

- [🐳 Installation](#-docker-setup--running)
- [🐳 Установка](#-настройка-docker-и-запуск)

⸻

## English

The ai-assistant-api project allows interaction with LLMs (Large Language Models) via API.
Supported models: OpenAI and Gemini.

With this project, you can:
- Send requests to LLMs (sync and async)
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
├── alembic/                    # Database migrations (PostgreSQL)
│   ├── env.py                  # Alembic environment configuration
│   ├── README                  # Notes and description
│   ├── script.py.mako          # Alembic migration script template
│   └── versions/               # Migration files
├── alembic.ini                  # Alembic configuration
├── app/                        # Core application library
│   ├── api/                    # FastAPI endpoints
│   │   ├── auth.py             # Endpoints for login/register users
│   │   ├── chat.py             # Sync chat endpoints: /chat/ and /chat/rag
│   │   ├── chat_async.py       # Async chat endpoints: /chat/async and /chat/rag/async
│   │   ├── embeddings.py       # Endpoints for embeddings search
│   │   ├── ingestion.py        # Endpoint to ingest documents into vector DB
│   │   ├── search.py           # GET endpoint for searching stored embeddings
│   │   └── inference.py        # Endpoints for async inference jobs
│   ├── container.py            # Application container setup (DI)
│   ├── core/                   # Core configuration and utilities
│   │   ├── config.py           # App settings and environment variables
│   │   ├── logging.py          # Logging setup
│   │   ├── redis.py            # Redis client for rate limiting
│   │   ├── security.py         # Security helpers
│   │   ├── timing.py           # Request timing metrics
│   │   ├── tokens.py           # JWT token utils
│   │   └── vault.py            # Vault client helpers
│   ├── dependencies/           # FastAPI dependencies
│   │   ├── auth.py             # Auth dependency
│   │   ├── rate_limit.py       # Rate limiting dependency
│   │   ├── security.py         # Security/logging dependency
│   │   ├── user.py             # Current user context dependency
│   │   ├── validation.py       # Chat request validation
│   │   └── inference.py        # Inference service dependency
│   ├── embeddings/             # Embeddings clients and services
│   │   ├── clients/            # Provider clients
│   │   │   ├── client.py
│   │   │   ├── gemini_client.py
│   │   │   └── openai_client.py
│   │   ├── factory.py
│   │   ├── schemas.py
│   │   ├── service.py
│   │   ├── similarity.py
│   │   └── vector_store.py
│   ├── inference/              # Async inference logic
│   │   ├── inference_service.py # Job creation, status tracking
│   │   ├── inference_repository.py # Redis job storage
│   │   └── workers/            # Background worker scripts
│   │       ├── async_inference_worker.py
│   │       ├── inference_worker.py
│   │       └── worker_main.py
│   ├── infra/                  # Infrastructure utilities
│   │   ├── chunker.py          # Document chunking logic
│   │   ├── pdf_loader.py       # PDF parser
│   │   └── db/                 # Database interaction
│   │       ├── models/         # SQLAlchemy models
│   │       ├── pg.py           # PostgreSQL client
│   │       └── qdrant.py       # Qdrant client
│   ├── llm/                     # LLM adapters and utilities
│   │   ├── adapters/           # LLM provider adapters
│   │   │   ├── client.py
│   │   │   ├── geminiAdapter.py
│   │   │   └── openAIAdapter.py
│   │   ├── config.py
│   │   ├── factory.py
│   │   ├── filter.py
│   │   ├── normalizer.py
│   │   ├── runner.py
│   │   ├── sanitizer.py        # Sanitizes user prompts
│   │   └── schemas.py
│   ├── main.py                 # FastAPI entrypoint
│   ├── middlewares/            # Custom middlewares
│   │   ├── body.py
│   │   ├── observability.py
│   │   ├── prometheus.py
│   │   ├── timings.py
│   │   └── tokens.py
│   ├── models/                 # Data models
│   │   └── user.py
│   ├── schemas/                # Pydantic schemas
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
│       ├── generation.py
│       ├── provider.py
│       └── timeout.py
├── docker-compose.yaml
├── Dockerfile
├── gemini/
│   └── main.py                 # Scripts to test Gemini API
├── openai/
│   └── main.py                 # Scripts to test OpenAI API
├── json_requests/              # Saved JSON responses from LLM
├── prometheus.yaml
├── README.md
├── reflection.md
└── requirements.txt
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
  ROOT_USR_PASS="somepass"
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

#### /auth
- POST /auth/login — login user and return JWT token
- POST /auth/register — register a new user (admin only) and return JWT token

#### /chat
- POST /chat/ — sync LLM call
- POST /chat/rag — sync RAG call
- POST /chat/async — async LLM call, returns job_id
- POST /chat/rag/async — async RAG call, returns job_id

#### /embeddings
- POST /embeddings/search — semantic search, returns top-k results

#### /ingestion
- POST /ingestion/ingest — ingest PDF documents into vector DB with embedding, tracks ingestion limits

#### /search
- GET /search/ — search pre-ingested embeddings, returns top-k matches

#### /inference
- POST /inference/ — create async inference job
- GET /inference/{job_id} — get status and result/error of async job

⸻

### ⚙️ Async Inference Worker

#### Purpose:
The Async Inference Worker handles asynchronous execution of LLM requests. Users do not need to wait for the LLM to finish in real time — they can fetch results later using a job_id.

#### How it works under the hood:
1.	Job creation:
- User sends a request to /chat/async or /chat/rag/async.
- The service creates a job object with a unique job_id and saves it in Redis.
2.	Job queue:
- New jobs enter a queue.
- The queue manages order and execution rate, respecting rate limits and LLM load.
3.	Workers:
- Workers run as separate processes or containers.
- Each worker periodically checks the queue for new jobs.
- When a worker picks up a job, it:
	1.	Sends the request to the selected LLM (OpenAI/Gemini).
	2.	Processes the response (normalization, filtering, logging).
	3.	Saves the result or error back to Redis.
4.	Heartbeat and monitoring:
- Workers send periodic heartbeats to indicate they are alive.
- If a worker crashes, pending jobs stay in the queue and can be picked up by another worker.
5.	Fetching results:
- User calls GET /inference/{job_id}.
- The service returns:
- Status: pending, completed, error
- Result (if ready)
- Error message (if any)

#### 🔧 Usage
- Run a worker:
```bash
python -m app.inference.workers.worker_main
```
- Multiple workers can run simultaneously for horizontal scaling.
- Workers automatically balance load via the job queue.
- Works together with rate-limiting to prevent overloading LLM.

#### Related endpoints:
- POST /chat/async — create async LLM job
- POST /chat/rag/async — create async RAG job
- GET /inference/{job_id} — fetch job result/status

⸻

#### 📚 Resources
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference/introduction)
- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs?hl=en)

⸻

## Русский

Проект ai-assistant-api позволяет взаимодействовать с LLM (Large Language Models, большие языковые модели) через API.
Поддерживаемые модели: OpenAI и Gemini.

С этим проектом вы можете:
- Отправлять запросы к LLM (синхронные и асинхронные)
- Использовать RAG (retrieval-augmented generation, генерацию с использованием поиска)
- Экспериментировать с параметрами генерации (temperature, top_p, max_tokens и др.)
- Отслеживать статус задач через API асинхронного инференса
- Управлять таймаутами запросов
- Сохранять ответы в формате JSON для анализа и тестирования
- Переключаться между несколькими провайдерами LLM в одном запросе
- Фильтровать системные/запрещенные команды и очищать пользовательский ввод
- Отслеживать и логировать вредоносные запросы
- Применять лимитирование запросов на пользователя/администратора
- Встраивать документы, хранить их в векторной базе (Qdrant) и выполнять семантический поиск
- Работать с мультиязычным контентом и большими документами с разбиением на чанки
- Использовать Swagger UI с поддержкой JWT авторизации
- Использовать асинхронные воркеры инференса с очередью задач и мониторингом heartbeat

⸻

### 📁 Структура проекта
```
ai-assistant-api/
├── alembic/                    # Миграции базы данных (PostgreSQL)
│   ├── env.py                  # Конфигурация окружения Alembic
│   ├── README                  # Примечания и описание
│   ├── script.py.mako          # Шаблон скрипта миграции Alembic
│   └── versions/               # Файлы миграций
├── alembic.ini                  # Конфигурация Alembic
├── app/                        # Основная библиотека приложения
│   ├── api/                    # Эндпоинты FastAPI
│   │   ├── auth.py             # Эндпоинты логина/регистрации пользователей
│   │   ├── chat.py             # Синхронные чат-эндпоинты: /chat/ и /chat/rag
│   │   ├── chat_async.py       # Асинхронные чат-эндпоинты: /chat/async и /chat/rag/async
│   │   ├── embeddings.py       # Эндпоинты поиска по embeddings
│   │   ├── ingestion.py        # Эндпоинт для загрузки документов в векторную БД
│   │   ├── search.py           # GET эндпоинт поиска по загруженным embeddings
│   │   └── inference.py        # Эндпоинты для асинхронных задач инференса
│   ├── container.py            # Настройка контейнера приложения (DI)
│   ├── core/                   # Основные настройки и утилиты
│   │   ├── config.py           # Настройки приложения и переменные окружения
│   │   ├── logging.py          # Настройка логирования
│   │   ├── redis.py            # Клиент Redis для лимитирования
│   │   ├── security.py         # Помощники для безопасности
│   │   ├── timing.py           # Метрики времени запросов
│   │   ├── tokens.py           # JWT утилиты
│   │   └── vault.py            # Клиент Vault
│   ├── dependencies/           # Зависимости FastAPI
│   │   ├── auth.py             # Зависимость авторизации
│   │   ├── rate_limit.py       # Зависимость лимитирования
│   │   ├── security.py         # Зависимость безопасности/логирования
│   │   ├── user.py             # Контекст текущего пользователя
│   │   ├── validation.py       # Валидация запросов чата
│   │   └── inference.py        # Зависимость сервиса инференса
│   ├── embeddings/             # Клиенты и сервисы embeddings
│   │   ├── clients/            # Клиенты провайдеров
│   │   │   ├── client.py
│   │   │   ├── gemini_client.py
│   │   │   └── openai_client.py
│   │   ├── factory.py
│   │   ├── schemas.py
│   │   ├── service.py
│   │   ├── similarity.py
│   │   └── vector_store.py
│   ├── inference/              # Логика асинхронного инференса
│   │   ├── inference_service.py # Создание задач, отслеживание статуса
│   │   ├── inference_repository.py # Хранение задач в Redis
│   │   └── workers/            # Скрипты фоновых воркеров
│   │       ├── async_inference_worker.py
│   │       ├── inference_worker.py
│   │       └── worker_main.py
│   ├── infra/                  # Инфраструктурные утилиты
│   │   ├── chunker.py          # Логика разбиения документов
│   │   ├── pdf_loader.py       # Парсер PDF
│   │   └── db/                 # Взаимодействие с базой данных
│   │       ├── models/         # Модели SQLAlchemy
│   │       ├── pg.py           # Клиент PostgreSQL
│   │       └── qdrant.py       # Клиент Qdrant
│   ├── llm/                     # Адаптеры LLM и утилиты
│   │   ├── adapters/           # Адаптеры провайдеров
│   │   │   ├── client.py
│   │   │   ├── geminiAdapter.py
│   │   │   └── openAIAdapter.py
│   │   ├── config.py
│   │   ├── factory.py
│   │   ├── filter.py
│   │   ├── normalizer.py
│   │   ├── runner.py
│   │   ├── sanitizer.py        # Очистка пользовательских запросов
│   │   └── schemas.py
│   ├── main.py                 # Точка входа FastAPI
│   ├── middlewares/            # Кастомные middlewares
│   │   ├── body.py
│   │   ├── observability.py
│   │   ├── prometheus.py
│   │   ├── timings.py
│   │   └── tokens.py
│   ├── models/                 # Модели данных
│   │   └── user.py
│   ├── schemas/                # Pydantic схемы
│   │   ├── auth.py
│   │   ├── chat.py
│   │   └── inference.py
│   ├── services/               # Сервисы приложения
│   │   ├── auth_service.py
│   │   ├── chat_service.py
│   │   ├── ingestion.py
│   │   ├── rag_service.py
│   │   └── worker_main.py
│   └── validators/             # Валидаторы ввода
│       ├── generation.py
│       ├── provider.py
│       └── timeout.py
├── docker-compose.yaml
├── Dockerfile
├── gemini/
│   └── main.py                 # Скрипты для теста Gemini API
├── openai/
│   └── main.py                 # Скрипты для теста OpenAI API
├── json_requests/              # Сохраненные JSON ответы от LLM
├── prometheus.yaml
├── README.md
├── reflection.md
└── requirements.txt
```
⸻

### 🐳 Настройка Docker и запуск
1.	Собрать и запустить контейнеры:
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
  ROOT_USR_PASS="somepass"
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
- POST /auth/login — вход пользователя и возврат JWT токена
- POST /auth/register — регистрация нового пользователя (только админ) и возврат JWT токена

#### /chat
- POST /chat/ — синхронный вызов LLM
- POST /chat/rag — синхронный вызов RAG
- POST /chat/async — асинхронный вызов LLM, возвращает job_id
- POST /chat/rag/async — асинхронный вызов RAG, возвращает job_id

#### /embeddings
- POST /embeddings/search — семантический поиск, возвращает top-k результатов

#### /ingestion
- POST /ingestion/ingest — загрузка PDF документов в векторную БД с embedding, отслеживает лимиты

#### /search
- GET /search/ — поиск по загруженным embeddings, возвращает top-k совпадений

#### /inference
- POST /inference/ — создание асинхронной задачи инференса
- GET /inference/{job_id} — получение статуса и результата/ошибки асинхронной задачи

⸻

### ⚙️ Асинхронный воркер

#### Назначение:
Асинхронный воркер отвечает за выполнение запросов к LLM в фоне. Пользователи могут не ждать ответа модели в реальном времени, а получать результат позже по job_id.

#### Как это работает «под капотом»:
1.	Создание задания:
- Пользователь отправляет запрос на /chat/async или /chat/rag/async.
- Сервис создаёт объект задания с уникальным job_id и сохраняет его в Redis.
2.	Очередь заданий:
- Все новые задания попадают в очередь.
- Очередь управляет порядком и скоростью выполнения, соблюдая rate-limit и нагрузку на LLM.
3.	Воркеры:
- Воркеры запускаются как отдельные процессы или контейнеры.
- Каждый воркер периодически проверяет очередь на новые задания.
- Когда воркер берёт задание, он:
	1.	Отправляет запрос к выбранной LLM (OpenAI/Gemini).
	2.	Обрабатывает ответ (нормализация, фильтрация, логирование).
	3.	Сохраняет результат или ошибку обратно в Redis.
4.	Heartbeat и мониторинг:
- Воркеры регулярно отправляют heartbeat, чтобы сервис знал, что они живы.
- Если воркер падает, задания остаются в очереди и могут быть выполнены другим воркером.
5.	Получение результата пользователем:
- Пользователь делает GET /inference/{job_id}.
- Сервис возвращает:
- Статус: pending, completed, error
- Результат (если готов)
- Сообщение об ошибке (если есть)

🔧 Использование
- Запуск воркера:
```bash
python -m app.inference.workers.worker_main
```
- Можно запускать несколько воркеров для масштабирования.
- Воркеры балансируют нагрузку через очередь заданий.
- Работает вместе с rate-limiter для предотвращения перегрузки LLM.

#### Связанные эндпоинты:
- POST /chat/async — создать async LLM-задание
- POST /chat/rag/async — создать async RAG-задание
- GET /inference/{job_id} — получить статус/результат задания

### 📚 Ресурсы
- [Документация OpenAI API](https://platform.openai.com/docs/api-reference/introduction)
- [Документация Gemini API](https://ai.google.dev/gemini-api/docs?hl=ru)