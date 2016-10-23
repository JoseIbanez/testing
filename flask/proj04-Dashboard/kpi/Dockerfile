FROM ubuntu:14.04
MAINTAINER Jose Ibañez "ibanez.j@gmail.com"
RUN apt-get update -y
RUN apt-get install -y \
          build-essential \
          python-pip python-dev \
          gunicorn \
          libmysqlclient-dev

RUN pip install \
          flask \
          flask-mysql

EXPOSE 8010
COPY . /app
WORKDIR /app
#ENTRYPOINT ["python"]
CMD ["/app/run.sh"]
