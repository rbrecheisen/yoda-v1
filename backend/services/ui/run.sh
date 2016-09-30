#!/usr/bin/env sh

echo "window.environ = {};" >> /usr/local/nginx/html/js/environ.js
echo "window.environ.UI_SERVICE_HOST = '${UI_SERVICE_HOST}';" >> /usr/local/nginx/html/js/environ.js
echo "window.environ.UI_SERVICE_PORT = '${UI_SERVICE_PORT}';" >> /usr/local/nginx/html/js/environ.js

sed -i "s/AUTH_SERVICE_HOST/${AUTH_SERVICE_HOST}/" /usr/local/nginx/conf/nginx.conf
sed -i "s/AUTH_SERVICE_PORT/${AUTH_SERVICE_PORT}/" /usr/local/nginx/conf/nginx.conf
sed -i "s/COMPUTE_SERVICE_HOST/${COMPUTE_SERVICE_HOST}/" /usr/local/nginx/conf/nginx.conf
sed -i "s/COMPUTE_SERVICE_PORT/${COMPUTE_SERVICE_PORT}/" /usr/local/nginx/conf/nginx.conf
sed -i "s/STORAGE_SERVICE_HOST/${STORAGE_SERVICE_HOST}/" /usr/local/nginx/conf/nginx.conf
sed -i "s/STORAGE_SERVICE_PORT/${STORAGE_SERVICE_PORT}/" /usr/local/nginx/conf/nginx.conf

nginx
