FROM python:3.11.3
WORKDIR /bot
COPY . /bot
RUN apt-get update && apt-get install -y cron
RUN pip install -r requirements.txt
RUN chmod +x clear_products_json.sh
RUN chmod +x upload_phrases_for_cron.sh
RUN chmod +x setup_cron.sh
RUN bash setup_cron.sh