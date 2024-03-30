FROM python:3.11.3
WORKDIR /bot
COPY . /bot
RUN apt-get update && apt-get install -y cron
RUN pip install -r requirements.txt