FROM python:3.11-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    -y libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./

RUN pip install poetry

RUN poetry config virtualenvs.create false \
    && poetry install