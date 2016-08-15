import json
import logging
import os
from flask import Flask, request, make_response
from flask_restful import Api, Resource
from jose import jwt
from lib.util import get_correlation_id, init_env

LOG = logging.getLogger(__name__)

app = Flask(__name__)

if os.getenv('AUTH_SERVICE_SETTINGS', None) is not None:
    app.config.from_envvar('AUTH_SERVICE_SETTINGS')
else:
    app.config['SECRET'] = os.urandom(64)
    app.config['USERS'] = []
    app.config['USERS'].append({
        'username': 'ralph',
        'password': 'secret',
        'admin': True,
    })

for key in app.config.keys():
    print(app.config[key])


def find_user(username):
    for user in app.config['USERS']:
        if user['username'] == username:
            return user
    return None


def create_token(user):
    return jwt.encode(user, app.config['SECRET'], algorithm='HS256')


def check_token(token):
    data = jwt.decode(token, app.config['SECRET'], algorithms=['HS256'])
    return find_user(data['username'])


class RootResource(Resource):
    def get(self):
        return {
            'service': 'auth',
            'resources': {
                'tokens': {},
                'token-checks': {},
            }
        }


class TokensResource(Resource):
    def post(self):
        correlation_id = get_correlation_id(request)
        LOG.info('{} calling tokens resource'.format(correlation_id))
        auth = request.authorization
        if auth is None:
            LOG.info('{} missing user credentials'.format(correlation_id))
            return {'message': 'Missing user credentials'}, 403
        user = find_user(auth.username)
        if user is None:
            LOG.info('{} unknown user'.format(correlation_id))
            return {'message': 'User not found'}, 403
        if user['password'] != auth.password:
            LOG.info('{} invalid password'.format(correlation_id))
            return {'message': 'Invalid password'}, 403
        token = create_token(user)
        LOG.info('{} token created'.format(correlation_id))
        return {'token': token}, 201


class TokenChecksResource(Resource):
    def post(self):
        correlation_id = get_correlation_id(request)
        LOG.info('{} calling token checks resource'.format(correlation_id))
        auth = request.authorization
        if auth is None:
            LOG.info('{} missing token'.format(correlation_id))
            return {'message': 'Missing token'}
        user = check_token(auth.username)
        if user is None:
            LOG.info('{} invalid token or unknown user'.format(correlation_id))
            return {'message': 'Invalid token or user not found'}, 403
        LOG.info('{} token ok'.format(correlation_id))
        return {'user': user}, 201


api = Api(app)
api.add_resource(RootResource, '/')
api.add_resource(TokensResource, '/tokens')
api.add_resource(TokenChecksResource, '/token-checks')


@api.representation('application/json')
def output_json(data, code, headers=None):
    response = make_response(json.dumps(data), code)
    response.headers.extend(headers or {})
    return response


if __name__ == '__main__':
    init_env()
    host = os.getenv('AUTH_SERVICE_HOST')
    port = os.getenv('AUTH_SERVICE_PORT')
    port = int(port)
    app.run(host=host, port=port)
