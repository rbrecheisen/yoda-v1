FROM brecheisen/nginx-base:v1

MAINTAINER Ralph Brecheisen <ralph.brecheisen@gmail.com>

COPY nginx-big-upload /usr/local/nginx/modules/nginx-big-upload
COPY nginx.conf.template /usr/local/nginx/conf/nginx.conf.template
COPY run.sh /usr/local/nginx/run.sh

WORKDIR /usr/local/nginx

CMD ["./run.sh"]