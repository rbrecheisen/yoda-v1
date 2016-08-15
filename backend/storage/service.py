import os
import json
import requests
import logging
from flask import Flask, make_response, request
from flask_restful import Api, Resource
from backend.lib import get_correlation_id, get_headers, init_env

LOG = logging.getLogger(__name__)

app = Flask(__name__)

if os.getenv('STORAGE_SERVICE_SETTINGS', None) is not None:
    app.config.from_envvar('STORAGE_SERVICE_SETTINGS')
else:
    pass


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
        LOG.info('{} calling files resource'.format(correlation_id))
        auth = request.authorization
        if auth is None:
            LOG.info('{} missing token'.format(correlation_id))
            return {'message': 'Missing token'}, 403
        LOG.info('{} calling auth service for authentication'.format(correlation_id))
        uri = 'http://{}:{}/token-checks'.format(os.getenv('AUTH_SERVICE_HOST'), os.getenv('AUTH_SERVICE_PORT'))
        response = requests.post(uri, headers=get_headers(auth.username, correlation_id))
        if response.status_code != 201:
            LOG.info('{} authentication failed'.format(correlation_id))
            return {'message': 'POST /files not permitted ({})'.format(response.json())}, 403
        LOG.info('{} authentication succeeded, uploading file'.format(correlation_id))
        LOG.info('{} file uploaded'.format(correlation_id))
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
