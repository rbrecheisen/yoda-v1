#!/bin/bash

#docker run -d --name redis -h redis -p 6379:6379 redis:3.2.3

docker run -d --name worker -h worker \
    -v $(pwd)/backend/lib:/var/www/backend/lib \
    -v $(pwd)/backend/services/compute/service:/var/www/backend/service \
    -v $(pwd)/backend/services/compute/run_worker.sh:/var/www/backend/run_worker.sh \
    --env C_FORCE_ROOT=1 \
    --env BROKER_URL=redis://192.68.99.100:6379/0 \
    --env CELERY_TASK_SERIALIZER=json \
    brecheisen/compute:v1 ./run_worker.sh
