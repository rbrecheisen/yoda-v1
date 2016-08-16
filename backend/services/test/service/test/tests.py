import os
import base64
import requests
import logging

LOG = logging.getLogger(__name__)


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
        return {'message': 'auth: GET / failed'}
    response = requests.post('{}/tokens'.format(get_uri('auth')), headers=login_header('ralph', 'secret'))
    if response.status_code != 201:
        return {'message': 'auth: GET /tokens failed'}
    token = response.json()['token']
    response = requests.post('{}/token-checks'.format(get_uri('auth')), headers=token_header(token))
    if response.status_code != 201:
        return {'message': 'auth: GET /token-checks failed'}
    user = response.json()['user']
    if user['username'] != 'ralph':
        return {'message': 'auth: username != ralph'}
    return {'message': 'auth: OK'}


def test_compute_service():
    response = requests.get(get_uri('compute'))
    if response.status_code != 200:
        return {'message': 'compute: GET / failed'}
    return {'message': 'compute: OK'}


def test_storage_service():
    response = requests.get(get_uri('storage'))
    if response.status_code != 200:
        return {'message': 'storage: GET / failed'}
    return {'message': 'storage: OK'}


def test_storage_service_file_upload():

    # Request access token
    response = requests.post('{}/tokens'.format(get_uri('auth')), headers=login_header('ralph', 'secret'))
    if response.status_code != 201:
        return {'message': 'storage: GET /tokens failed'}
    token = response.json()['token']

    file_name = 'data.nii.gz'
    file_path = os.path.abspath('data') if os.getenv('TEST_SERVICE_HOST') == '0.0.0.0' else '/tmp'

    # Post file to storage service
    with open(os.path.join(file_path, file_name), 'rb') as f:
        headers = token_header(token)
        headers.update({'Content-Disposition': 'attachment; filename={}'.format(file_name)})
        response = requests.post('{}/files'.format(get_uri('storage')), headers=headers, data=f.read())
        if response.status_code != 201:
            return {'message': 'storage: POST /files failed'}
    return {'message': 'storage: OK'}


TESTS = [
    test_auth_service,
    test_compute_service,
    test_storage_service,
    test_storage_service_file_upload,
]
