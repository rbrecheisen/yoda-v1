import os
import json
from flask import Flask, make_response
from flask_restful import Api, Resource

app = Flask(__name__)

if os.getenv('COMPUTE_SERVICE_SETTINGS', None) is not None:
    app.config.from_envvar('COMPUTE_SERVICE_SETTINGS')
else:
    pass


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
    host = os.getenv('COMPUTE_SERVICE_HOST', '0.0.0.0')
    port = os.getenv('COMPUTE_SERVICE_PORT', '5000')
    port = int(port)
    app.run(host=host, port=port)
