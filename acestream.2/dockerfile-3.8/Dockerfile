# Use debian buster (10)
FROM python:3.8-slim-buster AS build

# https://docs.acestream.net/products/#linux
ENV ACE_VER 3.1.75rc4
ENV ACE_SRC "https://download.acestream.media/linux/acestream_${ACE_VER}_ubuntu_18.04_x86_64_py3.8.tar.gz"
ENV ACE_DIR /acestream

# Install build dependencies
RUN apt-get -q update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libsqlite3-dev \
        ca-certificates \
        curl


# Install dependencies and acestream engine
RUN mkdir -p $ACE_DIR && \
    cd $ACE_DIR && \
    curl $ACE_SRC | tar xzf -  && \
    pip install -r requirements.txt 


# Use debian bullseye (11)
FROM python:3.8-slim-buster AS main

ENV ACE_DIR /acestream
ENV PATH $ACE_DIR:$PATH

# Install dependencies and acestream engine
RUN apt-get -q update && \
    apt-get install -y --no-install-recommends \
        libsqlite3-0 \
        netcat wget \
        net-tools \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* \
           /var/cache/*

COPY --from=build /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=build $ACE_DIR $ACE_DIR


# Copy entrypoint scripts
COPY ./print_token.py /
COPY ./start.sh /
COPY ./acestream.conf /acestream/acestream.conf

# Make entrypoint executable
RUN chmod +x /start.sh

# Let docker know how to test container health
HEALTHCHECK CMD wget -q -t1 -O- 'http://127.0.0.1:6878/webui/api/service?method=get_version' | grep '"error": null'

# Start acestream (client console only)
ENTRYPOINT [ "/start.sh" ]

EXPOSE 6878
EXPOSE 8621