import os
import random
import string
import base64
import requests
from functools import wraps
from flask import request, g


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


def generate_id(n=16):
    if n <= 8:
        return ''.join(random.sample(string.digits, n))
    k = int(n / 8)
    r = n - 8 * k
    nr = ''
    for i in range(k):
        nr += ''.join(random.sample(string.digits, 8))
    nr += ''.join(random.sample(string.digits, r))
    return nr


def get_correlation_id():
    if 'X-Correlation-ID' in request.headers:
        correlation_id = request.headers['X-Correlation-ID']
    else:
        correlation_id = generate_id(8)
    return correlation_id


def init_env():
    port = 5000
    for service in ['AUTH', 'COMPUTE', 'STORAGE', 'FILE']:
        if os.getenv('{}_SERVICE_HOST'.format(service), None) is None:
            os.environ['{}_SERVICE_HOST'.format(service)] = '0.0.0.0'
            os.environ['{}_SERVICE_PORT'.format(service)] = str(port)
            port += 1
