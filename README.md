# AI Assistant API (EN)

The ai-assistant-api project allows interaction with LLMs (Large Language Models) via API. Supported models: OpenAI and Gemini.

With this project, you can:
	•	send requests to LLMs,
	•	receive responses,
	•	experiment with parameters like temperature and top_p.

⸻

📁 Project Structure

ai-assistant-api/
├── gemini
│   └── main.py       # main script for working with Gemini LLM
├── openai
│   └── main.py       # main script for working with OpenAI LLM
├── requirements.txt  # Python dependencies
├── .env              # API keys
├── reflection.md     # mini-reflection after practice
├── README.md         # this file


⸻

🐍 Installation
	1.	Clone the repository:

git clone https://github.com/yourusername/ai-assistant-api.git
cd ai-assistant-api

	2.	Create a virtual environment:

python -m venv venv

	3.	Activate it:

Windows:

venv\Scripts\activate

macOS / Linux:

source venv/bin/activate

	4.	Install dependencies:

pip install -r requirements.txt


⸻

🔑 API Key Setup

Create a .env file in the project root and add your keys:

# OpenAI API
OPENAI_API_KEY=your_openai_api_key

# Gemini API (if used)
GEMINI_API_KEY=your_gemini_api_key

⚠️ Never publish your API keys in public repositories!

⸻

🔧 LLM Parameter Settings
	•	temperature — model creativity (0.0–2.0)
	•	top_p — probability filtering of tokens (0–1)
	•	model — chosen language model

⸻

💡 Tips
	•	For experiments, use small values of temperature and top_p to save tokens.
	•	Always check your API quota, otherwise you’ll get a 429 error (insufficient_quota).

⸻

📚 Resources
	•	OpenAI API Docs￼
	•	Gemini API Docs￼


# AI Assistant API (RU)

Проект ai-assistant-api позволяет взаимодействовать с LLM (Large Language Models) через API. Поддерживаются OpenAI и Gemini.

С помощью этого проекта можно:
	•	отправлять запросы к LLM,
	•	получать ответы,
	•	экспериментировать с параметрами вроде temperature и top_p.

⸻

📁 Структура проекта

ai-assistant-api/
├── gemini
    ├── main.py       # основной скрипт для работы с LLM Gemini
├── openai
    ├── main.py       # основной скрипт для работы с LLM OpenAI
├── requirements.txt  # зависимости Python
├── .env              # API-ключи
├── reflection.md     # мини-рефлексия после практики
├── README.md         # этот файл


⸻

🐍 Установка
	1.	Клонируем репозиторий:

        git clone https://github.com/yourusername/ai-assistant-api.git
        cd ai-assistant-api

	2.	Создаём виртуальное окружение:

        python -m venv venv

	3.	Активируем его:

        Windows:

            venv\Scripts\activate

        macOS / Linux:

            source venv/bin/activate

	4.	Устанавливаем зависимости:

        pip install -r requirements.txt


⸻

🔑 Настройка API-ключей

Создайте файл .env в корне проекта и добавьте ваши ключи:

# OpenAI API
OPENAI_API_KEY=ваш_openai_api_key

# Gemini API (если используете)
GEMINI_API_KEY=ваш_gemini_api_key

⚠️ Никогда не публикуйте ваши ключи в открытых репозиториях!

⸻

🔧 Настройка параметров LLM
	•	temperature — креативность модели (0.0–2.0)
	•	top_p — ограничение выбора наиболее вероятных токенов (0–1)
	•	model — выбираемая языковая модель

⸻

💡 Советы
	•	Для экспериментов используйте небольшие значения temperature и top_p, чтобы экономить токены.
	•	Всегда проверяйте лимит квоты API — иначе получите ошибку 429 (insufficient_quota).

⸻

📚 Ресурсы
	•	OpenAI API Docs￼
	•	Gemini API Docs