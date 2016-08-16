import json
import os
from flask import Flask, request, make_response
from flask_restful import Api
from jose import jwt
from lib.util import init_env
from lib.resource import BaseResource

app = Flask(__name__)

if os.getenv('AUTH_SERVICE_SETTINGS', None) is None:
    os.environ['AUTH_SERVICE_SETTINGS'] = os.path.abspath('service/auth/service_settings.py')
app.config.from_envvar('AUTH_SERVICE_SETTINGS')
print(app.config)


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


class RootResource(BaseResource):
    def get(self):
        return {
            'service': 'auth',
            'resources': {
                'tokens': {},
                'token-checks': {},
            }
        }


class TokensResource(BaseResource):
    def post(self):
        auth = request.authorization
        if auth is None:
            return self.error_response('Missing user credentials', 403)
        user = find_user(auth.username)
        if user is None:
            return self.error_response('Unknown user', 403)
        if user['password'] != auth.password:
            return self.error_response('Invalid password', 403)
        token = create_token(user)
        self.log_info('Token created')
        return self.response({'token': token}, 201)


class TokenChecksResource(BaseResource):
    def post(self):
        auth = request.authorization
        if auth is None:
            return self.error_response('Missing token', 403)
        user = check_token(auth.username)
        if user is None:
            return self.error_response('Invalid token or user not found', 403)
        self.log_info('Token accepted')
        return self.response({'user': user}, 201)


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
