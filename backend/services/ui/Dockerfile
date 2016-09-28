FROM brecheisen/nginx-base:v1

MAINTAINER Ralph Brecheisen <ralph.brecheisen@gmail.com>

COPY static /usr/share/nginx/html
COPY nginx.conf.template /etc/nginx/nginx.conf.template
COPY run.sh /usr/share/nginx/run.sh

WORKDIR /usr/share/nginx

EXPOSE 80 443

CMD ["./run.sh"]