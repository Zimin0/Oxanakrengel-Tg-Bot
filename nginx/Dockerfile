FROM ubuntu

# Install Nginx
RUN apt-get update && apt-get install -y nginx

# Copy the Nginx config
COPY nginx.conf /etc/nginx/sites-available/default

# Expose the ports for HTTP and HTTPS
EXPOSE 80/tcp
EXPOSE 443/tcp

# Run the Nginx server
CMD ["/usr/sbin/nginx", "-g", "daemon off;"]
