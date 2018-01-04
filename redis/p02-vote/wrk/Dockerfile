FROM python:2.7-alpine
LABEL maintainer="ibanez.j@gmail.com"

# update source
RUN apk update && \
	pip install Flask gunicorn redis && \
	rm -rf /var/cache/apk/* 

COPY *.py run.sh /home/

WORKDIR /home/


EXPOSE 8000
CMD ["./run.sh"]
