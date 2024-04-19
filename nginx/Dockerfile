# Pull the minimal Ubuntu image
FROM ubuntu

# Install Nginx and Certbot
RUN apt-get -y update && apt-get -y install nginx software-properties-common
RUN add-apt-repository ppa:certbot/certbot
RUN apt-get update && apt-get install -y python-certbot-nginx

# Copy the Nginx config
COPY nginx.conf /etc/nginx/sites-available/default
COPY ssl-params.conf /etc/nginx/snippets/ssl-params.conf

# Expose the port for access
EXPOSE 80 443/tcp

# Run the Nginx server
CMD ["/usr/sbin/nginx", "-g", "daemon off;"]
