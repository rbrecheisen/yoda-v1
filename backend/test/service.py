import os
import json
import requests
from flask import Flask, make_response
from flask_restful import Api, Resource

app = Flask(__name__)

if os.getenv('TEST_SERVICE_SETTINGS', None) is not None:
    app.config.from_envvar('TEST_SERVICE_SETTINGS')
else:
    pass


def test_auth_service():
    host = os.getenv('AUTH_SERVICE_HOST')
    port = os.getenv('AUTH_SERVICE_PORT')
    uri = 'http://{}:{}'.format(host, port)
    print(uri)
    response = requests.get(uri)
    result = 'SUCCESS' if response.status_code == 200 else 'FAIL'
    return {'test_auth_service': result}


def test_compute_service():
    host = os.getenv('COMPUTE_SERVICE_HOST')
    port = os.getenv('COMPUTE_SERVICE_PORT')
    uri = 'http://{}:{}'.format(host, port)
    print(uri)
    response = requests.get(uri)
    result = 'SUCCESS' if response.status_code == 200 else 'FAIL'
    return {'test_compute_service': result}


def test_storage_service():
    host = os.getenv('STORAGE_SERVICE_HOST')
    port = os.getenv('STORAGE_SERVICE_PORT')
    uri = 'http://{}:{}'.format(host, port)
    print(uri)
    response = requests.get(uri)
    result = 'SUCCESS' if response.status_code == 200 else 'FAIL'
    return {'test_storage_service': result}


TESTS = [
    test_auth_service,
    test_compute_service,
    test_storage_service,
]


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
        results = []
        for test in TESTS:
            results.append(test())
        return results, 200


api = Api(app)
api.add_resource(RootResource, '/')
api.add_resource(TestsResource, '/tests')


@api.representation('application/json')
def output_json(data, code, headers=None):
    response = make_response(json.dumps(data), code)
    response.headers.extend(headers or {})
    return response


if __name__ == '__main__':
    host = os.getenv('TEST_SERVICE_HOST', '0.0.0.0')
    port = os.getenv('TEST_SERVICE_PORT', '5003')
    port = int(port)
    app.run(host=host, port=port)
