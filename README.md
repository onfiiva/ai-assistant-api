# AI Assistant API

[English](#english) | [Русский](#русский)

- [🐳 Installation](#-docker-setup--running)
- [🐳 Установка](#-docker-установка-и-запуск)

⸻

## English

The ai-assistant-api project allows interaction with LLMs (Large Language Models) via API.
Supported models:
- [OpenAI](https://openai.com)
- [Gemini](https://gemini.google.com)
- [Ollama](https://ollama.com) (used: [mistral:7b-instruct-q4_K_M](https://ollama.com/library/mistral:7b-instruct-q4_K_M))
- [Qwen3](https://qwen.ai/) (used: [Qwen3-4B-VL-Instruct](https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct))

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
- Simple LoRa

⸻

### 📁 Project Structure
```bash
ai-assistant-api/
├── docker-compose.yaml                   # Docker Compose configuration to run all project services
├── models                                # Directory for storing machine learning models
│   └── qwen3-vl-4b-instruct              # Specific model Qwen3-VL-4B
│       ├── chat_template.json            # Chat templates for the model
│       ├── config.json                   # Main model configuration
│       ├── generation_config.json        # Text/video generation settings
│       ├── merges.txt                    # Token merges file (for tokenizer)
│       ├── model-00001-of-00002.safetensors # Model weights (part 1)
│       ├── model-00002-of-00002.safetensors # Model weights (part 2)
│       ├── model.safetensors.index.json  # Model weights index
│       ├── preprocessor_config.json      # Data preprocessor configuration
│       ├── README.md                     # Model documentation
│       ├── tokenizer_config.json         # Tokenizer configuration
│       ├── tokenizer.json                # Model tokenizer
│       ├── video_preprocessor_config.json # Video preprocessor configuration
│       └── vocab.json                    # Model vocabulary
├── README.md                             # General project documentation
└── services                              # Project services directory
    ├── api                               # API service (FastAPI)
    │   ├── alembic                       # Database migration configuration via Alembic
    │   │   ├── env.py                    # Main Alembic environment script
    │   │   ├── README                    # Alembic documentation
    │   │   ├── script.py.mako            # Migration script template
    │   │   └── versions                  # Migration history
    │   ├── alembic.ini                   # Alembic configuration for DB connection
    │   ├── app                            # Main application code
    │   │   ├── agents                    # Agent logic (AI/LLM)
    │   │   │   ├── actions.py            # Definition of agent actions
    │   │   │   ├── config.py             # Agent configuration
    │   │   │   ├── memory                # Agent memory modules
    │   │   │   │   ├── base.py           # Base memory class
    │   │   │   │   ├── in_memory.py      # In-memory storage
    │   │   │   │   ├── redis_async.py    # Asynchronous Redis memory
    │   │   │   │   ├── redis.py          # Synchronous Redis memory
    │   │   │   │   ├── summarize.py      # Memory summarization module
    │   │   │   │   └── vector_memory.py  # Vector memory
    │   │   │   ├── react                  # Reactive agents
    │   │   │   │   └── agent.py          # Reactive agent logic
    │   │   │   ├── schemas.py            # Pydantic schemas for agents
    │   │   │   ├── services              # Auxiliary agent services
    │   │   │   │   └── summary.py        # Summarization service
    │   │   │   ├── state.py              # Agent state storage
    │   │   │   └── tools                 # Agent tools
    │   │   │       ├── __init__.py       # Tools module initialization
    │   │   │       ├── actions
    │   │   │       │   └── execute.py    # Execute agent actions
    │   │   │       ├── base.py           # Base agent tools
    │   │   │       ├── external_api.py   # Working with external APIs
    │   │   │       ├── registry.py       # Agent tool registry
    │   │   │       ├── search.py         # Agent search functions
    │   │   │       ├── summary.py        # Agent data summarization
    │   │   │       ├── validation.py     # Input data validation
    │   │   │       ├── vector_search_async.py # Asynchronous vector search
    │   │   │       └── vector_search.py  # Synchronous vector search
    │   │   ├── api                        # FastAPI endpoints
    │   │   │   ├── agents.py             # Endpoints for agents
    │   │   │   ├── auth.py               # Authorization and authentication
    │   │   │   ├── chat_async.py         # Asynchronous chat
    │   │   │   ├── chat.py               # Synchronous chat
    │   │   │   ├── embeddings.py         # Endpoints for embeddings
    │   │   │   ├── inference.py          # Model inference endpoints
    │   │   │   ├── ingestion.py          # Data ingestion for models
    │   │   │   ├── instruction_tuning.py # LLM instruction tuning
    │   │   │   ├── search.py             # Search endpoints
    │   │   │   └── smart_chat.py         # Smart chat endpoint
    │   │   ├── container.py              # DI container for the application
    │   │   ├── core                        # Application core
    │   │   │   ├── config.py             # Core configuration
    │   │   │   ├── logging.py            # Application logging
    │   │   │   ├── redis.py              # Redis configuration
    │   │   │   ├── security.py           # Security and encryption
    │   │   │   ├── timing.py             # Timing utilities
    │   │   │   ├── tokens.py             # Token handling
    │   │   │   └── vault.py              # Secret vault integration
    │   │   ├── dependencies               # FastAPI dependencies
    │   │   │   ├── agent_params.py       # Agent parameters
    │   │   │   ├── auth.py               # Authorization dependencies
    │   │   │   ├── inference.py          # Inference dependencies
    │   │   │   ├── rate_limit.py         # Request rate limiting
    │   │   │   ├── security.py           # Endpoint security
    │   │   │   ├── user.py               # User dependencies
    │   │   │   └── validation.py         # General validation
    │   │   ├── embeddings                 # Embedding management
    │   │   │   ├── clients               # Embedding clients
    │   │   │   │   ├── client.py         # Base embedding client
    │   │   │   │   ├── gemini_client.py  # Gemini client
    │   │   │   │   └── openai_client.py  # OpenAI client
    │   │   │   ├── factory.py            # Embedding factory
    │   │   │   ├── schemas.py            # Embedding data schemas
    │   │   │   ├── service.py            # Embedding service
    │   │   │   ├── similarity.py         # Similarity calculations
    │   │   │   └── vector_store.py       # Vector storage
    │   │   ├── inference                  # Model inference module
    │   │   │   ├── inference_repository.py       # Inference repository
    │   │   │   ├── inference_service.py  # Inference service
    │   │   │   └── workers               # Inference workers
    │   │   │       ├── async_inference_worker.py # Asynchronous worker
    │   │   │       ├── inference_worker.py       # Synchronous worker
    │   │   │       ├── job_handler       # Job handlers
    │   │   │       │   ├── base.py       # Base handler template
    │   │   │       │   ├── llm_handler.py        # LLM handler
    │   │   │       │   ├── react_handler.py      # ReAct agent handler
    │   │   │       │   └── smart_orchestration_handler.py        # Orchestrator handler
    │   │   │       └── worker_main.py   # Main worker process
    │   │   ├── infra                    # Infrastructure
    │   │   │   ├── __init__.py
    │   │   │   ├── chunker.py           # Data chunking
    │   │   │   ├── db                   # Database utilities
    │   │   │   │   ├── __init__.py
    │   │   │   │   ├── models           # DB models
    │   │   │   │   │   ├── __init__.py
    │   │   │   │   │   ├── base.py      # Base model
    │   │   │   │   │   ├── models.py    # Core collection models
    │   │   │   │   │   └── user_model.py  # User model
    │   │   │   │   ├── pg.py              # PostgreSQL connection
    │   │   │   │   └── qdrant.py          # Qdrant connection
    │   │   │   └── pdf_loader.py          # PDF loading and processing
    │   │   ├── llm                         # LLM logic
    │   │   │   ├── adapters               # Adapters for different LLMs
    │   │   │   │   ├── client.py          # Base client
    │   │   │   │   ├── geminiAdapter.py   # Gemini client
    │   │   │   │   ├── ollamaAdapter.py   # Ollama client
    │   │   │   │   ├── openAIAdapter.py   # OpenAI client
    │   │   │   │   └── qwen3vlAdapter.py  # Qwen3 4B VL Instruct client
    │   │   │   ├── config.py            # LLM configuration
    │   │   │   ├── factory.py           # LLM factory
    │   │   │   ├── filter.py            # LLM filter
    │   │   │   ├── normalizer.py        # Data normalizer
    │   │   │   ├── runner.py            # LLM runner
    │   │   │   ├── sanitizer.py         # Security checks
    │   │   │   └── schemas.py           # LLM schemas (input/output/gen config)
    │   │   ├── main.py                     # FastAPI application entry point
    │   │   ├── middlewares                # FastAPI middlewares
    │   │   │   ├── body.py                # Request body processing
    │   │   │   ├── observability.py       # Metrics and observability
    │   │   │   ├── prometheus.py          # Export metrics to Prometheus
    │   │   │   ├── timings.py             # Request timing
    │   │   │   └── tokens.py              # Token processing middleware
    │   │   ├── models                     # Models
    │   │   │   └── user.py                # User model
    │   │   ├── schemas                    # Pydantic schemas
    │   │   │   ├── agent.py               # Agent schemas
    │   │   │   ├── auth.py                # Auth/register schemas
    │   │   │   ├── chat.py                # Base request schemas
    │   │   │   └── inference.py           # Inference schemas
    │   │   ├── services                   # Business logic services
    │   │   │   ├── auth_service.py        # Auth service
    │   │   │   ├── chat_service.py        # Chat service
    │   │   │   ├── ingestion.py           # Data ingestion service
    │   │   │   ├── orchestration          # LLM and agent orchestration
    │   │   │   │   ├── classifier.py      # One-shot or complex request classifier
    │   │   │   │   └── orchestrator.py    # Orchestrator between agent and simple LLM
    │   │   │   ├── prompts                # LLM prompts
    │   │   │   │   └── classifier_prompt.py  # Classification prompt
    │   │   │   └── rag_service.py         # Retrieval-Augmented Generation service
    │   │   ├── startup.py                 # Application initialization
    │   │   └── validators                 # Validators
    │   │       ├── agent.py               # Agent validation
    │   │       ├── generation.py          # Generation config validation
    │   │       ├── provider.py            # Provider validation
    │   │       └── timeout.py             # Timeout validation
    │   ├── Dockerfile                      # Dockerfile for API service
    │   ├── prometheus.yaml                 # Prometheus monitoring configuration
    │   ├── reflection.md                   # Service documentation/reflection
    │   └── requirements.txt                # Python project dependencies
    └── qwen                                # Separate Qwen service
        ├── Dockerfile.qwen                 # Dockerfile for Qwen service
        ├── inference_service.py            # Model inference launcher
        └── main.py                         # Main file for Qwen service
```

⸻

### 🐳 Docker Setup & Running
Hint: If you are happy owner of Apple Silicon, launch Ollama/Qwen/other open source models locally, NOT via Docker

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
  OLLAMA_BASE_URL="http://host.docker.internal:11434" \
  QWEN3_VL_BASE_URL="http://host.docker.internal:8000" \
  ALLOWED_PROVIDERS='["openai","gemini","ollama","qwen3vl"]' \
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
5. Qwen3 Inference API launch:
- If Apple Silicon:
```bash
uvicorn services.qwen.main:app --reload
```
- If your hardware have drivers in Docker - uncomment docker compose qwen block and change Vault secret QWEN3_VL_BASE_URL and model path to "/models/qwen3v1"

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

/chat/smart
- POST /chat/smart/run - process a single-shot or complex prompt via agent or raw LLM

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
- [HuggingFace](https://huggingface.co/)
- [Ollama](https://ollama.com)


## Русский

Проект ai-assistant-api позволяет взаимодействовать с LLM (Large Language Models — большие языковые модели) через API.
Поддерживаемые модели:
- [OpenAI](https://openai.com)
- [Gemini](https://gemini.google.com)
- [Ollama](https://ollama.com) (использована: [mistral:7b-instruct-q4_K_M](https://ollama.com/library/mistral:7b-instruct-q4_K_M))
- [Qwen3](https://qwen.ai/) (использована: [Qwen3-4B-VL-Instruct](https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct))

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
- Простая LoRa

⸻

### 📁 Структура проекта
```bash
ai-assistant-api/
├── docker-compose.yaml                   # Конфигурация Docker Compose для запуска всех сервисов проекта
├── models                                # Каталог для хранения моделей машинного обучения
│   └── qwen3-vl-4b-instruct              # Конкретная модель Qwen3-VL-4B
│       ├── chat_template.json            # Шаблоны диалогов для модели
│       ├── config.json                   # Основная конфигурация модели
│       ├── generation_config.json        # Настройки генерации текста/видео
│       ├── merges.txt                    # Файл с объединениями токенов (для токенизатора)
│       ├── model-00001-of-00002.safetensors # Весы модели (часть 1)
│       ├── model-00002-of-00002.safetensors # Весы модели (часть 2)
│       ├── model.safetensors.index.json  # Индекс весов модели
│       ├── preprocessor_config.json      # Конфигурация препроцессора данных
│       ├── README.md                     # Документация для модели
│       ├── tokenizer_config.json         # Конфигурация токенизатора
│       ├── tokenizer.json                # Токенизатор модели
│       ├── video_preprocessor_config.json # Конфигурация видео препроцессора
│       └── vocab.json                    # Словарь модели
├── README.md                             # Общая документация проекта
└── services                              # Каталог с сервисами проекта
    ├── api                               # Сервис API (FastAPI)
    │   ├── alembic                       # Конфигурация миграций БД через Alembic
    │   │   ├── env.py                    # Основной скрипт среды Alembic
    │   │   ├── README                    # Документация Alembic
    │   │   ├── script.py.mako            # Шаблон генерации скриптов миграции
    │   │   └── versions                  # История миграций
    │   ├── alembic.ini                   # Настройки Alembic для подключения к БД
    │   ├── app                            # Основной код приложения
    │   │   ├── agents                    # Логика агентов (AI/LLM)
    │   │   │   ├── actions.py            # Определение действий агентов
    │   │   │   ├── config.py             # Конфигурация агентов
    │   │   │   ├── memory                # Модули памяти агентов
    │   │   │   │   ├── base.py           # Базовый класс памяти
    │   │   │   │   ├── in_memory.py      # Память в оперативке
    │   │   │   │   ├── redis_async.py    # Асинхронная память через Redis
    │   │   │   │   ├── redis.py          # Синхронная память Redis
    │   │   │   │   ├── summarize.py      # Модуль суммаризации памяти
    │   │   │   │   └── vector_memory.py  # Векторная память
    │   │   │   ├── react                  # Реактивные агенты
    │   │   │   │   └── agent.py          # Логика реактивного агента
    │   │   │   ├── schemas.py            # Pydantic схемы для агентов
    │   │   │   ├── services              # Вспомогательные сервисы агентов
    │   │   │   │   └── summary.py        # Сервис суммаризации
    │   │   │   ├── state.py              # Хранение состояния агентов
    │   │   │   └── tools                 # Инструменты агентов
    │   │   │       ├── __init__.py       # Инициализация модуля tools
    │   │   │       ├── actions
    │   │   │       │   └── execute.py    # Исполнение действий агентов
    │   │   │       ├── base.py           # Базовые инструменты агентов
    │   │   │       ├── external_api.py   # Работа с внешними API
    │   │   │       ├── registry.py       # Реестр инструментов агентов
    │   │   │       ├── search.py         # Поисковые функции агентов
    │   │   │       ├── summary.py        # Суммаризация данных агентов
    │   │   │       ├── validation.py     # Проверка корректности входных данных
    │   │   │       ├── vector_search_async.py # Асинхронный векторный поиск
    │   │   │       └── vector_search.py  # Синхронный векторный поиск
    │   │   ├── api                        # Эндпоинты FastAPI
    │   │   │   ├── agents.py             # Эндпоинты для работы с агентами
    │   │   │   ├── auth.py               # Авторизация и аутентификация
    │   │   │   ├── chat_async.py         # Асинхронный чат
    │   │   │   ├── chat.py               # Синхронный чат
    │   │   │   ├── embeddings.py         # Эндпоинты для работы с эмбеддингами
    │   │   │   ├── inference.py          # Эндпоинты инференса моделей
    │   │   │   ├── ingestion.py          # Ингест данных для моделей
    │   │   │   ├── instruction_tuning.py # Подстройка инструкций LLM
    │   │   │   ├── search.py             # Поисковые эндпоинты
    │   │   │   └── smart_chat.py         # Эндпоинт умного чата
    │   │   ├── container.py              # DI контейнер приложения
    │   │   ├── core                        # Ядро приложения
    │   │   │   ├── config.py             # Основные конфиги
    │   │   │   ├── logging.py            # Логирование приложения
    │   │   │   ├── redis.py              # Конфигурация Redis
    │   │   │   ├── security.py           # Безопасность и шифрование
    │   │   │   ├── timing.py             # Замеры времени операций
    │   │   │   ├── tokens.py             # Работа с токенами
    │   │   │   └── vault.py              # Интеграция с секретным хранилищем
    │   │   ├── dependencies               # Зависимости FastAPI
    │   │   │   ├── agent_params.py       # Параметры агентов
    │   │   │   ├── auth.py               # Зависимости авторизации
    │   │   │   ├── inference.py          # Зависимости инференса
    │   │   │   ├── rate_limit.py         # Ограничение количества запросов
    │   │   │   ├── security.py           # Безопасность эндпоинтов
    │   │   │   ├── user.py               # Зависимости пользователя
    │   │   │   └── validation.py         # Общая валидация данных
    │   │   ├── embeddings                 # Работа с эмбеддингами
    │   │   │   ├── clients               # Клиенты эмбеддингов
    │   │   │   │   ├── client.py         # Базовый клиент эмбеддингов
    │   │   │   │   ├── gemini_client.py  # Клиент Gemini
    │   │   │   │   └── openai_client.py  # Клиент OpenAI
    │   │   │   ├── factory.py            # Фабрика эмбеддингов
    │   │   │   ├── schemas.py            # Схемы данных эмбеддингов
    │   │   │   ├── service.py            # Сервис работы с эмбеддингами
    │   │   │   ├── similarity.py         # Вычисление схожести
    │   │   │   └── vector_store.py       # Хранилище векторов
    │   │   ├── inference                         # Модуль инференса моделей
    │   │   │   ├── inference_repository.py       # Репозиторий инференса
    │   │   │   ├── inference_service.py  # Сервис инференса
    │   │   │   └── workers               # Рабочие процессы инференса
    │   │   │       ├── async_inference_worker.py # Асинхронный воркер
    │   │   │       ├── inference_worker.py       # Синхронный воркер
    │   │   │       ├── job_handler       # Обработчики разных заданий
    │   │   │       │   ├── base.py       # Шаблон обработчика
    │   │   │       │   ├── llm_handler.py        # Обработчик LLM 
    │   │   │       │   ├── react_handler.py      # Обработчик ReAct агента
    │   │   │       │   └── smart_orchestration_handler.py        # Обработчик оркестратора
    │   │   │       └── worker_main.py   # Основной процесс воркера
    │   │   ├── infra                    # Инфраструктура
    │   │   │   ├── __init__.py
    │   │   │   ├── chunker.py           # Разделение данных на чанки
    │   │   │   ├── db                   # Работа с БД
    │   │   │   │   ├── __init__.py
    │   │   │   │   ├── models           # Модели БД
    │   │   │   │   │   ├── __init__.py
    │   │   │   │   │   ├── base.py      # Базовая модель
    │   │   │   │   │   ├── models.py    # Основные модели коллекций
    │   │   │   │   │   └── user_model.py  # Модель пользователя
    │   │   │   │   ├── pg.py              # Подключение PostgreSQL
    │   │   │   │   └── qdrant.py          # Подключение Qdrant
    │   │   │   └── pdf_loader.py          # Загрузка и обработка PDF
    │   │   ├── llm                         # Работа с LLM
    │   │   │   ├── adapters               # Адаптеры для разных LLM
    │   │   │   │   ├── client.py          # Базовый клиент
    │   │   │   │   ├── geminiAdapter.py   # Клиент Gemini
    │   │   │   │   ├── ollamaAdapter.py   # Клиент Ollama
    │   │   │   │   ├── openAIAdapter.py   # Клиент OpenAI
    │   │   │   │   └── qwen3vlAdapter.py  # Клиент Qwen3 4B VL Instruct
    │   │   │   ├── config.py            # Конфигурация LLM
    │   │   │   ├── factory.py           # LLM Factory
    │   │   │   ├── filter.py            # Фильтр LLM
    │   │   │   ├── normalizer.py        # Нормализатор данных
    │   │   │   ├── runner.py            # LLM Runner
    │   │   │   ├── sanitizer.py         # Проверки безопасности
    │   │   │   └── schemas.py           # Схемы LLM (ввод/вывод/gen конфиг)
    │   │   ├── main.py                     # Точка входа FastAPI приложения
    │   │   ├── middlewares                # Middleware FastAPI
    │   │   │   ├── body.py                # Обработка тела запросов
    │   │   │   ├── observability.py       # Метрики и наблюдаемость
    │   │   │   ├── prometheus.py          # Экспорт метрик в Prometheus
    │   │   │   ├── timings.py             # Замеры времени обработки запросов
    │   │   │   └── tokens.py              # Обработка токенов в middleware
    │   │   ├── models                     # Модели
    │   │   │   └── user.py                # Модель пользователя
    │   │   ├── schemas                    # Pydantic схемы
    │   │   │   ├── agent.py               # Схемы агента
    │   │   │   ├── auth.py                # Схемы авторизации / регистрации
    │   │   │   ├── chat.py                # Схемы базовых запросов
    │   │   │   └── inference.py           # Схемы inference
    │   │   ├── services                   # Сервисы бизнес-логики
    │   │   │   ├── auth_service.py        # Сервис авторизации
    │   │   │   ├── chat_service.py        # Сервис чата
    │   │   │   ├── ingestion.py           # Сервис обработки и загрузки данных
    │   │   │   ├── orchestration          # Оркестрация LLM и агентов
    │   │   │   │   ├── classifier.py      # Классификатор one-shot или complex запросов
    │   │   │   │   └── orchestrator.py    # Оркестратор между агентом и простым LLM
    │   │   │   ├── prompts                # Промпты для LLM
    │   │   │   │   └── classifier_prompt.py  # Промпт классификации
    │   │   │   └── rag_service.py         # Retrieval-Augmented Generation сервис
    │   │   ├── startup.py                 # Инициализация приложения
    │   │   └── validators                 # Валидаторы
    │   │       ├── agent.py               # Валидация агентов
    │   │       ├── generation.py          # Валидация значений generation конфигурации
    │   │       ├── provider.py            # Валидация провайдеров
    │   │       └── timeout.py             # Валидация таймаута
    │   ├── Dockerfile                      # Dockerfile для сервиса API
    │   ├── prometheus.yaml                 # Конфигурация мониторинга Prometheus
    │   ├── reflection.md                   # Документация/рефлексия по сервису
    │   └── requirements.txt                # Зависимости Python проекта
    └── qwen                                # Отдельный сервис Qwen
        ├── Dockerfile.qwen                 # Dockerfile для сервиса Qwen
        ├── inference_service.py            # Запуск инференса модели
        └── main.py                         # Основной файл сервиса Qwen
```
⸻

### 🐳 Docker: установка и запуск
Подсказка: Если Вы счастливый обладатель Apple Silicon, запускайте Ollama/Qwen/любую open source модель локально, не через Docker

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
  OLLAMA_BASE_URL="http://host.docker.internal:11434" \
  QWEN3_VL_BASE_URL="http://host.docker.internal:8000" \
  ALLOWED_PROVIDERS='["openai","gemini","ollama","qwen3vl"]' \
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
5. Запуск Qwen3 Inference API:
- Если у вас Apple Silicon:
```bash
uvicorn services.qwen.main:app --reload
```
- Если у вашего графического ядра есть драйвера в Docker - раскомментируйте docker compose qwen блок и смените Vault secret QWEN3_VL_BASE_URL и model path на "/models/qwen3v1".
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
- [HuggingFace](https://huggingface.co/)
- [Ollama](https://ollama.com)