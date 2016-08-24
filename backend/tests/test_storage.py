import os
import requests
from util import uri, read_chunks
from lib.util import generate_string
from lib.authentication import login_header, token_header


# --------------------------------------------------------------------------------------------------------------------
def test_root():
    response = requests.get(uri('storage'))
    assert response.status_code == 200
    pass


# --------------------------------------------------------------------------------------------------------------------
def get_file_type_scan_type_and_repository(token):

    response = requests.get(uri('storage', '/file-types?name=txt'), headers=token_header(token))
    assert response.status_code == 200
    file_type_id = response.json()[0]['id']

    response = requests.get(uri('storage', '/scan-types?name=none'), headers=token_header(token))
    assert response.status_code == 200
    scan_type_id = response.json()[0]['id']

    name = generate_string()
    response = requests.post(uri('storage', '/repositories'), json={'name': name}, headers=token_header(token))
    assert response.status_code == 201
    repository_id = response.json()['id']

    return file_type_id, scan_type_id, repository_id


# --------------------------------------------------------------------------------------------------------------------
def test_upload_file():

    if os.getenv('DATA_DIR', None) is None:
        return

    response = requests.post(uri('auth', '/tokens'), headers=login_header('ralph', 'secret'))
    assert response.status_code == 201
    token = response.json()['token']

    file_type_id, scan_type_id, repository_id = get_file_type_scan_type_and_repository(token)

    f_name = 'data.nii.gz'
    f_path = os.path.join(os.getenv('DATA_DIR'), f_name)
    session_id = None
    storage_id = None

    with open(f_path, 'rb') as f:
        i = 0
        j = 1
        n = os.path.getsize(f_path)
        for chunk in read_chunks(f, 1024*1024):
            content_length = len(chunk)
            content_range = 'bytes {}-{}/{}'.format(i, i + len(chunk) - 1, n)
            headers = token_header(token)
            headers.update({
                'Content-Length': '{}'.format(content_length),
                'Content-Type': 'application/octet-stream',
                'Content-Disposition': 'attachment; filename={}'.format(f_name),
                'X-Content-Range': content_range,
                'X-Session-ID': session_id,
                'X-File-Type': '{}'.format(file_type_id),
                'X-Scan-Type': '{}'.format(scan_type_id),
                'X-Repository-ID': '{}'.format(repository_id),
            })
            response = requests.post(uri('file', '/files'), headers=headers, data=chunk)
            if response.status_code == 201:
                assert 'id' in response.json()
                assert 'storage_id' in response.json()
                assert 'storage_path' in response.json()
                assert response.json()['name'] == f_name
                assert response.json()['size'] == n
                assert response.json()['repository'] == repository_id
                storage_id = response.json()['storage_id']
                break
            assert response.status_code == 202
            session_id = response.headers['X-Session-ID']
            i += len(chunk)
            j += 1

    response = requests.get(uri('file', '/downloads/{}'.format(storage_id)), headers=token_header(token))
    assert response.status_code == 200
    assert response.content

    with open('tmp.nii.gz', 'wb') as f:
        for chunk in response.iter_content(1024 * 1024):
            f.write(chunk)

    n = os.path.getsize('tmp.nii.gz')
    m = os.path.getsize(f_path)
    assert n == m

    os.system('rm -f tmp.nii.gz')
