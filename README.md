# AI Assistant API

## English Version

The ai-assistant-api project allows interaction with LLMs (Large Language Models) via API. Supported models: OpenAI and Gemini.

With this project, you can:
	•	Send requests to LLMs
	•	Receive responses
	•	Experiment with parameters like temperature and top_p
	•	Save responses in JSON format for analysis and testing

⸻

### 📁 Project Structure

ai-assistant-api/
├── gemini/
│   └── main.py       # Main script for working with Gemini LLM
├── openai/
│   └── main.py       # Main script for working with OpenAI LLM
├── app/              # Core library: adapters, runner, schemas
├── requirements.txt  # Python dependencies
├── .env              # API keys
├── json_requests/    # Saved JSON responses from LLMs
├── reflection.md     # Mini-reflection after practice
├── README.md         # This file


⸻

### 🐍 Installation
	1.	Clone the repository:
        ```
        git clone https://github.com/yourusername/ai-assistant-api.git
        cd ai-assistant-api
        ```

	2.	Create a virtual environment:

        `python -m venv venv`

	3.	Activate it:

	•	Windows:

        `venv\Scripts\activate`

	•	macOS / Linux:

        `source venv/bin/activate`

	4.	Install dependencies:

        `pip install -r requirements.txt`


⸻

### 🔑 API Key Setup

Create a .env file in the project root and add your keys:

#### OpenAI API
OPENAI_API_KEY=your_openai_api_key

#### Gemini API (if used)
GEMINI_API_KEY=your_gemini_api_key

⚠️ Never publish your API keys in public repositories!

⸻

### 🔧 LLM Parameter Settings
	•	temperature — model creativity (0.0–2.0)
	•	top_p — probability filtering of tokens (0–1)
	•	model — chosen language model
	•	max_tokens — max tokens to generate

⸻

### 💡 Tips
	•	For experiments, use smaller values of temperature and top_p to save tokens.
	•	Always check your API quota, otherwise you’ll get a 429 error (insufficient quota).
	•	Responses can be automatically saved as JSON in the json_requests folder for analysis.

⸻

### 📚 Resources
	•	OpenAI API Docs￼
	•	Gemini API Docs￼

⸻

# Russian Version

Проект ai-assistant-api позволяет взаимодействовать с LLM (Large Language Models) через API. Поддерживаются OpenAI и Gemini.

С помощью этого проекта можно:
	•	Отправлять запросы к LLM
	•	Получать ответы
	•	Экспериментировать с параметрами вроде temperature и top_p
	•	Сохранять ответы в формате JSON для анализа и тестов

⸻

### 📁 Структура проекта

ai-assistant-api/
├── gemini/
│   └── main.py       # Основной скрипт для работы с LLM Gemini
├── openai/
│   └── main.py       # Основной скрипт для работы с LLM OpenAI
├── app/              # Ядро проекта: адаптеры, раннер, схемы
├── requirements.txt  # Зависимости Python
├── .env              # API-ключи
├── json_requests/    # Сохраненные JSON-ответы от LLM
├── reflection.md     # Мини-рефлексия после практики
├── README.md         # Этот файл


⸻

### 🐍 Установка
	1.	Клонируем репозиторий:
        ```
        git clone https://github.com/yourusername/ai-assistant-api.git
        cd ai-assistant-api
        ```

	2.	Создаем виртуальное окружение:

        `python -m venv venv`

	3.	Активируем его:

	•	Windows:

        `venv\Scripts\activate`

	•	macOS / Linux:

        `source venv/bin/activate`

	4.	Устанавливаем зависимости:

        `pip install -r requirements.txt`


⸻

### 🔑 Настройка API-ключей

Создайте файл .env в корне проекта и добавьте ваши ключи:

#### OpenAI API
OPENAI_API_KEY=ваш_openai_api_key

#### Gemini API (если используете)
GEMINI_API_KEY=ваш_gemini_api_key

⚠️ Никогда не публикуйте ваши ключи в открытых репозиториях!

⸻

### 🔧 Настройка параметров LLM
	•	temperature — креативность модели (0.0–2.0)
	•	top_p — ограничение выбора наиболее вероятных токенов (0–1)
	•	model — выбираемая языковая модель
	•	max_tokens — максимальное количество генерируемых токенов

⸻

### 💡 Советы
	•	Для экспериментов используйте небольшие значения temperature и top_p, чтобы экономить токены.
	•	Всегда проверяйте лимит квоты API — иначе получите ошибку 429.
	•	Ответы можно автоматически сохранять в JSON в папке json_requests для анализа.

⸻

### 📚 Ресурсы
	•	Документация OpenAI API￼
	•	Документация Gemini API￼