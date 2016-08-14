import os
import json
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
        auth = request.authorization
        if auth is None:
            return {'message': 'Missing user credentials'}, 403
        user = find_user(auth.username)
        if user is None:
            return {'message': 'User not found'}, 403
        if user['password'] != auth.password:
            return {'message': 'Invalid password'}, 403
        token = create_token(user)
        return {'token': token}, 201


class TokenChecksResource(Resource):
    def post(self):
        data = request.get_json()
        if 'token' not in data:
            return {'message': 'Missing token'}
        user = check_token(data['token'])
        if user is None:
            return {'message': 'Invalid token or user not found'}, 403
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
