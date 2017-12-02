# Dockerfile to AWS SQS tester

FROM python:2.7-alpine
#MAINTAINER ibanez.j@gmail.com

LABEL maintainer="ibanez.j@gmail.com"
LABEL Version="0.1"

# RUN apk --update --no-cache add py-pip
RUN pip install boto3

COPY *.py /home/

WORKDIR /home/


#CMD ["python"]
