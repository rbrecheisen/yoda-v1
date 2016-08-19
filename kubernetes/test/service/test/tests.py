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


def read_chunks(file_obj, chunk_size):
    while True:
        byte_data = file_obj.read(chunk_size)
        if not byte_data:
            break
        yield byte_data


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

    # Post chunked file to storage service
    session_id = None
    with open(os.path.join(file_path, file_name), 'rb') as f:
        i = 0
        n = os.path.getsize(os.path.join(file_path, file_name))
        for chunk in read_chunks(f, chunk_size=1024 * 1024):
            content_range = 'bytes {}-{}/{}'.format(i, i+len(chunk)-1, n)
            headers = token_header(token)
            headers.update({
                'Content-Length': str(len(chunk)),
                'Content-Type': 'application/octet-stream',
                'Content-Disposition': 'attachment; filename={}'.format(file_name),
                'X-Content-Range': content_range,
                'X-Session-ID': session_id,
            })
            response = requests.post('{}/files'.format(get_uri('storage')), headers=headers, data=chunk)
            if response.status_code == 201:
                break
            if response.status_code != 202:
                return {'message': 'storage: POST /files (chunked) failed'}
            session_id = response.headers['X-Session-ID']  # Get session ID and use it in subsequent requests
            i += len(chunk)

    return {'message': 'storage: OK'}


TESTS = [
    test_auth_service,
    test_compute_service,
    test_storage_service,
    test_storage_service_file_upload,
]
