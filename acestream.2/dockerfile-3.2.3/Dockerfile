# syntax=docker/dockerfile:1
FROM --platform=linux/amd64 ubuntu:focal

ENV LC_ALL="C.UTF-8" \
    LANG="C.UTF-8" \
    DOWNLOAD_URL="https://download.acestream.media/linux/acestream_3.2.3_ubuntu_18.04_x86_64_py3.8.tar.gz" \
    CHECKSUM="bf45376f1f28aaff7d9849ff991bf34a6b9a65542460a2344a8826126c33727d"

# Install system packages.
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked\
    --mount=type=cache,target=/var/lib/apt,sharing=locked\
    --mount=type=tmpfs,target=/tmp\
    set -ex && \
    apt-get update && \
    apt-get install -yq --no-install-recommends \
        ca-certificates \
        python3.8 \
        libpython3.8 \
        python3-pip \
        wget

# Download acestream
RUN mkdir -p /opt/acestream && \
    wget --no-verbose --output-document /tmp/acestream.tgz $DOWNLOAD_URL && \
    echo "$CHECKSUM /tmp/acestream.tgz" | sha256sum --check && \
    tar --extract --gzip --directory /opt/acestream --file /tmp/acestream.tgz && \
    rm /tmp/acestream.tgz

# Install python requirements
RUN python3 -m pip install -r /opt/acestream/requirements.txt

# Test acesstream
RUN /opt/acestream/start-engine --version

COPY ./start.sh /start.sh
COPY acestream.conf /opt/acestream/acestream.conf

# Prep dir serving m3u8 files.
RUN mkdir /acelink

EXPOSE 6878
EXPOSE 8621

ENTRYPOINT ["/opt/acestream/start-engine", "@/opt/acestream/acestream.conf"]
HEALTHCHECK CMD wget -q -t1 -O- 'http://127.0.0.1:6878/webui/api/service?method=get_version' | grep '"error": null'