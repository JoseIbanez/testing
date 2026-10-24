# syntax=docker/dockerfile:1
FROM --platform=linux/amd64 ubuntu:jammy

#     DOWNLOAD_URL="https://download.acestream.media/linux/acestream_3.2.3_ubuntu_18.04_x86_64_py3.8.tar.gz" \
#     CHECKSUM="bf45376f1f28aaff7d9849ff991bf34a6b9a65542460a2344a8826126c33727d"
ENV LC_ALL="C.UTF-8" \
    LANG="C.UTF-8" \
    DOWNLOAD_URL="https://download.acestream.media/linux/acestream_3.2.11_ubuntu_22.04_x86_64_py3.10.tar.gz" \
    CHECKSUM="9b6bbd76a55e5a434641afae3b9cf8e6154ce1cf392152ec3aed5ac265432b2e"

# Install system packages.
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked\
    --mount=type=cache,target=/var/lib/apt,sharing=locked\
    --mount=type=tmpfs,target=/tmp\
    set -ex;\
    apt-get update -y;\
    apt-get install -yq --no-install-recommends ca-certificates python3.10 libpython3.10 python3-pip \
                    wget ffmpeg supervisor;\
    mkdir -p /opt/acestream;\
    wget --no-verbose --output-document /opt/acestream/acestream.tgz $DOWNLOAD_URL;\
    echo "$CHECKSUM /opt/acestream/acestream.tgz" | sha256sum --check;\
    tar --extract --gzip --directory /opt/acestream --file /opt/acestream/acestream.tgz;\
    rm /opt/acestream/acestream.tgz;\
    python3 -m pip install -r /opt/acestream/requirements.txt;\
    /opt/acestream/start-engine --version;

COPY acestream.conf /opt/acestream/acestream.conf

# Prep dir serving m3u8 files.
RUN mkdir -p /acelink
RUN mkdir -p /mnt/hls
RUN mkdir -p /var/log/supervisor/conf.d/

COPY internal-hls.sh /acelink/
COPY entrypoint.sh /acelink/
COPY acestream-srv.conf /etc/supervisor/conf.d/acestream.conf


EXPOSE 6878
EXPOSE 8621

ENTRYPOINT ["/acelink/entrypoint.sh"]
HEALTHCHECK CMD wget -q -t1 -O- 'http://127.0.0.1:6878/webui/api/service?method=get_version' | grep '"error": null'
