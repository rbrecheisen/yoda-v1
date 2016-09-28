#!/usr/bin/env bash

envsubst < /usr/local/nginx/conf/nginx.conf.template > /usr/local/nginx/conf/nginx.conf

nginx
