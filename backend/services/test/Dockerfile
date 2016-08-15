FROM brecheisen/base:v1

MAINTAINER Ralph Brecheisen <ralph.brecheisen@gmail.com>

COPY service /var/www/backend/service
COPY requirements.txt /tmp/requirements.txt
COPY run.sh /var/www/backend/run.sh

RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

ENV AUTH_SERVICE_SETTINGS /var/www/backend/service/test/service_settings.py

WORKDIR /var/www/backend

CMD ["./run.sh"]