#!/usr/bin/env bash

sed -i "s/STORAGE_APP_SERVICE_HOST/${STORAGE_APP_SERVICE_HOST}/" /usr/local/nginx/conf/nginx.conf
sed -i "s/STORAGE_APP_SERVICE_PORT/${STORAGE_APP_SERVICE_PORT}/" /usr/local/nginx/conf/nginx.conf

nginx
