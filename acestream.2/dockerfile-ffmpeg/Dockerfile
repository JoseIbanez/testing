FROM acelink

# Install system packages

RUN set -ex && \
    apt-get update && \
    apt-get install -yq --no-install-recommends \
        software-properties-common \
        iproute2 \
        ffmpeg \
        supervisor && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /var/cache/*



RUN mkdir -p /mnt/hls
RUN mkdir -p /acelink
RUN mkdir -p /var/log/supervisor/conf.d/

COPY  * /acelink/
COPY ./supervisor.conf /etc/supervisor/conf.d/acestream.conf
#COPY ffmpeg.conf    /etc/supervisor/conf.d/ffmpeg.conf

ENTRYPOINT ["/acelink/entrypoint.sh"]

