FROM python:2.7

MAINTAINER Ralph Brecheisen <ralph.brecheisen@gmail.com>

RUN apt-get update && apt-get install -yy vim curl dnsutils

COPY lib /var/www/backend/lib
COPY requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

WORKDIR /var/www/backend