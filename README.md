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

⸻

### 📁 Project Structure
```
ai-assistant-api/
├── gemini/
│   └── main.py           # Main *dumb* script for testing and working with Gemini LLM directly
├── openai/
│   └── main.py           # Main *dumb* script for testing and working with OpenAI LLM directly
├── app/                  # Core library containing main application logic
│   ├── api/              # FastAPI routes for handling HTTP requests
│   │   └── chat.py       # FastAPI endpoint for chat interactions with LLMs
│   ├── core/             # Core configurations and settings
│   │   ├── config.py     # Application settings, environment variables, API keys
│   │   └── logging.py    # Logging configuration for the project
│   ├── llm/              # LLM library: adapters, runner, normalization, schemas
│   │   ├── client.py        # Base client interface for LLM adapters
│   │   ├── config.py        # Default generation configurations for LLMs
│   │   ├── geminiAdapter.py # Adapter for interacting with Gemini LLM API
│   │   ├── normalizer.py    # Normalizes raw LLM responses into consistent format
│   │   ├── openAIAdapter.py # Adapter for interacting with OpenAI LLM API
│   │   ├── runner.py        # Handles requests to LLMs with retries, backoff, and timeout
│   │   └── schemas.py       # Pydantic schemas for LLM inputs and outputs
│   └── services/        # Application services for business logic
│       └── chat_service.py # ChatService to switch between multiple LLMs in the same request
├── requirements.txt     # Python dependencies for the project
├── .flake8              # Flake8 configuration for code style linting
├── .gitignore           # Git ignore rules for virtualenv, caches, and other files
├── .env                 # Environment variables, including API keys
├── json_requests/       # Saved raw JSON responses from LLMs for debugging or testing
├── reflection.md        # Mini-reflection notes after practice sessions
└── README.md            # Project overview, instructions, and documentation
```

⸻

### 🐍 Installation
1.	Clone the repository:
```
git clone https://github.com/yourusername/ai-assistant-api.git
cd ai-assistant-api
```

2.	Create a virtual environment:
```
python -m venv venv
```

3.	Activate it:

•	Windows:
```
venv\Scripts\activate
```

•	macOS / Linux:
```
source venv/bin/activate
```

4.	Install dependencies:
```
pip install -r requirements.txt
```

5.  Lauch
```
uvicorn app.main:app --reload
```

Swagger
```
http://127.0.0.1:8000/docs
```
⸻

### 🔑 API Key Setup

Create a .env file in the project root and add your keys:

#### OpenAI API key
```
OPENAI_API_KEY=your_openai_api_key
```
#### Gemini API key
```
GEMINI_API_KEY=your_gemini_api_key
```
#### Default provider
```
DEFAULT_PROVIDER=openai (if openai)
DEFAULT_PROVIDER=gemini (if gemeni)
```

⚠️ Never publish your API keys in public repositories!

⸻

### 🔧 LLM Parameter Settings
- temperature — model creativity (0.0–2.0)
- top_p — probability filtering of tokens (0–1)
- model — chosen language model
- max_tokens — max tokens to generate
- timeout — max seconds to wait for a response

⸻

### 💡 Usage Examples

FastAPI endpoint:
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

The response will be returned in a normalized JSON format and optionally saved in json_requests/.

⸻

### 💡 Tips
- Use smaller temperature and top_p values to save tokens when testing.
- Always monitor your API quota to avoid 429 errors (too many requests).
- Responses can be automatically saved as JSON in the json_requests folder for analysis.
- Logging is enabled to track prompts, responses, retries, and timeout events.

⸻

### 📚 Resources
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference/introduction)
- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs?hl=en)

# AI Assistant API

## Русский

Проект ai-assistant-api позволяет взаимодействовать с LLM (Large Language Models) через API.
Поддерживаемые модели: OpenAI и Gemini.

С помощью этого проекта можно:
- Отправлять запросы к LLM
- Получать ответы
- Экспериментировать с параметрами, такими как temperature и top_p
- Контролировать таймауты запросов
- Сохранять ответы в формате JSON для анализа и тестирования
- Переключаться между несколькими провайдерами LLM в одном запросе

⸻

