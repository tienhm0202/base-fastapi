#!/usr/bin/env bash
env PYTHONPATH=. alembic upgrade head
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:5000