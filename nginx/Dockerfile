# Pull the minimal Ubuntu image
FROM ubuntu

# Install Nginx
RUN apt-get -y update && apt-get -y install nginx
RUN apt-get -y update && apt-get -y upgrade && apt-get -y install nano

# Copy the Nginx config
COPY nginx.conf /etc/nginx/sites-available/default

# Expose the port for access
EXPOSE 80/tcp

# Run the Nginx server
CMD ["/usr/sbin/nginx", "-g", "daemon off;"]