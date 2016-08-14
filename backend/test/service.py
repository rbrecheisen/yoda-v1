import os
import sys
import json
import requests
from flask import Flask, make_response
from flask_restful import Api, Resource

app = Flask(__name__)

if os.getenv('TEST_SERVICE_SETTINGS', None) is not None:
    app.config.from_envvar('TEST_SERVICE_SETTINGS')
else:
    pass


def get_uri(service):
    return 'http://{}:{}'.format(
        os.getenv('{}_SERVICE_HOST'.format(service.upper())),
        os.getenv('{}_SERVICE_PORT'.format(service.upper())))


def test_auth_service():
    response = requests.get(get_uri('auth'))
    result = 'SUCCESS' if response.status_code == 200 else 'FAIL'
    return {'test_auth_service': result}


def test_compute_service():
    response = requests.get(get_uri('compute'))
    result = 'SUCCESS' if response.status_code == 200 else 'FAIL'
    return {'test_compute_service': result}


def test_storage_service():
    response = requests.get(get_uri('storage'))
    result = 'SUCCESS' if response.status_code == 200 else 'FAIL'
    return {'test_storage_service': result}


TESTS = [
    test_auth_service,
    test_compute_service,
    test_storage_service,
]


def run_tests():
    results = []
    for test in TESTS:
        results.append(test())
    return results


def init_env():
    port = 5000
    for service in ['AUTH', 'COMPUTE', 'STORAGE']:
        if os.getenv('{}_SERVICE_HOST'.format(service), None) is None:
            os.environ['{}_SERVICE_HOST'.format(service)] = '0.0.0.0'
            os.environ['{}_SERVICE_PORT'.format(service)] = str(port)
            port += 1


class RootResource(Resource):
    def get(self):
        return {
            'service': 'test',
            'resources': {
                'tests': {},
            }
        }


class TestsResource(Resource):
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
    if len(sys.argv) == 2 and sys.argv[1] == 'no-server':
        init_env()
        for result in run_tests():
            print(result)
    else:
        host = os.getenv('TEST_SERVICE_HOST', '0.0.0.0')
        port = os.getenv('TEST_SERVICE_PORT', '5003')
        port = int(port)
        app.run(host=host, port=port)
