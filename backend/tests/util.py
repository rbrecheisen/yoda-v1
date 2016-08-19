import os
import base64


def uri(service, path=''):
    if path.startswith(os.path.sep):
        path = path[1:]
    return 'http://{}:{}/{}'.format(
        os.getenv('{}_SERVICE_HOST'.format(service.upper())),
        os.getenv('{}_SERVICE_PORT'.format(service.upper())), path)


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
