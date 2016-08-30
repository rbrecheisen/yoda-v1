FROM brecheisen/compute-base:v1

MAINTAINER Ralph Brecheisen <ralph.brecheisen@gmail.com>

COPY service /var/www/backend/service
COPY run.sh /var/www/backend/run.sh

WORKDIR /var/www/backend

CMD ["./run.sh"]