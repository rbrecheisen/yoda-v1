#!/bin/bash

docker run -d --name redis -h redis redis:3

docker run -it --rm \
    -v $(pwd)/backend/lib:/var/www/backend/lib \
    -v $(pwd)/backend/services/compute/service:/var/www/backend/service \
    -v $(pwd)/backend/services/compute/run_worker.sh:/var/www/backend/run_worker.sh \
    --env C_FORCE_ROOT=1 \
    brecheisen/compute:v1 ./run_worker.sh
