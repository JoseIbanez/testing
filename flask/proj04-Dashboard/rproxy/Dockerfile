FROM nginx
MAINTAINER Jose Ibañez "ibanez.j@gmail.com"

COPY ./html/pages   /usr/share/nginx/html/
COPY ./html/data    /usr/share/nginx/html/
COPY ./html/js      /usr/share/nginx/html/
COPY ./html/dist    /usr/share/nginx/html/
COPY ./html/vendor  /usr/share/nginx/html/

COPY ./install/default    /etc/nginx/sites-available/default
COPY ./install/nginx.conf /etc/nginx/nginx.conf
