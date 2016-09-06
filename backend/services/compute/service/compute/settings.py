import os
import logging

# ------------------------------------------------------------------------------------------------------------------
# Log settings
# ------------------------------------------------------------------------------------------------------------------

formatter = logging.Formatter('%(asctime)s - [%(levelname)s] %(message)s')

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

# ------------------------------------------------------------------------------------------------------------------
# Flask settings
# ------------------------------------------------------------------------------------------------------------------

PROPAGATE_EXCEPTIONS = True
RESTFUL_JSON = {'indent': 2, 'sort_keys': True}

# ------------------------------------------------------------------------------------------------------------------
# Celery settings
# ------------------------------------------------------------------------------------------------------------------

BROKER_URL = os.getenv('BROKER_URL', 'redis://localhost:6379/0')

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
CELERY_CHORD_PROPAGATES = True
CELERY_TASK_DIRS = [
    'service.compute.pipelines.stats.predict',
    'service.compute.pipelines.stats.train',
]

# ------------------------------------------------------------------------------------------------------------------
# Security settings
# ------------------------------------------------------------------------------------------------------------------
WORKER_USERNAME = 'worker'
WORKER_PASSWORD = 'secret'
