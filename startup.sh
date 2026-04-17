#!/bin/sh
set -eu

echo "Starting Django deployment bootstrap..."
if [ "${RUN_MIGRATIONS:-0}" = "1" ]; then
  echo "Running migrations..."
  python manage.py migrate --noinput
else
  echo "Skipping migrations during container startup."
fi

if [ "${RUN_COLLECTSTATIC:-0}" = "1" ]; then
  echo "Collecting static files..."
  python manage.py collectstatic --noinput
else
  echo "Skipping collectstatic during container startup."
fi

echo "Starting Gunicorn on port ${PORT:-8000}..."
exec gunicorn --bind=0.0.0.0:${PORT:-8000} --timeout 600 chat_project.wsgi:application
