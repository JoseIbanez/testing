FROM python:3.10-slim

LABEL name="botliche"
LABEL maintainer="Jose Ibanez <ibanez.j@gmail.com>"
LABEL description="Simple Bot"

RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get -y install iputils-ping dnsutils procps && \
    rm -rf /var/lib/apt/lists/*

ENV FILE_LOGLEVEL None
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip && \
    pip install wheel 

RUN adduser --disabled-password --gecos "" worker

#USER worker
WORKDIR /home/worker

COPY ./requirements.txt .
RUN pip install -r requirements.txt 

COPY . .


RUN pip install --no-cache-dir .

CMD ["botliched"]
