#!/bin/sh
set -e

if [ "$DJANGO_MAKEMIGRATIONS" = "1" ]; then
    echo "Создаем миграции..."
    python manage.py makemigrations --noinput
fi

echo "Применяем миграции..."
python manage.py migrate --noinput

exec "$@"