### 📁 Структура проекта
```
ai-assistant-api/
├── gemini/
│   └── main.py           # Основной "глупый" скрипт для тестирования и работы с Gemini LLM напрямую
├── openai/
│   └── main.py           # Основной "глупый" скрипт для тестирования и работы с OpenAI LLM напрямую
├── app/                  # Основная библиотека с логикой приложения
│   ├── api/              # FastAPI маршруты для обработки HTTP-запросов
│   │   └── chat.py       # FastAPI эндпоинт для взаимодействия с LLM
│   ├── core/             # Основные конфигурации и настройки
│   │   ├── config.py     # Настройки приложения, переменные окружения, API ключи
│   │   └── logging.py    # Настройка логирования для проекта
│   ├── llm/              # Библиотека LLM: адаптеры, раннер, нормализация, схемы
│   │   ├── client.py        # Базовый интерфейс клиента для адаптеров LLM
│   │   ├── config.py        # Конфигурации генерации по умолчанию для LLM
│   │   ├── geminiAdapter.py # Адаптер для взаимодействия с API Gemini LLM
│   │   ├── normalizer.py    # Нормализация сырых ответов LLM в единый формат
│   │   ├── openAIAdapter.py # Адаптер для взаимодействия с API OpenAI LLM
│   │   ├── runner.py        # Обработка запросов к LLM с ретраями, backoff и таймаутами
│   │   └── schemas.py       # Pydantic схемы для входных и выходных данных LLM
│   └── services/        # Сервисы приложения с бизнес-логикой
│       └── chat_service.py # ChatService для переключения между несколькими LLM в одном запросе
├── requirements.txt     # Python зависимости проекта
├── .flake8              # Конфигурация Flake8 для проверки стиля кода
├── .gitignore           # Правила игнорирования файлов git (venv, кэш и др.)
├── .env                 # Переменные окружения, включая API ключи
├── json_requests/       # Сохранённые сырые JSON ответы от LLM для отладки и тестирования
├── reflection.md        # Краткие заметки после практики
└── README.md            # Обзор проекта, инструкции и документация
```

⸻

### 🐍 Установка

1.	Клонируйте репозиторий:
```
git clone https://github.com/yourusername/ai-assistant-api.git
cd ai-assistant-api
```

2.	Создайте виртуальное окружение:
```
python -m venv venv
```

3.	Активируйте его:

•	Windows:
```
venv\Scripts\activate
```

•	macOS / Linux:
```
source venv/bin/activate
```

4.	Установите зависимости:
```
pip install -r requirements.txt
```

5.  Запуск
```
uvicorn app.main:app --reload
```

Swagger
```
http://127.0.0.1:8000/docs
```
⸻

### 🔑 Настройка API ключей

Создайте файл .env в корне проекта и добавьте ключи:

#### OpenAI API ключ
```
OPENAI_API_KEY=your_openai_api_key
```

#### Gemini API ключ
```
GEMINI_API_KEY=your_gemini_api_key
```
#### Провайдер по умолчанию
```
DEFAULT_PROVIDER=openai (if openai)
DEFAULT_PROVIDER=gemini (if gemeni)
```

⚠️ Никогда не публикуйте API ключи в публичных репозиториях!

⸻

### 🔧 Настройки параметров LLM
- temperature — креативность модели (0.0–2.0)
- top_p — фильтрация вероятности токенов (0–1)
- model — выбранная языковая модель
- max_tokens — максимальное количество токенов для генерации
- timeout — максимальное время ожидания ответа в секундах

⸻

### 💡 Примеры использования

FastAPI эндпоинт:
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

Ответ возвращается в нормализованном JSON формате и при желании сохраняется в папку json_requests/.

⸻

### 💡 Советы
- Используйте меньшие значения temperature и top_p для экономии токенов при тестировании.
- Следите за квотой API, чтобы не получать ошибки 429 (слишком много запросов).
- Ответы можно автоматически сохранять в формате JSON в папку json_requests/ для анализа.
- Включено логирование для отслеживания промптов, ответов, ретраев и событий таймаута.

⸻

### 📚 Ресурсы
- [Документация OpenAI API](https://platform.openai.com/docs/api-reference/introduction)
- [Документация Gemini API](https://ai.google.dev/gemini-api/docs?hl=ru)