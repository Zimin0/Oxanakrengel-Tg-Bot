from multiprocessing import cpu_count
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

bind = '0.0.0.0:' + os.getenv('PORT', '8000')
max_requests = 1000
worker_class = 'gevent'
workers = cpu_count() # кол-во ядер == кол-ву воркеров
env = {
    'DJANGO_SETTINGS_MODULE': 'config.settings'
}
reload = True
name = 'service_project'