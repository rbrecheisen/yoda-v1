import os
import json
import base64
import requests
import logging
from flask import Flask, make_response, request
from flask_restful import Api, Resource

formatter = logging.Formatter(
    '%(asctime)s - %(name)s:%(lineno)s - [%(levelname)s] %(funcName)s() %(message)s')
logger_handler = logging.StreamHandler()
logger_handler.setLevel(logging.DEBUG)
logger_handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logger_handler)

app = Flask(__name__)

if os.getenv('STORAGE_SERVICE_SETTINGS', None) is not None:
    app.config.from_envvar('STORAGE_SERVICE_SETTINGS')
else:
    pass


def token_header(token):
    return {'Authorization': 'Basic {}'.format(base64.b64encode('{}:unused'.format(token)))}


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
        auth = request.authorization
        uri = 'http://{}:{}/token-checks'.format(os.getenv('AUTH_SERVICE_HOST'), os.getenv('AUTH_SERVICE_PORT'))
        response = requests.post(uri, json={'token': auth.username})
        if response.status_code != 201:
            return {'message': 'POST /files not permitted ({})'.format(response.json())}, 403
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
