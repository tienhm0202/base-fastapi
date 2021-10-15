FROM tienhm/uvicorn-gunicorn-fastapi:python3.8-slim

LABEL maintainer="Hoang Manh Tien <tienhm.0202@gmail.com>"

ARG PIP_EXTRA_INDEX_URL

WORKDIR /app

RUN apt-get update && apt-get install git -y && rm -rf /var/lib/apt/lists/*
COPY ./pyproject.toml ./
COPY ./poetry.lock* ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

COPY ./prestart.sh ./
COPY . ./
RUN find . -type f -name "*.py[co]" -delete
RUN find . -type d -name "__pycache__" -delete
