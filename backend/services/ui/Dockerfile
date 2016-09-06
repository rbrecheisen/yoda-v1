FROM nginx:1.10-alpine

MAINTAINER Ralph Brecheisen <ralph.brecheisen@gmail.com>

COPY static /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
COPY run.sh /usr/share/nginx/run.sh

WORKDIR /usr/share/nginx

EXPOSE 80 443

CMD ["./run.sh"]