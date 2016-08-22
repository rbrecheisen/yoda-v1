FROM ubuntu:14.04

MAINTAINER Ralph Brecheisen <ralph.brecheisen@gmail.com>

ENV NGINX_VERSION 1.10.1
ENV LD_LIBRARY_PATH /usr/local/lib

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y build-essential autoconf openssl libssl-dev \
    libpcre3 libpcre3-dev zlib1g zlib1g-dev wget git curl \
    && mkdir -p /tmp/src \
	 && cd /tmp/src \
    && git clone http://luajit.org/git/luajit-2.0.git \
    && cd luajit-2.0 \
    && make \
    && make install \
    && cd .. \
    && wget http://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz \
    && tar -zxf nginx-${NGINX_VERSION}.tar.gz \
    && rm nginx-${NGINX_VERSION}.tar.gz \
    && git clone https://github.com/simpl/ngx_devel_kit.git \
    && git clone https://github.com/openresty/lua-nginx-module.git \
    # && git clone https://github.com/pgaertig/nginx-big-upload.git \
    && cd nginx-${NGINX_VERSION} \
    && ./configure --prefix=/usr/local/nginx \
            --with-http_gzip_static_module \
            --with-http_ssl_module \
            --with-http_stub_status_module \
    		--with-http_auth_request_module \
            --http-log-path=/var/log/nginx/access.log \
            --error-log-path=/var/log/nginx/error.log \
            --sbin-path=/usr/local/sbin/nginx \
            --add-module=../ngx_devel_kit \
            --add-module=../lua-nginx-module \
    && make \
    && make install \
    && cd .. \
    && mkdir -p /usr/local/nginx/modules \
    # && mv ngx-big-upload /usr/local/ngx/modules \
	&& ln -sf /dev/stdout /var/log/nginx/access.log \
	&& ln -sf /dev/stderr /var/log/nginx/error.log \
	&& mkdir -p /mnt/shared/files \
	&& rm -rf /tmp/src

EXPOSE 80 443

CMD ["nginx"]

#FROM gliderlabs/alpine:3.3
#
#MAINTAINER Ralph Brecheisen <ralph.brecheisen@gmail.com>
#
#ENV NGINX_VERSION 1.10.1
#ENV LD_LIBRARY_PATH /usr/local/lib
#
#RUN apk --update add openssl-dev pcre zlib pcre-dev zlib-dev wget curl build-base perl perl-dev git vim bash \
#    && mkdir -p /tmp/src \
#	&& cd /tmp/src \
#    && git clone http://luajit.org/git/luajit-2.0.git \
#    && cd luajit-2.0 \
#    && make \
#    && make install \
#    && cd .. \
#    && wget http://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz \
#    && tar -zxf nginx-${NGINX_VERSION}.tar.gz \
#    && rm nginx-${NGINX_VERSION}.tar.gz \
#    && git clone https://github.com/simpl/ngx_devel_kit.git \
#    && git clone https://github.com/openresty/lua-nginx-module.git \
#    # && git clone https://github.com/pgaertig/nginx-big-upload.git \
#    && cd nginx-${NGINX_VERSION} \
#    && ./configure --prefix=/usr/local/nginx \
#            --with-http_gzip_static_module \
#            --with-http_ssl_module \
#            --with-http_stub_status_module \
#    		--with-http_auth_request_module \
#            --http-log-path=/var/log/nginx/access.log \
#            --error-log-path=/var/log/nginx/error.log \
#            --sbin-path=/usr/local/sbin/nginx \
#            --add-module=../ngx_devel_kit \
#            --add-module=../lua-nginx-module \
#    && make \
#    && make install \
#    && cd .. \
#    && mkdir -p /usr/local/nginx/modules \
#    # && mv ngx-big-upload /usr/local/ngx/modules \
#	&& ln -sf /dev/stdout /var/log/nginx/access.log \
#	&& ln -sf /dev/stderr /var/log/nginx/error.log \
#	&& mkdir -p /mnt/shared/files \
#	&& apk del openssl-dev pcre-dev zlib-dev wget git \
#	&& rm -rf /tmp/src \
#	&& rm -rf /var/cache/apk/*
#
#EXPOSE 80 443
#
#CMD ["nginx"]
