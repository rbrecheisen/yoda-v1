#!/usr/bin/env sh

echo "window.environ = {};" >> /usr/share/nginx/html/js/env.js
echo "window.environ.UI_SERVICE_HOST = '${UI_SERVICE_HOST}';" >> /usr/share/nginx/html/js/env.js
echo "window.environ.UI_SERVICE_PORT = '${UI_SERVICE_PORT}';" >> /usr/share/nginx/html/js/env.js

nginx
