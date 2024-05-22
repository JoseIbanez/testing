FROM acelink

# Install system packages

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked\
    --mount=type=cache,target=/var/lib/apt,sharing=locked\
    --mount=type=tmpfs,target=/tmp\
    set -ex && \
    apt-get update && \
    apt-get install -yq --no-install-recommends \
        software-properties-common \
        iproute2 \
        ffmpeg \
        procps \
        supervisor 


RUN mkdir -p /mnt/hls
RUN mkdir -p /acelink
RUN mkdir -p /var/log/supervisor/conf.d/

COPY  * /acelink/
COPY ./supervisor.conf /etc/supervisor/conf.d/acestream.conf
#COPY ffmpeg.conf    /etc/supervisor/conf.d/ffmpeg.conf

ENTRYPOINT ["/acelink/entrypoint.sh"]

