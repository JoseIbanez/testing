FROM ubuntu:14.04
MAINTAINER ibanez.j@gmail.com

RUN apt-get update
RUN apt-get install -y python-pip python-dev
RUN apt-get install -y gunicorn
RUN apt-get install -y libmysqlclient-dev
RUN pip install flask
RUN pip install flask-mysql

#DEVEL
RUN apt-get install -y git nano wget 

RUN mkdir -p /home/ubuntu/worker
WORKDIR /home/ubuntu/worker


ADD * ./

EXPOSE 8000
#ENTRYPOINT ["./run.sh"]
