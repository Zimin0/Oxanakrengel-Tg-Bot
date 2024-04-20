# Pull the minimal Ubuntu image
FROM ubuntu:jammy

# Install Nginx and Certbot from Ubuntu repositories
RUN apt-get update && apt-get install -y nginx certbot python3-certbot-nginx

# Copy the Nginx config and SSL params snippet
COPY nginx.conf /etc/nginx/sites-available/default
COPY ssl-params.conf /etc/nginx/snippets/ssl-params.conf

# Expose the ports for HTTP and HTTPS access
EXPOSE 80 443

# Run the Nginx server
CMD ["/usr/sbin/nginx", "-g", "daemon off;"]
