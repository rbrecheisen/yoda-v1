import base64
import os
import requests
from functools import wraps
from flask import request, g
from lib.util import get_correlation_id, service_uri


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
            return {'message': 'Missing authorization header'}, 403
        headers = token_header(auth.username)
        headers.update({
            'X-Correlation-ID': get_correlation_id()})
        print('Sending authentication request to auth service...')
        response = requests.post('{}/token-checks'.format(service_uri('auth')), headers=headers)
        if response.status_code != 201:
            return {'message': 'Authentication failed ({})'.format(response.json())}, 403
        g.current_user = response.json()['user']
        return f(*args, **kwargs)
    return decorated
