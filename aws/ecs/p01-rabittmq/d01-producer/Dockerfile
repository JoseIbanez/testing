# Dockerfile to RabbitMQ test

FROM python:2.7-alpine
#MAINTAINER ibanez.j@gmail.com

LABEL maintainer="ibanez.j@gmail.com"
LABEL Version="0.2"

# RUN apk --update --no-cache add py-pip
RUN pip install pika

COPY *.py /home/

WORKDIR /home/


#CMD ["python"]
