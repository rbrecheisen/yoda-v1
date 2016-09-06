#!/usr/bin/env sh

# Generate env.js file that contains some environment variables
echo "(function (window) {" > /usr/share/nginx/html/js/env.js
echo "    window.environment = window.environment || {};" >> /usr/share/nginx/html/js/env.js
echo "    window.environment.UI_SERVICE_HOST = '${UI_SERVICE_HOST}';" >> /usr/share/nginx/html/js/env.js
echo "    window.environment.UI_SERVICE_PORT = '${UI_SERVICE_PORT}';" >> /usr/share/nginx/html/js/env.js
echo "}(this));" >> /usr/share/nginx/html/js/env.js

# Start Nginx
nginx
