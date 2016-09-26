FROM ubuntu:14.04
MAINTAINER ibanez.j@gmail.com

RUN apt-get update
RUN apt-get install -y python-pip python-dev python-redis gunicorn
RUN pip install flask

#DEVEL
#RUN apt-get install -y nano wget

RUN mkdir -p /home/ubuntu/worker
WORKDIR /home/ubuntu/worker


ADD * ./


EXPOSE 8000
#ENTRYPOINT ["./p07.py"]
CMD ["/home/ubuntu/worker/run.sh"]
