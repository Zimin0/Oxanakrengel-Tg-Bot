FROM ubuntu

# Установка Nginx
RUN apt-get -y update && apt-get -y install nginx
RUN apt-get -y update && apt-get -y upgrade && apt-get -y install nano

# Установка certbot
RUN apt install software-properties-common && add-apt-repository universe && add-apt-repository ppa:certbot/certbot && apt update && apt install certbot python3-certbot-nginx 

# Копируем Nginx конфиг
COPY nginx.conf /etc/nginx/sites-available/default

EXPOSE 80/tcp

CMD ["/usr/sbin/nginx", "-g", "daemon off;"]