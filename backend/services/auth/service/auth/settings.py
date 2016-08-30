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

SECRET_KEY = os.urandom(64)
ROOT_USERNAME = 'root'
ROOT_PASSWORD = 'secret'
ROOT_EMAIL = 'root@yoda.com'
PASSWORD_SCHEMES = ['pbkdf2_sha512']

USERS = [
    {
        'username': 'ralph',
        'password': 'secret',
        'email': 'ralph@yoda.com',
        'is_admin': True,
    },
    {
        'username': 'quentin',
        'password': 'secret',
        'email': 'quentin@yoda.com',
        'is_admin': True,
    },
    {
        'username': 'johnny',
        'password': 'secret',
        'email': 'johnny@yoda.com',
        'is_admin': False,
    },
    {
        'username': 'worker',
        'password': 'secret',
        'email': 'worker@yoda.com',
        'is_admin': False,
    }
]
