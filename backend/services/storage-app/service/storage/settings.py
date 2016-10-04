import os
import logging

# ------------------------------------------------------------------------------------------------------------------
# Development settings for environment variables
# ------------------------------------------------------------------------------------------------------------------

if not os.getenv('AUTH_SERVICE_HOST'):
    os.environ['AUTH_SERVICE_HOST'] = '0.0.0.0'
    os.environ['AUTH_SERVICE_PORT'] = '5000'

if not os.getenv('STORAGE_APP_SERVICE_HOST'):
    os.environ['STORAGE_APP_SERVICE_HOST'] = '0.0.0.0'
    os.environ['STORAGE_APP_SERVICE_PORT'] = '5003'

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
# Database settings
# ------------------------------------------------------------------------------------------------------------------

SQLALCHEMY_TRACK_MODIFICATIONS = False

if os.getenv('DB_USER', None) is not None:
    SQLALCHEMY_DATABASE_URI = 'postgres://{}:{}@{}:{}/{}'.format(
        os.getenv('DB_USER'),
        os.getenv('DB_PASS'),
        os.getenv('DB_HOST'),
        os.getenv('DB_PORT'),
        os.getenv('DB_NAME'))
else:
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/yoda.db'


# ------------------------------------------------------------------------------------------------------------------
# Security settings
# ------------------------------------------------------------------------------------------------------------------

SERVICE_USERNAME = 'storage'
SERVICE_PASSWORD = 'secret'

# ------------------------------------------------------------------------------------------------------------------
# Debug settings
# ------------------------------------------------------------------------------------------------------------------

STORAGE_ROOT_DIR = os.getenv('STORAGE_ROOT_DIR')
