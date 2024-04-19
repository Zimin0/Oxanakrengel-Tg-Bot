# Используем официальный базовый образ Ubuntu
FROM ubuntu:latest

# Установка Nginx
RUN apt-get update && \
    apt-get install -y nginx && \
    apt-get install -y nano

# Установка software-properties-common и добавление репозитория Certbot
RUN apt-get install -y software-properties-common && \
    add-apt-repository universe && \
    add-apt-repository ppa:certbot/certbot && \
    apt-get update

# Установка Certbot
RUN apt-get install -y certbot python3-certbot-nginx

# Копирование Nginx конфигурации
COPY nginx.conf /etc/nginx/sites-available/default

EXPOSE 80/tcp

CMD ["/usr/sbin/nginx", "-g", "daemon off;"]