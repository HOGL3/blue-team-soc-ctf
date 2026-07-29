#!/bin/bash
set -e

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Seeding initial data..."
python manage.py seed_data

echo "Starting Gunicorn server..."
exec gunicorn blue_team_portal.wsgi:application --bind 0.0.0.0:8000 --workers 3
