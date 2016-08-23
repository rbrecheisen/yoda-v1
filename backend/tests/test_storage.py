import os
import requests
from util import uri, login_header, token_header, read_chunks


def test_root():
    response = requests.get(uri('storage'))
    assert response.status_code == 200


def test_upload_file():

    response = requests.post(uri('auth', '/tokens'), headers=login_header('ralph', 'secret'))
    assert response.status_code == 201
    token = response.json()['token']

    f_name = 'data.nii.gz'
    f_path = os.path.join(os.getenv('DATA_DIR', os.path.abspath('data')), f_name)
    session_id = None

    with open(f_path, 'rb') as f:
        i = 0
        j = 1
        n = os.path.getsize(f_path)
        for chunk in read_chunks(f, 1024*1024):
            content_length = len(chunk)
            content_range = 'bytes {}-{}/{}'.format(i, i + len(chunk) - 1, n)
            print('sending range {} (length {})'.format(content_range, content_length))
            headers = token_header(token)
            headers.update({
                'Content-Length': '{}'.format(content_length),
                'Content-Type': 'application/octet-stream',
                'Content-Disposition': 'attachment; filename={}'.format(f_name),
                'X-Content-Range': content_range,
                'X-Session-ID': session_id,
            })
            response = requests.post(uri('file', '/files'), headers=headers, data=chunk)
            if response.status_code == 201:
                break
            print('sent chunk {}'.format(j))
            assert response.status_code == 202
            session_id = response.headers['X-Session-ID']
            i += len(chunk)
            j += 1
