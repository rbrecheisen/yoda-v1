import os
import json
from flask import Flask, make_response
from flask_restful import Api, Resource

app = Flask(__name__)

if os.getenv('COMPUTE_SERVICE_SETTINGS', None) is not None:
    app.config.from_envvar('COMPUTE_SERVICE_SETTINGS')
else:
    pass


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
            'service': 'compute',
            'resources': {
                'tasks': {},
            }
        }


class TasksResource(Resource):
    def post(self):
        return {}, 201


api = Api(app)
api.add_resource(RootResource, '/')
api.add_resource(TasksResource, '/tasks')


@api.representation('application/json')
def output_json(data, code, headers=None):
    response = make_response(json.dumps(data), code)
    response.headers.extend(headers or {})
    return response


if __name__ == '__main__':
    init_env()
    host = os.getenv('COMPUTE_SERVICE_HOST')
    port = os.getenv('COMPUTE_SERVICE_PORT')
    port = int(port)
    app.run(host=host, port=port)
