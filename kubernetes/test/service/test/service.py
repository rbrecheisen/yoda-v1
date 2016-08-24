import os
import sys
import json
from flask import Flask, make_response
from flask_restful import Api
from lib.resources import BaseResource
from tests import TESTS

app = Flask(__name__)

if os.getenv('TEST_SERVICE_SETTINGS', None) is None:
    os.environ['TEST_SERVICE_SETTINGS'] = os.path.abspath('service/test/service_settings.py')
app.config.from_envvar('TEST_SERVICE_SETTINGS')
print(app.config)


def run_tests():
    results = []
    for test in TESTS:
        results.append(test())
    return results


def init_env():
    port = 5000
    for service in ['AUTH', 'COMPUTE', 'STORAGE', 'TEST']:
        if os.getenv('{}_SERVICE_HOST'.format(service), None) is None:
            os.environ['{}_SERVICE_HOST'.format(service)] = '0.0.0.0'
            os.environ['{}_SERVICE_PORT'.format(service)] = str(port)
            port += 1


class RootResource(BaseResource):
    def get(self):
        return {
            'service': 'test',
            'resources': {
                'tests': {},
            }
        }


class TestsResource(BaseResource):
    def get(self):
        return run_tests(), 200


api = Api(app)
api.add_resource(RootResource, '/')
api.add_resource(TestsResource, '/tests')


@api.representation('application/json')
def output_json(data, code, headers=None):
    response = make_response(json.dumps(data), code)
    response.headers.extend(headers or {})
    return response


if __name__ == '__main__':
    init_env()
    if len(sys.argv) == 2 and sys.argv[1] == 'no-server':
        for result in run_tests():
            print(result)
    else:
        host = os.getenv('TEST_SERVICE_HOST')
        port = os.getenv('TEST_SERVICE_PORT')
        port = int(port)
        app.run(host=host, port=port)
