#!/bin/bash

export DJANGO_SETTINGS_MODULE=your_project_name.settings

python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Запуск скрипта для создания суперпользователя
python create_superuser.py --noinput
