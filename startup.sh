#!/bin/sh
set -e

echo "==== Running migrations on mounted volume ===="

# Ensure persistent data dir and file exist
mkdir -p /data
touch /data/db.sqlite3

# Run Django migrations
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "==== Collecting static files ===="
python manage.py collectstatic --noinput

echo "==== Starting Gunicorn ===="
exec gunicorn --bind 0.0.0.0:8000 --workers 1 ridwan.wsgi
