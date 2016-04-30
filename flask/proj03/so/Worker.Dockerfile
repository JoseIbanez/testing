FROM ubuntu
RUN apt-get update
RUN apt-get install -y python-pip python-dev
RUN apt-get install -y gunicorn
RUN pip install flask
RUN apt-get install -y git nano
RUN mkdir -p /home/ubuntu
