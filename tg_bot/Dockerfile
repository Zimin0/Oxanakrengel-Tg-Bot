FROM python:3.11.3
WORKDIR /bot
COPY . /bot
RUN apt-get update && apt-get install -y cron
# Для дебага
RUN apt-get install -y systemctl && apt-get install nano && apt-get install ping 
RUN pip install -r requirements.txt
RUN crontab cron_file.txt