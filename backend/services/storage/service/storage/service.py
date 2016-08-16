import os
import json
from flask import Flask, make_response
from flask_restful import Api, Resource
from lib.util import init_env, token_required
from lib.resource import BaseResource

app = Flask(__name__)

if os.getenv('STORAGE_SERVICE_SETTINGS', None) is not None:
    app.config.from_envvar('STORAGE_SERVICE_SETTINGS')
else:
    pass

print(app.config)


class RootResource(Resource):
    def get(self):
        return {
            'service': 'storage',
            'resources': {
                'files': {},
            }
        }


class FilesResource(BaseResource):
    @token_required
    def post(self):
        self.log_info('Authentication succeeded, uploading file')
        self.log_info('File uploaded')
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
