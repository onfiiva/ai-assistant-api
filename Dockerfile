# 1. Базовый образ Python
FROM python:3.13-slim

# 2. Установим зависимости для uvicorn, gcc (для некоторых пакетов)
RUN apt-get update && \
    apt-get install -y build-essential python3-dev libffi-dev pkg-config curl && \
    rm -rf /var/lib/apt/lists/*

# 3. Рабочая директория
WORKDIR /app

# 4. Копируем зависимости
COPY requirements.txt /app/

# 5. Устанавливаем зависимости
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Копируем весь проект
COPY . /app

# 7. Открываем порт
EXPOSE 8000

# 8. Команда запуска FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]