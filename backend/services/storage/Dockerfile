FROM brecheisen/base:v1

MAINTAINER Ralph Brecheisen <ralph.brecheisen@gmail.com>

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt
RUN mkdir -p /var/www/backend

WORKDIR /var/www/backend

CMD ["./run.sh"]