#!/bin/sh
set -eu

echo "Starting Django deployment bootstrap..."
echo "Running migrations..."
python manage.py migrate --noinput
echo "Collecting static files..."
python manage.py collectstatic --noinput
echo "Starting Gunicorn on port ${PORT:-8000}..."
exec gunicorn --bind=0.0.0.0:${PORT:-8000} --timeout 600 chat_project.wsgi:application
