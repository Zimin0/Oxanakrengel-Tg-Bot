# Скрипт создает миграции и админа, если такогового не существует

from dotenv import load_dotenv
import os
import django
from django.contrib.auth.models import User

load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings") # указывает файл настроект проекта 
django.setup() # инициализирует django

username = os.getenv('DJANGO_SUPERUSER_USERNAME')
email = os.getenv('DJANGO_SUPERUSER_EMAIL')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

if not all([username, email, password]):
    [print(f"Перменная среды {var} не установлена!" for var in [username, email, password])]
else:
    if not User.objects.filter(username=username).exists():
        try:
            User.objects.create_superuser(username, email, password)
            print(f"Суперпользователь {username} был создан!")
        except Exception as e:
            print('ОШИБКА:', e)
    else:
        print(f"Суперпользователь {username} уже существует!")
