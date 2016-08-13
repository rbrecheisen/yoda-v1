FROM brecheisen/base:v1

MAINTAINER Ralph Brecheisen <ralph.brecheisen@gmail.com>

COPY service.py /var/www/backend/service.py
COPY run.sh /var/www/backend/run.sh
COPY settings.py /var/www/backend/settings.py

COPY requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

ENV STORAGE_SERVICE_SETTINGS /var/www/backend/settings.py

WORKDIR /var/www/backend

CMD ["./run.sh"]