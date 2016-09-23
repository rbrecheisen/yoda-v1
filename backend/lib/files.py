import os
import requests
from lib.util import uri
from lib.authentication import token_header


# --------------------------------------------------------------------------------------------------------------------
def read_chunks(file_obj, chunk_size):
    while True:
        byte_data = file_obj.read(chunk_size)
        if not byte_data:
            break
        yield byte_data


# --------------------------------------------------------------------------------------------------------------------
def upload_file(file_name, file_type_id, scan_type_id, repository_id, token):
    session_id = None
    file_id = None
    storage_id = None
    with open(file_name, 'rb') as f:
        i = 0
        n = os.path.getsize(file_name)
        chunk_size = int(n / 10)
        for chunk in read_chunks(f, chunk_size):
            content_length = len(chunk)
            content_range = 'bytes {}-{}/{}'.format(i, i + len(chunk) - 1, n)
            headers = token_header(token)
            headers.update({
                'Content-Length': '{}'.format(content_length),
                'Content-Type': 'application/octet-stream',
                'Content-Disposition': 'attachment; filename={}'.format(file_name),
                'X-Content-Range': content_range,
                'X-Session-ID': session_id,
                'X-File-Type': '{}'.format(file_type_id),
                'X-Scan-Type': '{}'.format(scan_type_id),
                'X-Repository-ID': '{}'.format(repository_id)})
            response = requests.post(uri('storage', '/files'), headers=headers, data=chunk)
            if response.status_code == 201:
                file_id = response.json()['id']
                storage_id = response.json()['storage_id']
                break
            if response.status_code != 202:
                raise RuntimeError('Response not 202 ({})'.format(response.status_code))
            session_id = response.headers['X-Session-ID']
            i += len(chunk)
    return file_id, storage_id


# --------------------------------------------------------------------------------------------------------------------
def download_file(storage_id, target_dir, token, extension=None):
    response = requests.get(
        uri('storage', '/downloads/{}'.format(storage_id)), headers=token_header(token))
    file_path = os.path.join(target_dir, storage_id)
    if extension:
        if not extension.startswith('.'):
            extension = '.{}'.format(extension)
        file_path = '{}{}'.format(file_path, extension)
    with open(file_path, 'wb') as f:
        for chunk in response.iter_content(1024 * 1024):
            f.write(chunk)
    return file_path
