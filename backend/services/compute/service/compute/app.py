import os
import json
from flask import Flask, make_response
from flask_restful import Api
from lib.util import init_env, token_required
from lib.resource import BaseResource
from service.compute.worker import run_task

app = Flask(__name__)

if os.getenv('COMPUTE_SERVICE_SETTINGS', None) is None:
    os.environ['COMPUTE_SERVICE_SETTINGS'] = os.path.abspath('service/compute/settings.py')
app.config.from_envvar('COMPUTE_SERVICE_SETTINGS')
print(app.config)


class RootResource(BaseResource):
    def get(self):
        return self.response({
            'service': 'compute',
            'resources': {
                'tasks': {},
            }
        }, 200)


class TasksResource(BaseResource):

    @token_required
    def post(self):
        run_task.apply_async()
        return self.response({}, 201)


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
