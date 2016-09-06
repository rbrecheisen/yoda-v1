FROM nginx:1.10-alpine

MAINTAINER Ralph Brecheisen <ralph.brecheisen@gmail.com>

COPY static /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80 443

CMD ["nginx"]