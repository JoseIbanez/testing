FROM ubuntu:14.04
MAINTAINER Jose Ibañez "ibanez.j@gmail.com"

RUN apt-get update && apt-get install -y \
          build-essential \
          python-pip python-dev \
          gunicorn \
          libmysqlclient-dev

RUN pip install \
          flask \
          flask-mysql

EXPOSE 8000
COPY . /app
WORKDIR /app
#ENTRYPOINT ["python"]
CMD ["/app/run.sh"]
