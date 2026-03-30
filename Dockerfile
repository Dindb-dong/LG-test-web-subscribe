FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV UV_LINK_MODE=copy

RUN pip install --no-cache-dir uv

COPY pyproject.toml /app/pyproject.toml
RUN uv sync --dev --no-install-project

COPY . /app

EXPOSE 8000

CMD ["sh", "-c", "uv run uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
