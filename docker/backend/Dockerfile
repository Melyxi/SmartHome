FROM python:3.12-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# 1. Копируем файлы зависимостей
COPY pyproject.toml ./
COPY uv.lock ./

# 2. Синхронизируем зависимости системно (без создания .venv)
# Флаг --frozen гарантирует, что uv не будет обновлять lock-файл
RUN uv sync --frozen --no-cache --no-install-project

# 3. Копируем проект (включая README.md)
COPY . .

# 4. Устанавливаем сам проект (текущую папку)
RUN uv sync --frozen --no-cache

# Переменные окружения
ENV DEBUG=True
ENV PYTHONUNBUFFERED=1
# Добавляем путь к установленным бинарникам проекта в PATH
ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app/backend
# Запуск (теперь можно без полного пути к uvicorn)
CMD sleep 10
CMD uvicorn app:create_app --host 0.0.0.0 --port 8000 --reload
