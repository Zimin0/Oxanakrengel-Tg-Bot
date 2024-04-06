#!/bin/bash

export DJANGO_SETTINGS_MODULE=config.settings

sleep 5

python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Запуск скрипта для создания суперпользователя
python create_superuser.py --noinput
