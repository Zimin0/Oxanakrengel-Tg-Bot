FROM python:3.11.3
WORKDIR /django_project
COPY . /django_project
RUN pip install -r requirements.txt --no-input
RUN python manage.py collectstatic --no-input