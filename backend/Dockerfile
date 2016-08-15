FROM python:2.7

MAINTAINER Ralph Brecheisen <ralph.brecheisen@gmail.com>

COPY lib /var/www/backend/lib

COPY requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt
