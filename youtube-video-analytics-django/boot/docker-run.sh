#!/bin/bash

# Activate virtual environment
source /opt/venv/bin/activate

# Move to Django project root (where manage.py is)
cd /code

# Set defaults if env vars are not provided
RUN_PORT=${PORT:-8000}
RUN_HOST=${HOST:-127.0.0.1}

# Run Django with Gunicorn (WSGI)
gunicorn config.wsgi:application \
  --bind $RUN_HOST:$RUN_PORT \
  --workers 3 \
  --timeout 120
