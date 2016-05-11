FROM ubuntu
RUN apt-get update
RUN apt-get install -y python-pip python-dev
RUN apt-get install -y gunicorn
RUN pip install flask
RUN apt-get install -y git nano

RUN mkdir -p /home/ubuntu
WORKDIR /home/ubuntu
RUN git clone https://github.com/JoseIbanez/testing.git

WORKDIR /home/ubuntu/testing/flask/proj03/worker
ADD run.sh .

EXPOSE 8000
ENTRYPOINT ["./run.sh"]
