FROM python:3.11.3
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt --noinput
RUN python manage.py collectstatic --noinput
RUN chmod +x initialize_db.sh