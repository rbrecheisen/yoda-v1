FROM brecheisen/base:v1

MAINTAINER Ralph Brecheisen <ralph.brecheisen@gmail.com>

COPY requirements.txt /tmp/requirements.txt
COPY service /var/www/backend/service
COPY run.sh /var/www/backend/run.sh
COPY run_worker.sh /var/www/backend/run_worker.sh

RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

WORKDIR /var/www/backend

CMD ["./run.sh"]