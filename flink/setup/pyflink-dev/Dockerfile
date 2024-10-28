FROM flink:latest

# install python3 and pip3
RUN apt-get update -y && \
apt-get install -y python3.11 python3-pip python3.11-dev && rm -rf /var/lib/apt/lists/*
RUN ln -s /usr/bin/python3.11 /usr/bin/python

# install PyFlink
#COPY apache-flink*.tar.gz /
#RUN pip3 install /apache-flink-libraries*.tar.gz && pip3 install /apache-flink*.tar.gz
#RUN pip3 install apache-flink-libraries
RUN python -m pip install apache-flink

