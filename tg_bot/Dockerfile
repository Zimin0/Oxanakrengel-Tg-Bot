FROM python:3.11.3
WORKDIR /bot
COPY . /bot
RUN apt-get update && apt-get install -y cron 
RUN apt-get install -y systemctl && apt-get install -y nano && apt-get install -y iputils-ping 
RUN pip install -r requirements.txt
RUN crontab cron_file.txt