import os
import json
import base64
import requests
import random
import string
import logging
from flask import Flask, make_response, request
from flask_restful import Api, Resource

formatter = logging.Formatter(
    '%(asctime)s - %(name)s:%(lineno)s - [%(levelname)s] %(funcName)s() %(message)s')
logger_handler = logging.StreamHandler()
logger_handler.setLevel(logging.DEBUG)
logger_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logger_handler)
logger = logging.getLogger(__name__)

app = Flask(__name__)

if os.getenv('STORAGE_SERVICE_SETTINGS', None) is not None:
    app.config.from_envvar('STORAGE_SERVICE_SETTINGS')
else:
    pass


def get_headers(token, correlation_id):
    return {
        'Authorization': 'Basic {}'.format(base64.b64encode('{}:unused'.format(token))),
        'X-Correlation-ID': correlation_id,
    }


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
            'service': 'storage',
            'resources': {
                'tokens': {},
                'token-checks': {},
            }
        }


class FilesResource(Resource):
    def post(self):
        correlation_id = get_correlation_id(request)
        logging.info('{} calling files resource'.format(correlation_id))
        auth = request.authorization
        if auth is None:
            logging.info('{} missing token'.format(correlation_id))
            return {'message': 'Missing token'}, 403
        logging.info('{} calling auth service for authentication'.format(correlation_id))
        uri = 'http://{}:{}/token-checks'.format(os.getenv('AUTH_SERVICE_HOST'), os.getenv('AUTH_SERVICE_PORT'))
        response = requests.post(uri, headers=get_headers(auth.username, correlation_id))
        if response.status_code != 201:
            logging.info('{} authentication failed'.format(correlation_id))
            return {'message': 'POST /files not permitted ({})'.format(response.json())}, 403
        logging.info('{} authentication succeeded, uploading file'.format(correlation_id))
        logging.info('{} file uploaded'.format(correlation_id))
        return {'files': []}, 201


api = Api(app)
api.add_resource(RootResource, '/')
api.add_resource(FilesResource, '/files')


@api.representation('application/json')
def output_json(data, code, headers=None):
    response = make_response(json.dumps(data), code)
    response.headers.extend(headers or {})
    return response


if __name__ == '__main__':
    init_env()
    host = os.getenv('STORAGE_SERVICE_HOST')
    port = os.getenv('STORAGE_SERVICE_PORT')
    port = int(port)
    app.run(host=host, port=port)
