#!/bin/sh

# # Загрузка переменных окружения из файла .env в текущий shell
# if [ -f .env ]; then
#   set -a  # Автоматически экспортировать все переменные
#   . ./.env
#   set +a  # Выключить автоэкспорт
# fi

# echo "Ожидание Постгрес."

# until PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$HOST_DB" -p "$PORT_DB" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
#   >&2 echo "Постгрес недоступен..."
#   sleep 1
# done

# >&2 echo "Пострес работает."

# # Выход при любой ошибке
# set -e

# python manage.py makemigrations --noinput
# python manage.py migrate --noinput

# # Запуск скрипта для создания суперпользователя
# python create_superuser.py --noinput

# exec "$@"
