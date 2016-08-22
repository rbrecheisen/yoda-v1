FROM python:2.7

MAINTAINER Ralph Brecheisen <ralph.brecheisen@gmail.com>

COPY lib /var/www/backend/lib
COPY requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

#FROM alpine:latest
#
## https://github.com/jfloff/alpine-python/blob/master/2.7/Dockerfile
#
#RUN echo "@testing http://dl-4.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories \
#  && apk add --update \
#              musl \
#              musl-dev \
#              build-base \
#              linux-headers \
#              bash \
#              git \
#              python \
#              python-dev \
#              py-pip \
#  && pip install --upgrade pip \
#  && rm /var/cache/apk/*
#
#RUN cd /usr/bin \
#  && ln -sf easy_install-2.7 easy_install \
#  && ln -sf python2.7 python \
#  && ln -sf python2.7-config python-config \
#  && ln -sf pip2.7 pip
#
#COPY lib /var/www/backend/lib
#COPY requirements.txt /tmp
#
#RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt
