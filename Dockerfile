FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.1.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# Системные зависимости (если нужны для сборки пакетов)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка poetry
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# Копируем только файлы зависимостей
COPY pyproject.toml poetry.lock* ./

# Установка зависимостей
RUN poetry install --no-root --only main

# Копируем проект
COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--log-config", "app/core/logging.yaml"]
