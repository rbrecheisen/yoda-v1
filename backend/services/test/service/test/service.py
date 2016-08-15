import os
import sys
import json
import base64
import requests
from flask import Flask, make_response
from flask_restful import Api, Resource

app = Flask(__name__)

if os.getenv('TEST_SERVICE_SETTINGS', None) is not None:
    app.config.from_envvar('TEST_SERVICE_SETTINGS')
else:
    pass

print(app.config)


def get_uri(service):
    return 'http://{}:{}'.format(
        os.getenv('{}_SERVICE_HOST'.format(service.upper())),
        os.getenv('{}_SERVICE_PORT'.format(service.upper())))


def login_header(username, password):
    return {'Authorization': 'Basic {}'.format(base64.b64encode('{}:{}'.format(username, password)))}


def token_header(token):
    return {'Authorization': 'Basic {}'.format(base64.b64encode('{}:unused'.format(token)))}


def test_auth_service():
    response = requests.get(get_uri('auth'))
    if response.status_code != 200:
        result = 'FAIL: {}'.format(response.json())
    else:
        result = 'SUCCESS'
    return {'test_auth_service': result}


def test_compute_service():
    response = requests.get(get_uri('compute'))
    if response.status_code != 200:
        result = 'FAIL: {}'.format(response.json())
    else:
        result = 'SUCCESS'
    return {'test_compute_service': result}


def test_storage_service():
    response = requests.get(get_uri('storage'))
    if response.status_code != 200:
        result = 'FAIL: {}'.format(response.json())
    else:
        result = 'SUCCESS'
    return {'test_storage_service': result}


def test_storage_service_file_upload():
    response = requests.post('{}/tokens'.format(get_uri('auth')), headers=login_header('ralph', 'secret'))
    if response.status_code != 201:
        result = 'FAIL: {}'.format(response.json())
    else:
        token = response.json()['token']
        response = requests.post('{}/files'.format(get_uri('storage')), headers=token_header(token))
        if response.status_code != 201:
            result = 'FAIL: {}'.format(response.json())
        else:
            result = 'SUCCESS'
    return {'test_storage_service_file_upload': result}


TESTS = [
    test_auth_service,
    test_compute_service,
    test_storage_service,
    test_storage_service_file_upload,
]


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
    init_env()
    if len(sys.argv) == 2 and sys.argv[1] == 'no-server':
        for result in run_tests():
            print(result)
    else:
        host = os.getenv('TEST_SERVICE_HOST')
        port = os.getenv('TEST_SERVICE_PORT')
        port = int(port)
        app.run(host=host, port=port)
