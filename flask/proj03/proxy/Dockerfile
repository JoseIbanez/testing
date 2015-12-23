FROM ubuntu
RUN apt-get update
RUN apt-get install -y wget nano dialog net-tools
RUN apt-get install -y nginx

# Remove the default Nginx configuration file
RUN rm -v /etc/nginx/nginx.conf

# Copy a configuration file from the current directory
ADD nginx.conf  /etc/nginx/
ADD servers.lst /etc/nginx/

# Log to stdout
RUN ln -sf /dev/stdout /var/log/nginx/access.log
RUN ln -sf /dev/stdout /var/log/nginx/error.log


# Expose ports
EXPOSE 80

# Set the default command to execute
CMD service nginx start
