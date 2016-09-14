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

PASSWORD_SCHEMES = ['pbkdf2_sha512']

USERS = [
    {
        'username': 'ralph',
        'password': 'secret',
        'email': 'ralph@yoda.com',
        'first_name': 'Ralph',
        'last_name': 'Brecheisen',
        'is_superuser': True,
        'is_admin': True,
        'is_active': True,
        'is_visible': True,
    },
    {
        'username': 'quentin',
        'password': 'secret',
        'email': 'quentin@yoda.com',
        'first_name': 'Quentin',
        'last_name': 'Noirhomme',
        'is_superuser': False,
        'is_admin': True,
        'is_active': True,
        'is_visible': True,
    },
    {
        'username': 'armin',
        'password': 'secret',
        'email': 'armin@yoda.com',
        'first_name': 'Armin',
        'last_name': 'Heinecke',
        'is_superuser': False,
        'is_admin': False,
        'is_active': True,
        'is_visible': True,
    },
    {
        'username': 'worker',
        'password': 'secret',
        'email': 'worker@yoda.com',
        'first_name': None,
        'last_name': None,
        'is_superuser': False,
        'is_admin': False,
        'is_active': True,
        'is_visible': False,
    }
]
