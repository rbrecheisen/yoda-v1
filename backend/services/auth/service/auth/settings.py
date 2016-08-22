import os
import logging

SECRET_KEY = os.urandom(64)

USERS = [
    {
        'username': 'ralph',
        'password': 'secret',
        'admin': True,
    },
]

formatter = logging.Formatter('%(asctime)s - [%(levelname)s] %(message)s')

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
