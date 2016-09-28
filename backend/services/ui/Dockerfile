FROM brecheisen/nginx-base:v1

MAINTAINER Ralph Brecheisen <ralph.brecheisen@gmail.com>

COPY static /usr/local/nginx/html
COPY nginx.conf /usr/local/nginx/conf/nginx.conf
COPY run.sh /usr/local/nginx/run.sh

WORKDIR /usr/local/nginx

EXPOSE 5004

CMD ["./run.sh"]