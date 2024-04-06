#!/bin/bash

python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Запуск скрипта для создания суперпользователя
python create_superuser.py --noinput
