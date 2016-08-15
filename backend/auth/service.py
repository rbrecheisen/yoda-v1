import os
import json
import string
import random
import base64
import logging
from flask import Flask, request, make_response
from flask_restful import Api, Resource
from jose import jwt

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

formatter = logging.Formatter(
    '%(asctime)s - %(name)s:%(lineno)s - [%(levelname)s] %(funcName)s() %(message)s')
logger_handler = logging.StreamHandler()
logger_handler.setLevel(logging.DEBUG)
logger_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logger_handler)
logger = logging.getLogger(__name__)


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


def get_correlation_id(request):
    if 'X-Correlation-ID' in request.headers:
        correlation_id = request.headers['X-Correlation-ID']
    else:
        correlation_id = generate_id(8)
    return correlation_id


def init_env():
    port = 5000
    for service in ['AUTH', 'COMPUTE', 'STORAGE', 'TEST']:
        if os.getenv('{}_SERVICE_HOST'.format(service), None) is None:
            os.environ['{}_SERVICE_HOST'.format(service)] = '0.0.0.0'
            os.environ['{}_SERVICE_PORT'.format(service)] = str(port)
            port += 1


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
        logging.info('{} calling tokens resource'.format(correlation_id))
        auth = request.authorization
        if auth is None:
            logging.info('{} missing user credentials'.format(correlation_id))
            return {'message': 'Missing user credentials'}, 403
        user = find_user(auth.username)
        if user is None:
            logging.info('{} unknown user'.format(correlation_id))
            return {'message': 'User not found'}, 403
        if user['password'] != auth.password:
            logging.info('{} invalid password'.format(correlation_id))
            return {'message': 'Invalid password'}, 403
        token = create_token(user)
        logging.info('{} token created'.format(correlation_id))
        return {'token': token}, 201


class TokenChecksResource(Resource):
    def post(self):
        correlation_id = get_correlation_id(request)
        logging.info('{} calling token checks resource'.format(correlation_id))
        auth = request.authorization
        if auth is None:
            logging.info('{} missing token'.format(correlation_id))
            return {'message': 'Missing token'}
        user = check_token(auth.username)
        if user is None:
            logging.info('{} invalid token or unknown user'.format(correlation_id))
            return {'message': 'Invalid token or user not found'}, 403
        logging.info('{} token ok'.format(correlation_id))
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
