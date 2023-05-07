FROM python:3.8-slim

LABEL name="redis-cluster"
LABEL maintainer="AppSquad.ReadyNetworks@vodafone.com"

RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get -y install iputils-ping dnsutils procps && \
    rm -rf /var/lib/apt/lists/*

ENV INSTALL_PATH /project
ENV FILE_LOGLEVEL None
ENV PYTHONUNBUFFERED 1
WORKDIR $INSTALL_PATH

COPY ./requirements.txt $INSTALL_PATH
RUN pip install --no-cache-dir -r requirements.txt

COPY . $INSTALL_PATH


CMD ["python", "app/my-app.py"]