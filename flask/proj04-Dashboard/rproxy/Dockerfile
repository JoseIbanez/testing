FROM nginx
MAINTAINER Jose Ibañez "ibanez.j@gmail.com"

COPY ./html/pages   /usr/share/nginx/html/pages/
COPY ./html/data    /usr/share/nginx/html/data/
COPY ./html/js      /usr/share/nginx/html/js/
COPY ./html/dist    /usr/share/nginx/html/dist/
COPY ./html/vendor  /usr/share/nginx/html/vendor/

COPY ./install/default.conf     /etc/nginx/conf.d/default.conf
COPY ./install/nginx.conf       /etc/nginx/nginx.conf
