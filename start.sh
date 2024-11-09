#!/bin/bash
export PYTHONPATH=/home/hossien/PycharmProjects/restaurant_fastapi
source /home/hossien/PycharmProjects/restaurant_fastapi/.venv/bin/activate
exec /home/hossien/.local/bin/uvicorn main:app --host 0.0.0.0 --port 8000

