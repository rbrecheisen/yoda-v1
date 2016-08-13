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
        'username': 'admin',
        'password': 'secret',
        'admin': True,
    })


def find_user(username):
    for user in app.config['USERS']:
        if user['username'] == username:
            return user
    return None


def check_token(token):
    data = json.loads(jwt.decode(token, app.config['SECRET'], algorithms=['HS256']))
    user = find_user(data['username'])
    if user is None:
        return user
    return None


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
        token = jwt.encode(json.dumps(user), app.config['SECRET'], algorithm='HS256')
        return {'token': token}, 201


class TokenChecksResource(Resource):
    def post(self):
        auth = request.authorization
        if auth is None:
            return {'message': 'Missing token'}, 403
        user = check_token(auth.username)
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
    host = os.getenv('AUTH_SERVICE_HOST', '0.0.0.0')
    port = os.getenv('AUTH_SERVICE_PORT', '5000')
    port = int(port)
    app.run(host=host, port=port)
