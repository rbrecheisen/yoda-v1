import os

SECRET = os.urandom(64)

USERS = [
    {
        'username': 'ralph',
        'password': 'secret',
        'admin': True,
    },
]
