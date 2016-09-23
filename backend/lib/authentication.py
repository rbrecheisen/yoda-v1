import base64
import requests
from functools import wraps
from flask import request, g
from lib.util import uri


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
        # Check cache for a token. If it's not there request one from the auth service.
        token = g.cache.get('token')
        if token is None:
            print('Could not find token in cache')
            # Get username and password from service settings
            username = g.config['SERVICE_USERNAME']
            password = g.config['SERVICE_PASSWORD']
            # Request new access token
            print('Requesting new token for user {}'.format(username))
            response = requests.post(uri('auth', '/tokens'), headers=login_header(username, password))
            if response.status_code != 201:
                return {'message': 'Authentication failed ({})'.format(response.json())}, 403
            # Get token and store it in cache for future use
            token = response.json()['token']
            print('Received token {}, storing in cache'.format(token))
            g.cache.set('token', token)
        # Send request to auth service to verify the client token
        response = requests.post(
            uri('auth', '/token-checks'), json={'token': auth.username}, headers=token_header(token))
        if response.status_code != 201:
            return {'message': 'Authentication failed ({})'.format(response.json())}, 403
        # Token verification was successful
        g.current_user = response.json()['user']
        return f(*args, **kwargs)
    return decorated
