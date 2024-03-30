FROM python:3.11.3
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]