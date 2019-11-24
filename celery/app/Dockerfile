FROM python:3-slim

ENV INSTALL_PATH /myapp
ENV REDIS_HOST redis
ENV REDIS_PORT 6379

RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

EXPOSE 5000
EXPOSE 5555
