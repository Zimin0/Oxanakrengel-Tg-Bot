#!/bin/sh

# Загрузка переменных окружения из файла .env в текущий shell
if [ -f .env ]; then
  while read -r line; do
    if echo "$line" | grep -F = &>/dev/null; then
      varname=$(echo "$line" | cut -d '=' -f 1)
      export "$varname"=$(echo "$line" | cut -d '=' -f 2-)
    fi
  done < .env
fi

# Проверка использования базы данных PostgreSQL
if [ "$DATABASE" = "postgres" ]; then
  echo "Ожидание Постгрес."

  # Ожидание доступности PostgreSQL
  until nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
    sleep 0.1
  done

  echo "Постгрес работает."
fi

# Выход при любой ошибке
set -e

# Выполнение миграций Django
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Запуск скрипта для создания суперпользователя
python create_superuser.py --noinput

exec "$@"
