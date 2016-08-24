import base64
import os
import requests
from functools import wraps
from flask import request, g
from lib.util import get_correlation_id


# ----------------------------------------------------------------------------------------------------------------------
def encode(username, password='unused'):
    return base64.b64encode('{}:{}'.format(username, password))


# ----------------------------------------------------------------------------------------------------------------------
def login_header(username, password):
    return {'Authorization': 'Basic {}'.format(encode(username, password))}


# ----------------------------------------------------------------------------------------------------------------------
def token_header(token):
    return {'Authorization': 'Basic {}'.format(encode(token))}


# ----------------------------------------------------------------------------------------------------------------------
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not getattr(f, 'token_required', True):
            return f(*args, **kwargs)
        auth = request.authorization
        if auth is None:
            raise RuntimeError('Missing authorization header')
        headers = {
            'Authorization': 'Basic {}'.format(base64.b64encode('{}:unused'.format(auth.username))),
            'X-Correlation-ID': get_correlation_id()}
        auth_uri = 'http://{}:{}/token-checks'.format(os.getenv('AUTH_SERVICE_HOST'), os.getenv('AUTH_SERVICE_PORT'))
        print('token_required: {}'.format(auth_uri))
        response = requests.post(auth_uri, headers=headers)
        if response.status_code != 201:
            raise RuntimeError('Authentication failed ({})'.format(response.json()))
        g.current_user = response.json()['user']
        return f(*args, **kwargs)
    return decorated
