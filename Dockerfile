FROM python:3.11-slim

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

# Set environment variables for Django
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=project_k.settings

# Collect static files at build time (optional)
RUN python manage.py collectstatic --noinput

# The command will be overridden by docker-compose.yml
