# AI Assistant API

[English](#english) | [Русский](#русский)<br/>

- [🐳 Installation](#-docker-setup--running)<br/>
- [🐳 Установка](#-docker-установка-и-запуск)<br/>

⸻

## English

The ai-assistant-api project allows interaction with LLMs (Large Language Models) via API.
Supported models:<br/>
- [OpenAI](https://openai.com)<br/>
- [Gemini](https://gemini.google.com)<br/>

Local supported models:<br/>
[API for Qwen models](https://github.com/onfiiva/qwen3-apis)<br/>

- [Ollama](https://ollama.com)<br/>
[mistral:7b-instruct-q4_K_M](https://ollama.com/library/mistral:7b-instruct-q4_K_M)<br/>
- [Qwen3](https://qwen.ai/)<br/>
[Qwen3-4B-VL-Instruct](https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct)<br/>
[Qwen3-TTS-12Hz-1.7B-CustomVoice](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice)<br/>


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
- Send requests to LMStudio
- Send TTS voice generation requests
- Evaluate models and Base / Fine-tuned / RAG requests

⸻

### 📁 Project Structure
```bash
ai-assistant-api/                         # Root directory of the AI assistant project
├── api/                                  # Main backend service (FastAPI)
│   ├── alembic/                          # Database migrations (Alembic)
│   │   ├── env.py                        # Alembic initialization and DB connection setup
│   │   ├── README                        # Migration documentation
│   │   ├── script.py.mako                # Migration file generation template
│   │   └── versions/                     # Migration history
│   ├── alembic.ini                       # Alembic configuration (DB URL and settings)
│   ├── app/                              # Main application source code
│   │   ├── agents/                       # AI agent logic (ReAct, tool-based, etc.)
│   │   │   ├── actions.py                # Definition of possible agent actions
│   │   │   ├── config.py                 # Agent configuration (temperature, limits, etc.)
│   │   │   ├── memory/                   # Agent memory subsystem
│   │   │   │   ├── base.py               # Base memory interface
│   │   │   │   ├── in_memory.py          # In-memory storage
│   │   │   │   ├── redis_async.py        # Asynchronous Redis memory
│   │   │   │   ├── redis.py              # Synchronous Redis memory
│   │   │   │   ├── summarize.py          # Conversation history summarization
│   │   │   │   └── vector_memory.py      # Vector-based memory (RAG)
│   │   │   ├── react/                    # ReAct agent implementation
│   │   │   │   └── agent.py              # ReAct loop logic (Thought → Action → Observation)
│   │   │   ├── schemas.py                # Pydantic schemas for agents
│   │   │   ├── services/
│   │   │   │   └── summary.py            # Conversation summarization service
│   │   │   ├── state.py                  # Agent state management
│   │   │   └── tools/                    # Tools available to the agent
│   │   │       ├── __init__.py           # Tools package initialization
│   │   │       ├── actions/execute.py    # Agent action execution logic
│   │   │       ├── base.py               # Base tool class
│   │   │       ├── external_api.py       # External API integrations
│   │   │       ├── registry.py           # Tool registry
│   │   │       ├── search.py             # Search (local / vector)
│   │   │       ├── summary.py            # Data summarization tool
│   │   │       ├── validation.py         # Tool input validation
│   │   │       ├── vector_search_async.py# Asynchronous vector search
│   │   │       └── vector_search.py      # Synchronous vector search
│   │   ├── api/                          # FastAPI HTTP endpoints
│   │   │   ├── agents.py                 # Agent-related API endpoints
│   │   │   ├── auth.py                   # Authentication and authorization
│   │   │   ├── chat.py                   # Synchronous chat endpoint
│   │   │   ├── chat_async.py             # Asynchronous chat endpoint
│   │   │   ├── embeddings.py             # Embedding generation endpoint
│   │   │   ├── inference.py              # Generic inference endpoint
│   │   │   ├── ingestion.py              # Data upload and indexing
│   │   │   ├── instruction_tuning.py     # Fine-tuning / instruction tuning
│   │   │   ├── lmstudio.py               # LM Studio integration
│   │   │   ├── search.py                 # Search API endpoint
│   │   │   ├── smart_chat.py             # Smart orchestrated chat endpoint
│   │   │   └── tts.py                    # Text-to-Speech endpoint
│   │   ├── container.py                  # Dependency Injection container
│   │   ├── core/                         # Core infrastructure configuration
│   │   │   ├── config.py                 # Global application settings
│   │   │   ├── logging.py                # Logging configuration
│   │   │   ├── redis.py                  # Redis configuration
│   │   │   ├── security.py               # Security, hashing, encryption
│   │   │   ├── timing.py                 # Timing utilities
│   │   │   ├── tokens.py                 # Token usage tracking (LLM usage)
│   │   │   └── vault.py                  # Secret vault integration
│   │   ├── dependencies/                 # FastAPI dependency modules
│   │   │   ├── agent_params.py           # Agent parameters extraction from request
│   │   │   ├── auth.py                   # Authentication dependency
│   │   │   ├── inference.py              # Inference dependency
│   │   │   ├── rate_limit.py             # Request rate limiting
│   │   │   ├── security.py               # Security checks
│   │   │   ├── user.py                   # Current user extraction
│   │   │   └── validation.py             # General validation dependency
│   │   ├── embeddings/                   # Embedding subsystem
│   │   │   ├── clients/                  # External embedding provider clients
│   │   │   ├── factory.py                # Embedding client factory
│   │   │   ├── schemas.py                # Embedding data schemas
│   │   │   ├── service.py                # Embedding business logic
│   │   │   ├── similarity.py             # Similarity calculation
│   │   │   └── vector_store.py           # Vector storage integration
│   │   ├── inference/                    # Asynchronous LLM task processing
│   │   │   ├── inference_repository.py   # Task persistence layer
│   │   │   ├── inference_service.py      # Inference execution service
│   │   │   └── workers/                  # Background workers
│   │   │       ├── async_inference_worker.py
│   │   │       ├── inference_worker.py
│   │   │       ├── worker_main.py        # Worker entry point
│   │   │       └── job_handler/          # Handlers for different job types
│   │   ├── infra/                        # Infrastructure layer
│   │   │   ├── chunker.py                # Text chunking utility
│   │   │   ├── pdf_loader.py             # PDF parsing and loading
│   │   │   └── db/                       # Database integration
│   │   ├── llm/                          # Unified LLM abstraction layer
│   │   │   ├── adapters/                 # Provider-specific adapters
│   │   │   │   ├── base/                 # Base abstractions (generation, embedding, TTS)
│   │   │   │   ├── geminiAdapter.py      # Google Gemini adapter
│   │   │   │   ├── LMStudioAdapter.py    # LM Studio adapter
│   │   │   │   ├── ollamaAdapter.py      # Ollama adapter
│   │   │   │   ├── openAIAdapter.py      # OpenAI adapter
│   │   │   │   ├── qwen3TTSAdapter.py    # Qwen TTS adapter
│   │   │   │   └── qwen3vlAdapter.py     # Qwen3-VL (vision-language) adapter
│   │   │   ├── config.py                 # LLM configuration
│   │   │   ├── factory.py                # LLM factory
│   │   │   ├── filter.py                 # Request filtering
│   │   │   ├── normalizer.py             # Input normalization
│   │   │   ├── runner.py                 # Unified LLM execution runner
│   │   │   ├── sanitizer.py              # Prompt sanitization and safety
│   │   │   └── schemas.py                # LLM request/response schemas
│   │   ├── middlewares/                  # FastAPI middleware
│   │   ├── models/user.py                # ORM user model
│   │   ├── schemas/                      # API Pydantic schemas
│   │   ├── services/                     # Application business logic
│   │   │   ├── auth_service.py           # Authentication logic
│   │   │   ├── chat_service.py           # Chat processing logic
│   │   │   ├── ingestion.py              # Data indexing logic
│   │   │   ├── rag_service.py            # Retrieval-Augmented Generation logic
│   │   │   ├── tts_service.py            # Text-to-Speech business logic
│   │   │   └── orchestration/            # LLM and agent orchestration
│   │   ├── startup.py                    # Application initialization logic
│   │   └── validators/                   # Parameter validators
│   ├── evaluation/                       # Evaluation source code
│   │   ├── reports/                      # Evaluation JSON reports
│   │   ├── runners/                      # Evaluation runners
│   │   │   ├── base/                     # Base runner abstract classes
│   │   │   │   └── base.py               # Base runner interface
│   │   │   ├── __init__.py               # Init python module
│   │   │   ├── base_model_runner.py      # Base endpoint runner
│   │   │   ├── finetuned_model_runner.py # Fine-tuned endpoint runner
│   │   │   └── rag_runner.py             # RAG endpoint runner
│   │   ├── __init__.py                   # Init python module
│   │   ├── dataset.json                  # Evaluation dataset
│   │   ├── evaluator.py                  # Evaluator
│   │   ├── metrics.py                    # Evaluation metrics
│   │   ├── report.py                     # Ways to report evaluations
│   │   └── run_evaluator.py              # Evaluator executor
│   ├── Dockerfile                        # Docker image definition for API service
│   ├── prometheus.yaml                   # Prometheus metrics configuration
│   ├── reflection.md                     # Architecture notes and reflections
│   └── requirements.txt                  # Python dependencies
├── docker-compose.yaml                   # Multi-service orchestration (API, DB, Redis, etc.)
└── README.md                             # General project documentation
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
  OLLAMA_BASE_URL="http://host.docker.internal:11434" \
  QWEN3_VL_BASE_URL="http://host.docker.internal:8000" \
  QWEN_TTS_BASE_URL="http://host.docker.internal:8000" \
  TTS_API_URL="http://host.docker.internal:9000" \
  LMSTUDIO_BASE_URL="someurl" \
  LMSTUDIO_API_KEY="somekey" \
  ALLOWED_PROVIDERS='["openai","gemini","ollama","qwen-tts","lmstudio"]' \
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
5. Evaluation:
```bash
python -m evaluation.run_evaluator
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

#### /chat/smart
- POST /chat/smart/run - process a single-shot or complex prompt via agent or raw LLM

#### /agents
- POST /agents/run — run an agent with a goal, returns job_id
- GET /agents/{job_id} — get agent job status and step history
- GET /agents/tools — list available tools for the agent

#### /embeddings
- POST /embeddings/search — semantic search, returns top-k results

#### /ingestion
- POST /ingestion/ingest — ingest PDF documents into vector DB with embeddings

#### /search
- GET /search/ — search pre-ingested embeddings, returns top-k matches

#### /inference
- POST /inference/ — create async inference job
- GET /inference/{job_id} — get status and result/error of async job

#### /tts
- POST / — create voice .wav file to download

#### /lmstudio
- GET /models/ — search available lmstudio models

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
Поддерживаемые модели:<br/>
- [OpenAI](https://openai.com)<br/>
- [Gemini](https://gemini.google.com)<br/>

Локальные поддерживаемые модели:<br/>
[API for Qwen models](https://github.com/onfiiva/qwen3-apis)<br/>

- [Ollama](https://ollama.com)<br/>
[mistral:7b-instruct-q4_K_M](https://ollama.com/library/mistral:7b-instruct-q4_K_M)<br/>
- [Qwen3](https://qwen.ai/)<br/>
[Qwen3-4B-VL-Instruct](https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct)<br/>
[Qwen3-TTS-12Hz-1.7B-CustomVoice](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice)<br/>

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
- Генерировать голосовые файлы .wav с помощью TTS
- Обращаться к LMService

⸻

### 📁 Структура проекта
```bash
ai-assistant-api/                         # Корень проекта AI-ассистента
├── api/                                  # Основной backend-сервис (FastAPI)
│   ├── alembic/                          # Миграции базы данных (Alembic)
│   │   ├── env.py                        # Инициализация Alembic, подключение к БД
│   │   ├── README                        # Документация по миграциям
│   │   ├── script.py.mako                # Шаблон генерации файлов миграций
│   │   └── versions/                     # История миграций
│   ├── alembic.ini                       # Конфигурация Alembic (URL БД и настройки)
│   ├── app/                              # Основной код приложения
│   │   ├── agents/                       # Логика AI-агентов (ReAct, tool-based и др.)
│   │   │   ├── actions.py                # Определение возможных действий агента
│   │   │   ├── config.py                 # Конфигурация агентов (температура, лимиты и т.д.)
│   │   │   ├── memory/                   # Подсистема памяти агента
│   │   │   │   ├── base.py               # Базовый интерфейс памяти
│   │   │   │   ├── in_memory.py          # Память в оперативке
│   │   │   │   ├── redis_async.py        # Асинхронная Redis-память
│   │   │   │   ├── redis.py              # Синхронная Redis-память
│   │   │   │   ├── summarize.py          # Саммаризация истории диалога
│   │   │   │   └── vector_memory.py      # Векторная память (RAG)
│   │   │   ├── react/                    # Реализация ReAct-агента
│   │   │   │   └── agent.py              # Логика ReAct цикла (Thought → Action → Observation)
│   │   │   ├── schemas.py                # Pydantic-схемы для агентов
│   │   │   ├── services/
│   │   │   │   └── summary.py            # Сервис суммаризации истории
│   │   │   ├── state.py                  # Хранение состояния агента
│   │   │   └── tools/                    # Инструменты, которыми пользуется агент
│   │   │       ├── __init__.py           # Инициализация пакета tools
│   │   │       ├── actions/execute.py    # Исполнение действий агента
│   │   │       ├── base.py               # Базовый класс инструмента
│   │   │       ├── external_api.py       # Вызовы внешних API
│   │   │       ├── registry.py           # Реестр доступных инструментов
│   │   │       ├── search.py             # Поиск (локальный / векторный)
│   │   │       ├── summary.py            # Саммаризация данных
│   │   │       ├── validation.py         # Валидация входных данных инструмента
│   │   │       ├── vector_search_async.py# Асинхронный векторный поиск
│   │   │       └── vector_search.py      # Синхронный векторный поиск
│   │   ├── api/                          # HTTP-эндпоинты FastAPI
│   │   │   ├── agents.py                 # API для работы с агентами
│   │   │   ├── auth.py                   # Авторизация и аутентификация
│   │   │   ├── chat.py                   # Синхронный чат
│   │   │   ├── chat_async.py             # Асинхронный чат
│   │   │   ├── embeddings.py             # Генерация эмбеддингов
│   │   │   ├── inference.py              # Универсальный inference endpoint
│   │   │   ├── ingestion.py              # Загрузка и индексация данных
│   │   │   ├── instruction_tuning.py     # Fine-tuning / instruction tuning
│   │   │   ├── lmstudio.py               # Интеграция с LM Studio
│   │   │   ├── search.py                 # API поиска
│   │   │   ├── smart_chat.py             # Умный оркестрированный чат
│   │   │   └── tts.py                    # Text-to-Speech endpoint
│   │   ├── container.py                  # Dependency Injection контейнер
│   │   ├── core/                         # Базовая инфраструктурная конфигурация
│   │   │   ├── config.py                 # Глобальные настройки приложения
│   │   │   ├── logging.py                # Настройка логирования
│   │   │   ├── redis.py                  # Конфигурация Redis
│   │   │   ├── security.py               # Безопасность, хэширование, шифрование
│   │   │   ├── timing.py                 # Утилиты замера времени
│   │   │   ├── tokens.py                 # Работа с токенами (LLM usage)
│   │   │   └── vault.py                  # Интеграция с секрет-хранилищем
│   │   ├── dependencies/                 # FastAPI dependencies
│   │   │   ├── agent_params.py           # Параметры агента из запроса
│   │   │   ├── auth.py                   # Dependency авторизации
│   │   │   ├── inference.py              # Dependency для инференса
│   │   │   ├── rate_limit.py             # Ограничение частоты запросов
│   │   │   ├── security.py               # Проверки безопасности
│   │   │   ├── user.py                   # Получение пользователя
│   │   │   └── validation.py             # Общая валидация
│   │   ├── embeddings/                   # Подсистема эмбеддингов
│   │   │   ├── clients/                  # Клиенты внешних embedding-провайдеров
│   │   │   ├── factory.py                # Фабрика создания embedding-клиентов
│   │   │   ├── schemas.py                # Схемы эмбеддингов
│   │   │   ├── service.py                # Бизнес-логика эмбеддингов
│   │   │   ├── similarity.py             # Расчёт similarity
│   │   │   └── vector_store.py           # Работа с векторным хранилищем
│   │   ├── inference/                    # Асинхронная обработка LLM-задач
│   │   │   ├── inference_repository.py   # Работа с хранилищем задач
│   │   │   ├── inference_service.py      # Сервис запуска инференса
│   │   │   └── workers/                  # Воркеры обработки задач
│   │   │       ├── async_inference_worker.py
│   │   │       ├── inference_worker.py
│   │   │       ├── worker_main.py        # Точка входа воркера
│   │   │       └── job_handler/          # Обработчики разных типов задач
│   │   ├── infra/                        # Инфраструктурный слой
│   │   │   ├── chunker.py                # Разбиение текста на чанки
│   │   │   ├── pdf_loader.py             # Парсинг PDF
│   │   │   └── db/                       # Работа с БД
│   │   ├── llm/                          # Универсальный LLM-слой
│   │   │   ├── adapters/                 # Адаптеры разных провайдеров
│   │   │   │   ├── base/                 # Базовые абстракции (generation, embedding, tts)
│   │   │   │   ├── geminiAdapter.py      # Google Gemini
│   │   │   │   ├── LMStudioAdapter.py    # LM Studio
│   │   │   │   ├── ollamaAdapter.py      # Ollama
│   │   │   │   ├── openAIAdapter.py      # OpenAI
│   │   │   │   ├── qwen3TTSAdapter.py    # Qwen TTS
│   │   │   │   └── qwen3vlAdapter.py     # Qwen3-VL (vision-language)
│   │   │   ├── config.py                 # Конфигурация LLM
│   │   │   ├── factory.py                # Фабрика создания LLM
│   │   │   ├── filter.py                 # Фильтрация запросов
│   │   │   ├── normalizer.py             # Нормализация входных данных
│   │   │   ├── runner.py                 # Универсальный запуск LLM
│   │   │   ├── sanitizer.py              # Безопасность (prompt sanitation)
│   │   │   └── schemas.py                # Схемы LLM-запросов/ответов
│   │   ├── middlewares/                  # Middleware FastAPI
│   │   ├── models/user.py                # ORM модель пользователя
│   │   ├── schemas/                      # Pydantic-схемы API
│   │   ├── services/                     # Бизнес-логика приложения
│   │   │   ├── auth_service.py           # Логика авторизации
│   │   │   ├── chat_service.py           # Логика чата
│   │   │   ├── ingestion.py              # Индексация данных
│   │   │   ├── rag_service.py            # Retrieval-Augmented Generation
│   │   │   ├── tts_service.py            # Text-to-Speech логика
│   │   │   └── orchestration/            # Оркестрация LLM и агентов
│   │   ├── startup.py                    # Инициализация приложения
│   │   └── validators/                   # Валидаторы параметров
│   ├── evaluation/                       # Исходный код сервиса оценки
│   │   ├── reports/                      # Отчеты об оценке
│   │   ├── runners/                      # Runner'ы
│   │   │   ├── base/                     # Базовые абстрактные runner'ы
│   │   │   │   └── base.py               # Базовый интерфейс runner'а
│   │   │   ├── __init__.py               # Инициализация python модуля
│   │   │   ├── base_model_runner.py      # Runner базового endpoint'а
│   │   │   ├── finetuned_model_runner.py # Runner Fine-tuned endpoint'а
│   │   │   └── rag_runner.py             # Runner RAG endpoint'а
│   │   ├── __init__.py                   # Инициализация python модуля
│   │   ├── dataset.json                  # Набор данных для оценки
│   │   ├── evaluator.py                  # Оценщик
│   │   ├── metrics.py                    # Метрики оценок
│   │   ├── report.py                     # Управление отчетностью
│   │   └── run_evaluator.py              # Выполняемый файл оценщика
│   ├── Dockerfile                        # Docker-образ API сервиса
│   ├── prometheus.yaml                   # Конфигурация метрик Prometheus
│   ├── reflection.md                     # Архитектурные заметки
│   └── requirements.txt                  # Python-зависимости
├── docker-compose.yaml                   # Оркестрация сервисов (API, БД, Redis и т.д.)
└── README.md                             # Общая документация проекта
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
  OLLAMA_BASE_URL="http://host.docker.internal:11434" \
  QWEN3_VL_BASE_URL="http://host.docker.internal:8000" \
  QWEN_TTS_BASE_URL="http://host.docker.internal:8000" \
  TTS_API_URL="http://host.docker.internal:9000" \
  LMSTUDIO_BASE_URL="someurl" \
  LMSTUDIO_API_KEY="somekey" \
  ALLOWED_PROVIDERS='["openai","gemini","ollama","qwen-tts","lmstudio"]' \
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
5. Оценка запросов к модели:
```bash
python -m evaluation.run_evaluator
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

#### /tts
- POST / — создание голосового .wav файла для скачивания

#### /lmstudio
- GET /models/ — найти доступные модели LMStudio

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