FROM python:3.11.3
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt --no-input
RUN python manage.py collectstatic --no-input
RUN chmod +x initialize_db.sh