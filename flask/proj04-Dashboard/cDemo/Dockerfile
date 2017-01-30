FROM alpine
MAINTAINER Jose Ibañez "ibanez.j@gmail.com"

# basic flask environment
RUN apk add --no-cache bash git py-gunicorn py2-pip \
          	&& pip2 install --upgrade pip \
          	&& pip2 install flask flask-mysql

EXPOSE 8012
COPY . /app
WORKDIR /app
#ENTRYPOINT ["python"]
CMD ["/app/entrypoint.sh"]
