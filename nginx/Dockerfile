# Pull the minimal Ubuntu image
FROM ubuntu

# Install Nginx
RUN apt-get -y update && apt-get -y install nginx
RUN apt-get -y update && apt-get -y upgrade && apt-get -y install nano

# Copy the Nginx config and SSL params snippet
COPY nginx.conf /etc/nginx/sites-available/default
COPY ssl-params.conf /etc/nginx/snippets/ssl-params.conf

# Expose the ports for HTTP and HTTPS
EXPOSE 80/tcp
EXPOSE 443/tcp

# Run the Nginx server
CMD ["/usr/sbin/nginx", "-g", "daemon off;"]
