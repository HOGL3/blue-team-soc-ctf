#!/bin/bash
set -e

DB_DIR="/app/database"
DB_PATH="${DB_DIR}/db.sqlite3"
APP_USER="appuser"

echo "=== System Startup Diagnostics ==="
echo "Current user: $(id -un)"
echo "Database path: ${DB_PATH}"

# 1. Verify whether /app/database exists and create if missing
if [ ! -d "$DB_DIR" ]; then
    echo "Directory ${DB_DIR} does not exist. Creating it..."
    mkdir -p "$DB_DIR"
fi

# 2. Inspect ownership and permissions
DIR_OWNER=$(stat -c '%U' "$DB_DIR")
DIR_PERMS=$(stat -c '%a' "$DB_DIR")

echo "Directory ownership: ${DIR_OWNER}"
echo "Directory permissions: ${DIR_PERMS}"

# 3. Only perform chown if ownership is incorrect
if [ "$DIR_OWNER" != "$APP_USER" ]; then
    echo "Ownership correction required. Changing ownership of ${DB_DIR} to ${APP_USER}..."
    chown -R ${APP_USER}:${APP_USER} "$DB_DIR"
else
    echo "Ownership is correct. No correction required."
fi

# 4. Ensure the directory is writable by appuser
chmod 755 "$DB_DIR"

echo "=== Handing over to application ==="

echo "Collecting static files..."
runuser -u ${APP_USER} -- python manage.py collectstatic --noinput

echo "Applying database migrations..."
runuser -u ${APP_USER} -- python manage.py migrate --noinput

echo "Seeding initial data..."
runuser -u ${APP_USER} -- python manage.py seed_data

echo "Starting Gunicorn server..."
exec runuser -u ${APP_USER} -- gunicorn blue_team_portal.wsgi:application --bind 0.0.0.0:8000 --workers 3
